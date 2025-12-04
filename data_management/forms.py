from django import forms
from .models import Trip
from .models import Route
from .models import Stop
import re

class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = ['name', 'latitude', 'longitude']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if not name:
            return cleaned_data
        
        name = name.strip()
        cleaned_data['name'] = name

        reg = r'^[a-zA-Z0-9\s-]+$'
        if not re.match(reg, name):
            self.add_error('name', 'Názov zastávky môže obsahovať iba písmená, čísla, medzery a pomlčky.')

        if len(name) < 4 or len(name) > 100:
            self.add_error('name', 'Názov zastávky nemá požadovanú veľkosť (od 4 do 100)')

        return cleaned_data

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'type']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if not name:
            return cleaned_data

        name = name.strip()
        cleaned_data['name'] = name

        reg = r'^[a-zA-Z0-9\s-]+$'
        if not re.match(reg, name):
            self.add_error('name', 'Názov linky môže obsahovať iba písmená, čísla, medzery a pomlčky.')

        if len(name) < 4 or len(name) > 100:
            self.add_error('name', 'Názov linky nemá požadovanú veľkosť (od 4 do 100)')

        return cleaned_data

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['route', 'startStop', 'endStop', 'departureTime', 'arrivalTime']

    def clean(self):
        cleaned_data = super().clean()
        start_stop = cleaned_data.get('start_stop')
        end_stop = cleaned_data.get('end_stop')
        departure_time = cleaned_data.get('departure_time')
        arrival_time = cleaned_data.get('arrival_time')

        if start_stop and end_stop and start_stop == end_stop:
            self.add_error('end_stop', "Začiatočná a koncová zastávka nemôžu byť rovnaké.")

        if departure_time and arrival_time and departure_time >= arrival_time:
            self.add_error('arrival_time', "Čas príchodu musí byť neskôr ako čas odchodu.")

        return cleaned_data