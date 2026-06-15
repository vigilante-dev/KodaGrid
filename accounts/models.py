from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True,
    )
    career_interest = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Create your models here.
