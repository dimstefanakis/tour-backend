from django.contrib import admin
from .models import Destination, Location, Vessel
# Register your models here.

admin.site.register(Destination)
admin.site.register(Location)
admin.site.register(Vessel)
