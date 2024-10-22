from django.db import models
from car.models import Car
from perceptor.models import Perceptor

class PaymentTax(models.Model):
    date_paiement = models.DateTimeField(db_column="date_paiement", auto_now_add=True)
    montant = models.FloatField(db_column="montant")
    ref_car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, db_column="ref_car")
    ref_perceptor = models.ForeignKey(Perceptor, on_delete=models.DO_NOTHING, db_column="ref_perceptor")

    class Meta:
        db_table = 'tb_payment_tax'

