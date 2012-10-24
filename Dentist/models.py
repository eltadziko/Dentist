# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Imie i nazwisko w dentyscie i pacjencie, user w pacjencie moze byc null. 
#Dodac do pacjenta typ ubezpieczenia, numer ubezp zmienic na max_length=255
#ZMienić chorobas w adminie
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
        return u'Dentysta: %s %s' % (user.first_name, user.last_name)

class disease(models.Model):
    disease_name = models.CharField("Nazwa choroby", max_length=30)

    class Meta:
        verbose_name = "Choroba"
        verbose_name_plural = "Choroby"

    def __unicode__(self):
        return u'Choroba: %s' % (self.disease_name)
    
class patient(models.Model):
    first_name = models.CharField("Imię", max_length=30)
    last_name = models.CharField("Nazwisko", max_length=30)
    birth_date = models.DateField("Data ur.")
    address = models.CharField("Adres", max_length=100)
    PESEL = models.CharField("PESEL", max_length=11, unique=True)
    TYPE_CHOICES = (('praca RMUA', 'raport miesięczny ZUS RMUA'),
                    ('praca zaświadczenie', 'zaświadczenie z zakładu pracy'),
                    ('praca legitymacja', 'legitymacja ubezpieczeniowa'),
                    ('działalność gospodarcza', 'działalność gospodarcza'),
                    ('KRUS', 'KRUS'),
                    ('emeryt', 'legitymacja emeryta'),
                    ('rencista', 'legitymacja rencisty'),
                    ('bezrobotny', 'zaświadczenie z urzędu pracy'),
                    ('ubezpieczony dobrowolnie', 'ubezpieczony dobrowolnie'),
                    ('członek rodziny ubezp. dowód', 'członek rodziny ubezp. dowód'),
                    ('członek rodziny ubezp. pracodawca', 'członek rodziny ubezp. pracodawca'),
                    ('członek rodziny ubezp. KRUS', 'członek rodziny ubezp. KRUS'),
                    ('członek rodziny ubezp. legitymacja', 'członek rodziny ubezp. legitymacja'),
                    ('członek rodziny ubezp. emeryt', 'członek rodziny ubezp. emeryt'),
                    ('członek rodziny ubezp. rencista', 'członek rodziny ubezp. rencista'),
                    ('członek rodziny ubezp. dzieci', 'członek rodziny ubezp. dzieci'),
                    ('student po 26', 'student po 26'),
                    ('nieubezp. spełn. kryt. dochodowe', 'nieubezp. spełn. kryt. dochodowe'),
                    ('ubezpieczony w UE EFTA', 'ubezpieczony w UE EFTA'),
                    ('ubezpieczony w UE EFTA2', 'ubezpieczony w UE EFTA2'),
                    ('zasiłek chorobowy', 'zasiłek chorobowy'),)
    insurance_type = models.CharField("Rodzaj ubezpieczenia", max_length=200, choices=TYPE_CHOICES)
    insurance_number = models.CharField("Nr ubezp.", max_length=100)
    phone = models.CharField("Telefon", max_length=9, blank=True, null=True)
    comment = models.TextField("Uwagi", blank=True, null=True)
    user = models.OneToOneField(User, verbose_name="User",  blank=True, null=True)
    diseases = models.ManyToManyField(disease, through="patient_diseases")
    
    class Meta:
        verbose_name= "Pacjent"
        verbose_name_plural = "Pacjenci"

    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        return u'%s %s, %s' % (self.last_name, self.first_name, self.address)
    
class patient_diseases(models.Model):
    patient = models.ForeignKey(patient, verbose_name="Pacjent")
    disease = models.ForeignKey(disease, verbose_name="Choroba")
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
    dentist = models.ForeignKey(dentist, verbose_name="Dentysta")
    dental_office = models.ForeignKey(dental_office, verbose_name="Gabinet")
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
    dentist = models.ForeignKey(dentist, verbose_name="Dentysta")
    dental_office = models.ForeignKey(dental_office, verbose_name="Gabinet")
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
    dentist = models.ForeignKey(dentist, verbose_name="Dentysta")
    patient = models.ForeignKey(patient, verbose_name="Pacjent")
    dental_office = models.ForeignKey(dental_office, verbose_name="Gabinet")
    appointment_type = models.ForeignKey(appointment_type, verbose_name="Typ wizyty")
    
    class Meta:
        verbose_name = "Wizyta"

    def __unicode__(self):
        return self.date
    
class tooth(models.Model):
    TYPE_CHOICES = (('siekacz', 'siekacz'),('kieł', 'kieł'),('przedtrzonowiec', 'przedtrzonowiec'),('trzonowiec', 'trzonowiec'))
    type = models.CharField("Rodzaj zęba", max_length=15, choices=TYPE_CHOICES)
    JAW_CHOICES = (('górna', 'górna'), ('dolna', 'dolna'))
    jaw = models.CharField("Szczęka", max_length=5, choices=JAW_CHOICES)
    SIDE_CHOICES = (('lewa', 'lewa'), ('prawa', 'prawa'))
    side = models.CharField("Strona", max_length=5, choices=SIDE_CHOICES)
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
    appointment = models.ForeignKey(appointment, verbose_name="Wizyta")
    tooth = models.ForeignKey(tooth, verbose_name="Ząb")
    loss_type = models.ForeignKey(loss_type, verbose_name="Typ ubytku")
    tooth_part = models.ForeignKey(tooth_part, verbose_name="Część zęba")
    comment = models.TextField("Komentarz", blank=True, null=True)
    
    class Meta:
        verbose_name = "Ubytek zęba"

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
