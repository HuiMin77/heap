from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from events.models import CCA

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    # first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    # student_id = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # mobile_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.ModelChoiceField(queryset=CCA.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('email','username','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'