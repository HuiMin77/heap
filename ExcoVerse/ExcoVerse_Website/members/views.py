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
from .models import UserProfile
import stripe
import os

from dotenv import load_dotenv
# from events.models import PaymentPoll
import hashlib
# from importlib import import_module


# Import the PaymentPoll model after initializing the Django application

# Load environment variables from .env file

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.', '.env')
load_dotenv(dotenv_path)
stripe.api_key = os.environ.get('STRIPE_API_KEY')

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
            email = form.cleaned_data['email']
            user = authenticate(username = username,password=password)
            login(request,user)
            stripe_account_tuple = create_connected_account()
            account_id = stripe_account_tuple[0]
            account_link = stripe_account_tuple[1]
            
            redirect_stripe_url = account_link.url
            print(account_link)
            stripe_account_id = account_id
            update_stripe_account_id(request.user,stripe_account_id)

            
            print(redirect_stripe_url)
            messages.success(request,("Registration Successful"))
            

            return redirect(redirect_stripe_url)
    else:
        form = RegisterUserForm()
       
    return render(request,'authenticate/register_user.html',{'form':form,})

def create_connected_account():
    account = stripe.Account.create(
        type="standard",  # Use "standard" or another account type as needed
        country="SG",  # Replace with the country code of the connected account
       
        
    )
    account_id = account.stripe_id

    account_link = stripe.AccountLink.create(
        account=account_id,
        refresh_url="http://127.0.0.1:8000/authenticate/register_user.html",
        return_url="http://127.0.0.1:8000/",
        type="account_onboarding",
    )
    return (account_id,account_link)

def update_stripe_account_id(user, stripe_account_id):
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.stripe_account_id = stripe_account_id
    user_profile.save()

# def qr_gen(request):
#     if request.method == 'POST':

#         return render(request, 'index.html', {'img_name': img_name})
#     return render(request, 'index.html')