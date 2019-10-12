
import django
# Create your models here.

from django.db import models
from adminapp.models import Hall_detail_list,Hall_pricing,Location,Country,City
# from adminapp.models import Location,Country,City
from membershipapp.models import UserDetail
from backofficeapp.models import SystemUserProfile

HALL_IMAGES_PATH = 'HallImage'

IS_DELETED = (
    (True, True),
    (False, False),
)

EQUIPMENT_SPECIFICATON = (
    ('Charges_for_use_within_Primises', 'Charges_for_use_within_Primises'),
    ('Charges_for_use_outside_MCCIA_Primises', 'Charges_for_use_outside_MCCIA_Primises'),
)


LOCATION_STATUS = (
    (True, True),
    (False, False),
)

PAYMENT_METHOD = (
    (0, 'Offline'),
    (1, 'Online'),
)

OFFLINE_PAYMENT_METHOD = (
    (0, 'Cheque'),
    (1, 'Cash'),
    (2, 'NEFT'),
    (3, 'Deposit'),
)

PASSPORT_COPY = (
    ('YES', 'YES'),
    ('NO', 'NO'),
)

HOLIDAY_STATUS = (
    (0, 'Active'),
    (1, 'Inactive'),
    (2, 'Deleted'),
)
HOLIDAY_TYPE = (
    (0, 'MCCIA Holiday'),
    (1, 'National Holiday'),    
)

PAYMENT_STATUS = (
    (0, 'Cancelled'),
    (1, 'Paid'),
    (2, 'Online Pending'),
    (3, 'Offline Pending'),
    (4, 'Spot Booking Pending'),
    (5, 'MCCIA Booking Pending'),
    (6, 'Confirmed'),
    (7, 'Settled'),
    (8, 'Pending'),
    (9, 'Partial'),
    (10, 'Not Paid'),
    (11, 'Failed'),
    (12, 'Initiated'),
)
BOOKING_STATUS =(
    (0, 'Cancelled'),
    (1, 'Paid'),
    (2, 'Online Pending'),
    (3, 'Offline Pending'),
    (4, 'Spot Booking Pending'),
    (5, 'MCCIA Booking Pending'),
    (6, 'Confirmed'),
    (7, 'Settled'),
    (8, 'Pending'),
    (9, 'Accepted'),
    (10, 'Rejected'),
)
BOOKING_FOR = (
    (0, 'Internal'),
    (1, 'Member'),
    (2, 'Non-Member'),
)

CANCELLATION_TYPE = (
    (0, 'User'),
    (1, 'MCCIA')
)

DEPOSIT_STATUS = (
    (0, 'Retained'),
    (1, 'Refund'),
)

REFUND_STATUS = (
    (0, 'Not Initiated'),
    (1, 'Initiated'),
    (2, 'Refunded'),
)


class Hallbooking_company_detail(models.Model):
    company_individual_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=150, blank=True)
    contact_person = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    tel_r = models.CharField(max_length=50, blank=True, null=True)
    tel_o = models.CharField(max_length=50, blank=True, null=True)
    std_code = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=90, blank=True)
    event_nature = models.CharField(max_length=50, blank=True)
    from_date = models.DateField(default=django.utils.timezone.now,blank=True)
    to_date = models.DateField(default=django.utils.timezone.now,blank=True)
    member = models.ForeignKey(UserDetail, blank=True, null=True)
    total_rent = models.CharField(max_length=20, blank=True, null=True, default=0)
    total_payable = models.CharField(max_length=20, blank=True, null=True, default=0)
    deposit = models.CharField(max_length=20, blank=True, null=True, default=0)
    gst = models.CharField(max_length=20, blank=True, null=True, default=0)
    payment_method = models.CharField(max_length=20, default='Offline', blank=True, null=True, choices=PAYMENT_METHOD)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.company_individual_name)


class Hall_booking_detail(models.Model):
    hall_detail = models.ForeignKey(Hall_detail_list, blank=True, null=True)
    hall_pricing = models.ForeignKey(Hall_pricing, blank=True, null=True)
    Hallbooking_company_detail = models.ForeignKey(Hallbooking_company_detail, blank=True, null=True)
    booking_from_date = models.DateTimeField(default=django.utils.timezone.now)
    booking_to_date = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.hall_detail.hall_name)+ '_'+ str(self.booking_from_date))



class HallLocation(models.Model):

    city = models.ForeignKey(City, blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=True)
    contact_person1 = models.ForeignKey(SystemUserProfile, blank=True, null=True, related_name='contact_person3')
    contact_person2 = models.ForeignKey(SystemUserProfile, blank=True, null=True, related_name='contact_person4')
    terms_condition = models.CharField(max_length=100, blank=True, null=True)

    hall_rent_on_holiday = models.FloatField(blank=True, null=True)
    deposit_holiday_factor = models.FloatField(blank=True, null=True)

    email = models.EmailField(max_length=100, blank=True, null=True)
    deposit = models.FloatField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    meta_title = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keyphrases = models.TextField(blank=True, null=True)

    priority = models.IntegerField(blank=True, null=True)
    from_hour = models.CharField(max_length=50, blank=True, null=True)
    to_hour = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    from_time = models.TimeField(max_length=50, blank=True, null=True)
    to_time = models.TimeField(max_length=50, blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.location)


class HallFunctioningEquipment(models.Model):
  equipment_name = models.CharField(max_length=300)
  created_by = models.CharField(max_length=100, blank=True, null=True)
  updated_by = models.CharField(max_length=100, blank=True, null=True)
  created_date = models.DateTimeField(default=django.utils.timezone.now)
  updated_date = models.DateTimeField(blank=True, null=True)
  is_active = models.BooleanField(choices=IS_DELETED, default=True)
  is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

  def __unicode__(self):
      return unicode(self.equipment_name)


class HallInterest(models.Model):

    hall_location = models.ForeignKey(HallLocation, blank=True, null=True)
    add_location = models.CharField(max_length=100, blank=True, null=True)
    hall_name = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    contact_no = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)




class HallSpecialAnnouncement(models.Model):

    hall_location = models.ForeignKey(HallLocation, blank=True, null=True)
    announcement = models.CharField(max_length=500, blank=False, null=True)
    created_by = models.CharField(max_length=80, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)


class HallDetail(models.Model):
    hall_location = models.ForeignKey('HallLocation', blank=True, null=True)

    hall_name = models.CharField(max_length=75, blank=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    capacity = models.IntegerField(default=50)
    seating_style = models.CharField(max_length=20, blank=True)

    facility = models.TextField(blank=True, null=True)
    hall_image = models.ImageField(upload_to=HALL_IMAGES_PATH, null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    extra_pre_hour = models.CharField(max_length=10, blank=True)
    extra_hour = models.CharField(max_length=10, blank=True)
    extra_member_price = models.IntegerField(default=50)
    extra_nonmember_price = models.IntegerField(default=50)

    booking_start_time = models.TimeField(blank=True, null=True)
    booking_end_time = models.TimeField(blank=True, null=True)

    hall_merge = models.CharField(max_length=100, blank=True, null=True)
    is_merge = models.BooleanField(choices=IS_DELETED, default=False)

    hall_equipment = models.ManyToManyField(HallFunctioningEquipment)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_video = models.BooleanField(choices=IS_DELETED, default=False)
    is_open_for_online = models.BooleanField(choices=IS_DELETED, default=True)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.hall_name))


class Holiday(models.Model):
    hall_location = models.ForeignKey(HallLocation, blank=True, null=True)
    hall_detail = models.ForeignKey(HallDetail,blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    holiday_date = models.DateField(blank=True, null=True)
    holiday_date_to = models.DateField(blank=True, null=True)
    holiday_status = models.IntegerField(choices=HOLIDAY_STATUS, default=8)
    holiday_type = models.IntegerField(choices=HOLIDAY_TYPE, default=0)
    is_booking_available = models.BooleanField(choices=IS_DELETED, default=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)    
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.holiday_date))


class HallEquipment(models.Model):

    hall_detail = models.ForeignKey(HallDetail, blank=True, null=True)
    hall_functioning_equipment = models.ForeignKey(HallFunctioningEquipment, blank=True, null=True)
    member_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    non_member_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)


class HallPricing(models.Model):
    hall_detail = models.ForeignKey(HallDetail,blank=True, null=True)
    hours = models.CharField(max_length=10, blank=True)
    member_price = models.IntegerField(default=50)
    nonmember_price = models.IntegerField(default=50)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.hall_detail.hall_name))


class HallCancelPolicy(models.Model):
    day_range = models.CharField(max_length=10, blank=True, null=True)
    charges = models.DecimalField(max_digits=4, decimal_places=0, default=0, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.day_range))


# Deposit retaining/ Blacklisting of Member/ Non member, Maintaining track of every user for auto populating Hall booking field

class UserTrackDetail(models.Model):
    member = models.ForeignKey(UserDetail, blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    contact_person = models.CharField(max_length=70, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    tel_r = models.CharField(max_length=50, blank=True, null=True)
    tel_o = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=90, blank=True, null=True)
    gst = models.CharField(max_length=50, blank=True, null=True)

    deposit_available = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    deposit_status = models.IntegerField(choices=DEPOSIT_STATUS, default=0, blank=True, null=True)
    deposit_remark = models.CharField(max_length=250, blank=True, null=True)
    refund_status = models.IntegerField(choices=REFUND_STATUS, default=0, blank=True, null=True)

    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(default=django.utils.timezone.now)
    is_blacklisted = models.BooleanField(choices=IS_DELETED, default=False)
    blacklist_remark = models.CharField(max_length=250, blank=True, null=True)
    blacklisted_date = models.DateField(blank=True, null=True)
    blacklisted_by = models.CharField(max_length=80, blank=True, null=True)
    reactivated_date = models.DateField(blank=True, null=True)
    reactivated_remark = models.CharField(max_length=250, blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        # return unicode(str(self.id) + '_' + str(self.hall_detail.hall_name)+ '_'+ str(self.booking_from_date))
        return unicode(str(self.id))


class UserTrackDepositDetail(models.Model):
    user_track = models.ForeignKey(UserTrackDetail, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    deposit_remark = models.CharField(max_length=250, blank=True, null=True)
    cheque_no = models.CharField(max_length=10, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    bank_name = models.CharField(max_length=30, blank=True, null=True)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id))


class HallBooking(models.Model):
    member = models.ForeignKey(UserDetail, blank=True, null=True)
    user_track = models.ForeignKey(UserTrackDetail, blank=True, null=True)
    system_user_profile = models.ForeignKey(SystemUserProfile, blank=True, null=True)
    
    booking_no = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    gst_no = models.CharField(max_length=20, blank=True, null=True)
    from_date = models.DateField(default=django.utils.timezone.now,blank=True)
    to_date = models.DateField(default=django.utils.timezone.now,blank=True)

    total_rent = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    first_total_rent_for_reference = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    discounted_total_rent = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    is_discount = models.BooleanField(choices=IS_DELETED, default=False)

    tds = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    deposit_status = models.IntegerField(choices=DEPOSIT_STATUS, blank=True, null=True)
    is_deposit_through_cheque = models.BooleanField(choices=IS_DELETED, default=False)

    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    discount_per = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    gst_tax = models.CharField(max_length=20, blank=True, null=True)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_payable = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    payment_method = models.IntegerField(default=0, choices=PAYMENT_METHOD)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=8)
    # booking_status = models.IntegerField(choices=BOOKING_STATUS, default=8)
    booking_status = models.IntegerField(choices=BOOKING_STATUS, default=8)
    booking_for = models.IntegerField(choices=BOOKING_FOR, default=2)

    extra_pre_hour  = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_post_hour  = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_hour_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_broken_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_facility_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    total_cancellation_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    # added by sp 17sep18
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    bill_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    bill_date = models.DateTimeField(blank=True, null=True)
    bill_no = models.CharField(max_length=50, blank=True, null=True)
    total_services = models.CharField(max_length=20, blank=True, null=True)
    shexcesspayment = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    shexcesspayment_desc = models.TextField(blank=True, null=True)
    educess = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    seducess = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    invoice_total_rent = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    
    created_by = models.CharField(max_length=300, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_completed = models.BooleanField(choices=IS_DELETED, default=False)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id)+ '_' + str(self.name))


class HallBookingDepositDetail(models.Model):
    hall_booking = models.ForeignKey(HallBooking, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    cheque_no = models.CharField(max_length=10, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    bank_name = models.CharField(max_length=30, blank=True, null=True)

    customer_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=90, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    date_of_return = models.DateTimeField(blank=True, null=True)
    deposit_status = models.IntegerField(choices=DEPOSIT_STATUS, blank=True, null=True)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id))


class HallBookingDetail(models.Model):
    hall_location = models.ForeignKey(HallLocation, blank=True, null=True)
    hall_detail = models.ForeignKey(HallDetail, blank=True, null=True)
    hall_booking = models.ForeignKey(HallBooking, blank=True, null=True, on_delete=models.CASCADE)
    pi_no = models.CharField(max_length=15,blank=True,null=True)
    booking_detail_no = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    contact_person = models.CharField(max_length=70, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    tel_r = models.CharField(max_length=50, blank=True, null=True)
    tel_o = models.CharField(max_length=50, blank=True, null=True)
    std_code = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=90, blank=True, null=True)
    event_nature = models.CharField(max_length=50, blank=True, null=True)
    booking_from_date = models.DateTimeField(default=django.utils.timezone.now)
    booking_to_date = models.DateTimeField(default=django.utils.timezone.now)
    booking_from_date_for_reference = models.DateTimeField(default=django.utils.timezone.now)
    booking_to_date_for_reference = models.DateTimeField(default=django.utils.timezone.now)

    slot = models.CharField(max_length=5, blank=True, null=True)
    member_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    non_member_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    member_extra_hour_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    non_member_extra_hour_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    # hall_rent_on_holiday = models.FloatField(blank=True, null=True)
    # deposit_holiday_factor = models.FloatField(blank=True, null=True)
    extra_pre_hour = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_hour = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_hour_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    #Broken Charge Field
    extra_broken_detail = models.CharField(max_length=30, blank=True, null=True)
    extra_broken_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    total_rent = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    first_total_rent_for_reference = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    discount_percent = models.CharField(max_length=20, blank=True, null=True)
    facility_detail = models.TextField(blank=True, null=True)
    total_facility_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    # booking_status = models.IntegerField(choices=BOOKING_STATUS, default=8)
    # Cancellation Policy Added SB 17 Dec 18
    is_cancelled = models.BooleanField(choices=IS_DELETED, default=False)
    cancellation_date = models.DateField(blank=True, null=True)
    cancellation_type = models.IntegerField(default=0, choices=CANCELLATION_TYPE)
    cancellation_percent = models.DecimalField(max_digits=5, decimal_places=0, default=0, blank=True, null=True)
    cancellation_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    cancellation_gst = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    cancellation_remark = models.CharField(max_length=100, blank=True, null=True)

    booking_status = models.IntegerField(choices=BOOKING_STATUS, default=8)

    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        # return unicode(str(self.id) + '_' + str(self.hall_detail.hall_name)+ '_'+ str(self.booking_from_date))
        return unicode(str(self.id) + '_'+ str(self.booking_from_date))


class BookingDetailHistory(models.Model):
    hall_booking_detail = models.ForeignKey(HallBookingDetail, blank=True, null=True, on_delete=models.CASCADE)

    total_rent = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    discount_percent = models.CharField(max_length=20, blank=True, null=True)
    extra_pre_hour = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_hour = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_hour_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    extra_broken_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    facility_detail = models.TextField(blank=True, null=True)
    total_facility_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        # return unicode(str(self.id) + '_' + str(self.hall_detail.hall_name)+ '_'+ str(self.booking_from_date))
        return unicode(str(self.id))


class HallCheckAvailability(models.Model):
    hall_detail = models.ForeignKey(HallDetail, blank=True, null=True)
    hall_booking_detail = models.ForeignKey(HallBookingDetail, blank=True, null=True, on_delete=models.CASCADE)
    booking_from_date = models.DateTimeField(default=django.utils.timezone.now)
    booking_to_date = models.DateTimeField(default=django.utils.timezone.now)
    booking_from_time = models.TimeField(blank=True, null=True)
    booking_to_time = models.TimeField(blank=True, null=True)
    booking_status = models.IntegerField(choices=BOOKING_STATUS, default=8)

    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.hall_detail.hall_name))


class HallPaymentDetail(models.Model):
    hall_booking = models.ForeignKey(HallBooking, blank=True, null=True, on_delete=models.CASCADE)
    payment_mode = models.IntegerField(default=0, choices=PAYMENT_METHOD)
    offline_payment_by = models.CharField(max_length=20, default='Cheque', blank=True, null=True, choices=OFFLINE_PAYMENT_METHOD)
    payable_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    tds_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    is_tds = models.BooleanField(choices=IS_DELETED, default=False)

    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=10)
    payment_date = models.DateTimeField(blank=True, null=True)

    cheque_no = models.CharField(max_length=10, blank=True, null=True)
    cheque_date = models.DateField(blank=True, null=True)
    bank_name = models.CharField(max_length=30, blank=True, null=True)
    bounce_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    bounce_cheque_remark = models.CharField(max_length=250, blank=True, null=True)
    neft_id = models.CharField(max_length=30, blank=True, null=True)
    cash_no = models.CharField(max_length=30, blank=True, null=True)  # added by sp 17sep18
    transaction_no = models.CharField(max_length=30, blank=True, null=True)  # added by sp 17sep18

    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id))