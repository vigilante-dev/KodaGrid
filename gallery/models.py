from django.db import models


class GalleryImage(models.Model):
    CATEGORIES = [
        ('training', 'Training Sessions'),
        ('workshops', 'Workshops'),
        ('graduation', 'Graduation Ceremonies'),
        ('projects', 'Student Projects'),
        ('hackathons', 'Hackathons'),
        ('outreach', 'Community Outreach'),
    ]

    title = models.CharField(max_length=160)
    category = models.CharField(max_length=40, choices=CATEGORIES)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    caption = models.TextField(blank=True)
    detected_subject = models.CharField(max_length=160, blank=True)
    detected_activity = models.CharField(max_length=180, blank=True)
    age_group = models.CharField(max_length=80, blank=True)
    educational_relevance = models.CharField(max_length=220, blank=True)
    suggested_placement = models.CharField(max_length=120, blank=True)
    optimized_from = models.CharField(max_length=240, blank=True)
    date_taken = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# Create your models here.
