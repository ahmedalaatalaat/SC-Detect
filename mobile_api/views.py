from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from main.utils import get_object_or_none
from rest_framework.views import APIView
from rest_framework import status
from django.views import View
from .serializers import *
from random import sample
from .models import *
import json



class RegistrationView(APIView):
    def post(self, request):
        my_user = get_object_or_none(User, username=request.data.get('email').lower())
        if my_user:
            return Response({"code": 701, "error": "user already exists!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            my_user = User.objects.create_user(
                username=request.data.get('email').lower(),
                first_name=request.data.get('name'),
                password=request.data.get('password')
            )
            
            system_user = SystemUser.objects.create(
                phone=request.data.get('phone'),
                image=request.FILES.get('image'),
                birthday=request.data.get('birthday'),
                gender=request.data.get('gender'),
                user=my_user
            )
            
            token = Token.objects.get(user=my_user)
            
            data = {
                "token": str(token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    
    def get(self, request):
        serializer = LoginSerializer(data=request.query_params)
        if serializer.is_valid():
            my_user = get_object_or_none(User, username=request.query_params.get('email').lower())
            if not my_user:
                return Response({"code": 702, "error": "Invalid Email or Password!"}, status=status.HTTP_403_FORBIDDEN)
            
            if my_user.check_password(request.query_params.get('password')):
                token = Token.objects.get(user=my_user)
            
                data = {
                    "token": str(token),
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"code": 702, "error": "Invalid Email or Password!"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        system_user = SystemUser.objects.get(user=request.user)
        
        serializer = ProfileSerializer(system_user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request):
        system_user = SystemUser.objects.get(user=request.user)
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            system_user.phone = request.data.get('phone')
            system_user.gender = request.data.get('gender')
            system_user.birthday = request.data.get('birthday')
            system_user.user.first_name = request.data.get('name')

            if request.FILES.get('image'):
                system_user.image = request.FILES.get('image')
            
            
            system_user.save()
            system_user.user.save()
            
            serializer = ProfileSerializer(system_user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)