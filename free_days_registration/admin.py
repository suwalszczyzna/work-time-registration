from django.contrib import admin
from free_days_registration.models import FreeDayRegistration, FreeDayType

admin.site.register(FreeDayType)


class FreeDayRegistrationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'free_day_type', 'start_date', 'end_date', 'num_of_days', 'create_date', 'status')


admin.site.register(FreeDayRegistration, FreeDayRegistrationAdmin)