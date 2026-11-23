from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class Student(models.Model):
    class ApprovalStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

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
    phone_number = models.CharField(max_length=32, blank=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateField(auto_now_add=True)
    approval_status = models.CharField(
        max_length=12,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
        db_index=True,
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='student_applications_reviewed',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Create your models here.
