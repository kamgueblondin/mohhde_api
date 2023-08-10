from rest_framework import generics
from .models import Annonce
from .serializers import AnnonceSerializer

class AnnonceListCreateView(generics.ListCreateAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer

class AnnonceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer