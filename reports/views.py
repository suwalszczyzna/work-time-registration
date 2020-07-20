from datetime import datetime

from django.shortcuts import render

from free_days_registration.helpers import get_free_day_registrations_by
from time_registration.decorators import employee_login_required
from time_registration.helpers import get_employee_by_user_id
from time_registration.models import Employee
from .reports import MonthlyReport, Report


@employee_login_required
def monthly_report_view(request):

    employee: Employee = get_employee_by_user_id(request.user.id)
    free_day_registrations = get_free_day_registrations_by(employee)
    report_date = datetime.now()
    month_report: Report = MonthlyReport(free_day_registrations, employee, report_date)
    month_report_rows = month_report.rows()

    context = {
        'report_date': report_date,
        'rows': month_report_rows
    }
    return render(request, 'reports/monthly_report.html', context)
