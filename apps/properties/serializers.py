from rest_framework import serializers 
from .models import Property, PropertyViews, PropertyPictures, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'region', 'street']

class PropertySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    property_photos = serializers.SerializerMethodField()
    location = LocationSerializer()
    published_status = serializers.BooleanField(read_only=True)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
            "profile_photo",
            "title",
            "slug",
            "ref_code",
            "description",
            'location',
            "property_number",
            "price",
            "plot_area",
            "total_floors",
            "bedrooms",
            "bathrooms",
            "property_status",
            "property_type",
            "cover_photo",
            "published_status",
            "views",
            "property_photos",
        ]
    def get_user(self, obj):
        return obj.user.email
    
    def get_cover_photo(self, obj):
        return obj.cover_photo.url
    
    def get_profile_photo(self, obj):
        return obj.user.profile.profile_photo.url
    
    def get_property_photos(self, obj):
        # Retrieve property photos associated with this property
        property_photos = PropertyPictures.objects.filter(property_id=obj)
        # Serialize property photos data
        return PropertyPicturesSerializer(property_photos, many=True).data

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        property_instance = Property.objects.create(location=location, **validated_data)
        return property_instance
    
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location')
        location_serializer = LocationSerializer(instance.location, data=location_data)
        if location_serializer.is_valid():
            location_serializer.save()
        else:
            raise serializers.ValidationError(location_serializer.errors)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class PropertyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        exclude = ["updated_at", "pkid"]


class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ["updated_at", "pkid"]


class PropertyPicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPictures
        fields = ['property_id', 'image']  

