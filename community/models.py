# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Communaute(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    nombre_utilisateurs = models.IntegerField()
    objectif = models.TextField()
    contacts = models.TextField()
    est_active = models.BooleanField(default=False)

class Participant(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('moderateur', 'Modérateur'),
        ('invite', 'Invité'),
    )
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)