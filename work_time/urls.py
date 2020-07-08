from django.contrib import admin
from django.urls import path
from time_registration import views
from free_days_registration.views import free_days_form_summary_view, free_days_register_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('correction/<str:pk>', views.correction, name='correction'),
    path('free_days_form/', free_days_register_form, name='free-days-form'),
    path('free_days_form_summary/', free_days_form_summary_view, name='free-days-form-summary'),
    path('unemployed/', views.unemployed_warning_page, name='unemployed-warning-page'),
    path('', views.index, name='home')
]
