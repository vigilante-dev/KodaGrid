from django import forms

from .models import NewsletterSubscriber, Testimonial


class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ('email',)


class TestimonialSubmissionForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('course_completed', 'feedback', 'rating')
        widgets = {
            'course_completed': forms.TextInput(attrs={'autocomplete': 'off'}),
            'feedback': forms.Textarea(attrs={'rows': 4, 'maxlength': 2000}),
            'rating': forms.Select(choices=[(value, f'{value} / 5') for value in range(5, 0, -1)]),
        }
