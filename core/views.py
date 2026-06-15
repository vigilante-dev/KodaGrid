from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, View

from blog.models import BlogPost
from courses.models import Course
from events.models import Event
from gallery.models import GalleryImage

from .forms import NewsletterSignupForm
from .models import Testimonial, VideoStory


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_courses'] = Course.objects.filter(is_featured=True)[:6]
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:3]
        context['upcoming_events'] = Event.objects.filter(date__gte=timezone.now())[:3]
        context['featured_posts'] = BlogPost.objects.filter(is_featured=True)[:2]
        context['featured_video'] = VideoStory.objects.filter(is_featured=True).first()
        gallery_images = GalleryImage.objects.exclude(image='').exclude(image__isnull=True)
        context['hero_image'] = (
            gallery_images.filter(suggested_placement__icontains='Hero').first()
            or gallery_images.filter(detected_activity__icontains='coding').first()
            or gallery_images.first()
        )
        context['visual_story_images'] = list(
            gallery_images.filter(
                Q(suggested_placement__icontains='Hero')
                | Q(suggested_placement__icontains='Girls')
                | Q(suggested_placement__icontains='Community')
                | Q(suggested_placement__icontains='Learning')
                | Q(educational_relevance__icontains='AI')
                | Q(detected_activity__icontains='coding')
            )[:6]
        )
        if len(context['visual_story_images']) < 4:
            context['visual_story_images'] = list(gallery_images[:6])
        context['newsletter_form'] = NewsletterSignupForm()
        context['stats'] = [
            {'value': 3500, 'suffix': '+', 'label': 'Total Students'},
            {'value': 1280, 'suffix': '+', 'label': 'Active Learners'},
            {'value': 46, 'suffix': '+', 'label': 'Trainers'},
            {'value': 72, 'suffix': '+', 'label': 'Courses'},
            {'value': 620, 'suffix': '+', 'label': 'Projects Completed'},
            {'value': 2100, 'suffix': '+', 'label': 'Certifications Issued'},
        ]
        context['partners'] = ['Savannah Cloud', 'STEM Hub Africa', 'Future Labs', 'SecureNet', 'DataBridge']
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
                messages.success(request, 'You are subscribed to CodeSavannah updates.')
            except IntegrityError:
                messages.info(request, 'That email is already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        return redirect(request.POST.get('next') or reverse_lazy('core:home'))
