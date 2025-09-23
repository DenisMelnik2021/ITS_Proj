from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Station(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=100,
        verbose_name='Название станции',
    )

    line = models.CharField(
        max_length=100,
        verbose_name='Название линии',
    )

    coordinates = models.CharField(
        max_length=200,
        null=True, blank=True,
        verbose_name='Координаты станции',
    )

    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'
        constraints = [
            models.UniqueConstraint(fields=['name', 'line'], name='unique_station_per_line')
        ]

    def __str__(self):
        return f"{self.name} ({self.line})"
    

class Escalator(models.Model):
    id = models.AutoField(primary_key=True)

    station = models.ForeignKey(
        'Station',
        on_delete=models.CASCADE,
        verbose_name="Станция",
        db_index=True,
        related_name='escalators'  # добавляем это
    )

    number = models.IntegerField(
        verbose_name='Номер эскалатора',
    )

    STATUS_WORKING = "working"
    STATUS_NOT_WORKING = "not_working"
    STATUS_UNDER_MAINTENANCE = "under_maintenance"

    STATUS_CHOICES = [
        (STATUS_WORKING, "работает"),
        (STATUS_NOT_WORKING, "не работает"),
        (STATUS_UNDER_MAINTENANCE, "обслуживается"),
    ]
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=25,
        default=STATUS_WORKING,
    )

    class Meta:
        verbose_name = 'Эскалатор'
        verbose_name_plural = 'Эскалаторы'
        constraints = [
            models.UniqueConstraint(fields=['station', 'number'], name='unique_escalator_per_station'),
        ]

    def __str__(self):
        return f"Эскалатор № {self.number} ({self.station})"
    

class Camera(models.Model):
    id = models.AutoField(primary_key=True)

    station = models.ForeignKey(
        'Station',
        on_delete=models.CASCADE,
        verbose_name="Станция",
        related_name='cameras',
    )

    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_IN_MAINTENANCE = "in_maintenance"
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "активна"),
        (STATUS_INACTIVE, "неактивна"),
        (STATUS_IN_MAINTENANCE, "в обслуживании"),
    ]
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=25,
        default=STATUS_ACTIVE,
    )

    installed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата установки',
    )

    description = models.TextField(
        verbose_name='Описание камеры',
        null=True,
    )

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        constraints = [
            models.UniqueConstraint(fields=['id'], name='unique_camera_id')
        ]

    def __str__(self):
        return f"Камера {self.id} ({self.station})"

class CameraEscalator(models.Model): # Переходная модель для связи
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE)
    escalator = models.ForeignKey('Escalator', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь камеры и эскалатора'
        verbose_name_plural = 'Связи камер и эскалаторов'

        constraints = [
            # Все эскалаторы, связанные с одной камерой, должны быть на одной станции
            models.UniqueConstraint(
                fields=['camera', 'escalator'],
                name='unique_camera_escalator_pair',
            )
        ]

    def clean(self):
        if self.escalator.station != self.camera.station:
            raise ValidationError('Эскалатор и камера должны быть на одной станции.')
        
    def __str__(self):
        return f"{self.camera} → {self.escalator}"
