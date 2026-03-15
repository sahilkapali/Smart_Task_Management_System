from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer

#  Task Views

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class   = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user only sees their own tasks
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically attach the logged-in user to the task being created
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only view, update, or delete their own tasks
        return Task.objects.filter(user=self.request.user)