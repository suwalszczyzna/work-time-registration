from django.urls import path
from .views import free_days_register_form, free_days_form_summary_view

urlpatterns = [
    path('form/', free_days_register_form, name='free-days-form'),
    path('summary/', free_days_form_summary_view, name='free-days-form-summary'),
]