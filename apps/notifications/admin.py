from django.contrib import admin

from .models import FCMToken, Notification

# Register your models here.

admin.site.register([Notification, FCMToken])
