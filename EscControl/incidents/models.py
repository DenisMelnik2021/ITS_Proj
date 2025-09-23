import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class IncidentType(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(blank=True)

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

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_CLOSED = "closed"
    STATUS_INCORRECT_ORDER = "incorrect_order"
    
    STATUS_CHOICES = [
        (STATUS_NEW, "Новый"),
        (STATUS_IN_PROGRESS, "В обработке"),
        (STATUS_CLOSED, "Закрыт"),
        (STATUS_INCORRECT_ORDER, "Ложное срабатывание")
    ]
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=25,
        default=STATUS_NEW,
    )

    screenshot = models.ImageField(
        upload_to="incident_screenshots/",
    )

    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Инцидент'
        verbose_name_plural = 'Инциденты'

    def __str__(self):
        return f"{self.incident_type} ({self.created_at})"

@receiver(post_delete, sender=Incident)
def delete_screenshot(sender, instance, **kwargs):
    if instance.screenshot:
        if os.path.exists(instance.screenshot.path):
            os.remove(instance.screenshot.path)

