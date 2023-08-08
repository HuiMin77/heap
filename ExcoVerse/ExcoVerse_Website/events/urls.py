from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('add_event',views.add_event,name='add-event'),
    path('events',views.events, name="events"),
    path('venues',views.all_venues, name="list-venues"),
    path('update/', views.update, name='update'),
    path('remove/<str:id>/', views.remove, name='remove'),
    path('add_venue',views.add_venue,name='add-venue'),
    path('add_student',views.add_student,name='add-student'),
    path('add_payment',views.add_payment,name='payment'),
    path('transfer_payment',views.transfer_payment,name='transfer-payment'),
    path('track_payments',views.track_event_payment_polls,name='track_payments'),
    path('scan_qrcode/<str:status>/<str:eventId>', views.scan_qrcode_view, name='scan_qrcode'),
    path('attendance/<str:id>/', views.get_attendance, name='attendance'),
    path('all_events/',views.all_events, name="list-events"),
    path('all_cal_events/',views.all_cal_events, name="all_cal_events"),
    path('add_calendar_event/',views.add_calendar_event, name="add_calendar_event"),
    path('change_stripe_acct/',views.change_stripe_acct, name="change_stripe_acct"),
    

]


