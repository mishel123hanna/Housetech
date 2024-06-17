from rest_framework import serializers 
from .models import Property, PropertyViews, PropertyImages, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'region', 'street']

class PropertyImagesSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = PropertyImages
        fields = ['pkid', 'image', 'property']

 
class PropertySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    # property_photos = serializers.SerializerMethodField()
    images = PropertyImagesSerializer(many=True, read_only=True)
    location = LocationSerializer()
    published_status = serializers.BooleanField(read_only=True)
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
            "user_type",
            "created_at",
            "updated_at",
            "profile_photo",
            "phone_number",
            "title",
            "slug",
            "ref_code",
            "description",
            'location',
            "property_number",
            "price",
            "plot_area",
            "total_floors",
            "floor_number",
            "bedrooms",
            "bathrooms",
            "kitchens",
            "living_rooms",
            "property_status",
            "property_type",
            "ownership_type",
            "covering",
            "elevator",
            "pool",
            "solar_panels",
            "furnishing",
            "direction",
            "total_rooms",
            "rent_type",
            "cover_photo",
            "published_status",
            "views",
            # "property_photos",
            "images",
        ]
    def get_user(self, obj):
        return obj.user.email
    
  
    def get_profile_photo(self, obj):
        return obj.user.profile.profile_photo.url
    
    def get_phone_number(self, obj):
        return obj.user.profile.phone_number
    # def get_property_photos(self, obj):
    #     # Retrieve property photos associated with this property
    #     property_photos = PropertyImages.objects.filter(property_id=obj)
    #     # Serialize property photos data
    #     return PropertyImagesSerializer(property_photos, many=True).data

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        property_instance = Property.objects.create(location=location, **validated_data)
        return property_instance
    
    def update(self, instance, validated_data):
        try:
            location_data = validated_data.pop('location')
            location_serializer = LocationSerializer(instance.location, data=location_data)
            if location_serializer.is_valid():
                location_serializer.save()
            else:
                raise serializers.ValidationError(location_serializer.errors)
        except:
            pass
        # try:
        #     images_data = validated_data.pop('images')
        #     print(images_data)
        #     images_serializer = PropertyImages(instance, data=images_data)
        #     if images_serializer.is_valid():
        #         images_serializer.save()
        #     else:
        #         raise serializers.ValidationError(location_serializer.errors)
        # except:
        #     pass
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Customize the serialized representation of the instance.
        """
        data = super().to_representation(instance)

        # If property is not for sale, remove the ownership_type field
        if instance.property_status != "For Sale":
            data.pop("ownership_type")

        return data
    # def update(self, instance, validated_data):
    #     images_data = validated_data.pop('images', [])

    #     # Update property fields
    #     instance.address = validated_data.get('address', instance.address)
    #     # ... update other fields
    #     instance.save()

    #     # Handle existing and new images
    #     existing_images = instance.images.all()
    #     for image_data in images_data:
    #         if image_data.get('id'):
    #             # Update existing image
    #             existing_image = existing_images.get(pk=image_data['id'])
    #             existing_image.image = image_data['image']
    #             existing_image.save()
    #         else:
    #             # Create new image
    #             PropertyImages.objects.create(property=instance, **image_data)

    #     # Delete removed images (optional)
    #     for image in existing_images:
    #         if image not in instance.images.all():
    #             image.delete()

    #     return instance
class PropertyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        exclude = ["updated_at", "pkid"]


class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ["updated_at", "pkid"]



