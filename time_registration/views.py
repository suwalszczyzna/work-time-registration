from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned
import datetime

from .forms import CreateUserForm
from .models import TimeRegistration


@login_required(login_url='login')
def index(request):
    time_registration = TimeRegistration.objects.filter(employee__user_id__exact=request.user.id,
                                                        date__exact=datetime.datetime.date(timezone.now()))\
                                                .first()

    context = {'time_registration': time_registration}
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