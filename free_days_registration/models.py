from django.db import models
from django.utils import timezone
from time_registration.models import Employee
from django.utils.translation import ugettext_lazy as _


class FreeDayType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FreeDayRegistration(models.Model):

    class Status(models.IntegerChoices):
        PENDING = 1, _('W toku')
        ACCEPTED = 2, _('Zaakceptowany')
        REJECTED = 3, _('Odrzucony')

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='pracownik')
    free_day_type = models.ForeignKey(FreeDayType, on_delete=models.CASCADE, verbose_name='typ urlopu')
    start_date = models.DateField(verbose_name='data od')
    end_date = models.DateField(verbose_name='data do')
    create_date = models.DateField(default=timezone.now, verbose_name='data złożenia wniosku')
    note = models.CharField(max_length=4000, null=True, blank=True, verbose_name='notatka')
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING, verbose_name='status')

    def __str__(self):
        return "{0} dni, typ urlopu: {1}".format(self.num_of_days, self.free_day_type)

    @property
    def num_of_days(self):
        delta_time = self.end_date - self.start_date
        return delta_time.days + 1

    @property
    def status_name(self):
        return self.Status.labels[self.status-1]

    class Meta:
        verbose_name = _("wniosek urlopowy")
        verbose_name_plural = _("wnioski urlopowe")
