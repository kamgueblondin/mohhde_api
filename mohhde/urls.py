"""
URL configuration for mohhde project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import register_view, validate_register_view, reload_register_view, login_view, logout_view, check_reset_password_code, send_reset_password_email, reset_password,infos_profile,update_profile,change_password,media_profile,media_galerie,ma_photo_profile,mes_photos_galerie,archive_media_profile,archive_media_galerie

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),
    path('api/together/', include('together.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/annonce/', include('annonce.urls')),
    path('api/stockage/', include('stockage.urls')),
    path('', include('chat.urls')),
    path('api/register/', register_view, name='register'),
    path('api/register/validate/', validate_register_view, name='register_validate'),
    path('api/register/reload/', reload_register_view, name='register_reload'),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
    path('api/start_reset/', send_reset_password_email, name='start_reset'),
    path('api/verify_reset/', check_reset_password_code, name='verify_password_reset'),
    path('api/validate_reset/', reset_password, name='validate_password_reset'),
    path('api/infos_profile/', infos_profile, name='infos_profile'),
    path('api/update_profile/', update_profile, name='update_profile'),
    path('api/change_password/', change_password, name='change_password'),
    path('api/media_profile/', media_profile, name='media_profile'),
    path('api/media_galerie/', media_galerie, name='media_galerie'),
    path('api/ma_photo_profile/', ma_photo_profile, name='ma_photo_profile'),
    path('api/mes_photos_galerie/', mes_photos_galerie, name='mes_photos_galerie'),
    path('api/archive_media_profile/', archive_media_profile, name='archive_media_profile'),
    path('api/archive_media_galerie/', archive_media_galerie, name='archive_media_galerie'),
]
