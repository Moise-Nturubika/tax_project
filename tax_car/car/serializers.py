from rest_framework import serializers
from car.models import CarCategory

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = '__all__'