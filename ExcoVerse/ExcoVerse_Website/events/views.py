from django.shortcuts import render
from .models import Venue
from django.shortcuts import render
import calendar 
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse 
from events.models import Event
from .forms import VenueForm, EventForm

def home(request):
    # img = ['']
    # title = 
    # description = 
    return render(request,'events/home.html',{})

def all_venues(request):
    #note random order would be order_by(?)
    venue_list = Venue.objects.all()
    return render(request,'events/venue_list.html',{'venue_list':venue_list})

 
# Create your views here.
def events(request):  
    all_events = Event.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'events/events.html',context)
 
def all_events(request):
    all_events = Event.objects.all()
    events_data = []
    for event in all_events:
        events_data.append({
            'title': event.name,
            'start': event.start_event_date.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event.end_event_date.strftime("%Y-%m-%d %H:%M:%S"),
            'id': event.id,
        })
    return JsonResponse(events_data, safe=False)
 
def add_event(request):
    start_event_date = request.GET.get("start_event_date", None)
    end_event_date = request.GET.get("end_event_date", None)
    name = request.GET.get("name", None)
    event = Event(name=str(name), start_event_date=start_event_date, end_event_date=end_event_date)
    event.save()
    data = {}
    return JsonResponse(data)
 
def update(request):
    start_event_date = request.GET.get("start_event_date", None)
    end_event_date = request.GET.get("end_event_date", None)
    name = request.GET.get("name", None)
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.start_event_date = start_event_date
    event.end_event_date = end_event_date
    event.name = name
    event.save()
    data = {}
    return JsonResponse(data)
 
def remove(request):
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        # Valid stuff?
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else: 
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request,'events/add_venue.html',{'form':form, 'submitted': submitted})

# def add_event(request):
#     submitted = False
#     if request.method == "POST":
#         form = EventForm(request.POST)
#         # Valid stuff?
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/add_event?submitted=True')
#     else: 
#         form = EventForm
#         if 'submitted' in request.GET:
#             submitted = True
#     return render(request,'events/add_event.html',{'form':form, 'submitted': submitted})