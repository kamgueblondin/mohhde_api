from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from together.models import Friendship
from together.serializers import FriendshipSerializer,UserSerializer
from django.utils import timezone

class UserSearchView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class FriendshipRequestView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        friendship = Friendship(user=user, friend=friend, status='pending', category=request.data.get('category'))
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class FriendshipAcceptView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        friendship = get_object_or_404(Friendship, user=user, friend=friend, status='pending')
        friendship.status = 'accepted'
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)
    
class FriendshipReAcceptView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        friendship = get_object_or_404(Friendship, user=user, friend=friend)
        friendship.status = 'accepted'
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class FriendListView(APIView):
    def get(self, request):
        user = get_object_or_404(User, username=request.GET.get('username'))
        friends = Friendship.objects.filter(user=user, status='accepted')
        serializer = FriendshipSerializer(friends, many=True)
        return Response(serializer.data)
    
class AllListView(APIView):
    def get(self, request):
        user = get_object_or_404(User, username=request.GET.get('username'))
        friends = Friendship.objects.filter(user=user)
        serializer = FriendshipSerializer(friends, many=True)
        return Response(serializer.data)

class FriendDetailView(APIView):
    def get(self, request):
        friend = get_object_or_404(User, username=request.GET.get('friend'))
        user = get_object_or_404(User, username=request.GET.get('username'))
        friendship = Friendship.objects.get(user=user, friend=friend, status='accepted')
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class ReportFriendView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        friendship = Friendship.objects.get(user=user, friend=friend, status='accepted')
        friendship.status = 'reported'
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class BlockFriendView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        friendship = Friendship.objects.get(user=user, friend=friend, status='accepted')
        friendship.status = 'blocked'
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)

class RemoveFriendView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        friendship = Friendship.objects.filter(user=user, friend=friend)
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)