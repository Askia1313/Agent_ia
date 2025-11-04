"""
Script de test et évaluation du système RAG
Teste 20 questions avec métriques de performance
"""

import requests
import time
import json
from typing import List, Dict, Tuple
from datetime import datetime
import statistics

# Configuration
API_URL = "http://localhost:8000/api/question/"
N_RESULTATS = 3

# Dataset de test : 20 questions avec réponses attendues
# Basé sur les procédures administratives réelles au Burkina Faso
TEST_DATASET = [
    {
        "id": 1,
        "question": "Comment obtenir un passeport au Burkina Faso ?",
        "mots_cles_attendus": ["passeport", "pièce", "identité", "photo", "demande", "délai"],
        "sources_pertinentes": ["passeport", "service-public", "mae.gov.bf"],
        "categorie": "Documents d'identité"
    },
    {
        "id": 2,
        "question": "Quelles sont les démarches pour obtenir une CNIB (Carte Nationale d'Identité Burkinabè) ?",
        "mots_cles_attendus": ["CNIB", "carte", "identité", "acte", "naissance", "photo", "empreintes"],
        "sources_pertinentes": ["cnib", "carte", "identite", "onea"],
        "categorie": "Documents d'identité"
    },
    {
        "id": 3,
        "question": "Comment obtenir un acte de mariage ?",
        "mots_cles_attendus": ["acte", "mariage", "mairie", "état civil", "copie", "extrait"],
        "sources_pertinentes": ["mariage", "acte", "etat-civil", "mairie"],
        "categorie": "État civil"
    },
    {
        "id": 4,
        "question": "Où et comment obtenir un acte de naissance ?",
        "mots_cles_attendus": ["acte", "naissance", "mairie", "état civil", "copie", "lieu"],
        "sources_pertinentes": ["acte", "naissance", "etat-civil", "mairie"],
        "categorie": "État civil"
    },
    {
        "id": 5,
        "question": "Quelles sont les conditions pour obtenir un permis de travail au Burkina Faso ?",
        "mots_cles_attendus": ["permis", "travail", "étranger", "autorisation", "emploi", "ministère"],
        "sources_pertinentes": ["permis", "travail", "fonction-publique", "emploi"],
        "categorie": "Travail et Emploi"
    },
    {
        "id": 6,
        "question": "Comment faire une demande de permis de construire ?",
        "mots_cles_attendus": ["permis", "construire", "construction", "plan", "autorisation", "mairie"],
        "sources_pertinentes": ["permis", "construire", "urbanisme", "matd"],
        "categorie": "Urbanisme"
    },
    {
        "id": 7,
        "question": "Comment faire légaliser un document ou une signature ?",
        "mots_cles_attendus": ["légalisation", "signature", "document", "mairie", "authentification", "tampon"],
        "sources_pertinentes": ["legalisation", "signature", "authentification", "mairie"],
        "categorie": "Documents administratifs"
    },
    {
        "id": 8,
        "question": "Quelles sont les démarches pour établir une procuration ?",
        "mots_cles_attendus": ["procuration", "mandat", "notaire", "signature", "représentation", "légalisation"],
        "sources_pertinentes": ["procuration", "notaire", "mandat", "justice"],
        "categorie": "Documents juridiques"
    },
    {
        "id": 9,
        "question": "Comment obtenir une licence de travail pour un étranger ?",
        "mots_cles_attendus": ["licence", "travail", "étranger", "carte", "séjour", "autorisation"],
        "sources_pertinentes": ["licence", "travail", "etranger", "fonction-publique"],
        "categorie": "Travail et Emploi"
    },
    {
        "id": 10,
        "question": "Quelles sont les conditions pour obtenir un visa de séjour au Burkina Faso ?",
        "mots_cles_attendus": ["visa", "séjour", "passeport", "carte", "résidence", "immigration"],
        "sources_pertinentes": ["visa", "sejour", "mae.gov.bf", "immigration"],
        "categorie": "Immigration"
    },
    {
        "id": 11,
        "question": "Comment obtenir un certificat de vie ?",
        "mots_cles_attendus": ["certificat", "vie", "mairie", "attestation", "vivant", "pensionné"],
        "sources_pertinentes": ["certificat", "vie", "mairie", "action-sociale"],
        "categorie": "Documents administratifs"
    },
    {
        "id": 12,
        "question": "Quelles sont les démarches pour obtenir un certificat de célibat ?",
        "mots_cles_attendus": ["certificat", "célibat", "mairie", "état civil", "non marié", "attestation"],
        "sources_pertinentes": ["certificat", "celibat", "etat-civil", "mairie"],
        "categorie": "État civil"
    },
    {
        "id": 13,
        "question": "Comment obtenir un certificat de décès ?",
        "mots_cles_attendus": ["certificat", "décès", "acte", "mort", "mairie", "état civil", "médecin"],
        "sources_pertinentes": ["certificat", "deces", "acte", "etat-civil"],
        "categorie": "État civil"
    },
    {
        "id": 14,
        "question": "Comment renouveler un passeport expiré ?",
        "mots_cles_attendus": ["renouveler", "passeport", "expiré", "ancien", "nouveau", "validité"],
        "sources_pertinentes": ["passeport", "renouvellement", "mae.gov.bf"],
        "categorie": "Documents d'identité"
    },
    {
        "id": 15,
        "question": "Quels documents sont nécessaires pour faire une déclaration de naissance ?",
        "mots_cles_attendus": ["déclaration", "naissance", "mairie", "délai", "certificat", "médical", "parents"],
        "sources_pertinentes": ["naissance", "declaration", "etat-civil", "mairie"],
        "categorie": "État civil"
    },
    {
        "id": 16,
        "question": "Comment obtenir un casier judiciaire au Burkina Faso ?",
        "mots_cles_attendus": ["casier", "judiciaire", "demande", "tribunal", "extrait", "bulletin"],
        "sources_pertinentes": ["casier-judiciaire", "ecasier", "justice"],
        "categorie": "Documents judiciaires"
    },
    {
        "id": 17,
        "question": "Quelles sont les étapes pour obtenir un certificat de nationalité burkinabè ?",
        "mots_cles_attendus": ["certificat", "nationalité", "burkinabè", "tribunal", "acte", "naissance"],
        "sources_pertinentes": ["certificat-nationalite", "nationalite", "ecertificat"],
        "categorie": "Documents d'identité"
    },
    {
        "id": 18,
        "question": "Comment faire une demande d'attestation de résidence ?",
        "mots_cles_attendus": ["attestation", "résidence", "domicile", "mairie", "justificatif", "adresse"],
        "sources_pertinentes": ["attestation", "residence", "domicile", "mairie"],
        "categorie": "Documents administratifs"
    },
    {
        "id": 19,
        "question": "Quels sont les documents requis pour un mariage civil au Burkina Faso ?",
        "mots_cles_attendus": ["mariage", "civil", "acte", "naissance", "certificat", "célibat", "mairie"],
        "sources_pertinentes": ["mariage", "civil", "etat-civil", "mairie"],
        "categorie": "État civil"
    },
    {
        "id": 20,
        "question": "Comment obtenir une carte de séjour pour étranger au Burkina Faso ?",
        "mots_cles_attendus": ["carte", "séjour", "étranger", "visa", "résidence", "immigration", "police"],
        "sources_pertinentes": ["carte", "sejour", "etranger", "immigration"],
        "categorie": "Immigration"
    }
]


class RAGTester:
    """Classe pour tester et évaluer le système RAG"""
    
    def __init__(self, api_url: str, n_resultats: int = 3):
        self.api_url = api_url
        self.n_resultats = n_resultats
        self.resultats = []
        
    def poser_question(self, question: str) -> Tuple[Dict, float]:
        """
        Pose une question à l'API et mesure le temps de réponse
        
        Returns:
            Tuple[Dict, float]: (réponse JSON, temps en secondes)
        """
        start_time = time.time()
        
        try:
            response = requests.post(
                self.api_url,
                json={
                    "question": question,
                    "n_resultats": self.n_resultats
                },
                timeout=30
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                return response.json(), elapsed_time
            else:
                return {"success": False, "error": f"Status {response.status_code}"}, elapsed_time
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {"success": False, "error": str(e)}, elapsed_time
    
    def evaluer_precision_retrieval(self, sources_obtenues: List, sources_pertinentes: List[str]) -> float:
        """
        Évalue la précision du retrieval
        
        Returns:
            float: Score de précision entre 0 et 1
        """
        if not sources_obtenues:
            return 0.0
        
        # Gérer les deux formats possibles : liste de dicts ou liste de strings
        sources_texte = []
        for s in sources_obtenues:
            if isinstance(s, dict):
                sources_texte.append(s.get('source', '').lower())
            elif isinstance(s, str):
                sources_texte.append(s.lower())
            else:
                sources_texte.append(str(s).lower())
        
        pertinents_trouves = 0
        for source_pertinente in sources_pertinentes:
            for source_obtenue in sources_texte:
                if source_pertinente.lower() in source_obtenue:
                    pertinents_trouves += 1
                    break
        
        return pertinents_trouves / len(sources_pertinentes) if sources_pertinentes else 0.0
    
    def evaluer_pertinence_reponse(self, reponse: str, mots_cles: List[str]) -> float:
        """
        Évalue la pertinence de la réponse (score sur 5)
        
        Returns:
            float: Score entre 0 et 5
        """
        if not reponse:
            return 0.0
        
        reponse_lower = reponse.lower()
        
        # Compter combien de mots-clés sont présents
        mots_trouves = sum(1 for mot in mots_cles if mot.lower() in reponse_lower)
        
        # Score basé sur le pourcentage de mots-clés trouvés
        pourcentage = mots_trouves / len(mots_cles) if mots_cles else 0
        
        # Bonus si la réponse est suffisamment longue (au moins 50 caractères)
        bonus_longueur = 0.5 if len(reponse) >= 50 else 0
        
        # Score sur 5
        score = (pourcentage * 4.5) + bonus_longueur
        
        return min(score, 5.0)
    
    def tester_question(self, test_case: Dict) -> Dict:
        """
        Teste une question et retourne les métriques
        
        Returns:
            Dict: Résultats du test avec métriques
        """
        print(f"\n{'='*80}")
        print(f"Test #{test_case['id']}: {test_case['categorie']}")
        print(f"Question: {test_case['question']}")
        print(f"{'='*80}")
        
        # Poser la question
        reponse, temps_reponse = self.poser_question(test_case['question'])
        
        if not reponse.get('success', False):
            print(f"❌ ERREUR: {reponse.get('error', 'Erreur inconnue')}")
            return {
                "id": test_case['id'],
                "question": test_case['question'],
                "categorie": test_case['categorie'],
                "succes": False,
                "erreur": reponse.get('error', 'Erreur inconnue'),
                "temps_reponse": temps_reponse,
                "precision_retrieval": 0.0,
                "pertinence_reponse": 0.0
            }
        
        # Extraire les données
        reponse_texte = reponse.get('reponse', '')
        sources = reponse.get('sources', [])
        
        # Calculer les métriques
        precision_retrieval = self.evaluer_precision_retrieval(
            sources,
            test_case['sources_pertinentes']
        )
        
        pertinence_reponse = self.evaluer_pertinence_reponse(
            reponse_texte,
            test_case['mots_cles_attendus']
        )
        
        # Afficher les résultats
        print(f"\n📊 MÉTRIQUES:")
        print(f"  ⏱️  Temps de réponse: {temps_reponse:.2f}s")
        print(f"  🎯 Précision Retrieval: {precision_retrieval*100:.1f}%")
        print(f"  ⭐ Pertinence Réponse: {pertinence_reponse:.1f}/5")
        
        print(f"\n💬 RÉPONSE ({len(reponse_texte)} caractères):")
        print(f"  {reponse_texte[:200]}{'...' if len(reponse_texte) > 200 else ''}")
        
        print(f"\n📚 SOURCES ({len(sources)}):")
        for i, source in enumerate(sources, 1):
            if isinstance(source, dict):
                print(f"  {i}. {source.get('source', 'N/A')} (distance: {source.get('distance', 0):.3f})")
            else:
                print(f"  {i}. {source}")
        
        return {
            "id": test_case['id'],
            "question": test_case['question'],
            "categorie": test_case['categorie'],
            "succes": True,
            "temps_reponse": temps_reponse,
            "precision_retrieval": precision_retrieval,
            "pertinence_reponse": pertinence_reponse,
            "reponse": reponse_texte,
            "sources": sources,
            "nb_sources": len(sources)
        }
    
    def executer_tests(self, dataset: List[Dict]) -> List[Dict]:
        """
        Exécute tous les tests du dataset
        
        Returns:
            List[Dict]: Liste des résultats
        """
        print(f"\n{'#'*80}")
        print(f"{'DÉBUT DES TESTS - SYSTÈME RAG':^80}")
        print(f"{'#'*80}")
        print(f"\nNombre de questions: {len(dataset)}")
        print(f"API URL: {self.api_url}")
        print(f"Nombre de résultats par question: {self.n_resultats}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        resultats = []
        
        for test_case in dataset:
            resultat = self.tester_question(test_case)
            resultats.append(resultat)
            
            # Petite pause entre les requêtes
            time.sleep(0.5)
        
        self.resultats = resultats
        return resultats
    
    def generer_rapport(self) -> Dict:
        """
        Génère un rapport statistique complet
        
        Returns:
            Dict: Rapport avec statistiques globales
        """
        if not self.resultats:
            return {"erreur": "Aucun résultat disponible"}
        
        # Filtrer les tests réussis
        tests_reussis = [r for r in self.resultats if r.get('succes', False)]
        nb_tests_reussis = len(tests_reussis)
        nb_tests_total = len(self.resultats)
        
        if not tests_reussis:
            return {
                "erreur": "Aucun test réussi",
                "taux_succes": 0.0,
                "nb_tests_total": nb_tests_total
            }
        
        # Calculer les statistiques
        temps_reponses = [r['temps_reponse'] for r in tests_reussis]
        precisions_retrieval = [r['precision_retrieval'] for r in tests_reussis]
        pertinences_reponses = [r['pertinence_reponse'] for r in tests_reussis]
        
        # Statistiques par catégorie
        categories = {}
        for r in tests_reussis:
            cat = r['categorie']
            if cat not in categories:
                categories[cat] = {
                    'count': 0,
                    'precision_retrieval': [],
                    'pertinence_reponse': [],
                    'temps_reponse': []
                }
            categories[cat]['count'] += 1
            categories[cat]['precision_retrieval'].append(r['precision_retrieval'])
            categories[cat]['pertinence_reponse'].append(r['pertinence_reponse'])
            categories[cat]['temps_reponse'].append(r['temps_reponse'])
        
        # Calculer les moyennes par catégorie
        stats_categories = {}
        for cat, data in categories.items():
            stats_categories[cat] = {
                'nombre_tests': data['count'],
                'precision_retrieval_moyenne': statistics.mean(data['precision_retrieval']) * 100,
                'pertinence_reponse_moyenne': statistics.mean(data['pertinence_reponse']),
                'temps_reponse_moyen': statistics.mean(data['temps_reponse'])
            }
        
        rapport = {
            "resume": {
                "nb_tests_total": nb_tests_total,
                "nb_tests_reussis": nb_tests_reussis,
                "nb_tests_echoues": nb_tests_total - nb_tests_reussis,
                "taux_succes": (nb_tests_reussis / nb_tests_total) * 100
            },
            "temps_reponse": {
                "moyenne": statistics.mean(temps_reponses),
                "mediane": statistics.median(temps_reponses),
                "min": min(temps_reponses),
                "max": max(temps_reponses),
                "ecart_type": statistics.stdev(temps_reponses) if len(temps_reponses) > 1 else 0
            },
            "precision_retrieval": {
                "moyenne": statistics.mean(precisions_retrieval) * 100,
                "mediane": statistics.median(precisions_retrieval) * 100,
                "min": min(precisions_retrieval) * 100,
                "max": max(precisions_retrieval) * 100,
                "ecart_type": statistics.stdev(precisions_retrieval) * 100 if len(precisions_retrieval) > 1 else 0
            },
            "pertinence_reponse": {
                "moyenne": statistics.mean(pertinences_reponses),
                "mediane": statistics.median(pertinences_reponses),
                "min": min(pertinences_reponses),
                "max": max(pertinences_reponses),
                "ecart_type": statistics.stdev(pertinences_reponses) if len(pertinences_reponses) > 1 else 0
            },
            "par_categorie": stats_categories
        }
        
        return rapport
    
    def afficher_rapport(self):
        """Affiche le rapport de manière formatée"""
        rapport = self.generer_rapport()
        
        if "erreur" in rapport:
            print(f"\n❌ ERREUR: {rapport['erreur']}")
            return
        
        print(f"\n\n{'#'*80}")
        print(f"{'RAPPORT DE TEST - SYSTÈME RAG':^80}")
        print(f"{'#'*80}")
        
        # Résumé
        print(f"\n📊 RÉSUMÉ")
        print(f"{'─'*80}")
        resume = rapport['resume']
        print(f"  Tests total:      {resume['nb_tests_total']}")
        print(f"  Tests réussis:    {resume['nb_tests_reussis']} ✅")
        print(f"  Tests échoués:    {resume['nb_tests_echoues']} ❌")
        print(f"  Taux de succès:   {resume['taux_succes']:.1f}%")
        
        # Temps de réponse
        print(f"\n⏱️  TEMPS DE RÉPONSE")
        print(f"{'─'*80}")
        temps = rapport['temps_reponse']
        print(f"  Moyenne:     {temps['moyenne']:.3f}s")
        print(f"  Médiane:     {temps['mediane']:.3f}s")
        print(f"  Min:         {temps['min']:.3f}s")
        print(f"  Max:         {temps['max']:.3f}s")
        print(f"  Écart-type:  {temps['ecart_type']:.3f}s")
        
        # Précision Retrieval
        print(f"\n🎯 PRÉCISION RETRIEVAL (% documents pertinents)")
        print(f"{'─'*80}")
        precision = rapport['precision_retrieval']
        print(f"  Moyenne:     {precision['moyenne']:.1f}%")
        print(f"  Médiane:     {precision['mediane']:.1f}%")
        print(f"  Min:         {precision['min']:.1f}%")
        print(f"  Max:         {precision['max']:.1f}%")
        print(f"  Écart-type:  {precision['ecart_type']:.1f}%")
        
        # Pertinence Réponse
        print(f"\n⭐ PERTINENCE RÉPONSE (score sur 5)")
        print(f"{'─'*80}")
        pertinence = rapport['pertinence_reponse']
        print(f"  Moyenne:     {pertinence['moyenne']:.2f}/5")
        print(f"  Médiane:     {pertinence['mediane']:.2f}/5")
        print(f"  Min:         {pertinence['min']:.2f}/5")
        print(f"  Max:         {pertinence['max']:.2f}/5")
        print(f"  Écart-type:  {pertinence['ecart_type']:.2f}")
        
        # Statistiques par catégorie
        print(f"\n📂 STATISTIQUES PAR CATÉGORIE")
        print(f"{'─'*80}")
        for cat, stats in rapport['par_categorie'].items():
            print(f"\n  {cat} ({stats['nombre_tests']} tests)")
            print(f"    Précision Retrieval: {stats['precision_retrieval_moyenne']:.1f}%")
            print(f"    Pertinence Réponse:  {stats['pertinence_reponse_moyenne']:.2f}/5")
            print(f"    Temps Réponse:       {stats['temps_reponse_moyen']:.3f}s")
        
        print(f"\n{'#'*80}\n")
    
    def sauvegarder_rapport(self, fichier: str = "rapport_test_rag.json"):
        """Sauvegarde le rapport en JSON"""
        rapport = {
            "date": datetime.now().isoformat(),
            "configuration": {
                "api_url": self.api_url,
                "n_resultats": self.n_resultats,
                "nb_tests": len(self.resultats)
            },
            "resultats_detailles": self.resultats,
            "statistiques": self.generer_rapport()
        }
        
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Rapport sauvegardé dans: {fichier}")


def main():
    """Fonction principale"""
    print("🤖 Test du système RAG - Agent IA")
    print("="*80)
    
    # Vérifier que l'API est accessible
    print("\n🔍 Vérification de l'API...")
    try:
        # Tester avec une requête simple
        response = requests.post(
            "http://localhost:8000/api/question/",
            json={"question": "test", "n_resultats": 1},
            timeout=5
        )
        if response.status_code in [200, 400]:  # 200 OK ou 400 Bad Request (mais serveur répond)
            print("✅ API accessible")
        else:
            print(f"⚠️  API répond avec le code: {response.status_code}")
            print("⚠️  Les tests vont continuer mais peuvent échouer...")
    except Exception as e:
        print(f"❌ Impossible de contacter l'API: {e}")
        print("\n💡 Assurez-vous que le backend Django est démarré:")
        print("   cd backend")
        print("   python manage.py runserver")
        print("\n⚠️  Voulez-vous continuer quand même? (O/N)")
        choix = input().strip().upper()
        if choix != "O":
            return
    
    # Créer le testeur
    tester = RAGTester(api_url=API_URL, n_resultats=N_RESULTATS)
    
    # Exécuter les tests
    resultats = tester.executer_tests(TEST_DATASET)
    
    # Afficher le rapport
    tester.afficher_rapport()
    
    # Sauvegarder le rapport
    tester.sauvegarder_rapport()
    
    print("\n✅ Tests terminés!")


if __name__ == "__main__":
    main()
