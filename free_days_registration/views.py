from django.contrib import messages
from django.shortcuts import render, redirect
from free_days_registration.models import FreeDayType, FreeDayRegistration
from time_registration.decorators import employee_login_required
from time_registration.helpers import get_employee_by_user_id
from .forms import FreeDayRegisterForm

@employee_login_required
def free_days_form_view(request):
    free_days_types = FreeDayType.objects.all()

    if request.method == "POST":
        employee = get_employee_by_user_id(request.user.id)
        type_id_form = request.POST.get('proposal', 1)
        free_day_type_obj = FreeDayType.objects.get(pk=type_id_form)

        start_date = request.POST.get('start-absense')
        end_date = request.POST.get('end-absense')
        note = request.POST.get('more-info')

        if start_date and end_date:
            new_free_days_registration = FreeDayRegistration.objects.create(
                employee_id=employee.id,
                free_day_type_id=free_day_type_obj.id,
                start_date=start_date,
                end_date=end_date,
                note=note
            )
            new_free_days_registration.save()
            return redirect('home')
        else:
            messages.error(request, 'Daty są niepoprawne')

    context = {
        'free_days_types': free_days_types
    }

    return render(request, 'new_free_days_form.html', context)


@employee_login_required
def free_days_form_summary_view(request):
    current_user_id = request.user.id
    free_days_registrations = FreeDayRegistration.objects.filter(employee__user_id__exact=current_user_id)
    context = {'free_days_registrations': free_days_registrations}
    return render(request, 'free_days_form_summary.html', context)


@employee_login_required
def free_days_form_boot_view(request):
    form = FreeDayRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'free_days_form.html', context)
