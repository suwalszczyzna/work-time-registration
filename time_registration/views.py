from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from .forms import CreateUserForm, CorrectionForm
from .helpers import plan_leaving_hours, get_employee_by_user_id, is_register_owner, combine_plan_leaving_date
from .models import TimeRegistration, Employee
from .decorators import employee_login_required, unauthenticated_user


@employee_login_required
def index(request):
    time_registration: TimeRegistration = TimeRegistration.objects.filter(
        employee__user_id__exact=request.user.id,
        date__exact=timezone.datetime.date(datetime.now())).first()

    context = {
        'time_registration': time_registration
    }
    if 'arrival' in request.POST:
        employee = get_employee_by_user_id(request.user.id)
        new_time_registration = TimeRegistration.objects.create(
            arrival=timezone.datetime.time(datetime.now()),
            employee_id=employee.id
        )
        new_time_registration.plan_leaving = plan_leaving_hours(new_time_registration)
        new_time_registration.save()
        return redirect('home')

    if 'add_break' in request.POST:
        minutes_brake = request.POST.get('minutesOfBreak', 0)
        time_registration.brakes += int(minutes_brake)
        time_registration.plan_leaving = combine_plan_leaving_date(time_registration)
        time_registration.save()
        return redirect('home')

    if 'go_home' in request.POST:
        time_registration.leaving = timezone.datetime.time(datetime.now())
        time_registration.save()
        return redirect('home')
    return render(request, 'time_registration/panel.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Pomyślnie założono konto: ' + username)
            form.clean()
    context = {'form': form}
    return render(request, 'base/register.html', context)


@employee_login_required
def correction(request, pk):
    time_registration = get_object_or_404(TimeRegistration, pk=pk)
    if not is_register_owner(request.user.id, time_registration):
        return redirect('home')

    if request.method == "POST":

        if 'save' in request.POST:
            arrival = request.POST.get('arrival')
            leaving = request.POST.get('leaving')

            if (arrival and leaving) and arrival > leaving:
                messages.error(request, 'Godzina wyjścia nie może być późniejsza niż przyjście')
            else:
                if arrival:
                    time_registration.arrival = arrival
                if leaving:
                    time_registration.leaving = leaving

                time_registration.save()
                return redirect('home')
        elif 'delete' in request.POST:
            time_registration.delete()
            return redirect('home')

    context = {
        'time_registration': time_registration,
    }
    return render(request, 'time_registration/correction_form.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nazwa lub hasło jest niepoprawne')

    context = {}
    return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def unemployed_warning_page(request):
    return render(request, 'base/not_employee_warning_page.html', context={})
