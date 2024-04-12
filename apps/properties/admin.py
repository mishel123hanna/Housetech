from django.contrib import admin
from .models import *
# Register your models here.


class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'region']
    list_filter = ['city', 'region']

class PropertyAdmin(admin.ModelAdmin):
    list_display = ["user","title", "property_status", "property_type", "location"]
    list_filter = ["property_status", "property_type", "location__city", "location__region"]

    def location(self, obj):
        return obj.location

    location.short_description = "Location"

class PropertyImagesAdmin(admin.ModelAdmin):
    list_display = ['pkid','property', 'image']

admin.site.register(Location, LocationAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImages, PropertyImagesAdmin)
admin.site.register([PropertyViews])