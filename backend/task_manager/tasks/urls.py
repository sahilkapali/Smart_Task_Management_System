from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    # Tasks (all protected via IsAuthenticated)
    path('', TaskListCreateView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]