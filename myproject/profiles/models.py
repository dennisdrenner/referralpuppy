from django.db import models
from django.contrib.auth.models import User, Group
from tracker.models import Referral



class Profile (models.Model):
    PROFESSIONS = (
        ('LAWYER','Lawyer'),
        ('DOCTOR','Doctor'),
        ('INDIAN_CHIEF','Indian Chief'),
        )
    
    user = models.OneToOneField(User)

    address1 = models.CharField(max_length=60, default ='', blank=True)
    address2 = models.CharField(max_length=60, default ='', blank=True)
    city = models.CharField(max_length=60, default ='', blank=True)
    state = models.CharField(max_length=2,default ='' , blank=True)
    zipcode = models.CharField(max_length=5, default = '' , blank=True)
    zipcode2 = models.CharField(max_length=4, default = '' , blank=True)
    phone = models.CharField(max_length=12,default ='' , blank=True)
    profession = models.CharField(max_length=20,default ='' ,
                                  choices = PROFESSIONS, blank=True)
    referrals_given = models.IntegerField(default=0, blank = True)
    referrals_received = models.IntegerField(default=0, blank=True)
    joined = models.DateTimeField()
    referrer_rating = models.IntegerField(default=0, blank=True)
    referee_rating = models.IntegerField(default=0, blank=True)
    bio=models.TextField(default='' , blank=True)
    website=models.URLField(max_length=200, default='' , blank=True)
    photo = models.ImageField(upload_to='userProfilePhotos/',
                              default='userProfilePhotos/None/defaultPhoto.jpg',
                              blank=True)

    def __unicode__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)

    def referral_given(self):
           referrals_given = Referral.objects.filter(referrer = self.user).count()
           return referrals_given
        
    def referral_received(self):
           referrals_received = Referral.objects.filter(receiver = self.user).count()
           return referrals_given
