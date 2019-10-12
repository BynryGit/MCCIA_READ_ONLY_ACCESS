from django.db import models
import django
from hallbookingapp.models import HallBooking
from eventsapp.models import EventRegistration
from membershipapp.models import MembershipInvoice, PaymentDetails

TXN_STATUS = (
    (0, 'Inprogress'),
    (1, 'Success'),
    (2, 'Initiated'),
    (3, 'Failed'),
    (4, 'Aborted'),
)

IS_DELETED = (
    (True, True),
    (False, False),
)

PAYMENT_FOR = (
    (1, 'Membership'),
    (2, 'Hall Booking'),
    (3, 'Event'),
    (0, 'None'),
)

PAYMENT_STATUS =(
    (0, 'Inprogress'),
    (1, 'Success'),
    (2, 'Initiated'),
    (3, 'Failed'),
    (4, 'Aborted'),
    (5, 'Pending'),
    (6, 'Not Paid'),
)

PAYMENT_MODE = (
    (1, 'Online'),
    (2, 'UPI'),
    (3, 'Card'),
    (4, 'Wallet'),
    (5, 'IMPS'),
    (6, 'Cash Cards'),
    (7, 'MIVSA'),
    (8, 'Debit Pin'),
    (9, 'EMI Banks'),
    (0, 'None'),
)


class PaymentTransaction(models.Model):
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    reg_no = models.CharField(max_length=100, blank=True, null=True)#no need
    payment_for = models.IntegerField(choices=PAYMENT_FOR, default=0)
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, default=0)

    # consumer card and payment info
    merchant_id = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.CharField(max_length=20, blank=True, null=True)
    consumer_name = models.CharField(max_length=100,blank=True, null=True)
    consumer_mobile_no = models.CharField(max_length=50,blank=True, null=True)
    consumer_email = models.CharField(max_length=100,blank=True, null=True)

    # filed used to store response parameter
    txn_status = models.CharField(max_length=10, blank=True, null=True)
    txn_msg = models.TextField(blank=True, null=True)
    txn_err_msg = models.TextField(blank=True, null=True)
    clnt_txn_ref = models.CharField(max_length=100, blank=True, null=True)
    tpsl_bank_cd = models.CharField(max_length=100, blank=True, null=True)
    tpsl_txn_id = models.CharField(max_length=100, blank=True, null=True)
    txn_amt = models.CharField(max_length=100, blank=True, null=True)
    clnt_rqst_meta = models.TextField(blank=True, null=True)
    tpsl_txn_time = models.CharField(max_length=100, blank=True, null=True)
    bal_amt = models.CharField(max_length=100, blank=True, null=True)
    card_id = models.CharField(max_length=100, blank=True, null=True)
    alias_name = models.CharField(max_length=100, blank=True, null=True)
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    mandate_reg_no = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_hash_matched = models.BooleanField(choices=IS_DELETED, default=True)

    def __unicode__(self):
        return str(self.id)


class EventPaymentTransaction(models.Model):
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    event_reg = models.ForeignKey(EventRegistration, blank=True, null=True, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=100, blank=True, null=True)#no need
    payment_for = models.IntegerField(choices=PAYMENT_FOR, default=3)
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, default=1)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=6)

    # consumer card and payment info
    merchant_id = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.CharField(max_length=20, blank=True, null=True)
    consumer_name = models.CharField(max_length=100,blank=True, null=True)
    consumer_mobile_no = models.CharField(max_length=50,blank=True, null=True)
    consumer_email = models.CharField(max_length=100,blank=True, null=True)

    # filed used to store response parameter
    txn_status = models.CharField(max_length=10, blank=True, null=True)
    txn_msg = models.TextField(blank=True, null=True)
    txn_err_msg = models.TextField(blank=True, null=True)
    clnt_txn_ref = models.CharField(max_length=100, blank=True, null=True)
    tpsl_bank_cd = models.CharField(max_length=100, blank=True, null=True)
    tpsl_txn_id = models.CharField(max_length=100, blank=True, null=True)
    txn_amt = models.CharField(max_length=100, blank=True, null=True)
    clnt_rqst_meta = models.TextField(blank=True, null=True)
    tpsl_txn_time = models.CharField(max_length=100, blank=True, null=True)
    bal_amt = models.CharField(max_length=100, blank=True, null=True)
    card_id = models.CharField(max_length=100, blank=True, null=True)
    alias_name = models.CharField(max_length=100, blank=True, null=True)
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    mandate_reg_no = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_hash_matched = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return str(self.id)


class HallPaymentTransaction(models.Model):
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    hall_booking = models.ForeignKey(HallBooking, blank=True, null=True, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=100, blank=True, null=True)#no need
    payment_for = models.IntegerField(choices=PAYMENT_FOR, default=2)
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, default=1)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=6)

    # consumer card and payment info
    merchant_id = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.CharField(max_length=20, blank=True, null=True)
    consumer_name = models.CharField(max_length=100,blank=True, null=True)
    consumer_mobile_no = models.CharField(max_length=50,blank=True, null=True)
    consumer_email = models.CharField(max_length=100,blank=True, null=True)

    # filed used to store response parameter
    txn_status = models.CharField(max_length=10, blank=True, null=True)
    txn_msg = models.TextField(blank=True, null=True)
    txn_err_msg = models.TextField(blank=True, null=True)
    clnt_txn_ref = models.CharField(max_length=100, blank=True, null=True)
    tpsl_bank_cd = models.CharField(max_length=100, blank=True, null=True)
    tpsl_txn_id = models.CharField(max_length=100, blank=True, null=True)
    txn_amt = models.CharField(max_length=100, blank=True, null=True)
    clnt_rqst_meta = models.TextField(blank=True, null=True)
    tpsl_txn_time = models.CharField(max_length=100, blank=True, null=True)
    bal_amt = models.CharField(max_length=100, blank=True, null=True)
    card_id = models.CharField(max_length=100, blank=True, null=True)
    alias_name = models.CharField(max_length=100, blank=True, null=True)
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    mandate_reg_no = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_hash_matched = models.BooleanField(choices=IS_DELETED, default=True)

    def __unicode__(self):
        return str(self.id)


class MembershipPaymentTransaction(models.Model):
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    membership_invoice = models.ForeignKey(MembershipInvoice, blank=True, null=True)
    payment_detail = models.ForeignKey(PaymentDetails, blank=True, null=True)
    reg_no = models.CharField(max_length=100, blank=True, null=True)#no need
    payment_for = models.IntegerField(choices=PAYMENT_FOR, default=1)
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, default=0)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=6)

    # consumer card and payment info
    merchant_id = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.CharField(max_length=20, blank=True, null=True)
    consumer_name = models.CharField(max_length=100,blank=True, null=True)
    consumer_mobile_no = models.CharField(max_length=50,blank=True, null=True)
    consumer_email = models.CharField(max_length=100,blank=True, null=True)

    # filed used to store response parameter
    txn_status = models.CharField(max_length=10, blank=True, null=True)
    txn_msg = models.TextField(blank=True, null=True)
    txn_err_msg = models.TextField(blank=True, null=True)
    clnt_txn_ref = models.CharField(max_length=100, blank=True, null=True)
    tpsl_bank_cd = models.CharField(max_length=100, blank=True, null=True)
    tpsl_txn_id = models.CharField(max_length=100, blank=True, null=True)
    txn_amt = models.CharField(max_length=100, blank=True, null=True)
    clnt_rqst_meta = models.TextField(blank=True, null=True)
    tpsl_txn_time = models.CharField(max_length=100, blank=True, null=True)
    bal_amt = models.CharField(max_length=100, blank=True, null=True)
    card_id = models.CharField(max_length=100, blank=True, null=True)
    alias_name = models.CharField(max_length=100, blank=True, null=True)
    bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    mandate_reg_no = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_hash_matched = models.BooleanField(choices=IS_DELETED, default=True)
    is_renew = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return str(self.id)


class PendingTransaction(models.Model):
    payment_transaction = models.ForeignKey('PaymentTransaction', blank=True, null=True)

    txn_status = models.IntegerField(choices=TXN_STATUS, default=0)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=5)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return str(self.id)
#
# class PaymentTransaction(models.Model):
#     transaction_id = models.CharField(max_length=50, blank=True, null=True)
#     reg_no = models.CharField(max_length=100, blank=True, null=True)#no need
#     payment_for = models.IntegerField(choices=PAYMENT_FOR, default=0)
#     payment_mode = models.IntegerField(choices=PAYMENT_MODE, default=0)
#
#     # consumer card and payment info
#     merchant_id = models.CharField(max_length=20, blank=True, null=True)
#     total_amount = models.CharField(max_length=20, blank=True, null=True)
#     #account_number = models.CharField(max_length=100,blank=True, null=True)
#     consumer_name = models.CharField(max_length=100,blank=True, null=True)
#     #consumer_id = models.CharField(max_length=50,blank=True, null=True)
#     consumer_mobile_no = models.CharField(max_length=50,blank=True, null=True)
#     consumer_email = models.CharField(max_length=100,blank=True, null=True)
#     # debit_start_date = models.DateTimeField(default=django.utils.timezone.now)
#     # debit_end_date = models.DateTimeField(default=django.utils.timezone.now)
#     # max_amount = models.CharField(max_length=20, blank=True, null=True)
#     # amount_type = models.CharField(max_length=20, blank=True, null=True)
#     # frequency = models.CharField(max_length=20, blank=True, null=True)
#     # card_number = models.CharField(max_length=50, blank=True, null=True)
#     # exp_month = models.CharField(max_length=10, blank=True, null=True)
#     # exp_year = models.CharField(max_length=10, blank=True, null=True)
#     # cvv_code = models.CharField(max_length=10, blank=True, null=True)
#
#     # filed used to store response parameter
#     # txn_status_code = models.CharField(max_length=20, blank=True, null=True)
#     txn_status = models.CharField(max_length=10, blank=True, null=True)
#     txn_msg = models.TextField(blank=True, null=True)
#     txn_err_msg = models.TextField(blank=True, null=True)
#     clnt_txn_ref = models.CharField(max_length=100, blank=True, null=True)
#     tpsl_bank_cd = models.CharField(max_length=100, blank=True, null=True)
#     tpsl_txn_id = models.CharField(max_length=100, blank=True, null=True)
#     txn_amt = models.CharField(max_length=100, blank=True, null=True)
#     clnt_rqst_meta = models.TextField(blank=True, null=True)
#     tpsl_txn_time = models.CharField(max_length=100, blank=True, null=True)
#     bal_amt = models.CharField(max_length=100, blank=True, null=True)
#     card_id = models.CharField(max_length=100, blank=True, null=True)
#     alias_name = models.CharField(max_length=100, blank=True, null=True)
#     bank_transaction_id = models.CharField(max_length=100, blank=True, null=True)
#     mandate_reg_no = models.CharField(max_length=100, blank=True, null=True)
#
#     created_by = models.CharField(max_length=100, blank=True, null=True)
#     updated_by = models.CharField(max_length=100, blank=True, null=True)
#     created_date = models.DateTimeField(default=django.utils.timezone.now)
#     updated_date = models.DateTimeField(blank=True, null=True)
#     is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
#     is_hash_matched = models.BooleanField(choices=IS_DELETED, default=True)
#
#     def __unicode__(self):
#         return str(self.id)
