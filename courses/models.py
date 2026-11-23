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
    notes = models.TextField(blank=True, help_text='Course notes shown on the public course page.')
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


def _lines(text):
    return [line.strip() for line in (text or '').splitlines() if line.strip()]


class CourseSection(models.Model):
    """A unit of a course, e.g. "Week 1: Python Basics", made up of classroom topics."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=180)
    week_label = models.CharField(
        max_length=60, blank=True,
        help_text='Optional label shown before the title, e.g. "Week 1" or "Module 2".',
    )
    order = models.PositiveIntegerField(default=1)
    overview = models.TextField(blank=True, help_text='What this section covers and why it matters.')
    learning_objectives = models.TextField(blank=True, help_text='One objective per line.')
    is_published = models.BooleanField(default=True, help_text='Untick to keep this section as a draft.')

    class Meta:
        ordering = ['course', 'order', 'id']

    def __str__(self):
        label = f'{self.week_label}: ' if self.week_label else ''
        return f'{self.course.title} — {label}{self.title}'

    def objective_list(self):
        return _lines(self.learning_objectives)


class CourseTopic(models.Model):
    """One classroom session within a section: notes, activity, discussion, and homework."""

    FORMAT_CHOICES = [
        ('lecture', 'Lecture'),
        ('workshop', 'Hands-on workshop'),
        ('lab', 'Coding lab'),
        ('discussion', 'Group discussion'),
        ('project', 'Project work'),
        ('assessment', 'Assessment'),
        ('self-study', 'Self-study'),
    ]

    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=180)
    order = models.PositiveIntegerField(default=1)
    session_format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='lecture')
    duration_minutes = models.PositiveIntegerField(default=60)
    summary = models.CharField(max_length=300, blank=True, help_text='One-line summary shown in the syllabus.')
    notes = models.TextField(blank=True, help_text='Topic notes for students. Links are made clickable.')
    in_class_activity = models.TextField(blank=True, help_text='What students do together during the session.')
    discussion_questions = models.TextField(blank=True, help_text='One question per line.')
    homework = models.TextField(blank=True)
    resources = models.TextField(
        blank=True,
        help_text='One link per line. Use "Title | https://example.com" or just the URL.',
    )
    attachment = models.FileField(
        upload_to='materials/course-topics/', blank=True, null=True,
        help_text='Slides or handouts. Downloadable by signed-in users.',
    )
    trainer_notes = models.TextField(
        blank=True,
        help_text='Private teaching notes: timing, common mistakes, answers. Only staff and approved trainers see these.',
    )
    is_published = models.BooleanField(default=True, help_text='Untick to keep this topic as a draft.')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section', 'order', 'id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:topic', kwargs={'slug': self.section.course.slug, 'pk': self.pk})

    def question_list(self):
        return _lines(self.discussion_questions)

    def resource_list(self):
        links = []
        for line in _lines(self.resources):
            title, _sep, url = line.rpartition('|')
            url = url.strip()
            if url.startswith(('https://', 'http://')):
                links.append({'title': title.strip() or url, 'url': url})
        return links

