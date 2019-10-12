from django.contrib import admin

# Register your models here.
from massmailingapp import models


class CompanyDetailAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'membership_no']

class PersonDetailAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email', 'extra_email']

class EmailDetailAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email']


admin.site.register(models.CompanyDetail, CompanyDetailAdmin)
admin.site.register(models.PersonDetail, PersonDetailAdmin)
admin.site.register(models.EmailDetail, EmailDetailAdmin)
