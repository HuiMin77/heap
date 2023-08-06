from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('add_event',views.add_event,name='add-event'),
    path('events',views.events, name="events"),
    path('venues',views.all_venues, name="list-venues"),
    path('all_events/',views.all_events, name="list-events"),
    path('all_cal_events/',views.all_cal_events, name="all_cal_events"),
    path('add_event/', views.add_event, name='add_event'), 
    # path('add_calendar_event/', views.add_calendar_event, name='add_calendar_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('add_venue',views.add_venue,name='add-venue'),
    path('add_student',views.add_student,name='add-student'),
    # path('add_event',views.add_event,name='add-event')
]
