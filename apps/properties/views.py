import logging

from django.shortcuts import get_object_or_404
import django_filters
from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from .models import Property, PropertyViews, PropertyImages, UserPropertyFavorite
from .pagination import PropertyPagination
from .serializers import (PropertyCreateSerializer, PropertySerializer,
                          PropertyViewSerializer, PropertyImagesSerializer, UserPropertyFavoriteSerializer)
from .permissions import IsOwnerOrReadOnly, IsOwnerOfProperty
import threading
logger = logging.getLogger(__name__)


class PropertyFilter(django_filters.FilterSet):

    property_status = django_filters.CharFilter(
        field_name="property_status", lookup_expr="iexact"
    )
    rent_type = django_filters.CharFilter(
        field_name="rent_type", lookup_expr="iexact"
    )

    property_type = django_filters.CharFilter(
        field_name="property_type", lookup_expr="iexact"
    )
    total_rooms = django_filters.NumberFilter()
    furnishing = django_filters.CharFilter(field_name="furnishing", lookup_expr="exact")
    covering = django_filters.CharFilter(field_name="covering", lookup_expr="exact")
    solar_panels = django_filters.BooleanFilter()
    pool = django_filters.BooleanFilter()
    elevator = django_filters.BooleanFilter()

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
    permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

    def perform_create(self, serializer):
        property_instance = serializer.save(user=self.request.user)

        # images_data = self.request.FILES.getlist('images')
        # for image_data in images_data:
        #     PropertyImages.objects.create(property=property_instance, image=image_data)

class PropertyImagesCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOfProperty)
    serializer_class = PropertyImagesSerializer
    queryset = PropertyImages.objects.all()

    def create(self, request, *args, **kwargs):
        property_id = request.data.get('property_id')
        try:
            property_instance = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response(
                {"error": "Property not found."},
                status=status.HTTP_404_NOT_FOUND
            )


        images = request.FILES.getlist('image')

        if not images:
            return Response(
                {"error": "No images provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
     
        image_instances = []
        for image in images:          
            image_instance = PropertyImages(property=property_instance, image=image)
            image_instances.append(image_instance)

        
        PropertyImages.objects.bulk_create(image_instances)


        serializer = self.get_serializer(image_instances, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# upload images using threading

# class PropertyImagesCreateAPIView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated, IsOwnerOfProperty)
#     serializer_class = PropertyImagesSerializer
#     queryset = PropertyImages.objects.all()

#     def create(self, request, *args, **kwargs):
#         property_id = request.data.get('property_id')
#         try:
#             property_instance = Property.objects.get(id=property_id)
#         except Property.DoesNotExist:
#             return Response(
#                 {"error": "Property not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         images = request.FILES.getlist('image')
#         if not images:
#             return Response(
#                 {"error": "No images provided."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Read files into memory
#         image_files = []
#         for image in images:
#             image_files.append((image.name, image.read()))

#         # Start a thread to save image instances
#         threading.Thread(target=self.save_images, args=(property_instance, image_files)).start()

#         return Response({"message": "Images are being uploaded."}, status=status.HTTP_201_CREATED)

#     def save_images(self, property_instance, image_files):
#         image_instances = []
#         for name, content in image_files:
#             # Create an in-memory file object
#             from django.core.files.base import ContentFile
#             in_memory_file = ContentFile(content, name=name)

#             # Create an image instance with the provided property and in-memory file
#             image_instance = PropertyImages(property=property_instance, image=in_memory_file)
#             image_instance.save()
#             image_instances.append(image_instance)

class PropertyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'slug'

    def perform_update(self, serializer):
        property_instance = serializer.save(user=self.request.user)
        # images_data = self.request.data.get('images', [])
        # pkid = self.request.data.get('pkid')
        
        # if pkid is not None:
        #     PropertyImages.objects.filter(property = property_instance, pkid=pkid).update(image=images_data)
        # else:
        #     images_data = self.request.FILES.getlist('images')
        #     for image_data in images_data:
        #         PropertyImages.objects.create(property=property_instance, image=image_data)
        #     # PropertyImages.objects.filter(property = property_instance).create(image = images_data)
        #     # Handle the case if pkid is not provided
        #     # You may want to raise an error or handle this case differently based on your requirements
        #     pass
        # images_data = self.request.FILES.getlist('images')
        # for image_data in images_data:
        #     PropertyImages.objects.update(property=property_instance, image=image_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        if not PropertyViews.objects.filter(property=instance, ip=ip).exists():
            PropertyViews.objects.create(property=instance, ip=ip)
            instance.views += 1
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class PropertyImageDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = PropertyImagesSerializer
    queryset = PropertyImages.objects.all()
    lookup_field = 'pkid'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Image deleted successfully"}, status=status.HTTP_200_OK)
    
class UserProperties(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer

    def get_queryset(self):
            user = self.request.user
            return user.owner.all()  

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if queryset.exists():
            return super().list(request, *args, **kwargs)
        else:
            return Response({"success":False,"message": "No properties for user"}, status=status.HTTP_200_OK)

# from rest_framework.decorators import api_view, permission_classes

# @api_view(['GET'])
# def get_user_properties(request):
#     user = request.user
#     print(user)
#     properties = user.owner.all()
#     serializer = PropertySerializer(properties, many=True) 

#     return Response(serializer.data, status=status.HTTP_200_OK)


class UserPropertyFavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = UserPropertyFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPropertyFavorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        property_id = self.request.data.get('property_id')
        property_instance = get_object_or_404(Property, id=property_id)
        user = self.request.user
        if UserPropertyFavorite.objects.filter(user=user, property=property_instance).exists():
            raise ValidationError("You have already added this property to your favorites.")
        serializer.save(user=user, property=property_instance)

class UserPropertyFavoriteDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, format=None):
        property_id = self.request.data.get('property_id')
        print(f"property_id: {property_id}")
        print(f"t: {request.auth}")
        property_instance = Property.objects.get(id=property_id)
        favorite = get_object_or_404(UserPropertyFavorite, user=request.user, property=property_instance)
        favorite.delete()
        return Response(status=204)
    

# from django.urls import resolve
# from django.http import HttpResponse
# def debug_url_patterns(request):
#     match = resolve(request.path_info)
#     return HttpResponse(f"URL Name: {match.url_name}, View: {match.func.__name__}")
