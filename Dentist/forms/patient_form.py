# -*- coding: utf-8 -*-
from django import forms
from ..models import patient
from django.forms.extras.widgets import SelectDateWidget

class PatientForm(forms.ModelForm):
    
    years = []
    for i in range(1920, 2010):
        years.append(i)
    
    birth_date = forms.DateField(widget=SelectDateWidget(years=years), label="Data ur.")
    
    class Meta:
        model = patient
        exclude = ("diseases", "user", "comment")
        
class PatientProfileForm(forms.ModelForm):
    
    years = []
    for i in range(1920, 2010):
        years.append(i)

    birth_date = forms.DateField(widget=SelectDateWidget(years=years), label="Data ur.")
    class Meta:
        model = patient
        exclude = ("diseases", "user")