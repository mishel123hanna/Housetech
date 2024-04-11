import logging

import django_filters
from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Property, PropertyViews, PropertyImages
from .pagination import PropertyPagination
from .serializers import (PropertyCreateSerializer, PropertySerializer,
                          PropertyViewSerializer, PropertyImagesSerializer)
from .permissions import IsOwnerOrReadOnly
logger = logging.getLogger(__name__)


class PropertyFilter(django_filters.FilterSet):

    property_status = django_filters.CharFilter(
        field_name="property_status", lookup_expr="iexact"
    )

    property_type = django_filters.CharFilter(
        field_name="property_type", lookup_expr="iexact"
    )

    price = django_filters.NumberFilter()
    price_gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price_lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")
    city = django_filters.CharFilter(field_name="location__city", lookup_expr='iexact')
    region = django_filters.CharFilter(field_name="location__region", lookup_expr="iexact")

    class Meta:
        model = Property
        fields = ["property_status", "property_type", "price"]


class ListAllPropertiesAPIView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = PropertyFilter
    # search_fields = ["city", "region"]
    ordering_fields = ["created_at"]

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def add_property(request):
    user = request.user
    data = request.data
    data["user"] = request.user.pkid
    serializer = PropertyCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"property {serializer.data.get('title')} created by {user.email}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyCreateAPIView(generics.CreateAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        property_instance = serializer.save(user=self.request.user)

        images_data = self.request.FILES.getlist('images')
        for image_data in images_data:
            PropertyImages.objects.create(property=property_instance, image=image_data)

class PropertyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'slug'

    def perform_update(self, serializer):
        property_instance = serializer.save(user=self.request.user)
        images_data = self.request.data.get('images', [])
        pkid = self.request.data.get('pkid')
        
        if pkid is not None:
            PropertyImages.objects.filter(property = property_instance, pkid=pkid).update(image=images_data)
        else:
            images_data = self.request.FILES.getlist('images')
            for image_data in images_data:
                PropertyImages.objects.create(property=property_instance, image=image_data)
            # PropertyImages.objects.filter(property = property_instance).create(image = images_data)
            # Handle the case if pkid is not provided
            # You may want to raise an error or handle this case differently based on your requirements
            pass
        # images_data = self.request.FILES.getlist('images')
        # for image_data in images_data:
        #     PropertyImages.objects.update(property=property_instance, image=image_data)


class PropertyImageDelete(generics.DestroyAPIView):
    serializer_class = PropertyImagesSerializer
    queryset = PropertyImages.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'pkid'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Image deleted successfully"}, status=status.HTTP_200_OK)