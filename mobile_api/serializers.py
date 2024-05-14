from rest_framework import serializers
from .models import *

class RegistrationSerializer(serializers.Serializer):
    gender_types = (
        ("M", "Male"),
        ("F", "Female"),
    )
    
    email = serializers.EmailField()
    name = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(min_length=8, max_length=20)
    gender = serializers.ChoiceField(gender_types)
    birthday = serializers.DateField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=20)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.username', required=False)
    name = serializers.CharField(source="user.first_name")
    
    
    class Meta:
        model = SystemUser
        fields = ["name", "email", "phone", "image", 'birthday', 'gender']


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, max_length=20)
    new_password = serializers.CharField(min_length=8, max_length=20)


class SCDHistorySerializer(serializers.ModelSerializer):
    diagnose = serializers.CharField(required=False)
    
    class Meta:
        model = SCDHistory
        fields = ["id", "timestamp", "diagnose", "image"]
