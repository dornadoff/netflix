# Generated by Django 4.1.7 on 2023-03-17 12:03

import django.core.validators
from django.db import migrations, models
import film.models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aktyor',
            name='davlat',
            field=models.CharField(max_length=100, validators=[film.models.validate_davlat]),
        ),
        migrations.AlterField(
            model_name='tarif',
            name='narx',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(3)]),
        ),
    ]
