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
    )

    number = models.IntegerField(
        verbose_name='Номер эскалатора',
    )

    status_choices = [
        ("working", "Работает"),
        ("notWorking", "Не работает"),
        ("mainTenance", "В обслуживании"),
    ]
    status = models.CharField(
        choices=status_choices,
        max_length=25,
        default="working",
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

    # Поля для хранения информации о камере (связь с несколькими эскалаторами)
    escalators = models.ManyToManyField(
        'Escalator',
        verbose_name="Эскалаторы",
        related_name='cameras',
        through="CameraEscalator", # Переходная модель для связи
    )

    cam_status_choices = [
        ("working", "Работает"),
        ("notWorking", "Не работает"),
        ("mainTenance", "В обслуживании"),
    ]
    status = models.CharField(
        choices=cam_status_choices,
        max_length=25,
        default="working",
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
        return f"Камера {self.id} ({', '.join(str(e) for e in self.escalators.all())})"

class CameraEscalator(models.Model): # Переходная модель для связи
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE)
    escalator = models.ForeignKey('Escalator', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)

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
        if self.escalator.station != self.station:
            raise ValidationError('Эскалатор и камера должны быть на одной станции.')
        
    def __str__(self):
        return f"Связь {self.camera}"
