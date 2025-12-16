from django.db import models

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=20, unique=True, verbose_name='ŠPZ / Evidenčné číslo')
    capacity = models.PositiveIntegerField(verbose_name='Kapacita cestujúcich')
    model_name = models.CharField(max_length=100, verbose_name='Model vozidla')

    class Meta:
        verbose_name = 'Vozidlo'
        verbose_name_plural = 'Vozidlá'

    def __str__(self):
        return f"{self.model_name} ({self.registration_number})"

class Stop(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Názov zastávky')
    latitude = models.FloatField(verbose_name='Zemepisná šírka')
    longitude = models.FloatField(verbose_name='Zemepisná dĺžka')

    class Meta:
        verbose_name = 'Zastávka'
        verbose_name_plural = 'Zastávky'

    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='číslo alebo názov linky')
    
    TYPE_CHOICES = [
        ('bus', 'Autobus'),
        ('trolley', 'Trolejbus'),
        ('tram', 'Električka')
    ]

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name='Typ dopravy'
    )

    class Meta:
        verbose_name = 'Linka'
        verbose_name_plural = 'Linky'

    def __str__(self):
        return f'Linka {self.name}'

class Trip(models.Model):
    routeID = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Linka')
    vehicleID = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Priradené vozidlo')
    startStopID = models.ForeignKey(Stop, related_name='trip_start', on_delete=models.CASCADE, verbose_name='Začiatočná zastávka')
    endStopID = models.ForeignKey(Stop, related_name='trip_end', on_delete=models.CASCADE, verbose_name='Koncová zastávka')

    departureTime = models.DateTimeField(verbose_name='čas odchodu')
    arrivalTime = models.DateTimeField(verbose_name='čas príchodu')

    class Meta:
        verbose_name = 'Spoj'
        verbose_name_plural = 'Spoje'

    def __str__(self):
        return f"Spoj linky {self.routeID}, zaciatok {self.startStopID}, koniec {self.endStopID}"