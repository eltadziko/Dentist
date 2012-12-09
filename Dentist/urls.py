from django.conf.urls import patterns, include, url
from Dentist import views
from forms.set_password_form import SetPasswordForm
from django.views.static import *
from django.conf import settings

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
    url(r'^$', views.index),
    url(r'^index', views.index),
    url(r'^register/', views.register),
    url(r'^register2/', views.register2),
    url(r'^dentist_register/', views.dentist_register),
    url(r'^dentist_register2/', views.dentist_register2),
    url(r'^dentist_register3/', views.dentist_register3),
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
    url(r'^patient_user/', views.patient_user),
    url(r'^appointment_list/$', views.appointment_list),
    url(r'^appointment_list2/$', views.appointment_list2),
    url(r'^day_graphic/$', views.day_graphic),
    url(r'^offices/$', views.offices),
    url(r'^dentists/$', views.dentists),
    url(r'^reservations/$', views.reservations),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^dates_addition/', views.dates_addition),
    url(r'^date_addition/', views.date_addition),
    url(r'^dates_addition_edit/', views.dates_addition_edit),
    url(r'^patient_card/', views.patient_card),
    url(r'^patient_card_dentist/', views.patient_card_dentist),
    url(r'^dentist_profile/', views.dentist_profile),
    url(r'^send_reminders/', views.send_reminders),
    
)
