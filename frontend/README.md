# Application Frontend

Ceci est le frontend pour le projet Agent_ia, construit avec React, Vite, et TypeScript. Il fournit l'interface utilisateur pour interagir avec l'agent IA.

## Stack Technique

- **Framework**: [React](https://react.dev/)
- **Outil de Build**: [Vite](https://vitejs.dev/)
- **Langage**: [TypeScript](https://www.typescriptlang.org/)
- **Composants UI**: [shadcn/ui](https://ui.shadcn.com/)
- **Style**: [Tailwind CSS](https://tailwindcss.com/)
- **Client HTTP**: [Axios](https://axios-http.com/)
- **Routage**: [React Router](https://reactrouter.com/)
- **Gestion d'état**: [TanStack Query (React Query)](https://tanstack.com/query/latest)

## Structure du Projet

Le répertoire `src` contient le code source principal de l'application.

```
src/
├── assets/         # Fichiers statiques comme les images et les SVG
├── components/     # Composants UI réutilisables
│   ├── chat/       # Composants spécifiques à l'interface de chat
│   └── ui/         # Composants UI génériques de shadcn/ui
├── hooks/          # Hooks React personnalisés
├── lib/            # Fonctions utilitaires
├── pages/          # Composants de page de haut niveau
└── services/       # Définitions des services API pour la communication avec le backend
```

## Scripts Disponibles

### Installation

Pour installer les dépendances nécessaires, exécutez la commande suivante depuis le répertoire `frontend` :

```bash
npm install
```

### Serveur de Développement

Pour démarrer le serveur de développement local avec rechargement à chaud, exécutez :

```bash
npm run dev
```

L'application sera disponible à l'adresse `http://localhost:5173` par défaut (ou le prochain port disponible).

### Linting

Pour vérifier le code à la recherche de problèmes de linting, exécutez :

```bash
npm run lint
```

### Build de Production

Pour compiler l'application pour la production, exécutez :

```bash
npm run build
```

Cette commande transpile le code TypeScript et empaquette l'application dans le répertoire `dist`.

### Aperçu du Build de Production

Pour servir le build de production localement pour un aperçu, exécutez :

```bash
npm run preview
```

## Déploiement

Le frontend est configuré pour être déployé avec Docker. Les fichiers `Dockerfile` et `nginx.conf` sont configurés pour créer un conteneur prêt pour la production qui sert les fichiers statiques générés par Vite.