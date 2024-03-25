from django.contrib import admin
from .models import *
# Register your models here.

class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "city", "property_status", "property_type"]
    list_filter = ["property_status", "property_type", "city"]


admin.site.register(Property, PropertyAdmin)
admin.site.register([PropertyViews, PropertyPictures])