from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Course(models.Model):
    WEB = 'web-development'
    MOBILE = 'mobile-app-development'
    PYTHON = 'python-programming'
    AI = 'ai-machine-learning'
    CYBER = 'cybersecurity'
    ROBOTICS = 'robotics'
    UIUX = 'ui-ux-design'
    MARKETING = 'digital-marketing'
    DATA = 'data-science'
    CLOUD = 'cloud-computing'

    CATEGORY_CHOICES = [
        (WEB, 'Web Development'),
        (MOBILE, 'Mobile App Development'),
        (PYTHON, 'Python Programming'),
        (AI, 'Artificial Intelligence & Machine Learning'),
        (CYBER, 'Cybersecurity'),
        (ROBOTICS, 'Robotics'),
        (UIUX, 'UI/UX Design'),
        (MARKETING, 'Digital Marketing'),
        (DATA, 'Data Science'),
        (CLOUD, 'Cloud Computing'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    learning_outcomes = models.TextField(blank=True)
    duration = models.CharField(max_length=80)
    category = models.CharField(max_length=60, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES, default='beginner')
    requirements = models.TextField(blank=True)
    certification_details = models.TextField(blank=True)
    instructor = models.CharField(max_length=120)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def outcome_list(self):
        return [item.strip() for item in self.learning_outcomes.splitlines() if item.strip()]

    def __str__(self):
        return self.title

# Create your models here.
