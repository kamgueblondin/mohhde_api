from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_space = models.PositiveIntegerField(default=0)
    used_space = models.PositiveIntegerField(default=0)

class Element(models.Model):
    name = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)