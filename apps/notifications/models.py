from django.db import models

from project import settings

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class FCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    device_type = models.CharField(
        max_length=10, choices=[("web", "Web"), ("android", "Android")]
    )
