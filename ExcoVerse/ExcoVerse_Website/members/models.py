from django.db import models
import hashlib
# Create your models here.
# class CCA(models.Model):
#     username = models.CharField('CCA Name', max_length=120)
#     email = models.EmailField()
#     password = models.CharField(max_length=120)
#     hashed_password = models.CharField(max_length=120)
    
#     def __str__(self):
#         return self.name
    
#     def generate_hashed_password(self,password):
#     # Hash the password using SHA-256
#         hashed_password = hashlib.sha256(password.encode()).hexdigest()
#         print("hashed is "+ hashed_password)
#         return hashed_password
    
#     def save(self, *args, **kwargs):
#         # Generate the random code and hash the password
#         if not self.pk:  # Only generate the code if it's a new Payment poll
            
#             hashed_password = self.generate_hashed_password(self.password)
#             self.hashed_password = hashed_password
#             print("success")
#         super().save(*args, **kwargs) 

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_account_id = models.CharField(max_length=50, blank=True, null=True)
    # Other fields for the user profile

    def __str__(self):
        return self.user.username

