from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MediaConfiguration
from .models import Chain, Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('title', 'description', 'type')

class ChainSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Chain
        fields = ('name', 'description', 'type', 'media')

class MediaConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaConfiguration
        fields = ('autoplay', 'loop')

class ChainSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Chain
        fields = ['id', 'name', 'description', 'type', 'user', 'is_system', 'is_active', 'is_shared']

class ChainDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    medias = serializers.StringRelatedField(many=True)

    class Meta:
        model = Chain
        fields = ['id', 'name', 'description', 'type', 'user', 'is_system', 'is_active', 'is_shared', 'medias']

class MediaSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    chain = ChainSerializer()

    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'type', 'user', 'chain', 'is_favorite']

class MediaDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    chain = ChainSerializer()

    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'type', 'user', 'chain', 'is_favorite']