from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['address1','address2','city',
                  'state','zipcode','zipcode2','phone','profession','bio','website','photo']

def viewProfile(request, publicProfileName = 'dennisdrenner1'):
    userProfiles = Profile.objects.all()
    try: 
        userProfile = userProfiles.get(user__username = publicProfileName)
        ## Update values for referrals given and received
        userProfile.referral_given()
        userProfile.referral_given()
        print "RG", userProfile.referrals_given
        
    except ObjectDoesNotExist:
        return HttpResponse("Alert, alert, user does not exist!")
    
    return render (request, 'viewPublicProfile.html', {'userProfile': userProfile}) 
            

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES,
                               instance=request.user.profile)
        if form.is_valid():
            form.save()
            return render (request, 'edit_profile2.html', {'form':form})
    else:
        if request.user.profile:
 
            form = EditProfileForm(instance=request.user.profile)
        else:
            return HttpResponse ('You have no profile')
                
    return render (request, 'edit_profile2.html',{'form':form})
