from django import forms
from .models import Stop, Route, Trip, Vehicle
import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = ['name', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'latitude': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.000001', 'min': -90, 'max': 90}),
            'longitude': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.000001', 'min': -180, 'max': 180}),
        }

    def clean_latitude(self):
        lat = self.cleaned_data.get('latitude')
        if lat < - 90 or lat > 90:
            raise forms.ValidationError("Zemepisná šírka musí byť v rozsahu od -90 do 90.")
        return lat
        
    def clean_longitude(self):
        lon = self.cleaned_data.get('longitude')
        if lon < - 180 or lon > 180:
            raise forms.ValidationError("Zemepisná dĺžka musí byť v rozsahu od -180 do 180.")
        return lon

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        
        if len(name) < 5:
             raise ValidationError("Názov zastávky musí mať aspoň 5 znakov.")

        reg = r'^[a-zA-Z0-9\s.,\-áäčďéíľĺňóôŕšťúýžÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ.,]+$'
        
        if not re.match(reg, name):
            raise ValidationError("Názov zastávky obsahuje nepovolené znaky (povolené sú písmená, čísla, medzery, pomlčky, bodky a čiarky).")

        qs = Stop.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Zastávka s týmto názvom už existuje.")
            
        return name

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'start_stop', 'end_stop']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'start_stop': forms.Select(attrs={'class': 'form-input'}),
            'end_stop': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 4:
            raise ValidationError("Názov linky musí mať aspoň 4 znaky.")
        return name

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['route', 'vehicleID', 'departure_time', 'arrival_time']
        widgets = {
            'route': forms.Select(attrs={'class': 'form-input', 'required': True}),
            'vehicleID': forms.Select(attrs={'class': 'form-input'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}, format='%H:%M'),
            'arrival_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}, format='%H:%M'),
        }

    def clean(self):
        cleaned_data = super().clean()
        dep = cleaned_data.get('departure_time')
        arr = cleaned_data.get('arrival_time')
        vehicle = cleaned_data.get('vehicleID')

        if dep and arr and dep >= arr:
            raise ValidationError({'arrival_time': "Čas príchodu musí byť neskôr ako čas odchodu."})

        if vehicle and dep and arr:
            overlapping_trips = Trip.objects.filter(
                vehicleID=vehicle,
                departure_time__lt=arr,
                arrival_time__gt=dep
            )
            if self.instance.pk:
                overlapping_trips = overlapping_trips.exclude(pk=self.instance.pk)

            if overlapping_trips.exists():
                collision = overlapping_trips.first()
                raise ValidationError({
                    'vehicleID': f"Vozidlo {vehicle} je v tomto čase už obsadené spojom na linke {collision.route.name} "
                                 f"({collision.departure_time.strftime('%H:%M')} - {collision.arrival_time.strftime('%H:%M')})."
                })

        return cleaned_data

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'vehicle_type', 'capacity']
        widgets = {
            'registration_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'napr. ZA-123AB'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-input'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
        }

    def clean_registration_number(self):
        return self.cleaned_data.get('registration_number', '').upper()