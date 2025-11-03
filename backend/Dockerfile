# Utiliser une image Python officielle comme image de base
FROM python:3.13-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . /app/

# Exposer le port sur lequel l'application tourne
EXPOSE 8000

# Commande pour lancer l'application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
