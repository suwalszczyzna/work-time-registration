from django.contrib import admin
from django.urls import path
from time_registration import views
from free_days_registration.views import free_days_form_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('correction/<str:pk>', views.correction, name='correction'),
    path('add_brake/<str:pk>', views.add_brake, name='add-brake'),
    path('free_days_form/', free_days_form_view, name='free-days-form'),
    path('', views.index, name='home')
]