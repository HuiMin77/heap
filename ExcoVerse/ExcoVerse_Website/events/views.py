from django.shortcuts import render
from .models import Venue
from django.shortcuts import render, redirect
import calendar 
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse 
from events.models import Event, Membership, CCA, Student, Attendance
from .forms import VenueForm, EventForm, StudentForm
import cv2
from pyzbar.pyzbar import decode
import time
from django.http import HttpResponse
from django.http import StreamingHttpResponse, HttpResponse
from pyzbar.pyzbar import decode
import cv2
import time


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

def add_student(request):
    submitted = False
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            add_membership(request, first_name, last_name)  # Pass the 'request' argument
            return HttpResponseRedirect('/add_student?submitted=True')
    else:
        form = StudentForm()  # Instantiate the form
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_student.html', {'form': form, 'submitted': submitted})

def add_membership(request, first_name, last_name):
    if request.user.is_authenticated:
        username = request.user.username
        cca_instance, cca_created = CCA.objects.get_or_create(name=username)
        
        student_instance, student_created = Student.objects.get_or_create(
            first_name=first_name,
            last_name=last_name
        )
        
        membership = Membership.objects.create(student=student_instance, cca=cca_instance)

def generate_frames(status):
   
    print(status)
    cam = cv2.VideoCapture(0)
   
    last_scan_time = 0
    scan_delay = 1  # Set the delay in seconds
    delay_passed = True
   
    while status == 'true':
        
        cam.set(3, 640)
        cam.set(4, 480)

        success, frame = cam.read()
        if not success:
            break

        current_time = time.time()

        if delay_passed and current_time - last_scan_time >= scan_delay:
            for qr_code in decode(frame):
                data = qr_code.data.decode('utf-8')
                print('crying',data)
                take_attendance(data)
               
                last_scan_time = current_time  # Update last scan time
                delay_passed = False  # Set the delay flag

        _, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()

        # Check if the delay has passed and reset the flag
        if not delay_passed and current_time - last_scan_time >= scan_delay:
            delay_passed = True
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + image_data + b'\r\n')
    
    print(status)
    if status == "false":
        cam.release()  # Release the camera when status is 'false'\
        cv2.destroyAllWindows()
        # print('hi1',cam.isOpened())
        return HttpResponse('hi')

def scan_qrcode_view(request,status):

    return StreamingHttpResponse(generate_frames(status), content_type='multipart/x-mixed-replace; boundary=frame')

def take_attendance(data):
    print(data)
    split_parts = data.split('-')
    attendance_list = Attendance.objects.all()
    print(attendance_list)
    
    for attendance in attendance_list:
        print('event',attendance.event.name)
        print(split_parts[0])
        full_name =  attendance.student.first_name + ' '+ attendance.student.last_name
        print(full_name)
        print(str(split_parts[1]))
        if full_name == str(split_parts[0]) and attendance.event.name == str(split_parts[1]):
            print('hi')
            attendanceDB = Attendance.objects.get(id=attendance.id)
            print("Primary key:", attendanceDB.id)  # Access the primary key using 'id'
            attendanceDB.student = attendance.student
            attendanceDB.event = attendance.event
            attendanceDB.present = True
            attendanceDB.save()
            data = {}
            return JsonResponse(data)
        else:
            print('gg.com')

def get_attendance(request):
    #note random order would be order_by(?)
    if request.method == "POST":
        searched = request.POST['searched']
        if searched == '':
            attendance_list = Attendance.objects.all()
            return render(request,'events/attendance.html',{'attendance_list':attendance_list})
        events = Attendance.objects.filter(event__name__contains=searched)  # Assuming 'event' is a ForeignKey to an Event model with a 'name' field
        return render(request,'events/attendance.html',{'searched':searched,'events':events})
        
    else:
        attendance_list = Attendance.objects.all()
        return render(request,'events/attendance.html',{'attendance_list':attendance_list})
