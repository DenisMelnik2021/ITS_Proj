from django.db import models

# Create your models here.
class station(models.Model):
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
    

class escalator(models.Model):
    id = models.AutoField(primary_key=True)

    station = models.ForeignKey(
        'station',
        on_delete=models.CASCADE,
        verbose_name="Станция",
        db_index=True,
    )

    number = models.IntegerField(
        verbose_name='Номер эскалатора',
    )

    status_choices = [
        ("working", "Работает"),
        ("not_working", "Не работает"),
        ("maintenance", "В обслуживании"),
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
        return f"{self.number} ({self.station})"
    
