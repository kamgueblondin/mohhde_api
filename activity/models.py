from django.contrib.auth.models import User
from django.db import models
from community.models import Communaute

from medias.models import Chain


class Activite(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    nb_abonnes = models.IntegerField(default=0)
    objectif = models.CharField(max_length=255, null=True)
    contacts = models.ManyToManyField(User, related_name='activites')
    activee = models.BooleanField(default=False)
    chaine_mise_avant = models.ForeignKey(Chain, related_name='activites_mise_avant', on_delete=models.SET_NULL, null=True)
    chaine_couverture = models.ForeignKey(Chain, related_name='activites_couverture', on_delete=models.SET_NULL, null=True)
    chaine_media = models.ForeignKey(Chain, related_name='activites_media', on_delete=models.SET_NULL,null=True)
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE, null=True)

    
    
class Membre(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('moderateur', 'Modérateur'),
        ('invite', 'Invité'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    
    