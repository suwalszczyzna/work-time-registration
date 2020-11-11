from datetime import datetime

from django.shortcuts import render

from free_days_registration.helpers import get_free_day_registrations_by
from time_registration.decorators import employee_login_required
from time_registration.helpers import get_employee_by_user_id
from time_registration.models import Employee
from .generators import PdfGenerator, FileNameGenerator
from .models import MonthlyReport
from django.core.handlers.wsgi import WSGIRequest


@employee_login_required
def monthly_report_view(request: WSGIRequest):
    employee: Employee = get_employee_by_user_id(request.user.id)
    free_day_registrations = get_free_day_registrations_by(employee)
    report_date = datetime.now()
    month_report: MonthlyReport = MonthlyReport(free_day_registrations, employee, report_date)

    context = create_context(employee, month_report, report_date)

    if 'download_report' in request.POST:
        file_name = 'raport_{}-{}'.format(context.get('employee'), context.get('report_date'))
        fg = FileNameGenerator(file_name).generate()

        pdf_generator: PdfGenerator = PdfGenerator(
            fg,
            '../templates/reports/monthly_report/monthly_report_pdf.html'
        )

        return pdf_generator.generate(context)
    elif 'apply-date' in request.POST:
        new_report_date_raw = request.POST.get('date-input')
        report_date = datetime.strptime(new_report_date_raw, '%Y-%m-%d')
        month_report = MonthlyReport(free_day_registrations, employee, report_date)
        context = create_context(employee, month_report, report_date)

    return render(request, 'reports/monthly_report/monthly_report.html', context)


def create_context(employee: Employee, month_report: MonthlyReport, report_date: datetime):
    context = {
        'report_date': report_date,
        'report_rows': month_report.report_rows,
        'employee': employee.user.get_full_name(),
        'overtime': month_report.get_overtime(),
        'lack': month_report.get_lack()
    }
    return context
