from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Camera
from .serializers import YoloCameraSerializer, FrontendCameraSerializer


# Create your views here.

# API для фронтенда
class FrontendCameraList(generics.ListCreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = FrontendCameraSerializer

# API для Yolo
class YoloCameraList(generics.ListAPIView):
    queryset = Camera.objects.all()
    serializer_class = YoloCameraSerializer
    authentication_classes = [TokenAuthentication]  # Используем токен-аутентификацию
    permission_classes = [IsAuthenticated]          # Только авторизованные пользователи
