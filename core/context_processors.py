from django.conf import settings


def site_settings(request):
    return {
        'ANALYTICS_ID': settings.ANALYTICS_ID,
    }
