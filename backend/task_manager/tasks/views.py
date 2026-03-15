from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task
from .serializers import TaskSerializer, RegisterSerializer, LoginSerializer


# ─────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────

def get_tokens_for_user(user):
    """
    Generate a JWT refresh + access token pair for *user*.
    Returns a plain dict so it can be embedded in any response.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


# ─────────────────────────────────────────────
#  Auth Views
# ─────────────────────────────────────────────

class RegisterView(APIView):
    """
    POST /api/auth/register/
    Public endpoint – creates a new user and returns JWT tokens.

    Request body:
        {
            "username": "john",
            "email":    "john@example.com",
            "password":  "strongpass123",
            "password2": "strongpass123"
        }

    Success (201):
        {
            "message": "User registered successfully.",
            "user":    { "id": 1, "username": "john", "email": "john@example.com" },
            "tokens":  { "refresh": "...", "access": "..." }
        }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    'message': 'User registered successfully.',
                    'user': {
                        'id':       user.id,
                        'username': user.username,
                        'email':    user.email,
                    },
                    'tokens': tokens,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/auth/login/
    Public endpoint – authenticates a user and returns JWT tokens.

    Request body:
        { "username": "john", "password": "strongpass123" }

    Success (200):
        {
            "message": "Login successful.",
            "user":    { "id": 1, "username": "john", "email": "john@example.com" },
            "tokens":  { "refresh": "...", "access": "..." }
        }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Protected endpoint – blacklists the refresh token so it can no longer
    be used to generate new access tokens.

    Request body:
        { "refresh": "<refresh_token>" }

    Success (205):
        { "message": "Logout successful." }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()           # requires INSTALLED_APPS: rest_framework_simplejwt.token_blacklist
            return Response(
                {'message': 'Logout successful.'},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {'error': 'Invalid or already-expired token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserProfileView(APIView):
    """
    GET /api/auth/profile/
    Protected endpoint – returns the authenticated user's profile.
    No request body needed; identity is taken from the JWT in the
    Authorization header.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                'id':           user.id,
                'username':     user.username,
                'email':        user.email,
                'date_joined':  user.date_joined,
                'is_staff':     user.is_staff,
            },
            status=status.HTTP_200_OK,
        )


# ─────────────────────────────────────────────
#  Task Views  (protected – unchanged logic)
# ─────────────────────────────────────────────

class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/tasks/   – list all tasks owned by the authenticated user.
    POST /api/tasks/   – create a new task for the authenticated user.
    Requires: Authorization: Bearer <access_token>
    """
    serializer_class   = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/tasks/<id>/  – retrieve a task.
    PUT    /api/tasks/<id>/  – full update.
    PATCH  /api/tasks/<id>/  – partial update.
    DELETE /api/tasks/<id>/  – delete.
    Requires: Authorization: Bearer <access_token>
    """
    serializer_class   = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
