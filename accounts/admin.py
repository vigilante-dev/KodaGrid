from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'career_interest', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('name', 'email', 'career_interest')

# Register your models here.
