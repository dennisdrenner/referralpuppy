
from django.db import models
from django.contrib.auth.models import User

        
class Referral (models.Model):
    REFERRAL_STATUS = ( ('No Contact','NO CONTACT'),
                        ('Customer Contact','CUSTOMER CONTACT'),
                        ('Booked','BOOKED'))
    
    referral_date = models.DateTimeField()
    referrer = models.ForeignKey(User, related_name = 'referring_user')
    receiver = models.ForeignKey(User, related_name = 'receiving_user')
    business_referred_member = models.ForeignKey(User, related_name = 'business_referred_member',
                                                 null=True , blank=True)
    business_referred_non_member = models.CharField(max_length=20, default='', blank=True)
    reference_note = models.TextField(default='' , blank=True)
    authenticated = models.BooleanField(default=0)
    cash_value = models.IntegerField(default=0 , blank=True)
    status = models.CharField(max_length=200, choices = REFERRAL_STATUS, default = 'No Contact',
                              blank =True)
    receiver_notes = models.TextField(default='' , blank=True)
            
    def __unicode__(self):
        return "From %s, %s to %s, %s" %(self.referrer.last_name, self.referrer.first_name,
                                         self.receiver.last_name, self.receiver.first_name)
    
class Email (models.Model):
    sender = models.ForeignKey (User, related_name='sender')
    to = models.ForeignKey (User, related_name='to')
    subject = models.CharField(max_length=20,default='')
    content = models.CharField(max_length=200,default='')

    def __unicode__(self):
        return self.subject



