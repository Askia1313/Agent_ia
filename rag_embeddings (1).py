"""
Système RAG Complet pour Documents Administratifs
Avec modèle léger local (Ollama)
"""

# Installation requise:
# pip install sentence-transformers chromadb pypdf2 ollama langchain

import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import PyPDF2
from pathlib import Path
from typing import List, Dict
import ollama

class RAGSystemComplet:
    def __init__(self, 
                 embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                 llm_model="mistral:latest",
                 ollama_host=None):
        """
        Initialise le système RAG complet
        
        Args:
            embedding_model: Modèle pour embeddings
            llm_model: Modèle de génération (doit être installé dans Ollama)
            ollama_host: URL du serveur Ollama distant (ex: "http://192.168.1.100:11434")
                        Si None, utilise le serveur local
        """
        print(f"📥 Chargement du modèle d'embeddings: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Base de données vectorielle locale
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents_administratifs",
            metadata={"description": "Procédures administratives"}
        )
        
        # Configuration du modèle de langage distant
        self.llm_model = llm_model
        self.ollama_host = ollama_host
        
        if ollama_host:
            print(f"🌐 Connexion au serveur Ollama distant: {ollama_host}")
            self.ollama_client = ollama.Client(host=ollama_host)
        else:
            print(f"💻 Utilisation du serveur Ollama local")
            self.ollama_client = ollama.Client()
        
        # Vérifier la connexion et lister les modèles disponibles
        try:
            models = self.ollama_client.list()
            print(f"✅ Ollama connecté")
            print(f"\n📋 Modèles disponibles sur le serveur:")
            if 'models' in models:
                for model in models['models']:
                    # Gérer différents formats de réponse
                    if isinstance(model, dict):
                        model_name = model.get('name') or model.get('model') or str(model)
                    else:
                        model_name = str(model)
                    print(f"   - {model_name}")
            else:
                print(f"   Format de réponse: {models}")
            print(f"\n🎯 Modèle sélectionné: {llm_model}")
        except Exception as e:
            print(f"❌ Erreur lors de la liste des modèles: {e}")
            if ollama_host:
                print(f"   Vérifiez que le serveur distant est accessible à {ollama_host}")
            else:
                print("   Installez Ollama depuis: https://ollama.ai")
        
        print("✅ Système RAG initialisé")
    
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
        """Découpe le texte en chunks"""
        chunks = []
        debut = 0
        
        while debut < len(texte):
            fin = debut + taille_chunk
            chunk = texte[debut:fin]
            
            if fin < len(texte):
                dernier_point = chunk.rfind('.')
                if dernier_point > taille_chunk * 0.5:
                    chunk = chunk[:dernier_point + 1]
                    fin = debut + dernier_point + 1
            
            chunks.append(chunk.strip())
            debut = fin - overlap
        
        return chunks
    
    def traiter_dossier(self, chemin_dossier: str):
        """Traite tous les documents d'un dossier"""
        dossier = Path(chemin_dossier)
        documents_traites = 0
        
        print(f"\n📂 Traitement du dossier: {chemin_dossier}")
        
        for fichier in dossier.rglob('*'):
            if not fichier.is_file():
                continue
            
            try:
                if fichier.suffix.lower() == '.pdf':
                    print(f"  📄 Traitement PDF: {fichier.name}")
                    texte = self.lire_pdf(str(fichier))
                elif fichier.suffix.lower() in ['.txt', '.md']:
                    print(f"  📝 Traitement TXT: {fichier.name}")
                    texte = self.lire_txt(str(fichier))
                else:
                    continue
                
                chunks = self.decouper_texte(texte)
                print(f"    ✂️  {len(chunks)} chunks créés")
                
                embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
                
                ids = [f"{fichier.stem}_{i}" for i in range(len(chunks))]
                metadatas = [
                    {
                        "source": fichier.name,
                        "chunk_id": i,
                        "type": fichier.suffix
                    } for i in range(len(chunks))
                ]
                
                self.collection.add(
                    embeddings=embeddings.tolist(),
                    documents=chunks,
                    metadatas=metadatas,
                    ids=ids
                )
                
                documents_traites += 1
                print(f"    ✅ Embeddings créés et sauvegardés")
                
            except Exception as e:
                print(f"    ❌ Erreur: {e}")
        
        print(f"\n🎉 Traitement terminé: {documents_traites} documents traités")
        print(f"📊 Total dans la base: {self.collection.count()} chunks")
    
    def rechercher_contexte(self, question: str, n_resultats=3) -> List[Dict]:
        """Recherche les passages pertinents"""
        question_embedding = self.embedding_model.encode([question])[0]
        
        resultats = self.collection.query(
            query_embeddings=[question_embedding.tolist()],
            n_results=n_resultats
        )
        
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
        Génère une réponse complète avec le modèle léger
        
        Args:
            question: Question de l'utilisateur
            n_contextes: Nombre de passages à utiliser comme contexte
        
        Returns:
            Dict avec la réponse et les sources
        """
        print(f"\n🔍 Recherche de contexte pour: {question}")
        
        # 1. Rechercher les passages pertinents
        contextes = self.rechercher_contexte(question, n_resultats=n_contextes)
        
        if not contextes:
            return {
                'reponse': "Désolé, je n'ai pas trouvé d'information pertinente dans les documents.",
                'sources': []
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
            # 4. Générer avec Ollama (local ou distant)
            import time
            start_time = time.time()
            print(f"⏳ Envoi de la requête au serveur...")
            
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
            return {
                'reponse': f"Erreur lors de la génération: {e}",
                'sources': []
            }
    
    def conversation_interactive(self):
        """Mode conversation interactive"""
        print("\n" + "="*60)
        print("💬 MODE CONVERSATION INTERACTIVE")
        print("="*60)
        print("Tapez 'exit' ou 'quitter' pour sortir\n")
        
        while True:
            question = input("❓ Votre question: ").strip()
            
            if question.lower() in ['exit', 'quitter', 'quit']:
                print("\n👋 Au revoir!")
                break
            
            if not question:
                continue
            
            resultat = self.generer_reponse(question)
            
            print("\n" + "="*60)
            print("💡 RÉPONSE:")
            print("="*60)
            print(resultat['reponse'])
            
            if resultat['sources']:
                print("\n📚 Sources consultées:")
                for source in resultat['sources']:
                    print(f"  - {source}")
            
            print("\n" + "-"*60 + "\n")


# ============ EXEMPLE D'UTILISATION ============

if __name__ == "__main__":
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         SYSTÈME RAG - PROCÉDURES ADMINISTRATIVES          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 1. Initialiser le système avec serveur distant
    # Remplacez par l'IP/URL de votre machine distante
    rag = RAGSystemComplet(
        llm_model="mistral:latest",  # Utiliser le nom exact du modèle disponible
        ollama_host="http://localhost:11434"  # IP de la machine distante
    )
    
    # Pour serveur local, ne pas mettre ollama_host:
    # rag = RAGSystemComplet(llm_model="llama3.2:3b")
    
    # 2. Vérifier si la base contient des documents
    try:
        nb_documents = rag.collection.count()
        print(f"\n📊 Documents dans la base: {nb_documents} chunks")
        
        if nb_documents == 0:
            print("\n⚠️  La base de données semble vide!")
            print("💡 Si vous avez déjà chargé les documents avec 'agent ia.py',")
            print("   vérifiez que les deux scripts utilisent la même base de données.")
            print("\n🔍 Tentative de récupération des données...")
            # Essayer de lister les collections
            collections = rag.chroma_client.list_collections()
            print(f"📋 Collections disponibles: {[c.name for c in collections]}")
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification: {e}")
        nb_documents = 0
    
    # 3. Poser une question
    print("\n" + "="*60)
    print("🧪 TEST DE QUESTION")
    print("="*60)
    
    question = "comment obternir mon casier judiciare ?"
    resultat = rag.generer_reponse(question)
    
    print(f"\n❓ Question: {question}\n")
    print("💡 Réponse:")
    print(resultat['reponse'])
    
    if resultat['sources']:
        print("\n📚 Sources:")
        for source in resultat['sources']:
            print(f"  - {source}")
    
    # 4. Mode conversation interactive
    # Décommenter pour utiliser:
    # rag.conversation_interactive()
