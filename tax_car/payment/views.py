from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from payment.models import PaymentTax
from payment.serializers import PaymentTaxSerializer
from car.serializers import *
from car.models import *

class PaymentTaxApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        List all PaymentTaxes or get a single PaymentTax by ID.
        """
        payment_tax_id = request.query_params.get('id', None)
        if payment_tax_id:
            try:
                payment_tax = PaymentTax.objects.get(id=payment_tax_id)
                serializer = PaymentTaxSerializer(payment_tax)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PaymentTax.DoesNotExist:
                return Response({'error': 'PaymentTax not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            payment_taxes = PaymentTax.objects.all()
            serializer = PaymentTaxSerializer(payment_taxes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new PaymentTax entry with Car, Plaque, and CarPlaque associations.
        """
        # Récupérer les données pour Car, Plaque et PaymentTax depuis la requête
        car_data = request.data.get("car")
        plaque_data = request.data.get("plaque")
        payment_tax_data = request.data.get("payment_tax")

        # Validation de la présence des données nécessaires
        if not car_data or not plaque_data or not payment_tax_data:
            return Response(
                {'error': 'Car, Plaque, and PaymentTax data are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 1. Création d'une nouvelle instance de Car
        car_serializer = CarSerializer(data=car_data)
        if car_serializer.is_valid():
            car_instance = car_serializer.save()
        else:
            return Response(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Création d'une nouvelle instance de Plaque
        plaque_serializer = PlaqueSerializer(data=plaque_data)
        if plaque_serializer.is_valid():
            plaque_instance = plaque_serializer.save()
        else:
            # Supprimer le véhicule si la création de la plaque échoue
            car_instance.delete()
            return Response(plaque_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. Création de l'association entre la voiture et la plaque dans CarPlaque
        car_plaque = CarPlaque(car=car_instance, plaque=plaque_instance)
        car_plaque.save()

        # 4. Création de l'instance PaymentTax avec les références nécessaires
        payment_tax_data["ref_car"] = car_instance.id  # Associer la voiture
        payment_tax_data["ref_perceptor"] = 1
        payment_tax_serializer = PaymentTaxSerializer(data=payment_tax_data)
        if payment_tax_serializer.is_valid():
            payment_tax_instance = payment_tax_serializer.save()
            return Response(payment_tax_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Supprimer les instances créées en cas d'erreur
            car_plaque.delete()
            plaque_instance.delete()
            car_instance.delete()
            return Response(payment_tax_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        Update an existing PaymentTax entry.
        """
        payment_tax_id = request.data.get('id', None)
        if payment_tax_id:
            try:
                payment_tax = PaymentTax.objects.get(id=payment_tax_id)
                serializer = PaymentTaxSerializer(payment_tax, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except PaymentTax.DoesNotExist:
                return Response({'error': 'PaymentTax not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'ID is required to update a record'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete a PaymentTax entry.
        """
        payment_tax_id = request.data.get('id', None)
        if payment_tax_id:
            try:
                payment_tax = PaymentTax.objects.get(id=payment_tax_id)
                payment_tax.delete()
                return Response({'message': 'PaymentTax deleted successfully'}, status=status.HTTP_200_OK)
            except PaymentTax.DoesNotExist:
                return Response({'error': 'PaymentTax not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'ID is required to delete a record'}, status=status.HTTP_400_BAD_REQUEST)