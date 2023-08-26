from rest_framework import serializers
from .models import Stock, Element

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['total_space', 'used_space']

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ['name', 'size']