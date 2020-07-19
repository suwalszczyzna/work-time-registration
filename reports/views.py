from math import fabs

from django.db.models import QuerySet
from django.shortcuts import render
from datetime import datetime, date, timedelta, time

from .reports import MonthlyReport, Report

from free_days_registration.helpers import get_free_day_registrations_by
from free_days_registration.models import FreeDayRegistration
from time_registration.helpers import get_employee_by_user_id
from time_registration.models import TimeRegistration, Employee
from calendar import monthrange


def monthly_report_view(request):

    employee: Employee = get_employee_by_user_id(request.user.id)
    free_day_registrations = get_free_day_registrations_by(employee)
    month_report: Report = MonthlyReport(free_day_registrations, employee, datetime.now())
    month_report_rows = month_report.rows()

    context = {
        'rows': month_report_rows
    }
    return render(request, 'reports/monthly_report.html', context)
