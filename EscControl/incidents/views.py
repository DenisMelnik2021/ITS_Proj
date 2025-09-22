from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import FrontendIncidentSerializer, YoloIncidentReportSerializer
from .models import Incident
from django.utils.dateparse import parse_datetime


# Create your views here.
class FrontendIncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.select_related('incident_type', 'escalator').order_by('-created_at')
    serializer_class = FrontendIncidentSerializer

class IncidentViewSet(viewsets.GenericViewSet):
    queryset = Incident.objects.all()

    @action(methods=['post'], detail=False)
    def report(self, request):
        ser = YoloIncidentReportSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()

        ts = ser.initial_data.get('ts')
        if ts:
            dt = parse_datetime(ts)
            if dt:
                obj.created_at = dt
                obj.save(update_fields=['created_at'])
        return Response(FrontendIncidentSerializer(obj).data, status=status.HTTP_201_CREATED)