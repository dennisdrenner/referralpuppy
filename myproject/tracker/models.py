from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class Profile (models.Model):
    user = models.OneToOneField(User)
    address1 = models.CharField(max_length=20, default ='', blank=True)
    address = models.CharField(max_length=20,default ='', blank=True)
    city = models.CharField(max_length=20,default ='', blank=True)
    state = models.CharField(max_length=2,default ='' , blank=True)
    zipcode = models.CharField(max_length=10,default ='' , blank=True)
    phone = models.CharField(max_length=12,default ='' , blank=True)
    profession = models.CharField(max_length=20,default ='' , blank=True)
    referrals_given = models.IntegerField(default=0)
    referrals_received = models.IntegerField(default=0)
    joined = models.DateTimeField()
    referrer_rating = models.IntegerField(default=0)
    referee_rating = models.IntegerField(default=0)
    bio=models.CharField(max_length=500, default='' , blank=True)
    website=models.CharField(max_length=500, default='' , blank=True)

##    def __unicode__(self):
##        u=self.user.get.first_name
##        return u
    
        
class Referral (models.Model):
    referral_date = models.DateTimeField()
    referrer = models.ForeignKey(User, related_name = 'referrer')
    receiver = models.ForeignKey(User, related_name = 'receiver')
    business_referred_member = models.ForeignKey(User, related_name = 'business_referred_member', null=True , blank=True)
    business_referred_non_member = models.CharField(max_length=20, default='', blank=True)
    reference_note = models.CharField(max_length=200,default='' , blank=True)
    authenticated = models.BooleanField(default=1)
    cash_value = models.IntegerField(default=0 , blank=True)
    
    def __unicode__(self):
        return self.referrer ##"Referral to: %s" %self.business_referred_non_member


class Email (models.Model):
    sender = models.ForeignKey (User, related_name='sender')
    to = models.ForeignKey (User, related_name='to')
    subject = models.CharField(max_length=20,default='')
    content = models.CharField(max_length=200,default='')

    def __unicode__(self):
        return self.subject



