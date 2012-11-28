# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from ..models import dental_office, dentist, dates, appointment_type, appointment, patient
from django.forms.widgets import RadioSelect
import datetime

class MyRadioSelect(RadioSelect):
    def render(self, name, value, attrs=None, choices=()):
        html = super(MyRadioSelect, self).render(name, value, attrs, choices)
        html = html.replace('<ul>', '')
        html = html.replace('</ul>', '')
        html = html.replace('<li>', '<br />')
        html = html.replace('</li>', '')
        return mark_safe(html)

class RegisterForm(forms.Form):
	def __init__(self, office, dent, date, apps, typ, sort, *args, **kwargs):
         super(RegisterForm, self).__init__(*args, **kwargs)
         if office!=-1:
            self.fields['office'].initial = office
            if sort == '0':
                dats = dates.objects.values_list('dentist', flat = True).filter(dental_office=office).filter(date__gte=datetime.date.today)
                dents = dentist.objects.filter(id__in=dats).order_by('last_name')
                self.fields['dentist'].queryset = dents
            else:
                dats = dates.objects.values_list('date', flat=True).filter(dental_office=office).filter(date__gte=datetime.date.today).order_by('date').distinct()
                print dats
                self.fields['date'].choices = [(d, d) for d in dats]
                if date != -1:
                    self.fields['date'].initial = date
                    self.fields['dentist'].queryset = dentist.objects.filter(id__in = dates.objects.values_list('dentist', flat=True).filter(dental_office=office).filter(date=date)).order_by('last_name')
            if dent!=-1:
                if sort == '0':
                    dats = dates.objects.filter(dental_office=office).filter(dentist=dent).filter(date__gte=datetime.date.today).order_by('date')
                    self.fields['date'].choices = [(d, d) for d in dats]
                self.fields['dentist'].initial = dent
                if apps!=-1:
                    self.fields['appoint'].choices = [(h, h.strftime('%H:%M')) for h in apps]
                    self.fields['date'].initial = date             
		if typ!=-1:
			self.fields['type'].initial = typ
	
	office = forms.ModelChoiceField(queryset=dental_office.objects.all(),
                                                    widget=forms.Select(),
                                                    required=False,
                                                    label="Gabinet",
                                                    empty_label=None)
	dentist = forms.ModelChoiceField(queryset=dentist.objects.none(), 
									widget=MyRadioSelect, 
									label="Dentyści",
									empty_label=None)
	date = forms.ModelChoiceField(queryset=dates.objects.none(), 
									widget=MyRadioSelect, 
									label="Daty",
									empty_label=None)
	type = forms.ModelChoiceField(queryset=appointment_type.objects.all(),
								widget=forms.Select(),
								label="Typ wizyty",
								empty_label=None)
	appoint = forms.ModelChoiceField(queryset=appointment.objects.none(),
								widget=MyRadioSelect,
								label="Terminy",
								empty_label=None)	
    
class RegisterReceptionistForm(forms.Form):
    
    def __init__(self, office, dent, date, apps, typ, last_name, patient_id, sort, *args, **kwargs):
        super(RegisterReceptionistForm, self).__init__(*args, **kwargs)
        if office!=-1:
            self.fields['office'].initial = office
            if sort == '0':
                dats = dates.objects.values_list('dentist', flat = True).filter(dental_office=office).filter(date__gte=datetime.date.today)
                dents = dentist.objects.filter(id__in=dats).order_by('last_name')
                self.fields['dentist'].queryset = dents
            else:
                dats = dates.objects.values_list('date', flat=True).filter(dental_office=office).filter(date__gte=datetime.date.today).order_by('date').distinct()
                self.fields['date'].choices = [(d, d) for d in dats]
                if date != -1:
                    self.fields['date'].initial = date
                    self.fields['dentist'].queryset = dentist.objects.filter(id__in = dates.objects.values_list('dentist', flat=True).filter(dental_office=office).filter(date=date)).order_by('last_name')
            if dent!=-1:
                if sort == '0':
                    dats = dates.objects.filter(dental_office=office).filter(dentist=dent).filter(date__gte=datetime.date.today).order_by('date')
                    self.fields['date'].choices = [(d, d) for d in dats]
                self.fields['dentist'].initial = dent
                if apps!=-1:
                    self.fields['appoint'].choices = [(h, h.strftime('%H:%M')) for h in apps]
                    self.fields['date'].initial = date 
        if typ!=-1:
            self.fields['type'].initial = typ
        if patient_id != -1:
            self.fields['patients'].initial = patient_id
        pat2 = patient.objects.filter(last_name__startswith=last_name.title()).order_by('last_name')
        self.fields['patients'].queryset = pat2 
        self.fields['pat'].initial = last_name
    
    pat = forms.CharField(label="Nazwisko pacjenta")
    patients = forms.ModelChoiceField(queryset=patient.objects.none(),
                                      widget=MyRadioSelect,
                                      label="Pacjenci",
                                      empty_label=None)
    office = forms.ModelChoiceField(queryset=dental_office.objects.all(),
                                                    widget=forms.Select(),
                                                    label="Gabinet",
                                                    empty_label=None)
    dentist = forms.ModelChoiceField(queryset=dentist.objects.none(), 
                                    widget=MyRadioSelect, 
                                    label="Dentyści",
                                    empty_label=None)
    date = forms.ModelChoiceField(queryset=dates.objects.none(), 
                                    widget=MyRadioSelect, 
                                    label="Daty",
                                    empty_label=None)
    type = forms.ModelChoiceField(queryset=appointment_type.objects.all(),
                                widget=forms.Select(),
                                label="Typ wizyty",
                                empty_label=None)
    appoint = forms.ModelChoiceField(queryset=appointment.objects.none(),
                                widget=MyRadioSelect,
                                label="Terminy",
                                empty_label=None)	
    
class RegisterReceptionistForm2(forms.Form):
    
    def __init__(self, office, dent, date, last_name, patient_id, *args, **kwargs):
        super(RegisterReceptionistForm2, self).__init__(*args, **kwargs)
        if office!=-1:
            self.fields['office'].initial = office
            dats = dates.objects.values_list('dentist', flat = True).filter(dental_office=office).filter(date__gte=datetime.date.today)
            dents = dentist.objects.filter(id__in=dats).order_by('last_name')
            self.fields['dentist'].queryset = dents
            if dent!=-1:
                dats = dates.objects.filter(dental_office=office).filter(dentist=dent).filter(date__gte=datetime.date.today).order_by('date')
                self.fields['date'].choices = [(d, d) for d in dats]
                self.fields['dentist'].initial = dent
        if patient_id != -1:
            self.fields['patients'].initial = patient_id
        pat2 = patient.objects.filter(last_name__startswith=last_name.title()).order_by('last_name')
        self.fields['patients'].queryset = pat2 
        self.fields['pat'].initial = last_name
    
    pat = forms.CharField(label="Nazwisko pacjenta")
    patients = forms.ModelChoiceField(queryset=patient.objects.none(),
                                      widget=MyRadioSelect,
                                      label="Pacjenci",
                                      empty_label=None)
    office = forms.ModelChoiceField(queryset=dental_office.objects.all(),
                                                    widget=forms.Select(),
                                                    label="Gabinet",
                                                    empty_label=None)
    dentist = forms.ModelChoiceField(queryset=dentist.objects.none(), 
                                    widget=MyRadioSelect, 
                                    label="Dentyści",
                                    empty_label=None)
    date = forms.ModelChoiceField(queryset=dates.objects.none(), 
                                    widget=MyRadioSelect, 
                                    label="Daty",
                                    empty_label=None)   
    
class RegisterChangeForm(forms.Form):
    
    def __init__(self, office, dent, date, apps, typ, *args, **kwargs):
        super(RegisterChangeForm, self).__init__(*args, **kwargs)
        dats = dates.objects.filter(dental_office=office).filter(dentist=dent).filter(date__gte=datetime.date.today).order_by('date')
        self.fields['date'].queryset = dats
        if apps!=-1:
            self.fields['appoint'].choices = [(h, h.strftime('%H:%M')) for h in apps]
            self.fields['date'].initial = date 
    
    date = forms.ModelChoiceField(queryset=dates.objects.none(), 
                                    widget=MyRadioSelect, 
                                    label="Daty",
                                    empty_label=None)
    appoint = forms.ModelChoiceField(queryset=appointment.objects.none(),
                                widget=MyRadioSelect,
                                label="Terminy",
                                empty_label=None)