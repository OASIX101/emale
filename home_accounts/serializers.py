from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'gender', 'is_vendor']

class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=500)
