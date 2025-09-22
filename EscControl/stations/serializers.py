from rest_framework import serializers
from .models import Camera

# Для фронтенда
class FrontendCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['id', 'name', 'station', 'status']

# Для Yolo
class YoloCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['id', 'installed_at', 'coordinates']
