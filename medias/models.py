# Importer les modules nécessaires
from django.db import models
from django.contrib.auth.models import User

# Création du modèle pour les chaînes
class Chain(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type_choices = (('I', 'Image'), ('V', 'Video'), ('A', 'Audio'), ('D', 'Document'))
    type = models.CharField(max_length=1, choices=type_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_shared = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Modèle pour les médias
class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type_choices = (('I', 'Image'), ('V', 'Video'), ('A', 'Audio'), ('D', 'Document'))
    type = models.CharField(max_length=1, choices=type_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Modèle pour les abonnements utilisateur
class Subscription(models.Model):
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chain.name

# Modèle pour les chaînes filtrées
class Filter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_type_choices = (('A', 'All'), ('I', 'Image'), ('V', 'Video'), ('A', 'Audio'), ('D', 'Document'), ('F', 'Favorites'))
    media_type = models.CharField(max_length=1, choices=media_type_choices)
    popular_choices = (('P', 'Popular'), ('N', 'New'))
    popularity = models.CharField(max_length=1, choices=popular_choices, default='N')
    educational = models.BooleanField(default=False)
    funny = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Modèle pour la liste de chaînes de chaque utilisateur
class ChannelList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    chains = models.ManyToManyField(Chain, blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name