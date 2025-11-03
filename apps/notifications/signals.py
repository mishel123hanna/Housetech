import urllib.parse

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.properties.models import Property

from .service import send_topic_notification


@receiver(post_save, sender=Property)
def send_notification(sender, instance, created, **kwargs):
    if created:
        property_city = instance.location.city
        property_type = instance.property_type
        property_status = instance.property_status
        property_title = instance.title
        property_slug = instance.slug

        message = f"تم اضافة العقار {property_title} في {property_city} نوعه {property_type} حالته {property_status}"
        topic = f"{property_city}-{property_type}-{property_status}"
        encoded_topic = urllib.parse.quote(topic)
        print(topic)
        print(encoded_topic)

        send_topic_notification(
            f"{encoded_topic}", "New Property Alert", message, {"slug": property_slug}
        )


# FCM Token

# @receiver(post_save, sender=Property)
# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         property_city = instance.location.city
#         property_region = instance.location.region

#         print(f"Property added: {property_city}, {property_region}")

#         profiles = Profile.objects.all()

#         matching_profiles = []
#         for profile in profiles:
#             preferred_locations = profile.preferred_locations_list
#             if property_city in preferred_locations or property_region in preferred_locations:
#                 matching_profiles.append(profile)

#         print(f"Found {len(matching_profiles)} profiles with matching locations")

#         for profile in matching_profiles:
#             print(f"Creating notification for user: {profile.user.get_full_name}")
#             location_message = "A new property has been added in your preferred location: "
#             if property_city and property_region:
#                 location_message += f"{property_city}, {property_region}"
#             elif property_city:
#                 location_message += f"{property_city}"
#             elif property_region:
#                 location_message += f"{property_region}"
#             else:
#                 continue
#             Notification.objects.create(
#                 user=profile.user,
#                 message=location_message
#             )

#             fcm_tokens = FCMToken.objects.filter(user=profile.user)
#             for token in fcm_tokens:
#                 print(f"Sending FCM notification to user: {profile.user.get_full_name} with token: {token.token}")
#                 message = messaging.Message(
#                     notification=messaging.Notification(
#                         title="New Property Alert",
#                         body=f"A new property has been added in your preferred location: {property_city}, {property_region}",
#                     ),
#                     token=token.token,
#                 )
#                 try:
#                     response = messaging.send(message)
#                     print('Successfully sent message:', response)
#                 except Exception as e:
#                     print('Error sending message:', e)


# FCM Topic

# @receiver(post_save, sender=Property)
# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         property_city = instance.location.city
#         property_region = instance.location.region

#         print(f"Property added: {property_city}, {property_region}")

#         profiles = Profile.objects.all()
#         matching_profiles = []

#         for profile in profiles:
#             preferred_locations = profile.preferred_locations_list
#             if property_city in preferred_locations or property_region in preferred_locations:
#                 matching_profiles.append(profile)

#         print(f"Found {len(matching_profiles)} profiles with matching locations")

#         if property_city and property_region:
#             location_message = f"A new property has been added in your preferred location: {property_city}, {property_region}"
#         elif property_city:
#             location_message = f"A new property has been added in your preferred location: {property_city}"
#         elif property_region:
#             location_message = f"A new property has been added in your preferred location: {property_region}"
#         else:
#             location_message = "A new property has been added in your preferred location"

#         # Send notification to users via topics based on location
#         if property_city:
#             send_topic_notification(f"{property_city}", "New Property Alert", location_message)
#         if property_region:
#             send_topic_notification(f"user", "New Property Alert", location_message)

#         for profile in matching_profiles:
#             print(f"Creating notification for user: {profile.user.get_full_name}")
#             Notification.objects.create(
#                 user=profile.user,
#                 message=location_message
#             )
