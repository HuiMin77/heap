from django import forms
from django.forms import ModelForm
from .models import Venue, Event

#Create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name','image_url','address','zip_code','web')
        labels = {
            'name': '',
            'image_url':'',
            'address':'',
            'zip_code':'',
            'web':''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'image_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Image URL'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Zip Code'}),
            'web':forms.TextInput(attrs={'class':'form-control','placeholder':'Webiste'})
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','start_event_date','end_event_date','venue','image_url','internal','manager','description')
        labels = {
            'name': '',
            'start_event_date':'',
            'end_event_date':'',
            'venue':'',
            'image_url':'',
            'internal':'Internal Event?',
            'manager':'',
            'description':'',
            


        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'start_event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Start Event Date'}),
            'end_event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'End Event Date'}),
            'venue':forms.TextInput(attrs={'class':'form-control','placeholder':'Venue'}),
            'image_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Image URL'}),
            'internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'manager':forms.TextInput(attrs={'class':'form-control','placeholder':'manager'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),    
            
        }
