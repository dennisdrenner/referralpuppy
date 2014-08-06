from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

## MAIN SITE VIEWS AND URLS
                       
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','myproject.views.home', name='home'),                    
##    url(r'^login/','django.contrib.auth.views.login',
##        {'template_name': 'login/login.html',
##         'current_app':'myproject', 'extra_context': {'next':'/loginsuccess'}}),
    url(r'^login/','myproject.views.login_view', name='login_view'),
    url(r'^logout/', 'myproject.views.logout_view'),
                       
    url(r'^editprofile/$', 'profiles.views.editprofile', name='editprofile'),
    url(r'^viewprofile/(?P<publicProfileName>.*)/$', 'profiles.views.viewProfile', name='viewProfile'),                  
    url(r'^loginsuccess', 'myproject.views.loginsuccess', name='loginsuccess'),
    url(r'^register/$', 'myproject.views.register', name='newuserregister'),
                       
##    url('^register/', CreateView.as_view(
##            template_name='register/register.html',
##            form_class=UserCreationForm,
##            success_url='/'
##    )),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^groups/$', 'myproject.views.groupSelect', name='groupSelect'),
    url(r'^search/$', 'myproject.views.searchUsers', name='searchUsers'),
    url(r'^refer/$', 'tracker.views.referral', name='referBusiness'),
    url(r'^refer/(?P<publicProfileName>.*)/$', 'tracker.views.referral', name='referBusiness'),
    url(r'^myreferrals/$','tracker.views.myReferrals'),
    url(r'^myreferrals/receivedhandler/$','tracker.views.receivedHandler'),
    url(r'^myreferrals/senthandler/$','tracker.views.sentHandler'),
                       
    # Serve static content.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),

#### REFERRAL TRACKER APP VIEWS AND URLS                       
##    url(r'^refer/', include('tracker.urls')),
##                       
##                      
## SERVE USER UPLOADED FILES DURING DEVELOPMENT, DEBUG MODE ONLY
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

