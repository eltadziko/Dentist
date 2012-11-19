# -*- coding: utf-8 -*-
from django import forms
from ..models import dentist
from django.forms.extras.widgets import SelectDateWidget
   
class DentistForm(forms.ModelForm):
    
    class Meta:
        model = dentist
        exclude = ("description", "user")