# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
import datetime
from models import *
from forms.user_form import UserForm
from forms.profile_form import ProfileForm
from forms.patient_form import PatientForm, PatientProfileForm
from forms.diseases_form import DiseasesForm, DiseasesFormReceptionist
from forms.password_form import PasswordForm
from django.contrib.auth.decorators import login_required, user_passes_test
from decorators import *

def access_denied(request):
    return render(request, 'access_denied.html')

@anonymous_required
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
            patient.save()
            
            password = password_creation(user = user, last_change = datetime.datetime.now().date())
            password.save()
            
            #automatyczne logowanie użytkownika
            user2 = authenticate(username = user.username, password = request.POST['password'])
            login(request, user2)
            
            return HttpResponseRedirect('/diseases/')
    else:
        form = UserForm
        form_patient = PatientForm
    return render(request, 'register.html', {'form': form, 'form_patient': form_patient})

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
def register_by_receptionist(request):
    if request.method == 'POST':
        form_patient = PatientForm(request.POST)
        form_diseases = DiseasesFormReceptionist(request.POST)
        if form_patient.is_valid():             
            patient = form_patient.save()
            for disease2 in request.POST.getlist('diseases'):
                dis = disease.objects.get(id=disease2)
                pat_dis = patient_diseases(patient=patient.id, disease=dis, date=datetime.datetime.now().date())
                pat_dis.save()
            return HttpResponseRedirect('/index/')
    else:
        form_patient = PatientForm
        form_diseases = DiseasesFormReceptionist
    return render(request, 'register_patient.html', {'form_patient': form_patient, 'form_diseases': form_diseases})

@login_required
@user_passes_test(in_patient_group, login_url='/access_denied/')
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

@login_required
@user_passes_test(in_group, login_url='/access_denied/')
def update_profile(request, patient_id = -1):
    if request.user.groups.filter(name='pacjent').count() == 1:
        user = User.objects.get(id = request.user.id)
        pat = patient.objects.get(user = user.id)
    else:
        if patient_id == -1:
            return HttpResponseRedirect('/access_denied/')
        pat = patient.objects.get(id = patient_id)
        user = User.objects.get(id = pat.user_id)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = user)
        form_patient = PatientProfileForm(request.POST, instance = pat)
        if form.is_valid() and form_patient.is_valid(): 
            form.save()            
            form_patient.save()
            return HttpResponseRedirect('/index/')
    else:
        form = ProfileForm(instance = user)
        form_patient = PatientProfileForm(instance = pat)
    return render(request, 'profile.html', {'form': form, 'form_patient': form_patient})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(request.POST['password'])
            request.user.save()
            
            password = password_creation(user = request.user, last_change = datetime.datetime.now().date())
            password.save()
            return HttpResponseRedirect('/index/')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})
        
@login_required
def logout_view(request):
    logout(request) 
    return HttpResponseRedirect('/index/')  

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
def patient_list(request):
    patients = patient.objects.all()
    return render(request, 'patients.html', {'patients': patients}) 