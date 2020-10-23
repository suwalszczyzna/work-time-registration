from django.urls import path, include
from .views import monthly_report_view

urlpatterns = [
    path('monthly/', monthly_report_view, name='monthly-report'),
]
