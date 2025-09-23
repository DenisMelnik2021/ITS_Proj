from django.contrib import admin
from incidents import models

# Register your models here.

@admin.register(models.Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'incident_type', 'escalator', 'status')

@admin.register(models.IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')