from django.urls import path

from .views import AboutView, HomeView, NewsletterSignupView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('newsletter/signup/', NewsletterSignupView.as_view(), name='newsletter_signup'),
]
