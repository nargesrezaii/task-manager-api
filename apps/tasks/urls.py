from django.urls import path

from apps.tasks.views import (
    TaskListCreateView,
    TaskDetailView,
)

urlpatterns = [
    path(
        '',
         TaskListCreateView.as_view(),
         name='task-list-create',
    ),   
    path(
        '<int:pk>/',
         TaskDetailView.as_view(),
         name='task-detail',
    ),    
]