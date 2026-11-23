import mimetypes

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from academy.models import Assignment, Certificate, ClassMembership, LearningPath, MentorshipBooking, Submission

from .forms import StudentProfileForm, StudentRegistrationForm
from .models import Student


@staff_member_required
def student_photo(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if not student.profile_picture:
        raise Http404('Student photo not found.')

    content_type, _encoding = mimetypes.guess_type(student.profile_picture.name)
    if not content_type or not content_type.startswith('image/'):
        raise Http404('Student photo not found.')
    try:
        photo = student.profile_picture.open('rb')
    except OSError as error:
        raise Http404('Student photo not found.') from error

    response = FileResponse(photo, content_type=content_type)
    response['Cache-Control'] = 'private, no-store'
    response['X-Content-Type-Options'] = 'nosniff'
    return response


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        with transaction.atomic():
            form.save()
        messages.success(
            self.request,
            'Your account has been successfully registered and is awaiting administrator '
            'approval. You will be able to log in once your application has been approved.',
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_student(self):
        user = self.request.user
        try:
            return user.student_profile
        except Student.DoesNotExist:
            pass
        # Staff and trainers reach the portal without a student record. Anyone signed in has
        # already passed the approval backend, so the new profile must be APPROVED; the model
        # default (PENDING) would make the backend reject this user on their next request.
        email = (user.email or '').strip()
        if not email or Student.objects.filter(email__iexact=email).exists():
            email = f'{user.username}.{user.pk}@users.invalid'
        now = timezone.now()
        return Student.objects.create(
            user=user,
            name=user.get_full_name() or user.username,
            email=email,
            approval_status=Student.ApprovalStatus.APPROVED,
            approved_at=now,
            reviewed_at=now,
        )

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
            with transaction.atomic():
                student = form.save()
                # Keep the login account in sync: password reset emails go to User.email.
                user = request.user
                parts = student.name.split(' ', 1)
                user.first_name = parts[0][:150]
                user.last_name = parts[1][:150] if len(parts) > 1 else ''
                user.email = student.email
                user.save(update_fields=['first_name', 'last_name', 'email'])
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        return self.render_to_response(self.get_context_data(form=form))

# Create your views here.
