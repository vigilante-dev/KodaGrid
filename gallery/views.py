from django.views.generic import ListView

from .models import GalleryImage


class GalleryView(ListView):
    model = GalleryImage
    template_name = 'gallery/gallery.html'
    context_object_name = 'images'
    paginate_by = 12

    def get_queryset(self):
        queryset = GalleryImage.objects.all()
        category = self.request.GET.get('category', '').strip()
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GalleryImage.CATEGORIES
        context['active_category'] = self.request.GET.get('category', '')
        return context

# Create your views here.
