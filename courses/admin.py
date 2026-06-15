from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'duration', 'instructor', 'is_featured')
    list_filter = ('category', 'level', 'is_featured')
    search_fields = ('title', 'description', 'instructor')
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
