from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Renommer related names des relations ManyToManyField vers Group et Permission.
    groups = models.ManyToManyField('auth.Group', related_name='custom_users')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_users')

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    user_token=models.CharField(max_length=255,blank=True,null=True,unique=True)
    app_token=models.CharField(max_length=255,blank=True,null=True,unique=True)
    notification_token=models.CharField(max_length=255,blank=True,null=True,unique=True)
    otp=models.CharField(max_length=255,blank=True,null=True)
    reset_code=models.CharField(max_length=255,blank=True,null=True)
    phone=models.CharField(max_length=30,blank=True,null=True,unique=True)
    birthday=models.DateField(blank=True,null=True)
    sex_choices=(
        ('male','Male'),
        ('female','Female'),
        ('other','Other'),
    )
    sex=models.CharField(max_length=20,choices=sex_choices,blank=True,null=True)
    def  __str__(self):
        return self.user.username