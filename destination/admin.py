from django.contrib import admin
from .models import Destination, Location, Vessel
# Register your models here.

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    filter_horizontal = ('tour_locations',)


admin.site.register(Destination)
admin.site.register(Location, LocationAdmin)
admin.site.register(Vessel)