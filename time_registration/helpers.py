from datetime import datetime, timedelta, time

from time_registration.models import Employee, TimeRegistration


def is_register_owner(user_id, time_registration):
    employee = get_employee_by_user_id(user_id)

    if time_registration.employee.id == employee.id:
        return True
    else:
        return False


def is_employed(user_id):
    employee = get_employee_by_user_id(user_id)
    if employee:
        return True
    else:
        return False


def get_employee_by_user_id(user_id):
    try:
        return Employee.objects.get(user_id__exact=user_id)
    except Employee.DoesNotExist:
        return None


def plan_leaving_hours(time_registration):
    employee = time_registration.employee
    working_hours = employee.working_hours
    plan_date: datetime = datetime.combine(
        time_registration.date, time_registration.arrival
    ) + timedelta(hours=working_hours)

    plan_time: time = time(plan_date.hour, plan_date.minute)
    return plan_time


def plan_leaving_hour_with_brakes(time_registration: TimeRegistration) -> time:
    plan_hours: time = plan_leaving_hours(time_registration)
    _dumb_plan_leaving: datetime = datetime(100, 1, 1, plan_hours.hour, plan_hours.minute)
    result_plan_leaving: datetime = _dumb_plan_leaving + timedelta(minutes=time_registration.brakes)

    return result_plan_leaving.time()


def round_time(dt: datetime, date_delta: timedelta, to='average') -> datetime:
    """
    Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    from:  http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python
    """
    round_to = date_delta.total_seconds()
    seconds = (dt - dt.min).seconds

    if seconds % round_to == 0 and dt.microsecond == 0:
        rounding = (seconds + round_to / 2) // round_to * round_to
    else:
        if to == 'up':
            # // is a floor division, not a comment on following line (like in javascript):
            rounding = (seconds + dt.microsecond/1000000 +
                        round_to) // round_to * round_to
        elif to == 'down':
            rounding = seconds // round_to * round_to
        else:
            rounding = (seconds + round_to / 2) // round_to * round_to

    return dt + timedelta(0, rounding - seconds, - dt.microsecond)


def get_time_registration_by(date_to_row: datetime, employee: Employee):
    time_registrations = TimeRegistration.objects.filter(
        date__month=date_to_row.month,
        date__year=date_to_row.year,
        employee_id=employee.id
    )
    return time_registrations
