# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
import re

class SetPasswordForm(forms.Form):
    
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'too_short': 'Hasło jest za krótkie. Musi posiadać co najmniej 8 znaków',
        'no_letter': 'Hasło musi zawierać co najmniej jedną literę.',
        'no_number': 'Hasło musi zawierać co namniej jedną cyfrę.'
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['too_short'])
        else:
            if not re.search('[a-zA-Z]+', password1):
                raise forms.ValidationError(self.error_messages['no_letter'])
            else:
                if not re.search('[0-9]+', password1):
                    raise forms.ValidationError(self.error_messages['no_number'])
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user