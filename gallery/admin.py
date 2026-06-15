from django.contrib import admin

from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'suggested_placement', 'age_group', 'date_taken', 'created_at')
    list_filter = ('category', 'suggested_placement', 'age_group', 'date_taken')
    search_fields = ('title', 'caption', 'detected_subject', 'detected_activity', 'educational_relevance')

# Register your models here.
