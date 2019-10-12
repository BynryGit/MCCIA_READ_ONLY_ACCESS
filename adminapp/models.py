
import django
from django.db import models
from backofficeapp.models import SystemUserProfile
# Create your models here.


IS_DELETED = (
    (True, True),
    (False, False),
)
HALL_EQUIPMENT_SCALE = (
    ('WF', 'WIFI'),
    ('VD', 'Video'),
    ('AD', 'Audio'),
    ('PH', 'Phone'),
)
APPLICABLE_TO= (
    ('Associates', 'Associates'),
    ('Members', 'Members'),
    ('Individual', 'Individual'),
)

HALL_IMAGES_PATH = 'HallImage'

DESIGNATION = (
    (0, 'President'),
    (1, 'Director General'),
)

FILE_PATH ='SignFolder'


#previos_id:used to store the id of existing mccia strcture

class TaskForce(models.Model):
    task_force = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.task_force)

class Committee(models.Model):
    committee = models.CharField(max_length=150, blank=True)
    task_force = models.ForeignKey(TaskForce, blank=True, null=True)
    chairman1_name = models.CharField(max_length=150, blank=True)
    chairman1_company = models.CharField(max_length=150, blank=True)
    chairman1_designation = models.CharField(max_length=150, blank=True)
    chairman1_address = models.CharField(max_length=300, blank=True)
    chairman1_email = models.CharField(max_length=150, blank=True)
    chairman1_mobile = models.CharField(max_length=35, blank=True)
    chairman1_telephone = models.CharField(max_length=35, blank=True)
    chairman1_profile_link = models.CharField(max_length=250, blank=True)
    chairman2_name = models.CharField(max_length=150, blank=True)
    chairman2_company = models.CharField(max_length=150, blank=True)
    chairman2_designation = models.CharField(max_length=150, blank=True)
    chairman2_address = models.CharField(max_length=300, blank=True)
    chairman2_email = models.CharField(max_length=150, blank=True)
    chairman2_mobile = models.CharField(max_length=35, blank=True)
    chairman2_telephone = models.CharField(max_length=35, blank=True)
    chairman2_profile_link = models.CharField(max_length=250, blank=True)
    contact_person1 = models.ForeignKey(SystemUserProfile, blank=True, null=True , related_name = 'committee_contact_person1')
    contact_person2 = models.ForeignKey(SystemUserProfile, blank=True, null=True, related_name = 'committee_contact_person2')
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.committee)


class MembershipDetail(models.Model):
    code = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.description)


class MembershipCategory(models.Model):
    enroll_type = models.CharField(max_length=150, blank=True,null=True)
    category_enroll_type = models.CharField(max_length=150, blank=True,null=True)
    membership_code = models.CharField(max_length=150, blank=True)#used to store the previos_id
    membership_category = models.CharField(max_length=150, blank=True)
    membership_type = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.membership_category)


class SlabCriteria(models.Model):
    slab_criteria= models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.slab_criteria)


class MembershipSlab(models.Model):
    code = models.CharField(max_length=100, blank=True,null=True)#used to store the previos_id
    slab = models.CharField(max_length=150, blank=True,null=True)
    enroll_type = models.CharField(max_length=150, blank=True,null=True)
    slab_type = models.CharField(max_length=150, blank=True,null=True)
    membershipCategory = models.ForeignKey(MembershipCategory, blank=True, null=True)
    applicableTo = models.CharField(max_length=15, choices=APPLICABLE_TO, default="Associates")
    annual_fee = models.CharField(max_length=150, blank=True,null=True)
    entrance_fee = models.CharField(max_length=150, blank=True,null=True)
    cr3 = models.ForeignKey(SlabCriteria, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.code) + '-' + str(self.slab))


class MembershipDescription(models.Model):
    previous_id = models.CharField(max_length=100, blank=True)
    membership_description = models.CharField(max_length=150, blank=True)
    code = models.CharField(max_length=20, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.membership_description)


class IndustryDescription(models.Model):
    previous_id = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.description)


class LegalStatus(models.Model):
    previous_id = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.description)


class Country(models.Model):
    country_name = models.CharField(max_length=50, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.country_name)


class State(models.Model):
    state_name = models.CharField(max_length=50, blank=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.state_name)


class City(models.Model):
    city_name = models.CharField(max_length=50, default=None)
    state = models.ForeignKey(State, blank=True, null=True)
    created_by = models.CharField(max_length=500, blank=True, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.city_name))


class Location(models.Model):
    location = models.CharField(max_length=100, blank=True)
    city = models.ForeignKey(City, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.location)

class Hall_Functioning_Equipment(models.Model):
  equipment_name = models.CharField(max_length=300)
  created_by = models.CharField(max_length=100, blank=True, null=True)
  updated_by = models.CharField(max_length=100, blank=True, null=True)
  created_date = models.DateTimeField(default=django.utils.timezone.now)
  updated_date = models.DateTimeField(blank=True, null=True)
  is_active = models.BooleanField(choices=IS_DELETED, default=True)
  is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

  def __unicode__(self):
      return unicode(self.equipment_name)

class Hall_detail_list(models.Model):
    hall_name = models.CharField(max_length=40, blank=True)
    hall_address = models.CharField(max_length=100, blank=True)
    capacity = models.IntegerField(default=50)
    seating_style = models.CharField(max_length=20, blank=True)
    amenities = models.CharField(max_length=150, blank=True)
    hall_image = models.ImageField(upload_to=HALL_IMAGES_PATH, null=True, blank=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    hall_equipment = models.ManyToManyField(Hall_Functioning_Equipment)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.hall_name)


class Hall_pricing(models.Model):
    hours = models.CharField(max_length=10, blank=True)
    eight_member_price = models.IntegerField(default=50)
    eight_nonmember_price = models.IntegerField(default=50)
    four_member_price = models.IntegerField(default=50)
    four_nonmember_price = models.IntegerField(default=50)
    two_member_price = models.IntegerField(default=50)
    two_nonmember_price = models.IntegerField(default=50)
    hall_detail = models.ForeignKey(Hall_detail_list, blank=True, null=True)
    deposit_holiday = models.IntegerField(default=50)
    deposit_working = models.IntegerField(default=50)
    extra_hour = models.CharField(max_length=10, blank=True)
    extra_member_price = models.IntegerField(default=50)
    extra_nonmember_price = models.IntegerField(default=50)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.hall_detail.hall_name))

TAX_TYPE = (
    (0, 'GST'),
    (1, 'IGST'),
 ) 

class Servicetax(models.Model):
    amount=models.CharField(max_length=20, blank=True,default=10)
    tax=models.CharField(max_length=20, blank=True)
    cgst=models.CharField(max_length=20, blank=True)
    sgst=models.CharField(max_length=20, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    tax_type = models.IntegerField(choices=TAX_TYPE,default=0)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.amount))


class NameSign(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    sign = models.FileField(upload_to=FILE_PATH,null=True, blank=True)
    designation = models.IntegerField(choices=DESIGNATION,default=0)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.id)