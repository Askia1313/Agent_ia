"""
Configuration des URLs pour l'app Communication
Mappe les endpoints API aux fonctions views
"""

from django.urls import path
from . import views

# Namespace pour les URLs de l'app
app_name = 'communication'

urlpatterns = [
    # Endpoint pour poser une question
    # POST /api/question/
    path('question/', views.poser_question, name='poser_question'),
    
]
