from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import os
from pathlib import Path
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from academy.models import Assignment, Certificate, ClassMembership, LearningPath, MentorshipBooking, Submission

from .forms import StudentProfileForm, StudentRegistrationForm
from .models import Student


@csrf_exempt
@require_POST
def firebase_session(request):
    """Exchange a Firebase ID token for the site's normal Django session."""
    project_id = os.environ.get('FIREBASE_PROJECT_ID', 'codesavannah-94f36')
    try:
        body = json.loads(request.body or '{}')
        token = body.get('id_token', '')
        import firebase_admin
        from firebase_admin import auth as firebase_auth
        try:
            app = firebase_admin.get_app()
        except ValueError:
            service_account = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
            service_account_file = os.environ.get('FIREBASE_SERVICE_ACCOUNT_FILE')
            if not service_account_file:
                local_credential = Path(__file__).resolve().parent.parent / 'codesavannah-94f36-firebase-adminsdk-fbsvc-f5a638f54a.json'
                if local_credential.is_file():
                    service_account_file = str(local_credential)
            if service_account:
                from firebase_admin import credentials
                credential = credentials.Certificate(json.loads(service_account))
                app = firebase_admin.initialize_app(credential, options={'projectId': project_id})
            elif service_account_file:
                from firebase_admin import credentials
                credential = credentials.Certificate(service_account_file)
                app = firebase_admin.initialize_app(credential, options={'projectId': project_id})
            else:
                app = firebase_admin.initialize_app(options={'projectId': project_id})
        claims = firebase_auth.verify_id_token(token, app=app, check_revoked=True)
    except Exception:
        return JsonResponse({'error': 'Firebase sign-in could not be verified. Check Firebase Admin credentials and try again.'}, status=401)
    email = (claims.get('email') or '').strip().lower()
    if not email or not claims.get('email_verified'):
        return JsonResponse({'error': 'Verify your email address in Firebase before continuing.'}, status=403)
    User = get_user_model()
    user = User.objects.filter(email__iexact=email).first()
    if user is None:
        base = email.split('@', 1)[0][:120] or 'learner'
        username = base
        suffix = 1
        while User.objects.filter(username=username).exists():
            suffix += 1
            username = f'{base[:110]}-{suffix}'
        full_name = (claims.get('name') or '').strip()
        parts = full_name.split(' ', 1)
        user = User.objects.create_user(username=username, email=email, password=None,
                                        first_name=parts[0][:150] if parts else '',
                                        last_name=parts[1][:150] if len(parts) > 1 else '')
        user.set_unusable_password()
        user.save(update_fields=['password'])
    if not user.is_active:
        return JsonResponse({'error': 'This account is disabled.'}, status=403)
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return JsonResponse({'ok': True, 'redirect': str(reverse_lazy('accounts:profile'))})


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Welcome to KodaGrid. Your student account is ready.')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_student(self):
        user = self.request.user
        full_name = user.get_full_name() or user.username
        student, _created = Student.objects.get_or_create(
            user=user,
            defaults={'name': full_name, 'email': user.email or f'{user.username}@example.com'},
        )
        return student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_student()
        memberships = ClassMembership.objects.filter(student=self.request.user).select_related(
            'classroom',
            'classroom__trainer',
            'classroom__learning_path',
        )
        classroom_ids = memberships.values_list('classroom_id', flat=True)
        assignments = Assignment.objects.filter(classroom_id__in=classroom_ids).select_related('classroom')
        submissions = Submission.objects.filter(student=self.request.user).select_related('assignment', 'assignment__classroom')
        certificates = Certificate.objects.filter(student_name__iexact=student.name)
        mentor_bookings = MentorshipBooking.objects.filter(email__iexact=student.email)
        if student.career_interest:
            recommended_paths = LearningPath.objects.filter(
                Q(title__icontains=student.career_interest)
                | Q(summary__icontains=student.career_interest)
                | Q(skill_stack__icontains=student.career_interest)
            )[:4]
        else:
            recommended_paths = LearningPath.objects.filter(is_featured=True)[:4]
        context['student'] = student
        context['form'] = kwargs.get('form') or StudentProfileForm(instance=student)
        context['portal_stats'] = [
            {'label': 'Courses active', 'value': memberships.count()},
            {'label': 'Assignments due', 'value': assignments.filter(due_date__gte=timezone.now()).exclude(submissions__student=self.request.user).count()},
            {'label': 'Certificates earned', 'value': certificates.count()},
            {'label': 'Mentor sessions', 'value': mentor_bookings.count()},
        ]
        context['memberships'] = memberships[:5]
        context['assignments_due'] = assignments.filter(due_date__gte=timezone.now()).exclude(submissions__student=self.request.user)[:5]
        context['submissions'] = submissions[:5]
        context['certificates'] = certificates[:4]
        context['recommended_paths'] = recommended_paths
        return context

    def post(self, request, *args, **kwargs):
        student = self.get_student()
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        return self.render_to_response(self.get_context_data(form=form))

# Create your views here.
