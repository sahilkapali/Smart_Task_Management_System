from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CustomLoginView,
    RegisterView,
    UserProfileView,
    LoginView,
    LogoutView,
    ChangePasswordView,
)

urlpatterns = [
    path('register/',        RegisterView.as_view(),       name='user-register'),
    path('login/',           LoginView.as_view(),           name='user-login'),
    path('token/refresh/',   TokenRefreshView.as_view(),    name='token-refresh'),
    path('logout/',          LogoutView.as_view(),          name='user-logout'),
    path('profile/',         UserProfileView.as_view(),     name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(),  name='change-password'),
]