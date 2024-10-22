from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from car.serializers import CarCategorySerializer
from car.models import CarCategory


class CarCategoryApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the car categories for given requested user
        '''
        categories = CarCategory.objects.all()
        serializer = CarCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''
        Create the car category with given data
        '''
        data = {
            'label': request.data.get('label'), 
            'tax_amount': request.data.get('tax_amount')
        }
        serializer = CarCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarCategoryDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, category_id):
        '''
        Helper method to get the object with given category_id, and user_id
        '''
        try:
            return CarCategory.objects.get(id=category_id)
        except CarCategory.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, category_id, *args, **kwargs):
        '''
        Retrieves the categories with given category_id
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Category with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CarCategorySerializer(category_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, category_id, *args, **kwargs):
        '''
        Updates the category item with given category_id if exists
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Object with category id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = CarCategorySerializer(instance = category_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, category_id, *args, **kwargs):
        '''
        Deletes the category item with given category_id if exists
        '''
        category_instance = self.get_object(category_id, request.user.id)
        if not category_instance:
            return Response(
                {"res": "Object with category id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        category_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )