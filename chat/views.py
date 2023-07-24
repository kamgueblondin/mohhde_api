from chat.models import Message
from django.shortcuts import render

# Create your views here.
def chat(request):
    return render(request, './templates/chat.html', context={})

def room(request, room_name):
    return render(request, './templates/chatroom.html', context={'room_name': room_name})

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class ConversationMessagesAPIView(APIView):
    def get(self, request):
        user = get_object_or_404(User, username=request.GET.get('username'))
        user_token = request.GET.get('user_token')
        conversation_id=request.GET.get('conversation_id')
        if not user_token:
            return Response({'success': False, 'message': 'Missing required parameter: user_token'})

        if user.profile.user_token != user_token:
            return Response({'success': False, 'message': 'Invalid token for the specified user'})
        
        # Récupérer tous les messages de la conversation donnée par son ID
        messages = Message.objects.filter(conversation_id=conversation_id)
        
        # Sérialiser les données des messages 
        serializer = MessageSerializer(messages, many=True)
        
        return Response(serializer.data)