#Serializer pour l'inscription :


from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers
from django.utils.crypto import get_random_string


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email','phone','sex','birthday')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        # Generate a random 60-digit code
        reset_code = get_random_string(length=60)
        profile=Profile.objects.create(
            user=user,
            phone=validated_data['phone'],
            birthday=validated_data['birthday'],
            sex=validated_data['sex'],
            user_token=reset_code

        )
        profile.save()
        return user

#Serializer pour la connexion :


from django.contrib.auth import authenticate
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password'],
        )
        if not user:
            raise serializers.ValidationError(
                'Invalid Credentials'
            )
        return attrs