from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    ChangePasswordView
)

urlpatterns = [
    # Authentication (public)
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),

    # Authentication (protected)
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/profile/', UserProfileView.as_view(), name='auth-profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='auth-change-password'),

    # JWT Token Management
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]