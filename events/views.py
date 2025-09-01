from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Event
from .forms import EventForm
from users.views import organizer_required, participant_required

@login_required
def event_list(request):
    events = Event.objects.order_by('date')
    is_organizer = request.user.groups.filter(name='Organizer').exists()
    return render(request, 'events/event_list.html', {
        'events': events,
        'is_organizer': is_organizer
    })

@login_required
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # RSVP check
    rsvped = event.participants.filter(id=request.user.id).exists()
    
    # Participant check
    is_participant = request.user.groups.filter(name='Participant').exists() if request.user.is_authenticated else False
    
    # Organizer check (optional, jodi template e use koro)
    is_organizer = request.user.groups.filter(name='Organizer').exists() if request.user.is_authenticated else False
    
    context = {
        'event': event,
        'rsvped': rsvped,
        'is_participant': is_participant,
        'is_organizer': is_organizer,
    }
    
    return render(request, 'events/event_detail.html', context)


@login_required
@organizer_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
@organizer_required
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated.')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
@organizer_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, 'Event deleted.')
    return redirect('event_list')

@login_required
@participant_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.participants.filter(id=request.user.id).exists():
        messages.info(request, "You already RSVP'd to this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, 'RSVP confirmed! A confirmation email was sent.')
    return redirect(reverse('event_detail', args=[event.id]))
