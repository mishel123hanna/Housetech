from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging
from .models import Notification, FCMToken
from apps.accounts.models import Profile
from apps.properties.models import Property

@receiver(post_save, sender=Property)
def send_notification(sender, instance, created, **kwargs):
    if created:
        property_city = instance.location.city
        property_region = instance.location.region

        print(f"Property added: {property_city}, {property_region}")
        
        profiles = Profile.objects.all()

        matching_profiles = []
        for profile in profiles:
            preferred_locations = profile.preferred_locations_list
            if property_city in preferred_locations or property_region in preferred_locations:
                matching_profiles.append(profile)

        print(f"Found {len(matching_profiles)} profiles with matching locations")

        for profile in matching_profiles:
            print(f"Creating notification for user: {profile.user.get_full_name}")
            location_message = "A new property has been added in your preferred location: "
            if property_city and property_region:
                location_message += f"{property_city}, {property_region}"
            elif property_city:
                location_message += f"{property_city}"
            elif property_region:
                location_message += f"{property_region}"
            else:
                continue
            Notification.objects.create(
                user=profile.user,
                message=location_message
            )
            
            fcm_tokens = FCMToken.objects.filter(user=profile.user)
            for token in fcm_tokens:
                print(f"Sending FCM notification to user: {profile.user.get_full_name} with token: {token.token}")
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="New Property Alert",
                        body=f"A new property has been added in your preferred location: {property_city}, {property_region}",
                    ),
                    token=token.token,
                )
                try:
                    response = messaging.send(message)
                    print('Successfully sent message:', response)
                except Exception as e:
                    print('Error sending message:', e)
