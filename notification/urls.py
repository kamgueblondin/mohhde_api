from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet,get_unread_notifications,mark_notification_as_read

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('unread/notifications/', get_unread_notifications),
    path('mark-as-read/notifications/', mark_notification_as_read),
]