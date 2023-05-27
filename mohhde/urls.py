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
from .views import register_view, login_view, check_reset_password_code, send_reset_password_email, reset_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),
    path('api/register/', register_view, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/start_reset/', send_reset_password_email, name='start_reset'),
    path('api/verify_reset/', check_reset_password_code, name='verify_password_reset'),
    path('api/validate_reset/', reset_password, name='validate_password_reset'),
]
