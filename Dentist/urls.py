from django.conf.urls import patterns, include, url
from Dentist import views
from forms.set_password_form import SetPasswordForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # (r'^hello/$', views.hello),
    # Examples:
    # url(r'^$', 'Dentist.views.home', name='home'),
    # url(r'^Dentist/', include('Dentist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', views.register),
    url(r'^register_patient/', views.register_by_receptionist),
    url(r'^diseases/', views.diseases),
    url(r'^profile/$', views.update_profile),
    url(r'^profile/(?P<patient_id>\d+)/$', views.update_profile),
    url(r'^password/$', views.change_password),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', 
        {'set_password_form' : SetPasswordForm}),
    url(r'^password/', include('django.contrib.auth.urls')),
    url(r'^access_denied/', views.access_denied),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/', views.logout_view),
    url(r'^patients/', views.patient_list),
    
)
