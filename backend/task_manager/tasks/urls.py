from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    # Auth
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    # Tasks
    TaskListCreateView,
    TaskDetailView,
)

urlpatterns = [
    # Tasks (all protected via IsAuthenticated)
    path('', TaskListCreateView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
