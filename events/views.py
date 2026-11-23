from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .forms import EventRegistrationForm
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 6

    def get_queryset(self):
        queryset = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        query = self.request.GET.get('q', '').strip()
        event_type = self.request.GET.get('type', '').strip()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = Event.EVENT_TYPES
        context['active_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form') or EventRegistrationForm()
        context['registration_closed'] = self.object.date < timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.date < timezone.now():
            messages.info(request, 'Registration for this event has closed.')
            return redirect(self.object.get_absolute_url())
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = self.object
            try:
                registration.save()
            except IntegrityError:
                messages.info(request, 'This email is already registered for the event.')
                return redirect(self.object.get_absolute_url())
            sent = send_mail(
                subject=f'Event registration: {self.object.title}',
                message=(
                    f'Hi {registration.name},\n\n'
                    f'You are registered for {self.object.title} on '
                    f'{timezone.localtime(self.object.date):%A %d %B %Y, %H:%M} at {self.object.location}.\n\n'
                    'See you there!'
                ),
                from_email=None,
                recipient_list=[registration.email],
                fail_silently=True,
            )
            if sent:
                messages.success(request, 'Registration received. We have sent a confirmation email.')
            else:
                messages.success(request, 'Registration received. We look forward to seeing you.')
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))

