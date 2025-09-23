from django.urls import path
from .views import IncidentViewSet


app_name = 'incidents_api'

urlpatterns = [
    path(
        "yolo/incidents/report/",
        IncidentViewSet.as_view({"post": "report"}),
        name="incidents-report",
    ),
]