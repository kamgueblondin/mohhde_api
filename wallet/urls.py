from django.urls import include, path
from rest_framework import routers
from .views import AccountViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]