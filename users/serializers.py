from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ProviderApplication


# ===========================
# USER REGISTER
# ===========================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'address']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            name=validated_data['name'],
            password=validated_data['password'],
            address=validated_data.get('address'),
            role='USER'
        )
        return user


# ===========================
# USER LOGIN
# ===========================

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['email'],   # important
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        data['user'] = user
        return data


# ===========================
# PROVIDER APPLY
# ===========================

class ProviderApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderApplication
        fields = [
            'service_type',
            'experience',
            'skills',
            'available',
            'status'
        ]
        read_only_fields = ['status']


# ===========================
# USER PROFILE (OPTIONAL BUT USEFUL)
# ===========================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'address',
            'role',
            'latitude',
            'longitude'
        ]