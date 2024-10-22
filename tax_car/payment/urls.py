from django.urls import path
from payment.views import PaymentTaxApiView

urlpatterns = [
    path('api/payment-taxes/', PaymentTaxApiView.as_view(), name='payment-taxes'),
]