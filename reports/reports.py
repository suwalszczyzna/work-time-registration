from abc import ABC, abstractmethod
from calendar import monthrange
from datetime import datetime, time, timedelta, date
from math import fabs

from django.db.models import QuerySet

from free_days_registration.models import FreeDayRegistration
from time_registration.helpers import get_time_registration_by
from time_registration.models import Employee, TimeRegistration


class MonthlyReport:

    def __init__(
            self, 
            free_day_registrations: QuerySet,
            emp: Employee,
            report_date: datetime,
    ) -> None:
        self.free_day_registrations = free_day_registrations
        self.emp = emp
        self.report_rows: list = []
        self.report_date: datetime = report_date
        self.generate_rows()

    def generate_rows(self):

        max_day = monthrange(self.report_date.year, self.report_date.month)[1]

        for day in range(1, max_day + 1):
            _date_to_row: datetime = datetime(self.report_date.year, self.report_date.month, day)

            _time_registrations = get_time_registration_by(_date_to_row, self.emp)
            _tr: TimeRegistration = _time_registrations.filter(date__exact=_date_to_row).first()

            monthly_row = MonthlyReportRow(self.free_day_registrations, self.emp, _date_to_row, _tr)
            self.report_rows.append(monthly_row)


class MonthlyReportRow:
    def __init__(self, _free_day_reg_set: QuerySet, _emp: Employee, _date: datetime, _time_reg: TimeRegistration):
        self.date = _date
        self.time_reg = _time_reg
        self.free_day_reg_set = _free_day_reg_set
        self.employee = _emp
        self.realization_hour_sec = None
        self.realization_time = None
        self.overtime = None
        self.lack = None
        self.free_day_type = None
        self.worked_day = None

        self.update_values()

    def update_values(self, ):
        self.reset_values()
        self.overtime = self.calc_overtime()
        self.realization_time = self.calc_realization_time()
        self.lack = self.calc_lack()
        self.free_day_type = self.calc_free_day_type()
        self.worked_day = self.is_worked_day()

    def calc_realization_time(self) -> time:
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
            return time(int(hours[0]), int(minutes[0]))
        return time()

    def calc_overtime(self) -> timedelta:
        dif_realize_to_work_sec = self._realize_to_work_sec()
        if dif_realize_to_work_sec > 0:
            return timedelta(seconds=dif_realize_to_work_sec)
        return timedelta(seconds=0)

    def calc_lack(self) -> timedelta:
        dif_realize_to_work_sec = self._realize_to_work_sec()
        if dif_realize_to_work_sec < 0:
            return timedelta(seconds=fabs(dif_realize_to_work_sec))
        return timedelta(seconds=0)

    def calc_free_day_type(self) -> FreeDayRegistration:
        for fdr in self.free_day_reg_set:
            if fdr.start_date <= self.date.date() <= fdr.end_date:
                return fdr.free_day_type

    def is_worked_day(self):
        _time_arrival = getattr(self.time_reg, 'arrival', None)
        _time_leaving = getattr(self.time_reg, 'leaving', None)
        if _time_arrival and _time_leaving:
            return True
        else:
            return False

    def reset_values(self):
        self.realization_hour_sec = 0

    def _realize_to_work_sec(self):
        _ = self.realization_time
        working_hours: int = self.employee.working_hours
        working_seconds = working_hours * 3600
        realize_to_work_sec = self.realization_hour_sec - working_seconds
        return realize_to_work_sec
