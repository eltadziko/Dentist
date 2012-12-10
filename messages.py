# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import Dentist.settings
setup_environ(Dentist.settings)
import datetime, time
from Dentist.models import *
from django.core.mail import send_mail, send_mass_mail

sended = False

while not sended:
    now = datetime.datetime.now().time()
    send_time = datetime.datetime.strptime('10:00', '%H:%M').time()
    if now>send_time:
        print 'Zaczeto rozsylanie przypomnien'
        today = datetime.datetime.today().date()
        tomorow = today + datetime.timedelta(days=2)
        appointments = appointment.objects.filter(date=tomorow)
        messages_list = []
        for app in appointments:
            subject = "Przypomnienie wizyty"
            if app.hour:
                hour = app.hour.strftime("%H:%M")
            else:
                hour = 'bezterminowa'
            text = "Przypominamy o wizycie w dniu jutrzejszym ("+app.date.strftime("%d-%m-%Y")+") o godz: "+hour+" w gabinecie "+str(app.dental_office)+". Lekarz: "+str(app.dentist)+"."
            to = app.patient.user.email
            message=(subject, text, 'dentistzpi@gmail.com', [to] )
            messages_list.append(message)
        send_mass_mail(messages_list, fail_silently=False)
        print 'Rozesłano przypomnienia mailowe'
        time.sleep(23*60*60+50*60)
    print 'Nie teraz'
    time.sleep(60)