from django.contrib import admin
from stations import models

admin.site.register(models.station)
admin.site.register(models.escalator)

