from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from .forms import CreateUserForm
from .models import TimeRegistration, Employee
from .decorators import employee_login_required


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


@employee_login_required
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
