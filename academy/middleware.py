from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse


def client_ip(request):
    """Best-effort client IP. Behind a trusted proxy (Render) REMOTE_ADDR is the proxy itself."""
    if getattr(settings, 'RATE_LIMIT_TRUST_FORWARDED_FOR', False):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
        first_hop = forwarded.split(',')[0].strip()
        if first_hop:
            return first_hop
    return request.META.get('REMOTE_ADDR', 'unknown')


class SimpleRateLimitMiddleware:
    """Small built-in POST throttle for public forms without third-party packages."""

    LIMIT = 45
    WINDOW_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and not request.path.startswith('/admin/'):
            key = f'post-rate:{client_ip(request)}:{request.path}'
            # add() sets the counter only if absent, so the window isn't extended on every hit.
            cache.add(key, 0, self.WINDOW_SECONDS)
            try:
                attempts = cache.incr(key)
            except ValueError:
                cache.set(key, 1, self.WINDOW_SECONDS)
                attempts = 1
            if attempts > self.LIMIT:
                return HttpResponse('Too many requests. Please wait a moment and try again.', status=429)
        return self.get_response(request)
