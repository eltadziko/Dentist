# -*- coding: utf-8 -*-
from django import forms
from ..models import patient
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

class MyRadioSelect(RadioSelect):
    def render(self, name, value, attrs=None, choices=()):
        html = super(MyRadioSelect, self).render(name, value, attrs, choices)
        html = html.replace('<ul>', '')
        html = html.replace('</ul>', '')
        html = html.replace('<li>', '<br />')
        html = html.replace('</li>', '')
        return mark_safe(html)
    
class PatientUserForm(forms.Form):
    
    def __init__(self, last_name, *args, **kwargs):
        super(PatientUserForm, self).__init__(*args, **kwargs)
        pat2 = patient.objects.filter(last_name=last_name)
        self.fields['patients'].queryset = pat2 

    pat = forms.CharField(label="Nazwisko pacjenta")
    login = forms.CharField(label="Login pacjenta")
    patients = forms.ModelChoiceField(queryset=patient.objects.all(), widget=MyRadioSelect, initial=1, label="Pacjenci") 
    
    