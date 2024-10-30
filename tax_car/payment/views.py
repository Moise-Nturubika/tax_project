from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from payment.models import PaymentTax
from payment.serializers import PaymentTaxSerializer
from car.serializers import *
from car.models import *
from car.utils import custom_response

class PaymentTaxApiView(APIView):
    def get(self, request, *args, **kwargs):
        payment_tax_id = request.query_params.get('id', None)
        if payment_tax_id:
            try:
                payment_tax = PaymentTax.objects.get(id=payment_tax_id)
                serializer = PaymentTaxSerializer(payment_tax)
                return custom_response("success", "PaymentTax retrieved successfully", serializer.data)
            except PaymentTax.DoesNotExist:
                return custom_response("error", "PaymentTax not found", status_code=status.HTTP_404_NOT_FOUND)
        else:
            payment_taxes = PaymentTax.objects.all()
            serializer = PaymentTaxSerializer(payment_taxes, many=True)
            return custom_response("success", "All PaymentTaxes retrieved successfully", serializer.data)

    def post(self, request, *args, **kwargs):
        car_data = request.data.get("car")
        plaque_data = request.data.get("plaques")  # Expecting a list of plaques
        payment_tax_data = request.data.get("payment_tax")

        if not car_data or not plaque_data or not payment_tax_data:
            return custom_response("error", "Car, Plaque, and PaymentTax data are required", status_code=status.HTTP_400_BAD_REQUEST)

        # Création de Car
        car_serializer = CarSerializer(data=car_data)
        if car_serializer.is_valid():
            car_instance = car_serializer.save()
        else:
            return custom_response("error", "Invalid Car data", errors=car_serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

        # Création de Plaque(s)
        plaques_instances = []
        for plaque in plaque_data[:2]:  # Maximum two plaques
            plaque_serializer = PlaqueSerializer(data=plaque)
            if plaque_serializer.is_valid():
                plaque_instance = plaque_serializer.save()
                plaques_instances.append(plaque_instance)
                CarPlaque.objects.create(car=car_instance, plaque=plaque_instance)
            else:
                # Supprimer le véhicule en cas d'échec de création de plaque
                car_instance.delete()
                return custom_response("error", "Invalid Plaque data", errors=plaque_serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

        # Création de PaymentTax
        payment_tax_data["ref_car"] = car_instance.id
        payment_tax_serializer = PaymentTaxSerializer(data=payment_tax_data)
        if payment_tax_serializer.is_valid():
            payment_tax_instance = payment_tax_serializer.save()
            return custom_response("success", "PaymentTax created successfully", payment_tax_serializer.data, status_code=status.HTTP_201_CREATED)
        else:
            # Nettoyer les enregistrements en cas d'erreur
            for plaque_instance in plaques_instances:
                CarPlaque.objects.filter(car=car_instance, plaque=plaque_instance).delete()
                plaque_instance.delete()
            car_instance.delete()
            return custom_response("error", "Invalid PaymentTax data", errors=payment_tax_serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        payment_tax_id = request.data.get('id', None)
        if payment_tax_id:
            try:
                payment_tax = PaymentTax.objects.get(id=payment_tax_id)
                serializer = PaymentTaxSerializer(payment_tax, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return custom_response("success", "PaymentTax updated successfully", serializer.data)
                return custom_response("error", "Invalid data", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            except PaymentTax.DoesNotExist:
                return custom_response("error", "PaymentTax not found", status_code=status.HTTP_404_NOT_FOUND)
        else:
            return custom_response("error", "ID is required to update a record", status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        payment_tax_id = request.data.get('id', None)
        if payment_tax_id:
            try:
                payment_tax = PaymentTax.objects.get(id=payment_tax_id)
                payment_tax.delete()
                return custom_response("success", "PaymentTax deleted successfully")
            except PaymentTax.DoesNotExist:
                return custom_response("error", "PaymentTax not found", status_code=status.HTTP_404_NOT_FOUND)
        else:
            return custom_response("error", "ID is required to delete a record", status_code=status.HTTP_400_BAD_REQUEST)