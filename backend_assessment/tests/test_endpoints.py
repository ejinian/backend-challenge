from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from tasks.models import Label, Task
from tasks.serializers import LabelSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class LabelListAPITest(APITestCase):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def setUp(self):
        # rest_framework.authtoken.models import Token was not working so I manually get the JWT here
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    # GET LABEL LIST
    def test_get_label_list(self):
        Label.objects.create(name='Label 1', owner=self.user)
        Label.objects.create(name='Label 2', owner=self.user)

        url = reverse('label-list')
        response = self.client.get(url)

        labels = Label.objects.filter(owner=self.user)
        serializer = LabelSerializer(labels, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # CREATE LABEL
    def test_create_label(self):
        url = reverse('label-list')
        data = {'name': 'New Label', 'owner': self.user.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 1)

        created_label = Label.objects.get(id=response.data['id'])
        self.assertEqual(created_label.name, 'New Label')
        self.assertEqual(created_label.owner, self.user)

    # CREATE INVALID LABEL
    def test_create_invalid_label(self):
        url = reverse('label-list')
        data = {'name': ''}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Label.objects.count(), 0)

    # GET LABEL
    def test_get_label_detail(self):
        label = Label.objects.create(name='Label 1', owner=self.user)
        url = reverse('label-detail', kwargs={'pk': label.pk})
        response = self.client.get(url)

        serializer = LabelSerializer(label)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # UPDATE LABEL
    def test_update_label(self):
        label = Label.objects.create(name='Label 1', owner=self.user)
        url = reverse('label-detail', kwargs={'pk': label.pk})
        data = {'name': 'Updated Label', 'owner': self.user.id}

        response = self.client.put(url, data, format='json')

        label.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(label.name, 'Updated Label')

    # DELETE LABEL
    def test_delete_label(self):
        label = Label.objects.create(name='Label 1', owner=self.user)
        url = reverse('label-detail', kwargs={'pk': label.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())

