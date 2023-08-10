# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from audit.utils import create_audit, update_audit, delete_audit

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

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        user = User.objects.get(username='nom_utilisateur')  # Remplacez 'nom_utilisateur' par le nom d'utilisateur approprié
        if is_new:
            create_audit(self, user)
        else:
            update_audit(self, user)

    def delete(self, *args, **kwargs):
        user = User.objects.get(username='nom_utilisateur')  # Remplacez 'nom_utilisateur' par le nom d'utilisateur approprié
        delete_audit(self, user)
        super().delete(*args, **kwargs)