from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Chain, Media
from .serializers import ChainSerializer, MediaSerializer

# Tests pour les chaînes

class ChainTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.chain = Chain.objects.create(name='Test Chain', description='Test Chain description', type='I', user=self.user)

    def test_get_chain_list(self):
        url = reverse('chain-list')
        response = self.client.get(url)
        chains = Chain.objects.all()
        serializer = ChainSerializer(chains, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_chain(self):
        url = reverse('chain-create')
        data = {'name': 'New Chain', 'description': 'New Chain description', 'type': 'I'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chain.objects.count(), 2)

    def test_get_chain_detail(self):
        url = reverse('chain-detail', kwargs={'pk': self.chain.id})
        response = self.client.get(url)
        chain = Chain.objects.get(id=self.chain.id)
        serializer = ChainSerializer(chain)
        self.assertEqual(response.data, serializer.data)

    def test_update_chain(self):
        url = reverse('chain-update', kwargs={'pk': self.chain.id})
        data = {'name': 'Updated Chain', 'description': 'Updated Chain description', 'type': 'V'}
        response = self.client.put(url, data, format='json')
       