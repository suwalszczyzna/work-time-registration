from django.contrib import admin

from time_registration.models import Employee, Company, TimeRegistration

admin.site.register(Employee)
admin.site.register(Company)


class TimeRegistrationAdmin(admin.ModelAdmin):
    list_display = ('date', 'arrival', 'leaving', 'employee')


admin.site.register(TimeRegistration, TimeRegistrationAdmin)