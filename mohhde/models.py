from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    user_token=models.CharField(max_length=255,blank=True,null=True,unique=True)
    app_token=models.CharField(max_length=255,blank=True,null=True,unique=True)
    notification_token=models.CharField(max_length=255,blank=True,null=True,unique=True)
    otp=models.CharField(max_length=255,blank=True,null=True)
    reset_code=models.CharField(max_length=255,blank=True,null=True)
    phone=models.CharField(max_length=30,blank=True,null=True,unique=True)
    email=models.EmailField(max_length=50,blank=True,null=True,unique=True)
    birthday=models.DateField(blank=True,null=True)
    sex_choices=(
        ('male','Male'),
        ('female','Female'),
        ('other','Other'),
    )
    sex=models.CharField(max_length=20,choices=sex_choices,blank=True,null=True)
    est_expert=models.BooleanField(default=False)
    def  __str__(self):
        return self.user.username