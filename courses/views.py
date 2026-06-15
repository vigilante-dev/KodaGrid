from django.db.models import Count, Q
from django.views.generic import DetailView, ListView

from academy.models import LearningPath
from .models import Course


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from academy.models import LearningPath
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
        return context

# Create your views here.
