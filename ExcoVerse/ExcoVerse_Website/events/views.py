from django.shortcuts import render
from .models import Venue
from django.shortcuts import render
import calendar 
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse 
from events.models import Event, Membership, CCA, Student, Attendance
from .forms import VenueForm, EventForm, StudentForm
from django.core import serializers
import re

def home(request):
    # img = ['']
    # title = 
    # description = 
    return render(request,'events/home.html',{})

def all_venues(request):
    #note random order would be order_by(?)
    venue_list = Venue.objects.all()
    return render(request,'events/venue_list.html',{'venue_list':venue_list})

def venues_events(request):
    venue_list = Venue.objects.all()
    venue_list_json = serializers.serialize('json', venue_list)
    return JsonResponse(venue_list_json, safe=False)

# Create your views here.
def events(request):  
    all_events = Event.objects.all()
    venue_list = Venue.objects.all()
    context = {
        "events": all_events,
        "venue_list": venue_list,
    }
    return render(request, 'events/events.html', context)
 
def all_events(request):
    events_list = Event.objects.all()
    # events_data = []
    # for event in all_events:
    #     events_data.append({
    #         'title': event.name,
    #         'start': event.start_event_date.strftime("%Y-%m-%d %H:%M:%S"),
    #         'end': event.end_event_date.strftime("%Y-%m-%d %H:%M:%S"),
    #         'id': event.id,
    #         'description': event.description, 
    #         'venue_id': event.venue_id
    #     })
    # return JsonResponse(events_data, safe=False)
    return render(request, 'events/events-list.html',
                  {'event_list':events_list})
 
# def add_event(request):
#     start_event_date = request.GET.get("start_event_date", None)
#     end_event_date = request.GET.get("end_event_date", None)
#     description = request.GET.get("description", None)
#     form = EventForm(request.POST)
#     if form.is_valid():
#         form.save()
#     venue_id = request.GET.get("venue_id", None)
#     name = request.GET.get("name", None)
#     event = Event(name=str(name), start_event_date=start_event_date, end_event_date=end_event_date, description=description, venue_id=venue_id)
#     event.save()
#     data = {}
#     return JsonResponse(data)

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission
            # (e.g., redirect to a success page or show a success message)
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})
 
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



import re

def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()  # Save the event
            attendees = form.cleaned_data.get('attendees')

            for email in attendees:
                print(email)
                # Split the student name into first name and last name
                student_instance, student_created = Student.objects.get_or_create(email=email)

                add_attendance(request, student=student_instance, event=event)

            return HttpResponseRedirect('/add_event?submitted=True')
    else:  
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def add_attendance(request, student, event):
    if request.user.is_authenticated:
        # Get or create the event instance
        # Create the attendance record
        Attendance.objects.create(student=student, event=event, present=False)

def add_student(request):
    submitted = False
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            add_membership(request, email)  # Pass the 'request' argument
            return HttpResponseRedirect('/add_student?submitted=True')
    else:
        form = StudentForm()  # Instantiate the form
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_student.html', {'form': form, 'submitted': submitted})

def add_membership(request, email):
    if request.user.is_authenticated:
        username = request.user.username
        cca_instance, cca_created= CCA.objects.get_or_create(name=username)
        student_instance, student_created = Student.objects.get_or_create(
            email = email
        )
        
        Membership.objects.create(student=student_instance, cca=cca_instance)

def scan_QRCode():
    cam = cv2.VideoCapture(0)

    cam.set(5, 640)
    cam.set(6, 480)

    camera = True
    while camera == True:
        success, frame = cam.read()

        for i in decode(frame):
            # print(i.type)
            print(i.data.decode('utf-8'))
            time.sleep(3)

            cv2.imshow("OurQr_Code_Scanner", frame)
            cv2.waitKey(3)





