from firebase_admin import messaging
import firebase_admin

if not firebase_admin._apps:
    from .firebase import default_app

def send_topic_notification(topic, title, body, data=None):
    """
    Sends a push notification to a topic via FCM.
    
    :param topic: The topic to which users have subscribed.
    :param title: The title of the notification.
    :param body: The body of the notification.
    :param data: Any additional data to send with the notification.
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic=topic,
        data=data or {}
    )

    try:
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending notification: {e}")
        return None