import base64
from chat.models import Conversation
from medias.models import Chain, Media
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from together.models import Friendship
from together.serializers import FriendshipSerializer,UserSerializer
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


class UserSearchView(APIView):
    def get(self, request):
        username = request.data.get('username')
        user_token = request.data.get('user_token')
        username_search=request.data.get('query')

        if not username or not user_token:
            return Response({'success': False, 'message': 'Missing required parameters'})
        
        # Vérifier si l'utilisateur correspond au jeton utilisateur
        users = User.objects.filter(username__icontains=username_search)
        serializer = UserSerializer(users, many=True)
        if len(users) == 0:
            return Response({'success': False, 'message':'No users found with the specified username'})
        
        response_data ={
            'success': True,
            'users': serializer.data
        }
        
        return Response(response_data)


class FriendsConversationCodes(APIView):
    def get(self, request):
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})

        friendships = Friendship.objects.filter(status='accepted')
        friend_data = []
        
        for friendship in friendships:
            data = {
                'user': friendship.user.username,
                'friend': friendship.friend.username,
                'status': friendship.status,
                'category': friendship.category,
                'conversation_code': friendship.conversation.code if friendship.conversation else None
            }
            
            friend_data.append(data)
        
        response_data = {
            "success": True,
            "friendship": friend_data
        }
        
        return Response(response_data)
    
class FriendshipRequestView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})

        friendship = Friendship(user=user, friend=friend, status='pending', category=request.data.get('category'))
        friendship.save()
        
        serializer = FriendshipSerializer(friendship)
        response_data ={
            'success': True,
            'friendship': serializer.data
        }
        
        return Response(response_data)


class FriendshipAcceptView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        friendships = Friendship.objects.filter(user=user, friend=friend, status='pending')
        for friendship in friendships:
                friendship.status = 'accepted'
                friendship.save()
    
                # Créer une nouvelle instance de la classe Conversation avec le participant actuel (utilisateur connecté)
                conversation = Conversation.objects.create()
        
                # Ajouter le participant actuel à la conversation
                conversation.participants.add(user)
                conversation.participants.add(friend)

                # Ajouter la conversation à l'amitié
                friendship.conversation = conversation
                friendship.save()
        
        return Response({'success': True, 'message': 'ok'})
        


class FriendshipReAcceptView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        friendship = get_object_or_404(Friendship, user=user, friend=friend)
        friendship.status = 'accepted'
        friendship.conversation.state='ACTIVE'
        friendship.conversation.save()
        friendship.save()
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data)


class FriendListView(APIView):
    def get(self, request):
        user = get_object_or_404(User, username=request.GET.get('username'))
        friends = Friendship.objects.filter(user=user, status='accepted')
        user_token = request.GET.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        serializer = FriendshipSerializer(friends, many=True)

        response_data ={
            'success': True,
            'friendship': serializer.data
        }
        
        return Response(response_data)


class AllListView(APIView):
    def get(self, request):
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        friends = Friendship.objects.filter(user=user, status='pending')
        serializer = FriendshipSerializer(friends, many=True)
        response_data ={
            'success': True,
            'friendship': serializer.data
        }
        
        return Response(response_data)


class FriendDetailView(APIView):
    def get(self, request):
        friend = get_object_or_404(User, username=request.GET.get('friend'))
        user = get_object_or_404(User, username=request.GET.get('username'))
        user_token = request.GET.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        try:
            friendship = Friendship.objects.get(user=user, friend=friend, status='accepted')
            serializer = FriendshipSerializer(friendship)
            response_data ={
                'success': True,
                'friendship': serializer.data
            }
            
            return Response(response_data)
        
        except ObjectDoesNotExist:
            return Response({'success': False, 'message': 'No accepted friendship found matching the criteria'})


class ReportFriendView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        try:
            friendship = Friendship.objects.get(user=user, friend=friend, status='accepted')
            friendship.status = 'reported'
            friendship.conversation.state='ARCHIVED'
            friendship.conversation.save()
            friendship.save()
            serializer = FriendshipSerializer(friendship)
            response_data ={
                'success': True,
                'friendship': serializer.data
            }
            
            return Response(response_data)
        except ObjectDoesNotExist:
            return Response({'success': False, 'message': 'No Accepted friendship found matching the criteria'})


class BlockFriendView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        try:
            friendship = Friendship.objects.get(user=user, friend=friend, status='accepted')
            friendship.status = 'blocked'
            friendship.conversation.state='ARCHIVED'
            friendship.conversation.save()
            friendship.save()
            serializer = FriendshipSerializer(friendship)
            response_data ={
                'success': True,
                'friendship': serializer.data
            }
            
            return Response(response_data)
        except ObjectDoesNotExist:
            return Response({'success': False, 'message': 'No Accepted friendship found matching the criteria'})


class RemoveFriendView(APIView):
    def post(self, request):
        friend = get_object_or_404(User, username=request.data.get('friend'))
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        friendship = Friendship.objects.filter(user=user, friend=friend)
        friendship.delete()
        return Response({'success': True, 'message': 'ok'})


class ProfileFriendView(APIView):
    def get(self, request):
        friend = get_object_or_404(User, username=request.GET.get('friend'))
        user = get_object_or_404(User, username=request.GET.get('username'))
        user_token = request.GET.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        try:
            profile_chain = Chain.objects.get(name='profile', user=friend)
            # Récupérer le premier média non archivé (is_archived=False) de l'utilisateur
            media = Media.objects.filter(user=friend, is_archived=False, chain=profile_chain).first()
            
            if media:
                image_path = "./templates/profile/"+media.description
                
                with open(image_path, 'rb') as file:
                    encoded_image_data = base64.b64encode(file.read()).decode('utf-8')
                    
                response_data ={
                    'success': True,
                    'media_title': media.description,
                    'image_base64': encoded_image_data
                }
                
                return Response(response_data)
            
            else:
                return Response({'success': False, 'message':'No profile media found for this user'})
        except Chain.DoesNotExist:
            return Response({'success': False, 'message':'No chain profile found for this user'})


class GalerieFriendView(APIView):
    def get(self, request):
        friend = get_object_or_404(User, username=request.GET.get('friend'))
        user = get_object_or_404(User, username=request.GET.get('username'))
        user_token = request.GET.get('user_token')

        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        try:
            galerie_chain = Chain.objects.get(name='galerie', user=friend)
            # Récupérer tous les médias non archivés (is_archived=False) de la chaîne galerie de l'utilisateur
            media_list = Media.objects.filter(user=friend, is_archived=False, chain=galerie_chain)
    
    
            
            if media_list:

                response_data ={
                    'success': True,
                    'media_count': len(media_list),
                    'media': []
                }
                
                for media in media_list:
                    image_path = "./templates/galerie/" + media.description
                    
                    with open(image_path, 'rb') as file:
                        encoded_image_data = base64.b64encode(file.read()).decode('utf-8')
                        
                    response_data['media'].append({
                        'title': media.description,
                        'image_base64': encoded_image_data
                    })
                    
                return Response(response_data)
            
            else:
                return Response({'success': False, 'message':'No galerie media found for this user'})
        except Chain.DoesNotExist:
            return Response({'success': False, 'message':'No chain galerie found for this user'})
