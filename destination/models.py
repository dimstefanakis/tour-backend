from django.db import models


class Vessel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Destination(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    eta = models.DateTimeField(blank=True, null=True)
    etd = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.vessel.name + ' - ' + self.location.name
