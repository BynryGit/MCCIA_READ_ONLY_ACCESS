from django.contrib import admin
from eventsapp import models


# Register your models here.
admin.site.register(models.EventType)
admin.site.register(models.EventDetails)
admin.site.register(models.EventRegistration)
admin.site.register(models.EventParticipantUser)
admin.site.register(models.EventBannerImage)
admin.site.register(models.EventSpecialAnnouncement)
admin.site.register(models.EventSponsorImage)
admin.site.register(models.EventParticipantReportTable)
admin.site.register(models.PromoCode)


