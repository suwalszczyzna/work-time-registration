from django.shortcuts import render
from datetime import datetime
from free_days_registration.models import FreeDayRegistration
from time_registration.models import TimeRegistration


def monthly_report_view(request) -> render:
    date: datetime = datetime.now()
    user_id = request.user.id

    time_registrations = TimeRegistration.objects.filter(
        date__month=date.month
    )

    free_day_registrations = FreeDayRegistration.objects.filter(
        employee__user_id__exact=user_id,
        status=FreeDayRegistration.Status.ACCEPTED,
    )

    context = {
        'time_registrations': time_registrations,
        'free_day_registrations': free_day_registrations
    }
    return render(request, 'reports/monthly_report.html', context)
