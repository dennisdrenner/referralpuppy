from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class user_info(models.Model):
    user = models.ForeignKey(User)
    address1 = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=12)
    profession = models.CharField(max_length=20)
    referrals_given = models.IntegerField(default=0)
    referrals_received = models.IntegerField(default=0)
    joined = models.DateTimeField()
    last_login = models.DateTimeField()
    referrer_rating = models.IntegerField(default=0)
    referee_rating = models.IntegerField(default=0)
    

    def __unicode__(self):
        return self.profession
    
        
class reference(models.Model):
    reference_date = models.DateTimeField()
    referrer = models.ForeignKey(User, related_name = 'referrer')
    receiver = models.ForeignKey(User, related_name = 'receiver')
    business_referred_member = models.ForeignKey(User, related_name = 'business_referred_member')
    business_referred_non_member = models.CharField(max_length=20)
    reference_note = models.CharField(max_length=200)
    authenticated = models.BooleanField(default=0)
    cash_value = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.business_referred


 
