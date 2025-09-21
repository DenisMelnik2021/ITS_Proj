from django.contrib import admin
from stations import models

# Inline для редактирования связей между камерой и эскалаторами
class CameraEscalatorInline(admin.TabularInline):  # или admin.StackedInline
    model = models.CameraEscalator
    extra = 1  # Количество пустых форм для добавления новых связей
    verbose_name_plural = "Эскалаторы"
    verbose_name = "Связь камеры и эскалатора"

class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'installed_at', 'description')
    readonly_fields = ('installed_at',)
    inlines = [CameraEscalatorInline]  # Добавление inline-редактора

admin.site.register(models.Station)
admin.site.register(models.Escalator)
admin.site.register(models.Camera, CameraAdmin)
admin.site.register(models.CameraEscalator)
