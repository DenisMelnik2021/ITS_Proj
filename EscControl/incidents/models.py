from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class IncidentType(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    class Meta:
        verbose_name = 'Тип инцидента'
        verbose_name_plural = 'Типы инцидентов'

    def __str__(self):
        return self.name

class Incident(models.Model):
    id = models.AutoField(primary_key=True)

    incident_type = models.ForeignKey(
        'IncidentType',
        on_delete=models.CASCADE
    )
    
    escalator = models.ForeignKey(
        'stations.Escalator',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    statusChoices = [
        ('Open', 'Открыто'),
        ('Closed', 'Закрыт'),
        ('inprogress', 'В работе'),
    ]
    status = models.CharField(
        choices=statusChoices,
        max_length=25,
        default='Open',
    )

    # screenshot = models.ImageField() - дописать импорт Pillow и добавить поле
    notes = models.TextField()

    class Meta:
        verbose_name = 'Инцидент'
        verbose_name_plural = 'Инциденты'
    
    def __str__(self):
        return f"{self.incident_type} ({self.created_at})"



