from mixer.backend.django import mixer
import pytest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from time_registration.models import TimeRegistration, Employee
from time_registration.views import index, register


class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()

    def test_index_user_is_not_employee(self):
        path = reverse(index)
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = index(request)
        assert response.status_code == 302
        assert response.url == "/login/?next=/"

    def test_index_user_is_employee(self):
        path = reverse(index)
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        mixer.blend(Employee, user=request.user)

        response = index(request)
        assert response.status_code == 200

    def test_register_view(self):
        path = reverse(register)
        request = RequestFactory().get(path)
        response = register(request)
        assert response.status_code == 200