import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ContactMessageForm

logger = logging.getLogger(__name__)


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('contact:contact')

    def form_valid(self, form):
        message = form.save()
        if settings.CONTACT_EMAIL:
            try:
                send_mail(
                    subject=f'New contact message: {message.subject}',
                    message=f'{message.name} <{message.email}> wrote:\n\n{message.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                )
            except Exception:
                # The message is already saved and visible in the admin, so a mail outage
                # must not turn a successful submission into a server error.
                logger.exception('Could not send contact notification for message %s', message.pk)
        messages.success(self.request, 'Thanks for reaching out. Your message has been received and our team will reply soon.')
        return super().form_valid(form)
