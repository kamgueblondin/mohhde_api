from rest_framework import serializers
from .models import Projet

class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = ['titre', 'description', 'code_securite', 'cible', 'objectif', 'cout_total', 'nombre_cycles', 'echeance', 'proprietaire', 'utilise_fonds_physiques', 'chaine_mise_avant', 'chaine_couverture', 'chaine_media']