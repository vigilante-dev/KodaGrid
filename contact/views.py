from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ContactMessageForm


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactMessageForm
    success_url = reverse_lazy('contact:contact')

    def form_valid(self, form):
        message = form.save()
        send_mail(
            subject=f'New contact message: {message.subject}',
            message=f'{message.name} <{message.email}> wrote:\n\n{message.message}',
            from_email=None,
            recipient_list=['hello@codesavannah.local'],
            fail_silently=True,
        )
        messages.success(self.request, 'Thank you. Our admissions team will respond soon.')
        return super().form_valid(form)

# Create your views here.
