from django.db import models
from django.contrib.auth.models import User

class Annonce(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    state = models.BooleanField(default=True)
    is_system = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
