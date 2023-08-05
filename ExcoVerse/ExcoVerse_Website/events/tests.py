import django
django.setup()
import os
import sys
from django.test import TestCase
from events.models import PaymentPoll
from events.models import Event
from events.models import PaymentDetails
from events.models import Student
from events.models import Tracking_Payment


student = Student.objects.get(chat_id = 'iynixx')
event = Event.objects.get(name = PaymentPoll.payment_event)
tracking_payments = Tracking_Payment.objects.filter(student=student, event = event)
for payment in tracking_payments:
    print(payment)
    payment.paid = True
    payment.save()
# Create your tests here.
