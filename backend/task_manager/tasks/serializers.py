from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Task


# ─────────────────────────────────────────────
#  Auth Serializers
# ─────────────────────────────────────────────

class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles new-user registration.
    `password` is write-only and confirmed via `password2`.
    """
    password = serializers.CharField(
        write_only=True, required=True, min_length=8,
        style={'input_type': 'password'},
        help_text='At least 8 characters.'
    )
    password2 = serializers.CharField(
        write_only=True, required=True,
        style={'input_type': 'password'},
        label='Confirm password'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True},
        }

    # ---------- validation ----------

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    # ---------- creation ----------

    def create(self, validated_data):
        validated_data.pop('password2')          # remove confirmation field
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Validates credentials and returns the authenticated User object.
    Does NOT create / update anything in the DB.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password'],
        )
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account has been disabled.')
        attrs['user'] = user
        return attrs


# ─────────────────────────────────────────────
#  Task Serializer  (unchanged)
# ─────────────────────────────────────────────

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']
