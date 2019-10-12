from django.contrib import admin
from awardsapp import models

# Register your models here.


admin.site.register(models.AwardFor)
admin.site.register(models.AwardDetail)
admin.site.register(models.AwardRegistration)
