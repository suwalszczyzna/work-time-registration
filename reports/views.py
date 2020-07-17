from math import fabs

from django.db.models import QuerySet
from django.shortcuts import render
from datetime import datetime, date, timedelta, time
from free_days_registration.models import FreeDayRegistration
from time_registration.helpers import get_employee_by_user_id
from time_registration.models import TimeRegistration, Employee
from calendar import monthrange


class ReportRowGenerator:
    def __init__(self, _free_day_reg_set: QuerySet, _emp: Employee):
        self.date = None
        self.time_reg = None
        self.free_day_reg_set = _free_day_reg_set
        self.employee = _emp
        self.realization_hour_sec = 0

    def update_row(self, _date: datetime, _time_reg: TimeRegistration):
        self.date = _date
        self.time_reg = _time_reg

    @property
    def realization(self) -> time:
        if isinstance(self.time_reg, TimeRegistration) and self.time_reg.arrival and self.time_reg.leaving:
            duration = datetime(
                1, 1, 1, self.time_reg.leaving.hour, self.time_reg.leaving.minute
            ) - datetime(
                1, 1, 1, self.time_reg.arrival.hour, self.time_reg.arrival.minute
            )
            self.realization_hour_sec = duration.total_seconds()
            days = divmod(self.realization_hour_sec, 86400)  # Get days (without [0]!)
            hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
            minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
            seconds = divmod(minutes[1], 1)
            return time(int(hours[0]), int(minutes[0]))

    @property
    def overtime(self) -> timedelta:
        dif_realize_to_work_sec = self._realize_to_work_sec()
        if dif_realize_to_work_sec > 0:
            return timedelta(seconds=dif_realize_to_work_sec)
        return timedelta(seconds=0)

    @property
    def lack(self) -> timedelta:
        dif_realize_to_work_sec = self._realize_to_work_sec()
        if dif_realize_to_work_sec < 0:
            return timedelta(seconds=dif_realize_to_work_sec)
        return timedelta(seconds=0)

    @property
    def free_day_type(self):
        for fdr in self.free_day_reg_set:
            if fdr.start_date <= self.date <= fdr.end_date:
                return fdr.free_day_type

    def row_generate(self) -> list:
        row_date = self.date.strftime("%d.%m.%Y")
        time_arrival = getattr(self.time_reg, 'arrival', '-')
        time_leaving = getattr(self.time_reg, 'leaving', '-')
        plan_leaving = getattr(self.time_reg, 'plan_leaving', '-')
        brakes = getattr(self.time_reg, 'brakes', '-')

        result = [
            row_date,
            time_arrival,
            time_leaving,
            plan_leaving,
            f'{brakes} min.',
            self.realization,
            self.overtime,
            self.lack,
            self.free_day_type
        ]

        return result

    def _realize_to_work_sec(self):
        working_hours: int = self.employee.working_hours
        working_seconds = working_hours * 3600
        realize_to_work_sec = self.realization_hour_sec - working_seconds
        return realize_to_work_sec


def monthly_report_view(request) -> render:

    employee: Employee = get_employee_by_user_id(request.user.id)
    free_day_registrations = get_free_day_registrations_by(employee)
    report_rows = generate_month_report_rows(datetime.now(), employee, free_day_registrations)

    context = {
        'rows': report_rows
    }
    return render(request, 'reports/monthly_report.html', context)


def generate_month_report_rows(
        report_date: datetime,
        employee: Employee,
        free_day_reg: QuerySet) -> list:

    result = []
    report_row_generator: ReportRowGenerator = ReportRowGenerator(free_day_reg, employee)

    max_day = monthrange(report_date.year, report_date.month)[1]

    for day in range(1, max_day+1):
        _date_to_row: datetime = date(report_date.year, report_date.month, day)

        _time_registrations = get_time_registration_by(_date_to_row, employee)
        _tr: TimeRegistration = _time_registrations.filter(date__exact=_date_to_row).first()

        report_row_generator.update_row(_date_to_row, _tr)
        result.append(report_row_generator.row_generate())
    return result


def get_free_day_registrations_by(employee: Employee):
    free_day_registrations = FreeDayRegistration.objects.filter(
        employee_id=employee.id,
        status=FreeDayRegistration.Status.ACCEPTED,
    )
    return free_day_registrations


def get_time_registration_by(date_to_row: datetime, employee: Employee):
    time_registrations = TimeRegistration.objects.filter(
        date__month=date_to_row.month,
        date__year=date_to_row.year,
        employee_id=employee.id
    )
    return time_registrations
