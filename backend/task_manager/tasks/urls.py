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

    # ── Authentication (public) ──────────────────────────────────────────
    path('auth/register/', RegisterView.as_view(),  name='auth-register'),
    path('auth/login/',    LoginView.as_view(),     name='auth-login'),

    # ── Authentication (protected) ───────────────────────────────────────
    path('auth/logout/',   LogoutView.as_view(),    name='auth-logout'),
    path('auth/profile/',  UserProfileView.as_view(), name='auth-profile'),

    # ── JWT Token Management ─────────────────────────────────────────────
    # Use the refresh token to get a new access token (built-in view)
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ── Tasks (all protected via IsAuthenticated) ────────────────────────
    path('',         TaskListCreateView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(),    name='task-detail'),

]
