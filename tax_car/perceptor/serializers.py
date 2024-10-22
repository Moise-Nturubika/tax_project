from rest_framework import serializers
from perceptor.models import Perceptor, PosteAttache, Utilisateur, UserRole, Role

class PerceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perceptor
        fields = '__all__'



