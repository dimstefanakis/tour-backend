from django.db import models
from decimal import Decimal
from destination.models import Location


class Guide(models.Model):
    email = models.EmailField(blank=True, default='')
    name = models.CharField(max_length=50, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=True, related_name='guides')
    fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    def __str__(self):
        return self.name


class ResponseStatus(models.Model):
    class STATUS(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
        NA = 'NA', 'Not Applicable'

    day = models.DateField()
    guide = models.ForeignKey(
        Guide, on_delete=models.CASCADE, related_name='responses')
    status = models.CharField(
        max_length=2, choices=STATUS.choices, default=STATUS.NA)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.guide.name + ' - ' + self.day.strftime('%m/%d/%Y')
