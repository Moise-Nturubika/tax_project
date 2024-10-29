from rest_framework import serializers
from car.models import CarCategory, Car, Plaque

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'client_name', 'category', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PlaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plaque
        fields = ['id', 'numero', 'code_pays']



