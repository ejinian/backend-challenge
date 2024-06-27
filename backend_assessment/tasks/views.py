from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer
from django.contrib.auth.models import User

@api_view(['GET'])
def home(request):
    task_count = Task.objects.count()
    label_count = Label.objects.count()
    total_users = User.objects.count()

    data = {
        "message": "Welcome to the Task and Label API",
        "statistics": {
            "total_tasks": task_count,
            "total_labels": label_count,
            "total_users": total_users
        }
    }

    return Response(data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def label_list(request):
    """GET or POST to the /labels/ route"""
    if request.method == 'GET':
        labels = Label.objects.filter(owner=request.user)
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LabelSerializer(data=request.data)
        # validating data from the body
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def label_detail(request, pk):
    """GET, PUT, or DELETE to the /labels/<label_id> route"""
    try:
        # resources can only be accessed by their creator
        label = Label.objects.get(pk=pk, owner=request.user)
    except Label.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LabelSerializer(label)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):
    """GET or POST to the /tasks/ route"""
    if request.method == 'GET':
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    """GET, PUT, or DELETE to the /tasks/<task_id> route"""
    try:
        task = Task.objects.get(pk=pk, owner=request.user)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
