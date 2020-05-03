from django.contrib.auth.decorators import user_passes_test, login_required

from time_registration.views import is_employed


def employee_login_required(view_func):
    emp_login_required = user_passes_test(lambda u: True if is_employed(u.id) else False, login_url='login')
    decorated_view_func = login_required(emp_login_required(view_func), login_url='login')
    return decorated_view_func
