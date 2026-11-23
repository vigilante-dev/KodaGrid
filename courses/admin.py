from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import Course, CourseSection, CourseTopic

CLASSROOM_PLAN_HELP = 'Plan the live session: what students do together, what to discuss, and what to take home.'


class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    extra = 1
    fields = ('order', 'week_label', 'title', 'is_published', 'topic_count')
    readonly_fields = ('topic_count',)
    ordering = ('order', 'id')
    show_change_link = True

    @admin.display(description='Topics')
    def topic_count(self, section):
        if not section.pk:
            return '—'
        return section.topics.count()


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'duration', 'instructor', 'section_count', 'is_featured')
    list_filter = ('category', 'level', 'is_featured')
    search_fields = ('title', 'description', 'notes', 'instructor')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CourseSectionInline]
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'category', 'level', 'duration', 'instructor', 'image', 'is_featured')}),
        ('Course page content', {'fields': ('description', 'learning_outcomes', 'requirements', 'certification_details')}),
        ('Course notes', {
            'fields': ('notes',),
            'description': 'General notes shown on the course page. Add notes for specific topics under Sections below.',
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_section_count=Count('sections'))

    @admin.display(description='Sections', ordering='_section_count')
    def section_count(self, course):
        return course._section_count


class CourseTopicInline(admin.StackedInline):
    model = CourseTopic
    extra = 1
    ordering = ('order', 'id')
    show_change_link = True
    fieldsets = (
        (None, {'fields': (('order', 'title'), ('session_format', 'duration_minutes', 'is_published'), 'summary')}),
        ('Topic notes for students', {'fields': ('notes',)}),
        ('Classroom plan', {
            'fields': ('in_class_activity', 'discussion_questions', 'homework'),
            'description': CLASSROOM_PLAN_HELP,
        }),
        ('Resources', {'fields': ('resources', 'attachment'), 'classes': ('collapse',)}),
        ('Trainer only', {'fields': ('trainer_notes',), 'classes': ('collapse',)}),
    )


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'week_label', 'order', 'topic_count', 'is_published')
    list_display_links = ('title',)
    list_editable = ('order', 'is_published')
    list_filter = ('is_published', 'course')
    list_select_related = ('course',)
    search_fields = ('title', 'overview', 'course__title')
    autocomplete_fields = ('course',)
    inlines = [CourseTopicInline]
    fieldsets = (
        (None, {'fields': ('course', ('order', 'week_label'), 'title', 'is_published')}),
        ('Section overview', {'fields': ('overview', 'learning_objectives')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_topic_count=Count('topics'))

    @admin.display(description='Topics', ordering='_topic_count')
    def topic_count(self, section):
        return section._topic_count

    def view_on_site(self, section):
        return section.course.get_absolute_url() + '#syllabus'


@admin.register(CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'course_link', 'session_format', 'duration_minutes', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    list_filter = ('is_published', 'session_format', 'section__course')
    list_select_related = ('section', 'section__course')
    search_fields = ('title', 'summary', 'notes', 'section__title', 'section__course__title')
    autocomplete_fields = ('section',)
    actions = ('publish_topics', 'unpublish_topics')
    fieldsets = CourseTopicInline.fieldsets[:1] + (
        (None, {'fields': ('section',)}),
    ) + CourseTopicInline.fieldsets[1:]

    @admin.display(description='Course', ordering='section__course__title')
    def course_link(self, topic):
        course = topic.section.course
        return format_html('<a href="{}">{}</a>', reverse('admin:courses_course_change', args=(course.pk,)), course.title)

    @admin.action(description='Publish selected topics')
    def publish_topics(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} topic(s) published.')

    @admin.action(description='Move selected topics to draft')
    def unpublish_topics(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} topic(s) moved to draft.')
