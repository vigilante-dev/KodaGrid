from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class BlogPost(models.Model):
    CATEGORIES = [
        ('career', 'Career Guidance'),
        ('coding', 'Coding Tutorials'),
        ('ai', 'Artificial Intelligence'),
        ('cybersecurity', 'Cybersecurity'),
        ('news', 'Technology News'),
        ('student-life', 'Student Life'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(max_length=320)
    content = models.TextField()
    category = models.CharField(max_length=40, choices=CATEGORIES, default='coding')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    date_published = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_published']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

# Create your models here.
