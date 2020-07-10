from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class Brake(models.Model):
    minutes = models.IntegerField(default=0, blank=False, null=False)
    added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} min brake'.format(self.minutes)


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='nazwa')
    email = models.EmailField()
    boss = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name='szef')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('firma')
        verbose_name_plural = _('firmy')


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='użytkownik')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='firma')
    working_hours = models.IntegerField(default=8, verbose_name='ilość godzin dziennie')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('pracownik')
        verbose_name_plural = _('pracownicy')


class TimeRegistration(models.Model):
    arrival = models.TimeField(null=True, blank=True, verbose_name='rozpoczęcie pracy')
    leaving = models.TimeField(null=True, blank=True, verbose_name='zakonczenie pracy')
    plan_leaving = models.TimeField(null=True, blank=True, verbose_name='planowana godzina zakończenia')
    date = models.DateField(default=timezone.now, verbose_name='data rejestracji')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False, verbose_name='pracownik')
    brakes = models.IntegerField(default=0, verbose_name='przerwy (min)')

    class Meta:
        verbose_name = _('rejestracja czasu pracy')
        verbose_name_plural = _('rejestracja czasu pracy')

