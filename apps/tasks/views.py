from rest_framework import viewsets, filters
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
    
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "priority",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        return Task.objects.filter(
            owner=self.request.user
        )
    
    def perform_create(self, serializer):
        serializer.save(
            owner = self.request.user
        )