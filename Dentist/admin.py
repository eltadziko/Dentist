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
    
    list_display = ('user_first_name', 'user_last_name', 'title', 'description', 'phone', 'show_user_url')   
    list_display_links = ('user_first_name', 'user_last_name', 'title')
    

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
    
    list_display = ('user_first_name', 'user_last_name', 'PESEL', 'birth_date', 'address',
                     'insurance_number', 'phone', 'comment', 'show_user_url')
    list_display_links = ('user_first_name', 'user_last_name', 'PESEL',)
   
    
# admin.site.register(User, UsAdmin)
admin.site.register(dentist, DentistAdmin)
admin.site.register(patient, PatientAdmin)