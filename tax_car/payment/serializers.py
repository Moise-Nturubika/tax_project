from rest_framework import serializers
from payment.models import PaymentTax

class PaymentTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTax
        fields = '__all__'