from django.urls import path
from . import views


app_name = 'incidents_frontend'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stations/', views.stations, name='stations'),
    path('incidents/', views.incidents, name='incidents'),
    path('analytics/', views.analytics, name='analytics'),
]