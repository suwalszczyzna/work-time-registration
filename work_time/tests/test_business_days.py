from django.test import TestCase
import pytest
from free_days_registration.business_days import number_of_business_days_without_holidays
from datetime import date


class TestWorkingDays(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestWorkingDays, cls).setUpClass()

    def test_error_number_of_business_days_without_holidays(self):
        with pytest.raises(ValueError) as exception_info:
            number_of_business_days_without_holidays(date(2020, 8, 16), date(2020, 8, 10))
        assert "date_from should be earlier than date_to" in str(exception_info.value)

    def test_number_of_business_days_without_holidays(self):
        days = number_of_business_days_without_holidays(date(2020, 8, 10), date(2020, 8, 16))
        assert days == 5

        days = number_of_business_days_without_holidays(date(2020, 8, 15), date(2020, 8, 22))
        assert days == 5
