from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect

from .helpers import is_employed


def employee_login_required(view_func):
    emp_login_required = user_passes_test(lambda u: True if is_employed(u.id) else False, login_url='login')
    decorated_view_func = login_required(emp_login_required(view_func), login_url='login')
    return decorated_view_func


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func