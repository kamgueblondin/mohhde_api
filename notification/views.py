from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def get_unread_notifications(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            unread_notifications = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')[:4]
        
            # Marquer les notifications comme lues
            #for notification in unread_notifications:
            #    notification.is_read = True
            #    notification.save()
            
            serializer = NotificationSerializer(unread_notifications, many=True)
            response_data ={
                'success': True,
                'notifications': serializer.data
            }
            
            return Response(response_data)
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})

@api_view(['POST'])
def mark_notification_as_read(request):
    if request.method == 'POST':
        notification_id= request.data.get('notification_id')
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            notification = Notification.objects.get(id=notification_id)
        
            # Marquer la notification comme lue
            notification.is_read = True
            notification.save()
            
            return Response({'success': True, 'message': "Notification marquée comme lue"})
            
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})