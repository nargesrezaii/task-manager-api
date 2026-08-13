from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(
            owner = self.request.user    
        )
    
    def perform_create(self, serializer):
        serializer.save(
            owner = self.request.user    
        )
        

class TaskDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filer(
            owner=self.request.user
        )
    