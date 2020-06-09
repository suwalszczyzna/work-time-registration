from mixer.backend.django import mixer
import pytest
from time_registration.models import Employee, Company, Brake


@pytest.mark.django_db
class TestModels:
    def test_employee_model(self):
        employee: Employee = mixer.blend('time_registration.Employee')
        assert isinstance(employee, Employee)
        assert employee.__str__() == employee.user.username

    def test_company_model(self):
        company: Company = mixer.blend('time_registration.Company', name='Grapple')
        assert isinstance(company, Company)
        assert company.__str__() == company.name
        assert company.name == 'Grapple'

    def test_brake_minutes_model(self):
        brake: Brake = mixer.blend('time_registration.Brake')
        assert brake.__str__() == '0 min brake'
