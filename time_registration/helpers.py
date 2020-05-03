from datetime import datetime, timedelta

from time_registration.models import Employee


def is_register_owner(user_id, time_registration):
    employee = get_employee_by_userid(user_id)

    if time_registration.employee.id == employee.id:
        return True
    else:
        return False


def is_employed(user_id):
    employee = get_employee_by_userid(user_id)
    if employee:
        return True
    else:
        return False


def get_employee_by_userid(user_id):
    try:
        employee = Employee.objects.get(user_id__exact=user_id)
    except Employee.DoesNotExist:
        employee = None
    return employee


def plan_leaving_hours(request, time_registration):
    employee = get_employee_by_userid(request.user.id)
    working_hours = employee.working_hours
    plan_time = datetime.combine(time_registration.date, time_registration.arrival) + timedelta(hours=working_hours)
    return plan_time.time()
