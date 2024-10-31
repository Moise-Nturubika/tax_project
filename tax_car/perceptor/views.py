from rest_framework import status
from .models import PosteAttache, Perceptor, Utilisateur, UserRole, Role
from .serializers import *
from car.utils import custom_response  # Import du modèle de réponse personnalisé
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password

# PosteAttache Views
class PosteAttacheListView(APIView):
    def get(self, request):
        categories = PosteAttache.objects.all()
        serializer = PosteAttacheSerializer(categories, many=True)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PosteAttacheSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="PosteAttache created", status=status.HTTP_201_CREATED)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

class PosteAttacheDetailView(APIView):
    def get_object(self, pk):
        try:
            return PosteAttache.objects.get(pk=pk)
        except PosteAttache.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return custom_response(errors="PosteAttache not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = PosteAttacheSerializer(category)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return custom_response(errors="PosteAttache not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = PosteAttacheSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="PosteAttache updated", status=status.HTTP_200_OK)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return custom_response(errors="PosteAttache not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return custom_response(data=None, message="PosteAttache deleted", status=status.HTTP_204_NO_CONTENT)

# Perceptor Views
class PerceptorListView(APIView):
    def get(self, request):
        perceptrs = Perceptor.objects.all()
        serializer = PerceptorSerializer(perceptrs, many=True)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a Perceptor and associated Utilisateur with hashed password.
        """
        perceptor_data = request.data.get("perceptor")
        password = request.data.get("password")

        if not perceptor_data or not password:
            return custom_response("error", "Perceptor data and password are required", status_code=status.HTTP_400_BAD_REQUEST)
        
        perceptor_serializer = PerceptorSerializer(data=perceptor_data)
        if perceptor_serializer.is_valid():
            perceptor_instance = perceptor_serializer.save()
            Utilisateur.objects.create(
                ref_perceptor=perceptor_instance,
                password=make_password(password)
            )
            return custom_response("success", "Perceptor and Utilisateur created successfully", perceptor_serializer.data, status_code=status.HTTP_201_CREATED)
        else:
            return custom_response("error", "Validation failed", errors=perceptor_serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class PerceptorDetailView(APIView):
    def get_object(self, pk):
        try:
            return Perceptor.objects.get(pk=pk)
        except Perceptor.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        """
        List all Perceptors with associated Utilisateur data.
        """
        perceptrors = Perceptor.objects.all()
        perceptor_data = PerceptorSerializer(perceptrors, many=True).data
        return custom_response("success", "Data fetched successfully", perceptor_data)


    def put(self, request, *args, **kwargs):
        """
        Update Perceptor and associated Utilisateur password.
        """
        perceptor_id = request.data.get("id")
        perceptor_data = request.data.get("perceptor")
        password = request.data.get("password")

        try:
            perceptor = Perceptor.objects.get(id=perceptor_id)
            perceptor_serializer = PerceptorSerializer(perceptor, data=perceptor_data, partial=True)
            if perceptor_serializer.is_valid():
                perceptor_instance = perceptor_serializer.save()
                if password:
                    utilisateur = Utilisateur.objects.get(ref_perceptor=perceptor_instance)
                    utilisateur.password = make_password(password)
                    utilisateur.save()
                return custom_response("success", "Perceptor updated successfully", perceptor_serializer.data)
            else:
                return custom_response("error", "Validation failed", errors=perceptor_serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except Perceptor.DoesNotExist:
            return custom_response("error", "Perceptor not found", status_code=status.HTTP_404_NOT_FOUND)


    def delete(self, request, *args, **kwargs):
        """
        Delete a Perceptor and its associated Utilisateur.
        """
        perceptor_id = request.data.get("id")
        try:
            perceptor = Perceptor.objects.get(id=perceptor_id)
            perceptor.delete()
            return custom_response("success", "Perceptor deleted successfully")
        except Perceptor.DoesNotExist:
            return custom_response("error", "Perceptor not found", status_code=status.HTTP_404_NOT_FOUND)

class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Authenticate user by phone number and password.
        """
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        try:
            perceptor = Perceptor.objects.get(phone_number=phone_number)
            utilisateur = Utilisateur.objects.get(ref_perceptor=perceptor)

            if check_password(password, utilisateur.password):
                return custom_response("success", "Login successful")
            else:
                return custom_response("error", "Incorrect password", status_code=status.HTTP_400_BAD_REQUEST)
        except (Perceptor.DoesNotExist, Utilisateur.DoesNotExist):
            return custom_response("error", "User not found", status_code=status.HTTP_404_NOT_FOUND)

# Utilisateur Views
class UtilisateurListView(APIView):
    def get(self, request):
        users = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(users, many=True)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="Utilisateur created", status=status.HTTP_201_CREATED)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

class UtilisateurDetailView(APIView):
    def get_object(self, pk):
        try:
            return Utilisateur.objects.get(pk=pk)
        except Utilisateur.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return custom_response(errors="Utilisateur not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = UtilisateurSerializer(user)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return custom_response(errors="Utilisateur not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = UtilisateurSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="Utilisateur updated", status=status.HTTP_200_OK)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return custom_response(errors="Utilisateur not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return custom_response(data=None, message="Utilisateur deleted", status=status.HTTP_204_NO_CONTENT)

# Role Views
class RoleListView(APIView):
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="Role created", status=status.HTTP_201_CREATED)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

class RoleDetailView(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return None

    def get(self, request, pk):
        role = self.get_object(pk)
        if role is None:
            return custom_response(errors="Role not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def put(self, request, pk):
        role = self.get_object(pk)
        if role is None:
            return custom_response(errors="Role not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="Role updated", status=status.HTTP_200_OK)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        if role is None:
            return custom_response(errors="Role not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        role.delete()
        return custom_response(data=None, message="Role deleted", status=status.HTTP_204_NO_CONTENT)

# UserRole Views
class UserRoleListView(APIView):
    def get(self, request):
        user_roles = UserRole.objects.all()
        serializer = UserRoleSerializer(user_roles, many=True)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="UserRole created", status=status.HTTP_201_CREATED)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

class UserRoleDetailView(APIView):
    def get_object(self, pk):
        try:
            return UserRole.objects.get(pk=pk)
        except UserRole.DoesNotExist:
            return None

    def get(self, request, pk):
        user_role = self.get_object(pk)
        if user_role is None:
            return custom_response(errors="UserRole not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = UserRoleSerializer(user_role)
        return custom_response(data=serializer.data, message="Success", status=status.HTTP_200_OK)

    def put(self, request, pk):
        user_role = self.get_object(pk)
        if user_role is None:
            return custom_response(errors="UserRole not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        serializer = UserRoleSerializer(user_role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(data=serializer.data, message="UserRole updated", status=status.HTTP_200_OK)
        return custom_response(errors=serializer.errors, message="Invalid data", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_role = self.get_object(pk)
        if user_role is None:
            return custom_response(errors="UserRole not found", message="Error", status=status.HTTP_404_NOT_FOUND)
        user_role.delete()
        return custom_response(data=None, message="UserRole deleted", status=status.HTTP_204_NO_CONTENT)