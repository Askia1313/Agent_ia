"""
Endpoints API pour le système RAG
Gère les requêtes de questions et retourne les réponses
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os
from pathlib import Path

# Ajouter le chemin parent pour importer agent_ia
base_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(base_dir))

from agent_ia import RAGDocumentProcessor

# Initialiser le système RAG une seule fois avec le chemin absolu vers la base de données
print("🚀 Initialisation du système RAG...")
print(f"📂 Répertoire de base: {base_dir}")

# Chemin absolu vers la base de données ChromaDB
db_path = os.path.join(base_dir, "chroma_db")
print(f"📂 Chemin de la base de données: {db_path}")

rag_system = RAGDocumentProcessor(db_path=db_path)
print("✅ Système RAG prêt\n")


@csrf_exempt
@require_http_methods(["POST"])
def poser_question(request):
    """
    Endpoint pour poser une question au système RAG
    
    Méthode: POST
    URL: /api/question/
    
    Corps de la requête (JSON):
    {
        "question": "Votre question ici",
        "n_resultats": 3  (optionnel, défaut: 3)
    }
    
    Réponse (JSON):
    {
        "success": true/false,
        "question": "Votre question",
        "resultats": [
            {
                "texte": "Passage pertinent",
                "source": "Nom du document ou URL",
                "distance": 0.1234
            }
        ],
        "message": "Message d'erreur si applicable"
    }
    """
    try:
        # Récupérer les données JSON de la requête
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        n_resultats = data.get('n_resultats', 3)
        
        # Valider la question
        if not question:
            return JsonResponse({
                'success': False,
                'message': 'La question ne peut pas être vide'
            }, status=400)
        
        # Valider n_resultats
        if not isinstance(n_resultats, int) or n_resultats < 1:
            n_resultats = 3
        
        # Générer une réponse complète avec Ollama
        print(f"🔍 Recherche pour: {question}")
        print(f"📊 Nombre de chunks dans la base: {rag_system.collection.count()}")
        
        # Utiliser generer_reponse au lieu de rechercher
        resultat = rag_system.generer_reponse(question, n_contextes=n_resultats)
        
        print(f"✅ Réponse générée avec {len(resultat.get('sources', []))} source(s)")
        
        # Formater la réponse
        return JsonResponse({
            'success': True,
            'question': question,
            'reponse': resultat['reponse'],
            'sources': resultat['sources'],
            'contextes': resultat.get('contextes_utilises', [])
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Format JSON invalide'
        }, status=400)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Erreur serveur: {str(e)}'
        }, status=500)


