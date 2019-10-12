from django.contrib import admin
from hallbookingapp import models


class HallBookingAdmin(admin.ModelAdmin):
	search_fields = ['booking_no', 'name']


class HallBookingDetailAdmin(admin.ModelAdmin):
	search_fields = ['hall_booking__booking_no', 'hall_booking__name', 'pi_no']		

admin.site.register(models.HallLocation)
admin.site.register(models.HallFunctioningEquipment)
admin.site.register(models.HallEquipment)
admin.site.register(models.HallInterest)
admin.site.register(models.Holiday)
admin.site.register(models.HallSpecialAnnouncement)
admin.site.register(models.HallDetail)
admin.site.register(models.HallPricing)
admin.site.register(models.HallBooking, HallBookingAdmin)
admin.site.register(models.HallBookingDepositDetail)
admin.site.register(models.HallBookingDetail, HallBookingDetailAdmin)
admin.site.register(models.HallCheckAvailability)
admin.site.register(models.HallPaymentDetail)
admin.site.register(models.BookingDetailHistory)
admin.site.register(models.HallCancelPolicy)
admin.site.register(models.UserTrackDepositDetail)
admin.site.register(models.UserTrackDetail)