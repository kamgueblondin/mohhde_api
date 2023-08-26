from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Annonce
from .serializers import AnnonceSerializer
from django.contrib.auth.models import User

class AnnonceListCreateView(generics.ListCreateAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer

class AnnonceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_system_active_announcement(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.data.get('username'))
        user_token = request.data.get('user_token')
        if user.profile.user_token == user_token:
            try:
                announcement = Annonce.objects.filter(state=True, is_system=True).first()
        
                serializer = AnnonceSerializer(announcement)

                response_data ={
                    'success': True,
                    'announcement': serializer.data
                }
                
                return Response(response_data)
            except Exception as e:
                return Response({'success': False, 'message': str(e)})
        else:
            return Response({'success': False, 'message': 'No user with this key'})
    else:
        return Response({'success': False, 'message': 'Invalid method'})