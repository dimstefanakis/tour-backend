# Generated by Django 3.2.16 on 2023-02-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0005_guide_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='guide',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
