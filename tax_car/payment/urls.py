from django.urls import path
from payment.views import PaymentTaxApiView

urlpatterns = [
    path('payment-taxes/', PaymentTaxApiView.as_view(), name='payment-taxes'),
]