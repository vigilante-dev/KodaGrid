from django.urls import path

from .views import CourseDetailView, CourseListView, CourseTopicDetailView

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='detail'),
    path('<slug:slug>/topics/<int:pk>/', CourseTopicDetailView.as_view(), name='topic'),
]
