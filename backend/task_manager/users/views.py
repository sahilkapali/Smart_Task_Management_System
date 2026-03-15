from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
)


# ─────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────

def get_tokens_for_user(user):
    """Return a JWT access + refresh token pair for *user*."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


# ─────────────────────────────────────────────
#  Register
# ─────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    """
    POST /api/users/register/
    Public – creates a new user and returns JWT tokens immediately.

    Request body:
        {
            "username":  "alice",
            "email":     "alice@example.com",
            "password":  "strongpass123",
            "password2": "strongpass123"
        }

    Success 201:
        {
            "message": "Account created successfully.",
            "user":   { "id": 1, "username": "alice", "email": "..." },
            "tokens": { "access": "...", "refresh": "..." }
        }
    """
    queryset           = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class   = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user   = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(
            {
                'message': 'Account created successfully.',
                'user': {
                    'id':       user.id,
                    'username': user.username,
                    'email':    user.email,
                },
                'tokens': tokens,
            },
            status=status.HTTP_201_CREATED,
        )


# ─────────────────────────────────────────────
#  Login
# ─────────────────────────────────────────────

class LoginView(APIView):
    """
    POST /api/users/login/
    Public – authenticates credentials and returns JWT tokens.

    Request body:
        { "username": "alice", "password": "strongpass123" }

    Success 200:
        {
            "message": "Login successful.",
            "user":    { "id": 1, "username": "alice", "email": "..." },
            "tokens":  { "access": "...", "refresh": "..." }
        }
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user   = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)

        return Response(
            {
                'message': 'Login successful.',
                'user': {
                    'id':       user.id,
                    'username': user.username,
                    'email':    user.email,
                },
                'tokens': tokens,
            },
            status=status.HTTP_200_OK,
        )


# ─────────────────────────────────────────────
#  Logout
# ─────────────────────────────────────────────

class LogoutView(APIView):
    """
    POST /api/users/logout/
    Protected – blacklists the refresh token so it cannot mint new access tokens.

    Request body:
        { "refresh": "<refresh_token>" }

    Success 205:
        { "message": "Logged out successfully." }
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {'error': 'Token is invalid or has already been blacklisted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': 'Logged out successfully.'},
            status=status.HTTP_205_RESET_CONTENT,
        )


# ─────────────────────────────────────────────
#  Profile – read & update
# ─────────────────────────────────────────────

class UserProfileView(APIView):
    """
    GET   /api/users/profile/  – return the authenticated user's full profile.
    PATCH /api/users/profile/  – update first_name, last_name, or email.

    Both methods require:  Authorization: Bearer <access_token>
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(
            {
                **serializer.data,
                'message': 'You have successfully accessed a protected route!',
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Profile updated successfully.',
                'user': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ─────────────────────────────────────────────
#  Password change
# ─────────────────────────────────────────────

class ChangePasswordView(APIView):
    """
    POST /api/users/change-password/
    Protected – changes the authenticated user's password.
    All active sessions remain valid; issue a fresh token pair if needed.

    Request body:
        {
            "old_password":  "currentpass",
            "new_password":  "newstrongpass",
            "new_password2": "newstrongpass"
        }

    Success 200:
        { "message": "Password changed successfully." }
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Password changed successfully. Please log in again with your new password.'},
            status=status.HTTP_200_OK,
        )
