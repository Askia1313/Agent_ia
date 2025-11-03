# Étape 1: Construire l'application React
FROM node:22-alpine AS build

# Définir le répertoire de travail
WORKDIR /app

# Copier package.json et installer les dépendances
COPY package.json ./
RUN npm install

# Copier le reste des fichiers de l'application
COPY . ./

# Construire l'application pour la production
RUN npm run build

# Étape 2: Servir l'application avec Nginx
FROM nginx:stable-alpine

# Copier les fichiers construits de l'étape précédente
COPY --from=build /app/dist /usr/share/nginx/html

# Copier la configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Commande pour démarrer le serveur Nginx
CMD ["nginx", "-g", "daemon off;"]
