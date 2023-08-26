from django.urls import path

from .views import StorageInfo

urlpatterns = [
    path('storage/<int:user_id>/', StorageInfo.as_view()),
]