from rest_framework import serializers 
from .models import Property, PropertyViews, PropertyPictures

class PropertySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    property_photos = serializers.SerializerMethodField()
    # property_location = serializers.SerializerMethodField()


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
            "city",
            "region",
            "street",
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
            # "property_location",
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

    # def get_property_location(self,obj):
    #     city = obj.location.city
    #     region = obj.location.region
    #     street = obj.location.street
    #     property_location = Location.objects.filter
    #     return 
    
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

# class propertyLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = '__all__'