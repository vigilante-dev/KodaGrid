from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Student


class StudentRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    career_interest = forms.CharField(max_length=120, required=False)

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'career_interest', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists() or Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        parts = self.cleaned_data['name'].split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                career_interest=self.cleaned_data.get('career_interest', ''),
            )
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'email', 'profile_picture', 'career_interest', 'bio')
