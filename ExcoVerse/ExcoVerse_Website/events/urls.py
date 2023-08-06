from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('events',views.events, name="events"),
    path('venues',views.all_venues, name="list-venues"),
    path('all_events/',views.all_events, name="all_events"),
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('add_venue',views.add_venue,name='add-venue'),
    path('add_student',views.add_student,name='add-student'),
    path('scan_qrcode/<str:status>/', views.scan_qrcode_view, name='scan_qrcode'),
]


