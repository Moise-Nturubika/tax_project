from rest_framework import serializers
from .models import PosteAttache, Perceptor, Utilisateur, Role, UserRole

class PosteAttacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosteAttache
        fields = '__all__'

class PerceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perceptor
        fields = '__all__'

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
