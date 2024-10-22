from django.db import models


class PosteAttache(models.Model):
    designation = models.CharField(db_column="designation", max_length=50)
    localisation = models.CharField(db_column="localisation", max_length=100)

    class Meta:
        db_table = 'tb_poste_attache'

class Perceptor(models.Model):
    fullname = models.CharField(db_column="fullname", max_length=100)
    phone_number = models.CharField(db_column="phone_number", max_length=20)
    ref_poste = models.ForeignKey(PosteAttache, on_delete=models.DO_NOTHING, db_column="ref_poste")

    class Meta:
        db_table = 'tb_perceptor'

class Utilisateur(models.Model):
    password = models.CharField(db_column="password", max_length=255)
    ref_perceptor = models.ForeignKey(Perceptor, on_delete=models.DO_NOTHING, db_column="ref_perceptor")

    class Meta:
        db_table = 'tb_utilisateur'

class Role(models.Model):
    designation = models.CharField(db_column="designation", max_length=100)

    class Meta:
        db_table = 'tb_role'

class UserRole(models.Model):
    ref_user = models.ForeignKey(Utilisateur, on_delete=models.DO_NOTHING, db_column="ref_user")
    ref_role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, db_column="ref_role")

    class Meta:
        db_table = 'tb_user_role'

