from django.urls import path
from rest_framework import routers
from django.urls import path, include
from . import views
from medias.views import FilteredMediaChainView,FavoritesView,MediaConfigurationView,LikeViewSet,RetrieveMediaViewSet,RetrieveChainViewSet,ActivateChainViewSet,ListUserChainViewSet,ArchiveChainViewSet,RestoreChainViewSet,FavoriteMediaViewSet,UnfavoriteMediaViewSet

router = routers.DefaultRouter()
router.register(r'chains', views.ChainViewSet)
router.register(r'media', views.MediaViewSet)
urlpatterns = [
    path('media/<str:filter_type>/', FilteredMediaChainView.as_view(), name='filtered_media_chain'),
    path('favorites/', FavoritesView.as_view(), name='favorites_list'),
    path('media/configuration/', MediaConfigurationView.as_view(), name='media_configuration'),
    path('', include(router.urls)),
    path('search/', views.search_view),
    path('user/chains/', views.UserChainListView.as_view()),
    path('chain/<int:pk>/', views.ChainDetailView.as_view()),
    path('chain/create/', views.ChainCreateView.as_view()),
    path('chain/update/<int:pk>/', views.ChainUpdateView.as_view()),
    path('chain/delete/<int:pk>/', views.ChainDeleteView.as_view()),
    path('chain/share/<int:pk>/', views.ChainShareView.as_view()),
    path('chain/subscribe/<int:pk>/', views.ChainSubscribeView.as_view()),
    path('chain/unsubscribe/<int:pk>/', views.ChainUnsubscribeView.as_view()),
    path('chain/block/<int:pk>/', views.ChainBlockView.as_view()),
    path('media/<int:pk>/', views.MediaDetailView.as_view()),
    path('media/create/', views.MediaCreateView.as_view()),
    path('media/update/<int:pk>/', views.MediaUpdateView.as_view()),
    path('media/delete/<int:pk>/', views.MediaDeleteView.as_view()),
    path('like/<int:pk>/', LikeViewSet.as_view(), name='like'),
    path('media/<int:pk>/', RetrieveMediaViewSet.as_view(), name='media'),
    path('chain/<int:pk>/', RetrieveChainViewSet.as_view(), name='chain'),
    path('chain/activate/<int:pk>/', ActivateChainViewSet.as_view(), name='activate_chain'),
    path('chain/user/', ListUserChainViewSet.as_view(), name='user_chains'),
    path('chain/archive/<int:pk>/', ArchiveChainViewSet.as_view(), name='archive_chain'),
    path('chain/restore/<int:pk>/', RestoreChainViewSet.as_view(), name='restore_chain'),
    path('media/favorite/<int:pk>/', FavoriteMediaViewSet.as_view(), name='favorite_media'),
    path('media/unfavorite/<int:pk>/', UnfavoriteMediaViewSet.as_view(), name='unfavorite_media'),
]