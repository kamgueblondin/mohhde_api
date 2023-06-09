from django.urls import path
from .views import UserSearchView, FriendshipRequestView, FriendshipAcceptanceView, FriendsListView, FriendDetailView, ReportFriendView, BlockFriendView, UnfriendView

urlpatterns = [
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('request/', FriendshipRequestView.as_view(), name='friendship-request'),
    path('accept/<int:pk>/', FriendshipAcceptanceView.as_view(), name='friendship-acceptance'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('friend/<int:pk>/', FriendDetailView.as_view(), name='friend-detail'),
    path('report/<int:pk>/', ReportFriendView.as_view(), name='report-friend'),
    path('block/<int:pk>/', BlockFriendView.as_view(), name='block-friend'),
    path('unfriend/<int:pk>/', UnfriendView.as_view(), name='unfriend'),
]
