from mixer.backend.django import mixer
from time_registration.helpers import get_employee_by_user_id, is_register_owner, is_employed, plan_leaving_hours
from time_registration.models import TimeRegistration
import pytest
import datetime


@pytest.mark.django_db
class TestHelpers:
    def test_is_register_owner(self):
        time_registration: TimeRegistration = mixer.blend('time_registration.TimeRegistration')
        time_registration2: TimeRegistration = mixer.blend('time_registration.TimeRegistration')
        user_id: int = time_registration.employee.user.id
        assert is_register_owner(user_id, time_registration)
        assert not is_register_owner(user_id, time_registration2)

    def test_get_employee_by_user_id(self):
        employee = mixer.blend('time_registration.Employee')
        assert get_employee_by_user_id(employee.user.id) == employee

    def test_dont_get_employee_by_user_id(self):
        employee = mixer.blend('time_registration.Employee')
        assert get_employee_by_user_id(0) != employee

    def test_false_get_employee_by_user_id(self):
        employee = mixer.blend('time_registration.Employee')
        employee2 = mixer.blend('time_registration.Employee')
        assert get_employee_by_user_id(employee.user.id) != employee2

    def test_is_employed(self):
        employee = mixer.blend('time_registration.Employee')
        assert is_employed(employee.user.id)

    def test_is_not_employed(self):
        assert not is_employed(0)

    def test_plan_leaving_hours(self):
        time = datetime.time(hour=0)
        time_registration: TimeRegistration = mixer.blend('time_registration.TimeRegistration', arrival=time)
        assert plan_leaving_hours(time_registration).time() == datetime.time(8, 0)
