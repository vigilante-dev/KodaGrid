from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from academy.models import LearningPath, TrainerProfile

from .models import Course, CourseSection, CourseTopic


def can_teach(user):
    """Staff and approved trainers can see drafts and private trainer notes."""
    if not user.is_authenticated:
        return False
    return user.is_staff or TrainerProfile.objects.filter(user=user, is_approved=True).exists()


def syllabus_for(course, include_drafts=False):
    sections = course.sections.all()
    topics = CourseTopic.objects.all()
    if not include_drafts:
        sections = sections.filter(is_published=True)
        topics = topics.filter(is_published=True)
    return sections.prefetch_related(Prefetch('topics', queryset=topics))


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

    def get_queryset(self):
        queryset = Course.objects.all()
        query = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(instructor__icontains=query)
            )
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Course.CATEGORY_CHOICES
        context['active_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        # All 61 learning paths grouped by category for the Learning Paths section
        context['learning_paths'] = (
            LearningPath.objects
            .annotate(lesson_count=Count('lessons'))
            .order_by('category', 'title')
        )
        context['path_categories'] = LearningPath.CATEGORIES
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied
        self.object = self.get_object()
        self.object.notes = request.POST.get('notes', '')
        self.object.save(update_fields=['notes', 'updated_at'])
        messages.success(request, 'Course notes saved.')
        return redirect(self.object.get_absolute_url() + '#course-notes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.object.slug
        # Try exact slug match first, then title-word fallback
        path = LearningPath.objects.filter(slug=slug).prefetch_related('lessons').first()
        if not path:
            words = [w for w in self.object.title.split() if len(w) > 3]
            for word in words:
                path = LearningPath.objects.filter(
                    title__icontains=word
                ).prefetch_related('lessons').first()
                if path:
                    break
        context['learning_path'] = path
        context['can_edit_course_notes'] = self.request.user.is_authenticated and self.request.user.is_staff
        is_teacher = can_teach(self.request.user)
        sections = list(syllabus_for(self.object, include_drafts=is_teacher))
        context['sections'] = sections
        context['topic_total'] = sum(len(section.topics.all()) for section in sections)
        minutes_total = sum(t.duration_minutes for section in sections for t in section.topics.all())
        context['hours_total'] = f'{minutes_total / 60:.1f}'.removesuffix('.0') if minutes_total else ''
        context['is_teacher'] = is_teacher
        return context


class CourseTopicDetailView(DetailView):
    template_name = 'courses/topic_detail.html'
    context_object_name = 'topic'

    def get_object(self, queryset=None):
        self.course = get_object_or_404(Course, slug=self.kwargs['slug'])
        topic = get_object_or_404(
            CourseTopic.objects.select_related('section', 'section__course'),
            pk=self.kwargs['pk'], section__course=self.course,
        )
        self.is_teacher = can_teach(self.request.user)
        if not self.is_teacher and not (topic.is_published and topic.section.is_published):
            raise Http404('Topic not found.')
        return topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sections = list(syllabus_for(self.course, include_drafts=self.is_teacher))
        ordered_topics = [topic for section in sections for topic in section.topics.all()]
        ids = [topic.pk for topic in ordered_topics]
        position = ids.index(self.object.pk) if self.object.pk in ids else 0
        context.update({
            'course': self.course,
            'sections': sections,
            'is_teacher': self.is_teacher,
            'prev_topic': ordered_topics[position - 1] if position > 0 else None,
            'next_topic': ordered_topics[position + 1] if position + 1 < len(ordered_topics) else None,
            'topic_number': position + 1,
            'topic_total': len(ordered_topics),
        })
        return context

