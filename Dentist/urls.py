from django.conf.urls import patterns, include, url
from Dentist import views

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
    url(r'^profile/', views.update_profile),
    url(r'^password/$', views.change_password),
    url(r'^password/', include('django.contrib.auth.urls')),
    url(r'^access_denied/', views.access_denied),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/', views.logout_view),
    
)
