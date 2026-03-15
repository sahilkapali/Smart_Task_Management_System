from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from django.contrib.auth.models import User
from .serializers import MyTokenObtainPairSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "message": "You have successfully accessed a protected route!"
        })

class CustomLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer