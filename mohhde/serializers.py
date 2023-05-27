#Serializer pour l'inscription :


from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(max_length=30, required=False)
    birthday = serializers.CharField(max_length=30, required=False)
    user_token = serializers.CharField(required=False)
    class Meta:
        model = Profile
        fields = ['id', 'phone', 'sex', 'birthday', 'email','user_token']