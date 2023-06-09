from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Friendship
from .serializers import FriendshipSerializer
from mohhde.serializers import UserSerializer, ProfileSerializer

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        queryset = User.objects.filter(username__icontains=query)
        return queryset

class FriendshipRequestView(generics.CreateAPIView):
    serializer_class = FriendshipSerializer

    def post(self, request, *args, **kwargs):
        friend_id = request.data.get('friend_id')
        category = request.data.get('category')
        friend = User.objects.get(id=friend_id)
        friendship = Friendship(user=request.user, friend=friend, status='pending', category=category)
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendshipAcceptanceView(generics.UpdateAPIView):
    serializer_class = FriendshipSerializer

    def patch(self, request, *args, **kwargs):
        friendship_id = kwargs['pk']
        friendship = Friendship.objects.get(id=friendship_id)
        friendship.status = 'accepted'
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class FriendsListView(generics.ListAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        queryset = Friendship.objects.filter(user=self.request.user, status='accepted')
        return queryset

class FriendDetailView(generics.RetrieveAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        queryset = Friendship.objects.filter(user=self.request.user, status='accepted')
        return queryset

class ReportFriendView(generics.UpdateAPIView):
    serializer_class = FriendshipSerializer

    def patch(self, request, *args, **kwargs):
        friendship_id = kwargs['pk']
        friendship = Friendship.objects.get(id=friendship_id)
        friendship.status = 'reported'
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class BlockFriendView(generics.UpdateAPIView):
    serializer_class = FriendshipSerializer

    def patch(self, request, *args, **kwargs):
        friendship_id = kwargs['pk']
        friendship = Friendship.objects.get(id=friendship_id)
        friendship.status = 'blocked'
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class UnfriendView(generics.DestroyAPIView):
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        queryset = Friendship.objects.filter(user=self.request.user, status='accepted')
        return queryset
