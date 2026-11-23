from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from accounts.views import student_photo
from core.media import media_file

urlpatterns = [
    path('admin-student-photo/<int:student_id>/', student_photo, name='student_photo'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('events/', include('events.urls')),
    path('blog/', include('blog.urls')),
    path('gallery/', include('gallery.urls')),
    path('contact/', include('contact.urls')),
    path('', include('academy.urls')),
]

urlpatterns += [
    re_path(rf'^{settings.MEDIA_URL.strip("/")}/(?P<path>.+)$', media_file, name='media'),
]
