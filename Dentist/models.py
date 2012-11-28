# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class dentist(models.Model):
    first_name = models.CharField("Imię", max_length=30)
    last_name = models.CharField("Nazwisko", max_length=30)
    title = models.CharField("Tytuł", max_length=30, blank=True, null=True)
    description = models.TextField("O dentyście", blank=True, null=True)
    phone = models.CharField("Telefon", max_length=9, blank=True, null=True)
    user = models.OneToOneField(User, verbose_name="User")
    
    class Meta:
        verbose_name = "Dentysta"
        verbose_name_plural = "Dentyści"

    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        return u'%s %s' % (self.last_name, self.first_name)

class disease(models.Model):
    disease_name = models.CharField("Nazwa choroby", max_length=30)

    class Meta:
        verbose_name = "Choroba"
        verbose_name_plural = "Choroby"

    def __unicode__(self):
        return u'%s' % (self.disease_name)
    
class insurance(models.Model):
    short_name = models.CharField("Krótka nazwa", max_length=30)
    name = models.CharField("Nazwa", max_length=100)
    description = models.CharField("Opis", max_length=250, blank=True, null=True)
    
    class Meta:
        verbose_name = "Ubezpieczenie"
        verbose_name_plural = "Ubezpieczenia"

    def __unicode__(self):
        return u'%s' % (self.name)
    
class patient(models.Model):
    first_name = models.CharField("Imię", max_length=30)
    last_name = models.CharField("Nazwisko", max_length=30)
    birth_date = models.DateField("Data ur.")
    address = models.CharField("Adres", max_length=100)
    PESEL = models.CharField("PESEL", max_length=11, unique=True)
    insurance_type = models.ForeignKey(insurance, verbose_name="Typ ubezpieczenia")
    insurance_number = models.CharField("Nr ubezp.", max_length=100)
    phone = models.CharField("Telefon", max_length=9, blank=True, null=True)
    comment = models.TextField("Uwagi", blank=True, null=True)
    user = models.OneToOneField(User, verbose_name="User",  blank=True, null=True)
    diseases = models.ManyToManyField(disease, through="patient_diseases")
    
    class Meta:
        verbose_name= "Pacjent"
        verbose_name_plural = "Pacjenci"

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)
    
class patient_diseases(models.Model):
    patient = models.ForeignKey(patient, verbose_name="Pacjent")
    disease = models.ForeignKey(disease, verbose_name="Choroba")
    date = models.DateField("Data")
    
    class Meta:
        verbose_name = "Choroba Pacjenta"
        verbose_name_plural = "Choroby Pacjenta"

    def __unicode__(self):
        p = patient.objects.get(id=self.patient_id)
        user = User.objects.get(id=p.user_id)
        d = disease.objects.get(id=self.disease_id)
        return u'Choroba %s dla Pacjenta: %s %s' % (d.disease_name, user.first_name, user.last_name)
    
class dental_office(models.Model):
    name = models.CharField("Nazwa", max_length=30, blank=True, null=True)
    address = models.CharField("Adres", max_length=100)
    phone = models.CharField("Telefon", max_length=9)
    email = models.EmailField("Email")
    description = models.TextField("O gabinecie", blank=True, null=True)

    class Meta:
        verbose_name = "Gabinet"
        verbose_name_plural = "Gabinety"

    def __unicode__(self):
        return u'%s' % (self.address)
    
class hours(models.Model): 
    week_day = models.IntegerField("Dzień tygodnia", max_length=1)
    begin = models.TimeField("Przyjmuje od")
    end = models.TimeField("Przyjmuje do")
    dentist = models.ForeignKey(dentist, verbose_name="Dentysta")
    dental_office = models.ForeignKey(dental_office, verbose_name="Gabinet")
    room = models.CharField("Pokój", max_length=5) 
    
    class Meta:
        verbose_name = "Godziny"
        verbose_name_plural = "Godziny"

    def __unicode__(self):
        d = dentist.objects.get(id=self.dentist_id)
        user = User.objects.get(id=d.user_id)
        do = dental_office.objects.get(id=self.dental_office_id)
        return u'%i' % (self.week_day)
    
class dates(models.Model):
    date = models.DateField("Data")
    begin = models.TimeField("Od")
    end = models.TimeField("Do")
    dentist = models.ForeignKey(dentist, verbose_name="Dentysta")
    dental_office = models.ForeignKey(dental_office, verbose_name="Gabinet")
    room = models.CharField("Pokój", max_length=5) 
    
    class Meta:
        verbose_name = "Termin"
        verbose_name_plural = "Terminy"
        unique_together = (("date", "begin", "end", "dentist"),)

    def __unicode__(self):
        return u'%s' % (self.date)
    
class appointment_type(models.Model):
    type = models.CharField("Typ", max_length=30)
    length = models.IntegerField("Długość")
    
    class Meta:
        verbose_name = "Typ wizyty"
        verbose_name_plural = "Typy wizyt"
    
    def __unicode__(self):
        return u'%s (%s min)' % (self.type, self.length)
    
class appointment(models.Model):
    date = models.DateField("Data")
    hour = models.TimeField("Godzina", blank=True, null=True)
    description = models.TextField("Opis", blank=True, null=True)
    dentist = models.ForeignKey(dentist, verbose_name="Dentysta")
    patient = models.ForeignKey(patient, verbose_name="Pacjent")
    dental_office = models.ForeignKey(dental_office, verbose_name="Gabinet")
    appointment_type = models.ForeignKey(appointment_type, verbose_name="Typ wizyty", blank=True, null=True)
    is_now = models.IntegerField("Trwa", blank=True, null=True)
    untimely = models.BooleanField("Nieterminowa", default=False)
    
    class Meta:
        verbose_name = "Wizyta"
        verbose_name_plural = "Wizyty"

    def __unicode__(self):
        return u'%s %s Pacjent: %s, Lekarz: %s' % (self.date, self.hour, self.patient, self.dentist)

class loss_type(models.Model):
    type = models.CharField("Typ", max_length=30)
    
    class Meta:
        verbose_name = "Typ ubytku"
        verbose_name_plural = "Typy ubytków"
    
    def __unicode__(self):
        return self.type
          
class tooth_part(models.Model):
    name = models.CharField("Nazwa", max_length=40)
    losses = models.ManyToManyField(loss_type)
    
    class Meta:
        verbose_name = "Część zęba"
        verbose_name_plural = "Części zębów"
    
    def __unicode__(self):
        return self.name
    
class tooth(models.Model):
    TYPE_CHOICES = (('siekacz', 'siekacz'),('kieł', 'kieł'),('przedtrzonowiec', 'przedtrzonowiec'),('trzonowiec', 'trzonowiec'))
    type = models.CharField("Rodzaj zęba", max_length=15, choices=TYPE_CHOICES)
    JAW_CHOICES = (('górna', 'górna'), ('dolna', 'dolna'))
    jaw = models.CharField("Szczęka", max_length=5, choices=JAW_CHOICES)
    SIDE_CHOICES = (('lewa', 'lewa'), ('prawa', 'prawa'))
    side = models.CharField("Strona", max_length=5, choices=SIDE_CHOICES)
    tooth_number = models.IntegerField("Nr zęba")
    parts = models.ManyToManyField(tooth_part)
    
    class Meta:
        verbose_name = "Ząb"
        verbose_name_plural = "Zęby"

    def __unicode__(self):
        return self.type
    
class tooth_loss(models.Model):
    appointment = models.ForeignKey(appointment, verbose_name="Wizyta")
    tooth = models.ForeignKey(tooth, verbose_name="Ząb")
    loss_type = models.ForeignKey(loss_type, blank=True, null=True, verbose_name="Typ ubytku")
    tooth_part = models.ForeignKey(tooth_part, verbose_name="Część zęba")
    comment = models.TextField("Komentarz", blank=True, null=True)
    
    class Meta:
        verbose_name = "Ubytek zęba"
        verbose_name_plural = "Ubytki zębów"

    def __unicode__(self):
        return self.comment
    
class password_creation(models.Model):
    user = models.OneToOneField(User, verbose_name="Użytkownik")
    last_change = models.DateField("Data")
    
    class Meta:
        verbose_name = "Hasło"
        verbose_name_plural = "Hasła"

    def __unicode__(self):
        return self.last_change
