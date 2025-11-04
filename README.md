# 🤖 Agent IA - Système RAG pour Procédures Administratives

Agent IA intelligent capable de répondre et de guider les utilisateurs dans les différentes démarches et procédures administratives au Burkina Faso. Le système utilise la technologie RAG (Retrieval-Augmented Generation) pour fournir des réponses précises basées sur des documents officiels et des sources web.

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Tests et Évaluation du Système RAG](#-tests-et-évaluation-du-système-rag)
- [Structure du projet](#-structure-du-projet)
- [Configuration](#-configuration)
- [Déploiement Docker](#-déploiement-docker)
- [Documentation](#-documentation)
- [Technologies utilisées](#-technologies-utilisées)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)

---

## 🎯 Vue d'ensemble

Ce projet est un système complet d'assistance administrative utilisant l'intelligence artificielle. Il combine :

- **Backend Django** : API REST pour le traitement des requêtes
- **Frontend React** : Interface utilisateur moderne et intuitive
- **Système RAG** : Recherche sémantique et génération de réponses contextuelles
- **ChromaDB** : Base de données vectorielle pour les embeddings
- **Ollama (Mistral)** : Modèle de langage pour la génération de réponses

### Cas d'usage

- ✅ Répondre aux questions sur les procédures administratives
- ✅ Guider les utilisateurs dans leurs démarches
- ✅ Fournir des informations précises avec sources
- ✅ Traiter des documents PDF et des pages web
- ✅ Recherche sémantique intelligente

---

## ✨ Fonctionnalités

### 🔍 Recherche Intelligente
- Recherche sémantique dans une base de documents vectorisés
- Support multilingue (français principalement)
- Résultats pertinents 

### 🤖 Génération de Réponses
- Réponses contextuelles générées par Ollama (Mistral)
- Citations des sources utilisées
- Réponses naturelles et précises

### 📄 Traitement de Documents
- Extraction de texte depuis des fichiers PDF
- Web scraping de pages officielles
- Découpage intelligent en chunks pour de meilleurs résultats

### 💬 Interface Utilisateur
- Interface de chat moderne et réactive
- Design responsive (mobile, tablette, desktop)
- Composants UI avec shadcn/ui


### 🔒 Sécurité et Performance
- CORS configuré pour la sécurité
- Cache et optimisations des requêtes

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     UTILISATEUR                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (React + Vite)                     │
│  - Interface de chat                                         │
│  - Composants UI (shadcn/ui)                                 │
│  - Gestion d'état (TanStack Query)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (Django API)                        │
│  - Endpoints REST                                            │
│  - Validation des requêtes                                   │
│  - Orchestration RAG                                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌────────────┐
│   ChromaDB   │ │  Ollama  │ │ Embeddings │
│  (Vectors)   │ │(Mistral) │ │   Model    │
└──────────────┘ └──────────┘ └────────────┘
```

### Flux de traitement

1. **Indexation** (une fois) :
   - Lecture des PDFs et scraping des URLs
   - Découpage en chunks
   - Création des embeddings
   - Stockage dans ChromaDB

2. **Requête utilisateur** :
   - L'utilisateur pose une question via le frontend
   - Le backend crée un embedding de la question
   - ChromaDB recherche les chunks les plus pertinents
   - Ollama génère une réponse basée sur le contexte
   - La réponse est retournée avec les sources

---

## 📦 Prérequis

### Logiciels requis

- **Python 3.11+** : Pour le backend Django
- **Node.js 18+** : Pour le frontend React
- **Ollama** : Serveur LLM local
- **Git** : Pour cloner le projet
- **Docker & Docker Compose** (optionnel) : Pour le déploiement

### Installation d'Ollama

```bash
# Télécharger depuis https://ollama.ai
# Puis installer le modèle Mistral

ollama pull mistral:latest

# Vérifier l'installation
ollama list
```

### Vérification des versions

```bash
# Python
python --version  # 3.11 ou supérieur

# Node.js
node --version    # 18 ou supérieur

# npm
npm --version     # 9 ou supérieur

# Ollama
ollama --version
```

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Askia1313/Agent_ia.git
cd Agent_ia
```

### 2. Configuration du Backend

```bash
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate
```

### 3. Configuration du Frontend

```bash
# Aller dans le dossier frontend
cd ../Frontend

# Installer les dépendances
npm install
```

### 4. Indexation des données



**Choisissez l'option appropriée dans le menu :**
- L'option 1 : Lancer le backend
- L'option 2 : Lancer le frontend
- L'option 3 : Lancer tout (backend + frontend)

**Note** : La base de données ChromaDB doit être préparée au préalable. Les documents PDF doivent être placés dans le dossier `./pdf` et les URLs dans le fichier `urls.txt`.

---

## 💻 Utilisation


**Menu interactif :**
```
📌 OPTIONS DE LANCEMENT
1 - Lancer le backend Django
2 - Lancer le frontend React
3 - Lancer tout (backend + frontend)
4 - Quitter
```

### Méthode 2 : Démarrage manuel

#### Démarrer le backend

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
python communication\agent_ia.py
python manage.py runserver
```

Le backend sera accessible sur **http://localhost:8000**

#### Démarrer le frontend

```bash
# Terminal 2 - Frontend
cd frontend
npm run dev
```

Le frontend sera accessible sur **http://localhost:5173**

#### Démarrer Ollama

```bash
# Terminal 3 - Ollama
ollama serve
```

### Tester l'application

1. Ouvrez votre navigateur sur **http://localhost:5173**
2. Posez une question dans l'interface de chat
3. L'agent IA vous répondra avec des sources

**Exemple de questions :**
- "Comment obtenir un passeport ?"
- "Quelles sont les démarches pour un certificat de nationalité ?"
- "Comment faire une demande de casier judiciaire ?"

---

## 🧪 Tests et Évaluation du Système RAG

Le projet inclut un script de test complet (`test_rag_system.py`) qui permet d'évaluer les performances du système RAG avec 20 questions de test couvrant différentes catégories de procédures administratives.

### Fonctionnalités du script de test

- **20 questions de test** couvrant 6 catégories :
  - Documents d'identité (passeport, CNIB, certificat de nationalité)
  - État civil (acte de naissance, mariage, décès)
  - Travail et Emploi (permis de travail, licence)
  - Immigration (visa, carte de séjour)
  - Documents administratifs (légalisation, attestation)
  - Documents judiciaires (casier judiciaire)

- **Métriques de performance** :
  - ⏱️ Temps de réponse (moyenne, médiane, min, max)
  - 🎯 Précision du retrieval (% de documents pertinents trouvés)
  - ⭐ Pertinence de la réponse (score sur 5)
  - 📊 Statistiques par catégorie

- **Rapport détaillé** :
  - Affichage console avec résultats en temps réel
  - Sauvegarde JSON du rapport complet
  - Statistiques globales et par catégorie

### Exécution des tests

#### Prérequis

Assurez-vous que le backend Django est démarré :

```bash
cd backend
python manage.py runserver
```

Le backend doit être accessible sur **http://localhost:8000**

#### Lancer les tests

```bash
# Depuis la racine du projet
python test_rag_system.py
```

Le script va :
1. Vérifier que l'API est accessible
2. Exécuter les 20 questions de test
3. Afficher les résultats en temps réel
4. Générer un rapport statistique complet
5. Sauvegarder le rapport dans `rapport_test_rag.json`

### Exemple de sortie

```
🤖 Test du système RAG - Agent IA
================================================================================

🔍 Vérification de l'API...
✅ API accessible

################################################################################
                    DÉBUT DES TESTS - SYSTÈME RAG
################################################################################

Nombre de questions: 20
API URL: http://localhost:8000/api/question/
Nombre de résultats par question: 3

================================================================================
Test #1: Documents d'identité
Question: Comment obtenir un passeport au Burkina Faso ?
================================================================================

📊 MÉTRIQUES:
  ⏱️  Temps de réponse: 2.34s
  🎯 Précision Retrieval: 66.7%
  ⭐ Pertinence Réponse: 4.2/5

💬 RÉPONSE (245 caractères):
  Pour obtenir un passeport au Burkina Faso, vous devez...

📚 SOURCES (3):
  1. passeport.pdf (distance: 0.123)
  2. mae.gov.bf (distance: 0.234)
  3. service-public.fr (distance: 0.345)

[... autres tests ...]

################################################################################
                    RAPPORT DE TEST - SYSTÈME RAG
################################################################################

📊 RÉSUMÉ
────────────────────────────────────────────────────────────────────────────────
  Tests total:      20
  Tests réussis:    20 ✅
  Tests échoués:    0 ❌
  Taux de succès:   100.0%

⏱️  TEMPS DE RÉPONSE
────────────────────────────────────────────────────────────────────────────────
  Moyenne:     2.145s
  Médiane:     2.089s
  Min:         1.234s
  Max:         3.456s

🎯 PRÉCISION RETRIEVAL (% documents pertinents)
────────────────────────────────────────────────────────────────────────────────
  Moyenne:     72.5%
  Médiane:     75.0%

⭐ PERTINENCE RÉPONSE (score sur 5)
────────────────────────────────────────────────────────────────────────────────
  Moyenne:     4.15/5
  Médiane:     4.20/5

✅ Tests terminés!
✅ Rapport sauvegardé dans: rapport_test_rag.json
```

### Interprétation des résultats

- **Temps de réponse** 
- **Précision Retrieval** 
- **Pertinence Réponse**

### Personnalisation des tests

Vous pouvez modifier le fichier `test_rag_system.py` pour :
- Ajouter de nouvelles questions dans `TEST_DATASET`
- Modifier le nombre de résultats : `N_RESULTATS = 3`
- Changer l'URL de l'API : `API_URL = "http://localhost:8000/api/question/"`

---

## 📁 Structure du projet

```
Agent_ia/
├── backend/                      # Backend Django
│   ├── backend_ia/              # Configuration Django
│   │   ├── settings.py          # Configuration (CORS, apps, BDD)
│   │   ├── urls.py              # Routage principal
│   │   ├── wsgi.py              # Point d'entrée WSGI
│   │   └── asgi.py              # Point d'entrée ASGI
│   │
│   ├── communication/           # Application API RAG
│   │   ├── views.py             # Endpoints API
│   │   ├── urls.py              # Routes API
│   │   ├── agent_ia.py          # Système RAG complet
│   │   └── migrations/          # Migrations Django
│   │
│   ├── manage.py                # CLI Django
│   ├── requirements.txt         # Dépendances Python
│   ├── Dockerfile               # Configuration Docker
│   └── README.md                # Documentation backend
│
├── frontend/                    # Frontend React
│   ├── src/
│   │   ├── components/          # Composants React
│   │   │   ├── chat/           # Composants de chat
│   │   │   └── ui/             # Composants UI (shadcn)
│   │   ├── pages/              # Pages de l'application
│   │   ├── services/           # Services API
│   │   ├── hooks/              # Hooks personnalisés
│   │   └── lib/                # Utilitaires
│   │
│   ├── public/                 # Fichiers statiques
│   ├── package.json            # Dépendances npm
│   ├── vite.config.ts          # Configuration Vite
│   ├── Dockerfile              # Configuration Docker
│   └── README.md               # Documentation frontend
│
├── pdf/                        # Documents PDF à indexer
├── chroma_db/                  # Base de données vectorielle
├── urls.txt                    # URLs à scraper
├── docker-compose.yml          # Configuration Docker Compose
├── test_rag_system.py          # Script de test et évaluation
└── README.md                   # Ce fichier
```

### Fichiers clés

- **`backend/communication/agent_ia.py`** : Cœur du système RAG
- **`backend/communication/views.py`** : Endpoints API
- **`frontend/src/services/`** : Communication avec l'API
- **`docker-compose.yml`** : Configuration des conteneurs

---

## ⚙️ Configuration

### Variables d'environnement Backend

Créez un fichier `.env` dans le dossier `backend/` :

```env
# Django
DEBUG=True
SECRET_KEY=votre-clé-secrète-django
ALLOWED_HOSTS=localhost,127.0.0.1

# Ollama
OLLAMA_HOST=http://localhost:11434

# ChromaDB
CHROMA_DB_PATH=../chroma_db
```

### Configuration CORS

Par défaut, le backend autorise les requêtes depuis :
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (React)
- `http://localhost:8080` (Vue.js alternatif)

Pour modifier, éditez `backend/backend_ia/settings.py` :

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://votre-domaine.com",
]
```

### Configuration Frontend

Le frontend se connecte au backend via `http://localhost:8000` par défaut.

Pour changer l'URL de l'API, modifiez `frontend/src/services/api.ts` :

```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

### Ajout de documents

#### PDFs

Placez vos fichiers PDF dans le dossier `pdf/` :

```bash
Agent_ia/
└── pdf/
    ├── passeport.pdf
    ├── carte_identite.pdf
    └── autres_documents.pdf
```

#### URLs

Ajoutez les URLs à scraper dans `urls.txt` :

```
https://www.service-public.fr/particuliers/vosdroits/F1341
https://ecertificat-nationalite.gov.bf/
https://ecasier-judiciaire.gov.bf/
```

Puis réindexez les données :

```bash
python launcher.py
# Choisir l'option de chargement des données
```

---

## 🐳 Déploiement Docker

### Démarrage avec Docker Compose

```bash
# Construire et démarrer tous les services
docker compose up --build

# En arrière-plan
docker compose up -d

# Voir les logs
docker compose logs -f

# Arrêter les services
docker compose down
```

### Services Docker

Le `docker-compose.yml` définit 3 services :

1. **backend** : API Django (port 8000)
2. **frontend** : Application React (port 80)
3. **chroma** : Base de données ChromaDB (port 8001)

### Accès aux services

- **Frontend** : http://localhost
- **Backend API** : http://localhost:8000
- **ChromaDB** : http://localhost:8001

### Configuration Docker

Les volumes suivants sont montés :

```yaml
volumes:
  - ./pdf:/app/pdf              # Documents PDF
  - ./chroma_db:/app/chroma_db  # Base vectorielle
```

**Important** : Assurez-vous qu'Ollama est installé sur la machine hôte et accessible via `http://host.docker.internal:11434`.

---

## 📚 Documentation

### Documentation détaillée

- **[Backend README](backend/README.md)** : Documentation complète du backend
- **[Frontend README](Frontend/README.md)** : Documentation du frontend
- **[API Documentation](API_DOCUMENTATION.md)** : Documentation des endpoints API

### API Endpoints

#### POST `/api/question/`

Pose une question au système RAG.

**Requête :**
```json
{
  "question": "Comment obtenir un passeport ?",
  "n_resultats": 3
}
```

**Réponse :**
```json
{
  "success": true,
  "question": "Comment obtenir un passeport ?",
  "reponse": "Pour obtenir un passeport...",
  "sources": [
    {
      "texte": "Extrait du document...",
      "source": "passeport.pdf",
      "distance": 0.1234
    }
  ]
}
```

Pour plus de détails, consultez [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

---

## 🛠️ Technologies utilisées

### Backend

| Technologie | Version | Description |
|------------|---------|-------------|
| Django | 5.2.6 | Framework web Python |
| Sentence Transformers | 5.1.2 | Modèles d'embeddings |
| ChromaDB | 1.3.0 | Base de données vectorielle |
| Ollama | 0.6.0 | Serveur LLM local |
| PyPDF2 | 3.0.1 | Extraction de texte PDF |
| BeautifulSoup4 | 4.12.2 | Web scraping |

### Frontend

| Technologie | Version | Description |
|------------|---------|-------------|
| React | 19.1.1 | Framework UI |
| Vite | 7.1.7 | Build tool |
| TypeScript | 5.9.3 | Typage statique |
| TailwindCSS | 4.1.16 | Framework CSS |
| shadcn/ui | - | Composants UI |
| TanStack Query | 5.90.6 | Gestion d'état |
| Axios | 1.13.1 | Client HTTP |

### Infrastructure

- **Docker** : Conteneurisation
- **Nginx** : Serveur web pour le frontend
- **ChromaDB** : Base vectorielle

---




## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

### Guidelines

- Suivez les conventions de code existantes
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation
- Assurez-vous que tous les tests passent

---





## 🔗 Liens utiles

- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation React](https://react.dev/)
- [Documentation Ollama](https://github.com/ollama/ollama)
- [Documentation ChromaDB](https://docs.trychroma.com/)
- [Documentation Sentence Transformers](https://www.sbert.net/)


