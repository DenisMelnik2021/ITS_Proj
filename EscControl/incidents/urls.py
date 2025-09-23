from django.urls import path, include

urlpatterns = [
    # фронт
    path("", include("incidents.frontend_urls", namespace="incidents_frontend")),
]