from django import forms

from .models import EventRegistration


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ('name', 'email', 'phone', 'message')
