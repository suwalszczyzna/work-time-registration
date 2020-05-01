from django.contrib import admin

from time_registration.models import Employee, Company, TimeRegistration


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'working_hours')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Company)


class TimeRegistrationAdmin(admin.ModelAdmin):
    list_display = ('date', 'arrival', 'leaving', 'employee')


admin.site.register(TimeRegistration, TimeRegistrationAdmin)