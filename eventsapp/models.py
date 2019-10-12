import django
from django.db import models
from membershipapp.models import UserDetail, NonMemberDetail, CompanyDetail
from adminapp.models import Committee
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallDetail

# Create your models here.
IS_DELETED = (
    (True, True),
    (False, False),
)

PAYMENT_MODE = (
    ('Online', 'Online'),
    ('Offline', 'Offline'),
)

EVENT_MODE = (
    (0, 'Open To All'),
    (1, 'On Payment'),
    (2, 'By Invitation'),
 )

EVENT_STATUS = (
    (0, 'Active'),
    (1, 'Inactive'),
    (2, 'Deleted'),
 )
EVENT_STAT = (
    (0, 'OK'),
    (1, 'CANCEL'),
    (2, 'POSTPONE')
)
VIEW_STATUS = (
    (0, 'OFF'),
    (1, 'ON'),
 )  

ONLINE_PAYMENT = (
    (0, 'OFF'),
    (1, 'ON'),
 )    
EVENT_PRIORITY = (
    (0, 'No Priority'),
    (1, 'Priority 1'),
    (2, 'Priority 2'),
    (3, 'Priority 3'),
)
PAYMENT_STATUS = (
    (0,'Pending'),
    (1,'Inprogress'),
    (2,'Initiated'),
    (3,'Failed'),
    (4,'Paid'),
)

ENROLL_TYPE = (
    ('CO', 'Company'),
    ('IN', 'Individual'),
)

PAYMENT_METHOD = (
    (0,'Cash'),
    (1,'Cheque'),
    (2,'NEFT'),
)

BANNER_TYPE = (
    (0, 'Event Banner'),
    (1, 'Sponsor Banner'),
)

REGISTER_STATUS=(
    (0,'Active'),
    (1,'Inactive'),
    (2,'Deleted')
)

EVENT_LEVEL = (
    (0,'Local'),
    (1,'State'),
    (2,'National'),
    (3,'International')
)

EVENT_SPONSORED =(
    (0,'False'),
    (1,'True')
)

MEDIUM_SOURCE=(
    (0,'Email from MCCIA'),
    (1,'Website'),
    (2,'Social Media'),
    (3,'Referred by Other')
)

SOCIAL_MEDIUM_SOURCE=(
    (0,'Facebook'),
    (1,'LinkedIn'),
    (2,'WhatsApp')
)

GST_OPTION= (
    ('UP', 'Under Process'),
    ('AP', 'Applicable'),
    ('NA', 'Not Applicable'),

)
FILE_PATH ='EventFiles/banners'


class EventType(models.Model):
    event_type = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.event_type)


class EventDetails(models.Model):
    event_title = models.CharField(max_length=200, blank=False, null=True)
    event_description_indetails = models.TextField(blank=True, null=True)
    to_whom_description = models.TextField(blank=True, null=True)
    organised_by = models.TextField(blank=True, null=True)
    event_objective = models.TextField(blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    registration_start_date = models.DateTimeField(blank=True, null=True)
    registration_end_date = models.DateTimeField(blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    hall_details = models.ForeignKey(HallDetail, blank=True, null=True)
    other_location_address = models.TextField(blank=True, null=True)
    member_charges = models.IntegerField(default=0,blank=True, null=True)
    non_member_charges = models.IntegerField(default=0,blank=True, null=True)
    other_charges_name = models.CharField(max_length=100,blank=True,null=True)
    other_charges_amount = models.IntegerField(default=0,blank=True, null=True)
    event_no = models.CharField(max_length=20, blank=True, null=True)

    is_early_bird = models.BooleanField(choices=IS_DELETED, default=False)
    early_member_charges = models.IntegerField(default=0,blank=True, null=True)
    early_non_member_charges = models.IntegerField(default=0,blank=True, null=True)
    early_bird_date = models.DateTimeField(blank=True, null=True)

    discount_1 = models.CharField(max_length=50,blank=True,null=True)
    discount_2 = models.CharField(max_length=50,blank=True,null=True)
    discount_3 = models.CharField(max_length=50,blank=True,null=True)
    expected_members = models.IntegerField(default=0,blank=True, null=True)
    expected_nonmembers = models.IntegerField(default=0,blank=True, null=True)
    expected_freemembers = models.IntegerField(default=0,blank=True, null=True)
    expected_sponsored_members = models.IntegerField(default=0,blank=True, null=True)
    expected_capacity = models.IntegerField(default=0,blank=True, null=True)
    organising_committee = models.ForeignKey(Committee, blank=True, null=True)
    contact_person1 = models.ForeignKey(SystemUserProfile, blank=True, null=True , related_name = 'contact_person1')
    contact_person2 = models.ForeignKey(SystemUserProfile, blank=True, null=True, related_name = 'contact_person2')
    priority = models.IntegerField(default=0, choices=EVENT_PRIORITY)
    event_type = models.ForeignKey(EventType, blank=True, null=True)
    event_mode = models.IntegerField(default=0,choices=EVENT_MODE)
    online_payment = models.IntegerField(choices=ONLINE_PAYMENT,default=0)
    meta_title = models.TextField(blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keyphrases = models.TextField(blank=True, null=True)
    event_status = models.IntegerField(default=0, choices=EVENT_STATUS)
    view_status = models.IntegerField(default=0, choices=VIEW_STATUS)
    current_event_stat = models.IntegerField(default=0, choices=EVENT_STAT)
    is_event_sponsored = models.IntegerField(choices=EVENT_SPONSORED, default=0)
    event_level = models.IntegerField(blank=True, null=True, choices=EVENT_LEVEL)
    created_by = models.CharField(max_length=80, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)


class EventSponsorImage(models.Model):
    event_id = models.ForeignKey(EventDetails, blank=True, null=True)
    document_files = models.FileField(upload_to=FILE_PATH, max_length=500, null=True, blank=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    creation_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.id)


class EventBannerImage(models.Model):
    event_detail_id = models.ForeignKey(EventDetails, blank=True, null=True)
    document_files = models.FileField(upload_to=FILE_PATH, max_length=500, null=True, blank=True)
    banner_type = models.IntegerField(default=0, choices=BANNER_TYPE)
    creation_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.id)        


class EventRegistration(models.Model):
    event = models.ForeignKey(EventDetails, blank=True, null=True)
    reg_no = models.CharField(max_length=100, blank=True, null=True)
    name_of_organisation = models.CharField(max_length=100, blank=False, null=True)
    enroll_type = models.CharField(max_length=2, choices=ENROLL_TYPE, default="CO")

    address = models.TextField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=100, blank=False, null=True)
    contact_person_number = models.CharField(max_length=50, blank=False, null=True)
    contact_person_number_two = models.CharField(max_length=50, blank=False, null=True)    
    office_contact = models.CharField(max_length=50, blank=False, null=True)    
    contact_person_email_id = models.CharField(max_length=100, blank=False, null=True)
    no_of_participant = models.IntegerField(blank=False, null=True, default=1)
    total_amount = models.FloatField(default=0, blank=True, null=True)

    total_fees_amount = models.FloatField(default=0, blank=True, null=True)
    extra_gst_amount = models.FloatField(default=0, blank=True, null=True)
    total_discount_amount = models.FloatField(default=0, blank=True, null=True)

    payment_mode = models.CharField(max_length=100, choices=PAYMENT_MODE, default='Online')#models.Enum(max_length=100, choices=PAYMENT_MODE, default='Online')
    payment_method = models.IntegerField(choices=PAYMENT_METHOD, blank=True, null=True)#models.Enum(max_length=100, choices=PAYMENT_MODE, default='Online')
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=0)#models.Enum(max_length=100, choices=PAYMENT_MODE, default='Online')
    cash_receipt_no = models.CharField(max_length=50, blank=True, null=True)
    cheque_no = models.CharField(max_length=10, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=False, null=True)
    cheque_date = models.DateField(blank=False, null=True)
    trasanction_id = models.CharField(max_length=50, blank=True, null=True)
    tds_amount = models.FloatField(default=0, blank=True, null=True)

    register_status = models.IntegerField(choices=REGISTER_STATUS, default=0)#models.Enum(max_length=100, choices=PAYMENT_MODE, default='Online')
    user_details = models.ForeignKey(UserDetail, blank=True, null=True)
    nonmemberdetail = models.ForeignKey(NonMemberDetail, blank=True, null=True)
    companydetail = models.ForeignKey(CompanyDetail, blank=True, null=True)
    gst =  models.CharField(max_length=50, blank=True, null=True)
    gst_in = models.CharField(max_length=2,choices=GST_OPTION,default="NA")
    pan = models.CharField(max_length=12, blank=True, null=True)
    is_member = models.BooleanField(choices=IS_DELETED, default=False)
    is_other = models.BooleanField(choices=IS_DELETED, default=False)
    is_invitee = models.BooleanField(choices=IS_DELETED, default=False)
    is_attendees = models.BooleanField(choices=IS_DELETED, default=True)

    medium_source = models.IntegerField(choices=MEDIUM_SOURCE, default=0)
    social_medium_source = models.IntegerField(choices=SOCIAL_MEDIUM_SOURCE, default=0)

    created_by = models.CharField(max_length=80, blank=False, null=True)
    updated_by = models.CharField(max_length=50, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)

    def __unicode__(self):
        return unicode(self.id)


# class EventRegistration(models.Model):
#     event = models.ForeignKey(EventDetails, blank=True, null=True)
#     reg_no = models.CharField(max_length=100, blank=True, null=True)
#     name_of_organisation = models.CharField(max_length=100, blank=False, null=True)
#     address = models.TextField(blank=True, null=True)
#     contact_person_name = models.CharField(max_length=100, blank=False, null=True)
#     contact_person_number = models.CharField(max_length=50, blank=False, null=True)    
#     office_contact = models.CharField(max_length=50, blank=False, null=True)    
#     contact_person_email_id = models.CharField(max_length=100, blank=False, null=True)
#     no_of_participant = models.IntegerField(blank=False, null=True, default=1)
#     total_amount = models.FloatField(default=0, blank=True, null=True)
#     total_fees_amount = models.FloatField(default=0, blank=True, null=True)
#     extra_gst_amount = models.FloatField(default=0, blank=True, null=True)
#     total_discount_amount = models.FloatField(default=0, blank=True, null=True)
#     payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=0)
#     register_status = models.IntegerField(choices=REGISTER_STATUS, default=0)
#     user_details = models.ForeignKey(UserDetail, blank=True, null=True)
#     gst =  models.CharField(max_length=50, blank=True, null=True)
#     gst_in = models.CharField(max_length=2,choices=GST_OPTION,default="NA")
#     pan = models.CharField(max_length=12, blank=True, null=True)
#     is_member = models.BooleanField(choices=IS_DELETED, default=False)
#     created_by = models.CharField(max_length=80, blank=False, null=True)
#     created_on = models.DateTimeField(default=django.utils.timezone.now)
#     is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
#     is_active = models.BooleanField(choices=IS_DELETED, default=True)

#     def __unicode__(self):
#         return unicode(self.id)


class EventParticipantUser(models.Model):
    event_user = models.ForeignKey(EventRegistration, blank=True, null=True)
    event_user_name = models.CharField(max_length=100, blank=False, null=True)
    designation = models.CharField(max_length=100, blank=False, null=True)
    department = models.CharField(max_length=100, blank=False, null=True)
    contact_no = models.CharField(max_length=50, blank=False, null=True)    
    email_id = models.CharField(max_length=100, blank=False, null=True)
    created_by = models.CharField(max_length=80, blank=False, null=True)
    updated_by = models.CharField(max_length=50, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_invitee = models.BooleanField(choices=IS_DELETED, default=False)
    is_attendees = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    register_status = models.IntegerField(choices=REGISTER_STATUS, default=0)

    def __unicode__(self):
        return unicode(self.id)


class PromoCode(models.Model):
    event_details = models.ForeignKey(EventDetails, blank=True, null=True)
    promo_code = models.CharField(max_length=150, blank=True,null=True)
    for_whom = models.CharField(max_length=250, blank=True,null=True)
    percent_discount = models.CharField(max_length=50,blank=True,null=True)
    discounted_amount = models.IntegerField(default=0,blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)


class EventSpecialAnnouncement(models.Model):
    announcement = models.CharField(max_length=500, blank=False, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=80, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)

#table for reporting only
class EventParticipantReportTable(models.Model):
    event_registration = models.ForeignKey(EventRegistration, blank=True, null=True)
    reg_no = models.CharField(max_length=100, blank=True, null=True)
    name_of_organisation = models.CharField(max_length=100, blank=False, null=True)
    address = models.CharField(max_length=200, blank=False, null=True)
    contact_person_name = models.CharField(max_length=100, blank=False, null=True)
    contact_person_number = models.CharField(max_length=50, blank=False, null=True)    
    designation = models.CharField(max_length=100, blank=False, null=True)
    department = models.CharField(max_length=100, blank=False, null=True)
    contact_person_email_id = models.CharField(max_length=100, blank=False, null=True)
    is_member = models.BooleanField(choices=IS_DELETED, default=False)
    created_by = models.CharField(max_length=80, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)
