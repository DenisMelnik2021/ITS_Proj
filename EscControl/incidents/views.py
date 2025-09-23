from django.shortcuts import render
from .models import Incident
from stations.models import Station, Escalator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.dateparse import parse_datetime
from .serializers import YoloIncidentReportSerializer
from .models import Incident
from django.utils import timezone
from django.db.models import Count
import logging
import json


#Frontend

def dashboard(request):
    """Основная страница с информацией"""
    total_escalators = Escalator.objects.count()
    working_escalators = Escalator.objects.filter(status='working').count()
    incidents_count = Incident.objects.count()
    recent_incidents = Incident.objects.order_by('-created_at')[:5]
    
    # Получаем станции с эскалаторами для карты
    stations_data = {}
    stations = Station.objects.prefetch_related('escalators').all()
    
    for station in stations:
        # Подсчитываем статистику по эскалаторам для каждой станции
        station_escalators = station.escalators.all()
        working_count = station_escalators.filter(status='working').count()
        not_working_count = station_escalators.filter(status='not_working').count()
        maintenance_count = station_escalators.filter(status='under_maintenance').count()
        
        # Получаем последние инциденты для станции
        station_incidents = Incident.objects.filter(
            escalator__station=station
        ).order_by('-created_at')[:3]
        
        stations_data[station.id] = {
            'id': station.id,
            'name': station.name,
            'line': station.line,
            'coordinates': station.coordinates,
            'total_escalators': station_escalators.count(),
            'working_escalators': working_count,
            'not_working_escalators': not_working_count,
            'maintenance_escalators': maintenance_count,
            'recent_incidents': [
                {
                    'type': incident.incident_type.name if incident.incident_type else 'Неизвестный',
                    'created_at': incident.created_at.strftime('%d.%m.%Y %H:%M'),
                    'escalator_number': incident.escalator.number
                }
                for incident in station_incidents
            ]
        }
    
    context = {
        'total_escalators': total_escalators,
        'working_escalators': working_escalators,
        'incidents_count': incidents_count,
        'recent_incidents': recent_incidents,
        'stations_data': json.dumps(stations_data),  # JSON для JavaScript
        'stations_data_raw': stations_data,  # Сырые данные для отладки
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
    agg = (
        Incident.objects
        .values('incident_type')
        .annotate(total=Count('id'))
        .order_by('-total', 'incident_type')
    )

    labels = [(row['incident_type'] or 'Неизвестный тип') for row in agg]
    data = [row['total'] for row in agg]

    context = {
        'chart_labels': json.dumps(labels, ensure_ascii=False),
        'chart_data': json.dumps(data, ensure_ascii=False),
        'total_incidents': Incident.objects.count(),
        'total_stations': Station.objects.count(),
        'total_escalators': Escalator.objects.count(),
    }
    return render(request, 'incidents/analytics.html', context)

# API

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