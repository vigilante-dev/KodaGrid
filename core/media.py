"""Serve uploaded media with per-folder access rules.

WhiteNoise only serves static files, so without this view nothing under MEDIA_ROOT is
reachable once DEBUG is off. MEDIA_ROOT also holds private uploads (student ID photos,
trainer CVs, assignment submissions), so folders are not all public.
"""
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.static import serve

PUBLIC_FOLDERS = {
    'blog', 'courses', 'events', 'gallery', 'resources', 'robotics',
    'testimonials', 'trainers', 'video-posters', 'videos',
}
MEMBER_FOLDERS = {'assignments', 'materials'}


def media_file(request, path):
    folder = path.split('/', 1)[0]
    if '..' in path.split('/'):
        raise Http404
    if folder in MEMBER_FOLDERS:
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
    elif folder not in PUBLIC_FOLDERS:
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not request.user.is_staff:
            raise PermissionDenied
    response = serve(request, path, document_root=settings.MEDIA_ROOT)
    response['X-Content-Type-Options'] = 'nosniff'
    if folder in PUBLIC_FOLDERS:
        response['Cache-Control'] = 'public, max-age=86400'
    else:
        response['Cache-Control'] = 'private, no-store'
        # Never let a private upload (e.g. an HTML "CV") render inline on our origin.
        response['Content-Disposition'] = 'attachment'
    return response
