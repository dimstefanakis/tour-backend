# Generated by Django 4.1.4 on 2022-12-21 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0001_initial'),
        ('destination', '0001_initial'),
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='destination.destination'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='guide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guide.guide'),
        ),
    ]
