from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from payment.models import PaymentTax
from payment.serializers import PaymentTaxSerializer

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
        Create a new PaymentTax entry.
        """
        serializer = PaymentTaxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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