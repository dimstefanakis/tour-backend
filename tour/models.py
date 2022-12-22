from django.db import models
from guide.models import Guide
from destination.models import Destination, Vessel

class Tour(models.Model):
    name = models.ForeignKey('TourName', on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    day = models.DateField()

    def __str__(self):
        return self.guide.name + ' - ' + self.destination.location.name + ' - ' + self.day.strftime('%m/%d/%Y')


class TourName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
