from django.urls import path
from .views import FrontendIncidentList

urlpatterns = [
    path("frontend/incidents/", FrontendIncidentList.as_view(), name="frontend-incidents"),
]