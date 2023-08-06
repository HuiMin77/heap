from django.db import models

# Create your models here.
class CCA(models.Model):
    name = models.CharField('CCA Name', max_length=120)
    email = models.CharField('Email', max_length=120,null=True)
    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_id = models.CharField(max_length=30)
    email = models.EmailField('User Email', unique=True)
    mobile_number = models.CharField(max_length=30)
    chat_id = models.CharField(max_length=30, null = True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.student_id

class Membership(models.Model):
    cca = models.ForeignKey(CCA, blank=True, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.CASCADE)
    # exco = models.BooleanField(default=False)
    
    def __str__(self):
        return self.student.email + ' ' + self.cca.name

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
    attendees = models.ManyToManyField(Student, blank=True, null=True)
    internal = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return self.student.first_name + ' ' + self.student.last_name 

