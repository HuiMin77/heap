from django import forms
from django.forms import ModelForm
from .models import Venue, Event, Student

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
            'web':forms.TextInput(attrs={'class':'form-control','placeholder':'Website'})
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','start_event_date','end_event_date','venue', 'attendees', 'internal','description')
        labels = {
            'name': 'Event Name',
            'start_event_date':'Start Event Date',
            'end_event_date':'End Event Date',
            'venue':'Venue',
            'internal':'Internal Event?',
            'attendees': 'Attendees',
            'description':'Description',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'start_event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Start Event Date'}),
            'end_event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'End Event Date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-select','placeholder':'Attendees'}),
            'internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),    
            
        }


#Create a student form
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('first_name','last_name','student_id','email','mobile_number','chat_id')
        labels = {
            'first_name': '',
            'last_name':'',
            'student_id':'',
            'email':'',
            'mobile_number':'',
            'chat_id':''
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'student_id':forms.TextInput(attrs={'class':'form-control','placeholder':'Student ID'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
            'mobile_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile Number'}),
            'chat_id':forms.TextInput(attrs={'class':'form-control','placeholder':'Chat ID'})
        }


class VenuesEventsForm(ModelForm):
    venue = forms.ModelChoiceField(queryset=Venue.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
            model = Event
            fields = ['name', 'start_event_date', 'end_event_date', 'description', 'venue']

        # Optionally, you can customize the way the venue field is displayed as a dropdown
    def __init__(self, *args, **kwargs):
            super(EventForm, self).__init__(*args, **kwargs)
            self.fields['venue'].widget.attrs.update({'class': 'form-control'})  # Add CSS class for styling