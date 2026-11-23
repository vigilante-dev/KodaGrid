from django.conf import settings


def site_settings(request):
    return {
        'ANALYTICS_ID': settings.ANALYTICS_ID,
        'PUBLIC_CONTACT_EMAIL': settings.PUBLIC_CONTACT_EMAIL,
        'PUBLIC_CONTACT_PHONE': settings.PUBLIC_CONTACT_PHONE,
        'SOCIAL_LINKS': settings.SOCIAL_LINKS,
    }
