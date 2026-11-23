from django import forms
from django.core.validators import FileExtensionValidator

MAX_DOCUMENT_UPLOAD_MB = 10


def validate_upload_size(upload, limit_mb=MAX_DOCUMENT_UPLOAD_MB):
    if upload and hasattr(upload, 'size') and upload.size > limit_mb * 1024 * 1024:
        raise forms.ValidationError(f'Files must be smaller than {limit_mb} MB.')
    return upload

from .models import Assignment, ChatMessage, ChatRoom, Classroom, MentorAIInteraction, MentorshipBooking, Submission, TrainerApplication


class JoinClassForm(forms.Form):
    class_code = forms.CharField(
        max_length=12,
        label='Class code',
        widget=forms.TextInput(attrs={'placeholder': 'CSA101', 'autocomplete': 'off'}),
    )

    def clean_class_code(self):
        return self.cleaned_data['class_code'].strip().upper()


class CreateClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ('name', 'learning_path', 'description', 'meeting_link', 'start_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AssignmentSubmissionForm(forms.ModelForm):
    assignment = forms.ModelChoiceField(queryset=Assignment.objects.none())

    class Meta:
        model = Submission
        fields = ('assignment', 'file', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your GitHub link, demo notes, or what you learned.'}),
        }

    def __init__(self, *args, **kwargs):
        assignments = kwargs.pop('assignments', Assignment.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['assignment'].queryset = assignments

    def clean_file(self):
        return validate_upload_size(self.cleaned_data.get('file'))

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('file') and not cleaned_data.get('notes'):
            raise forms.ValidationError('Upload a file or add submission notes before sending your work.')
        return cleaned_data


class ChatMessageForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=ChatRoom.objects.none())

    class Meta:
        model = ChatMessage
        fields = ('room', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask a question, share an update, or help a classmate.'}),
        }

    def __init__(self, *args, **kwargs):
        rooms = kwargs.pop('rooms', ChatRoom.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = rooms


class TrainerApplicationForm(forms.ModelForm):
    class Meta:
        model = TrainerApplication
        fields = ('name', 'email', 'phone', 'expertise', 'bio', 'cv', 'certifications_file', 'portfolio_url')
        widgets = {
            'cv': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
            'certifications_file': forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}),
        }

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            FileExtensionValidator(['pdf', 'doc', 'docx'])(cv)
        return validate_upload_size(cv)

    def clean_certifications_file(self):
        certificate = self.cleaned_data.get('certifications_file')
        if certificate:
            FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])(certificate)
        return validate_upload_size(certificate)


class MentorshipBookingForm(forms.ModelForm):
    class Meta:
        model = MentorshipBooking
        fields = ('trainer', 'student_name', 'email', 'topic', 'preferred_time', 'message')
        widgets = {
            'preferred_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MentorAIForm(forms.ModelForm):
    class Meta:
        model = MentorAIInteraction
        fields = ('name', 'question')
        widgets = {
            'question': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ask about coding, career paths, projects, or what to learn next...'}),
        }
