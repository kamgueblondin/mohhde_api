# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from medias.models import Chain

class Communaute(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    nombre_utilisateurs = models.IntegerField(default=0)
    objectif = models.TextField(null=True)
    contacts = models.TextField(null=True)
    est_active = models.BooleanField(default=False)
    chaine_mise_avant = models.ForeignKey(Chain, related_name='communaute_mise_avant', on_delete=models.SET_NULL, null=True)
    chaine_couverture = models.ForeignKey(Chain, related_name='communaute_couverture', on_delete=models.SET_NULL, null=True)
    chaine_media = models.ForeignKey(Chain, related_name='communaute_media', on_delete=models.SET_NULL,null=True)

class Participant(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('moderateur', 'Modérateur'),
        ('invite', 'Invité'),
    )
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)