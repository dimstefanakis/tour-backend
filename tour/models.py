from django.db import models
from guide.models import Guide
from destination.models import Destination, Vessel
from decimal import Decimal


class Tour(models.Model):
    name = models.ForeignKey('TourName', on_delete=models.CASCADE)
    guide = models.ForeignKey(
        Guide, on_delete=models.CASCADE, null=True, blank=True, related_name='tours')
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, null=True, blank=True)
    day = models.DateField()
    supplementary_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    def __str__(self):
        return self.guide.name + ' - ' + self.destination.location.name


class TourName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
