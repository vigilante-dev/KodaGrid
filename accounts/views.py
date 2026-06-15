from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from academy.models import Assignment, Certificate, ClassMembership, LearningPath, MentorshipBooking, Submission

from .forms import StudentProfileForm, StudentRegistrationForm
from .models import Student


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Welcome to CodeSavannah Academy. Your student account is ready.')
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
