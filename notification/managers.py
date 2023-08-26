from django.contrib.auth.models import User
from .models import Notification

class NotificationManager:
    @staticmethod
    def create_notification(user, message):
        notification = Notification.objects.create(
            user=user,
            message=message
        )
        return notification
