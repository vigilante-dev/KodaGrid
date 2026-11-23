from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Student


def validate_image_size(image):
    if not image or not hasattr(image, 'size'):
        return image
    limit_mb = getattr(settings, 'MAX_IMAGE_UPLOAD_MB', 5)
    if image.size > limit_mb * 1024 * 1024:
        raise ValidationError(f'Please upload an image smaller than {limit_mb} MB.')
    return image


class AccountPasswordResetForm(PasswordResetForm):
    """Let legacy passwordless accounts set their first Django password."""

    def get_users(self, email):
        User = get_user_model()
        email_field = User.get_email_field_name()
        active_users = User._default_manager.filter(
            **{f'{email_field}__iexact': email, 'is_active': True}
        ).filter(
            Q(is_staff=True)
            | Q(is_superuser=True)
            | Q(student_profile__approval_status=Student.ApprovalStatus.APPROVED)
            | Q(trainer_profile__is_approved=True)
        ).distinct()
        return (
            user for user in active_users
            if getattr(user, email_field).casefold() == email.casefold()
        )


class StudentRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=150, label='Full name')
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=32, label='Phone number')
    profile_picture = forms.ImageField(
        label='Student photo',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
    )
    career_interest = forms.CharField(max_length=120, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'phone_number',
            'profile_picture',
            'career_interest',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists() or Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_name(self):
        name = ' '.join(self.cleaned_data['name'].split())
        if not name:
            raise forms.ValidationError('Please enter your full name.')
        return name

    def clean_profile_picture(self):
        return validate_image_size(self.cleaned_data.get('profile_picture'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        parts = self.cleaned_data['name'].split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
                profile_picture=self.cleaned_data['profile_picture'],
                career_interest=self.cleaned_data.get('career_interest', ''),
                approval_status=Student.ApprovalStatus.PENDING,
            )
        return user


class StudentAuthenticationForm(AuthenticationForm):
    """Use Django sessions while explaining valid credentials for unapproved students."""

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            UserModel = get_user_model()
            self.user_cache = authenticate(
                self.request,
                **{UserModel.USERNAME_FIELD: username},
                password=password,
            )
            if self.user_cache is None:
                self._raise_login_error(UserModel, username, password)
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def _raise_login_error(self, UserModel, username, password):
        try:
            user = UserModel._default_manager.get(**{UserModel.USERNAME_FIELD: username})
        except (UserModel.DoesNotExist, TypeError, ValueError):
            user = None

        if user is not None and user.check_password(password):
            try:
                status = user.student_profile.approval_status
            except (AttributeError, Student.DoesNotExist):
                status = None
            if status == Student.ApprovalStatus.PENDING:
                message = (
                    'Your account has been successfully registered and is awaiting '
                    'administrator approval. You will be able to log in once your '
                    'application has been approved.'
                )
                raise ValidationError(message, code='pending_approval')
            if status == Student.ApprovalStatus.REJECTED:
                raise ValidationError(
                    'Your application has not been approved. Please contact the '
                    'platform administrator for further information.',
                    code='application_rejected',
                )
            if not user.is_active:
                raise ValidationError(self.error_messages['inactive'], code='inactive')

        raise ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'email', 'phone_number', 'profile_picture', 'career_interest', 'bio')
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_name(self):
        name = ' '.join(self.cleaned_data['name'].split())
        if not name:
            raise forms.ValidationError('Please enter your full name.')
        return name

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        other_users = User.objects.filter(email__iexact=email)
        if self.instance.user_id:
            other_users = other_users.exclude(pk=self.instance.user_id)
        if other_users.exists():
            raise forms.ValidationError('Another account already uses this email address.')
        return email

    def clean_profile_picture(self):
        return validate_image_size(self.cleaned_data.get('profile_picture'))
