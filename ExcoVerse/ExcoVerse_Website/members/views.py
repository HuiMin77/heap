from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import time
from events.models import CCA

def login_user(request):
    # Check if the person go to the webpage or fill out the form
    cca_list = CCA.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
            
        else:
            messages.success(request,("There Was An Error Logging In, Try Again..."))
            # Return an 'invalid login' error message.
            return redirect('login')
    else:
        return render(request,'authenticate/login.html',{'cca_list':cca_list})


def logout_user(request):
    logout(request)
    messages.success(request,("You Were Logged Out!"))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print('form is valid')
            form.save()
            username = form.cleaned_data['username']
            print(username)
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password=password)
            login(request,user)
            messages.success(request,("Registration Successful"))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request,'authenticate/register_user.html',{'form':form,})

# def qr_gen(request):
#     if request.method == 'POST':

#         return render(request, 'index.html', {'img_name': img_name})
#     return render(request, 'index.html')
