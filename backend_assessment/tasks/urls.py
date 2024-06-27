from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import label_list, label_detail, task_list, task_detail

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('labels/', label_list, name='label-list'),
    path('labels/<int:pk>/', label_detail, name='label-detail'),
    path('tasks/', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),
]
