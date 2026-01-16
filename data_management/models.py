from django.db import models
from django.utils import timezone

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('bus', 'Autobus'),
        ('tram', 'Električka'),
        ('trolleybus', 'Trolejbus'),
    ]
    
    registration_number = models.CharField(max_length=20, unique=True, verbose_name='ŠPZ')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, verbose_name='Typ vozidla')
    capacity = models.IntegerField(verbose_name='Kapacita', default=50)
    
    def __str__(self):
        return f"{self.registration_number} ({self.get_vehicle_type_display()})"
    
    class Meta:
        verbose_name = 'Vozidlo'
        verbose_name_plural = 'Vozidlá'


class Stop(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Názov zastávky')
    latitude = models.FloatField(verbose_name='Zemepisná šírka')
    longitude = models.FloatField(verbose_name='Zemepisná dĺžka')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Vytvorená')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Aktualizovaná')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Zastávka'
        verbose_name_plural = 'Zastávky'
        ordering = ['name']


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Číslo/Názov linky')
    start_stop = models.ForeignKey(Stop, on_delete=models.PROTECT, related_name='routes_start', verbose_name='Začiatočná zastávka')
    end_stop = models.ForeignKey(Stop, on_delete=models.PROTECT, related_name='routes_end', verbose_name='Koncová zastávka')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Vytvorená')
    
    def __str__(self):
        return f"{self.name} ({self.start_stop} → {self.end_stop})"
    
    class Meta:
        verbose_name = 'Linka'
        verbose_name_plural = 'Linky'
        ordering = ['name']


class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Linka')
    departure_time = models.TimeField(verbose_name='Čas odchodu')
    arrival_time = models.TimeField(verbose_name='Čas príchodu')
    vehicleID = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Vozidlo', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Vytvorený')
    
    def __str__(self):
        return f"{self.route} - {self.departure_time}"
    
    class Meta:
        verbose_name = 'Spoj'
        verbose_name_plural = 'Spoje'
        ordering = ['departure_time']