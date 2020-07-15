from mixer.backend.django import mixer
from time_registration.helpers import get_employee_by_user_id, is_register_owner, is_employed, plan_leaving_hours
from time_registration.models import TimeRegistration, Employee
from django.test import TestCase
import pytest
from datetime import datetime, time


@pytest.fixture
def time_registration(db) -> TimeRegistration:
    return mixer.blend(TimeRegistration)


@pytest.fixture
def time_registration2(db) -> TimeRegistration:
    return mixer.blend(TimeRegistration)


@pytest.fixture
def employee(db) -> Employee:
    return mixer.blend(Employee)


@pytest.fixture
def employee2(db) -> Employee:
    return mixer.blend(Employee)


def test_is_register_owner(time_registration, time_registration2):
    user_id: int = time_registration.employee.user.id
    assert is_register_owner(user_id, time_registration)
    assert not is_register_owner(user_id, time_registration2)


def test_get_employee_by_user_id(employee):
    assert get_employee_by_user_id(employee.user.id) == employee


def test_dont_get_employee_by_user_id(employee):
    assert get_employee_by_user_id(0) != employee


def test_false_get_employee_by_user_id(employee, employee2):
    assert get_employee_by_user_id(employee.user.id) != employee2


def test_is_employed(employee):
    assert is_employed(employee.user.id)


def test_is_not_employed(db):
    assert not is_employed(0)


def test_plan_leaving_hours(db):
    time_registration: TimeRegistration = mixer.blend(TimeRegistration, arrival=time(hour=0))
    assert plan_leaving_hours(time_registration) == time(8, 0)
