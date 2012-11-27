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
from forms.generate_dates_form import GenerateDatesForm, EditAddedDatesForm
from forms.register_form import *
from forms.dentist_form import *
from forms.tooth_edit_form import *
from django.contrib.auth.decorators import login_required, user_passes_test
from decorators import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ValidationError

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
            
            messages.add_message(request, messages.INFO, 'Pomyślnie się zarejestrowałeś. Zaznacz teraz choroby, na które chorujesz.')
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
            
            messages.add_message(request, messages.INFO, 'Poprawnie założyłeś konto. Skontaktuj się z recepcjonistą w dowolnym gabinecie, aby powiązać założone konto ze swoją kartą pacjenta.')
            return HttpResponseRedirect('/index/')
    else:
        form = UserForm
    return render(request, 'register2.html', {'form': form})

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
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
            messages.add_message(request, messages.INFO, 'Pomyślnie zarejestrowano pacjenta.')
            return HttpResponseRedirect('/index/')
    else:
        form_patient = PatientForm
        form_diseases = DiseasesFormReceptionist
    return render(request, 'register_patient.html', {'form_patient': form_patient, 'form_diseases': form_diseases})

@login_required
@user_passes_test(in_patient_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
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
            messages.add_message(request, messages.INFO, 'Pomyślnie dodano choroby.')
            return HttpResponseRedirect('/index/')
    else:
        form = DiseasesForm(request.user)
    return render(request, 'diseases.html', {'form': form})

@login_required
@user_passes_test(in_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def update_profile(request, patient_id = -1):
    if request.user.groups.filter(name='pacjent').count() == 1:
        user = User.objects.get(id = request.user.id)
        pat = patient.objects.get(user = user.id)
        url = ''
    else:
        if patient_id == -1:
            return HttpResponseRedirect('/access_denied/')
        pat = patient.objects.get(id = patient_id)
        user = User.objects.get(id = pat.user_id)
        url = str(pat.id)+'/'
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = user)
        form_patient = PatientProfileForm(request.POST, instance = pat)
        if form.is_valid() and form_patient.is_valid(): 
            form.save()            
            form_patient.save()
            messages.add_message(request, messages.INFO, 'Pomyślnie zaktualizowano profil.')
            return HttpResponseRedirect('/index/')
    else:
        form = ProfileForm(instance = user)
        form_patient = PatientProfileForm(instance = pat)
    return render(request, 'profile.html', {'form': form, 'form_patient': form_patient, 'patient': url})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(request.POST['password'])
            request.user.save()
            
            password = password_creation.objects.get(user = request.user)
            password.last_change = datetime.datetime.now().date()
            password.save()
            
            messages.add_message(request, messages.INFO, 'Pomyślnie zmieniono hasło.')
            return HttpResponseRedirect('/index/')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})
        
@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Nastąpiło pomyślne wylogowanie.')
    return HttpResponseRedirect('/index/')  

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def patient_list(request):
    if request.POST:
        patients = patient.objects.filter(last_name__startswith=request.POST['pat'].title()).order_by('first_name')
    else:
        patients = patient.objects.all().order_by('last_name')
    paginator = Paginator(patients, 25)
    page = request.GET.get('page')
    try:
        patients2 = paginator.page(page)
    except PageNotAnInteger:
        patients2 = paginator.page(1)
    except EmptyPage:
        patients2 = paginator.page(1)
    return render(request, 'patients.html', {'patients': patients2}) 

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
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
                    messages.add_message(request, messages.INFO, 'Pomyślnie przypisano konto do pacjenta.')
                    return HttpResponseRedirect('/index/')
        else:
            form = PatientUserForm('')
    return render(request, 'patient_user.html', {'form': form}) 

@user_passes_test(new_password, login_url="/password/")
def index(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(in_patient_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def dentist_register(request):
    
    if 'sort' in request.POST.keys():
        request.session['sort2'] = request.POST['sort']
    if not 'sort2' in request.session:
        request.session['sort2'] = '0'

    offices = dental_office.objects.all()
    if appointment.objects.filter(date__gte = datetime.datetime.now().date()).filter(patient = patient.objects.get(user = request.user)).count() >= 3:
        form = RegisterForm(offices[0].id, -1, -1, -1, -1, request.session['sort2'])
        return render(request, 'dentist_register.html', {'form': form, 'too_much': True})
    if request.POST:  
        if 'type' in request.POST.keys():
            typ = int(request.POST['type'])
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
                    messages.add_message(request, messages.INFO, 'Pomyślnie zarejestrowano do dentysty.')
                    return HttpResponseRedirect('/reservations/')
                else:
                    apps = []
                    day = dates.objects.filter(dentist = request.POST['dentist']).get(date=request.POST['date'])
                    daybegin = datetime.datetime.combine(day.date, day.begin)
                    dayend = datetime.datetime.combine(day.date, day.end)
                    if day.date == datetime.datetime.now().date() and daybegin < datetime.datetime.now():
                        hour = datetime.datetime.now()
                        minute = hour.time().minute
                        h = datetime.datetime.combine(day.date, hour.time())
                        typ2 = appointment_type.objects.get(id = typ).length
                        if minute < 15:
                            h = h + datetime.timedelta(minutes=(15 - minute))
                        elif minute < 30:
                            h = h + datetime.timedelta(minutes=(30 - minute))
                        elif minute < 45:
                            h = h + datetime.timedelta(minutes=(45 - minute))
                        else:
                            h = h + datetime.timedelta(minutes=(60 - minute))
                        h = h - datetime.timedelta(seconds = hour.time().second, microseconds = hour.time().microsecond)
                        hour = h
                    else:
                        hour = datetime.datetime.combine(day.date, day.begin)
                    minutes = 15
                    minutes2 = appointment_type.objects.get(id=typ).length
                    while hour + datetime.timedelta(minutes=minutes2)<=dayend:
                        apps.append(hour)
                        hour = hour + datetime.timedelta(minutes=minutes)
                    
                    deleted_apps = []
                    for h in apps:
                        for ap in appointment.objects.filter(date = day).filter(dentist = request.POST['dentist']).filter(dental_office = request.POST['office']).filter(untimely=False):
                            ap_date = datetime.datetime.combine(ap.date, ap.hour)
                            length = ap.appointment_type.length
                            ap_end = datetime.datetime.combine(ap.date, ap.hour) + datetime.timedelta(minutes=length)
                            h_end = h + datetime.timedelta(minutes=appointment_type.objects.get(id=typ).length)
                            if h >= ap_date and h.time() < ap_end.time() or h <= ap_date and h_end > ap_date:
                                if not h in deleted_apps:
                                    deleted_apps.append(h)
                                
                    for h in deleted_apps:            
                        apps.remove(h)
                    if request.GET.get('type', None) == 'ajax': 
                        form = RegisterForm(request.POST['office'], request.POST['dentist'], request.POST['date'], apps, typ, request.session['sort2'])
                    else:
                        form = RegisterForm(request.POST['office'], request.POST['dentist'], request.POST['date'], apps, typ, request.session['sort2'], request.POST)
            else:
                
                if request.GET.get('type', None) == 'ajax': 
                    form = RegisterForm(request.POST['office'], request.POST['dentist'], -1, -1, typ, request.session['sort2'])
                else:
                    form = RegisterForm(request.POST['office'], request.POST['dentist'], -1, -1, typ, request.session['sort2'], request.POST)
        else:
            if 'date' in request.POST.keys():
                if request.GET.get('type', None) == 'ajax': 
                    form = RegisterForm(request.POST['office'], -1, request.POST['date'], -1, typ, request.session['sort2'])
                else:
                    form = RegisterForm(request.POST['office'], -1, request.POST['date'], -1, typ, request.session['sort2'], request.POST)
            else:
                if request.GET.get('type', None) == 'ajax': 
                    form = RegisterForm(request.POST['office'], -1, -1, -1, typ, request.session['sort2'])   
                else:
                    form = RegisterForm(request.POST['office'], -1, -1, -1, typ, request.session['sort2'], request.POST)           
    else:
        form = RegisterForm(offices[0].id, -1, -1, -1, -1, request.session['sort2'])
    return render(request, 'dentist_register.html', {'form': form})

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def dentist_register2(request):
    
    if 'sort' in request.POST.keys():
        request.session['sort2'] = request.POST['sort']
    if not 'sort2' in request.session:
        request.session['sort2'] = '0'
          
    if request.POST:
        if 'type' in request.POST.keys():
            typ = int(request.POST['type'])
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
                    messages.add_message(request, messages.INFO, 'Pomyślnie zarejestrowano pacjenta do dentysty.')
                    return HttpResponseRedirect('/index/')
                else:
                    apps = []
                    day = dates.objects.filter(dentist = request.POST['dentist']).get(date=request.POST['date'])
                    daybegin = datetime.datetime.combine(day.date, day.begin)
                    dayend = datetime.datetime.combine(day.date, day.end)
                    if day.date == datetime.datetime.now().date() and daybegin < datetime.datetime.now():
                        hour = datetime.datetime.now()
                        minute = hour.time().minute
                        h = datetime.datetime.combine(day.date, hour.time())
                        typ2 = appointment_type.objects.get(id = typ).length
                        if minute < 15:
                            h = h + datetime.timedelta(minutes=(15 - minute))
                        elif minute < 30:
                            h = h + datetime.timedelta(minutes=(30 - minute))
                        elif minute < 45:
                            h = h + datetime.timedelta(minutes=(45 - minute))
                        else:
                            h = h + datetime.timedelta(minutes=(60 - minute))
                        h = h - datetime.timedelta(seconds = hour.time().second, microseconds = hour.time().microsecond)
                        hour = h
                    else:
                        hour = datetime.datetime.combine(day.date, day.begin)
                    minutes = 15
                    minutes2 = appointment_type.objects.get(id=typ).length
                    while hour + datetime.timedelta(minutes=minutes2)<=dayend:
                        apps.append(hour)
                        hour = hour + datetime.timedelta(minutes=minutes)

                    deleted_apps = []
                    for h in apps:
                        for ap in appointment.objects.filter(date = day).filter(dentist = request.POST['dentist']).filter(dental_office = request.POST['office']).filter(untimely=False):
                            ap_date = datetime.datetime.combine(ap.date, ap.hour)
                            length = ap.appointment_type.length
                            ap_end = datetime.datetime.combine(ap.date, ap.hour) + datetime.timedelta(minutes=length)
                            h_end = h + datetime.timedelta(minutes=appointment_type.objects.get(id=typ).length)
                            if h >= ap_date and h.time() < ap_end.time() or h <= ap_date and h_end > ap_date:
                                if not h in deleted_apps:
                                    deleted_apps.append(h)
           
                    for h in deleted_apps:            
                        apps.remove(h)
                    if request.GET.get('type', None) == 'ajax':  
                        form = RegisterReceptionistForm(request.POST['office'], request.POST['dentist'], request.POST['date'], apps, typ, pat, patients, request.session['sort2'])
                    else:
                        form = RegisterReceptionistForm(request.POST['office'], request.POST['dentist'], request.POST['date'], apps, typ, pat, patients, request.session['sort2'], request.POST)
            else:
                if request.GET.get('type', None) == 'ajax':  
                    form = RegisterReceptionistForm(request.POST['office'], request.POST['dentist'], -1, -1, typ, pat, patients, request.session['sort2'])
                else:
                    form = RegisterReceptionistForm(request.POST['office'], request.POST['dentist'], -1, -1, typ, pat, patients, request.session['sort2'], request.POST)
        else:
            if 'date' in request.POST.keys():
                if request.GET.get('type', None) == 'ajax':  
                    form = RegisterReceptionistForm(request.POST['office'], -1, request.POST['date'], -1, typ, pat, patients, request.session['sort2'])
                else:
                    form = RegisterReceptionistForm(request.POST['office'], -1, request.POST['date'], -1, typ, pat, patients, request.session['sort2'], request.POST)
            else:
                if request.GET.get('type', None) == 'ajax':  
                    form = RegisterReceptionistForm(request.POST['office'], -1, -1, -1, typ, pat, patients, request.session['sort2'])
                else:
                    form = RegisterReceptionistForm(request.POST['office'], -1, -1, -1, typ, pat, patients, request.session['sort2'], request.POST)         
    else:
        offices = dental_office.objects.all()
        form = RegisterReceptionistForm(offices[0].id, -1, -1, -1, -1, '', -1, request.session['sort2'])
    
    return render(request, 'dentist_register2.html', {'form': form})

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def dentist_register3(request):
       
    if request.POST:
            
        if 'pat' in request.POST.keys():
            pat = request.POST['pat']
        else:
            pat = ''
          
        if 'patients' in request.POST.keys():
            patients = request.POST['patients']
        else:
            patients = -1
             
        if 'dentist' in request.POST.keys():
            if 'date' in request.POST.keys() and 'patients' in request.POST.keys():
                day = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d')
                appoint = appointment(date = day.date(),
                                      dentist = dentist.objects.get(id=request.POST['dentist']),
                                      dental_office = dental_office.objects.get(id=request.POST['office']),
                                      patient = patient.objects.get(id=request.POST['patients']),
                                      untimely = True)
                appoint.save()
                messages.add_message(request, messages.INFO, 'Pomyślnie zarejestrowano pacjenta do dentysty.')
                return HttpResponseRedirect('/index/')
            else:
                if request.GET.get('type', None) == 'ajax':  
                    form = RegisterReceptionistForm2(request.POST['office'], request.POST['dentist'], -1, pat, patients)
                else:
                    form = RegisterReceptionistForm2(request.POST['office'], request.POST['dentist'], -1, pat, patients, request.POST)
        else:
            if request.GET.get('type', None) == 'ajax':  
                form = RegisterReceptionistForm2(request.POST['office'], -1, -1, pat, patients)
            else:
                form = RegisterReceptionistForm2(request.POST['office'], -1, -1, pat, patients, request.POST)         
    else:
        offices = dental_office.objects.all()
        form = RegisterReceptionistForm2(offices[0].id, -1, -1, '', -1)
    
    return render(request, 'dentist_register3.html', {'form': form})

@login_required
@user_passes_test(in_dentist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def appointment_list(request):
    if request.POST:
        if 'appoint' in request.POST.keys():
            request.session['appoint'] = request.POST['appoint']
            return HttpResponseRedirect('/patient_card_dentist/')
        if request.POST['date']!='0':
            date = request.POST['date']
            request.session['date'] = date
        else:
            date = datetime.datetime.today().date()
            date = date.strftime("%Y-%m-%d")
            request.session['date'] = date
        
    else:
        if 'date' in request.session:
            date = request.session['date']
        else:
            date = datetime.datetime.today().date()
            date = date.strftime("%Y-%m-%d")
            request.session['date'] = date
        if 'graphic' in request.session and request.session['graphic'] != '/appointment_list/':
            return HttpResponseRedirect(request.session['graphic'])
    
    request.session['graphic'] = '/appointment_list/'
    dent = dentist.objects.get(user = request.user.id)
    appoints = appointment.objects.filter(date = date).filter(dentist = dent).filter(untimely=False).order_by('hour')
    ends = []
    nows = []
    time = datetime.datetime.now()
    for a in appoints:
        ends.append((datetime.datetime.combine(a.date, a.hour) + datetime.timedelta(minutes=a.appointment_type.length)).time())
        nows.append(time>=datetime.datetime.combine(a.date, a.hour) and time<datetime.datetime.combine(a.date, ends[-1]))
    app = [{'appoint': t[0], 'end': t[1], 'now_time': t[2]} for t in zip(appoints, ends, nows)]
    
    appoints_untimely = appointment.objects.filter(date = date).filter(dentist = dent).filter(untimely=True).order_by('patient')
    
    return render(request, 'appointment_list.html', {'appoints': app, 'date': date, 'appoints_untimely': appoints_untimely})

@login_required
@user_passes_test(in_dentist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def appointment_list2(request):
    if request.POST:
        if 'appoint' in request.POST.keys():
            request.session['appoint'] = request.POST['appoint']
            return HttpResponseRedirect('/patient_card_dentist/')
        if request.POST['date']!='0':
            date = request.POST['date']
            request.session['date'] = date
        else:
            date = datetime.datetime.today().date()
            date = date.strftime("%Y-%m-%d")
            request.session['date'] = date
        
    else:
        if 'date' in request.session:
            date = request.session['date']
        else:
            date = datetime.datetime.today().date()
            date = date.strftime("%Y-%m-%d")
            request.session['date'] = date
        if 'graphic' in request.session and request.session['graphic'] != '/appointment_list2/':
            return HttpResponseRedirect(request.session['graphic'])
    
    request.session['graphic'] = '/appointment_list2/'
    dent = dentist.objects.get(user = request.user.id)
    appoints = appointment.objects.filter(date = date).filter(dentist = dent).filter(untimely=False).order_by('hour')
    hours = []
    hour = dates.objects.filter(date=date).filter(dentist = dent) 

    if appoints.count()!=0 and hour.count()!=0:
        begin = datetime.datetime.combine(appoints[0].date, hour[0].begin)
        end = datetime.datetime.combine(appoints[0].date, hour[0].end)

        while begin<end:
            hours.append(begin.time())
            begin = begin + datetime.timedelta(minutes=15)
    appoints = list(appoints)
    app = []
    
    i = 0
    for h in hours:
        dodano = False
        time = datetime.datetime.now()
        time_end = datetime.datetime.combine(appoints[0].date, h) + datetime.timedelta(minutes=15)
        now = (time<time_end and time>datetime.datetime.combine(appoints[0].date, h))
        for a in appoints:
            if h == a.hour:
                app.append({'appoint':a, 'hour':h, 'length':a.appointment_type.length/15, 'now_time': now})
                dodano = True
                i = a.appointment_type.length/15
        if not dodano:
            i = i-1
            app.append({'appoint':None, 'hour':h, 'length':i, 'now_time': now})
    
    appoints_untimely = appointment.objects.filter(date = date).filter(dentist = dent).filter(untimely=True).order_by('patient')
            
    return render(request, 'appointment_list2.html', {'appoints': app, 'date': date, 'hours': hours, 'appoints_untimely': appoints_untimely})

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def day_graphic(request):
    offices = dental_office.objects.all()
    
    if request.POST:
        if request.POST['date']!='0':
            date = request.POST['date']
            request.session['graphic_date'] = date
        else:
            date = datetime.datetime.today().date()
            date = date.strftime("%Y-%m-%d")
            request.session['graphic_date'] = date
        office = int(request.POST['office'])
    else:
        if 'graphic_date' in request.session:
            date = request.session['graphic_date']
            office = request.session['graphic_office']
        else:
            date = datetime.datetime.today().date()
            date = date.strftime("%Y-%m-%d")
            office = offices[0].id
            request.session['graphic_date'] = date
        
    
    request.session['graphic_office'] = office
        
    dents = dates.objects.values_list('dentist', flat = True).filter(date = date).filter(dental_office = office)    
    dent = dentist.objects.filter(id__in = dents).order_by('last_name')
    
    hours2 = []
    hours = dates.objects.filter(date = date).filter(dental_office = office)
    if hours.count() > 0:
        min = hours[0].begin
        max = hours[0].end
        
        for h in hours:
            if h.begin < min:
                min = h.begin
            if h.end > max:
                max = h.end
                
        begin = datetime.datetime.combine(hours[0].date, min)
        end = datetime.datetime.combine(hours[0].date, max)
        while begin<end:
            hours2.append(begin.time())
            begin = begin + datetime.timedelta(minutes=15)
        
    
    appoints = []
    for d in dent:
        appoints.append(appointment.objects.filter(date = date).filter(dentist = d).filter(untimely=False).order_by('hour'))
    
    graphics = []   
    i = [] 
    for h in hours2:
        appoint = []
        j = 0
        for d in appoints:
            i.append(0)
            dodano = False
            for a in d:
                if a.hour == h:
                    appoint.append({'appoint': a, 'length': a.appointment_type.length/15})
                    dodano = True
                    i[j] = a.appointment_type.length/15
            if not dodano:
                i[j] = i[j]-1
                appoint.append({'appoint': None, 'length': i[j]})  
            j = j+1
        time = datetime.datetime.now()
        time_end = datetime.datetime.combine(hours[0].date, h) + datetime.timedelta(minutes=15)
        now = (time<time_end and time>datetime.datetime.combine(hours[0].date, h))
        graphics.append({'hour': h, 'appoint': appoint, 'now_time': now})  
            
    appoints_untimely = []
    appoints_untimely2 = []
    i = 0
    max_appoint = 0
    for d in dent:
        pom = appointment.objects.filter(date = date).filter(dentist = d).filter(untimely=True).order_by('patient')
        appoints_untimely.append(pom)
        if max_appoint < pom.count():
            max_appoint = pom.count()
    
    for i in range(0, max_appoint):
        appoints_untimely2.append([])
        for a in appoints_untimely:
            if i<a.count():
                appoints_untimely2[i].append(a[i])
            else:
                appoints_untimely2[i].append(None)

    return render(request, 'day_graphic.html', {'appoints': graphics, 'date': date, 'dents': dent, 'offices': offices, 'office': office, 'appoints_untimely': appoints_untimely2})

@login_required
@user_passes_test(in_receptionist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def dates_addition(request):
    if request.POST:
        if 'generate_submit' in request.POST.keys():
            office = request.POST['office']
            dentist_man = request.POST['dentist_man']
            begin = request.POST['begin']
            end = request.POST['end']
            exclude = request.POST['exclude']
            exclude_string_list = []
            exclude_date_list = []
            if exclude != "":
                exclude_string_list = exclude.split(',')
                for el in exclude_string_list:
                    element = datetime.datetime.fromtimestamp(time.mktime(time.strptime(el, "%Y-%m-%d")))
                    exclude_date_list.append(element)
            if office!="" and dentist_man!="" and begin!="" and end!="":
                begin = datetime.datetime.fromtimestamp(time.mktime(time.strptime(begin, "%Y-%m-%d")))
                end = datetime.datetime.fromtimestamp(time.mktime(time.strptime(end, "%Y-%m-%d")))
                hh = hours.objects.filter(dentist__id=dentist_man, dental_office__id=office)
                added_date_list = []
                for h in hh:
                    date_start = begin
                    while date_start.weekday()+1 != h.week_day and date_start<=end:
                        date_start += datetime.timedelta(days=1)
                    while date_start <= end:
                        if exclude_date_list.count(date_start) == 0:
                            
                            date_dentist = dates(date = date_start,
                                                 begin = h.begin,
                                                 end = h.end,
                                                 dentist = dentist.objects.get(id=request.POST['dentist_man']),
                                                 dental_office = dental_office.objects.get(id=request.POST['office']),
                                                 room = h.room)
                            duplicate = dates.objects.filter(dentist__id=request.POST['dentist_man'], dental_office__id=request.POST['office'], date=date_dentist.date)
                            print duplicate
                            if not duplicate:
                                date_dentist.save()
                                added_date_list.append(date_dentist)
                            date_start += datetime.timedelta(days=7)
                        else:
                            date_start += datetime.timedelta(days=7)
                form = EditAddedDatesForm(added_date_list) 
                messages.add_message(request, messages.INFO, 'Pomyślnie dodano terminy.')
                
                f_ids = []
                f_dates = []
                f_begins = []
                f_ends = []
                f_dentists = []
                f_dental_offices = []
                f_rooms = []
                i = 0
                for f in form:
                   if i%7 == 0:
                       f_ids.append(f)
                   if i%7 == 1:
                       f_dates.append(f)
                   if i%7 == 2:
                       f_begins.append(f)
                   if i%7 == 3:
                       f_ends.append(f)
                   if i%7 == 4:
                       f_dentists.append(f)
                   if i%7 == 5:
                       f_dental_offices.append(f)
                   if i%7 == 6:
                       f_rooms.append(f)
                   i = i + 1
                new_form = zip(f_ids, f_dates, f_begins, f_ends, f_dentists, f_dental_offices, f_rooms)
                return render(request, 'edit_added_dates.html', {'form': form, 'new_form': new_form})
            elif dentist_man!="":
                if request.GET.get('type', None) == 'ajax':
                    form = GenerateDatesForm(request.POST['office'], dentist_man)
                else:
                    form = GenerateDatesForm(request.POST['office'], dentist_man, request.POST)
            else:
                if request.GET.get('type', None) == 'ajax':
                    form = GenerateDatesForm(request.POST['office'], -1)
                else:
                    form = GenerateDatesForm(request.POST['office'], -1, request.POST)
        elif 'office' in request.POST.keys():
            if 'dentist_man' in request.POST.keys():
                if request.GET.get('type', None) == 'ajax':
                    form = GenerateDatesForm(request.POST['office'], request.POST['dentist_man'])
                else:
                    form = GenerateDatesForm(request.POST['office'], request.POST['dentist_man'], request.POST)
            else:
                if request.GET.get('type', None) == 'ajax':
                    form = GenerateDatesForm(request.POST['office'], -1)
                else:
                    form = GenerateDatesForm(request.POST['office'], -1, request.POST)
        elif 'generate_submit_edit' in request.POST.keys():
            try:
                i = 1
                while i <= int(request.POST['number_of_fields']):
                    d = dates.objects.get(id=request.POST['id_%s' % i])
                    d.begin = request.POST['begin_%s' % i]
                    d.end = request.POST['end_%s' % i]
                    d.room = request.POST['room_%s' % i]
                    d.save()
                    i += 1 
            except ValidationError:
                added_date_list = []
                i = 1
                while i <= int(request.POST['number_of_fields']):
                    d = dates.objects.get(id=request.POST['id_%s' % i])
                    d.begin = request.POST['begin_%s' % i]
                    d.end = request.POST['end_%s' % i]
                    d.room = request.POST['room_%s' % i]
                    added_date_list.append(d)
                    i += 1 
                form = EditAddedDatesForm(added_date_list) 
                messages.add_message(request, messages.ERROR, 'Błędny format danych dla pola/pól "Od"/"Do". Użyj formatu "HH:mm"')
                
                f_ids = []
                f_dates = []
                f_begins = []
                f_ends = []
                f_dentists = []
                f_dental_offices = []
                f_rooms = []
                i = 0
                for f in form:
                   if i%7 == 0:
                       f_ids.append(f)
                   if i%7 == 1:
                       f_dates.append(f)
                   if i%7 == 2:
                       f_begins.append(f)
                   if i%7 == 3:
                       f_ends.append(f)
                   if i%7 == 4:
                       f_dentists.append(f)
                   if i%7 == 5:
                       f_dental_offices.append(f)
                   if i%7 == 6:
                       f_rooms.append(f)
                   i = i + 1
                new_form = zip(f_ids, f_dates, f_begins, f_ends, f_dentists, f_dental_offices, f_rooms)
                return render(request, 'edit_added_dates.html', {'form': form, 'new_form': new_form})
            else:
                offices = dental_office.objects.all()
                form = GenerateDatesForm(offices[0].id, -1) 
                messages.add_message(request, messages.INFO, 'Pomyślnie zaktualizowano dodane terminy.')
    else:
        offices = dental_office.objects.all()
        form = GenerateDatesForm(offices[0].id, -1)
    return render(request, 'dates_addition.html', {'form': form})

@user_passes_test(new_password, login_url="/password/")
def offices(request):
    offs = dental_office.objects.all()
    offices =[]
    dents = dentist.objects.all().order_by('last_name')
    pages = {}
    i = 0;
    for d in dents:
        page = i/5 + 1
        pages[d.last_name] = page
        i = i + 1
    for o in offs:
        hour = hours.objects.values_list('dentist').filter(dental_office=o.id)
        dentists = dentist.objects.filter(id__in=hour).order_by('last_name')
        dentists2 = []
        for d in dentists:
            hour = hours.objects.filter(dentist = d).filter(dental_office = o.id).order_by('week_day')
            dentists2.append({'d': d, 'page': pages[d.last_name], 'hours': hour})
        offices.append({'office':o, 'dentists':dentists2})
    return render(request, 'offices.html',{'offices': offices})

@user_passes_test(new_password, login_url="/password/")
def dentists(request):
    dents = dentist.objects.all().order_by('last_name')
    dentists = []
    for d in dents:
        hour = hours.objects.values_list('dental_office', flat=True).filter(dentist = d.id)
        offs = dental_office.objects.filter(id__in=hour)
        offices = []
        for o in offs:
            hour2 = hours.objects.filter(dentist=d.id).filter(dental_office=o.id).order_by('week_day')
            offices.append({'office':o, 'hours': hour2})
        dentists.append({'dentist': d, 'offices': offices})
    
    paginator = Paginator(dentists, 5)
    page = request.GET.get('page')
    try:
        dentists2 = paginator.page(page)
    except PageNotAnInteger:
        dentists2 = paginator.page(1)
    except EmptyPage:
        dentists2 = paginator.page(1)
    return render(request, 'dentists.html',{'dentists': dentists2})

@login_required
@user_passes_test(in_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/")
def reservations(request):
    if request.POST:
        if 'appointment' in request.POST.keys():
            app = request.POST['appointment']
            appointment.objects.get(id=app).delete()
            messages.add_message(request, messages.INFO, 'Pomyślnie usunięto termin wizyty.')
            return HttpResponseRedirect('/reservations/')
        elif 'appointment2' in request.POST.keys():
            app = appointment.objects.get(id=request.POST['appointment2'])
            if 'date' in request.POST.keys():
                if 'appoint' in request.POST.keys():
                    day = datetime.datetime.strptime(request.POST['appoint'], '%Y-%m-%d %H:%M:%S')
                    app.date = day.date()
                    app.hour = day.time()
                    app.save()
                    messages.add_message(request, messages.INFO, 'Pomyślnie zmieniono termin wizyty.')
                    return HttpResponseRedirect('/reservations/')
                else:
                    apps = []
                    day = dates.objects.get(id=request.POST['date'])
                    dayend = datetime.datetime.combine(day.date, day.end)
                    if day.date == datetime.datetime.now().date():
                        hour = datetime.datetime.now()
                        minute = hour.time().minute
                        h = datetime.datetime.combine(day.date, hour.time())
                        typ2 = appointment_type.objects.get(id = typ).length
                        if minute < 15 and typ2 == 15:
                            h = h + datetime.timedelta(minutes=(15 - minute))
                        elif minute < 30 and typ2 < 60:
                            h = h + datetime.timedelta(minutes=(30 - minute))
                        elif minute < 45 and typ2 == 15:
                            h = h + datetime.timedelta(minutes=(45 - minute))
                        else:
                            h = h + datetime.timedelta(minutes=(60 - minute))
                        h = h - datetime.timedelta(seconds = hour.time().second, microseconds = hour.time().microsecond)
                        hour = h
                    else:
                        hour = datetime.datetime.combine(day.date, day.begin)
                    minutes = app.appointment_type.length
                    while hour + datetime.timedelta(minutes=minutes)<=dayend:
                        apps.append(hour)
                        hour = hour + datetime.timedelta(minutes=minutes)
                    
                    deleted_apps = []
                    for h in apps:
                        for ap in appointment.objects.filter(date = day).filter(dentist = app.dentist.id).filter(dental_office = app.dental_office.id).filter(untimely=False):
                            ap_date = datetime.datetime.combine(ap.date, ap.hour)
                            length = ap.appointment_type.length
                            ap_end = datetime.datetime.combine(ap.date, ap.hour) + datetime.timedelta(minutes=length)
                            h_end = h + datetime.timedelta(minutes=app.appointment_type.length)
                            if h >= ap_date and h.time() < ap_end.time() or h <= ap_date and h_end > ap_date:
                                if not h in deleted_apps:
                                    deleted_apps.append(h)
                                
                    for h in deleted_apps:            
                        apps.remove(h)
                    if request.GET.get('type', None) == 'ajax':
                        form = RegisterChangeForm(app.dental_office.id, app.dentist.id, request.POST['date'], apps, app.appointment_type.id)
                    else:
                        form = RegisterChangeForm(app.dental_office.id, app.dentist.id, request.POST['date'], apps, app.appointment_type.id, request.POST)
                    return render(request, 'reservations_change.html', {'form': form, 'app_id': app.id})
            else:
                if request.GET.get('type', None) == 'ajax':
                    form = RegisterChangeForm(app.dental_office.id, app.dentist.id, -1, -1, app.appointment_type.id)
                else:
                    form = RegisterChangeForm(app.dental_office.id, app.dentist.id, -1, -1, app.appointment_type.id, request.POST)
                print 'a'
                if dates.objects.filter(dental_office=app.dental_office.id).filter(dentist=app.dentist.id).filter(date__gte=datetime.date.today).count() == 0:
                    messages.add_message(request, messages.ERROR, 'Nie ma innych wolnych terminów.')
                    return HttpResponseRedirect('/reservations/')
                return render(request, 'reservations_change.html', {'form': form, 'app_id': app.id})
    
    if in_patient_group(request.user):
        pat = patient.objects.get(user = request.user)
        reservations = appointment.objects.filter(patient=pat.id).filter(date__gte=datetime.datetime.now().date()).order_by('date')
    elif in_receptionist_group(request.user):
        if request.POST and 'patient' in request.POST.keys():
            reservations = appointment.objects.filter(patient=request.POST['patient']).filter(date__gte=datetime.datetime.now().date()).order_by('date')
            pat = patient.objects.get(id=request.POST['patient'])
        else:
            if request.POST and 'pat' in request.POST.keys():
                patients = patient.objects.filter(last_name__startswith=request.POST['pat'].title()).order_by('first_name')
            else:
                patients = patient.objects.all().order_by('last_name')
            paginator = Paginator(patients, 25)
            page = request.GET.get('page')
            try:
                patients2 = paginator.page(page)
            except PageNotAnInteger:
                patients2 = paginator.page(1)
            except EmptyPage:
                patients2 = paginator.page(1)
            return render(request, 'patients2.html', {'patients': patients2})
    return render(request, 'reservations.html', {'reservations': reservations, 'patient': pat})

@login_required
@user_passes_test(in_patient_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/") 
def patient_card(request):
    pat = patient.objects.get(user = request.user)
    appoints = appointment.objects.filter(patient = pat).filter(date__lte = datetime.datetime.now().date()).order_by('-date')
    
    losses = tooth_loss.objects.filter(appointment__in = appointment.objects.filter(patient = pat))
    if 'tooth' in request.POST.keys():
        losses = losses.filter(tooth = tooth.objects.get(id = request.POST['tooth'])).filter(tooth_part = tooth_part.objects.get(id = request.POST['tooth_part'])).order_by('-id')
    return render(request, 'patient_card.html', {'patient': pat, 'appoints': appoints, 'losses': losses })

@login_required
@user_passes_test(in_dentist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/") 
def patient_card_dentist(request):
    appoint = appointment.objects.get(id = request.session['appoint'])
    pat = appoint.patient
    appoints = appointment.objects.filter(patient = pat).filter(date__lt = datetime.datetime.now().date()).order_by('-date')
    form = ToothForm
    losses = tooth_loss.objects.filter(appointment__in = appointment.objects.filter(patient = pat))
    if request.POST:
        if 'patient_comment' in request.POST.keys():
            pat.comment = request.POST['patient_comment'].strip()
            pat.save()
        if 'is_now' in request.POST.keys():
            appoint.is_now = request.POST['is_now']
            appoint.save()
        if 'appointment_description' in request.POST.keys():
            appoint.description = request.POST['appointment_description'].strip()
            appoint.save()
        if 'app' in request.POST.keys():
            app = appointment.objects.get(id=request.POST['app'])
            app.description = request.POST['app_desc'].strip()
            app.save()
        if 'tooth' in request.POST.keys():
            if 'tooth_part' in request.POST.keys():
                if 'comment' in request.POST.keys():
                    loss = tooth_loss(appointment = appoint, 
                                      tooth = tooth.objects.get(id=request.POST['tooth']), 
                                      tooth_part = tooth_part.objects.get(id=request.POST['tooth_part']),
                                      loss_type = loss_type.objects.get(id=request.POST['loss_type']),
                                      comment = request.POST['comment'])
                    loss.save()
                else:
                    losses = losses.filter(tooth = tooth.objects.get(id = request.POST['tooth'])).filter(tooth_part = tooth_part.objects.get(id = request.POST['tooth_part'])).order_by('-id')
                    form = ToothForm(request.POST['tooth'], request.POST['tooth_part'])
            else:
                form = ToothForm(request.POST['tooth'])

    return render(request, 'patient_card_dentist.html', {'patient': pat, 'appoints': appoints, 'date': request.session['date'], 'graphic': request.session['graphic'], 'appointment': appoint, 'form': form, 'losses': losses })

@login_required
@user_passes_test(in_dentist_group, login_url='/access_denied/')
@user_passes_test(new_password, login_url="/password/") 
def dentist_profile(request):
    dent = dentist.objects.get(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = request.user)
        form_dentist = DentistForm(request.POST, instance = dent)
        if form.is_valid() and form_dentist.is_valid(): 
            form.save()            
            form_dentist.save()
            messages.add_message(request, messages.INFO, 'Pomyślnie zaktualizowano profil.')
            return HttpResponseRedirect('/index/')
    else:
        form = ProfileForm(instance = request.user)
        form_dentist = DentistForm(instance = dent)
    return render(request, 'dentist_profile.html', {'form': form, 'form_dentist': form_dentist})