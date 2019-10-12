from django.contrib import admin
from adminapp import models
# Register your models here.

class MembershipSlabAdmin(admin.ModelAdmin):
    list_display = ('id', 'slab', 'enroll_type','slab_type','membershipCategory_id','applicableTo','is_deleted')
    list_filter = ('slab', 'enroll_type','slab_type','membershipCategory_id','applicableTo','is_deleted')
    search_fields = ('id', 'slab', 'enroll_type','slab_type','membershipCategory_id','applicableTo')


admin.site.register(models.Committee)
admin.site.register(models.TaskForce)
admin.site.register(models.SlabCriteria)
admin.site.register(models.MembershipCategory)
admin.site.register(models.MembershipSlab,MembershipSlabAdmin)
admin.site.register(models.MembershipDescription)
admin.site.register(models.IndustryDescription)
admin.site.register(models.LegalStatus)
admin.site.register(models.Country)
admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.Location)
admin.site.register(models.Hall_Functioning_Equipment)
admin.site.register(models.Hall_detail_list)
admin.site.register(models.Hall_pricing)
admin.site.register(models.Servicetax)
admin.site.register(models.MembershipDetail)
admin.site.register(models.NameSign)

