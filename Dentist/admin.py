# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# class UserInline(admin.TabularInline):
    # model = User 

class DentistAdmin(admin.ModelAdmin):
    def user_first_name(self, instance):
        return instance.user.first_name
    user_first_name.short_description = u"Imię"
    
    def user_last_name(self, instance):
        return instance.user.last_name
    user_last_name.short_description = u"Nazwisko"
    
    def show_user_url(self, obj):
        return '<a href="../../auth/user/%s">%s</a>' % (obj.user.id, obj.user)
    show_user_url.allow_tags = True
    show_user_url.short_description = u"Użytkownik"
    
    list_display = ('first_name', 'last_name', 'title', 'description', 'phone', 'show_user_url')   
    list_display_links = ('first_name', 'last_name', 'title')
    

class PatientAdmin(admin.ModelAdmin):
    def user_first_name(self, instance):
        return instance.user.first_name
    user_first_name.short_description = u"Imię"
    
    def user_last_name(self, instance):
        return instance.user.last_name
    user_last_name.short_description = u"Nazwisko"
    
    def show_user_url(self, obj):
        return '<a href="../../auth/user/%s">%s</a>' % (obj.user.id, obj.user)
    show_user_url.allow_tags = True
    show_user_url.short_description = u"Użytkownik"
    
    list_display = ('first_name', 'last_name', 'PESEL', 'birth_date', 'address',
                     'insurance_number', 'phone', 'comment', 'show_user_url')
    list_display_links = ('first_name', 'last_name', 'PESEL',)
   
class DiseaseAdmin(admin.ModelAdmin):
    def show_disease_name(self, obj):
        return '%s' % (obj.disease_name)
    
    list_display = ('show_disease_name',)
    
class DentalOfficeAdmin(admin.ModelAdmin):
    list_display = ('address', 'name','phone', 'email', 'description')
     
class HoursAdmin(admin.ModelAdmin):    
    list_display = ('week_day', 'begin', 'end', 'dentist', 'dental_office', 'room')
    #list_display_links = ('week_day', 'dentist', 'dental_office',)

class AppointmentTypeAdmin(admin.ModelAdmin):    
    list_display = ('type', 'length')
    
class DatesAdmin(admin.ModelAdmin):    
    list_display = ('date', 'begin', 'end', 'dentist', 'dental_office', 'room')
    #list_display_links = ('date', 'dentist', 'dental_office',)

class AppointmentAdmin(admin.ModelAdmin):    
    list_display = ('date', 'hour', 'description', 'dentist', 'patient', 'dental_office', 'appointment_type')
    #list_display_links = ('date', 'dentist', 'patient', 'dental_office', 'appointment_type')
       
class ToothLossAdmin(admin.ModelAdmin):    
    list_display = ('appointment', 'tooth', 'loss_type', 'tooth_part', 'comment')       

# admin.site.register(User, UsAdmin)
admin.site.register(dentist, DentistAdmin)
admin.site.register(patient, PatientAdmin)
admin.site.register(disease, DiseaseAdmin)
admin.site.register(dental_office, DentalOfficeAdmin)
admin.site.register(hours, HoursAdmin)
admin.site.register(appointment_type, AppointmentTypeAdmin)
admin.site.register(dates, DatesAdmin)
admin.site.register(appointment, AppointmentAdmin)
admin.site.register(tooth_loss, ToothLossAdmin)