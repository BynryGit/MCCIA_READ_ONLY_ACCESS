from django.contrib import admin


from django.contrib import admin
from mediaapp import models


# Register your models here.
admin.site.register(models.MCCIALEADERSHIP)
admin.site.register(models.MCCIATeamImage)
admin.site.register(models.MCCIAVideoLinks)
admin.site.register(models.MCCIABanner)
admin.site.register(models.MCCIALinkToShare)


