from django import forms
from data_management.models import Stop
from django.core.validators import RegexValidator

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