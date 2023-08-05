from django.db import models

import random 
import string 
import hashlib 
 

# Create your models here.
class CCA(models.Model):
    name = models.CharField('CCA Name', max_length=120)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_id = models.CharField(max_length=30)
    email = models.EmailField('User Email')
    mobile_number = models.CharField(max_length=30)
    chat_id = models.CharField(max_length=30, null = True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Membership(models.Model):
    cca = models.ForeignKey(CCA, blank=True, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.CASCADE)
    exco = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.student)

class Payment(models.Model):
    membership = models.ForeignKey(Membership, blank=True, null=True, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.membership)

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    image_url = models.CharField('Venue Image URL', max_length=200) 
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    web = models.URLField('Website Address', blank=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    start_event_date = models.DateTimeField('Event Start Date')
    end_event_date = models.DateTimeField('Event End Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    image_url = models.CharField('Event Image URL', max_length=200)
    internal = models.BooleanField(default=False)
    manager = models.ForeignKey(Student, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return self.student

class PaymentPoll(models.Model): 
    subject = models.CharField('Subject', max_length=120) 
    description = models.TextField('Description') 
    price = models.DecimalField('Price', max_digits=8, decimal_places=2) 
 
    password = models.CharField(max_length=6) 
    hashed_password = models.CharField(max_length=120) 
    payment_event =  models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE) 
 
    def __str__(self): 
        return self.subject 
    def generate_poll_password(self): 
    # Generate a random 6-character code consisting of numbers and uppercase letters 
        characters = string.digits + string.ascii_uppercase 
        code = ''.join(random.choices(characters, k=6)) 
        print("password is"+code) 
        return code 
 
    def generate_hashed_poll_password(self,plain_password): 
    # Hash the password using SHA-256 
        hashed_password = hashlib.sha256(plain_password.encode()).hexdigest() 
        print("hashed is "+ hashed_password) 
        return hashed_password 
     
    def save(self, *args, **kwargs): 
        # Generate the random code and hash the password 
        if not self.pk:  # Only generate the code if it's a new Payment poll 
            six_digit_code = self.generate_poll_password() 
            self.password = six_digit_code 
            hashed_password = self.generate_hashed_poll_password(six_digit_code) 
            self.hashed_password = hashed_password 
            print("success") 
        super().save(*args, **kwargs)  
    
 
class PaymentDetails(models.Model): 
    tele_handle = models.CharField(max_length=255, default = '')
    user_id = models.IntegerField() 
    chat_id = models.IntegerField() 
    payment_id = models.CharField(max_length=255) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    currency = models.CharField(max_length=3) 
    payment_provider = models.CharField(max_length=255) 
    is_success = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    
class Tracking_Payment(models.Model):
    student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default = '')
    paid = models.BooleanField(default=False)
