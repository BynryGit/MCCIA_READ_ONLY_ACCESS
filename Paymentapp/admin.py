from django.contrib import admin
from Paymentapp import models
# Register your models here.

admin.site.register(models.PaymentTransaction)
admin.site.register(models.PendingTransaction)
admin.site.register(models.EventPaymentTransaction)
admin.site.register(models.HallPaymentTransaction)
admin.site.register(models.MembershipPaymentTransaction)