from django.db import models

class CarCategory(models.Model):
    label = models.CharField(max_length=100, db_column="label")
    tax_amount = models.IntegerField(db_column="tax_amount")

    class Meta:
        db_table = 'tb_car_category'

class Car(models.Model):
    client_name = models.CharField(db_column="nom_client", max_length=100)
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, db_column="ref_category")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = 'tb_car'

class Plaque(models.Model):
    numero = models.CharField(db_column="numero", max_length=20)
    code_pays = models.CharField(db_column="code_pays", max_length=20)

    class Meta:
        db_table = 'tb_plaque'

class CarPlaque(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, db_column="ref_car")
    plaque = models.ForeignKey(Plaque, on_delete=models.DO_NOTHING, db_column="ref_plaque")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = 'tb_car_plaque'