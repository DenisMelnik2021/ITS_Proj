from django.shortcuts import render
from .models import Incident
from stations.models import Station, Escalator

def dashboard(request):
    """Основная страница с информацией"""
    total_escalators = Escalator.objects.count()
    working_escalators = Escalator.objects.filter(status='working').count()
    incidents_count = Incident.objects.count()
    recent_incidents = Incident.objects.order_by('-created_at')[:5]
    
    context = {
        'total_escalators': total_escalators,
        'working_escalators': working_escalators,
        'incidents_count': incidents_count,
        'recent_incidents': recent_incidents,
    }
    return render(request, 'incidents/dashboard.html', context)

def stations(request):
    """Страница со списком станций и эскалаторами"""
    stations_with_escalators = Station.objects.prefetch_related('escalators')
    context = {
        'stations': stations_with_escalators,
    }
    return render(request, 'incidents/stations.html', context)

def incidents(request):
    """Страница с инцидентами"""
    incidents = Incident.objects.select_related('escalator__station', 'incident_type').order_by('-created_at')
    context = {
        'incidents': incidents,
    }
    return render(request, 'incidents/incidents.html', context)

def analytics(request):
    """Страница с аналитическими отчётами"""
    context = {}
    return render(request, 'incidents/analytics.html', context)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.dateparse import parse_datetime
from .serializers import YoloIncidentReportSerializer
from .models import Incident
from django.utils import timezone
import logging


# Create your views here.

logger = logging.getLogger(__name__)
class IncidentViewSet(viewsets.GenericViewSet):
    queryset = Incident.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='report')
    def report(self, request):
        ser = YoloIncidentReportSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        obj = ser.save()

        raw_ts = ser.validated_data.get('ts') or request.data.get('ts')
        if raw_ts:
            dt = parse_datetime(raw_ts)
            if dt:
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone.utc)
                obj.created_at = dt
                obj.save(update_fields=['created_at'])
            else:
                logger.warning(
                    "YOLO ts parse failed; keeping created_at auto. incident_id=%s ts=%r",
                    obj.id,
                    raw_ts
                )

        payload = {
            "id": obj.id,
            "created_at": obj.created_at.isoformat(),
            "status": obj.status,
        }

        return Response(payload, status=status.HTTP_201_CREATED)

