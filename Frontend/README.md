# Frontend RAG Chat - Vue.js

Interface conversationnelle simple pour le système RAG avec stockage local des conversations.

## 🚀 Installation

### 1. Installer les dépendances
```bash
npm install
```

### 2. Démarrer le serveur de développement
```bash
npm run dev
```

L'app démarre sur `http://localhost:5173`

## 📋 Structure du projet

```
Frontend/
├── index.html           # Point d'entrée HTML
├── vite.config.js       # Configuration Vite
├── package.json         # Dépendances
├── src/
│   ├── main.js          # Point d'entrée Vue.js
│   ├── App.vue          # Composant principal (interface de chat)
│   └── services/
│       └── ragApi.js    # Service API (requêtes HTTP)
└── README.md
```

## ✨ Fonctionnalités

### 💬 Interface de Chat
- Interface conversationnelle simple et intuitive
- Messages de l'utilisateur et réponses de l'agent
- Affichage des résultats avec sources et scores
- Animation de chargement pendant les requêtes

### 💾 Stockage Local
- Toutes les conversations sont sauvegardées dans le `localStorage` du navigateur
- Les conversations persistent après fermeture du navigateur
- Aucune donnée n'est envoyée à un serveur externe

### 📥 Actions
- **Effacer**: Supprimer toutes les conversations
- **Télécharger**: Exporter les conversations en JSON

### 📱 Responsive
- Design adapté aux mobiles et tablettes
- Interface fluide sur tous les appareils

## 🔧 Configuration

### Changer l'URL de l'API
Si le backend n'est pas sur `localhost:8000`, modifiez `src/services/ragApi.js`:

```javascript
const API_BASE_URL = 'http://votre-url:port/api'
```

### Changer le port du frontend
Modifiez `vite.config.js`:

```javascript
server: {
  port: 3000,  // Votre port
  host: 'localhost'
}
```

## 📦 Build pour la production

```bash
npm run build
```

Les fichiers compilés seront dans le dossier `dist/`.

## 🐛 Dépannage

### Erreur CORS
Si vous avez une erreur CORS, vérifiez que:
1. Le backend Django est démarré
2. Le port du frontend est dans `CORS_ALLOWED_ORIGINS` du backend

### Erreur "Cannot find module"
Assurez-vous que les dépendances sont installées:
```bash
npm install
```

### L'API ne répond pas
Vérifiez que:
1. Le serveur Django est démarré: `python manage.py runserver`
2. L'URL de l'API est correcte dans `ragApi.js`
3. La base de données RAG est chargée: `python agent\ ia.py`

## 📚 Utilisation

1. **Démarrer le backend**: `python manage.py runserver`
2. **Démarrer le frontend**: `npm run dev`
3. **Ouvrir le navigateur**: `http://localhost:5173`
4. **Poser une question**: Tapez votre question et appuyez sur Entrée
5. **Voir les résultats**: Les passages pertinents s'affichent
6. **Gérer les conversations**: Utilisez les boutons Effacer/Télécharger

## 🎨 Personnalisation

### Couleurs
Modifiez les couleurs dans `App.vue`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Thème
Vous pouvez créer un thème clair/sombre en ajoutant des variables CSS.

## 📝 Notes

- Les conversations sont stockées en JSON dans le `localStorage`
- La limite de stockage est généralement 5-10 MB par domaine
- Pour un stockage plus important, utilisez IndexedDB
- Les données ne sont jamais envoyées au serveur (sauf les questions)

## 🔐 Sécurité

- Les questions sont envoyées au backend
- Les réponses ne sont pas stockées sur le serveur
- Aucune authentification requise pour le moment
- À implémenter en production
