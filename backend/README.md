# 🤖 Backend API RAG - Django

API REST Django pour un système RAG (Retrieval-Augmented Generation) avec ChromaDB et Ollama. Ce backend permet de traiter des documents PDF et des pages web, de créer des embeddings vectoriels, et de générer des réponses contextuelles aux questions des utilisateurs.

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Endpoints](#-api-endpoints)
- [Structure du projet](#-structure-du-projet)
- [Docker](#-docker)
- [Dépannage](#-dépannage)
- [Technologies utilisées](#-technologies-utilisées)

---

## ✨ Fonctionnalités

- **🔍 Recherche sémantique** : Recherche intelligente dans une base de documents vectorisés
- **🤖 Génération de réponses** : Utilisation d'Ollama (Mistral) pour générer des réponses contextuelles
- **📄 Traitement de documents** : Support des fichiers PDF et des pages web
- **💾 Base vectorielle** : ChromaDB pour le stockage et la recherche d'embeddings
- **🌐 API REST** : Endpoints Django pour l'intégration frontend
- **🔒 CORS configuré** : Prêt pour l'intégration avec des applications frontend
- **🐳 Docker ready** : Configuration Docker complète pour le déploiement

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Django API │─────▶│  ChromaDB   │
│  (Reac.js)   │◀─────│   (Backend)  │◀─────│  (Vectors)  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    Ollama    │
                     │  (Mistral)   │
                     └──────────────┘
```

**Flux de traitement :**
1. L'utilisateur pose une question via le frontend
2. Django reçoit la requête et crée un embedding de la question
3. ChromaDB recherche les documents les plus pertinents
4. Ollama génère une réponse basée sur le contexte trouvé
5. La réponse est retournée au frontend avec les sources

---

## 📦 Prérequis

### Logiciels requis

- **Python 3.11+** : Langage de programmation
- **Ollama** : Serveur LLM local (avec le modèle Mistral)
- **Git** : Pour cloner le projet
- **Docker** (optionnel) : Pour le déploiement conteneurisé

### Installation d'Ollama

```bash
# Windows / macOS / Linux
# Télécharger depuis https://ollama.ai

# Installer le modèle Mistral
ollama pull mistral:latest

# Vérifier l'installation
ollama list
```

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Askia1313/Agent_ia.git
cd "agent ia/backend"
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Préparer la base de données RAG

Avant de démarrer le serveur, vous devez  :

```bash
# Depuis le dossier parent "agent ia"
cd ..
python communication/agent_ia.py
```

Cela va :
- ✅ Charger tous les PDFs du dossier `./pdf`
- ✅ Scraper les URLs du fichier `urls.txt`
- ✅ Créer les embeddings avec Sentence Transformers
- ✅ Indexer tout dans ChromaDB (`./chroma_db`)

### 5. Appliquer les migrations Django

```bash
cd backend
python manage.py migrate
```

### 6. Démarrer le serveur

```bash
python manage.py runserver
```

Le serveur démarre sur **`http://localhost:8000`**

---

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du backend :

```env
# Configuration Django
DEBUG=True
SECRET_KEY=votre-clé-secrète-django
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration Ollama
OLLAMA_HOST=http://localhost:11434

# Configuration ChromaDB
CHROMA_DB_PATH=../chroma_db
```

### Configuration CORS

Les origines suivantes sont autorisées par défaut (voir `backend_ia/settings.py`) :

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React.js par défaut
    "http://localhost:8080",      # React.js alternatif
    "http://localhost:5173",      
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
]
```

Pour ajouter d'autres origines, modifiez cette liste dans `settings.py`.

### Configuration du modèle d'embeddings

Le modèle par défaut est `paraphrase-multilingual-mpnet-base-v2` (bon pour le français).

Pour changer le modèle, modifiez `communication/agent_ia.py` :

```python
RAGDocumentProcessor(
    model_name="sentence-transformers/autre-modele",
    llm_model="mistral:latest"
)
```

---

## 💻 Utilisation

### Démarrage rapide

```bash
# 1. Activer l'environnement virtuel
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# 2. Démarrer Ollama (dans un autre terminal)
ollama serve

# 3. Démarrer Django
python manage.py runserver
```

### Tester l'API

```bash
# Health check
curl http://localhost:8000/api/health/

# Poser une question
curl -X POST http://localhost:8000/api/question/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Comment obtenir un passeport ?", "n_resultats": 3}'
```

---


## 📁 Structure du projet

```
backend/
├── backend_ia/                 # Configuration Django
│   ├── __init__.py
│   ├── settings.py            # Configuration (CORS, apps, BDD)
│   ├── urls.py                # Routage principal
│   ├── wsgi.py                # Point d'entrée WSGI
│   └── asgi.py                # Point d'entrée ASGI
│
├── communication/             # Application API RAG
│   ├── __init__.py
│   ├── admin.py               # Interface admin Django
│   ├── apps.py                # Configuration de l'app
│   ├── models.py              # Modèles de données (vide pour l'instant)
│   ├── views.py               # Endpoints API (logique métier)
│   ├── urls.py                # Routage des endpoints
│   ├── agent_ia.py            # Système RAG (embeddings, ChromaDB, Ollama)
│   ├── tests.py               # Tests unitaires
│   └── migrations/            # Migrations de base de données
│
├── manage.py                  # Utilitaire Django CLI
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Configuration Docker
├── .dockerignore              # Fichiers exclus de Docker
└── README.md                  # Ce fichier
```

### Fichiers clés

- **`views.py`** : Contient la logique des endpoints API
- **`agent_ia.py`** : Système RAG complet (embeddings, recherche, génération)
- **`settings.py`** : Configuration Django (CORS, apps, base de données)
- **`urls.py`** : Définition des routes API

---

## 🐳 Docker

### Démarrage avec Docker Compose

Depuis le dossier parent `agent ia/` :

```bash
# Construire et démarrer tous les services
docker-compose up --build

# En arrière-plan
docker-compose up -d

# Arrêter les services
docker-compose down
```

### Services Docker

Le `docker-compose.yml` définit 3 services :

1. **backend** : API Django (port 8000)
2. **frontend** : Application Vue.js (port 80)
3. **chroma** : Base de données ChromaDB (port 8001)

### Configuration Docker

Le backend utilise les volumes suivants :

```yaml
volumes:
  - ./pdf:/app/pdf              # Documents PDF
  - ./chroma_db:/app/chroma_db  # Base de données vectorielle
```

**Variables d'environnement Docker :**

```yaml
environment:
  - OLLAMA_HOST=http://host.docker.internal:11434
  - DJANGO_SETTINGS_MODULE=backend_ia.settings
```

### Construire l'image Docker manuellement

```bash
# Depuis le dossier backend/
docker build -t backend-rag .

# Lancer le conteneur
docker run -p 8000:8000 \
  -v $(pwd)/../chroma_db:/app/chroma_db \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  backend-rag
```



## 🛠️ Technologies utilisées

### Backend

- **[Django 5.2.6](https://www.djangoproject.com/)** : Framework web Python
- **[django-cors-headers 4.3.1](https://github.com/adamchainz/django-cors-headers)** : Gestion CORS

### Système RAG

- **[Sentence Transformers 5.1.2](https://www.sbert.net/)** : Modèles d'embeddings multilingues
- **[ChromaDB 1.3.0](https://www.trychroma.com/)** : Base de données vectorielle
- **[Ollama 0.6.0](https://ollama.ai/)** : Serveur LLM local (Mistral)
- **[LangChain Text Splitters 1.0.0](https://python.langchain.com/)** : Découpage de texte

### Traitement de documents

- **[PyPDF2 3.0.1](https://pypdf2.readthedocs.io/)** : Extraction de texte PDF
- **[BeautifulSoup4 4.12.2](https://www.crummy.com/software/BeautifulSoup/)** : Web scraping
- **[Requests 2.31.0](https://requests.readthedocs.io/)** : Requêtes HTTP

### Utilitaires

- **[python-dotenv 1.0.0](https://github.com/theskumar/python-dotenv)** : Gestion des variables d'environnement

---

## 📚 Documentation supplémentaire

- **[API_DOCUMENTATION.md](../API_DOCUMENTATION.md)** : Documentation détaillée des endpoints
- **[Django Documentation](https://docs.djangoproject.com/)** : Documentation officielle Django
- **[ChromaDB Documentation](https://docs.trychroma.com/)** : Guide ChromaDB
- **[Ollama Documentation](https://github.com/ollama/ollama)** : Guide Ollama

---

## 📝 Notes de développement

### Modèle d'embeddings

Le modèle `paraphrase-multilingual-mpnet-base-v2` est optimisé pour :
- ✅ Texte multilingue (français, anglais, etc.)
- ✅ Recherche sémantique
- ✅ Performance sur CPU
- ✅ Taille raisonnable (~420 MB)

### Chunking des documents

Les documents sont découpés en chunks de :
- **Taille** : 500 caractères
- **Overlap** : 50 caractères
- **Raison** : Équilibre entre contexte et précision

### Génération de réponses

Le système utilise Ollama avec Mistral pour :
- Générer des réponses naturelles
- Citer les sources utilisées
- Rester fidèle au contexte fourni

---

## 🤝 Contribution

Pour contribuer au projet :

1. Forkez le repository
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

---



- [Documentation API complète](../API_DOCUMENTATION.md)
- [Frontend Vue.js](../Frontend/README.md)
- [Guide de déploiement](../DEPLOYMENT.md)

