from django.contrib import admin
from stations import models

admin.site.register(models.Station)
admin.site.register(models.Escalator)
admin.site.register(models.Camera)
admin.site.register(models.CameraEscalator)
