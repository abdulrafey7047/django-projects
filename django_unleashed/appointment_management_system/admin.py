from django.contrib import admin

from .models import Doctor, Patient


class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'firstname', 'lastname']})
    ]


admin.site.register(Doctor)
admin.site.register(Patient, PatientAdmin)
