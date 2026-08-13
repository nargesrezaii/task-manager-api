from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer
from apps.tasks.permissions import IsTaskOwner


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated,
        IsTaskOwner,
    ]
    
    def get_queryset(self):
        return Task.objects.filter(
            owner=self.request.user
        )
    
    def perform_create(self, serializer):
        serializer.save(
            owner = self.request.user
        )