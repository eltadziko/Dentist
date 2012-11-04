# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
import datetime
import time
from models import *
from forms.user_form import UserForm
from forms.profile_form import ProfileForm
from forms.patient_form import PatientForm, PatientProfileForm
from forms.diseases_form import DiseasesForm, DiseasesFormReceptionist
from forms.password_form import PasswordForm
from forms.patient_user_form import PatientUserForm
from forms.register_form import *
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

@anonymous_required
def register2(request):
    if request.method == 'POST':
        form = UserForm(request.POST, initial={'date_joined': datetime.date.today, 'last_login': datetime.date.today})
        if form.is_valid(): 
            user = form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            
            password = password_creation(user = user, last_change = datetime.datetime.now().date())
            password.save()
            
            return HttpResponseRedirect('/confirm_register/')
    else:
        form = UserForm
    return render(request, 'register2.html', {'form': form})

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

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
def patient_user(request):
    if request.is_ajax:
        if request.POST:
            form = PatientUserForm(request.POST['pat'], request.POST)
            if form.is_valid():
                if 'patients' in request.POST.keys():
                    pat = patient.objects.get(id = request.POST['patients'])
                    user = User.objects.get(username = request.POST['login'])
                    pat.user = user
                    pat.save()
                    
                    g = Group.objects.get(name='pacjent')
                    g.user_set.add(user)
                    return HttpResponseRedirect('/index/')
        else:
            form = PatientUserForm('')
    return render(request, 'patient_user.html', {'form': form}) 

def index(request):
    return render(request, 'base.html')

def confirm_register(request):
    return render(request, 'confirm_register.html')

@login_required
@user_passes_test(in_patient_group, login_url='/access_denied/')
def dentist_register(request):
    if request.POST:
        if 'type' in request.POST.keys():
            typ = request.POST['type']
        else:
            typ = -1
        if 'dentist' in request.POST.keys():
            if 'date' in request.POST.keys():
                if 'appoint' in request.POST.keys():
                    day = datetime.datetime.strptime(request.POST['appoint'], '%Y-%m-%d %H:%M:%S')
                    appoint = appointment(date = day.date(),
                                          hour = day.time(),
                                          dentist = dentist.objects.get(id=request.POST['dentist']),
                                          dental_office = dental_office.objects.get(id=request.POST['office']),
                                          appointment_type = appointment_type.objects.get(id=request.POST['type']),
                                          patient = patient.objects.get(user=request.user.id))
                    appoint.save()
                    return HttpResponseRedirect('/index/')
                else:
                    apps = []
                    day = dates.objects.get(id=request.POST['date'])
                    dayend = datetime.datetime.combine(day.date, day.end)
                    hour = datetime.datetime.combine(day.date, day.begin)
                    minutes = appointment_type.objects.get(id=typ).length
                    while hour + datetime.timedelta(minutes=minutes)<=dayend:
                        apps.append(hour)
                        hour = hour + datetime.timedelta(minutes=minutes)
                    
                    deleted_apps = []
                    for h in apps:
                        for ap in appointment.objects.filter(date = day).filter(dentist = request.POST['dentist']).filter(dental_office = request.POST['office']):
                            ap_date = datetime.datetime.combine(ap.date, ap.hour)
                            length = ap.appointment_type.length
                            ap_end = datetime.datetime.combine(ap.date, ap.hour) + datetime.timedelta(minutes=length)
                            h_end = h + datetime.timedelta(minutes=appointment_type.objects.get(id=typ).length)
                            if h >= ap_date and h.time() < ap_end.time() or h <= ap_date and h_end > ap_date:
                                if not h in deleted_apps:
                                    deleted_apps.append(h)
                                
                    for h in deleted_apps:            
                        apps.remove(h)
                    form = RegisterForm(request.POST['office'], request.POST['dentist'], request.POST['date'], apps, typ)
            else:
                form = RegisterForm(request.POST['office'], request.POST['dentist'], -1, -1, typ)
        else:
            form = RegisterForm(request.POST['office'], -1, -1, -1, typ)        
    else:
        form = RegisterForm(-1, -1, -1, -1, -1)
    return render(request, 'dentist_register.html', {'form': form})

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
def dentist_register2(request):
    if request.POST:
        if 'type' in request.POST.keys():
            typ = request.POST['type']
        else:
            typ = -1
            
        if 'pat' in request.POST.keys():
            pat = request.POST['pat']
        else:
            pat = ''
          
        if 'patients' in request.POST.keys():
            patients = request.POST['patients']
        else:
            patients = -1
             
        if 'dentist' in request.POST.keys():
            if 'date' in request.POST.keys():
                if 'appoint' in request.POST.keys() and 'patients' in request.POST.keys():
                    day = datetime.datetime.strptime(request.POST['appoint'], '%Y-%m-%d %H:%M:%S')
                    appoint = appointment(date = day.date(),
                                          hour = day.time(),
                                          dentist = dentist.objects.get(id=request.POST['dentist']),
                                          dental_office = dental_office.objects.get(id=request.POST['office']),
                                          appointment_type = appointment_type.objects.get(id=request.POST['type']),
                                          patient = patient.objects.get(id=request.POST['patients']))
                    appoint.save()
                    return HttpResponseRedirect('/index/')
                else:
                    apps = []
                    day = dates.objects.get(id=request.POST['date'])
                    dayend = datetime.datetime.combine(day.date, day.end)
                    hour = datetime.datetime.combine(day.date, day.begin)
                    minutes = appointment_type.objects.get(id=typ).length
                    while hour + datetime.timedelta(minutes=minutes)<=dayend:
                        apps.append(hour)
                        hour = hour + datetime.timedelta(minutes=minutes)
                    
                    deleted_apps = []
                    for h in apps:
                        for ap in appointment.objects.filter(date = day).filter(dentist = request.POST['dentist']).filter(dental_office = request.POST['office']):
                            ap_date = datetime.datetime.combine(ap.date, ap.hour)
                            length = ap.appointment_type.length
                            ap_end = datetime.datetime.combine(ap.date, ap.hour) + datetime.timedelta(minutes=length)
                            h_end = h + datetime.timedelta(minutes=appointment_type.objects.get(id=typ).length)
                            if h >= ap_date and h.time() < ap_end.time() or h <= ap_date and h_end > ap_date:
                                if not h in deleted_apps:
                                    deleted_apps.append(h)
                                
                    for h in deleted_apps:            
                        apps.remove(h)
                    form = RegisterReceptionistForm(request.POST['office'], request.POST['dentist'], request.POST['date'], apps, typ, pat, patients)
            else:
                form = RegisterReceptionistForm(request.POST['office'], request.POST['dentist'], -1, -1, typ, pat, patients)
        else:
            form = RegisterReceptionistForm(request.POST['office'], -1, -1, -1, typ, pat, patients)        
    else:
        form = RegisterReceptionistForm(-1, -1, -1, -1, -1, '', -1)
    return render(request, 'dentist_register2.html', {'form': form})