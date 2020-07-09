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
