from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet
from django.urls import path
from . import views


router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incidents')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stations/', views.stations, name='stations'),
    path('incidents/', views.incidents, name='incidents'),
    path('analytics/', views.analytics, name='analytics'),
    path("a/", include(router.urls)),
]