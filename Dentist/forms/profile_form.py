# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class ProfileForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'required': _("This field is required."),
    }

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name == "":
            raise forms.ValidationError(self.error_messages['required'])
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name == "":
            raise forms.ValidationError(self.error_messages['required'])
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError(self.error_messages['required'])
        return email