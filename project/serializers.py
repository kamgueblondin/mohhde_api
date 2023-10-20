from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Projet

class ProjetSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.proprietaire.username

    class Meta:
        model = Projet
        fields = ['id', 'titre', 'description', 'code_securite', 'cible', 'objectif', 'cout_total', 'nombre_cycles', 'echeance', 'proprietaire', 'utilise_fonds_physiques', 'chaine_mise_avant', 'chaine_couverture', 'chaine_media', 'date_creation', 'date_modification', 'username']