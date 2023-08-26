from django.urls import path, include
from rest_framework.routers import DefaultRouter
from annonce.views import AnnonceListCreateView, AnnonceRetrieveUpdateDestroyView, get_system_active_announcement

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('annonces/', AnnonceListCreateView.as_view(), name='annonce-list-create'),
    path('annonces/<int:pk>/', AnnonceRetrieveUpdateDestroyView.as_view(), name='annonce-retrieve-update-destroy'),
    path('annonces/systeme/active/', get_system_active_announcement),
]