# -*- coding: utf-8 -*-
from django import forms
from ..models import patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = patient
        exclude = ("diseases", "user", "comment")