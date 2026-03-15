from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    ChangePasswordView,
)

urlpatterns = [

    # ── Public endpoints ─────────────────────────────────────────────────
    path('register/',        RegisterView.as_view(),       name='user-register'),
    path('login/',           LoginView.as_view(),           name='user-login'),

    # ── Token management ─────────────────────────────────────────────────
    # Exchange a valid refresh token for a new access token
    path('token/refresh/',   TokenRefreshView.as_view(),    name='token-refresh'),

    # ── Protected endpoints (require: Authorization: Bearer <access_token>) ──
    path('logout/',          LogoutView.as_view(),          name='user-logout'),
    path('profile/',         UserProfileView.as_view(),     name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(),  name='change-password'),

]
