from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View

from courses.models import Course
from events.models import Event

from .forms import NewsletterSignupForm, TestimonialSubmissionForm
from .models import Testimonial


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_courses'] = Course.objects.filter(is_featured=True)[:3]
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:3]
        context['testimonial_form'] = TestimonialSubmissionForm()
        context['upcoming_events'] = Event.objects.filter(date__gte=timezone.now())[:3]
        context['newsletter_form'] = NewsletterSignupForm()
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = [
            ('Practical Learning', 'Students learn by building useful products, portfolios, and team projects.'),
            ('Inclusive Access', 'We design pathways for beginners, schools, young professionals, and communities.'),
            ('Future Readiness', 'Every program connects technical skills with careers, entrepreneurship, and responsible innovation.'),
            ('Mentorship', 'Learners receive guidance from instructors, alumni, and technology partners.'),
        ]
        context['team'] = [
            {'name': 'Amina Wanjiku', 'role': 'Executive Director', 'focus': 'Youth innovation and partnerships'},
            {'name': 'Brian Otieno', 'role': 'Lead Instructor', 'focus': 'Software engineering and AI'},
            {'name': 'Grace Njeri', 'role': 'Career Programs Lead', 'focus': 'Internships, mentorship, and employability'},
        ]
        context['achievements'] = [
            'Launched coding clubs with partner schools.',
            'Supported student portfolios across web, mobile, robotics, and data projects.',
            'Hosted hackathons focused on community problem solving.',
            'Built career pathways with technology employers and mentors.',
        ]
        return context


class NewsletterSignupView(View):
    def post(self, request, *args, **kwargs):
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'You are subscribed to KodaGrid updates.')
            except IntegrityError:
                messages.info(request, 'That email is already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        return redirect(request.POST.get('next') or reverse_lazy('core:home'))


class TestimonialSubmissionView(LoginRequiredMixin, FormView):
    form_class = TestimonialSubmissionForm
    success_url = reverse_lazy('core:home')

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def form_valid(self, form):
        testimonial = form.save(commit=False)
        testimonial.student_name = self.request.user.get_full_name() or self.request.user.get_username()
        testimonial.submitted_by = self.request.user
        testimonial.is_featured = False
        testimonial.save()
        messages.success(self.request, 'Thanks for sharing your experience. Your testimonial is awaiting review.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please check the testimonial form and try again.')
        return redirect(self.success_url)
