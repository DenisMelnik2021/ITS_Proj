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
        constrains = [
            models.UniqueConstraint(fields=['name', 'line'], name='unique_station_per_line')
        ]

    def __str__(self):
        return f"{self.name} ({self.line})"