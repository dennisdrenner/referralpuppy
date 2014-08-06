from datetime import datetime
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import View, ListView, CreateView
from django.core.urlresolvers import reverse
##from tracker.models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.models import modelformset_factory
from django.forms import ModelForm
from tracker.models import Referral

class ReferralForm(ModelForm):
    class Meta:
        model = Referral
        fields = ['receiver', 'business_referred_member','business_referred_non_member',
                  'reference_note', 'cash_value']
    
@login_required
def referral (request, publicProfileName = 'dennisdrenner1'):
    
    if request.method == 'POST':
        form = ReferralForm(request.POST)
        if form.is_valid():
            ## form data
            receiver = form.cleaned_data['receiver']
            business_referred_member = form.cleaned_data['business_referred_member']
            business_referred_non_member = form.cleaned_data['business_referred_non_member']
            reference_note = form.cleaned_data['reference_note']
            cash_value = form.cleaned_data['cash_value']
            ## non form data            
            referrer = request.user
            referral_date = datetime.now()
            authenticated = False

            ##update referrals given by active user and save to DB
            current_user_profile=request.user.profile
            current_user_profile.referrals_given +=1
            current_user_profile.save()
            print "refs given", current_user_profile.referrals_given
            
            ##create new referral with info from validated form and save to DB
            new_referral = Referral(receiver = receiver, business_referred_member = business_referred_member,
                                    business_referred_non_member = business_referred_non_member,
                                    reference_note = reference_note, cash_value = cash_value,
                                    referrer = referrer, referral_date = referral_date,
                                    authenticated = authenticated)                                    
            new_referral.save()
            return render (request, 'referral_success.html',{'receiver':receiver,
                                                             'cash_value': cash_value})
        
    else:
        form = ReferralForm(initial = {'receiver' : User.objects.get(username=publicProfileName)})
        return render (request, 'referral_form.html', {'form':form})





 
class ReceivedReferralListForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super (ReceivedReferralListForm, self).__init__(*args, **kwargs)
        self.referrer = 'defaultReferrerName'
        self.referral_date = 'defaultDate'
        self.business_referred_member = ''
        self.business_referred_non_member = ''
        self.reference_note = ''
        
    class Meta:
        model = Referral        
        fields = ['cash_value','receiver_notes', 'status']  


class GivenReferralListForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super (GivenReferralListForm, self).__init__(*args, **kwargs)
        self.referral_date = 'defaultDate'
        self.receiver = 'defaultReceiverName'
        self.business_referred_member = ''
        self.business_referred_non_member = ''
        self.status = 'defaultStatus'
        self.cash_value = 0
   
    class Meta:
        model = Referral
        fields = ['reference_note']
    
@login_required
def myReferrals(request):
    ReceivedReferralListFormSet = modelformset_factory(Referral, form = ReceivedReferralListForm, extra=0)    
    GivenReferralListFormSet = modelformset_factory(Referral, form = GivenReferralListForm, extra=0)          
    referrals_received = Referral.objects.filter(receiver = request.user)
    referrals_given = Referral.objects.filter(referrer = request.user)
    
    if request.method == "POST":
        formset = ReceivedReferralListFormSet(request.POST, queryset = referrals_received)
        formset2 = GivenReferralListFormSet(request.POST, queryset = referrals_given)
##        
        if  formset.is_valid(): 
            for f_form in formset:
                if f_form.is_valid() and not f_form.has_changed():
                    f_form.save()
        if formset2.is_valid():
            for f_form in formset2:
                if f_form.is_valid() and not f_form.has_changed():
                    f_form.save()

            return redirect ('tracker.views.myReferrals')
        else:
            return render (request, 'referral_list.html', {'formset2': formset2, 'formset':formset})
        
    else:   ## for GET request 
            formset = ReceivedReferralListFormSet(queryset = referrals_received)
            formset2 = GivenReferralListFormSet(queryset = referrals_given)

## These loops attaches values to the formsets that we don't want the user to be able to edit, but which
## we do want them to be able to see (like the date, status, etc)

            ## Received referrals
            i=0
            for form in formset:
                form.referral_date = referrals_received[i].referral_date
                form.referrer = referrals_received[i].referrer
                form.business_referred_member = referrals_received[i].business_referred_member
                form.business_referred_non_member = referrals_received[i].business_referred_non_member
                form.reference_note = referrals_received[i].reference_note
                i+=1

            ## Given referrals
            i=0
            for form in formset2:
                print "FORMSET2", form
                form.referral_date = referrals_given[i].referral_date
                form.receiver = referrals_given[i].receiver
                form.cash_value = referrals_given[i].cash_value
                form.business_referred_member = referrals_given[i].business_referred_member
                form.business_referred_non_member = referrals_given[i].business_referred_non_member
                form.status = referrals_given[i].status     
                i+=1

               
            return render (request, 'referral_list.html', {'formset2': formset2,'formset':formset})
        

def receivedHandler(request):
    ReceivedReferralListFormSet = modelformset_factory(Referral,
                                                       form = ReceivedReferralListForm, extra=0)     
    referrals_received = Referral.objects.filter(receiver = request.user)

    if request.method == "POST":
        formset = ReceivedReferralListFormSet(request.POST, queryset = referrals_received)
##        formset2 = GivenReferralListFormSet(request.POST, queryset = referrals_given)
##        
        if  formset.is_valid():
            formset.save()
            
            return redirect ('tracker.views.myReferrals')
        else:
            return render (request, 'referral_list.html', {'formset':formset})
    
##    return HttpResponse ("Received handler")

def sentHandler(request):
    GivenReferralListFormSet = modelformset_factory(Referral, form = GivenReferralListForm, extra=0)          
    referrals_given = Referral.objects.filter(referrer = request.user)

    if request.method == "POST":
        formset2 = GivenReferralListFormSet(request.POST, queryset = referrals_given)
        
        if  formset2.is_valid():
            formset2.save()
            
            return redirect ('tracker.views.myReferrals')
        else:
            return render (request, 'referral_list.html', {'formset':formset})
    

##class CreateProfileView(CreateView):
##    model = Profile
##    template_name='edit_profile.html'
##
##    def get_success_url(self):
##        return reverse('profiles-list')
    
##def login_user (request):
##    state = "Please log in below..."
##    username = password = ''
##    if request.POST:
##        username = request.POST.get('username')
##        password = request.POST.get('password')
##        user = authenticate(username=username, password=password)
##        if user is not None:
##            if user.is_active:
##                login(request, user)
##                state = "You're successfully logged in!"
##            else:
##                state = "Your account is not active, please contact the site admin."
##        else:
##            state = "Your username and/or password were incorrect."
##    return render_to_response('login/auth.html',{'state':state, 'username': username})
##

    
##def index(request):
##    return HttpResponse("Hello, world. This is the referral tracker app")

##def profile(request):
##    return HttpResponse("You're looking at the profile page")
##
##def newreference(request):
##    return HttpResponse("You're looking at the new reference page")

##def vote(request):
##    return HttpResponse("You're voting on poll")
