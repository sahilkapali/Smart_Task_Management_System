from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


# ─────────────────────────────────────────────
#  Registration
# ─────────────────────────────────────────────

# 1. This is your original Registration Serializer (bringing it back!)
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Registers a new user.
    Both `password` fields are write-only; the second confirms the first.
    """
    password = serializers.CharField(
        write_only=True, required=True, min_length=8,
        style={'input_type': 'password'},
        help_text='Minimum 8 characters.',
    )
    password2 = serializers.CharField(
        write_only=True, required=True,
        style={'input_type': 'password'},
        label='Confirm password',
    )

    class Meta:
        model  = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
        }

    # ── field-level validation ──────────────────────────────────────────

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    # ── object-level validation ─────────────────────────────────────────

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    # ── creation ────────────────────────────────────────────────────────

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


# ─────────────────────────────────────────────
#  Login
# ─────────────────────────────────────────────

class UserLoginSerializer(serializers.Serializer):
    """
    Validates credentials and attaches the authenticated User to attrs.
    No DB writes – purely for input validation.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account has been deactivated.')
        attrs['user'] = user
        return attrs


# ─────────────────────────────────────────────
#  Profile read / update
# ─────────────────────────────────────────────

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Read-only representation of the authenticated user's profile.
    """
    class Meta:
        model  = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff')
        read_only_fields = fields


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Allows the authenticated user to update their own profile.
    Password changes go through a dedicated endpoint, not here.
    """
    class Meta:
        model  = User
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {
            'email': {'required': False},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use by another account.')
        return value


# ─────────────────────────────────────────────
#  Password change
# ─────────────────────────────────────────────

class ChangePasswordSerializer(serializers.Serializer):
    """
    Lets an authenticated user change their password.
    Requires the current password for verification.
    """
    old_password = serializers.CharField(
        required=True, write_only=True,
        style={'input_type': 'password'},
        label='Current password',
    )
    new_password = serializers.CharField(
        required=True, write_only=True, min_length=8,
        style={'input_type': 'password'},
        label='New password',
        help_text='Minimum 8 characters.',
    )
    new_password2 = serializers.CharField(
        required=True, write_only=True,
        style={'input_type': 'password'},
        label='Confirm new password',
    )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'New passwords do not match.'})
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({'new_password': 'New password must differ from the current one.'})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
