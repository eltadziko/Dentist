# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class patient(models.Model):
    birth_date = models.DateField("Data ur.")
    address = models.CharField("Adres", max_length=100)
    PESEL = models.CharField("PESEL", max_length=11, unique=True)
    insurance_number = models.CharField("Nr ubezp.", max_length=10)
    phone = models.CharField("Telefon", max_length=9, blank=True, null=True)
    comment = models.TextField("O pacjencie", blank=True, null=True)
    user_id = models.ForeignKey(User, verbose_name="User")
    
    class Meta:
        verbose_name= "Pacjent"

    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        return u'Pacjent: %s %s' % (user.first_name, user.last_name)
    
class dentist(models.Model):
    title = models.CharField("Tytuł", max_length=30, blank=True, null=True)
    description = models.TextField("O dentyście", blank=True, null=True)
    phone = models.CharField("Telefon", max_length=9, blank=True, null=True)
    user_id = models.ForeignKey(User, verbose_name="User")
    
    class Meta:
        verbose_name = "Dentysta"

    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        return u'Dentysta: %s %s' % (user.first_name, user.last_name)

class disease(models.Model):
    disease_name = models.CharField("Nazwa choroby", max_length=30)

    class Meta:
        verbose_name = "Choroba"

    def __unicode__(self):
        return u'Choroba: %s' % (self.disease_name)
    
class patient_diseases(models.Model):
    patient_id = models.ForeignKey(patient, verbose_name="Pacjent")
    disease_id = models.ForeignKey(disease, verbose_name="Choroba")
    date = models.DateField("Data")
    
    class Meta:
        verbose_name = "Choroby Pacjenta"

    def __unicode__(self):
        p = patient.objects.get(id=self.patient_id)
        user = User.objects.get(id=p.user_id)
        d = disease.objects.get(id=self.disease_id)
        return u'Choroba %s dla Pacjenta: %s %s' % (d.disease_name, user.first_name, user.last_name)
    
class dental_office(models.Model):
    name = models.CharField("Nazwa", max_length=30, blank=True, null=True)
    address = models.CharField("Adres", max_length=100)
    description = models.TextField("O gabinecie", blank=True, null=True)

    class Meta:
        verbose_name = "Gabinet"

    def __unicode__(self):
        return u'Gabinet: %s' % (self.name)
    
class hours(models.Model):
    week_day = models.IntegerField("Dzień tygodnia", max_length=1)
    begin = models.TimeField("Przyjmuje od")
    end = models.TimeField("Przyjmuje do")
    dentist_id = models.ForeignKey(dentist, verbose_name="Dentysta")
    dental_office_id = models.ForeignKey(dental_office, verbose_name="Gabinet")
    room = models.CharField("Pokój", max_length=5) 
    
    class Meta:
        verbose_name = "Godziny"

    def __unicode__(self):
        d = dentist.objects.get(id=self.dentist_id)
        user = User.objects.get(id=d.user_id)
        do = dental_office.objects.get(id=self.dental_office_id)
        return u'Dentysta %s %s przyjmujący w %s w godzinach %t-%t w gabinecie %s' % (user.first_name, user.last_name, self.week_day, self.begin, self.end, do.name)
    
class dates(models.Model):
    date = models.DateField("Data")
    begin = models.TimeField("Od")
    end = models.TimeField("Do")
    dentist_id = models.ForeignKey(dentist, verbose_name="Dentysta")
    dental_office_id = models.ForeignKey(dental_office, verbose_name="Gabinet")
    room = models.CharField("Pokój", max_length=5) 
    
    class Meta:
        verbose_name = "Termin"

    def __unicode__(self):
        return self.date
    
class appointment_type(models.Model):
    type = models.CharField("Typ", max_length=30)
    length = models.IntegerField("Długość")
    
    class Meta:
        verbose_name = "Typ wizyty"
    
    def __unicode__(self):
        return self.length
    
class appointment(models.Model):
    date = models.DateField("Data")
    description = models.TextField("Opis", blank=True, null=True)
    dentist_id = models.ForeignKey(dentist, verbose_name="Dentysta")
    patient_id = models.ForeignKey(patient, verbose_name="Pacjent")
    dental_office_id = models.ForeignKey(dental_office, verbose_name="Gabinet")
    appointment_type_id = models.ForeignKey(appointment_type, verbose_name="Typ wizyty")
    
    class Meta:
        verbose_name = "Wizyta"

    def __unicode__(self):
        return self.date
    
class tooth(models.Model):
    TYPE_CHOICES = (('si', 'siekacz'),('ki', 'kieł'),('pr', 'przedtrzonowiec'),('tr', 'trzonowiec'))
    type = models.CharField("Rodzaj zęba", max_length=2, choices=TYPE_CHOICES)
    JAW_CHOICES = (('g', 'górna'), ('d', 'dolna'))
    jaw = models.CharField("Szczęka", max_length=1, choices=JAW_CHOICES)
    SIDE_CHOICES = (('l', 'lewa'), ('p', 'prawa'))
    side = models.CharField("Strona", max_length=1, choices=SIDE_CHOICES)
    tooth_number = models.IntegerField("Nr zęba")
    
    class Meta:
        verbose_name = "Ząb"

    def __unicode__(self):
        return self.type
    
class loss_type(models.Model):
    type = models.CharField("Typ", max_length=30)
    
    class Meta:
        verbose_name = "Typ ubytku"
    
    def __unicode__(self):
        return self.type
    
class tooth_part(models.Model):
    name = models.CharField("Nazwa", max_length=30)
    
    class Meta:
        verbose_name = "Część zęba"
    
    def __unicode__(self):
        return self.name
    
class tooth_loss(models.Model):
    appointment_id = models.ForeignKey(appointment, verbose_name="Wizyta")
    tooth_id = models.ForeignKey(tooth, verbose_name="Ząb")
    loss_type_id = models.ForeignKey(loss_type, verbose_name="Typ ubytku")
    tooth_part_id = models.ForeignKey(tooth_part, verbose_name="Część zęba")
    comment = models.TextField("Komentarz", blank=True, null=True)
    
    class Meta:
        verbose_name = "Ubytek zęba"

    def __unicode__(self):
        return self.comment