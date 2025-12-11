from django import forms
from data_management.models import Stop, Trip, Route
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'type']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'type': forms.Select(attrs={'class': 'form-input', 'required': True}),
        }

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['routeID', 'startStopID', 'endStopID', 'departureTime', 'arrivalTime']
        widgets = {
            'routeID': forms.Select(attrs={'class': 'form-input', 'required': True}), 
            'startStopID': forms.Select(attrs={'class': 'form-input', 'required': True}),
            'endStopID': forms.Select(attrs={'class': 'form-input', 'required': True}),

            #'routeID': forms.Select(attrs={'class': 'form-input'}),
            #'routeID': forms.TextInput(attrs={'class': 'form-input', 'required': True}),

            #'startStopID': autocomplete.ModelSelect2(
            #    url='stop-autocomplete', 
            #    attrs={'class': 'form-input'}
            #),
            #'startStopID': forms.TextInput(attrs={'class': 'form-input', 'required': True}),

            #'endStopID': autocomplete.ModelSelect2(
            #    url='stop-autocomplete', 
            #    attrs={'class': 'form-input'}
            #),
            #'endStopID': forms.TextInput(attrs={'class': 'form-input', 'required': True}),

            'departureTime': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'},format='%Y-%m-%dT%H:%M',),
            'arrivalTime': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'},format='%Y-%m-%dT%H:%M',),

        }

    # SERVER-SIDE VALIDATION
    def clean(self):
        cleaned_data = super().clean()
        
        departure_time = cleaned_data.get("departureTime")
        arrival_time = cleaned_data.get("arrivalTime")

        if departure_time and arrival_time:
            if arrival_time <= departure_time:
                raise ValidationError(
                    "Čas príchodu musí byť neskôr ako čas odchodu.",
                    code='invalid_time_order'
                )

        return cleaned_data

class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = ['name', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001', 'min': -90, 'max': 90}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001', 'min': -180, 'max': 180}),
        }

    # SERVER-SIDE VALIDATION
    def clean_name(self):
        name = self.cleaned_data['name']
        
        if len(name) < 5:
             raise forms.ValidationError("Názov zastávky musí mať aspoň 5 znakov.")
        
        name_validator = RegexValidator(
            regex=r'^(?=.*[a-zA-Z])[a-zA-Z0-9 ]{5,}$',
            message="Názov musí obsahovať minimálne 5 znakov, iba písmená, číslice a medzery, pričom aspoň jedno musí byť písmeno."
        )
        
        try:
            name_validator(name)
        except forms.ValidationError as e:
            raise forms.ValidationError(e.message)
            
        return name
    
    def clean_latitude(self):
        lat = self.cleaned_data['latitude']
        if lat < -90 or lat > 90:
            raise forms.ValidationError("Zemepisná šírka musí byť v rozsahu -90 až 90.")
        return lat
    
    def clean_longitude(self):
        lon = self.cleaned_data['longitude']
        if lon < -180 or lon > 180:
            raise forms.ValidationError("Zemepisná dĺžka musí byť v rozsahu -180 až 180.")
        return lon