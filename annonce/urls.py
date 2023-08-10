from django.urls import path, include
from annonce.views import AnnonceListCreateView, AnnonceRetrieveUpdateDestroyView

urlpatterns = [
    # Autres URL de votre projet
    path('api/', include('annonces.urls'))
]

api_urlpatterns = [
    path('annonces/', AnnonceListCreateView.as_view(), name='annonce-list-create'),
    path('annonces/<int:pk>/', AnnonceRetrieveUpdateDestroyView.as_view(), name='annonce-retrieve-update-destroy')
]