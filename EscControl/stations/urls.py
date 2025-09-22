from django.urls import path
from .views import FrontendCameraList, YoloCameraList

urlpatterns = [
    path("frontend/cameras/", FrontendCameraList.as_view(), name="frontend-cameras"),
    path("yolo/cameras/", YoloCameraList.as_view(), name="yolo-cameras"),
]
