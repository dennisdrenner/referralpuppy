from django.db import models

# Create your models here.

from django.db import models

class Users(models.Model):
    joined_date = models.DateTimeField()
    last_login = models.DateTimeField()
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    profession = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

        
class Reference(models.Model):
    reference_date = models.DateTimeField()
    referrer = models.ForeignKey(Users, related_name = 'referrer')
    receiver = models.ForeignKey(Users, related_name = 'receiver')
    business_referred = models.CharField(max_length=200)
    reference_note = models.CharField(max_length=200)
    authenticated = models.BooleanField(default=0)
    
    
 
