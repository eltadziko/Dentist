# -*- coding: utf-8 -*-
from django import forms
from ..models import tooth, tooth_part, loss_type
   
class ToothForm(forms.Form):
    
    def __init__(self, t = 1, p = 1, *args, **kwargs):
         super(ToothForm, self).__init__(*args, **kwargs)
         self.fields['tooth'].initial = t
         self.fields['tooth_part'].queryset = tooth.objects.get(id = t).parts.order_by('name')
         self.fields['tooth_part'].initial = p
         self.fields['loss_type'].queryset = tooth_part.objects.get(id = p).losses.order_by('type')

    tooth = forms.ModelChoiceField(queryset=tooth.objects.all(),
                                                    widget=forms.Select(),
                                                    required=True,
                                                    label="Ząb",
                                                    empty_label=None)
    tooth_part = forms.ModelChoiceField(queryset=tooth_part.objects.all(),
                                                    widget=forms.Select(),
                                                    required=True,
                                                    label="Część zęba",
                                                    empty_label=None)
    loss_type = forms.ModelChoiceField(queryset=loss_type.objects.all(),
                                                    widget=forms.Select(),
                                                    required=True,
                                                    label="Rozpoznanie",
                                                    empty_label=None)
    description = forms.CharField(label='Komentarz',
                                  widget=forms.Textarea(attrs={'rows':'4', 'cols':'30'}))