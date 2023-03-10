# Generated by Django 3.2.16 on 2023-03-03 23:58

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0010_tourlocation_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='fee',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6),
        ),
    ]
