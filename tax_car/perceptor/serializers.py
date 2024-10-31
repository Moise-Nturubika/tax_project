from rest_framework import serializers
from .models import PosteAttache, Perceptor, Utilisateur, Role, UserRole

class PosteAttacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosteAttache
        fields = '__all__'

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PerceptorSerializer(serializers.ModelSerializer):
    poste = PosteAttacheSerializer(source='ref_poste', read_only=True)
    user = UtilisateurSerializer(source='utilisateur', read_only=True)

    class Meta:
        model = Perceptor
        fields = ['id', 'fullname', 'phone_number', 'ref_poste', 'poste', 'user']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
