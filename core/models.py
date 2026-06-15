from django.db import models


class Testimonial(models.Model):
    student_name = models.CharField(max_length=150)
    course_completed = models.CharField(max_length=160)
    feedback = models.TextField()
    student_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student_name} - {self.course_completed}'


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class VideoStory(models.Model):
    title = models.CharField(max_length=180)
    kicker = models.CharField(max_length=120, default='Inside the Academy')
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    poster = models.ImageField(upload_to='video-posters/', blank=True, null=True)
    duration_label = models.CharField(max_length=40, blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'video stories'

    def __str__(self):
        return self.title

# Create your models here.
