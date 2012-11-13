# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.widgets import *
from django.utils.safestring import mark_safe
from ..models import dental_office, dentist, dates, appointment_type, appointment, patient, hours
from django.forms.widgets import RadioSelect
import datetime
import time

class GenerateDatesForm(forms.Form):
    def __init__(self, office, dentista, *args, **kwargs):
        super(GenerateDatesForm, self).__init__(*args, **kwargs)
        if office!=-1:
            self.fields['office'].initial = office
            in_office = hours.objects.values_list('dentist', flat = True).filter(dental_office__id=office)
            dents = dentist.objects.filter(id__in=in_office)
            self.fields['dentist_man'].queryset = dents
            week_days = [u"poniedziałek", "wtorek", u"środa", "czwartek", u"piątek", "sobota", "niedziela"]
            if dentista!=-1:
                self.is_worker = True
                self.fields['dentist_man'].initial = dentista
                self.fields['office'].initial = office
                hh = hours.objects.filter(dentist__id=dentista, dental_office__id=office)
                string = ""
                for h in hh:
                    string += week_days[h.week_day-1] + " pok. " + h.room + ", " + h.begin.strftime('%H:%M') + "-" + h.end.strftime('%H:%M') + "\n"
                if string=="":
                    string = "Brak informacji o terminach przyjęć dla wybranego gabinetu."
                self.fields['information'].initial = string
            if dentista==-1 and dents.count()!=0:
                self.is_worker = True
                self.fields['dentist_man'].initial = dents[0].id
                self.fields['office'].initial = office
                hh = hours.objects.filter(dentist__id=dents[0].id, dental_office__id=office)
                string = ""
                for h in hh:
                    string += week_days[h.week_day-1] + " pok. " + h.room + ", " + h.begin.strftime('%H:%M') + "-" + h.end.strftime('%H:%M') + "\n"
                if string=="":
                    string = "Brak informacji o terminach przyjęć dla wybranego gabinetu."
                self.fields['information'].initial = string
    
    office = forms.ModelChoiceField(queryset=dental_office.objects.all(),
                                                    widget=forms.Select(),
                                                    required=False,
                                                    label="Gabinet",
                                                    empty_label=None)
    dentist_man = forms.ModelChoiceField(queryset=dentist.objects.none(), 
                                                    widget=forms.Select(),
                                                    required=False, 
                                                    label="Dentyści",
                                                    empty_label=None)
    information = forms.CharField(label='Terminy przyjęć',
                                      widget=forms.Textarea(attrs={'readonly':'True'}))
    begin = forms.CharField(label="Od")
    end = forms.CharField(label="Do")
    exclude = forms.CharField(label="Wyłączając")