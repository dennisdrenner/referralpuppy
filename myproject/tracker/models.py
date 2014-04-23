from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class User_info (models.Model):
    user = models.ForeignKey(User)
    address1 = models.CharField(max_length=20, default ='')
    address = models.CharField(max_length=20,default ='')
    city = models.CharField(max_length=20,default ='')
    state = models.CharField(max_length=2,default ='')
    zipcode = models.CharField(max_length=10,default ='')
    phone = models.CharField(max_length=12,default ='')
    profession = models.CharField(max_length=20,default ='')
    referrals_given = models.IntegerField(default=0)
    referrals_received = models.IntegerField(default=0)
    joined = models.DateTimeField()
    last_login = models.DateTimeField()
    referrer_rating = models.IntegerField(default=0)
    referee_rating = models.IntegerField(default=0)
    bio=models.CharField(max_length=500, default='')
    website=models.CharField(max_length=500, default='')

    def __unicode__(self):
        return self.profession
    
        
class Referral (models.Model):
    referral_date = models.DateTimeField()
    referrer = models.ForeignKey(User, related_name = 'referrer')
    receiver = models.ForeignKey(User, related_name = 'receiver')
    business_referred_member = models.ForeignKey(User, related_name = 'business_referred_member', null=True)
    business_referred_non_member = models.CharField(max_length=20, default='')
    reference_note = models.CharField(max_length=200,default='')
    authenticated = models.BooleanField(default=0)
    cash_value = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.reference_note


class Email (models.Model):
    sender = models.ForeignKey (User, related_name='sender')
    to = models.ForeignKey (User, related_name='to')
    subject = models.CharField(max_length=20,default='')
    content = models.CharField(max_length=200,default='')

    def __unicode__(self):
        return self.subject



