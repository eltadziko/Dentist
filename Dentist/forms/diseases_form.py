# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from ..models import disease

class MyCheckboxSelectMultiple(CheckboxSelectMultiple):
	def render(self, name, value, attrs=None, choices=()):
		html = super(MyCheckboxSelectMultiple, self).render(name, value, attrs, choices)
		html = html.replace('<ul>', '')
		html = html.replace('</ul>', '')
		html = html.replace('<li>', '')
		html = html.replace('</li>', '<br />')
		return mark_safe(html)

class DiseasesForm(forms.Form):
	diseases = disease.objects.all()
	diseases2 = forms.MultipleChoiceField(required=False,
        widget=MyCheckboxSelectMultiple, 
        choices=[(disease.id, disease.disease_name) for disease in diseases])
	

