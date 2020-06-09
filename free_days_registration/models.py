from django.db import models
from django.utils import timezone
from time_registration.models import Employee


class FreeDayType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


STATUS = (
    ('pending', 'W toku'),
    ('accepted', 'Zaakceptowany'),
    ('rejected', 'Odrzucony')
)


class FreeDayRegistration(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    free_day_type = models.ForeignKey(FreeDayType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    create_date = models.DateField(default=timezone.now)
    note = models.CharField(max_length=4000, default='')
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    def __str__(self):
        return "{0} dni, typ urlopu: {1}".format(self.num_of_days, self.free_day_type)

    @property
    def num_of_days(self):
        delta_time = self.end_date - self.start_date
        return delta_time.days + 1
