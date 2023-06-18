from django.urls import path
from .views import UserSearchView, FriendshipRequestView, FriendshipAcceptView, FriendshipReAcceptView, FriendListView, AllListView, FriendDetailView, ReportFriendView, BlockFriendView, RemoveFriendView

urlpatterns = [
    path('user/<str:username>/', UserSearchView.as_view(), name='user-search'),
    path('friend/request/', FriendshipRequestView.as_view(), name='friend-request'),
    path('friend/accept/request/', FriendshipAcceptView.as_view(), name='friend-accept'),
    path('friend/reactivate/accept/', FriendshipReAcceptView.as_view(), name='reactivate-friend-accept'),
    path('friend/list/', FriendListView.as_view(), name='friend-list'),
    path('all/list/', AllListView.as_view(), name='all-list'),
    path('friend/detail/one/', FriendDetailView.as_view(), name='friend-detail'),
    path('friend/report/problem/', ReportFriendView.as_view(), name='friend-report'),
    path('friend/block/problem/', BlockFriendView.as_view(), name='friend-block'),
    path('friend/remove/problem/', RemoveFriendView.as_view(), name='friend-remove'),
]