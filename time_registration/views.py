from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date, datetime, time, timedelta

from .forms import CreateUserForm
from .models import TimeRegistration, Employee


def get_employee_by_userid(user_id):
    return Employee.objects.get(user_id__exact=user_id)


def plan_leaving_hours(request, time_registration):
    employee = get_employee_by_userid(request.user.id)
    working_hours = employee.working_hours
    plan_time = datetime.combine(time_registration.date, time_registration.arrival) + timedelta(hours=working_hours)
    return plan_time.time()


@login_required(login_url='login')
def index(request):
    plan_leave_time = ''
    time_registration: TimeRegistration = TimeRegistration.objects.filter(
        employee__user_id__exact=request.user.id,
        date__exact=timezone.datetime.date(datetime.now())).first()

    if time_registration:
        plan_leave_time = plan_leaving_hours(request, time_registration)
    context = {
        'time_registration': time_registration,
        'plan_leaving_time': plan_leave_time
    }
    if 'arrival' in request.POST:
        employee = get_employee_by_userid(request.user.id)
        new_time_registration = TimeRegistration.objects.create(arrival=timezone.datetime.time(datetime.now()),
                                                                employee_id=employee.id)
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


def correction(request, pk):
    time_registration = TimeRegistration.objects.get(pk=pk)

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


def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
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