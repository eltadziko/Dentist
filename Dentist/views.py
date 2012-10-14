# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import render
from django import forms
from models import User

class UserForm(forms.ModelForm):
    password2 = forms.CharField(max_length=128)
    
    class Meta:
        model = User
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError(password2)
        return cleaned_data

def register(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            print 'a'
    else:
        form = UserForm
    return render(request, 'register.html', {'form': form})
    