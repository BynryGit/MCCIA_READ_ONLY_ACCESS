
import django
from adminapp.models import Country,State,City,LegalStatus,MembershipCategory,MembershipSlab,MembershipDescription,IndustryDescription
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

IS_DELETED = (
    (True, True),
    (False, False),
)

COMAPANY_SCALE = (
    ('MR', 'Micro'),
    ('SM', 'Small'),
    ('MD', 'Medium'),
    ('LR', 'Large'),
)

GST_OPTION= (
    ('UP', 'Under Process'),
    ('AP', 'Applicable'),
    ('NA', 'Not Applicable'),

)

MEMBERSHIP_TYPE = (
    ('NM', 'Non Member'),
    ('MM', 'Member'),
)
ENROLL_TYPE = (
    ('CO', 'Company'),
    ('IN', 'Individual'),
)


MEMBER_ASSOCIATION_TYPE = (
    ('Member', 'Member'),
    ('Associate', 'Associate'),
    ('Life Membership','Life Membership'),
    ('I','I')
)
PAYMENT_TYPE = (
    ('Cheque', 'Cheque'),
    ('Cash', 'Cash'),
    ('NEFT', 'NEFT'),
    ('Online', 'Online'),
)

PAYMENT_STATUS = (
    ('Paid', 'Paid'),
    ('UnPaid', 'UnPaid'),
    ('Partial', 'Partial'),
    ('Advance', 'Advance'),
)

PAYMENT_METHOD = (
    ('Online Pending', 'Online Pending'),
    ('Offline Pending', 'Offline Pending'),
    ('Confirmed', 'Confirmed'),
    ('Failed', 'Failed'),
    ('Deactivate', 'Deactivate'),
)

INVOICE_FOR = (
    ('NEW', 'NEW'),
    ('RENEW', 'RENEW'),
    ('RE-ASSOCIATE', 'RE-ASSOCIATE'),
)

RENEWAL_STATUS = (
    ('NOT_STARTED', 'NOT_STARTED'),
    ('STARTED', 'STARTED'),
    ('COMPLETED', 'COMPLETED')
)

AREA_OF_EXPERTIES =(
    (0,'unknown'),
    (1,'Engineer'),
    (2,'CA'),
    (3,'Doctors'),
    (4,'Consultant'),
    (5,'Marketing Professional'),
    (6,'Valuers'),
    (7,'Individual Finance Brokers'),
    (8,'Real Estate Broker'),
    (9,'Lawyers Solicitors'),
    (10,'Management Consultant'),
    (11,'Trainer'),
    (12,'Project Consultants'),
    (13,'Others')
)

TURNOVER_RANGE = (
    (0, '0-1'),
    (1, '1-5'),
    (2, '5-25'),
    (3, '25-100'),
    (4, '100-500'),
    (5, '500+'),
)

EMPLOYEE_RANGE = (
    (0, '0-10'),
    (1, '10-100'),
    (2, '100-500'),
    (3, '500-1000'),
    (4, '1000+'),
)

TYPE = (
    (0, 'Manual Letter'),
    (1, 'Schedule'),
    (2, 'Automate Letter'),
    (3, 'Membership Schedule'),
)

MAIL_SENT_STATUS = (
    (0, 'Not Sent'),
    (1, 'Sent'),
    (2, 'Failed'),
    (3, 'Schedule'),
)

FILE_PATH = 'Renewal_Schedule'

class HOD_Detail(models.Model):
    hr_name = models.CharField(max_length=50, blank=True, null=True)
    hr_contact = models.CharField(max_length=50, blank=True, null=True)
    hr_email = models.CharField(max_length=80, blank=True, null=True)
    finance_name = models.CharField(max_length=50, blank=True, null=True)
    finance_contact = models.CharField(max_length=50, blank=True, null=True)
    finance_email = models.CharField(max_length=80, blank=True, null=True)
    marketing_name = models.CharField(max_length=50, blank=True, null=True)
    marketing_contact = models.CharField(max_length=50, blank=True, null=True)
    marketing_email = models.CharField(max_length=80, blank=True, null=True)
    IT_name = models.CharField(max_length=50, blank=True, null=True)
    IT_contact = models.CharField(max_length=50, blank=True, null=True)
    IT_email = models.CharField(max_length=80, blank=True, null=True)
    corp_rel_name = models.CharField(max_length=50, blank=True, null=True)
    corp_rel_contact = models.CharField(max_length=50, blank=True, null=True)
    corp_rel_email = models.CharField(max_length=80, blank=True, null=True)
    tech_name = models.CharField(max_length=80, blank=True, null=True)
    tech_contact = models.CharField(max_length=80, blank=True, null=True)
    tech_email = models.CharField(max_length=80, blank=True, null=True)
    rnd_name = models.CharField(max_length=80, blank=True, null=True)
    rnd_contact= models.CharField(max_length=80, blank=True, null=True)
    rnd_email = models.CharField(max_length=80, blank=True, null=True)
    exim_name = models.CharField(max_length=80, blank=True, null=True)
    exim_contact = models.CharField(max_length=80, blank=True, null=True)
    exim_email = models.CharField(max_length=80, blank=True, null=True)
    stores_name = models.CharField(max_length=80, blank=True, null=True)
    stores_contact = models.CharField(max_length=80, blank=True, null=True)
    stores_email = models.CharField(max_length=80, blank=True, null=True)
    purchase_name = models.CharField(max_length=80, blank=True, null=True)
    purchase_contact = models.CharField(max_length=80, blank=True, null=True)
    purchase_email = models.CharField(max_length=80, blank=True, null=True)
    production_name = models.CharField(max_length=80, blank=True, null=True)
    production_contact = models.CharField(max_length=80, blank=True, null=True)
    production_email = models.CharField(max_length=80, blank=True, null=True)
    quality_name = models.CharField(max_length=80, blank=True, null=True)
    quality_contact = models.CharField(max_length=80, blank=True, null=True)
    quality_email = models.CharField(max_length=80, blank=True, null=True)
    supply_chain_name = models.CharField(max_length=80, blank=True, null=True)
    supply_chain_contact = models.CharField(max_length=80, blank=True, null=True)
    supply_chain_email = models.CharField(max_length=80, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=False)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)


class CompanyDetail(models.Model):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    description_of_business = models.CharField(max_length=200, blank=True, null=True)
    establish_year = models.IntegerField(blank=True, null=True)
    company_scale = models.CharField(max_length=2,choices=COMAPANY_SCALE,default="MR")
    block_inv_plant = models.CharField(max_length=50, blank=True, null=True)
    block_inv_land = models.CharField(max_length=50, blank=True, null=True)
    block_inv_total = models.CharField(max_length=50, blank=True, null=True)
    exportcountry = models.ManyToManyField(Country, related_name='export_country', blank=True)
    importcountry = models.ManyToManyField(Country, related_name='import_country', blank=True)
    textexport = models.TextField(blank=True, null=True)
    textimport = models.TextField(blank=True, null=True)
    rnd_facility = models.BooleanField(choices=IS_DELETED, default=True)
    govt_recognised = models.BooleanField(choices=IS_DELETED, default=True)
    iso = models.BooleanField(choices=IS_DELETED, default=False)
    iso_detail = models.TextField(blank=True, null=True)
    foreign_collaboration = models.BooleanField(choices=IS_DELETED, blank=True, default=True)
    eou = models.BooleanField(choices=IS_DELETED, default=True)
    eou_detail = models.CharField(max_length=100, blank=True, null=True)
    total_manager = models.IntegerField(default=0,blank=True, null=True)
    total_staff = models.IntegerField(default=0,blank=True, null=True)
    total_workers = models.IntegerField(default=0,blank=True, null=True)
    total_employees = models.IntegerField(default=0,blank=True, null=True)
    industrydescription = models.ManyToManyField(IndustryDescription, blank=True)
    industrydescription_other = models.CharField(max_length=100, blank=True, null=True)

    legalstatus = models.ForeignKey(LegalStatus, blank=True, null=True)
    hoddetail = models.ForeignKey(HOD_Detail, blank=True, null=True)
    same_as_above = models.BooleanField(choices=IS_DELETED, default=False)
    ceo_email_confirmation = models.BooleanField(choices=IS_DELETED, default=False)
    turnover_range = models.IntegerField(blank=True, null=True, choices=TURNOVER_RANGE)
    employee_range = models.IntegerField(blank=True, null=True, choices=EMPLOYEE_RANGE)

    is_member = models.BooleanField(choices=IS_DELETED, default=False)
    member_event_email = models.TextField(blank=True, null=True)
    gst = models.CharField(max_length=20, blank=True, null=True)
    enroll_type = models.CharField(max_length=2, choices=ENROLL_TYPE, default="CO")

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.company_name)


class UserDetail(models.Model):
    company = models.ForeignKey('CompanyDetail', blank=True, null=True)
    ceo_name = models.CharField(max_length=100, blank=True, null=True)
    ceo_email = models.EmailField(max_length=80, blank=True, null=True)
    ceo_designation = models.CharField(max_length=50, blank=True, null=True)
    ceo_cellno = models.CharField(max_length=50, blank=True, null=True)
    person_name = models.CharField(max_length=50, blank=True, null=True)
    person_email = models.CharField(max_length=50, blank=True, null=True)
    person_designation = models.CharField(max_length=50, blank=True, null=True)
    person_cellno = models.CharField(max_length=50, blank=True, null=True)
    correspond_address = models.TextField(blank=True, null=True)
    # correspond_address = models.CharField(max_length=200, blank=True, null=True)
    correspond_cellno = models.CharField(max_length=50, blank=True, null=True)
    correspond_email = models.CharField(max_length=80, blank=True, null=True)
    correspondstate = models.ForeignKey(State, related_name='correspond_state',blank=True, null=True)
    correspondcity = models.ForeignKey(City, related_name='correspond_city',blank=True, null=True)
    correspond_pincode = models.CharField(max_length=8, blank=True, null=True)
    correspond_std1 = models.CharField(max_length=100, blank=True, null=True)
    correspond_std2 = models.CharField(max_length=100, blank=True, null=True)#used to store Pk of demakh system
    correspond_landline1 = models.CharField(max_length=100, blank=True, null=True)
    correspond_landline2 = models.CharField(max_length=100, blank=True, null=True)
    poc_name = models.CharField(max_length=100, blank=True, null=True)
    poc_contact = models.CharField(max_length=50, blank=True, null=True)
    poc_email = models.EmailField(max_length=80, blank=True, null=True)
    factory_cellno = models.CharField(max_length=50, blank=True, null=True)
    factory_address = models.CharField(max_length=200, blank=True, null=True)
    factorystate = models.ForeignKey(State,related_name='factory_state', blank=True, null=True)
    factorycity = models.ForeignKey(City, related_name='factory_city',blank=True, null=True)
    factory_pincode = models.CharField(max_length=8, blank=True, null=True)
    factory_std1 = models.CharField(max_length=10, blank=True, null=True)
    factory_std2 = models.CharField(max_length=10, blank=True, null=True)
    factory_landline1 = models.CharField(max_length=100, blank=True, null=True)
    factory_landline2 = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    gst = models.CharField(max_length=50, blank=True, null=True)
    gst_in = models.CharField(max_length=2,choices=GST_OPTION,default="NA")
    pan = models.CharField(max_length=12, blank=True, null=True)
    aadhar = models.CharField(max_length=16,blank=True, null=True)
    awards = models.CharField(max_length=50, blank=True, null=True)
    membership_type= models.CharField(max_length=2,choices=MEMBERSHIP_TYPE,default="MM")
    enroll_type= models.CharField(max_length=2,choices=ENROLL_TYPE,default="CO")
    user_type = models.CharField(max_length=20, choices=MEMBER_ASSOCIATION_TYPE, blank=True, null=True)
    member_associate_no = models.CharField(max_length=150, default=None, blank=True, null=True)
    membership_acceptance_date = models.DateField(blank=True, null=True)

    membership_category=models.ForeignKey(MembershipCategory, blank=True, null=True)
    membership_slab=models.ForeignKey(MembershipSlab, blank=True, null=True)
    annual_turnover_year=models.CharField(max_length=150, blank=True, null=True)
    annual_turnover_rupees=models.CharField(max_length=100, blank=True, null=True)
    membership_year = models.CharField(max_length=100, blank=True, null=True)

    renewal_year = models.CharField(max_length=30, blank=True, null=True)
    renewal_status = models.CharField(max_length=15, default='NOT_STARTED' ,choices=RENEWAL_STATUS, blank=True, null=True)

    membership_description =models.ManyToManyField(MembershipDescription, blank=True)
    exclude_from_mailing = models.BooleanField(choices=IS_DELETED, default=False)
    valid_invalid_member = models.BooleanField(choices=IS_DELETED, default=False)
    executive_committee_member = models.BooleanField(choices=IS_DELETED, default=False)
    membership_ceritificate_dispatch = models.BooleanField(choices=IS_DELETED, default=False)
    payment_method = models.CharField(max_length=20, default='Offline Pending', blank=True, null=True, choices=PAYMENT_METHOD)
    created_by = models.CharField(max_length=100, blank=True, null=False)
    updated_by = models.CharField(max_length=100, blank=True, null=True) #used to store the previous ids
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_reassociate = models.BooleanField(choices=IS_DELETED, default=False)
    event_email = models.TextField(blank=True, null=True)
    area_of_experties =  models.IntegerField(blank=True, null=True,default=0, choices=AREA_OF_EXPERTIES)
    experties_other = models.CharField(max_length=100, blank=True, null=True)

    status = models.BooleanField(choices=IS_DELETED, default=False)
    mail_date = models.DateTimeField(blank=True, null=True)
    mail_sent = models.IntegerField(choices=MAIL_SENT_STATUS, default=0, blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.company)+'-'+str(self.enroll_type))


class NonMemberDetail(models.Model):
    company = models.ForeignKey('CompanyDetail', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst = models.CharField(max_length=20, blank=True, null=True)
    enroll_type = models.CharField(max_length=2, choices=ENROLL_TYPE, default="CO")
    email = models.CharField(max_length=80, blank=True, null=True)
    extra_email = models.TextField(blank=True, null=True)

    created_by = models.CharField(max_length=70, blank=True, null=False)
    updated_by = models.CharField(max_length=70, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id))


class Top3Member(models.Model):
    userdetail = models.ForeignKey('UserDetail', blank=True, null=True)
    rank = models.CharField(max_length=100, blank=True, null=False)
    name = models.EmailField(max_length=80, blank=True, null=False)
    created_by = models.CharField(max_length=100, blank=True, null=False)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.userdetail)+'-'+str(self.rank))


class MembershipInvoice(models.Model):
    userdetail = models.ForeignKey('UserDetail', blank=True, null=True)
    membership_category = models.ForeignKey(MembershipCategory, blank=True, null=True)
    membership_slab = models.ForeignKey(MembershipSlab, blank=True, null=True)
    valid_invalid_member = models.BooleanField(choices=IS_DELETED, default=False)
    subscription_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    entrance_fees = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    amount_payable = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    without_adv_amount_payable = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    financial_year = models.CharField(max_length=30, blank=True, null=True)
    last_due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    last_advance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    invoice_for = models.CharField(max_length=12, choices=INVOICE_FOR, default='NEW', blank=True, null=True)
    is_paid = models.BooleanField(choices=IS_DELETED, default=False)
    is_settled = models.BooleanField(choices=IS_DELETED, default=False)
    settle_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    is_tds = models.BooleanField(choices=IS_DELETED, default=False)
    tds_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    turnover_range = models.IntegerField(blank=True, null=True, choices=TURNOVER_RANGE)
    employee_range = models.IntegerField(blank=True, null=True, choices=EMPLOYEE_RANGE)
    user_type = models.CharField(max_length=20, choices=MEMBER_ASSOCIATION_TYPE, blank=True, null=True) # Added by SB
    membership_acceptance_date = models.DateField(blank=True, null=True) # Added by SB
    created_by = models.CharField(max_length=70, blank=True, null=True)
    updated_by = models.CharField(max_length=70, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.userdetail.company))


class PaymentDetails(models.Model):
    userdetail = models.ForeignKey('UserDetail', blank=True, null=True)
    membershipInvoice = models.ForeignKey('MembershipInvoice', blank=True, null=True)
    amount_payable = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    partial_amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    amount_due = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    amount_last_advance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    amount_next_advance= models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    next_advance_gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    cheque_no = models.CharField(max_length=100, blank=True, null=True)
    cheque_date = models.DateField(blank=True,null=True)
    bank_name = models.CharField(max_length=150, blank=True, null=True)
    neft_transfer_id = models.CharField(max_length=150, blank=True, null=True)
    cash_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    cheque_bounce_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    receipt_no = models.CharField(max_length=100, blank=True, null=True)
    receipt_date = models.DateField(blank=True, null=True)
    user_Payment_Type = models.CharField(max_length=20, default='Cheque', blank=True, null=True, choices=PAYMENT_TYPE)
    payment_date = models.DateField(blank=True, null=True)
    payment_received_status= models.CharField(max_length=20, default='UnPaid', blank=True, null=True, choices=PAYMENT_STATUS)
    financial_year = models.CharField(max_length=100, blank=True, null=True)
    bk_no = models.CharField(max_length=20, blank=True, null=True)
    is_cheque_bounce = models.BooleanField(choices=IS_DELETED, default=False)
    is_neft_failed = models.BooleanField(choices=IS_DELETED, default=False)
    is_other = models.BooleanField(choices=IS_DELETED, default=False)
    is_amount_refund = models.BooleanField(choices=IS_DELETED, default=False)
    is_settled = models.BooleanField(choices=IS_DELETED, default=False)
    settle_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    is_tds = models.BooleanField(choices=IS_DELETED, default=False)
    tds_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    payment_remark = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.userdetail.company))


class MembershipUser(User):
    userdetail = models.ForeignKey('UserDetail', blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.userdetail.company.company_name) + str(self.userdetail.member_associate_no))


class MembershipTypeTrack(models.Model):            
    userdetail = models.ForeignKey('UserDetail', blank=True, null=True)
    old_company_name = models.CharField(max_length=100, blank=True, null=True)
    old_user_type = models.CharField(max_length=20, choices=MEMBER_ASSOCIATION_TYPE, blank=True, null=True)
    old_enroll_type= models.CharField(max_length=2,choices=ENROLL_TYPE,default="CO")
    old_member_associate_no = models.CharField(max_length=150, default=None, blank=True, null=True)
    old_acceptance_date = models.DateField(blank=True, null=True)
    old_category=models.ForeignKey(MembershipCategory, blank=True, null=True)
    old_slab=models.ForeignKey(MembershipSlab, blank=True, null=True)
    last_membership_year = models.CharField(max_length=100, blank=True, null=True)
    last_renewal_year = models.CharField(max_length=30, blank=True, null=True)
    last_renewal_status = models.CharField(max_length=15, default='NOT_STARTED', choices=RENEWAL_STATUS, blank=True, null=True)
    new_user_type = models.CharField(max_length=20, choices=MEMBER_ASSOCIATION_TYPE, blank=True, null=True)    
    new_member_associate_no = models.CharField(max_length=150, default=None, blank=True, null=True)
    new_acceptance_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=70, blank=True, null=False)
    updated_by = models.CharField(max_length=70, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '-' + str(self.old_company_name)+'-'+str(self.userdetail.enroll_type))


class RenewLetterSchedule(models.Model):
    row_type = models.IntegerField(choices=TYPE, default=0, blank=False, null=False)
    renew_letter = models.TextField(blank=True, null=True)
    renew_schedule = models.FileField(upload_to=FILE_PATH, null=True, blank=True)
    renew_membership_schedule = models.FileField(upload_to=FILE_PATH, null=True, blank=True)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.row_type))