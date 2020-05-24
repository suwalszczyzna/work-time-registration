from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from .forms import CreateUserForm
from .helpers import plan_leaving_hours, get_employee_by_userid, is_register_owner
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
        employee = get_employee_by_userid(request.user.id)
        new_time_registration = TimeRegistration.objects.create(arrival=timezone.datetime.time(datetime.now()),
                                                                employee_id=employee.id)
        new_time_registration.plan_leaving = plan_leaving_hours(new_time_registration)
        new_time_registration.save()
        return redirect('home')
    if 'add_short_brake' in request.POST:
        print('add_short_brake')
    if 'go_home' in request.POST:
        time_registration.leaving = timezone.datetime.time(datetime.now())
        time_registration.save()
        return redirect('home')
    return render(request, 'panel.html', context)


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
    return render(request, 'register.html', context)


@employee_login_required
def correction(request, pk):
    time_registration = get_object_or_404(TimeRegistration, pk=pk)

    if not is_register_owner(request.user.id, time_registration):
        return redirect('home')

    if request.method == "POST":
        if 'save' in request.POST:
            arrival = request.POST.get('arrival')
            leaving = request.POST.get('leaving')
            if arrival:
                time_registration.arrival = arrival
            if leaving:
                time_registration.leaving = leaving
            time_registration.save()
        elif 'delete' in request.POST:
            time_registration.delete()
        return redirect('home')

    context = {'time_registration': time_registration}
    return render(request, 'correction.html', context)


def add_brake(request, pk):
    time_registration = get_object_or_404(TimeRegistration, pk=pk)
    if request.method == 'POST':
        minutes = 0
        if 'five-minutes' in request.POST:
            minutes = 5
        elif 'ten-minutes' in request.POST:
            minutes = 10
        elif 'fifteen-minutes' in request.POST:
            minutes = 15
        time_registration.brakes += minutes
        time_registration.plan_leaving = datetime.combine(
            time_registration.date, time_registration.plan_leaving) + \
            timedelta(minutes=time_registration.brakes)
        time_registration.save()
        return redirect('home')
    context = {}
    return render(request, 'add_brake.html', context)


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
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')
