from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User
import re

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']  # phone odstránený
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Používateľské meno',
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Heslo',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Potvrdenie hesla',
        })

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = 'Zadajte rovnaké heslo ako predtým, pre overenie.'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise ValidationError('Používateľské meno musí mať aspoň 4 znaky.')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Používateľské meno môže obsahovať len písmená, čísla a podčiarkovník.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Toto používateľské meno je už obsadené.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Neplatný formát emailu.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Tento email je už registrovaný.')
        return email.lower()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2:
            raise ValidationError('Meno musí mať aspoň 2 znaky.')
        if not re.match(r'^[a-zA-ZáäčďéíľĺňóôŕšťúýžÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ\s-]+$', first_name):
            raise ValidationError('Meno obsahuje nepovolené znaky.')
        return first_name.strip()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 2:
            raise ValidationError('Priezvisko musí mať aspoň 2 znaky.')
        if not re.match(r'^[a-zA-ZáäčďéíľĺňóôŕšťúýžÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ\s-]+$', last_name):
            raise ValidationError('Priezvisko obsahuje nepovolené znaky.')
        return last_name.strip()
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Heslá sa nezhodujú.')

            if len(password1) < 8:
                raise ValidationError('Heslo musí mať aspoň 8 znakov.')
            if not re.search(r'[A-Z]', password1):
                raise ValidationError('Heslo musí obsahovať aspoň jedno veľké písmeno.')
            if not re.search(r'[a-z]', password1):
                raise ValidationError('Heslo musí obsahovať aspoň jedno malé písmeno.')
            if not re.search(r'[0-9]', password1):
                raise ValidationError('Heslo musí obsahovať aspoň jedno číslo.')
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
                raise ValidationError('Heslo musí obsahovať aspoň jeden špeciálny znak (!@#$%^&* atď.).')
        
        return password2

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Meno',
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Priezvisko',
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Tento email je už registrovaný.')
        return email.lower()

class AdminUserEditForm(forms.ModelForm):
    """Formulár pre admina na úpravu používateľov"""
    
    is_staff = forms.BooleanField(
        required=False,
        label='Admin práva',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Meno',
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Priezvisko',
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Používateľské meno',
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Tento email je už registrovaný.')
        return email.lower()