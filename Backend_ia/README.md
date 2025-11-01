# Backend API RAG - Django

## Installation

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Préparer les données (depuis le dossier parent)
Avant de démarrer le serveur, assurez-vous que la base de données RAG est prête:

```bash
# Depuis le dossier "agent ia"
python agent_ia.py
```

Cela va:
- ✅ Charger tous les PDFs du dossier `./pdf`
- ✅ Scraper les URLs du fichier `urls.txt`
- ✅ Créer les embeddings et indexer tout dans ChromaDB

### 3. Démarrer le serveur Django
```bash
python manage.py runserver
```

Le serveur démarre sur `http://localhost:8000`

---

## Structure du projet

```
Backend_ia/
├── Backend_ia/              # Configuration Django
│   ├── settings.py          # Configuration (CORS, apps, etc.)
│   ├── urls.py              # Routage principal
│   ├── wsgi.py
│   └── asgi.py
├── Communication/           # App API RAG
│   ├── views.py             # Endpoints (3 fonctions)
│   ├── urls.py              # Routage des endpoints
│   ├── models.py
│   └── admin.py
├── manage.py
└── requirements.txt         # Dépendances Python
```

---

## Endpoints disponibles

### 1. Poser une question
```
POST /api/question/
```
Récupère les passages pertinents pour une question.

**Exemple:**
```bash
curl -X POST http://localhost:8000/api/question/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Comment obtenir un passeport ?", "n_resultats": 3}'
```

### 2. Vérifier le statut
```
GET /api/statut/
```
Retourne le nombre de chunks indexés.

**Exemple:**
```bash
curl http://localhost:8000/api/statut/
```

### 3. Health check
```
GET /api/health/
```
Vérifie que l'API fonctionne.

**Exemple:**
```bash
curl http://localhost:8000/api/health/
```

---

## Configuration CORS

Les ports suivants sont autorisés pour les requêtes du frontend:
- `localhost:3000` (Vue.js par défaut)
- `localhost:8080` (Vue.js alternatif)
- `localhost:5173` (Vite)

Pour ajouter d'autres ports, modifiez `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:VOTRE_PORT",
    "http://127.0.0.1:VOTRE_PORT",
]
```

---

## Dépannage

### Erreur: "No module named 'agent_ia'"
Assurez-vous que le fichier `agent ia.py` est dans le dossier parent:
```
agent ia/
├── Backend_ia/
├── agent ia.py          ← Doit être ici
└── urls.txt
```

### Erreur: "Base de données vide"
Exécutez d'abord `agent ia.py` pour charger les données:
```bash
python agent\ ia.py
```

### Erreur CORS
Vérifiez que `django-cors-headers` est installé:
```bash
pip install django-cors-headers
```

---

## Documentation complète

Voir `API_DOCUMENTATION.md` pour la documentation détaillée de tous les endpoints.
