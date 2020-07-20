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
        self.realization_time = None
        self.overtime = None
        self.lack = None
        self.free_day_type = None
        self.worked_day = None

        self.update_values()

    def update_values(self, ):
        self.realization_time = self.calc_realization_time()
        self.overtime = self.calc_overtime()
        self.lack = self.calc_lack()
        self.free_day_type = self.calc_free_day_type()
        self.worked_day = self.is_worked_day()

    def calc_realization_time(self) -> time:
        realization_seconds = self.calc_realization_time_seconds()
        if realization_seconds:
            days = divmod(realization_seconds, 86400)  # Get days (without [0]!)
            hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
            minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
            return time(int(hours[0]), int(minutes[0]))
        return time()

    def calc_realization_time_seconds(self) -> float:
        """
        Difference between leaving time and arrival time
        :return:total_seconds
        """
        if isinstance(self.time_reg, TimeRegistration) and self.time_reg.arrival and self.time_reg.leaving:
            leaving: datetime = datetime(
                    1, 1, 1, self.time_reg.leaving.hour, self.time_reg.leaving.minute
                )

            arrival: datetime = datetime(
                        1, 1, 1, self.time_reg.arrival.hour, self.time_reg.arrival.minute
                    )

            duration: timedelta = leaving - arrival
            return duration.total_seconds()
        return float(0)

    def calc_overtime(self) -> timedelta:
        dif_realize_to_work_sec = self.subtract_realization_time_and_work_time()
        if dif_realize_to_work_sec > 0:
            return timedelta(seconds=dif_realize_to_work_sec)
        return timedelta(seconds=0)

    def calc_lack(self) -> timedelta:
        dif_realize_to_work_sec = self.subtract_realization_time_and_work_time()
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

    def subtract_realization_time_and_work_time(self):
        realization_seconds = self.calc_realization_time_seconds()
        realize_to_work_sec = realization_seconds - self.get_working_hours_seconds()
        return realize_to_work_sec

    def get_working_hours_seconds(self):
        working_hours: int = self.employee.working_hours
        working_seconds = working_hours * 3600
        return working_seconds
