# -*- coding: utf-8 -*-
from django import forms
from ..models import tooth_loss
   
class ToothForm(forms.ModelForm):
    
    class Meta:
        model = tooth_loss