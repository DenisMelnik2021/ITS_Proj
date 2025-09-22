from rest_framework import serializers
from .models import Incident

class FrontendIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id', 'incident_type', 'escalator', 'created_at', 'confidence', 'status', 'notes']
