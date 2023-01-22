# Generated by Django 3.2.16 on 2023-01-16 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0001_initial'),
        ('tour', '0004_tour_supplementary_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='destination.location'),
        ),
    ]
