from django.db import models

# Create your models here.
class IncidentType(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

class Incident(models.Model):
    id = models.AutoField(primary_key=True)

    incidentType = models.ForeignKey(
        'IncidentType',
        on_delete=models.CASCADE
    )
    
    escalator = models.ForeignKey(
        'Escalator',
        on_delete=models.CASCADE
    )

    timestamps = models.DateTimeField()
    confidence = models.FloatField()

    statusChoices = [
        ('Open', 'Открыто'),
        ('Closed', 'Закрыт')
        ('inprogress', 'В работе'),
    ]
    status = models.CharField(
        choices=statusChoices,
        max_length=25,
        default='Open',
    )

    screenshot = models.ImageField()
    notes = models.TextField()


