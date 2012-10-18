# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'required': _("This field is required."),
        'too_short': 'Hasło jest za krótkie. Musi posiadać co najmniej 8 znaków'
    }

    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data.get("password2", "")
        if len(password) < 8:
            raise forms.ValidationError(
                self.error_messages['too_short'])
        else:
            if password != password2:
                raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password
    
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