from django.contrib.auth.models import User
from django.db import models


class Activite(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    nb_abonnes = models.IntegerField(default=0)
    objectif = models.CharField(max_length=255)
    contacts = models.ManyToManyField(User, related_name='activites')
    activee = models.BooleanField(default=False)


class Communaute(models.Model):
    participants = models.ManyToManyField(User, through='Membre')
    
    
class Membre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE)
    
    
    