"""
URL configuration for Backend_ia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # API endpoints pour le système RAG
    # Tous les endpoints commencent par /api/
    path('api/', include('communication.urls')),
]
