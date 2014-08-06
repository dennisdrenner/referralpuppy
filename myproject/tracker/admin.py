from django.contrib import admin
from tracker.models import Referral, Email


class ProfileAdmin (admin.ModelAdmin):
    fields = ['referral_date','referrer','receiver','business_referred_member',
              'business_referred_non_member','reference_note', 'authenticated',
              'cash_value', 'status','receiver_notes']
    
admin.site.register(Referral)
admin.site.register(Email)

##
##class ProfileAdmin (admin.ModelAdmin):
##    fields = ['address1','address','city','state','bio']
##    list_display = ('city','referral_given')
##
##
##admin.site.register(Profile, ProfileAdmin)

