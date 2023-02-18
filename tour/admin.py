from django.contrib import admin
from .models import Tour, TourName, TourLocation

# Register your models here.

admin.site.register(Tour)
admin.site.register(TourName)
admin.site.register(TourLocation)
