from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chain

class FilteredMediaChainView(APIView):
    def get(self, request, filter_type):
        chains = Chain.objects.filter(user=request.user, type=filter_type)
        data = []
        for chain in chains:
            chain_data = {
                'name': chain.name,
                'description': chain.description,
                'type': chain.type,
                'media': []
            }
            medias = chain.media_set.filter(is_archived=False)
            for media in medias:
                media_data = {
                    'title': media.title,
                    'description': media.description,
                    'type': media.type
                }
                chain_data['media'].append(media_data)
            data.append(chain_data)
            
        return Response(data)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Media
class FavoritesView(APIView):
    def get(self, request):
        favorites = Media.objects.filter(user=request.user, is_favorite=True, is_archived=False)
        serializer = MediaSerializer(favorites, many=True)
        return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MediaConfiguration

class MediaConfigurationView(APIView):
    def get(self, request):
        media_configuration = MediaConfiguration.objects.get(user=request.user)
        serializer = MediaConfigurationSerializer(media_configuration)
        return Response(serializer.data)

    def put(self, request):
        media_configuration = MediaConfiguration.objects.get(user=request.user)
        serializer = MediaConfigurationSerializer(media_configuration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Chain, Media
from .serializers import ChainSerializer, MediaSerializer
from django.contrib.auth.models import User

class ChainViewSet(viewsets.ModelViewSet):
    serializer_class = ChainSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Chain.objects.filter(user=user)
        return queryset

class MediaViewSet(viewsets.ModelViewSet):
    serializer_class = MediaSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Media.objects.filter(chain__user=user)
        return queryset

class UserChainListView(APIView):

    def get(self, request):
        user = self.request.user
        chains = Chain.objects.filter(user=user)
        serializer = ChainSerializer(chains, many=True)
        return Response(serializer.data)

class ChainDetailView(APIView):

    def get(self, request, pk):
        user = self.request.user
        chain = get_object_or_404(Chain.objects.filter(user=user), pk=pk)
        serializer = ChainSerializer(chain)
        return Response(serializer.data)

class ChainCreateView(APIView):

    def post(self, request):
        serializer = ChainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChainUpdateView(APIView):

    def put(self, request, pk):
        user = self.request.user
        chain = get_object_or_404(Chain.objects.filter(user=user), pk=pk)
        serializer = ChainSerializer(chain, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChainDeleteView(APIView):

    def delete(self, request, pk):
        user = self.request.user
        chain = get_object_or_404(Chain.objects.filter(user=user), pk=pk)
        chain.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChainShareView(APIView):

    def put(self, request, pk):
        user = self.request.user
        chain = get_object_or_404(Chain.objects.filter(user=user), pk=pk)
        chain.is_shared = True
        chain.save()
        serializer = ChainSerializer(chain)
        return Response(serializer.data)

class ChainSubscribeView(APIView):

    def put(self, request, pk):
        user = self.request.user
        chain = get_object_or_404(Chain.objects.exclude(user=user), pk=pk)
        chain.subscribers.add(user)
        chain.save()
        serializer = ChainSerializer(chain)
        return Response(serializer.data)

class ChainUnsubscribeView(APIView):

    def put(self, request, pk):
        user = self.request.user
        chain = get_object_or_404(Chain.objects.exclude(user=user), pk=pk)
        chain.subscribers.remove(user)
        chain.save()
        serializer = ChainSerializer(chain)
        return Response(serializer.data)

class ChainBlockView(APIView):

    def put(self, request, pk):
        user = self.request.user
        chain = get_object_or_404(Chain.objects.exclude(user=user).exclude(subscribers=user), pk=pk)
        chain.blocked_users.add(user)
        chain.save()
        serializer = ChainSerializer(chain)
        return Response(serializer.data)

class MediaDetailView(APIView):

    def get(self, request, pk):
        user = self.request.user
        media = get_object_or_404(Media.objects.filter(chain__user=user), pk=pk)
        serializer = MediaSerializer(media)
        return Response(serializer.data)

class MediaCreateView(APIView):

    def post(self, request):
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MediaUpdateView(APIView):

    def put(self, request, pk):
        user = self.request.user
        media = get_object_or_404(Media.objects.filter(chain__user=user), pk=pk)
        serializer = MediaSerializer(media, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MediaDeleteView(APIView):

    def delete(self, request, pk):
        user = self.request.user
        media = get_object_or_404(Media.objects.filter(chain__user=user), pk=pk)
        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chain, Media


class LikeViewSet(APIView):
    def post(self, request, pk):
        try:
            media_or_chain = Chain.objects.get(pk=pk)
            if media_or_chain:
                media_or_chain.likes += 1
                media_or_chain.save()
            else:
                media_or_chain = Media.objects.get(pk=pk)
                media_or_chain.likes += 1
                media_or_chain.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Media
from .serializers import MediaSerializer


class RetrieveMediaViewSet(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    lookup_field = 'pk'

# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chain
from .serializers import ChainSerializer


class RetrieveChainViewSet(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Chain.objects.all()
    serializer_class = ChainSerializer
    lookup_field = 'pk'

# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chain
from .serializers import ChainSerializer


class ActivateChainViewSet(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Chain.objects.all()
    serializer_class = ChainSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chain
from .serializers import ChainSerializer


class ListUserChainViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChainSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Chain.objects.filter(user=user)
        return queryset

# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chain
from .serializers import ChainSerializer


class ArchiveChainViewSet(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Chain.objects.all()
    serializer_class = ChainSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archived = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class RestoreChainViewSet(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Chain.objects.all()
    serializer_class = ChainSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archived = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Media
from .serializers import MediaSerializer


class FavoriteMediaViewSet(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_favorite = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Media
from .serializers import MediaSerializer


class UnfavoriteMediaViewSet(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_favorite = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)