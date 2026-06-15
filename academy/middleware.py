from django.core.cache import cache
from django.http import HttpResponse


class SimpleRateLimitMiddleware:
    """Small built-in POST throttle for public forms without third-party packages."""

    LIMIT = 45
    WINDOW_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and not request.path.startswith('/admin/'):
            ip_address = request.META.get('REMOTE_ADDR', 'unknown')
            key = f'post-rate:{ip_address}:{request.path}'
            attempts = cache.get(key, 0) + 1
            cache.set(key, attempts, self.WINDOW_SECONDS)
            if attempts > self.LIMIT:
                return HttpResponse('Too many requests. Please wait a moment and try again.', status=429)
        return self.get_response(request)
