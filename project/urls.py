from django.contrib import admin
from django.urls import path, include
from . import views
from .views import projet_add_api,get_projects,get_all_projects,media_projet,recup_projet




urlpatterns = [
    path('moi/ajoute_projet/', projet_add_api, name='projet_add_api'),
    path('moi/mes_projet/', get_projects, name='projet_my_api'),
    path('moi/all_projets/', get_all_projects, name='projet_all_my_api'),
    path('moi/media_projet/', media_projet, name='media_projet_my_api'),
    path('moi/recup_projet/', recup_projet, name='recup_projet_my_api'),
]