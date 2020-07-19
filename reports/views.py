from datetime import datetime

from django.shortcuts import render

from free_days_registration.helpers import get_free_day_registrations_by
from time_registration.helpers import get_employee_by_user_id
from time_registration.models import Employee
from .reports import MonthlyReport, Report


def monthly_report_view(request):

    employee: Employee = get_employee_by_user_id(request.user.id)
    free_day_registrations = get_free_day_registrations_by(employee)
    month_report: Report = MonthlyReport(free_day_registrations, employee, datetime.now())
    month_report_rows = month_report.rows()

    context = {
        'rows': month_report_rows
    }
    return render(request, 'reports/monthly_report.html', context)
