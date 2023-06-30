from django.contrib import admin

from .models import StoreBusinessHours, StoreTimezone, StoreStatus, Report

class StoreBusinessHoursAdmin(admin.ModelAdmin):
    pass

admin.site.register(StoreBusinessHours, StoreBusinessHoursAdmin)

class StoreTimezoneAdmin(admin.ModelAdmin):
    pass

admin.site.register(StoreTimezone, StoreTimezoneAdmin)

class StoreStatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(StoreStatus, StoreStatusAdmin)

class ReportAdmin(admin.ModelAdmin):
    pass

admin.site.register(Report, ReportAdmin)