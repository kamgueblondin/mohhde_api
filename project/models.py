import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from medias.models import Chain

class Projet(models.Model):
    CHOIX_CIBLE = (
        ('amis', 'Amis'),
        ('communaute', 'Communauté'),
        ('activites', 'Activités'),
        ('tout_le_monde', 'Tous le monde')
    )
    
    titre = models.CharField(max_length=255)
    description = models.TextField()
    code_securite = models.CharField(max_length=255, blank=True, null=True)
    identifiant_unique = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cible = models.CharField(max_length=50, choices=CHOIX_CIBLE)
    objectif = models.DateField()
    cout_total = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_cycles = models.IntegerField()
    echeance = models.DateField()
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
    utilise_fonds_physiques = models.BooleanField(default=False)
    chaine_mise_avant = models.ForeignKey(Chain, related_name='projets_mise_avant', on_delete=models.SET_NULL, null=True)
    chaine_couverture = models.ForeignKey(Chain, related_name='projets_couverture', on_delete=models.SET_NULL, null=True)
    chaine_media = models.ForeignKey(Chain, related_name='projets_media', on_delete=models.SET_NULL,null=True)
    
class Etape(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='etapes')
    cycle = models.IntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
class SourceFinancement(models.Model):
    CHOIX_TYPE = (
        ('amis', 'Amis'),
        ('communaute', 'Communauté'),
        ('activites', 'Activités'),
        ('tout_le_monde', 'Tous le monde')
    )
    
    titre = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=CHOIX_TYPE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='sources_financement')

class GarantieFinancement(models.Model):
    source_financement = models.ForeignKey(SourceFinancement, on_delete=models.CASCADE, related_name='garanties')
    nombre_tranches = models.IntegerField()
    montant_tranche = models.DecimalField(max_digits=10, decimal_places=2)
    montant_souscrit = models.DecimalField(max_digits=10, decimal_places=2)
    remuneration = models.DecimalField(max_digits=10, decimal_places=2)

class Investisseur(models.Model):
    source_financement = models.ForeignKey(SourceFinancement, on_delete=models.CASCADE, related_name='investisseurs')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    taux_retour_investissement = models.DecimalField(max_digits=5, decimal_places=2)

class Souscription(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='souscriptions')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_tranches = models.IntegerField()

class Financement(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    source = models.CharField(max_length=20) 


class Commentaire(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

class Partage(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_partage = models.DateTimeField(auto_now_add=True)

class CleinOeilMohhde(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
