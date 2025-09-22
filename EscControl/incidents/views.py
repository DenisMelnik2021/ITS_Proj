from django.shortcuts import render
from .serializers import FrontendIncidentSerializer
from .models import Incident
from rest_framework import generics

# Create your views here.
class FrontendIncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = FrontendIncidentSerializer