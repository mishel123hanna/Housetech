# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, FCMTokenViewSet

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')
router.register(r'fcm-tokens', FCMTokenViewSet, basename='fcm-token')

urlpatterns = [
    path('', include(router.urls)),
]
