from django.contrib import admin

from .models import NewsletterSubscriber, Testimonial, VideoStory


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_completed', 'submitted_by', 'rating', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'rating', 'created_at')
    search_fields = ('student_name', 'course_completed', 'feedback')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)


@admin.register(VideoStory)
class VideoStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'kicker', 'duration_label', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description', 'kicker')

# Register your models here.
