from django.contrib import admin
from adminapp import models
from membershipapp import models
# Register your models here.


class UserDetailAdmin(admin.ModelAdmin):
	search_fields = ['company__company_name', 'enroll_type', 'user_type', 'member_associate_no', 'membership_year']


class CompanyDetailAdmin(admin.ModelAdmin):
	search_fields = ['company_name', 'company_scale']


class MembershipUserAdmin(admin.ModelAdmin):
	search_fields = ['userdetail__member_associate_no', 'userdetail__company__company_name']	


admin.site.register(models.HOD_Detail)
admin.site.register(models.CompanyDetail, CompanyDetailAdmin)
admin.site.register(models.UserDetail, UserDetailAdmin)
admin.site.register(models.Top3Member)
admin.site.register(models.MembershipInvoice)
admin.site.register(models.PaymentDetails)
admin.site.register(models.MembershipUser, MembershipUserAdmin)
admin.site.register(models.MembershipTypeTrack)
admin.site.register(models.NonMemberDetail)
admin.site.register(models.RenewLetterSchedule)

