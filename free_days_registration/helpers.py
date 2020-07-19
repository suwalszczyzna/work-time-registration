from free_days_registration.models import FreeDayRegistration
from time_registration.models import Employee


def get_free_day_registrations_by(employee: Employee):
    free_day_registrations = FreeDayRegistration.objects.filter(
        employee_id=employee.id,
        status=FreeDayRegistration.Status.ACCEPTED,
    )
    return free_day_registrations
