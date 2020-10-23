from django.contrib import admin
from django.urls import path, include
from time_registration import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('correction/<str:pk>', views.correction, name='correction'),
    path('free_days/', include('free_days_registration.urls'), name='free-days'),
    path('unemployed/', views.unemployed_warning_page, name='unemployed-warning-page'),
    path('report/', include('reports.urls'), name='reports'),
    path('', views.index, name='home')
]
