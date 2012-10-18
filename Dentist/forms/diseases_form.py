# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from ..models import disease, patient_diseases, patient

class MyCheckboxSelectMultiple(CheckboxSelectMultiple):
	def render(self, name, value, attrs=None, choices=()):
		html = super(MyCheckboxSelectMultiple, self).render(name, value, attrs, choices)
		html = html.replace('<ul>', '')
		html = html.replace('</ul>', '')
		html = html.replace('<li>', '')
		html = html.replace('</li>', '<br />')
		html = html.replace('Choroba: ', '')
		return mark_safe(html)

class DiseasesForm(forms.Form):
	
	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(DiseasesForm, self).__init__(*args, **kwargs)
		pat = patient.objects.get(user=user.id)
		self.fields['diseases'].initial = patient_diseases.objects.values_list('disease_id', flat=True).filter(patient=pat.id)
	
	diseases = forms.ModelMultipleChoiceField(queryset=disease.objects.all(),
                                                    widget=MyCheckboxSelectMultiple(),
                                                    required=False)			