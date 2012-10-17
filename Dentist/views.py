# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate
import datetime
from models import *
from forms.user_form import UserForm
from forms.patient_form import PatientForm
from forms.diseases_form import DiseasesForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, initial={'date_joined': datetime.date.today, 'last_login': datetime.date.today})
        form_patient = PatientForm(request.POST)
        if form.is_valid() and form_patient.is_valid(): 
            user = form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            
            #dodanie uprawnienia pacjenta
            g = Group.objects.get(name='pacjent')
            g.user_set.add(user)
            
            patient = form_patient.save(commit=False)
            patient.user = user
            patient.save();
            
            #automatyczne logowanie użytkownika
            user2 = authenticate(username = user.username, password = request.POST['password'])
            login(request, user2)
            
            return HttpResponseRedirect('/diseases/')
    else:
        form = UserForm
        form_patient = PatientForm
    return render(request, 'register.html', {'form': form, 'form_patient': form_patient})

@login_required
def diseases(request):
    if request.POST:
        form = DiseasesForm(request.user, request.POST)
        if form.is_valid():
            pat = patient.objects.get(user=request.user.id)
            patient_diseases.objects.filter(patient_id=pat.id).delete()
            for disease2 in request.POST.getlist('diseases'):
                dis = disease.objects.get(id=disease2)
                pat_dis = patient_diseases(patient=pat,disease=dis, date=datetime.datetime.now().date())
                pat_dis.save()
            return HttpResponseRedirect('/index/')
    else:
        form = DiseasesForm(request.user)
    return render(request, 'diseases.html', {'form': form})
    