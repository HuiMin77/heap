from django.shortcuts import render
from .models import Venue
from django.shortcuts import render, get_list_or_404
import calendar 
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
# from django.http import JsonResponse 
from events.models import Event, Membership, PaymentDetails, PaymentPoll, Tracking_Payment, Student
from .forms import VenueForm, EventForm, StudentForm, PaymentForm, EventSelectionForm
from members.models import UserProfile, User
from django.db.models import Sum

import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import stripe
import os
stripe.api_key = os.environ.get('STRIPE_API_TOKEN')


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
        # Valid stuff?
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_student?submitted=True')
    else: 
        form = StudentForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request,'events/add_student.html',{'form':form, 'submitted': submitted})

# def add_cca(request):
#     submitted = False
#     if request.method == "POST":
#         form = CCAForm(request.POST)
#         # Valid stuff?
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/add_cca?submitted=True')
#     else: 
#         form = StudentForm
#         if 'submitted' in request.GET:
#             submitted = True
#     return render(request,'events/add_cca.html',{'form':form, 'submitted': submitted})

def add_payment(request):
    submitted = False
    password = ''
    # if they fill out the form and submit
    
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # payment_poll = form.save()  # Save the form data and get the PaymentPoll instance
            # print(payment_poll) 
            # # Get the form data
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            payment_event = form.cleaned_data['payment_event']
            
            
            # payment_poll = PaymentPoll.objects.get(subject=subject)
            # password = form.cleaned_data['password']
            payment_poll = form.save()  # Save the form data without committing to the database
            password = payment_poll.password  # Generate the password

            poll_creator = request.user
            payment_poll.poll_creator = poll_creator
            

            # payment_poll.stripe_account_id = user_profile.stripe_account_id
            payment_poll.save()

            # Hash the password
            # Save the instance with the generated and hashed password
            submitted = True
            print(payment_poll)
            print(subject,description,price,password,payment_event,payment_poll.poll_creator)
            students = Student.objects.all()

            #this prevents the same student participating in the same event from being allowed to pay twice (even if there are 2 payment poll instances created)
            for student in students:
                if Tracking_Payment.objects.get(student=student, event=payment_event) is None:
                    Tracking_Payment.objects.create(student=student, event=payment_event, price=payment_poll)
            
            # return HttpResponseRedirect('/add_payment?submitted=True')
            return render(request, 'events/add_payment.html', {'form': form, 'submitted': submitted, 'password': password})
    else:
        form = PaymentForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request,'events/add_payment.html',{'form':form,'submitted':submitted,'password':password})

def transfer_payment(request):
    poll_creator = request.user
    if request.method == 'POST':
    
    # stripe_account_id = user_profile.stripe_account_id
    # poll_id = PaymentPoll.objects.get(poll_creator=poll_creator)
    
    # payment_details_list = PaymentDetails.objects.filter(poll_id=poll_id,is_success_club=False,is_success_excoverse=True)
    # total_amount_sum = payment_details_list.aggregate(Sum('total_amount'))['total_amount__sum']
    # print(stripe.api_key)
    
        # unprocessed_payment_count = request.POST.get('unprocessed_payment_count')
        # tracking_payment_ids = request.POST.get('tracking_payment_ids')
        unprocessed_payment_count=0
        unprocessed_payment_object = Tracking_Payment.objects.filter(is_success_excoverse=True, is_success_club=False)
        print(unprocessed_payment_object)

        
        for p in unprocessed_payment_object:
            unprocessed_payment_count += p.price.price
        # unprocessed_payment_count = unprocessed_payment_object.aggregate(Sum('price'))['price']
        
        print("cost",unprocessed_payment_count)
        
        # tracking_payment_id_list = [int(id) for id in tracking_payment_ids.split(',')]

        # Retrieve the QuerySet using the IDs
        

            # Replace 'your-secret-key' with your actual Stripe secret key
        stripe.api_key = stripe.api_key

        try:
            # Create the transfer using the Stripe API
            user_profile = UserProfile.objects.get(user=poll_creator)

            stripe_account_id = user_profile.stripe_account_id
            # payment_details_list = PaymentDetails.objects.filter(stripe_account_id=stripe_account_id,is_success_club=False)
            # total_amount_sum = payment_details_list.aggregate(Sum('total_amount'))['total_amount__sum']
            print("stripe acct",stripe_account_id)
            # print(total_amount_sum)
            transfer = stripe.Transfer.create(
                amount=int(unprocessed_payment_count)*100,  # Replace with the actual amount
                currency='sgd',
                destination=stripe_account_id,
            )

            print("transfer to club success",transfer)
            unprocessed_payment_object.update(is_success_club=True)
            print("successfully updated db")
            
            return render(request, 'events/transfer_payment.html')

        except stripe.error.StripeError as e:
            print("Stripe Error:", str(e))
            return render(request, 'events/transfer_payment.html')

    
    # return render(request, 'events/transfer_payment.html',{'total_amount_sum': total_amount_sum,'payment_details_list':payment_details_list})
    

def track_event_payment_polls(request):
    selected_event = None
    tracking_payments = None
    unprocessed_payment_count = 0

    if request.method == 'POST':
        form = EventSelectionForm(request.POST)
        if form.is_valid():
            selected_event = form.cleaned_data['event']
            print(selected_event)
            if selected_event:
                
                tracking_payments = Tracking_Payment.objects.filter(event=selected_event).order_by('is_success_excoverse')
            else:
                tracking_payments = Tracking_Payment.objects.all().order_by('is_success_excoverse')

            # payment_poll = PaymentPoll.objects.get(payment_event=selected_event)
            
            
            # price = payment_poll.price
            unprocessed_payment_object = tracking_payments.filter(is_success_excoverse=True, is_success_club=False)
            print(unprocessed_payment_object)

            
            for p in unprocessed_payment_object:
                unprocessed_payment_count += p.price.price
            # unprocessed_payment_count = unprocessed_payment_object.aggregate(Sum('price'))['price']
            total_paid = tracking_payments.filter(is_success_excoverse=True).count()
            total_never_pay = tracking_payments.filter(is_success_excoverse=False).count()
            
    else:
        form = EventSelectionForm()
        # tracking_payments_list = [{}]
    
        # tracking_payments_js.on = json.dumps(tracking_payments_list)

        unprocessed_payment_object = Tracking_Payment.objects.filter(is_success_excoverse=True, is_success_club=False)
        print(unprocessed_payment_object)

        
        for p in unprocessed_payment_object:
            unprocessed_payment_count += p.price.price
        # unprocessed_payment_count = unprocessed_payment_object.aggregate(Sum('price'))['price']
        total_paid = Tracking_Payment.objects.filter(is_success_excoverse=True).count()
        total_never_pay = Tracking_Payment.objects.filter(is_success_excoverse=False).count()

    context = {
        'form': form,
        'tracking_payments': tracking_payments,
        'selected_event': selected_event,
        'unprocessed_payment_count':unprocessed_payment_count,
        'total_paid': total_paid,
        'total_never_pay': total_never_pay,
        


    }

    return render(request, 'events/Track_Payments.html', context)

    # stripe.Transfer.create(
    #         amount=total_amount_sum,
    #         currency="sgd",
    #         destination=stripe_account_id
    # )
    


# @csrf_exempt
# def initiate_transfer(request):
    

    #         return JsonResponse({'success': True})
    #     except stripe.error.StripeError as e:
    #         return JsonResponse({'error': str(e)})

    # return JsonResponse({'error': 'Invalid request method'})

