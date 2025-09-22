from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stations/', views.stations, name='stations'),
    path('incidents/', views.incidents, name='incidents'),
    path('analytics/', views.analytics, name='analytics'),
]