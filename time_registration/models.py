from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    boss = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class TimeRegistration(models.Model):
    arrival = models.TimeField(null=True, blank=True)
    leaving = models.TimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now())
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False)

