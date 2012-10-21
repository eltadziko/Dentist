# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
import re

class PasswordForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)
       
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'required': _("This field is required."),
        'bad_password': _("Your old password was entered incorrectly. Please enter it again."),
        'too_short': 'Hasło jest za krótkie. Musi posiadać co najmniej 8 znaków',
        'no_letter': 'Hasło musi zawierać co najmniej jedną literę.',
        'no_number': 'Hasło musi zawierać co namniej jedną cyfrę.',
        'no_change': 'Nowe hasło musi się różnić od starego.',
    }

    old_password = forms.CharField(label=_("Old password"),
        widget=forms.PasswordInput)
    password = forms.CharField(label=_("New password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("New password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    def clean_password(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data.get("password2", "")
        old_password = self.cleaned_data.get("old_password")
        if len(password) < 8:
            raise forms.ValidationError(
                self.error_messages['too_short'])
        else:
            if not re.search('[a-zA-Z]+', password):
                raise forms.ValidationError(self.error_messages['no_letter'])
            else:
                if not re.search('[0-9]+', password):
                    raise forms.ValidationError(self.error_messages['no_number'])
                else:
                    if password != password2:
                        raise forms.ValidationError(self.error_messages['password_mismatch'])
                    else:
                        if password == old_password:
                           raise forms.ValidationError(self.error_messages['no_change']) 
        return password
    
    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['bad_password'])
        return old_password            