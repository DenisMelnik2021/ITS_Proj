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