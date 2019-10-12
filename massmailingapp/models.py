import django
from django.db import models

# Create your models here.
from Paymentapp.models import IS_DELETED
from adminapp.models import IndustryDescription
from eventsapp.models import EventDetails
from membershipapp.models import COMAPANY_SCALE, ENROLL_TYPE, UserDetail, CompanyDetail as MMCompanyDetail, \
    NonMemberDetail


class CompanyDetail(models.Model):
    userdetail = models.ForeignKey(UserDetail, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_scale = models.CharField(max_length=2, choices=COMAPANY_SCALE, default="MR")
    industrydescription = models.ManyToManyField(IndustryDescription, blank=True, related_name='industrydescription')
    gst = models.CharField(max_length=50, blank=True, null=True)
    enroll_type = models.CharField(max_length=2, choices=ENROLL_TYPE, default="CO")
    is_member = models.BooleanField(choices=IS_DELETED, default=False)
    membership_no = models.CharField(max_length=30, blank=True, null=True)
    is_mccia = models.BooleanField(choices=IS_DELETED, default=False)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.company_name)


class PersonDetail(models.Model):
    companydetail = models.ForeignKey(CompanyDetail, blank=True, null=True, on_delete=models.CASCADE)
    eventdetail = models.ManyToManyField(EventDetails, blank=True)
    # event_attended = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=80, blank=True, null=True)
    extra_email = models.TextField(blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    cellno = models.CharField(max_length=50, blank=True, null=True)
    hash_tag = models.TextField(blank=True, null=True)
    is_member = models.BooleanField(choices=IS_DELETED, default=False)
    is_mccia_person = models.BooleanField(choices=IS_DELETED, default=False)

    created_by = models.CharField(max_length=100, blank=True, null=False)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.name))


class EmailDetail(models.Model):
    companydetail = models.ForeignKey(MMCompanyDetail, blank=True, null=True)
    nonmemberdetail = models.ForeignKey(NonMemberDetail, blank=True, null=True)
    userdetail = models.ForeignKey(UserDetail, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=80, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    cellno = models.CharField(max_length=50, blank=True, null=True)
    hash_tag = models.TextField(blank=True, null=True)
    is_member = models.BooleanField(choices=IS_DELETED, default=False)
    is_mccia_person = models.BooleanField(choices=IS_DELETED, default=False)
    interested_area = models.TextField(blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=False)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.email))