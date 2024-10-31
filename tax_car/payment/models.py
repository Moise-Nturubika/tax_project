from django.db import models
from car.models import Car
from perceptor.models import Perceptor
import uuid

class PaymentTax(models.Model):
    date_paiement = models.DateTimeField(db_column="date_paiement", auto_now_add=True)
    montant = models.FloatField(db_column="montant")
    # quittance_number = models.CharField(max_length=10, editable=False, unique=True, null=True, db_column="quittance_number")
    ref_car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, db_column="ref_car")
    ref_perceptor = models.ForeignKey(Perceptor, on_delete=models.DO_NOTHING, db_column="ref_perceptor")

    class Meta:
        db_table = 'tb_payment_tax'

    # def save(self, *args, **kwargs):
    #     if not self.quittance_number:
    #         unique_id = uuid.uuid4().int  # Generate a UUID-based integer
    #         self.quittance_number = f"{unique_id % 10**8:06d}"  # Get last 6 digits of UUID and format
    #     super(PaymentTax, self).save(*args, **kwargs)
