from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import logout, authenticate, login
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import time
from datetime import datetime
from profiles.models import Profile



class GroupForm(ModelForm):        
    groupOptions = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                                  label = "Choose your groups",
                                                  widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Group
        fields = ['groupOptions']

class SearchForm(ModelForm):
    last_name = forms.CharField(required = False)
    first_name = forms.CharField(required = False)
    class Meta:
        model = Profile
        fields = ['profession', 'zipcode','city','state',
                  'last_name','first_name']

def searchUsers(request):
    if request.method != 'POST':
        form = SearchForm ()
    else:
        form = SearchForm (request.POST)        
        if form.is_valid():
            zipcode = form.cleaned_data['zipcode']
            profession = form.cleaned_data['profession']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            results = Profile.objects.all()
            if zipcode != '':
                results = results.filter(zipcode = zipcode)
                print "results 1:",results, zipcode
            if profession != '':
                results = results.filter(profession = profession)
                print "results 2:",results, profession
            if city != '':
                results = results.filter(city = city)
                print "results 3:",results, city                
            if last_name != '':
                results = results.filter(user__last_name = last_name)
            if last_name != '':
                results.filter(user__first_name = first_name)
            return render (request, 'search/searchResults.html', {'results': results}) 
    return render (request, 'search/searchForm.html', {'form': form})        

def groupSelect(request):
    if request.method == 'POST':
        form = GroupForm (request.POST)
        if form.is_valid():
            group = form.cleaned_data['groupOptions']
            request.user.groups = group
            return render (request, 'groups/groupSelect.html' , {'form':form})
    else:
        form = GroupForm(initial={ 'groupOptions': request.user.groups.all() })
        return render (request, 'groups/groupSelect.html' , {'form':form})
    
def home(request):
    return render( request, 'mainSite/home.html')


class LoginForm (forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

def login_view(request):
      if request.method == 'POST':
          form = LoginForm(request.POST)
          if form.is_valid():
              username = form.cleaned_data['username']
              password = form.cleaned_data['password']
              user = authenticate(username=username, password=password)
              if user is not None:
                  if user.is_active:
                      login (request, user)
                      return HttpResponseRedirect('/loginsuccess')
                  else:
                      form.errors['Inactive']="Your account has been disabled"
              else:
                  form.errors['Invalid_login'] = "Username and password do not match."

      else:
          form = LoginForm()
      return render(request, 'login/login.html', {'form':form})

from django.contrib.auth import authenticate, login

class UserCreationFormExtended(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name","last_name",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user
    

def register(request):
    if request.method == 'POST':
        form = UserCreationFormExtended(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            new_user = User.objects.create_user(username=username,
                                                email=email, first_name=first_name,
                                                last_name=last_name,
                                                password = password)
            ## Create a new blank profile here at the
            ## same time as creating a new user
            new_Profile = Profile(user=new_user, joined = datetime.now() )
            new_Profile.save()

            ##Login new user
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
            
        
        else:    
            return render (request, 'register/register.html',{'form':form})        
    else:
        form = UserCreationFormExtended()
    return render (request, 'register/register.html',{'form':form})

   
def logout_view(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def loginsuccess(request):
    return render (request, 'mainSite/home.html')



        
