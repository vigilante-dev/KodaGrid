import secrets
import string
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class LearningPath(models.Model):
    CATEGORIES = [
        ('programming', 'Programming'),
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('databases', 'Databases'),
        ('cloud', 'Cloud'),
        ('cybersecurity', 'Cybersecurity'),
        ('ai', 'Artificial Intelligence'),
    ]

    LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('professional', 'Professional'),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=40, choices=CATEGORIES)
    summary = models.TextField()
    level = models.CharField(max_length=30, choices=LEVELS, default='beginner')
    duration = models.CharField(max_length=80, default='Self-paced')
    skill_stack = models.CharField(max_length=240, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('academy:learning_path_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Lesson(models.Model):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=1)
    objective = models.TextField()
    content = models.TextField()
    exercise_prompt = models.TextField(blank=True)
    quiz_question = models.TextField(blank=True)
    project_prompt = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    estimated_minutes = models.PositiveIntegerField(default=25)

    class Meta:
        ordering = ['learning_path', 'order']
        unique_together = ('learning_path', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.learning_path.title}: {self.title}'


class TrainerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='trainer_profile',
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    headline = models.CharField(max_length=180)
    bio = models.TextField()
    skills = models.CharField(max_length=240)
    certifications = models.TextField(blank=True)
    courses_taught = models.CharField(max_length=240, blank=True)
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TrainerApplication(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Reviewing'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    expertise = models.CharField(max_length=220)
    bio = models.TextField()
    cv = models.FileField(upload_to='trainer-applications/cv/', blank=True, null=True)
    certifications_file = models.FileField(upload_to='trainer-applications/certifications/', blank=True, null=True)
    portfolio_url = models.URLField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.expertise}'


class MentorshipBooking(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='bookings')
    student_name = models.CharField(max_length=150)
    email = models.EmailField()
    topic = models.CharField(max_length=180)
    preferred_time = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student_name} - {self.topic}'


def generate_class_code():
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))


class Classroom(models.Model):
    name = models.CharField(max_length=180)
    class_code = models.CharField(max_length=12, unique=True, default=generate_class_code)
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='classrooms')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.SET_NULL, blank=True, null=True, related_name='classrooms')
    description = models.TextField()
    meeting_link = models.URLField(blank=True)
    start_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ClassMembership(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='memberships')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='class_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    progress_percent = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('classroom', 'student')
        ordering = ['classroom', 'student__username']

    def __str__(self):
        return f'{self.student.username} in {self.classroom.name}'


class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=180)
    instructions = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    notes = models.TextField(blank=True)
    grade = models.PositiveIntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.student.username} - {self.assignment.title}'


class LearningMaterial(models.Model):
    MATERIAL_TYPES = [
        ('notes', 'Notes'),
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('template', 'Template'),
        ('challenge', 'Coding Challenge'),
    ]

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True, related_name='materials')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, blank=True, null=True, related_name='materials')
    title = models.CharField(max_length=180)
    material_type = models.CharField(max_length=30, choices=MATERIAL_TYPES)
    description = models.TextField()
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class AttendanceRecord(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    attended_on = models.DateField(default=timezone.now)
    was_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('classroom', 'student', 'attended_on')
        ordering = ['-attended_on']

    def __str__(self):
        return f'{self.student.username} - {self.attended_on}'


class Announcement(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True, related_name='announcements')
    title = models.CharField(max_length=180)
    message = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class LiveSession(models.Model):
    SESSION_TYPES = [
        ('video', 'Video Call'),
        ('audio', 'Audio Room'),
        ('screen', 'Screen Sharing'),
        ('consultation', 'Mentorship Consultation'),
    ]

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True, related_name='live_sessions')
    title = models.CharField(max_length=180)
    session_type = models.CharField(max_length=30, choices=SESSION_TYPES, default='video')
    agenda = models.TextField(blank=True)
    meeting_url = models.URLField(blank=True)
    scheduled_for = models.DateTimeField(default=timezone.now)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_for']

    def __str__(self):
        return self.title


class ChatRoom(models.Model):
    ROOM_TYPES = [
        ('group', 'Group Chat'),
        ('private', 'Private Chat'),
        ('voice', 'Voice Room'),
    ]

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True, related_name='chat_rooms')
    name = models.CharField(max_length=160)
    room_type = models.CharField(max_length=30, choices=ROOM_TYPES, default='group')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='academy_chat_rooms')
    call_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='academy_chat_messages')
    sender_name = models.CharField(max_length=150)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender_name}: {self.body[:60]}'


class FeePlan(models.Model):
    PROGRAM_LEVELS = [
        ('beginner', 'Beginner Programs'),
        ('intermediate', 'Intermediate Programs'),
        ('advanced', 'Advanced Programs'),
        ('certification', 'Professional Certifications'),
        ('corporate', 'Corporate Training'),
    ]

    name = models.CharField(max_length=160)
    level = models.CharField(max_length=40, choices=PROGRAM_LEVELS)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    term_price = models.DecimalField(max_digits=10, decimal_places=2)
    annual_price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['monthly_price']

    def feature_list(self):
        return [item.strip() for item in self.features.splitlines() if item.strip()]

    def __str__(self):
        return self.name


class Certificate(models.Model):
    student_name = models.CharField(max_length=150)
    course_name = models.CharField(max_length=180)
    completion_date = models.DateField(default=timezone.now)
    verification_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_at']

    def get_absolute_url(self):
        return reverse('academy:certificate_verify', kwargs={'code': self.verification_code})

    def __str__(self):
        return f'{self.student_name} - {self.course_name}'


class ForumTopic(models.Model):
    title = models.CharField(max_length=180)
    author_name = models.CharField(max_length=150)
    category = models.CharField(max_length=80, default='General')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ForumReply(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='replies')
    author_name = models.CharField(max_length=150)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'forum replies'

    def __str__(self):
        return f'Reply by {self.author_name}'


class CommunityChallenge(models.Model):
    title = models.CharField(max_length=180)
    challenge_type = models.CharField(max_length=80, default='Hackathon')
    description = models.TextField()
    deadline = models.DateField()
    prize = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.title


class JobOpportunity(models.Model):
    JOB_TYPES = [
        ('internship', 'Internship'),
        ('attachment', 'Attachment'),
        ('remote', 'Remote Job'),
        ('freelance', 'Freelance Opportunity'),
    ]

    title = models.CharField(max_length=180)
    company = models.CharField(max_length=150)
    job_type = models.CharField(max_length=40, choices=JOB_TYPES)
    location = models.CharField(max_length=120)
    description = models.TextField()
    application_url = models.URLField(blank=True)
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} at {self.company}'


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('notes', 'Notes'),
        ('pdf', 'PDF Guide'),
        ('cheatsheet', 'Cheat Sheet'),
        ('template', 'Template'),
        ('challenge', 'Coding Challenge'),
    ]

    title = models.CharField(max_length=180)
    resource_type = models.CharField(max_length=40, choices=RESOURCE_TYPES)
    summary = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class MentorAIInteraction(models.Model):
    name = models.CharField(max_length=150, blank=True)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:80]


class SkillAssessment(models.Model):
    SKILL_LEVELS = [
        ('explorer',     'Explorer (Ages 6–10)'),
        ('beginner',     'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced',     'Advanced'),
        ('expert',       'Expert'),
    ]
    LEARNING_STYLES = [
        ('visual',    'Visual Learner'),
        ('kinesthetic','Learn by Doing'),
        ('reading',   'Reading / Writing'),
        ('auditory',  'Auditory / Video'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skill_assessment',
        null=True, blank=True,
    )
    session_key    = models.CharField(max_length=40, blank=True)
    skill_level    = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    iq_score       = models.IntegerField(default=0)
    age_group      = models.CharField(max_length=40, blank=True)
    learning_style = models.CharField(max_length=40, choices=LEARNING_STYLES, blank=True)
    strengths      = models.JSONField(default=list)
    interests      = models.JSONField(default=list)
    recommended_paths = models.JSONField(default=list)
    recommended_books = models.JSONField(default=list)
    answers        = models.JSONField(default=dict)
    completed_at   = models.DateTimeField(null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        label = getattr(self.user, 'username', self.session_key or 'Anonymous')
        return f'{label} — {self.skill_level}'


class RoboticsKit(models.Model):
    DIFFICULTY = [
        ('kids',         'Kids (Ages 6–10)'),
        ('beginner',     'Beginner (Ages 11–14)'),
        ('intermediate', 'Intermediate (Ages 14+)'),
        ('advanced',     'Advanced'),
    ]

    name        = models.CharField(max_length=160)
    brand       = models.CharField(max_length=100)
    difficulty  = models.CharField(max_length=20, choices=DIFFICULTY)
    age_group   = models.CharField(max_length=60)
    description = models.TextField()
    components  = models.JSONField(default=list, help_text='List of component names')
    assembly_steps = models.JSONField(default=list, help_text='List of {step, instruction, tip} dicts')
    languages_used = models.CharField(max_length=180, blank=True)
    kit_image   = models.ImageField(upload_to='robotics/', blank=True, null=True)
    project_ideas = models.JSONField(default=list)
    is_featured = models.BooleanField(default=False)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.brand} {self.name}'
