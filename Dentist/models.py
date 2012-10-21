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
        return u'Dentysta: %s %s' % (user.first_name, user.last_name)

class disease(models.Model):
    disease_name = models.CharField("Nazwa choroby", max_length=30)

    class Meta:
        verbose_name = "Choroba"

    def __unicode__(self):
        return u'Choroba: %s' % (self.disease_name)
    
class patient(models.Model):
    first_name = models.CharField("Imię", max_length=30)
    last_name = models.CharField("Nazwisko", max_length=30)
    birth_date = models.DateField("Data ur.")
    address = models.CharField("Adres", max_length=100)
    PESEL = models.CharField("PESEL", max_length=11, unique=True)
    TYPE_CHOICES = (('praca RMUA', 'druk zgłoszenia do ubezpieczenia zdrowotnego oraz aktualnie potwierdzony raport miesięczny ZUS RMUA wydawany przez pracodawcę (nie dotyczy osób na urlopie bezpłatnym powyżej 30 dni)'),
                    ('praca zaświadczenie', 'aktualne zaświadczenie z zakładu pracy'),
                    ('praca legitymacja', 'legitymacja ubezpieczeniowa'),
                    ('działalność gospodarcza', 'druk zgłoszenia do ubezpieczenia zdrowotnego oraz aktualny dowód wpłaty składki na ubezpieczenie zdrowotne'),
                    ('KRUS', 'zaświadczenie lub legitymacja aktualnie podstemplowane przez KRUS'),
                    ('emeryt', 'legitymacja emeryta'),
                    ('rencista', 'legitymacja rencisty'),
                    ('bezrobotny', 'aktualne zaświadczenie z urzędu pracy o zgłoszeniu do ubezpieczenia zdrowotnego'),
                    ('ubezpieczony dobrowolnie', 'umowa zawarta z NFZ i dokument ZUS potwierdzający zgłoszenie do ubezpieczenia zdrowotnego wraz z aktualnym dowodem opłacenia składki zdrowotnej'),
                    ('członek rodziny ubezp. dowód', 'dowód opłacenia składki zdrowotnej przez osobę, która zgłosiła członków rodziny doubezpieczenia zdrowotnego wraz z kserokopią zgłoszenia (druki: ZUS RMUA + druk ZUSZCNA jeżeli zgłoszenie nastąpiło po 1 lipca 2008 r. (ZUS ZCZA jeżeli zgłoszenie nastąpiło przed dniem 1 lipca 2008 r.)'),
                    ('członek rodziny ubezp. pracodawca', 'aktualne zaświadczenie wydane przez pracodawcę o zgłoszeniu członków rodziny'),
                    ('członek rodziny ubezp. KRUS', 'zaświadczenie z KRUS o ubezpieczeniu członków rodziny'),
                    ('członek rodziny ubezp. legitymacja', 'legitymacja rodzinna z wpisanymi danymi członków rodziny wraz z aktualną datą i pieczątką zakładu pracy lub ZUS'),
                    ('członek rodziny ubezp. emeryt', 'legitymacja emeryta z wpisanymi członkami rodziny podlegającymi ubezpieczeniu, potwierdzająca dokonanie zgłoszenia w dniu 1 stycznia 1999 r. lub później, wraz z aktualnym odcinkiem wypłaty świadczenia – dotyczy tylko KRUS'),
                    ('członek rodziny ubezp. rencista', 'legitymacja rencisty z wpisanymi członkami rodziny podlegającymi ubezpieczeniu, potwierdzająca dokonanie zgłoszenia w dniu 1 stycznia 1999 r. lub później, wraz z aktualnym odcinkiem wypłaty świadczenia – dotyczy tylko KRUS'),
                    ('członek rodziny ubezp. dzieci', 'pomiędzy 18. a 26. rokiem życia – dodatkowo należy przedstawić dokument potwierdzający fakt kontynuacji nauki – np. legitymację szkolną/studencką lub dokument potwierdzający znaczny stopień niepełnosprawności'),
                    ('student po 26', 'zgłoszenie do ubezpieczenia przez uczelnię (druk ZUS ZZA) oraz legitymacja studencka lub doktorancka'),
                    ('nieubezp. spełn. kryt. dochodowe', 'decyzja wójta (burmistrza, prezydenta) gminy właściwej ze względu na miejsce zamieszkania tej osoby'),
                    ('ubezpieczony w UE EFTA', 'poświadczenie wydane przez NFZ – w przypadku zamieszkiwania na terenie RP'),
                    ('ubezpieczony w UE EFTA2', 'karta EKUZ (lub certyfikat ją zastępujący) wydana przez inny niż Polska kraj członkowski UE lub EFTA – w przypadku pobytu na terenie RP'),
                    ('zasiłek chorobowy', 'zaświadczenia z ZUS informujące o wypłacie zasiłku'),)
    insurance_type = models.CharField("Rodzaj zęba", max_length=200, choices=TYPE_CHOICES)
    insurance_number = models.CharField("Nr ubezp.", max_length=100)
    phone = models.CharField("Telefon", max_length=9, blank=True, null=True)
    comment = models.TextField("O pacjencie", blank=True, null=True)
    user = models.OneToOneField(User, verbose_name="User",  blank=True, null=True)
    diseases = models.ManyToManyField(disease, through="patient_diseases")
    
    class Meta:
        verbose_name= "Pacjent"
        verbose_name_plural = "Pacjenci"

    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        return u'Pacjent: %s %s' % (user.first_name, user.last_name)
    
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
    user = models.OneToOneField(User, verbose_name="User")
    last_change = models.DateField("Data")
    
    class Meta:
        verbose_name = "Hasło"
        verbose_name_plural = "Hasła"

    def __unicode__(self):
        return self.last_change