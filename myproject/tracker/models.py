from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class DB_Users(models.Model):
    profession = models.CharField(max_length=20)
    referrals_given = models.IntegerField(default=0)
    referrals_received = models.IntegerField(default=0)

    def __unicode__(self):
        return self.first + ' ' + self.last
    
        
class Reference(models.Model):
    reference_date = models.DateTimeField()
    referrer = models.ForeignKey(User, related_name = 'referrer')
    receiver = models.ForeignKey(User, related_name = 'receiver')
    business_referred = models.CharField(max_length=200)
    reference_note = models.CharField(max_length=200)
    authenticated = models.BooleanField(default=0)
    
    def __unicode__(self):
        return self.business_referred
 
