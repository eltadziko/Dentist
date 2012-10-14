# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class patient(models.Model):
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    PESEL = models.CharField(max_length=11)
    insurance_number = models.CharField(max_length=10)
    phone = models.CharField(max_length=9)
    comment = models.TextField()
    user_id = models.ForeignKey(User)

    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        return u'Pacjent: %s %s' % (user.first_name, user.last_name)
    
class dentist(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    phone = models.CharField(max_length=9)
    user_id = models.ForeignKey(User)

    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        return u'Dentysta: %s %s' % (user.first_name, user.last_name)

class disease(models.Model):
    diease_name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'Choroba: %s' % (self.diease_name)
    
class patient_dieases(models.Model):
    patient_id = models.ForeignKey(patient)
    disease_id = models.ForeignKey(disease)
    date = models.DateField()

    def __unicode__(self):
        p = patient.objects.get(id=self.patient_id)
        user = User.objects.get(id=p.user_id)
        d = disease.objects.get(id=self.diease_id)
        return u'Choroba %s dla Pacjenta: %s %s' % (d.diease_name, user.first_name, user.last_name)
    
class dental_office(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'Gabinet: %s' % (self.name)
    
class hours(models.Model):
    week_day = models.CharField(max_length=15)
    begin = models.TimeField()
    end = models.TimeField()
    dentist_id = models.ForeignKey(dentist)
    dental_office_id = models.ForeignKey(dental_office)
    room = models.IntegerField() #moze tak char? pokoj 2.12

    def __unicode__(self):
        d = dentist.objects.get(id=self.dentist_id)
        user = User.objects.get(id=d.user_id)
        do = dental_office.objects.get(id=self.dental_office_id)
        return u'Dentysta %s %s przyjmujący w %s w godzinach %t-%t w gabinecie %s' % (user.first_name, user.last_name, self.week_day, self.begin, self.end, do.name)
    
class dates(models.Model):
    date = models.DateField()
    begin = models.TimeField()
    end = models.TimeField()
    dentist_id = models.ForeignKey(dentist)
    dental_office_id = models.ForeignKey(dental_office)
    room = models.IntegerField() #moze tak char? pokoj 2.12

    def __unicode__(self):
        return self.date
    
class appointment_type(models.Model):
    type = models.CharField(max_length=30)
    length = models.IntegerField()
    
    def __unicode__(self):
        return self.length
    
class appointment(models.Model):
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    end = models.TimeField()
    dentist_id = models.ForeignKey(dentist)
    patient_id = models.ForeignKey(patient)
    dental_office_id = models.ForeignKey(dental_office)
    appointment_type_id = models.ForeignKey(appointment_type)

    def __unicode__(self):
        return self.date
    
class tooth(models.Model):
    TYPE_CHOICES = (('si', 'siekacz'),('ki', 'kieł'),('pr', 'przedtrzonowiec'),('tr', 'trzonowiec'))
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    JAW_CHOICES = (('g', 'górna'), ('d', 'dolna'))
    jaw = models.CharField(max_length=1, choices=JAW_CHOICES)
    SIDE_CHOICES = (('l', 'lewa'), ('p', 'prawa'))
    side = models.CharField(max_length=1, choices=SIDE_CHOICES)
    tooth_number = models.IntegerField()

    def __unicode__(self):
        return self.type
    
class loss_type(models.Model):
    type = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.type
    
class tooth_part(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    
class tooth_loss(models.Model):
    appointment_id = models.ForeignKey(appointment)
    tooth_id = models.ForeignKey(tooth)
    loss_type_id = models.ForeignKey(loss_type)
    tooth_part_id = models.ForeignKey(tooth_part)
    comment = models.TextField()

    def __unicode__(self):
        return self.comment