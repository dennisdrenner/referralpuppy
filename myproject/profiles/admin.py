from django.contrib import admin
from profiles.models import Profile


class ProfileAdmin (admin.ModelAdmin):
    fields = ['user','address1','address2','city',
              'state','zipcode','zipcode2','phone','profession','bio',
              'website','joined','photo', 'referrals_given','referrals_received']
 
admin.site.register(Profile, ProfileAdmin)

