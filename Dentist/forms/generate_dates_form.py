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
                self.fields['dentist_man'].initial = dentista
                self.fields['office'].initial = office
                hh = hours.objects.filter(dentist__id=dentista, dental_office__id=office)
                string = ""
                for h in hh:
                    string += week_days[h.week_day-1] + " pok. " + h.room + ", " + h.begin.strftime('%H:%M') + "-" + h.end.strftime('%H:%M') + "\n"
                if string=="":
                    string = "Brak informacji o terminach przyjęć dla wybranego gabinetu."
                self.fields['information'].initial = string
                
                dd = dates.objects.filter(dentist__id=dentista, dental_office__id=office)
                string = ""
                for d in dd:
                    string += d.date.strftime("%Y-%m-%d") + " " 
                self.fields['hidden'].initial = string
            elif dentista==-1 and dents.count()!=0:
                self.fields['dentist_man'].initial = dents[0].id
                self.fields['office'].initial = office
                hh = hours.objects.filter(dentist__id=dents[0].id, dental_office__id=office)
                string = ""
                for h in hh:
                    string += week_days[h.week_day-1] + " pok. " + h.room + ", " + h.begin.strftime('%H:%M') + "-" + h.end.strftime('%H:%M') + "\n"
                if string=="":
                    string = "Brak informacji o terminach przyjęć dla wybranego gabinetu."
                self.fields['information'].initial = string
                
                dd = dates.objects.filter(dentist__id=dents[0].id, dental_office__id=office)
                string = ""
                for d in dd:
                    string += d.date.strftime("%Y-%m-%d") + " " 
                self.fields['hidden'].initial = string
    
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
                                      widget=forms.Textarea(attrs={'readonly':'True', 'rows':'5', 'style':'width:280px'}))
    begin = forms.CharField(label="Od",
                            widget=forms.TextInput(attrs={'style':'width:200px'}))
    end = forms.CharField(label="Do",
                            widget=forms.TextInput(attrs={'style':'width:200px'}))
    exclude = forms.CharField(label="Wyłączając", required=False,
                            widget=forms.TextInput(attrs={'style':'width:200px'}))
    hidden = forms.CharField(label='Wpisane daty',
                                    required=False,
                                      widget=forms.Textarea(attrs={'readonly':'True', 'hidden':'hidden'}))
    
class EditAddedDatesForm(forms.Form):
    def __init__(self, last_added, *args, **kwargs):
        super(EditAddedDatesForm, self).__init__(*args, **kwargs)   
        i=1
        for date in last_added:
            self.fields['id_%s' % i] = forms.CharField(label="Id",
                                                       initial=date.id,
                                                       widget=forms.TextInput(attrs={'readonly':'True', 'hidden':'hidden', 'class':'edit_dates_field_id'}))
            self.fields['date_%s' % i] = forms.DateField(label="Data",
                                                         initial=date.date,
                                                         input_formats='%Y-%m-%d',
                                                         widget=forms.DateInput(attrs={'readonly':'True', 'class':'edit_dates_field_date'}))
            self.fields['begin_%s' % i] = forms.TimeField(label="Od",
                                                          initial=date.begin,
                                                          input_formats='%H:%M:%S',
                                                         widget=forms.TextInput(attrs={'class':'edit_dates_field_begin'}))
            self.fields['end_%s' % i] = forms.TimeField(label="Do",
                                                        initial=date.end,
                                                        input_formats='%H:%M:%S',
                                                         widget=forms.TextInput(attrs={'class':'edit_dates_field_end'}))
            self.fields['dentist_%s' % i] = forms.CharField(label="Dentysta",
                                                            initial=date.dentist,
                                                         widget=forms.TextInput(attrs={'readonly':'True', 'class':'edit_dates_field_dentist'}))
            self.fields['dental_office_%s' % i] = forms.CharField(label="Gabinet",
                                                                  initial=date.dental_office,
                                                         widget=forms.TextInput(attrs={'readonly':'True', 'class':'edit_dates_field_dental_office'}))
            self.fields['room_%s' % i] = forms.CharField(label="Pokój",
                                                         initial=date.room,
                                                         widget=forms.TextInput(attrs={'class':'edit_dates_field_room', 'maxlength': '5'}))
            i += 1
        
        self.fields['number_of_fields'] = forms.CharField(label="Liczba dat",
                                                       initial=i-1,
                                                       widget=forms.TextInput(attrs={'readonly':'True', 'hidden':'hidden', 'class':'edit_dates_field_number'}))   
        
class DatesAdditionEditForm(forms.Form):
    def __init__(self, office, dentista, *args, **kwargs):
        super(DatesAdditionEditForm, self).__init__(*args, **kwargs)
        if office!=-1:
            self.fields['office'].initial = office
            in_office = hours.objects.values_list('dentist', flat = True).filter(dental_office__id=office)
            dents = dentist.objects.filter(id__in=in_office)
            self.fields['dentist_man'].queryset = dents
            week_days = [u"poniedziałek", "wtorek", u"środa", "czwartek", u"piątek", "sobota", "niedziela"]
            if dentista!=-1:
                self.fields['dentist_man'].initial = dentista
                self.fields['office'].initial = office
            elif dentista==-1 and dents.count()!=0:
                self.fields['dentist_man'].initial = dents[0].id
                self.fields['office'].initial = office
    
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
    
class EditAddedDates2Form(forms.Form):
    def __init__(self, date, *args, **kwargs):
        super(EditAddedDates2Form, self).__init__(*args, **kwargs) 
        self.fields['id_1'] = forms.CharField(label="Id",
                                                   initial=date.id,
                                                   widget=forms.TextInput(attrs={'readonly':'True', 'hidden':'hidden', 'class':'edit_dates_field_id'}))
        self.fields['date_1'] = forms.DateField(label="Data",
                                                     initial=date.date,
                                                     input_formats='%Y-%m-%d',
                                                     widget=forms.DateInput(attrs={'readonly':'True', 'class':'edit_dates_field_date'}))
        self.fields['begin_1'] = forms.TimeField(label="Od",
                                                      initial=date.begin,
                                                      input_formats='%H:%M:%S',
                                                     widget=forms.TextInput(attrs={'class':'edit_dates_field_begin'}))
        self.fields['end_1'] = forms.TimeField(label="Do",
                                                    initial=date.end,
                                                    input_formats='%H:%M:%S',
                                                     widget=forms.TextInput(attrs={'class':'edit_dates_field_end'}))
        self.fields['dentist_1'] = forms.CharField(label="Dentysta",
                                                        initial=date.dentist,
                                                     widget=forms.TextInput(attrs={'readonly':'True', 'class':'edit_dates_field_dentist'}))
        self.fields['dental_office_1'] = forms.CharField(label="Gabinet",
                                                              initial=date.dental_office,
                                                     widget=forms.TextInput(attrs={'readonly':'True', 'class':'edit_dates_field_dental_office'}))
        self.fields['room_1'] = forms.CharField(label="Pokój",
                                                     initial=date.room,
                                                     widget=forms.TextInput(attrs={'class':'edit_dates_field_room', 'maxlength': '5'}))
        
class GenerateDateForm(forms.Form):
    def __init__(self, office, dentista, *args, **kwargs):
        super(GenerateDateForm, self).__init__(*args, **kwargs)
        if office!=-1:
            self.fields['office'].initial = office
            in_office = hours.objects.values_list('dentist', flat = True).filter(dental_office__id=office)
            dents = dentist.objects.filter(id__in=in_office)
            self.fields['dentist_man'].queryset = dents
            week_days = [u"poniedziałek", "wtorek", u"środa", "czwartek", u"piątek", "sobota", "niedziela"]
            if dentista!=-1:
                self.fields['dentist_man'].initial = dentista
                self.fields['office'].initial = office
                
                dd = dates.objects.filter(dentist__id=dentista, dental_office__id=office)
                string = ""
                for d in dd:
                    string += d.date.strftime("%Y-%m-%d") + " " 
                self.fields['hidden'].initial = string

            elif dentista==-1 and dents.count()!=0:
                self.fields['dentist_man'].initial = dents[0].id
                self.fields['office'].initial = office
                
                dd = dates.objects.filter(dentist__id=dents[0].id, dental_office__id=office)
                string = ""
                for d in dd:
                    string += d.date.strftime("%Y-%m-%d") + " " 
                self.fields['hidden'].initial = string

    
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
    date = forms.CharField(label="Data",
                            widget=forms.TextInput(attrs={'style':'width:150px'}))
    begin = forms.CharField(label="Przyjmuje od [gg:mm]",
                            widget=forms.TextInput(attrs={'style':'width:150px'}))
    end = forms.CharField(label="Przyjmuje do [gg:mm]",
                            widget=forms.TextInput(attrs={'style':'width:150px'}))
    room = forms.CharField(label="Pokój",
                           widget=forms.TextInput(attrs={'maxlength': '5', 'style':'width:100px'}))   
    hidden = forms.CharField(label='Wpisane daty',
                                    required=False,
                                      widget=forms.Textarea(attrs={'readonly':'True', 'hidden':'hidden'}))    