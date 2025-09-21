from django.contrib import admin
from stations import models

# Inline для связи между эскалатором и камерой
class CameraInline(admin.TabularInline):
    model = models.CameraEscalator
    extra = 0  # Не добавляем пустые формы
    verbose_name_plural = "Камеры"
    verbose_name = "Связь камеры и эскалатора"
    fields = ("camera", "station")  # Отображаемые поля


# Inline для связи между станцией и эскалаторами
class EscalatorInline(admin.TabularInline):
    model = models.Escalator
    extra = 1
    verbose_name_plural = "Эскалаторы"
    verbose_name = "Эскалатор"
    fields = ("number", "status")


# Админ для модели Station
@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "line", "coordinates")
    search_fields = ("name", "line")
    inlines = [EscalatorInline]  # Встраиваем эскалаторы


# Админ для модели Escalator
@admin.register(models.Escalator)
class EscalatorAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "station", "status")
    list_filter = ("status", "station")
    search_fields = ("number", "station__name")
    inlines = [CameraInline]  # Встраиваем камеры


# Админ для модели Camera
@admin.register(models.Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "installed_at", "description")
    readonly_fields = ("installed_at",)
    search_fields = ("description",)


# Админ для модели CameraEscalator
@admin.register(models.CameraEscalator)
class CameraEscalatorAdmin(admin.ModelAdmin):
    list_display = ("id", "camera", "escalator", "station")
    search_fields = ("camera__id", "escalator__id", "station__name")
