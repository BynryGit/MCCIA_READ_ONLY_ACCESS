from django.contrib import admin
from backofficeapp import models
from django.contrib.admin.models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    list_filter = ['user']


admin.site.register(models.UserPrivilege)
admin.site.register(models.UserRole)
admin.site.register(models.Department)
admin.site.register(models.Designation)
admin.site.register(models.SystemUserProfile)
admin.site.register(LogEntry, LogEntryAdmin)
