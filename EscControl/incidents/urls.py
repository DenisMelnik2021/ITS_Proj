from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FrontendIncidentList, IncidentViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incidents')

urlpatterns = [
    path("frontend/incidents/", FrontendIncidentList.as_view(), name="frontend-incidents"),
    path("", include(router.urls)),
]