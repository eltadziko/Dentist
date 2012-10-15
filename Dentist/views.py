# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
import datetime
from models import *
from forms import UserForm

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, initial={'date_joined': datetime.date.today, 'last_login': datetime.date.today})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/diseases/')
    else:
        form = UserForm
    return render(request, 'register.html', {'form': form})
    