from django.contrib import admin
from .models import Customer, WashService, Appointment

class BaseAdmin(admin.ModelAdmin):
    readonly_fields=('created_at', 'updated_at')


admin.site.register(Customer, BaseAdmin)
admin.site.register(WashService, BaseAdmin)
admin.site.register(Appointment, BaseAdmin)
