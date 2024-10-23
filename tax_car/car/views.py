from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from car.serializers import CarCategorySerializer
from car.models import CarCategory
from car.utils import custom_response


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
        return custom_response(
            data=serializer.data, 
            message="Car categories retrieved successfully", 
            status=status.HTTP_200_OK
        )
    
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
            return custom_response(
                data=serializer.data, 
                message="Car category created successfully", 
                status=status.HTTP_201_CREATED
            )

        return custom_response(
            data=serializer.errors, 
            message="Car category creation failed", 
            status=status.HTTP_400_BAD_REQUEST
        )


class CarCategoryDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, category_id):
        '''
        Helper method to get the object with given category_id
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
            return custom_response(
                data=None,
                message="Category with given id does not exist",
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CarCategorySerializer(category_instance)
        return custom_response(
            data=serializer.data,
            message="Category retrieved successfully",
            status=status.HTTP_200_OK
        )

    # 4. Update
    def put(self, request, category_id, *args, **kwargs):
        '''
        Updates the category item with given category_id if it exists
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return custom_response(
                data=None,
                message="Object with given category id does not exist", 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'label': request.data.get('label'), 
            'tax_amount': request.data.get('tax_amount')
        }
        serializer = CarCategorySerializer(instance=category_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                data=serializer.data,
                message="Category updated successfully",
                status=status.HTTP_200_OK
            )
        return custom_response(
            data=serializer.errors,
            message="Failed to update category",
            status=status.HTTP_400_BAD_REQUEST
        )

    # 5. Delete
    def delete(self, request, category_id, *args, **kwargs):
        '''
        Deletes the category item with given category_id if exists
        '''
        category_instance = self.get_object(category_id)
        if not category_instance:
            return custom_response(
                data=None,
                message="Object with given category id does not exist", 
                status=status.HTTP_400_BAD_REQUEST
            )
        category_instance.delete()
        return custom_response(
            data=None,
            message="Category deleted successfully",
            status=status.HTTP_200_OK
        )
