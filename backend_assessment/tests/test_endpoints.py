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

class TaskListAPITest(APITestCase):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # create stranger
        self.stranger = User.objects.create_user(username='bobross', password='12345')
        stranger_refresh = RefreshToken.for_user(self.stranger)
        self.stranger_token = str(stranger_refresh.access_token)
        
        self.label1 = Label.objects.create(name='Label 1', owner=self.user)
        self.label2 = Label.objects.create(name='Label 2', owner=self.user)

    # GET TASK LIST
    def test_get_task_list(self):
        Task.objects.create(title='Task 1', description='Description 1', is_completed=False, owner=self.user)
        Task.objects.create(title='Task 2', description='Description 2', is_completed=True, owner=self.user)

        url = reverse('task-list')
        response = self.client.get(url)

        tasks = Task.objects.filter(owner=self.user)
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # CREATE TASK
    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'is_completed': False,
            'owner': self.user.id,
            'labels': [self.label1.id, self.label2.id]
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        created_task = Task.objects.get(id=response.data['id'])
        self.assertEqual(created_task.title, 'New Task')
        self.assertEqual(created_task.description, 'New Task Description')
        self.assertFalse(created_task.is_completed)
        self.assertEqual(created_task.owner, self.user)
        self.assertEqual(list(created_task.labels.all()), [self.label1, self.label2])

    # CREATE INVALID TASK
    def test_create_invalid_task(self):
        url = reverse('task-list')
        data = {'title': ''}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    # GET TASK
    def test_get_task_detail(self):
        task = Task.objects.create(title='Task 1', description='Description 1', is_completed=False, owner=self.user)
        task.labels.set([self.label1, self.label2])
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.get(url)

        serializer = TaskSerializer(task)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # UPDATE TASK
    def test_update_task(self):
        task = Task.objects.create(title='Task 1', description='Description 1', is_completed=False, owner=self.user)
        task.labels.set([self.label1])
        url = reverse('task-detail', kwargs={'pk': task.pk})
        data = {
            'title': 'Updated Task',
            'description': 'Updated Task Description',
            'is_completed': True,
            'owner': self.user.id,
            'labels': [self.label2.id]
        }

        response = self.client.put(url, data, format='json')

        task.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.title, 'Updated Task')
        self.assertEqual(task.description, 'Updated Task Description')
        self.assertEqual(task.is_completed, True)
        self.assertTrue(task.is_completed)
        self.assertEqual(list(task.labels.all()), [self.label2])

    # DELETE TASK
    def test_delete_task(self):
        task = Task.objects.create(title='Task 1', description='Description 1', is_completed=False, owner=self.user)
        url = reverse('task-detail', kwargs={'pk': task.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
    
    # STRANGER ACCESS
    def test_stranger_access(self):
        # my task
        task = Task.objects.create(title='Task 1', description='Description 1', is_completed=False, owner=self.user)
        task.labels.set([self.label1, self.label2])
        label_url = reverse('label-detail', kwargs={'pk': self.label1.pk})
        task_url = reverse('task-detail', kwargs={'pk': task.pk})
        
        # stranger trying to access the task
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.stranger_token}')
        
        response_label = self.client.get(label_url)
        self.assertEqual(response_label.status_code, status.HTTP_404_NOT_FOUND)
        
        response_task = self.client.get(task_url)
        self.assertEqual(response_task.status_code, status.HTTP_404_NOT_FOUND)

        # reset credentials to the original user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')