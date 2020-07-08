import datetime
from django import forms
from free_days_registration.models import FreeDayType, FreeDayRegistration


class DateInput(forms.DateInput):
    input_type = 'date'


class FreeDayRegisterForm(forms.ModelForm):

    class Meta:
        model = FreeDayRegistration
        fields = ['free_day_type', 'start_date', 'end_date', 'note']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'note': forms.Textarea
        }
        labels = {
            'free_day_type': 'Rodzaj urlopu',
            'start_date': 'Data początku urlopu',
            'end_date': 'Data końca urlopu',
            'note': 'Informacja do przełożonego'
        }
