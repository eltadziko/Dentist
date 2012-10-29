# -*- coding: utf-8 -*-
from django import forms
from ..models import patient, dentist
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
        pat2 = patient.objects.filter(last_name=last_name).filter(user=None)
        self.fields['patients'].queryset = pat2 
        
    error_messages = {
        'required': _("This field is required."),
        'not_exist': "Użytkownik o takim loginie nie istnieje.",
        'taken': "To konto ma już przypisanego pacjenta lub lekarza",
    }

    pat = forms.CharField(label="Nazwisko pacjenta")
    login = forms.CharField(label="Login pacjenta")
    patients = forms.ModelChoiceField(queryset=patient.objects.all(), widget=MyRadioSelect, initial=1, label="Pacjenci")
    
    def clean_login(self):
        login = self.cleaned_data.get("login")
        if login == "":
            raise forms.ValidationError(self.error_messages['required'])
        if User.objects.filter(username = login).count() == 0:
            raise forms.ValidationError(self.error_messages['not_exist'])
        else:
            id = User.objects.get(username = login)
            if patient.objects.filter(user = id).count() > 0 or dentist.objects.filter(user = id).count() > 0:
                raise forms.ValidationError(self.error_messages['taken'])
        return login  
    