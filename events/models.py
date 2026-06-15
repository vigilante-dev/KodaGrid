from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('bootcamp', 'Bootcamp'),
        ('competition', 'Coding Competition'),
        ('hackathon', 'Hackathon'),
        ('career', 'Career Session'),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    event_type = models.CharField(max_length=40, choices=EVENT_TYPES, default='workshop')
    date = models.DateTimeField()
    location = models.CharField(max_length=180)
    seats_available = models.PositiveIntegerField(default=50)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'email')
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.name} - {self.event.title}'

# Create your models here.
