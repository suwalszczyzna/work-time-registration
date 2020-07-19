from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import TimeRegistration


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CorrectionForm(forms.ModelForm):
    class Meta:
        model = TimeRegistration
        fields = ['arrival', 'leaving']
        widgets = {
            'arrival': forms.TimeInput(),
            'leaving': forms.TimeInput(),
        }

        labels = {
            'arrival': 'Przyjazd do pracy',
            'leaving': 'Wyjście z pracy'
        }