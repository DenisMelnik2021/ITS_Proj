from django.contrib import admin
from incidents import models

# Register your models here.
admin.site.register(models.Incident)
admin.site.register(models.IncidentType)
