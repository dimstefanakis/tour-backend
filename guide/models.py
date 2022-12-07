from django.db import models

class Guide(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class ResponseStatus(models.Model):
    day = models.DateField()
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    statuses = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('NA', 'Not Applicable'),
    )

    status = models.CharField(max_length=2, choices=statuses, default='NA')

    def __str__(self):
        return self.guide.name + ' - ' + self.day.strftime('%m/%d/%Y')
