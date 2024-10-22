# Generated by Django 5.1.2 on 2024-10-17 09:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='created_at', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_column='updated_at'),
        ),
        migrations.AddField(
            model_name='carplaque',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='created_at', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carplaque',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_column='updated_at'),
        ),
    ]
