from django.contrib import admin
from django.urls import path, include
from . import views
from .views import projet_add_api




urlpatterns = [
    path('moi/ajoute_projet/', projet_add_api, name='projet_add_api'),
]