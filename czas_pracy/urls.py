from django.contrib import admin
from django.urls import path
from time_registration.views import index, register, login_page, logout_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', index, name='home')
]
