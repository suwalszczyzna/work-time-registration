from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from free_days_registration.models import FreeDayType, FreeDayRegistration
from time_registration.decorators import employee_login_required
from time_registration.helpers import get_employee_by_user_id
from time_registration.views import index
from .forms import FreeDayRegisterForm


@employee_login_required
def free_days_form_summary_view(request):
    current_user_id = request.user.id
    free_days_registrations = FreeDayRegistration.objects.filter(employee__user_id__exact=current_user_id)

    paginator = Paginator(free_days_registrations, 10)

    page = request.GET.get('page')

    context = {'objects': paginator.get_page(page)}
    return render(request, 'free_days_registration/free_days_form_summary.html', context)


@employee_login_required
def free_days_register_form(request):
    if request.method == "POST":

        form = FreeDayRegisterForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            employee = get_employee_by_user_id(request.user.id)
            start_date = form_data.get('start_date')
            end_date = form_data.get('end_date')
            free_day_type = form_data.get('free_day_type')
            note = form_data.get('note')

            if start_date > end_date:
                messages.error(request, 'Data końca urlopu nie może być mniejsza niż data początkowa')
            else:
                new_free_day = FreeDayRegistration.objects.create(
                    employee_id=employee.id,
                    start_date=start_date,
                    end_date=end_date,
                    free_day_type=free_day_type,
                    note=note
                )
                new_free_day.save()
                form.clean()
                return redirect('home')
    else:
        form = FreeDayRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'free_days_registration/free_days_form.html', context)
