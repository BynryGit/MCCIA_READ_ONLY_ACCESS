from django.db import models
import django

from backofficeapp.models import SystemUserProfile
from adminapp.models import City

# Create your models here.

IS_DELETED = (
    (True, True),
    (False, False),
)

LEGAL_STATUS = (
    (0, 'Proprietor'),
    (1, 'Partnership'),
    (2, 'Private Limited'),
    (3, 'Public Limited'),
    (4, 'LLP'),
    (5, 'Other')
)

AWARD_IMAGE_PATH = 'Award_Images'


class AwardFor(models.Model):
    award_for = models.CharField(max_length=50, blank=False, null=False)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.award_for)


class AwardDetail(models.Model):
    award_name = models.CharField(max_length=70, blank=True, null=True)
    awardfor = models.ForeignKey(AwardFor, blank=True, null=True)
    award_content = models.TextField(blank=True, null=True)
    award_nature = models.CharField(max_length=50, blank=True, null=True)
    award_image = models.FileField(upload_to=AWARD_IMAGE_PATH, blank=True, null=True)
    contact_person = models.ForeignKey(SystemUserProfile, blank=True, null=True)
    last_registration_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.award_name)


class AwardRegistration(models.Model):
    awarddetail = models.ForeignKey(AwardDetail, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    concerned_person_name = models.CharField(max_length=80, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    pin_code = models.IntegerField(default=0, blank=True, null=True)
    telephone_no = models.CharField(max_length=25, blank=True, null=True)
    fax_no = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    establish_year = models.IntegerField(default=0, blank=True, null=True)
    org_chief_name = models.CharField(max_length=80, blank=True, null=True)
    org_chief_designation = models.CharField(max_length=50, blank=True, null=True)
    product = models.TextField(blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    product_feature_advantage = models.TextField(blank=True, null=True)
    product_manufacture_date = models.DateField(blank=True, null=True)
    commercial_launch_date = models.DateField(blank=True, null=True)
    to_year_one = models.IntegerField(default=0, blank=True, null=True)
    to_year_two = models.IntegerField(default=0, blank=True, null=True)
    to_year_three = models.IntegerField(default=0, blank=True, null=True)
    profit_year_one = models.IntegerField(default=0, blank=True, null=True)
    profit_year_two = models.IntegerField(default=0, blank=True, null=True)
    profit_year_three = models.IntegerField(default=0, blank=True, null=True)
    to_one = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    to_two = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    to_three = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    profit_one = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    profit_two = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    profit_three = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    person_name = models.CharField(max_length=80, blank=True, null=True)
    first_gen_entp = models.BooleanField(default=False, choices=IS_DELETED)
    commencement_date = models.DateField(blank=True, null=True)
    starting_capital = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    msme_reg_no = models.CharField(max_length=25, blank=True, null=True)
    msme_reg_date = models.DateField(blank=True, null=True)
    legal_status = models.IntegerField(default=5, choices=LEGAL_STATUS)
    no_of_employees = models.IntegerField(default=0, blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    gross_block_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    plant_and_mc_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    net_block_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    patent_registered = models.BooleanField(default=False, choices=IS_DELETED)
    award_recognition = models.TextField(blank=True, null=True)
    certification_list = models.TextField(blank=True, null=True)
    about_yourself = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.company_name)