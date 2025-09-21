from django.contrib import admin
from stations import models

# Inline для связи между эскалатором и камерой
class CameraInline(admin.TabularInline):
    model = models.CameraEscalator
    extra = 1
    verbose_name_plural = "Эскалаторы"
    verbose_name = "Связь камеры и эскалатора"
    autocomplete_fields = ["escalator"]  # Для удобства выбора


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


# Админ для модели Camera
@admin.register(models.Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ("id", "station", "status", "installed_at", "description")
    search_fields = ("station__name", "description")
    inlines = [CameraInline]  # Встраиваем связи с эскалаторами
    list_filter = ("status", "station")  # Фильтр по статусу и станции


# Админ для модели CameraEscalator
@admin.register(models.CameraEscalator)
class CameraEscalatorAdmin(admin.ModelAdmin):
    list_display = ("camera", "escalator")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "escalator":
            # Если выбрана камера — фильтруем эскалаторы по её станции
            camera_id = request.GET.get("camera")
            if camera_id:
                try:
                    camera = models.Camera.objects.get(id=camera_id)
                    kwargs["queryset"] = models.Escalator.objects.filter(station=camera.station)
                except models.Camera.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            obj.save()
        except Exception as e:
            self.message_user(request, f"Ошибка: {e}", level="error")
            raise