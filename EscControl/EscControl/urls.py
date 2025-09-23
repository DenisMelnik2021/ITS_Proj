"""
URL configuration for EscControl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


# ---- API v1 ----
api_v1_patterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('', include('incidents.api_urls', namespace='incidents_api')),
    #path('', include('stations.urls', namespace='stations_api'))
]

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Для фронта
    path("", include("incidents.frontend_urls", namespace="incidents_frontend")),

    # API — только под /api/
    path("api/", include((api_v1_patterns, "api"), namespace="v1")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)