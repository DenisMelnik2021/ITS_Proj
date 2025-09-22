from rest_framework import serializers
from .models import *
from stations.models import Escalator

class FrontendIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id', 'incident_type', 'escalator', 'created_at', 'confidence', 'status', 'notes', 'screenshot']

class YoloIncidentReportSerializer(serializers.ModelSerializer):
    incident_type = serializers.PrimaryKeyRelatedField(queryset=IncidentType.objects.all())
    escalator = serializers.PrimaryKeyRelatedField(queryset=Escalator.objects.all())
    ts = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = Incident
        fields = ['id', 'incident_type', 'escalator', 'confidence', 'status', 'screenshot', 'notes', 'created_at', 'ts']
        read_only_fields = ['id', 'created_at']