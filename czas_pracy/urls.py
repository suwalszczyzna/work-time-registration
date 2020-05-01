from django.contrib import admin
from django.urls import path
from time_registration.views import index, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('', index)
]
