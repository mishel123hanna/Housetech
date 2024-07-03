from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification, FCMToken
from .serializers import *

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class FCMTokenViewSet(viewsets.ModelViewSet):
#     queryset = FCMToken.objects.all()
#     serializer_class = FCMTokenSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)