"""
Système RAG pour Documents Administratifs
Création d'embeddings et recherche sémantique
"""

# Installation requise (à exécuter une fois):
# pip install sentence-transformers chromadb pypdf langchain-text-splitters requests beautifulsoup4 ollama

import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import PyPDF2
from pathlib import Path
from typing import List, Dict
import json
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import time
import ollama

class RAGDocumentProcessor:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2", db_path=None, 
                 llm_model="mistral:latest", ollama_host=None):
        """
        Initialise le système RAG avec un modèle d'embeddings multilingue
        
        Args:
            model_name: Modèle pour créer les embeddings (bon en français)
            db_path: Chemin vers la base de données ChromaDB (défaut: ./chroma_db)
            llm_model: Modèle Ollama pour la génération (défaut: mistral:latest)
            ollama_host: URL du serveur Ollama (défaut: local)
        """
        print(f"📥 Chargement du modèle d'embeddings: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        # Base de données vectorielle locale
        # Si db_path n'est pas fourni, utiliser le chemin relatif
        if db_path is None:
            db_path = "./chroma_db"
        
        print(f"📂 Chemin de la base de données: {db_path}")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents_administratifs",
            metadata={"description": "Procédures administratives"}
        )
        
        # Afficher le nombre de documents dans la base
        count = self.collection.count()
        print(f"📊 {count} chunks dans la base de données")
        
        # Configuration Ollama pour la génération de réponses
        self.llm_model = llm_model
        self.ollama_host = ollama_host
        
        if ollama_host:
            print(f"🌐 Connexion au serveur Ollama distant: {ollama_host}")
            self.ollama_client = ollama.Client(host=ollama_host)
        else:
            print(f"💻 Utilisation du serveur Ollama local")
            self.ollama_client = ollama.Client()
        
        print(f"🤖 Modèle de génération: {llm_model}")
        print("✅ Système initialisé")
    
    def lire_pdf(self, chemin_pdf: str) -> str:
        """Extrait le texte d'un fichier PDF"""
        texte = ""
        with open(chemin_pdf, 'rb') as fichier:
            lecteur = PyPDF2.PdfReader(fichier)
            for page in lecteur.pages:
                texte += page.extract_text() + "\n"
        return texte
    
    def lire_txt(self, chemin_txt: str) -> str:
        """Lit un fichier texte"""
        with open(chemin_txt, 'r', encoding='utf-8') as f:
            return f.read()
    
    def decouper_texte(self, texte: str, taille_chunk=500, overlap=50) -> List[str]:
        """
        Découpe le texte en chunks (morceaux) pour de meilleurs embeddings
        
        Args:
            texte: Texte à découper
            taille_chunk: Nombre de caractères par chunk
            overlap: Chevauchement entre chunks
        """
        chunks = []
        debut = 0
        
        while debut < len(texte):
            fin = debut + taille_chunk
            chunk = texte[debut:fin]
            
            # Essayer de couper à la fin d'une phrase
            if fin < len(texte):
                dernier_point = chunk.rfind('.')
                if dernier_point > taille_chunk * 0.5:
                    chunk = chunk[:dernier_point + 1]
                    fin = debut + dernier_point + 1
            
            chunks.append(chunk.strip())
            debut = fin - overlap
        
        return chunks
    
    def traiter_dossier(self, chemin_dossier: str):
        """
        Traite tous les documents d'un dossier et crée les embeddings
        
        Args:
            chemin_dossier: Chemin vers le dossier contenant les documents
        """
        dossier = Path(chemin_dossier)
        documents_traites = 0
        
        print(f"\n📂 Traitement du dossier: {chemin_dossier}")
        
        for fichier in dossier.rglob('*'):
            if not fichier.is_file():
                continue
            
            try:
                # Lire selon le type de fichier
                if fichier.suffix.lower() == '.pdf':
                    print(f"  📄 Traitement PDF: {fichier.name}")
                    texte = self.lire_pdf(str(fichier))
                elif fichier.suffix.lower() in ['.txt', '.md']:
                    print(f"  📝 Traitement TXT: {fichier.name}")
                    texte = self.lire_txt(str(fichier))
                else:
                    continue
                
                # Découper en chunks
                chunks = self.decouper_texte(texte)
                print(f"    ✂️  {len(chunks)} chunks créés")
                
                # ============ ÉTAPE D'EMBEDDING COMMENTÉE ============
                # Cette étape est commentée pour l'instant car elle prend beaucoup de temps
                # Décommenter quand vous êtes prêt à créer les embeddings
                
                # # Créer les embeddings
                # embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
                # 
                # # Ajouter à la base vectorielle
                # ids = [f"{fichier.stem}_{i}" for i in range(len(chunks))]
                # metadatas = [
                #     {
                #         "source": fichier.name,
                #         "chunk_id": i,
                #         "type": fichier.suffix
                #     } for i in range(len(chunks))
                # ]
                # 
                # self.collection.add(
                #     embeddings=embeddings.tolist(),
                #     documents=chunks,
                #     metadatas=metadatas,
                #     ids=ids
                # )
                
                documents_traites += 1
                print(f"    ✅ Document traité (embeddings commentés)")
                
            except Exception as e:
                print(f"    ❌ Erreur: {e}")
        
        print(f"\n🎉 Traitement terminé: {documents_traites} documents traités")
        print(f"📊 Total d'éléments dans la base: {self.collection.count()}")
    
    def rechercher(self, question: str, n_resultats=3) -> List[Dict]:
        """
        Recherche les passages les plus pertinents pour une question
        
        Args:
            question: Question de l'utilisateur
            n_resultats: Nombre de résultats à retourner
        """
        # Créer l'embedding de la question
        question_embedding = self.embedding_model.encode([question])[0]
        
        # Rechercher dans la base vectorielle
        resultats = self.collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=n_resultats
        )
        
        # Formater les résultats
        passages = []
        for i in range(len(resultats['documents'][0])):
            passages.append({
                'texte': resultats['documents'][0][i],
                'source': resultats['metadatas'][0][i]['source'],
                'distance': resultats['distances'][0][i]
            })
        
        return passages
    
    def generer_reponse(self, question: str, n_contextes=3) -> Dict:
        """
        Génère une réponse complète avec Ollama en utilisant les passages pertinents
        
        Args:
            question: Question de l'utilisateur
            n_contextes: Nombre de passages à utiliser comme contexte
        
        Returns:
            Dict avec la réponse générée, les sources et les contextes utilisés
        """
        print(f"\n🔍 Recherche de contexte pour: {question}")
        
        # 1. Rechercher les passages pertinents
        contextes = self.rechercher(question, n_resultats=n_contextes)
        
        if not contextes:
            return {
                'reponse': "Désolé, je n'ai pas trouvé d'information pertinente dans les documents.",
                'sources': [],
                'contextes_utilises': []
            }
        
        # 2. Construire le contexte pour le LLM
        contexte_texte = "\n\n".join([
            f"[Source: {c['source']}]\n{c['texte']}" 
            for c in contextes
        ])
        
        # 3. Créer le prompt
        prompt = f"""Tu es un assistant spécialisé dans les procédures administratives. Réponds à la question en te basant UNIQUEMENT sur les informations fournies ci-dessous.

CONTEXTE DOCUMENTAIRE:
{contexte_texte}

QUESTION: {question}

INSTRUCTIONS:
- Réponds en français de manière claire et structurée
- Base-toi UNIQUEMENT sur les informations du contexte fourni
- Si l'information n'est pas dans le contexte, dis-le clairement
- Cite les sources entre crochets [Source: nom_document]
- Sois précis et concis

RÉPONSE:"""

        print(f"🤖 Génération de la réponse avec {self.llm_model}...")
        
        try:
            # 4. Générer avec Ollama
            start_time = time.time()
            print(f"⏳ Envoi de la requête au serveur Ollama...")
            
            response = self.ollama_client.generate(
                model=self.llm_model,
                prompt=prompt,
                options={
                    'temperature': 0.3,  # Réponses plus précises
                    'top_p': 0.9,
                    'num_predict': 500,  # Limiter la longueur de la réponse
                }
            )
            
            elapsed = time.time() - start_time
            print(f"✅ Réponse reçue en {elapsed:.1f}s")
            
            reponse_texte = response['response']
            
            # 5. Extraire les sources utilisées
            sources = list(set([c['source'] for c in contextes]))
            
            return {
                'reponse': reponse_texte,
                'sources': sources,
                'contextes_utilises': contextes
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return {
                'reponse': f"Erreur lors de la génération de la réponse: {str(e)}",
                'sources': [],
                'contextes_utilises': contextes
            }
    
    def verifier_robots_txt(self, url: str) -> bool:
        """
        Vérifie si le scraping est autorisé selon robots.txt
        
        Args:
            url: URL à vérifier
            
        Returns:
            True si le scraping est autorisé, False sinon
        """
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            robots_url = urljoin(base_url, "/robots.txt")
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            # Vérifier si l'accès est autorisé pour tous les user-agents
            can_fetch = rp.can_fetch("*", url)
            
            if can_fetch:
                print(f"  ✅ robots.txt: Scraping autorisé")
            else:
                print(f"  ⚠️  robots.txt: Scraping interdit")
            
            return can_fetch
            
        except Exception as e:
            print(f"  ⚠️  Impossible de vérifier robots.txt: {e}")
            # Par défaut, on autorise si on ne peut pas vérifier
            return True
    
    def scraper_url(self, url: str) -> str:
        """
        Scrape le contenu texte d'une URL
        
        Args:
            url: URL à scraper
            
        Returns:
            Texte extrait de la page
        """
        try:
            # Vérifier robots.txt
            if not self.verifier_robots_txt(url):
                print(f"  ❌ Scraping refusé par robots.txt")
                return ""
            
            # Récupérer la page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parser le HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Supprimer les scripts et styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extraire le texte
            texte = soup.get_text(separator='\n', strip=True)
            
            # Nettoyer les espaces excessifs
            texte = '\n'.join([ligne.strip() for ligne in texte.split('\n') if ligne.strip()])
            
            return texte
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Erreur lors du scraping: {e}")
            return ""
        except Exception as e:
            print(f"  ❌ Erreur inattendue: {e}")
            return ""
    
    def traiter_fichier_urls(self, chemin_fichier: str):
        """
        Traite un fichier texte contenant des URLs (une par ligne)
        Scrape chaque URL et ajoute le contenu à la base de données
        
        Args:
            chemin_fichier: Chemin vers le fichier .txt contenant les URLs
        """
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                urls = [ligne.strip() for ligne in f.readlines() if ligne.strip()]
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier: {e}")
            return
        
        if not urls:
            print(f"⚠️  Aucune URL trouvée dans {chemin_fichier}")
            return
        
        print(f"\n🌐 Scraping de {len(urls)} URL(s)...")
        urls_traitees = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\n  [{i}/{len(urls)}] Scraping: {url}")
            
            # Scraper le contenu
            texte = self.scraper_url(url)
            
            if not texte:
                print(f"    ⚠️  Aucun contenu extrait")
                continue
            
            # Découper en chunks
            chunks = self.decouper_texte(texte)
            print(f"    ✂️  {len(chunks)} chunks créés")
            
            # Créer les embeddings
            embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
            
            # Ajouter à la base vectorielle
            ids = [f"web_{urlparse(url).netloc}_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "source": url,
                    "chunk_id": i,
                    "type": "web"
                } for i in range(len(chunks))
            ]
            
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            urls_traitees += 1
            print(f"    ✅ Embeddings créés et sauvegardés")
            
            # Délai pour respecter le serveur
            time.sleep(1)
        
        print(f"\n🎉 Scraping terminé: {urls_traitees}/{len(urls)} URLs traitées")
        print(f"📊 Total d'éléments dans la base: {self.collection.count()}")


# ============ EXEMPLE D'UTILISATION ============

if __name__ == "__main__":
    # 1. Initialiser le système
    rag = RAGDocumentProcessor()
    
    # 2. Traiter les documents PDF
    print("\n" + "="*60)
    print("📄 ÉTAPE 1: TRAITEMENT DES PDF")
    print("="*60)
    rag.traiter_dossier("./pdf")
    
    # 3. Traiter les URLs depuis un fichier texte
    print("\n" + "="*60)
    print("🌐 ÉTAPE 2: SCRAPING WEB")
    print("="*60)
    # Créez un fichier "urls.txt" avec une URL par ligne
    if os.path.exists("./urls.txt"):
        rag.traiter_fichier_urls("./urls.txt")
    else:
        print("⚠️  Fichier './urls.txt' non trouvé")
        print("   Créez un fichier 'urls.txt' avec une URL par ligne")
    
    # 4. Tester la recherche
    print("\n" + "="*60)
    print("🔍 TEST DE RECHERCHE")
    print("="*60)
    
    question = "Comment obtenir un passeport ?"
    print(f"\n❓ Question: {question}\n")
    
    resultats = rag.rechercher(question, n_resultats=3)
    
    for i, resultat in enumerate(resultats, 1):
        print(f"Résultat {i}:")
        print(f"  Source: {resultat['source']}")
        print(f"  Score: {resultat['distance']:.4f}")
        print(f"  Extrait: {resultat['texte'][:200]}...")
        print()
