# System Module

from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
import traceback
import hashlib
import datetime
from django.db import transaction
import re
import logging
from django.db.models import Count, Sum, Q, F

# User Model

from membershipapp.models import MembershipInvoice, PaymentDetails, UserDetail, NonMemberDetail
from Paymentapp.view.membership import save_new_member
from Paymentapp.models import PaymentTransaction,PendingTransaction, EventPaymentTransaction, HallPaymentTransaction, MembershipPaymentTransaction
from eventsapp.models import EventRegistration, EventParticipantUser
from hallbookingapp.models import HallCheckAvailability, HallBooking, HallBookingDetail, HallPaymentDetail, UserTrackDetail, HallBookingDepositDetail
from massmailingapp.models import EmailDetail
from hallbookingapp.view.hall_booking_confirm import send_booking_invoice_mail, send_booking_invoice_mail_locationvise
from eventsapp.view.events_landing import send_event_reg_ack_mail
from backofficeapp.view import membership_details
from hallbookingapp.view.hall_booking_confirm import get_financial_year


try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


def get_check_mid_page(request):
    return render(request, 'payment/check_mid.html')


@csrf_exempt
@transaction.atomic
def get_payment_detail(request):
    print "----------------------------------"
    sid = transaction.savepoint()
    print "----------------------------------"
    try:
        # Add info according to your requirement
        total_amount=1
        consumer_name = 'Shubham Bharti'
        consumerMobileNo='7507743936'
        consumerEmailId='bhartis497@gmail.com'

        user_obj = UserDetail.objects.get(id=37741)

        merchant_id = 'T172654'
        salt='2093514954UVQFBK'
        # merchant_id = 'L172654'
        # salt = '2093514954UVQFBK'
        # merchant_id = 'L172655'
        # salt = '7171770084PTUXUD'
        itemId = 'MCCI' #scheme code
        transaction_id = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        try:
            PaymentTransaction_obj=PaymentTransaction(
                transaction_id=transaction_id,
                reg_no='1234',
                merchant_id = merchant_id,
                total_amount = total_amount,
                consumer_name = consumer_name,
                consumer_mobile_no = consumerMobileNo,
                consumer_email = consumerEmailId
            )

            PaymentTransaction_obj.save()

            m = hashlib.sha512()
            parameters = {'company_name': str(user_obj.company.company_name), 'membership_no': str(user_obj.member_associate_no)}
            card_desc = str(json.dumps(parameters))
            card_desc = card_desc.replace('"', '')

            msg = merchant_id + "|"  # consumerData.merchantId|
            msg += str(transaction_id) + "|"  # consumerData.txnId|
            msg += str(total_amount) + "|"  # totalamount|
            msg += "" + "|"  # consumerData.accountNo|
            msg += "" + "|"  # consumerData.consumerId|
            msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
            msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
            msg += "" + "|"  # consumerData.debitStartDate|
            msg += "" + "|"  # consumerData.debitEndDate|
            msg += "" + "|"  # consumerData.maxAmount|
            msg += "" + "|"  # consumerData.amountType|
            msg += "" + "|"  # consumerData.frequency|
            msg += "" + "|"  # consumerData.cardNumber|
            msg += "" + "|"  # consumerData. expMonth|
            msg += "" + "|"  # consumerData.expYear|
            msg += "" + "|"  # consumerData.cvvCode|
            msg += salt      #salt

            print msg

            # print token_string
            m.update(msg)

            configJson = {
                'tarCall': False,
                'features': {
                    'showPGResponseMsg': True,
                    'enableNewWindowFlow': True
                },
                'consumerData': {
                    'deviceId': 'WEBSH2',
                    'token': str(m.hexdigest()),
                    'responseHandler': 'handleResponse',
                    'paymentMode': 'all',
                    'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                    'merchantId':merchant_id,
                    'currency': 'INR',
                    'consumerId': '',
                    'consumerMobileNo':consumerMobileNo,
                    'consumerEmailId':consumerEmailId,
                    'txnId': str(transaction_id),
                    'cardNumber': '',
                    'expMonth': '',
                    'expYear': '',
                    'cvvCode': '',
                    'amount_type': '',
                    'frequency':'',
                    'amountType': '',
                    'debitStartDate': '',
                    'debitEndDate': '',
                    'maxAmount': '',
                    'accountNo': '',
                    'items': [{
                        'itemId': itemId,
                        'amount': str(total_amount),
                        'comAmt': '0'
                    }],
                    'cartDescription': card_desc,
                    'customStyle': {
                        'PRIMARY_COLOR_CODE': '#3977b7',
                        'SECONDARY_COLOR_CODE': '#FFFFFF',
                        'BUTTON_COLOR_CODE_1': '#1969bb',
                        'BUTTON_COLOR_CODE_2': '#FFFFFF'
                    }
                }
            }
            transaction.savepoint_commit(sid)
            data = {'configJson': configJson, 'success': 'true'}
        except Exception,e:
            print e
            pass
            transaction.rollback(sid)
            data = {'success': 'false'}


    except Exception, e:
        print e
        pass
        transaction.rollback(sid)
        data = {'success': 'false'}
    print data
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@transaction.atomic
def common_response_save(request):
    sid = transaction.savepoint()
    print request.POST
    data=request.POST
    try:
        salt = '2093514954UVQFBK'
        stringResponse=data['stringResponse']
        stringResponse_list=stringResponse.split('|')
        txn_status = stringResponse_list[0]
        txn_msg = stringResponse_list[1]
        txn_err_msg = stringResponse_list[2]
        clnt_txn_ref = stringResponse_list[3]
        tpsl_bank_cd = stringResponse_list[4]
        tpsl_txn_id = stringResponse_list[5]
        txn_amt = stringResponse_list[6]
        clnt_rqst_meta = stringResponse_list[7]
        tpsl_txn_time = stringResponse_list[8]
        bal_amt = stringResponse_list[9]
        card_id = stringResponse_list[10]
        alias_name = stringResponse_list[11]
        bank_transaction_id = stringResponse_list[12]
        mandate_reg_no = stringResponse_list[13]
        token = stringResponse_list[14]
        hash = stringResponse_list[15]

        msg = txn_status
        msg += '|' +txn_msg
        msg += '|' +txn_err_msg
        msg += '|' +clnt_txn_ref
        msg += '|' +tpsl_bank_cd
        msg += '|' +tpsl_txn_id
        msg += '|' +txn_amt
        msg += '|' +clnt_rqst_meta
        msg += '|' +tpsl_txn_time
        msg += '|' +bal_amt
        msg += '|' +card_id
        msg += '|' +alias_name
        msg += '|' +bank_transaction_id
        msg += '|' +mandate_reg_no
        msg += '|' +token
        msg += '|' + salt

        m = hashlib.sha512()
        m.update(msg)
        hex_msg=m.hexdigest()
        is_hash_match = hex_msg == hash

        try:
            statusCode = data['statusCode']  # 0300=Success,0398=Initiated,0399=failure,0396=Aborted
            responseType = data['responseType']  # hasg algo name
            errorMessage = data['errorMessage']
            accountNo = data['accountNo']
            reference = data['reference']
            bankReferenceIdentifier = data['bankReferenceIdentifier']
            merchantTransactionIdentifier = data['merchantTransactionIdentifier']
            merchantAdditionalDetails = data['merchantAdditionalDetails']
            dateTime = data['dateTime']  # convert to datetime object
            amount = data['amount']
            statusMessage = data['statusMessage']
            balanceAmount = data['balanceAmount']
            error = data['error']
            identifier = data['identifier']
            merchantTransactionRequestType = data['merchantTransactionRequestType']
            refundIdentifier = data['refundIdentifier']
            transactionState = data['transactionState']

            paymenttransactionobj = PaymentTransaction.objects.get(transaction_id=merchantTransactionIdentifier)

            paymenttransactionobj.txn_status=txn_status #statusCode
            paymenttransactionobj.txn_msg=txn_msg #statusMessage
            paymenttransactionobj.txn_err_msg=txn_err_msg #errorMessage
            paymenttransactionobj.clnt_txn_ref=clnt_txn_ref
            paymenttransactionobj.tpsl_bank_cd=tpsl_bank_cd
            paymenttransactionobj.tpsl_txn_id=tpsl_txn_id #identifier
            paymenttransactionobj.txn_amt=txn_amt
            paymenttransactionobj.clnt_rqst_meta=clnt_rqst_meta
            paymenttransactionobj.tpsl_txn_time=tpsl_txn_time
            paymenttransactionobj.bal_amt=bal_amt
            paymenttransactionobj.card_id=card_id
            paymenttransactionobj.alias_name=alias_name
            paymenttransactionobj.bank_transaction_id=bank_transaction_id
            paymenttransactionobj.mandate_reg_no=mandate_reg_no
            paymenttransactionobj.save()

            if statusCode == '0300' and is_hash_match:

                transaction.savepoint_commit(sid)

                #code for success
                #upate the status and send conformation mail to user

                pass
            elif statusCode == '0398' and is_hash_match:
                #code for Initiated transaction
                #add entry in pending transaction table
                add_to_pending(paymenttransactionobj.id)
                pass
            elif statusCode == '0399' and is_hash_match:
                #code for failure transaction
                pass
            elif statusCode == '0396' and is_hash_match:
                #code for aborted transaction
                #transaction is aborted by user
                pass
            elif is_hash_match:
                # code if hash is matched but no status code
                pass

            elif not is_hash_match and statusCode in ['0300','0398','0399','0396']:
                paymenttransactionobj.is_hash_matched = False
                paymenttransactionobj.save()
                #code if hash code is not matched  and with match statusCode
                pass

            else:
                # code if hash code is not matched  and without match statusCode
                pass

            transaction.savepoint_commit(sid)

        except Exception, e:
            pass

    except Exception,e:
        transaction.rollback(sid)
        pass
        data = {'success': 'false'}

    return HttpResponse(json.dumps(data), content_type='application/json')


def add_to_pending(id):
    try:
        pendingobj=PendingTransaction(
            payment_transaction_id=id
        )
        pendingobj.save()

    except Exception,e:
        pass

    return True


@csrf_exempt
@transaction.atomic
def get_event_payment_detail(request):
    print "--------------Event--------------------"
    sid = transaction.savepoint()
    try:
        event_reg_obj = EventRegistration.objects.get(id=request.POST.get('event_reg_id'))

        total_amount=str(event_reg_obj.total_amount)

        consumer_name = str(event_reg_obj.contact_person_name)
        consumerMobileNo= str(event_reg_obj.contact_person_number)
        consumerEmailId= str(event_reg_obj.contact_person_email_id)

        merchant_id = 'L172655'
        salt='6790264316SSAGPJ'
        # merchant_id = 'L172654'
        # salt = '2093514954UVQFBK'
        # merchant_id = 'T172654'
        # salt='2093514954UVQFBK'        
        itemId = 'MCCI' #scheme code
        transaction_id = str(event_reg_obj.reg_no) + '_' + str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        try:
            PaymentTransaction_obj=EventPaymentTransaction(
                transaction_id=transaction_id,
                event_reg=event_reg_obj,
                reg_no = '1234',
                merchant_id = merchant_id,
                total_amount = total_amount,
                consumer_name = consumer_name,
                consumer_mobile_no = consumerMobileNo,
                consumer_email = consumerEmailId
            )

            PaymentTransaction_obj.save()

            m = hashlib.sha512()

            parameters = {'event_title': re.sub(r'[^\x00-\x7F]+','', str(event_reg_obj.event.event_title)),
                          'party_name': str(event_reg_obj.name_of_organisation)}
            cart_desc = str(json.dumps(parameters))
            cart_desc = cart_desc.replace('"', '')            

            msg = merchant_id + "|"  # consumerData.merchantId|
            msg += str(transaction_id) + "|"  # consumerData.txnId|
            msg += str(total_amount) + "|"  # totalamount|
            msg += "" + "|"  # consumerData.accountNo|
            msg += "" + "|"  # consumerData.consumerId|
            msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
            msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
            msg += "" + "|"  # consumerData.debitStartDate|
            msg += "" + "|"  # consumerData.debitEndDate|
            msg += "" + "|"  # consumerData.maxAmount|
            msg += "" + "|"  # consumerData.amountType|
            msg += "" + "|"  # consumerData.frequency|
            msg += "" + "|"  # consumerData.cardNumber|
            msg += "" + "|"  # consumerData. expMonth|
            msg += "" + "|"  # consumerData.expYear|
            msg += "" + "|"  # consumerData.cvvCode|
            msg += salt      #salt

            print msg

            # print token_string
            m.update(msg)

            configJson = {
                'tarCall': False,
                'features': {
                    'showPGResponseMsg': True,
                    'enableNewWindowFlow': True
                },
                'consumerData': {
                    'deviceId': 'WEBSH2',
                    'token': str(m.hexdigest()),
                    'responseHandler': 'handleResponse',
                    'paymentMode': 'all',
                    'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                    'merchantId':merchant_id,
                    'currency': 'INR',
                    'consumerId': '',
                    'consumerMobileNo':consumerMobileNo,
                    'consumerEmailId':consumerEmailId,
                    'txnId': str(transaction_id),
                    'cardNumber': '',
                    'expMonth': '',
                    'expYear': '',
                    'cvvCode': '',
                    'amount_type': '',
                    'frequency':'',
                    'amountType': '',
                    'debitStartDate': '',
                    'debitEndDate': '',
                    'maxAmount': '',
                    'accountNo': '',
                    'items': [{
                        'itemId': itemId,
                        'amount': str(total_amount),
                        'comAmt': '0'
                    }],
                    'cartDescription': cart_desc,                    
                    'customStyle': {
                        'PRIMARY_COLOR_CODE': '#3977b7',
                        'SECONDARY_COLOR_CODE': '#FFFFFF',
                        'BUTTON_COLOR_CODE_1': '#1969bb',
                        'BUTTON_COLOR_CODE_2': '#FFFFFF'
                    }
                }
            }
            transaction.savepoint_commit(sid)
            data = {'configJson': configJson, 'success': 'true'}
        except Exception,e:
            print e
            pass
            transaction.rollback(sid)
            data = {'success': 'false'}


    except Exception, e:
        print e
        pass
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@transaction.atomic
def event_response_save(request):
    print 'Inside event_response_save'
    sid = transaction.savepoint()
    #print request.POST
    data=request.POST
    response_data = {}
    try:
        salt = '6790264316SSAGPJ'
        stringResponse=data['stringResponse']
        stringResponse_list=stringResponse.split('|')
        txn_status = stringResponse_list[0]
        txn_msg = stringResponse_list[1]
        txn_err_msg = stringResponse_list[2]
        clnt_txn_ref = stringResponse_list[3]
        tpsl_bank_cd = stringResponse_list[4]
        tpsl_txn_id = stringResponse_list[5]
        txn_amt = stringResponse_list[6]
        clnt_rqst_meta = stringResponse_list[7]
        tpsl_txn_time = stringResponse_list[8]
        bal_amt = stringResponse_list[9]
        card_id = stringResponse_list[10]
        alias_name = stringResponse_list[11]
        bank_transaction_id = stringResponse_list[12]
        mandate_reg_no = stringResponse_list[13]
        token = stringResponse_list[14]
        hash = stringResponse_list[15]

        msg = txn_status
        msg += '|' +txn_msg
        msg += '|' +txn_err_msg
        msg += '|' +clnt_txn_ref
        msg += '|' +tpsl_bank_cd
        msg += '|' +tpsl_txn_id
        msg += '|' +txn_amt
        msg += '|' +clnt_rqst_meta
        msg += '|' +tpsl_txn_time
        msg += '|' +bal_amt
        msg += '|' +card_id
        msg += '|' +alias_name
        msg += '|' +bank_transaction_id
        msg += '|' +mandate_reg_no
        msg += '|' +token
        msg += '|' + salt

        m = hashlib.sha512()
        m.update(msg)
        hex_msg=m.hexdigest()
        is_hash_match = hex_msg == hash

        # if (hex_msg == hash):
        try:
            statusCode = data['statusCode']  # 0300=Success,0398=Initiated,0399=failure,0396=Aborted
            responseType = data['responseType']  # hasg algo name
            errorMessage = data['errorMessage']
            accountNo = data['accountNo']
            reference = data['reference']
            bankReferenceIdentifier = data['bankReferenceIdentifier']
            merchantTransactionIdentifier = data['merchantTransactionIdentifier']
            merchantAdditionalDetails = data['merchantAdditionalDetails']
            dateTime = data['dateTime']  # convert to datetime object
            amount = data['amount']
            statusMessage = data['statusMessage']
            balanceAmount = data['balanceAmount']
            error = data['error']
            identifier = data['identifier']
            merchantTransactionRequestType = data['merchantTransactionRequestType']
            refundIdentifier = data['refundIdentifier']
            transactionState = data['transactionState']

            paymenttransactionobj = EventPaymentTransaction.objects.get(transaction_id=merchantTransactionIdentifier)
            paymenttransactionobj.txn_status=txn_status #statusCode
            paymenttransactionobj.txn_msg=txn_msg #statusMessage
            paymenttransactionobj.txn_err_msg=txn_err_msg #errorMessage
            paymenttransactionobj.clnt_txn_ref=clnt_txn_ref
            paymenttransactionobj.tpsl_bank_cd=tpsl_bank_cd
            paymenttransactionobj.tpsl_txn_id=tpsl_txn_id #identifier
            paymenttransactionobj.txn_amt=txn_amt
            paymenttransactionobj.clnt_rqst_meta=clnt_rqst_meta
            paymenttransactionobj.tpsl_txn_time=tpsl_txn_time
            paymenttransactionobj.bal_amt=bal_amt
            paymenttransactionobj.card_id=card_id
            paymenttransactionobj.alias_name=alias_name
            paymenttransactionobj.bank_transaction_id=bank_transaction_id
            paymenttransactionobj.mandate_reg_no=mandate_reg_no
            paymenttransactionobj.save()

            if statusCode == '0300' and is_hash_match:
                print '300 - hash matched'
                #code for success

                paymenttransactionobj.payment_status = 1
                paymenttransactionobj.save()                            
                event_reg_obj = EventRegistration.objects.get(id=request.POST.get('event_reg_id'))
                event_reg_obj.is_active = True
                event_reg_obj.is_deleted = False
                event_reg_obj.payment_status = 4
                event_reg_obj.save()
                adding_new_emails(request,event_reg_obj)
                transaction.savepoint_commit(sid)

                send_event_reg_ack_mail(event_reg_obj)
                response_data['success'] = 'true'

                pass
            elif statusCode == '0398' and is_hash_match:
                print '0398 - hash matched'
                #code for Initiated transaction
                #add entry in pending transaction table
                paymenttransactionobj.payment_status = 2
                paymenttransactionobj.save()
                event_reg_obj = EventRegistration.objects.get(id=request.POST.get('event_reg_id'))
                event_reg_obj.is_active = True
                event_reg_obj.is_deleted = False
                event_reg_obj.payment_status = 2
                event_reg_obj.save()                
                adding_new_emails(request,event_reg_obj)
                transaction.savepoint_commit(sid)

                send_event_reg_ack_mail(event_reg_obj)
                add_to_pending(paymenttransactionobj.id)
                response_data['success'] = 'initiated'
                pass
            elif statusCode == '0399' and is_hash_match:
                print '0399 - hash matched'
                #code for failure transaction
                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                response_data['success'] = 'failed'
                pass
            elif statusCode == '0396' and is_hash_match:
                print '0396 - hash matched'
                #code for aborted transaction
                #transaction is aborted by user
                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.save() 
                response_data['success'] = 'cancelled'               
                pass
            elif is_hash_match:
                print 'hash matched but no status code'
                # code if hash is matched but no status code
                pass

            elif not is_hash_match and statusCode in ['0300','0398','0399','0396']:
                #code if hash code is not matched  and with match statusCode
                if statusCode == '0300':              
                    print '0300 - hash not matched'      
                    paymenttransactionobj.payment_status = 1
                    paymenttransactionobj.is_hash_matched = False
                    paymenttransactionobj.save()                
                    event_reg_obj = EventRegistration.objects.get(id=request.POST.get('event_reg_id'))
                    event_reg_obj.is_active = True
                    event_reg_obj.is_deleted = False
                    event_reg_obj.payment_status = 4
                    event_reg_obj.save()
                    adding_new_emails(request,event_reg_obj)
                    transaction.savepoint_commit(sid)

                    send_event_reg_ack_mail(event_reg_obj)
                    response_data['success'] = 'true'

                elif statusCode == '0398':  
                    print '0398 - hash not matched'      
                    paymenttransactionobj.payment_status = 2
                    paymenttransactionobj.save()
                    event_reg_obj = EventRegistration.objects.get(id=request.POST.get('event_reg_id'))
                    event_reg_obj.is_active = True
                    event_reg_obj.is_deleted = False
                    event_reg_obj.payment_status = 2
                    event_reg_obj.save()
                    adding_new_emails(request,event_reg_obj)
                    transaction.savepoint_commit(sid)

                    send_event_reg_ack_mail(event_reg_obj)
                    response_data['success'] = 'initiated'

                    add_to_pending(paymenttransactionobj.id)

                elif statusCode == '0399':  
                    print '0399 - hash not matched'      
                    paymenttransactionobj.payment_status = 3
                    paymenttransactionobj.save()
                    response_data['success'] = 'failed'

                elif statusCode == '0396':  
                    print '0396 - hash not matched'      
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.save()         
                    response_data['success'] = 'cancelled'            
                pass

            else:
                print 'hash not matched and no status code'
                # code if hash code is not matched  and without match statusCode
                paymenttransactionobj.payment_status = 6
                paymenttransactionobj.save()
                response_data['success'] = 'notpaid'                
                pass

        except Exception, e:
            print e
            pass

    except Exception,e:
        transaction.rollback(sid)
        pass
        response_data['success'] = 'false'

    return HttpResponse(json.dumps(response_data), content_type='application/json')    


def adding_new_emails(request,event_reg_obj):
        #Start - Code for saving Email id's for Massmailing
        new_email_list = [obj.email_id for obj in  EventParticipantUser.objects.filter(event_user=event_reg_obj)]

        if event_reg_obj.user_details:
            #Start - Adding new email in UserDetail Table 
            member_obj = UserDetail.objects.get(id=event_reg_obj.user_details.id)
            event_email_list = member_obj.event_email.split(',') if member_obj.event_email else []
            email_to_add_list = (list(set(new_email_list) - set(event_email_list)))

            for new_email in email_to_add_list:
                member_obj.event_email = str(member_obj.event_email) +',' + str(new_email)
                member_obj.save()   
            #End - Adding new email in UserDetail Table     

            #Start - Adding new email in EmailDetail Table  
            try:
                event_participant_list = EventParticipantUser.objects.filter(event_user=event_reg_obj)
                for event_par in event_participant_list:
                    try:
                        old_email_obj = EmailDetail.objects.get(userdetail=member_obj,email=event_par.email_id)
                        old_email_obj.name = event_par.event_user_name
                        old_email_obj.designation = event_par.designation
                        old_email_obj.cellno = event_par.contact_no
                        old_email_obj.hash_tag = old_email_obj.hash_tag + ',' + str(event_par.event_user.event.organising_committee.committee) if old_email_obj.hash_tag else str(event_par.event_user.event.organising_committee.committee)
                        old_email_obj.save()

                        old_hash_tag_list = old_email_obj.hash_tag.split(',')
                        old_hash_tag_list = set(old_hash_tag_list)
                        str1 = ','.join(old_hash_tag_list)
                        old_email_obj.hash_tag = str1
                        old_email_obj.save()
                    except Exception as e:
                        print e
                        EmailDetail(
                            userdetail=member_obj,
                            name=event_par.event_user_name,
                            email=event_par.email_id,
                            designation=event_par.designation,
                            cellno=event_par.contact_no,
                            hash_tag=str(event_par.event_user.event.organising_committee.committee),
                            is_member = True,
                        ).save()    

                return True        

            except Exception as  e:
                print e
            #End - Adding new email in EmailDetail Table    

        elif event_reg_obj.nonmemberdetail:
            non_member_obj = NonMemberDetail.objects.get(id=event_reg_obj.nonmemberdetail.id)
            #Start - Adding new email in EmailDetail Table  
            try:
                event_participant_list = EventParticipantUser.objects.filter(event_user=event_reg_obj)
                for event_par in event_participant_list:
                    try:
                        old_email_obj = EmailDetail.objects.get(nonmemberdetail=non_member_obj,email=event_par.email_id)
                        old_email_obj.name = event_par.event_user_name
                        old_email_obj.designation = event_par.designation
                        old_email_obj.cellno = event_par.contact_no
                        old_email_obj.hash_tag = old_email_obj.hash_tag + ',' + str(event_par.event_user.event.organising_committee.committee) if old_email_obj.hash_tag else str(event_par.event_user.event.organising_committee.committee)
                        old_email_obj.save()

                        old_hash_tag_list = old_email_obj.hash_tag.split(',')
                        old_hash_tag_list = set(old_hash_tag_list)
                        str1 = ','.join(old_hash_tag_list)
                        old_email_obj.hash_tag = str1
                        old_email_obj.save()                        
                    except Exception as e:
                        print e
                        EmailDetail(
                            nonmemberdetail=non_member_obj,
                            name=event_par.event_user_name,
                            email=event_par.email_id,
                            designation=event_par.designation,
                            cellno=event_par.contact_no,
                            hash_tag=str(event_par.event_user.event.organising_committee.committee),
                            is_member = False,
                        ).save()  
                return True          

            except Exception as  e:
                print e
            #End - Adding new email in EmailDetail Table    

        return False

        #End - Code for saving Email id's for Massmailing


# Hall Booking
# Get Payment Detail
@csrf_exempt
@transaction.atomic
def get_hall_payment_detail(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | common.py | get_hall_payment_detail | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
#####################################

        hall_booking_obj.booking_no = str('HBK' + str(str.zfill(str(hall_booking_obj.id), 7)))
        hall_booking_obj.save()

        booking_sb_obj = HallBookingDetail.objects.filter(hall_location__location='MCCIA Trade Tower (5th Floor)',
                                                          pi_no__isnull=False).last()
        booking_tilak_obj = HallBookingDetail.objects.filter(hall_location__location='Tilak Road',
                                                             pi_no__isnull=False).last()
        booking_bhosari_obj = HallBookingDetail.objects.filter(hall_location__location='Bhosari',
                                                               pi_no__isnull=False).last()
        booking_hadapsar_obj = HallBookingDetail.objects.filter(hall_location__location='Hadapsar',
                                                                pi_no__isnull=False).last()

        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).values(
            'hall_location').annotate(dcount=Count('hall_location'))
        for i in booking_detail_list:
            booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj,
                                                                  hall_location=i['hall_location']).last()
            hall_location = booking_detail_obj.hall_location.location

            if hall_location == 'MCCIA Trade Tower (5th Floor)':
                booking_detail_obj.pi_no = int(booking_sb_obj.pi_no) + 1
            elif hall_location == 'Tilak Road':
                booking_detail_obj.pi_no = int(booking_tilak_obj.pi_no) + 1
            elif hall_location == 'Bhosari':
                booking_detail_obj.pi_no = int(booking_bhosari_obj.pi_no) + 1
            elif hall_location == 'Hadapsar':
                booking_detail_obj.pi_no = int(booking_hadapsar_obj.pi_no) + 1

            booking_detail_obj.save()

        user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)

        if request.POST.get('retain_sd_flag') == 'false' and user_track_obj.deposit_available >0: 
            print '......3....' 
            hall_booking_obj.deposit = user_track_obj.deposit_available
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.gst_amount, 0)
            # hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            # hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
            # hall_booking_payment_obj.save()


            hall_booking_obj.deposit_status = 1
            hall_booking_obj.save()
            user_track_obj.deposit_available = 0
            user_track_obj.deposit_status = 1
            user_track_obj.save()

        if request.POST.get('cheque_flag') == 'true': 
            print '......4....' 
            hall_booking_obj.deposit = 0
            hall_booking_obj.is_deposit_through_cheque = True
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.gst_amount, 0)
            print "------------hall_booking_obj.total_payable--------------------",hall_booking_obj.total_payable
            # hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            # hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
            # hall_booking_payment_obj.save()            
            if request.POST.get('retain_sd_flag') == 'true':
                hall_booking_obj.deposit_status = 0
            hall_booking_obj.save()
            user_track_obj.deposit_available = 0
            user_track_obj.deposit_status = 1
            user_track_obj.save()


###################################################

        hall_booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).first()

        total_amount = int(round(hall_booking_obj.total_payable - hall_booking_obj.deposit, 2))
        # total_amount = 1
        consumer_name = str(hall_booking_obj.name)
        consumerMobileNo = str(hall_booking_detail_obj.mobile_no)
        consumerEmailId = str(hall_booking_detail_obj.email)

        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True)
        sb_pi_no = ''
        tilak_pi_no = ''
        bpi_pi_no = ''
        hpi_pi_no = ''
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        get_financial = get_financial_year(current_date)        

        for item in booking_detail_list:
            hall_location = item.hall_location.location
            if hall_location == 'MCCIA Trade Tower (5th Floor)':
                sb_pi_no = 'PI/'+str(get_financial)+'/'+str(item.pi_no)
            elif hall_location == 'Tilak Road':
                tilak_pi_no = 'TPI/'+str(get_financial)+'/'+str(item.pi_no) 
            elif hall_location == 'Bhosari':
                bpi_pi_no = 'BPI/'+str(get_financial)+'/'+str(item.pi_no)
            elif hall_location == 'Hadapsar':
                hpi_pi_no = 'HPI/'+str(get_financial)+'/'+str(item.pi_no)

        final_pi_no = sb_pi_no + ' ' + tilak_pi_no + ' ' + bpi_pi_no + ' ' +  hpi_pi_no         

        #merchant_id = 'T172654'
        #salt = '2093514954UVQFBK'
        merchant_id = 'L172655'
        salt='6790264316SSAGPJ'
        # merchant_id = 'L172654'
        # salt = '2093514954UVQFBK'
        itemId = 'MCCI'  # scheme code
        transaction_id = str(hall_booking_detail_obj.hall_booking.booking_no) + '_' + str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        try:
            HallPaymentTransaction_obj = HallPaymentTransaction(
                transaction_id=transaction_id,
                hall_booking=hall_booking_obj,
                reg_no=str(hall_booking_obj.booking_no),
                merchant_id=merchant_id,
                total_amount=total_amount,
                consumer_name=consumer_name,
                consumer_mobile_no=consumerMobileNo,
                consumer_email=consumerEmailId
            )
            HallPaymentTransaction_obj.save()

            m = hashlib.sha512()

            parameters = {'PI_no': str(final_pi_no),
                          'party_name': str(hall_booking_obj.name)}
            cart_desc = str(json.dumps(parameters))
            cart_desc = cart_desc.replace('"', '')               

            msg = merchant_id + "|"  # consumerData.merchantId|
            msg += str(transaction_id) + "|"  # consumerData.txnId|
            msg += str(total_amount) + "|"  # totalamount|
            msg += "" + "|"  # consumerData.accountNo|
            msg += "" + "|"  # consumerData.consumerId|
            msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
            msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
            msg += "" + "|"  # consumerData.debitStartDate|
            msg += "" + "|"  # consumerData.debitEndDate|
            msg += "" + "|"  # consumerData.maxAmount|
            msg += "" + "|"  # consumerData.amountType|
            msg += "" + "|"  # consumerData.frequency|
            msg += "" + "|"  # consumerData.cardNumber|
            msg += "" + "|"  # consumerData. expMonth|
            msg += "" + "|"  # consumerData.expYear|
            msg += "" + "|"  # consumerData.cvvCode|
            msg += salt  # salt

            print msg

            m.update(msg)
            configJson = {
                'tarCall': False,
                'features': {
                    'showPGResponseMsg': True,
                    'enableNewWindowFlow': True
                },
                'consumerData': {
                    'deviceId': 'WEBSH2',
                    'token': str(m.hexdigest()),
                    'responseHandler': 'handleResponse',
                    'paymentMode': 'all',
                    'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                    'merchantId': merchant_id,
                    'currency': 'INR',
                    'consumerId': '',
                    'consumerMobileNo': consumerMobileNo,
                    'consumerEmailId': consumerEmailId,
                    'txnId': str(transaction_id),
                    'cardNumber': '',
                    'expMonth': '',
                    'expYear': '',
                    'cvvCode': '',
                    'amount_type': '',
                    'frequency': '',
                    'amountType': '',
                    'debitStartDate': '',
                    'debitEndDate': '',
                    'maxAmount': '',
                    'accountNo': '',
                    'items': [{
                        'itemId': itemId,
                        'amount': str(total_amount),
                        'comAmt': '0'
                    }],
                    'cartDescription': cart_desc,                       
                    'customStyle': {
                        'PRIMARY_COLOR_CODE': '#3977b7',
                        'SECONDARY_COLOR_CODE': '#FFFFFF',
                        'BUTTON_COLOR_CODE_1': '#1969bb',
                        'BUTTON_COLOR_CODE_2': '#FFFFFF'
                    }
                }
            }
            transaction.savepoint_commit(sid)
            data = {'configJson': configJson, 'success': 'true'}
        except Exception, e:
            print '\nException IN | common.py | get_hall_payment_detail | Excp = ', str(traceback.print_exc())
            pass
            transaction.rollback(sid)
            data = {'success': 'false'}
    except Exception, e:
        print '\nException IN | common.py | get_hall_payment_detail | Excp = ', str(traceback.print_exc())
        pass
        transaction.rollback(sid)
        data = {'success': 'false'}
    print data
    print '\nResponse OUT | common.py | get_hall_payment_detail | User = ', request.user
    return HttpResponse(json.dumps(data), content_type='application/json')


# Save Payment Response
@csrf_exempt
@transaction.atomic
def hall_response_save(request):
    sid = transaction.savepoint()
    # print '\nrequest.POST = ', request.POST
    # print '\nbooking_id = ', request.POST.get('booking_id')

    data = request.POST
    response_data = {}
    try:
        print '\nResponse IN | common.py | hall_response_save | User = ', request.user

        salt = '6790264316SSAGPJ'
        # salt = '2093514954UVQFBK'
        stringResponse=data['stringResponse']
        stringResponse_list=stringResponse.split('|')
        txn_status = stringResponse_list[0]
        txn_msg = stringResponse_list[1]
        txn_err_msg = stringResponse_list[2]
        clnt_txn_ref = stringResponse_list[3]
        tpsl_bank_cd = stringResponse_list[4]
        tpsl_txn_id = stringResponse_list[5]
        txn_amt = stringResponse_list[6]
        clnt_rqst_meta = stringResponse_list[7]
        tpsl_txn_time = stringResponse_list[8]
        bal_amt = stringResponse_list[9]
        card_id = stringResponse_list[10]
        alias_name = stringResponse_list[11]
        bank_transaction_id = stringResponse_list[12]
        mandate_reg_no = stringResponse_list[13]
        token = stringResponse_list[14]
        hash = stringResponse_list[15]

        msg = txn_status
        msg += '|' +txn_msg
        msg += '|' +txn_err_msg
        msg += '|' +clnt_txn_ref
        msg += '|' +tpsl_bank_cd
        msg += '|' +tpsl_txn_id
        msg += '|' +txn_amt
        msg += '|' +clnt_rqst_meta
        msg += '|' +tpsl_txn_time
        msg += '|' +bal_amt
        msg += '|' +card_id
        msg += '|' +alias_name
        msg += '|' +bank_transaction_id
        msg += '|' +mandate_reg_no
        msg += '|' +token
        msg += '|' + salt

        m = hashlib.sha512()
        m.update(msg)
        hex_msg = m.hexdigest()
        is_hash_match = hex_msg == hash

        try:
            statusCode = data['statusCode']  # 0300=Success,0398=Initiated,0399=failure,0396=Aborted
            responseType = data['responseType']  # hasg algo name
            errorMessage = data['errorMessage']
            accountNo = data['accountNo']
            reference = data['reference']
            bankReferenceIdentifier = data['bankReferenceIdentifier']
            merchantTransactionIdentifier = data['merchantTransactionIdentifier']
            merchantAdditionalDetails = data['merchantAdditionalDetails']
            dateTime = data['dateTime']  # convert to datetime object
            amount = data['amount']
            statusMessage = data['statusMessage']
            balanceAmount = data['balanceAmount']
            error = data['error']
            identifier = data['identifier']
            merchantTransactionRequestType = data['merchantTransactionRequestType']
            refundIdentifier = data['refundIdentifier']
            transactionState = data['transactionState']

            paymenttransactionobj = HallPaymentTransaction.objects.get(transaction_id=merchantTransactionIdentifier)

            paymenttransactionobj.txn_status = txn_status #statusCode
            paymenttransactionobj.txn_msg = txn_msg #statusMessage
            paymenttransactionobj.txn_err_msg = txn_err_msg #errorMessage
            paymenttransactionobj.clnt_txn_ref = clnt_txn_ref
            paymenttransactionobj.tpsl_bank_cd = tpsl_bank_cd
            paymenttransactionobj.tpsl_txn_id = tpsl_txn_id #identifier
            paymenttransactionobj.txn_amt = txn_amt
            paymenttransactionobj.clnt_rqst_meta = clnt_rqst_meta
            paymenttransactionobj.tpsl_txn_time = tpsl_txn_time
            paymenttransactionobj.bal_amt = bal_amt
            paymenttransactionobj.card_id = card_id
            paymenttransactionobj.alias_name = alias_name
            paymenttransactionobj.bank_transaction_id = bank_transaction_id
            paymenttransactionobj.mandate_reg_no = mandate_reg_no
            paymenttransactionobj.save()

            if statusCode == '0300' and is_hash_match:
                # Paid Successfully
                hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                hall_booking_obj.booking_status = 6
                hall_booking_obj.payment_method = 1
                hall_booking_obj.payment_status = 1
                hall_booking_obj.paid_amount = Decimal(txn_amt)
                hall_booking_obj.save()

                paymenttransactionobj.payment_status = 1
                paymenttransactionobj.save()

                for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                    hall_booking_detail.booking_status = 6
                    hall_booking_detail.save()
                    for hall_check_avail in HallCheckAvailability.objects.filter(
                            hall_booking_detail=hall_booking_detail):
                        hall_check_avail.booking_status = 6
                        hall_check_avail.save()

                booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                        payable_amount=hall_booking_obj.total_payable,
                                                        paid_amount=hall_booking_obj.paid_amount,
                                                        payment_status=1,
                                                        payment_date=datetime.datetime.now())
                booking_payment_obj.save()


#############################################
                if hall_booking_obj.user_track:
                    if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:  
                        if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                            user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)     
                            user_track_obj.deposit_available = hall_booking_obj.deposit  
                            user_track_obj.deposit_status = 0
                            user_track_obj.refund_status = 0
                            user_track_obj.save()     

                            exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),Q(is_completed = False),~Q(booking_status__in=[0,10])).exclude(id=hall_booking_obj.id)       
                            for hall_obj in exclude_hall_booking_list:
                                exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)
                                
                                if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                    exclude_hall_obj.is_deposit_through_cheque = False
                                    exclude_hall_obj.deposit_status = 0
                                    exclude_hall_obj.save()
                                    HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(is_deleted=True)
                                elif exclude_hall_obj.deposit:
                                    if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                        exclude_hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj).last()
                                        exclude_total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

                                        exclude_hall_obj.deposit = 0
                                        exclude_hall_obj.save()
                                        exclude_hall_obj.total_payable = round(exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount, 0)
                                        exclude_hall_obj.save()
                                        exclude_hall_payment_obj.payable_amount = Decimal(exclude_hall_obj.total_payable) - Decimal(exclude_total_paid_dict['total_paid'])
                                        exclude_hall_payment_obj.save()


##################################################                                            
                transaction.savepoint_commit(sid)
                send_mail_count = "FIRST"
                send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                response_data['success'] = 'true'
                pass
            elif statusCode == '0398' and is_hash_match:
                # Transaction Initiated. Add Entry in Pending Transaction
                hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                hall_booking_obj.booking_status = 8
                hall_booking_obj.save()

                paymenttransactionobj.payment_status = 2
                paymenttransactionobj.save()

                for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                    hall_booking_detail.booking_status = 8
                    hall_booking_detail.save()
                    for hall_check_avail in HallCheckAvailability.objects.filter(
                            hall_booking_detail=hall_booking_detail):
                        hall_check_avail.booking_status = 8
                        hall_check_avail.save()

                booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                        payable_amount=hall_booking_obj.total_payable,
                                                        paid_amount=hall_booking_obj.paid_amount,
                                                        payment_status=8,
                                                        payment_date=datetime.datetime.now())
                booking_payment_obj.save()


#############################################
                if hall_booking_obj.user_track:
                    if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:  
                        if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                            user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)     
                            user_track_obj.deposit_available = hall_booking_obj.deposit  
                            user_track_obj.deposit_status = 0
                            user_track_obj.refund_status = 0
                            user_track_obj.save()     

                            exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),Q(is_completed = False),~Q(booking_status__in=[0,10])).exclude(id=hall_booking_obj.id)       
                            for hall_obj in exclude_hall_booking_list:
                                exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)
                                
                                if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                    exclude_hall_obj.is_deposit_through_cheque = False
                                    exclude_hall_obj.deposit_status = 0
                                    exclude_hall_obj.save()
                                    HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(is_deleted=True)
                                elif exclude_hall_obj.deposit:
                                    if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                        exclude_hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj).last()
                                        exclude_total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

                                        exclude_hall_obj.deposit = 0
                                        exclude_hall_obj.save()
                                        exclude_hall_obj.total_payable = round(exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount, 0)
                                        exclude_hall_obj.save()
                                        exclude_hall_payment_obj.payable_amount = Decimal(exclude_hall_obj.total_payable) - Decimal(exclude_total_paid_dict['total_paid'])
                                        exclude_hall_payment_obj.save()



##################################################                  
                transaction.savepoint_commit(sid)
                send_mail_count = "FIRST"
                add_to_pending(paymenttransactionobj.id)
                send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                response_data['success'] = 'initiated'
                pass
            elif statusCode == '0399' and is_hash_match:
                # Failed Transaction

                # hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                # hall_booking_obj.booking_status = 0
                # hall_booking_obj.save()
                #
                # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                #     hall_booking_detail.booking_status = 0
                #     hall_booking_detail.save()
                #     for hall_check_avail in HallCheckAvailability.objects.filter(
                #             hall_booking_detail=hall_booking_detail):
                #         hall_check_avail.booking_status = 0
                #         hall_check_avail.save()
                # transaction.savepoint_commit(sid)

                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                pass
            elif statusCode == '0396' and is_hash_match:
                # Cancelled by User

                # hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                # hall_booking_obj.booking_status = 0
                # hall_booking_obj.save()
                #
                # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                #     hall_booking_detail.booking_status = 0
                #     hall_booking_detail.save()
                #     for hall_check_avail in HallCheckAvailability.objects.filter(
                #             hall_booking_detail=hall_booking_detail):
                #         hall_check_avail.booking_status = 0
                #         hall_check_avail.save()

                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                response_data['success'] = 'cancelled'
                pass
            elif is_hash_match:
                # code if hash is matched but no status code
                pass

            elif not is_hash_match and statusCode in ['0300', '0398', '0399', '0396']:
                paymenttransactionobj.is_hash_matched = False
                paymenttransactionobj.save()

                if statusCode == '0300':
                    hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                    hall_booking_obj.booking_status = 6
                    hall_booking_obj.payment_method = 1
                    hall_booking_obj.payment_status = 1
                    hall_booking_obj.paid_amount = Decimal(txn_amt)
                    hall_booking_obj.save()

                    paymenttransactionobj.payment_status = 1
                    paymenttransactionobj.save()

                    for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                        hall_booking_detail.booking_status = 6
                        hall_booking_detail.save()
                        for hall_check_avail in HallCheckAvailability.objects.filter(
                                hall_booking_detail=hall_booking_detail):
                            hall_check_avail.booking_status = 6
                            hall_check_avail.save()

                    booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                            payable_amount=hall_booking_obj.total_payable,
                                                            paid_amount=hall_booking_obj.paid_amount,
                                                            payment_status=1,
                                                            payment_date=datetime.datetime.now())
                    booking_payment_obj.save()


    #############################################
                    if hall_booking_obj.user_track:
                        if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:  
                            if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)     
                                user_track_obj.deposit_available = hall_booking_obj.deposit  
                                user_track_obj.deposit_status = 0
                                user_track_obj.refund_status = 0
                                user_track_obj.save()     

                                exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),Q(is_completed = False),~Q(booking_status__in=[0,10])).exclude(id=hall_booking_obj.id)       
                                for hall_obj in exclude_hall_booking_list:
                                    exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)
                                    
                                    if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                        exclude_hall_obj.is_deposit_through_cheque = False
                                        exclude_hall_obj.deposit_status = 0
                                        exclude_hall_obj.save()
                                        HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(is_deleted=True)
                                    elif exclude_hall_obj.deposit:
                                        if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                            exclude_hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj).last()
                                            exclude_total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

                                            exclude_hall_obj.deposit = 0
                                            exclude_hall_obj.save()
                                            exclude_hall_obj.total_payable = round(exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount, 0)
                                            exclude_hall_obj.save()
                                            exclude_hall_payment_obj.payable_amount = Decimal(exclude_hall_obj.total_payable) - Decimal(exclude_total_paid_dict['total_paid'])
                                            exclude_hall_payment_obj.save()


    ##################################################  

                    transaction.savepoint_commit(sid)
                    send_mail_count = "FIRST"
                    send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                    send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                    response_data['success'] = 'true'

                elif statusCode == '0398':
                    # Transaction Initiated. Add Entry in Pending Transaction
                    hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                    hall_booking_obj.booking_status = 8
                    hall_booking_obj.save()

                    paymenttransactionobj.payment_status = 2
                    paymenttransactionobj.save()

                    for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                        hall_booking_detail.booking_status = 8
                        hall_booking_detail.save()
                        for hall_check_avail in HallCheckAvailability.objects.filter(
                                hall_booking_detail=hall_booking_detail):
                            hall_check_avail.booking_status = 8
                            hall_check_avail.save()

                    booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                            payable_amount=hall_booking_obj.total_payable,
                                                            paid_amount=hall_booking_obj.paid_amount,
                                                            payment_status=8,
                                                            payment_date=datetime.datetime.now())
                    booking_payment_obj.save()

    #############################################
                    if hall_booking_obj.user_track:
                        if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:  
                            if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)     
                                user_track_obj.deposit_available = hall_booking_obj.deposit  
                                user_track_obj.deposit_status = 0
                                user_track_obj.refund_status = 0
                                user_track_obj.save()     

                                exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),Q(is_completed = False),~Q(booking_status__in=[0,10])).exclude(id=hall_booking_obj.id)       
                                for hall_obj in exclude_hall_booking_list:
                                    exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)
                                    
                                    if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                        exclude_hall_obj.is_deposit_through_cheque = False
                                        exclude_hall_obj.deposit_status = 0
                                        exclude_hall_obj.save()
                                        HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(is_deleted=True)
                                    elif exclude_hall_obj.deposit:

                                        if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                            exclude_hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj).last()
                                            exclude_total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

                                            exclude_hall_obj.deposit = 0
                                            exclude_hall_obj.save()
                                            exclude_hall_obj.total_payable = round(exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount, 0)
                                            exclude_hall_obj.save()
                                            exclude_hall_payment_obj.payable_amount = Decimal(exclude_hall_obj.total_payable) - Decimal(exclude_total_paid_dict['total_paid'])
                                            exclude_hall_payment_obj.save()


    ##################################################  

                    transaction.savepoint_commit(sid)
                    send_mail_count = "FIRST"
                    add_to_pending(paymenttransactionobj.id)
                    send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                    send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                    response_data['success'] = 'initiated'
                elif statusCode == '0399':
                    # Failed Transaction
                    paymenttransactionobj.payment_status = 3
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'failed'
                elif statusCode == '0396':
                    # Cancelled by User
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.save()

                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'cancelled'
                # code if hash code is not matched and with match statusCode
                pass

            else:
                # code if hash code is not matched and without match statusCode
                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                pass

            # transaction.savepoint_commit(sid)

        except Exception, e:
            log.debug('Error = {0}\n'.format(e))
            print e
            pass

    except Exception,e:
        print e
        transaction.rollback(sid)
        response_data['success'] = 'false'
        pass
    print '\nResponse Data hall_response_save = ', response_data
    print '\nResponse OUT | common.py | hall_response_save | User = ', request.user
    return HttpResponse(json.dumps(response_data), content_type='application/json')


# Membership
@csrf_exempt
@transaction.atomic
def get_membership_payment_detail(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | common.py | get_membership_payment_detail | User = ', request.user
        payment_obj = ''
        print "request.POST.get('payment_id') =========================== ", request.POST.get('payment_id')
        if request.POST.get('payment_id'):
            payment_obj = PaymentDetails.objects.get(id=request.POST.get('payment_id'))
        else:
            response_data = save_new_member(request)
            if response_data['success']:
                payment_obj = PaymentDetails.objects.get(id=response_data['payment_id'])
            else:
                print '\nMEMBER SAVE ERROR'
                return

        total_amount = int(round(payment_obj.membershipInvoice.amount_payable, 2))
        # total_amount = '1'
        consumer_name = str(payment_obj.userdetail.company.company_name)
        if payment_obj.userdetail.enroll_type == 'CO':
            consumerMobileNo = str(payment_obj.userdetail.ceo_cellno)
        else:
            consumerMobileNo = str(payment_obj.userdetail.correspond_landline1)
        consumerEmailId =  str(payment_obj.userdetail.ceo_email)

        merchant_id = 'L172654'
        salt = '2093514954UVQFBK'
        # merchant_id = 'T172654'
        # salt = '2093514954UVQFBK'
        itemId = 'MCCI'  # scheme code
        transaction_id = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        try:
            MembershipPaymentTransaction_obj = MembershipPaymentTransaction(
                transaction_id=transaction_id,
                membership_invoice=payment_obj.membershipInvoice,
                payment_detail=payment_obj,
                reg_no=str(payment_obj.bk_no),
                merchant_id=merchant_id,
                total_amount=total_amount,
                consumer_name=consumer_name,
                consumer_mobile_no=consumerMobileNo,
                consumer_email=consumerEmailId
            )
            MembershipPaymentTransaction_obj.save()

            m = hashlib.sha512()
            if payment_obj.userdetail.member_associate_no:
                parameters = {'company_name': str(payment_obj.userdetail.company.company_name),
                              'membership_no': str(payment_obj.userdetail.member_associate_no)}
            else:
                parameters = {'company_name': str(payment_obj.userdetail.company.company_name),
                              'membership_no': 'NEW'}
            cart_desc = str(json.dumps(parameters))
            cart_desc = cart_desc.replace('"', '')

            msg = merchant_id + "|"  # consumerData.merchantId|
            msg += str(transaction_id) + "|"  # consumerData.txnId|
            msg += str(total_amount) + "|"  # totalamount|
            msg += "" + "|"  # consumerData.accountNo|
            msg += "" + "|"  # consumerData.consumerId|
            msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
            msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
            msg += "" + "|"  # consumerData.debitStartDate|
            msg += "" + "|"  # consumerData.debitEndDate|
            msg += "" + "|"  # consumerData.maxAmount|
            msg += "" + "|"  # consumerData.amountType|
            msg += "" + "|"  # consumerData.frequency|
            msg += "" + "|"  # consumerData.cardNumber|
            msg += "" + "|"  # consumerData. expMonth|
            msg += "" + "|"  # consumerData.expYear|
            msg += "" + "|"  # consumerData.cvvCode|
            msg += salt  # salt

            print msg

            m.update(msg)
            configJson = {
                'tarCall': False,
                'features': {
                    'showPGResponseMsg': True,
                    'enableNewWindowFlow': True
                },
                'consumerData': {
                    'deviceId': 'WEBSH2',
                    'token': str(m.hexdigest()),
                    'responseHandler': 'handleResponse',
                    'paymentMode': 'all',
                    'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                    'merchantId': merchant_id,
                    'currency': 'INR',
                    'consumerId': '',
                    'consumerMobileNo': consumerMobileNo,
                    'consumerEmailId': consumerEmailId,
                    'txnId': str(transaction_id),
                    'cardNumber': '',
                    'expMonth': '',
                    'expYear': '',
                    'cvvCode': '',
                    'amount_type': '',
                    'frequency': '',
                    'amountType': '',
                    'debitStartDate': '',
                    'debitEndDate': '',
                    'maxAmount': '',
                    'accountNo': '',
                    'items': [{
                        'itemId': itemId,
                        'amount': str(total_amount),
                        'comAmt': '0'
                    }],
                    'cartDescription': cart_desc,
                    'customStyle': {
                        'PRIMARY_COLOR_CODE': '#3977b7',
                        'SECONDARY_COLOR_CODE': '#FFFFFF',
                        'BUTTON_COLOR_CODE_1': '#1969bb',
                        'BUTTON_COLOR_CODE_2': '#FFFFFF'
                    }
                }
            }
            transaction.savepoint_commit(sid)
            data = {'configJson': configJson, 'success': 'true', 'payment_obj_id': str(payment_obj.id)}
        except Exception, e:
            print e
            print '\nException IN | common.py | get_membership_payment_detail | Excp = ', str(traceback.print_exc())
            pass
            transaction.rollback(sid)
            data = {'success': 'false'}
    except Exception, e:
        print e
        print '\nException IN | common.py | get_membership_payment_detail | Excp = ', str(traceback.print_exc())
        pass
        transaction.rollback(sid)
        data = {'success': 'false'}
    print data
    print '\nResponse OUT | common.py | get_membership_payment_detail | User = ', request.user
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@transaction.atomic
def membership_response_save(request):
    sid = transaction.savepoint()
    data = request.POST
    response_data = {}
    try:
        print '\nResponse IN | common.py | membership_response_save | User = ', request.user

        salt = '2093514954UVQFBK'
        stringResponse=data['stringResponse']
        stringResponse_list=stringResponse.split('|')
        txn_status = stringResponse_list[0]
        txn_msg = stringResponse_list[1]
        txn_err_msg = stringResponse_list[2]
        clnt_txn_ref = stringResponse_list[3]
        tpsl_bank_cd = stringResponse_list[4]
        tpsl_txn_id = stringResponse_list[5]
        txn_amt = stringResponse_list[6]
        clnt_rqst_meta = stringResponse_list[7]
        tpsl_txn_time = stringResponse_list[8]
        bal_amt = stringResponse_list[9]
        card_id = stringResponse_list[10]
        alias_name = stringResponse_list[11]
        bank_transaction_id = stringResponse_list[12]
        mandate_reg_no = stringResponse_list[13]
        token = stringResponse_list[14]
        hash = stringResponse_list[15]

        msg = txn_status
        msg += '|' +txn_msg
        msg += '|' +txn_err_msg
        msg += '|' +clnt_txn_ref
        msg += '|' +tpsl_bank_cd
        msg += '|' +tpsl_txn_id
        msg += '|' +txn_amt
        msg += '|' +clnt_rqst_meta
        msg += '|' +tpsl_txn_time
        msg += '|' +bal_amt
        msg += '|' +card_id
        msg += '|' +alias_name
        msg += '|' +bank_transaction_id
        msg += '|' +mandate_reg_no
        msg += '|' +token
        msg += '|' + salt

        m = hashlib.sha512()
        m.update(msg)
        hex_msg = m.hexdigest()
        is_hash_match = hex_msg == hash

        try:
            statusCode = data['statusCode']  # 0300=Success,0398=Initiated,0399=failure,0396=Aborted,0392=CancelledByUser
            responseType = data['responseType']  # hasg algo name
            errorMessage = data['errorMessage']
            accountNo = data['accountNo']
            reference = data['reference']
            bankReferenceIdentifier = data['bankReferenceIdentifier']
            merchantTransactionIdentifier = data['merchantTransactionIdentifier']
            merchantAdditionalDetails = data['merchantAdditionalDetails']
            dateTime = data['dateTime']  # convert to datetime object
            amount = data['amount']
            statusMessage = data['statusMessage']
            balanceAmount = data['balanceAmount']
            error = data['error']
            identifier = data['identifier']
            merchantTransactionRequestType = data['merchantTransactionRequestType']
            refundIdentifier = data['refundIdentifier']
            transactionState = data['transactionState']

            paymenttransactionobj = MembershipPaymentTransaction.objects.get(transaction_id=merchantTransactionIdentifier)

            paymenttransactionobj.txn_status = txn_status #statusCode
            paymenttransactionobj.txn_msg = txn_msg #statusMessage
            paymenttransactionobj.txn_err_msg = txn_err_msg #errorMessage
            paymenttransactionobj.clnt_txn_ref = clnt_txn_ref
            paymenttransactionobj.tpsl_bank_cd = tpsl_bank_cd
            paymenttransactionobj.tpsl_txn_id = tpsl_txn_id #identifier
            paymenttransactionobj.txn_amt = txn_amt
            paymenttransactionobj.clnt_rqst_meta = clnt_rqst_meta
            paymenttransactionobj.tpsl_txn_time = tpsl_txn_time
            paymenttransactionobj.bal_amt = bal_amt
            paymenttransactionobj.card_id = card_id
            paymenttransactionobj.alias_name = alias_name
            paymenttransactionobj.bank_transaction_id = bank_transaction_id
            paymenttransactionobj.mandate_reg_no = mandate_reg_no
            paymenttransactionobj.save()

            payment_obj = PaymentDetails.objects.get(id=paymenttransactionobj.payment_detail.id)
            invoice_obj = MembershipInvoice.objects.get(id=paymenttransactionobj.membership_invoice.id)
            user_detail_obj = UserDetail.objects.get(id=invoice_obj.userdetail.id)

            if statusCode == '0300' and is_hash_match:
                # Paid Successfully
                print '\nSuccess'
                payment_obj.amount_paid = Decimal(txn_amt)
                payment_obj.payment_date = datetime.date.today()
                payment_obj.payment_received_status = 'Paid'
                payment_obj.user_Payment_Type = 'Online'
                payment_obj.neft_transfer_id = 'Paid_Online'
                payment_obj.save()

                # Save MBK Number
                bk_no = 'MBK' + str(payment_obj.id).zfill(7)
                payment_obj.bk_no = str(bk_no)
                payment_obj.save()

                invoice_obj.is_paid = True
                invoice_obj.save()

                user_detail_obj.valid_invalid_member = True
                user_detail_obj.payment_method = 'Online Pending'
                user_detail_obj.save()

                paymenttransactionobj.payment_status = 1
                paymenttransactionobj.payment_mode = 1
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                membership_details.send_mail_online_payment(payment_obj, invoice_obj, user_detail_obj)
                response_data['success'] = 'true'
                # pass
            elif statusCode == '0398' and is_hash_match:
                # Transaction Initiated. Add Entry in Pending Transaction
                print '\nInitiated'
                paymenttransactionobj.payment_status = 2
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                add_to_pending(paymenttransactionobj.id)
                membership_details.send_mail_online_payment(payment_obj, invoice_obj, user_detail_obj)
                response_data['success'] = 'initiated'
                # pass
            elif statusCode == '0399' and is_hash_match:
                # Failed Transaction
                print '\nFailed'
                user_detail_obj.payment_method = 'Failed'
                user_detail_obj.save()
                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                response_data['payment_id'] = str(payment_obj.id)
                # pass
            elif statusCode == '0396' and is_hash_match:
                # Cancelled by User
                print '\nCancelled'
                user_detail_obj.payment_method = 'Failed'
                user_detail_obj.save()
                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                response_data['success'] = 'cancelled'
                response_data['payment_id'] = str(payment_obj.id)
                # pass
            elif statusCode == '0392' and is_hash_match:
                print '\nCancelled by user'
                user_detail_obj.payment_method = 'Failed'
                user_detail_obj.save()
                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                response_data['success'] = 'cancelled'
                response_data['payment_id'] = str(payment_obj.id)
                # pass
            elif is_hash_match:
                # code if hash is matched but no status code
                pass

            elif not is_hash_match and statusCode in ['0300', '0398', '0399', '0396', '0392']:
                paymenttransactionobj.is_hash_matched = False
                paymenttransactionobj.save()

                if statusCode == '0300':
                    print '\nSuccess not hash'
                    payment_obj.amount_paid = Decimal(txn_amt)
                    payment_obj.payment_date = datetime.date.today()
                    payment_obj.payment_received_status = 'Paid'
                    payment_obj.user_Payment_Type = 'Online'
                    payment_obj.neft_transfer_id = 'Paid_Online'
                    payment_obj.save()

                    # Save MBK Number
                    bk_no = 'MBK' + str(payment_obj.id).zfill(7)
                    payment_obj.bk_no = str(bk_no)
                    payment_obj.save()

                    invoice_obj.is_paid = True
                    invoice_obj.save()

                    user_detail_obj.valid_invalid_member = True
                    user_detail_obj.payment_method = 'Online Pending'
                    user_detail_obj.save()

                    paymenttransactionobj.payment_status = 1
                    paymenttransactionobj.payment_mode = 1
                    paymenttransactionobj.save()

                    transaction.savepoint_commit(sid)
                    membership_details.send_mail_online_payment(payment_obj, invoice_obj, user_detail_obj)
                    response_data['success'] = 'true'
                elif statusCode == '0398':
                    print '\nInitiated not hash'
                    paymenttransactionobj.payment_status = 2
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    add_to_pending(paymenttransactionobj.id)
                    membership_details.send_mail_online_payment(payment_obj, invoice_obj, user_detail_obj)
                    response_data['success'] = 'initiated'
                elif statusCode == '0399':
                    print '\nFailed not hash'
                    user_detail_obj.payment_method = 'Failed'
                    user_detail_obj.save()
                    paymenttransactionobj.payment_status = 3
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'failed'
                    response_data['payment_id'] = str(payment_obj.id)
                elif statusCode == '0396':
                    print '\nCancelled not hash'
                    user_detail_obj.payment_method = 'Failed'
                    user_detail_obj.save()
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.save()

                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'cancelled'
                    response_data['payment_id'] = str(payment_obj.id)
                elif statusCode == '0392':
                    print '\nCancelled by user not hash'
                    user_detail_obj.payment_method = 'Failed'
                    user_detail_obj.save()
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'cancelled'
                    response_data['payment_id'] = str(payment_obj.id)
                # code if hash code is not matched and with match statusCode
                pass

            else:
                print '\nLast Else'
                # code if hash code is not matched and without match statusCode
                pass

            # transaction.savepoint_commit(sid)

        except Exception, e:
            print e
            pass

    except Exception,e:
        print e
        transaction.rollback(sid)
        pass
        response_data['success'] = 'false'
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def pay_mccia_landing(request):
    data = {'booking_id': 88773}
    return render(request, 'payment/hall_payment_link_landing.html', data)


@transaction.atomic
@csrf_exempt
def pay_mccia(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | common.py | pay_mccia | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
        # hall_booking_obj = HallBooking.objects.get(id=88773)
        hall_booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).first()
        # total_amount = int(round(hall_booking_obj.total_payable, 2))
        total_amount = 35631
        # total_amount = 1
        consumer_name = str(hall_booking_obj.name)
        consumerMobileNo = str(hall_booking_detail_obj.mobile_no)
        consumerEmailId = str(hall_booking_detail_obj.email)

        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True)
        sb_pi_no = ''
        tilak_pi_no = ''
        bpi_pi_no = ''
        hpi_pi_no = ''
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        get_financial = get_financial_year(current_date)

        for item in booking_detail_list:
            hall_location = item.hall_location.location
            if hall_location == 'MCCIA Trade Tower (5th Floor)':
                sb_pi_no = 'PI/' + str(get_financial) + '/' + str(item.pi_no)
            elif hall_location == 'Tilak Road':
                tilak_pi_no = 'TPI/' + str(get_financial) + '/' + str(item.pi_no)
            elif hall_location == 'Bhosari':
                bpi_pi_no = 'BPI/' + str(get_financial) + '/' + str(item.pi_no)
            elif hall_location == 'Hadapsar':
                hpi_pi_no = 'HPI/' + str(get_financial) + '/' + str(item.pi_no)

        final_pi_no = sb_pi_no + ' ' + tilak_pi_no + ' ' + bpi_pi_no + ' ' + hpi_pi_no

        merchant_id = 'L172655'
        salt = '6790264316SSAGPJ'
        itemId = 'MCCI'  # scheme code
        transaction_id = str(hall_booking_detail_obj.hall_booking.booking_no) + '_' + str(
            int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        try:
            HallPaymentTransaction_obj = HallPaymentTransaction(
                transaction_id=transaction_id,
                hall_booking=hall_booking_obj,
                reg_no=str(hall_booking_obj.booking_no),
                merchant_id=merchant_id,
                total_amount=total_amount,
                consumer_name=consumer_name,
                consumer_mobile_no=consumerMobileNo,
                consumer_email=consumerEmailId
            )
            HallPaymentTransaction_obj.save()

            m = hashlib.sha512()

            parameters = {'PI_no': str(final_pi_no),
                          'party_name': str(hall_booking_obj.name)}
            cart_desc = str(json.dumps(parameters))
            cart_desc = cart_desc.replace('"', '')

            msg = merchant_id + "|"  # consumerData.merchantId|
            msg += str(transaction_id) + "|"  # consumerData.txnId|
            msg += str(total_amount) + "|"  # totalamount|
            msg += "" + "|"  # consumerData.accountNo|
            msg += "" + "|"  # consumerData.consumerId|
            msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
            msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
            msg += "" + "|"  # consumerData.debitStartDate|
            msg += "" + "|"  # consumerData.debitEndDate|
            msg += "" + "|"  # consumerData.maxAmount|
            msg += "" + "|"  # consumerData.amountType|
            msg += "" + "|"  # consumerData.frequency|
            msg += "" + "|"  # consumerData.cardNumber|
            msg += "" + "|"  # consumerData. expMonth|
            msg += "" + "|"  # consumerData.expYear|
            msg += "" + "|"  # consumerData.cvvCode|
            msg += salt  # salt

            print msg

            m.update(msg)
            configJson = {
                'tarCall': False,
                'features': {
                    'showPGResponseMsg': True,
                    'enableNewWindowFlow': True
                },
                'consumerData': {
                    'deviceId': 'WEBSH2',
                    'token': str(m.hexdigest()),
                    'responseHandler': 'handleResponse',
                    'paymentMode': 'all',
                    'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                    'merchantId': merchant_id,
                    'currency': 'INR',
                    'consumerId': '',
                    'consumerMobileNo': consumerMobileNo,
                    'consumerEmailId': consumerEmailId,
                    'txnId': str(transaction_id),
                    'cardNumber': '',
                    'expMonth': '',
                    'expYear': '',
                    'cvvCode': '',
                    'amount_type': '',
                    'frequency': '',
                    'amountType': '',
                    'debitStartDate': '',
                    'debitEndDate': '',
                    'maxAmount': '',
                    'accountNo': '',
                    'items': [{
                        'itemId': itemId,
                        'amount': str(total_amount),
                        'comAmt': '0'
                    }],
                    'cartDescription': cart_desc,
                    'customStyle': {
                        'PRIMARY_COLOR_CODE': '#3977b7',
                        'SECONDARY_COLOR_CODE': '#FFFFFF',
                        'BUTTON_COLOR_CODE_1': '#1969bb',
                        'BUTTON_COLOR_CODE_2': '#FFFFFF'
                    }
                }
            }
            transaction.savepoint_commit(sid)
            data = {'configJson': configJson, 'success': 'true'}
        except Exception, e:
            print '\nException IN | common.py | pay_mccia | Excp = ', str(traceback.print_exc())
            pass
            transaction.rollback(sid)
            data = {'success': 'false'}
    except Exception, e:
        print '\nException IN | common.py | pay_mccia | Excp = ', str(traceback.print_exc())
        pass
        transaction.rollback(sid)
        data = {'success': 'false'}
    print data
    print '\nResponse OUT | common.py | pay_mccia | User = ', request.user
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def save_hall_payment_link_response(request):
    sid = transaction.savepoint()
    data = request.POST
    response_data = {}
    try:
        print '\nRequest IN | common.py | save_hall_payment_link_response | User = ', request.user

        salt = '6790264316SSAGPJ'
        stringResponse = data['stringResponse']
        stringResponse_list = stringResponse.split('|')
        txn_status = stringResponse_list[0]
        txn_msg = stringResponse_list[1]
        txn_err_msg = stringResponse_list[2]
        clnt_txn_ref = stringResponse_list[3]
        tpsl_bank_cd = stringResponse_list[4]
        tpsl_txn_id = stringResponse_list[5]
        txn_amt = stringResponse_list[6]
        clnt_rqst_meta = stringResponse_list[7]
        tpsl_txn_time = stringResponse_list[8]
        bal_amt = stringResponse_list[9]
        card_id = stringResponse_list[10]
        alias_name = stringResponse_list[11]
        bank_transaction_id = stringResponse_list[12]
        mandate_reg_no = stringResponse_list[13]
        token = stringResponse_list[14]
        hash = stringResponse_list[15]

        msg = txn_status
        msg += '|' + txn_msg
        msg += '|' + txn_err_msg
        msg += '|' + clnt_txn_ref
        msg += '|' + tpsl_bank_cd
        msg += '|' + tpsl_txn_id
        msg += '|' + txn_amt
        msg += '|' + clnt_rqst_meta
        msg += '|' + tpsl_txn_time
        msg += '|' + bal_amt
        msg += '|' + card_id
        msg += '|' + alias_name
        msg += '|' + bank_transaction_id
        msg += '|' + mandate_reg_no
        msg += '|' + token
        msg += '|' + salt

        m = hashlib.sha512()
        m.update(msg)
        hex_msg = m.hexdigest()
        is_hash_match = hex_msg == hash

        try:
            statusCode = data['statusCode']  # 0300=Success,0398=Initiated,0399=failure,0396=Aborted
            responseType = data['responseType']  # hasg algo name
            errorMessage = data['errorMessage']
            accountNo = data['accountNo']
            reference = data['reference']
            bankReferenceIdentifier = data['bankReferenceIdentifier']
            merchantTransactionIdentifier = data['merchantTransactionIdentifier']
            merchantAdditionalDetails = data['merchantAdditionalDetails']
            dateTime = data['dateTime']  # convert to datetime object
            amount = data['amount']
            statusMessage = data['statusMessage']
            balanceAmount = data['balanceAmount']
            error = data['error']
            identifier = data['identifier']
            merchantTransactionRequestType = data['merchantTransactionRequestType']
            refundIdentifier = data['refundIdentifier']
            transactionState = data['transactionState']

            paymenttransactionobj = HallPaymentTransaction.objects.get(transaction_id=merchantTransactionIdentifier)

            paymenttransactionobj.txn_status = txn_status  # statusCode
            paymenttransactionobj.txn_msg = txn_msg  # statusMessage
            paymenttransactionobj.txn_err_msg = txn_err_msg  # errorMessage
            paymenttransactionobj.clnt_txn_ref = clnt_txn_ref
            paymenttransactionobj.tpsl_bank_cd = tpsl_bank_cd
            paymenttransactionobj.tpsl_txn_id = tpsl_txn_id  # identifier
            paymenttransactionobj.txn_amt = txn_amt
            paymenttransactionobj.clnt_rqst_meta = clnt_rqst_meta
            paymenttransactionobj.tpsl_txn_time = tpsl_txn_time
            paymenttransactionobj.bal_amt = bal_amt
            paymenttransactionobj.card_id = card_id
            paymenttransactionobj.alias_name = alias_name
            paymenttransactionobj.bank_transaction_id = bank_transaction_id
            paymenttransactionobj.mandate_reg_no = mandate_reg_no
            paymenttransactionobj.save()

            if statusCode == '0300' and is_hash_match:
                # Paid Successfully
                hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                hall_booking_obj.booking_status = 6
                hall_booking_obj.payment_method = 1
                hall_booking_obj.payment_status = 1
                hall_booking_obj.paid_amount = Decimal(txn_amt)
                hall_booking_obj.save()

                paymenttransactionobj.payment_status = 1
                paymenttransactionobj.save()

                for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                    hall_booking_detail.booking_status = 6
                    hall_booking_detail.save()
                    for hall_check_avail in HallCheckAvailability.objects.filter(
                            hall_booking_detail=hall_booking_detail):
                        hall_check_avail.booking_status = 6
                        hall_check_avail.save()

                booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                        payable_amount=hall_booking_obj.total_payable,
                                                        paid_amount=hall_booking_obj.paid_amount,
                                                        payment_status=1,
                                                        payment_date=datetime.datetime.now())
                booking_payment_obj.save()

                #############################################
                if hall_booking_obj.user_track:
                    if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                        if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                            user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                            user_track_obj.deposit_available = hall_booking_obj.deposit
                            user_track_obj.deposit_status = 0
                            user_track_obj.refund_status = 0
                            user_track_obj.save()

                            exclude_hall_booking_list = HallBooking.objects.filter(
                                Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                            for hall_obj in exclude_hall_booking_list:
                                exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                    exclude_hall_obj.is_deposit_through_cheque = False
                                    exclude_hall_obj.deposit_status = 0
                                    exclude_hall_obj.save()
                                    HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                        is_deleted=True)
                                elif exclude_hall_obj.deposit:
                                    if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                        exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj).last()
                                        exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                            total_paid=Sum('paid_amount'))

                                        exclude_hall_obj.deposit = 0
                                        exclude_hall_obj.save()
                                        exclude_hall_obj.total_payable = round(
                                            exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                            0)
                                        exclude_hall_obj.save()
                                        exclude_hall_payment_obj.payable_amount = Decimal(
                                            exclude_hall_obj.total_payable) - Decimal(
                                            exclude_total_paid_dict['total_paid'])
                                        exclude_hall_payment_obj.save()

                ##################################################
                transaction.savepoint_commit(sid)
                # send_mail_count = "FIRST"
                # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                response_data['success'] = 'true'
                pass
            elif statusCode == '0398' and is_hash_match:
                # Transaction Initiated. Add Entry in Pending Transaction
                hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                hall_booking_obj.booking_status = 8
                hall_booking_obj.save()

                paymenttransactionobj.payment_status = 2
                paymenttransactionobj.save()

                for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                    hall_booking_detail.booking_status = 8
                    hall_booking_detail.save()
                    for hall_check_avail in HallCheckAvailability.objects.filter(
                            hall_booking_detail=hall_booking_detail):
                        hall_check_avail.booking_status = 8
                        hall_check_avail.save()

                booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                        payable_amount=hall_booking_obj.total_payable,
                                                        paid_amount=hall_booking_obj.paid_amount,
                                                        payment_status=8,
                                                        payment_date=datetime.datetime.now())
                booking_payment_obj.save()

                #############################################
                if hall_booking_obj.user_track:
                    if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                        if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                            user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                            user_track_obj.deposit_available = hall_booking_obj.deposit
                            user_track_obj.deposit_status = 0
                            user_track_obj.refund_status = 0
                            user_track_obj.save()

                            exclude_hall_booking_list = HallBooking.objects.filter(
                                Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                            for hall_obj in exclude_hall_booking_list:
                                exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                    exclude_hall_obj.is_deposit_through_cheque = False
                                    exclude_hall_obj.deposit_status = 0
                                    exclude_hall_obj.save()
                                    HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                        is_deleted=True)
                                elif exclude_hall_obj.deposit:
                                    if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                        exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj).last()
                                        exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                            total_paid=Sum('paid_amount'))

                                        exclude_hall_obj.deposit = 0
                                        exclude_hall_obj.save()
                                        exclude_hall_obj.total_payable = round(
                                            exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                            0)
                                        exclude_hall_obj.save()
                                        exclude_hall_payment_obj.payable_amount = Decimal(
                                            exclude_hall_obj.total_payable) - Decimal(
                                            exclude_total_paid_dict['total_paid'])
                                        exclude_hall_payment_obj.save()

                ##################################################
                transaction.savepoint_commit(sid)
                # send_mail_count = "FIRST"
                add_to_pending(paymenttransactionobj.id)
                # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                response_data['success'] = 'initiated'
                pass
            elif statusCode == '0399' and is_hash_match:
                # Failed Transaction

                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                pass
            elif statusCode == '0396' and is_hash_match:
                # Cancelled by User

                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                response_data['success'] = 'cancelled'
                pass
            elif is_hash_match:
                # code if hash is matched but no status code
                pass

            elif not is_hash_match and statusCode in ['0300', '0398', '0399', '0396']:
                paymenttransactionobj.is_hash_matched = False
                paymenttransactionobj.save()

                if statusCode == '0300':
                    hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                    hall_booking_obj.booking_status = 6
                    hall_booking_obj.payment_method = 1
                    hall_booking_obj.payment_status = 1
                    hall_booking_obj.paid_amount = Decimal(txn_amt)
                    hall_booking_obj.save()

                    paymenttransactionobj.payment_status = 1
                    paymenttransactionobj.save()

                    for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                        hall_booking_detail.booking_status = 6
                        hall_booking_detail.save()
                        for hall_check_avail in HallCheckAvailability.objects.filter(
                                hall_booking_detail=hall_booking_detail):
                            hall_check_avail.booking_status = 6
                            hall_check_avail.save()

                    booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                            payable_amount=hall_booking_obj.total_payable,
                                                            paid_amount=hall_booking_obj.paid_amount,
                                                            payment_status=1,
                                                            payment_date=datetime.datetime.now())
                    booking_payment_obj.save()

                    #############################################
                    if hall_booking_obj.user_track:
                        if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                            if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                                user_track_obj.deposit_available = hall_booking_obj.deposit
                                user_track_obj.deposit_status = 0
                                user_track_obj.refund_status = 0
                                user_track_obj.save()

                                exclude_hall_booking_list = HallBooking.objects.filter(
                                    Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                    ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                                for hall_obj in exclude_hall_booking_list:
                                    exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                    if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                        exclude_hall_obj.is_deposit_through_cheque = False
                                        exclude_hall_obj.deposit_status = 0
                                        exclude_hall_obj.save()
                                        HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                            is_deleted=True)
                                    elif exclude_hall_obj.deposit:
                                        if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                            exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj).last()
                                            exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                                total_paid=Sum('paid_amount'))

                                            exclude_hall_obj.deposit = 0
                                            exclude_hall_obj.save()
                                            exclude_hall_obj.total_payable = round(
                                                exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                                0)
                                            exclude_hall_obj.save()
                                            exclude_hall_payment_obj.payable_amount = Decimal(
                                                exclude_hall_obj.total_payable) - Decimal(
                                                exclude_total_paid_dict['total_paid'])
                                            exclude_hall_payment_obj.save()

                    ##################################################

                    transaction.savepoint_commit(sid)
                    # send_mail_count = "FIRST"
                    # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                    # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                    response_data['success'] = 'true'

                elif statusCode == '0398':
                    # Transaction Initiated. Add Entry in Pending Transaction
                    hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                    hall_booking_obj.booking_status = 8
                    hall_booking_obj.save()

                    paymenttransactionobj.payment_status = 2
                    paymenttransactionobj.save()

                    for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                        hall_booking_detail.booking_status = 8
                        hall_booking_detail.save()
                        for hall_check_avail in HallCheckAvailability.objects.filter(
                                hall_booking_detail=hall_booking_detail):
                            hall_check_avail.booking_status = 8
                            hall_check_avail.save()

                    booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                            payable_amount=hall_booking_obj.total_payable,
                                                            paid_amount=hall_booking_obj.paid_amount,
                                                            payment_status=8,
                                                            payment_date=datetime.datetime.now())
                    booking_payment_obj.save()

                    #############################################
                    if hall_booking_obj.user_track:
                        if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                            if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                                user_track_obj.deposit_available = hall_booking_obj.deposit
                                user_track_obj.deposit_status = 0
                                user_track_obj.refund_status = 0
                                user_track_obj.save()

                                exclude_hall_booking_list = HallBooking.objects.filter(
                                    Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                    ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                                for hall_obj in exclude_hall_booking_list:
                                    exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                    if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                        exclude_hall_obj.is_deposit_through_cheque = False
                                        exclude_hall_obj.deposit_status = 0
                                        exclude_hall_obj.save()
                                        HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                            is_deleted=True)
                                    elif exclude_hall_obj.deposit:

                                        if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                            exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj).last()
                                            exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                                total_paid=Sum('paid_amount'))

                                            exclude_hall_obj.deposit = 0
                                            exclude_hall_obj.save()
                                            exclude_hall_obj.total_payable = round(
                                                exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                                0)
                                            exclude_hall_obj.save()
                                            exclude_hall_payment_obj.payable_amount = Decimal(
                                                exclude_hall_obj.total_payable) - Decimal(
                                                exclude_total_paid_dict['total_paid'])
                                            exclude_hall_payment_obj.save()

                    ##################################################

                    transaction.savepoint_commit(sid)
                    # send_mail_count = "FIRST"
                    add_to_pending(paymenttransactionobj.id)
                    # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                    # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                    response_data['success'] = 'initiated'
                elif statusCode == '0399':
                    # Failed Transaction
                    paymenttransactionobj.payment_status = 3
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'failed'
                elif statusCode == '0396':
                    # Cancelled by User
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.save()

                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'cancelled'
                # code if hash code is not matched and with match statusCode
                pass

            else:
                # code if hash code is not matched and without match statusCode
                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                pass

            # transaction.savepoint_commit(sid)

        except Exception, e:
            log.debug('Error = {0}\n'.format(e))
            print e
            pass

    except Exception, e:
        print e
        transaction.rollback(sid)
        response_data['success'] = 'false'
        pass
    print '\nResponse Data save_hall_payment_link_response = ', response_data
    print '\nResponse OUT | common.py | save_hall_payment_link_response | User = ', request.user
    return HttpResponse(json.dumps(response_data), content_type='application/json')


# pay online later code
@csrf_exempt
@transaction.atomic
def pay_online_later_through_mail(request):
        sid = transaction.savepoint()
        try:
            print '\nRequest IN | common.py | pay_online_later_through_mail | User = ', request.user
            hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
            tds_amount_manual = request.POST.get('tds_amount')

            #####################################
            user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
            print '..........1......', request.POST.get('retain_sd_flag')
            print '..........2......', request.POST.get('cheque_flag')
            if request.POST.get('retain_sd_flag') == 'false' and user_track_obj.deposit_available > 0:
                print '......3....'
                hall_booking_obj.deposit = user_track_obj.deposit_available
                hall_booking_obj.save()
                hall_booking_obj.total_payable = round(hall_booking_obj.total_rent - hall_booking_obj.paid_amount + hall_booking_obj.gst_amount, 0)

                # hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
                hall_booking_obj.save()
                # hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
                # hall_booking_payment_obj.save()

                hall_booking_obj.deposit_status = 1
                hall_booking_obj.save()
                user_track_obj.deposit_available = 0
                user_track_obj.deposit_status = 1
                user_track_obj.save()

            if request.POST.get('cheque_flag') == 'true':
                print '......4....'
                hall_booking_obj.deposit = 0
                hall_booking_obj.is_deposit_through_cheque = True
                hall_booking_obj.save()
                hall_booking_obj.total_payable = round(hall_booking_obj.total_rent - hall_booking_obj.paid_amount + hall_booking_obj.gst_amount, 0)
                # hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
                hall_booking_obj.save()
                # hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
                # hall_booking_payment_obj.save()
                if request.POST.get('retain_sd_flag') == 'true':
                    hall_booking_obj.deposit_status = 0
                hall_booking_obj.save()
                user_track_obj.deposit_available = 0
                user_track_obj.deposit_status = 1
                user_track_obj.save()

            ###################################################

            hall_booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).first()

            total_amount = int(round(hall_booking_obj.total_payable - hall_booking_obj.deposit - hall_booking_obj.paid_amount - int(tds_amount_manual), 2))
            # total_amount = 1
            consumer_name = str(hall_booking_obj.name)
            consumerMobileNo = str(hall_booking_detail_obj.mobile_no)
            consumerEmailId = str(hall_booking_detail_obj.email)

            booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True)
            sb_pi_no = ''
            tilak_pi_no = ''
            bpi_pi_no = ''
            hpi_pi_no = ''
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            get_financial = get_financial_year(current_date)

            for item in booking_detail_list:
                hall_location = item.hall_location.location
                if hall_location == 'MCCIA Trade Tower (5th Floor)':
                    sb_pi_no = 'PI/' + str(get_financial) + '/' + str(item.pi_no)
                elif hall_location == 'Tilak Road':
                    tilak_pi_no = 'TPI/' + str(get_financial) + '/' + str(item.pi_no)
                elif hall_location == 'Bhosari':
                    bpi_pi_no = 'BPI/' + str(get_financial) + '/' + str(item.pi_no)
                elif hall_location == 'Hadapsar':
                    hpi_pi_no = 'HPI/' + str(get_financial) + '/' + str(item.pi_no)

            final_pi_no = sb_pi_no + ' ' + tilak_pi_no + ' ' + bpi_pi_no + ' ' + hpi_pi_no

            # merchant_id = 'T172654'
            # salt = '2093514954UVQFBK'
            merchant_id = 'L172655'
            salt = '6790264316SSAGPJ'
            # merchant_id = 'L172654'
            # salt = '2093514954UVQFBK'
            itemId = 'MCCI'  # scheme code
            transaction_id = str(hall_booking_detail_obj.hall_booking.booking_no) + '_' + str(
                int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            try:
                HallPaymentTransaction_obj = HallPaymentTransaction(
                    transaction_id=transaction_id,
                    hall_booking=hall_booking_obj,
                    reg_no=str(hall_booking_obj.booking_no),
                    merchant_id=merchant_id,
                    total_amount=total_amount,
                    consumer_name=consumer_name,
                    consumer_mobile_no=consumerMobileNo,
                    consumer_email=consumerEmailId
                )
                HallPaymentTransaction_obj.save()

                m = hashlib.sha512()

                parameters = {'PI_no': str(final_pi_no),
                              'party_name': str(hall_booking_obj.name)}
                cart_desc = str(json.dumps(parameters))
                cart_desc = cart_desc.replace('"', '')

                msg = merchant_id + "|"  # consumerData.merchantId|
                msg += str(transaction_id) + "|"  # consumerData.txnId|
                msg += str(total_amount) + "|"  # totalamount|
                msg += "" + "|"  # consumerData.accountNo|
                msg += "" + "|"  # consumerData.consumerId|
                msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
                msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
                msg += "" + "|"  # consumerData.debitStartDate|
                msg += "" + "|"  # consumerData.debitEndDate|
                msg += "" + "|"  # consumerData.maxAmount|
                msg += "" + "|"  # consumerData.amountType|
                msg += "" + "|"  # consumerData.frequency|
                msg += "" + "|"  # consumerData.cardNumber|
                msg += "" + "|"  # consumerData. expMonth|
                msg += "" + "|"  # consumerData.expYear|
                msg += "" + "|"  # consumerData.cvvCode|
                msg += salt  # salt

                print msg

                m.update(msg)
                configJson = {
                    'tarCall': False,
                    'features': {
                        'showPGResponseMsg': True,
                        'enableNewWindowFlow': True
                    },
                    'consumerData': {
                        'deviceId': 'WEBSH2',
                        'token': str(m.hexdigest()),
                        'responseHandler': 'handleResponse',
                        'paymentMode': 'all',
                        'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                        'merchantId': merchant_id,
                        'currency': 'INR',
                        'consumerId': '',
                        'consumerMobileNo': consumerMobileNo,
                        'consumerEmailId': consumerEmailId,
                        'txnId': str(transaction_id),
                        'cardNumber': '',
                        'expMonth': '',
                        'expYear': '',
                        'cvvCode': '',
                        'amount_type': '',
                        'frequency': '',
                        'amountType': '',
                        'debitStartDate': '',
                        'debitEndDate': '',
                        'maxAmount': '',
                        'accountNo': '',
                        'items': [{
                            'itemId': itemId,
                            'amount': str(total_amount),
                            'comAmt': '0'
                        }],
                        'cartDescription': cart_desc,
                        'customStyle': {
                            'PRIMARY_COLOR_CODE': '#3977b7',
                            'SECONDARY_COLOR_CODE': '#FFFFFF',
                            'BUTTON_COLOR_CODE_1': '#1969bb',
                            'BUTTON_COLOR_CODE_2': '#FFFFFF'
                        }
                    }
                }
                transaction.savepoint_commit(sid)
                data = {'configJson': configJson, 'success': 'true'}
            except Exception, e:
                print '\nException IN | common.py | pay_online_later_through_mail | Excp = ', str(traceback.print_exc())
                pass
                transaction.rollback(sid)
                data = {'success': 'false'}
        except Exception, e:
            print '\nException IN | common.py | pay_online_later_through_mail | Excp = ', str(traceback.print_exc())
            pass
            transaction.rollback(sid)
            data = {'success': 'false'}
        print data
        print '\nResponse OUT | common.py | pay_online_later_through_mail | User = ', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')


# Save online pay later Payment Response
@csrf_exempt
@transaction.atomic
def pay_later_payment_response_save(request):
    sid = transaction.savepoint()
    # print '\nrequest.POST = ', request.POST
    # print '\nbooking_id = ', request.POST.get('booking_id')

    data = request.POST
    response_data = {}
    try:
        print '\nResponse IN | common.py | pay_later_payment_response_save | User = ', request.user

        salt = '6790264316SSAGPJ'
        # salt = '2093514954UVQFBK'
        stringResponse = data['stringResponse']
        stringResponse_list = stringResponse.split('|')
        txn_status = stringResponse_list[0]
        txn_msg = stringResponse_list[1]
        txn_err_msg = stringResponse_list[2]
        clnt_txn_ref = stringResponse_list[3]
        tpsl_bank_cd = stringResponse_list[4]
        tpsl_txn_id = stringResponse_list[5]
        txn_amt = stringResponse_list[6]
        clnt_rqst_meta = stringResponse_list[7]
        tpsl_txn_time = stringResponse_list[8]
        bal_amt = stringResponse_list[9]
        card_id = stringResponse_list[10]
        alias_name = stringResponse_list[11]
        bank_transaction_id = stringResponse_list[12]
        mandate_reg_no = stringResponse_list[13]
        token = stringResponse_list[14]
        hash = stringResponse_list[15]

        msg = txn_status
        msg += '|' + txn_msg
        msg += '|' + txn_err_msg
        msg += '|' + clnt_txn_ref
        msg += '|' + tpsl_bank_cd
        msg += '|' + tpsl_txn_id
        msg += '|' + txn_amt
        msg += '|' + clnt_rqst_meta
        msg += '|' + tpsl_txn_time
        msg += '|' + bal_amt
        msg += '|' + card_id
        msg += '|' + alias_name
        msg += '|' + bank_transaction_id
        msg += '|' + mandate_reg_no
        msg += '|' + token
        msg += '|' + salt

        m = hashlib.sha512()
        m.update(msg)
        hex_msg = m.hexdigest()
        is_hash_match = hex_msg == hash

        try:
            statusCode = data['statusCode']  # 0300=Success,0398=Initiated,0399=failure,0396=Aborted
            responseType = data['responseType']  # hasg algo name
            errorMessage = data['errorMessage']
            accountNo = data['accountNo']
            reference = data['reference']
            bankReferenceIdentifier = data['bankReferenceIdentifier']
            merchantTransactionIdentifier = data['merchantTransactionIdentifier']
            merchantAdditionalDetails = data['merchantAdditionalDetails']
            dateTime = data['dateTime']  # convert to datetime object
            amount = data['amount']
            statusMessage = data['statusMessage']
            balanceAmount = data['balanceAmount']
            error = data['error']
            identifier = data['identifier']
            merchantTransactionRequestType = data['merchantTransactionRequestType']
            refundIdentifier = data['refundIdentifier']
            transactionState = data['transactionState']

            paymenttransactionobj = HallPaymentTransaction.objects.get(transaction_id=merchantTransactionIdentifier)

            paymenttransactionobj.txn_status = txn_status  # statusCode
            paymenttransactionobj.txn_msg = txn_msg  # statusMessage
            paymenttransactionobj.txn_err_msg = txn_err_msg  # errorMessage
            paymenttransactionobj.clnt_txn_ref = clnt_txn_ref
            paymenttransactionobj.tpsl_bank_cd = tpsl_bank_cd
            paymenttransactionobj.tpsl_txn_id = tpsl_txn_id  # identifier
            paymenttransactionobj.txn_amt = txn_amt
            paymenttransactionobj.clnt_rqst_meta = clnt_rqst_meta
            paymenttransactionobj.tpsl_txn_time = tpsl_txn_time
            paymenttransactionobj.bal_amt = bal_amt
            paymenttransactionobj.card_id = card_id
            paymenttransactionobj.alias_name = alias_name
            paymenttransactionobj.bank_transaction_id = bank_transaction_id
            paymenttransactionobj.mandate_reg_no = mandate_reg_no
            paymenttransactionobj.save()

            if statusCode == '0300' and is_hash_match:
                # Paid Successfully
                hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                tds_amount_enter = request.POST.get('tds_amount_hall')
                # hall_booking_obj.booking_status = 6
                hall_booking_obj.payment_method = 1
                hall_booking_obj.payment_status = 1
                hall_booking_obj.paid_amount = Decimal(txn_amt)
                hall_booking_obj.tds = Decimal(tds_amount_enter)
                hall_booking_obj.save()

                paymenttransactionobj.payment_status = 1
                paymenttransactionobj.save()

                # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                #     hall_booking_detail.booking_status = 6
                #     hall_booking_detail.save()
                #     for hall_check_avail in HallCheckAvailability.objects.filter(
                #             hall_booking_detail=hall_booking_detail):
                #         hall_check_avail.booking_status = 6
                #         hall_check_avail.save()

                booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                        payable_amount=hall_booking_obj.total_payable,
                                                        paid_amount=hall_booking_obj.paid_amount,
                                                        payment_status=1,
                                                        payment_date=datetime.datetime.now(),
                                                        tds_amount=Decimal(tds_amount_enter),
                                                        )
                booking_payment_obj.save()

                if tds_amount_enter > 0:
                    booking_payment_obj.is_tds = True
                    booking_payment_obj.save()

                #############################################
                if hall_booking_obj.user_track:
                    if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                        if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                            user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                            user_track_obj.deposit_available = hall_booking_obj.deposit
                            user_track_obj.deposit_status = 0
                            user_track_obj.refund_status = 0
                            user_track_obj.save()

                            exclude_hall_booking_list = HallBooking.objects.filter(
                                Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                            for hall_obj in exclude_hall_booking_list:
                                exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                    exclude_hall_obj.is_deposit_through_cheque = False
                                    exclude_hall_obj.deposit_status = 0
                                    exclude_hall_obj.save()
                                    HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                        is_deleted=True)
                                elif exclude_hall_obj.deposit:
                                    if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                        exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj).last()
                                        exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                            total_paid=Sum('paid_amount'))

                                        exclude_hall_obj.deposit = 0
                                        exclude_hall_obj.save()
                                        exclude_hall_obj.total_payable = round(
                                            exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                            0)
                                        exclude_hall_obj.save()
                                        exclude_hall_payment_obj.payable_amount = Decimal(
                                            exclude_hall_obj.total_payable) - Decimal(
                                            exclude_total_paid_dict['total_paid'])
                                        exclude_hall_payment_obj.save()

                ##################################################
                transaction.savepoint_commit(sid)
                # send_mail_count = "FIRST"
                # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                response_data['success'] = 'true'
                pass
            elif statusCode == '0398' and is_hash_match:
                # Transaction Initiated. Add Entry in Pending Transaction
                hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                tds_amount_enter = request.POST.get('tds_amount_hall')
                hall_booking_obj.booking_status = 9
                hall_booking_obj.tds = Decimal(tds_amount_enter)

                hall_booking_obj.save()

                paymenttransactionobj.payment_status = 2
                paymenttransactionobj.save()

                for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                    hall_booking_detail.booking_status = 8
                    hall_booking_detail.save()
                    for hall_check_avail in HallCheckAvailability.objects.filter(
                            hall_booking_detail=hall_booking_detail):
                        hall_check_avail.booking_status = 8
                        hall_check_avail.save()

                booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                        payable_amount=hall_booking_obj.total_payable,
                                                        paid_amount=hall_booking_obj.paid_amount,
                                                        payment_status=8,
                                                        payment_date=datetime.datetime.now(),
                                                        tds_amount=Decimal(tds_amount_enter))
                booking_payment_obj.save()

                if tds_amount_enter > 0:
                    booking_payment_obj.is_tds = True
                    booking_payment_obj.save()

                #############################################
                if hall_booking_obj.user_track:
                    if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                        if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                            user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                            user_track_obj.deposit_available = hall_booking_obj.deposit
                            user_track_obj.deposit_status = 0
                            user_track_obj.refund_status = 0
                            user_track_obj.save()

                            exclude_hall_booking_list = HallBooking.objects.filter(
                                Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                            for hall_obj in exclude_hall_booking_list:
                                exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                    exclude_hall_obj.is_deposit_through_cheque = False
                                    exclude_hall_obj.deposit_status = 0
                                    exclude_hall_obj.save()
                                    HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                        is_deleted=True)
                                elif exclude_hall_obj.deposit:
                                    if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                        exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj).last()
                                        exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                            hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                            total_paid=Sum('paid_amount'))

                                        exclude_hall_obj.deposit = 0
                                        exclude_hall_obj.save()
                                        exclude_hall_obj.total_payable = round(
                                            exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                            0)
                                        exclude_hall_obj.save()
                                        exclude_hall_payment_obj.payable_amount = Decimal(
                                            exclude_hall_obj.total_payable) - Decimal(
                                            exclude_total_paid_dict['total_paid'])
                                        exclude_hall_payment_obj.save()

                ##################################################
                transaction.savepoint_commit(sid)
                # send_mail_count = "FIRST"
                # add_to_pending(paymenttransactionobj.id)
                # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                response_data['success'] = 'initiated'
                pass
            elif statusCode == '0399' and is_hash_match:
                # Failed Transaction

                # hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                # hall_booking_obj.booking_status = 0
                # hall_booking_obj.save()
                #
                # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                #     hall_booking_detail.booking_status = 0
                #     hall_booking_detail.save()
                #     for hall_check_avail in HallCheckAvailability.objects.filter(
                #             hall_booking_detail=hall_booking_detail):
                #         hall_check_avail.booking_status = 0
                #         hall_check_avail.save()
                # transaction.savepoint_commit(sid)

                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                pass
            elif statusCode == '0396' and is_hash_match:
                # Cancelled by User

                # hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                # hall_booking_obj.booking_status = 0
                # hall_booking_obj.save()
                #
                # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                #     hall_booking_detail.booking_status = 0
                #     hall_booking_detail.save()
                #     for hall_check_avail in HallCheckAvailability.objects.filter(
                #             hall_booking_detail=hall_booking_detail):
                #         hall_check_avail.booking_status = 0
                #         hall_check_avail.save()

                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                response_data['success'] = 'cancelled'
                pass
            elif is_hash_match:
                # code if hash is matched but no status code
                pass

            elif not is_hash_match and statusCode in ['0300', '0398', '0399', '0396']:
                paymenttransactionobj.is_hash_matched = False
                paymenttransactionobj.save()

                if statusCode == '0300':
                    hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                    tds_amount_enter = request.POST.get('tds_amount_hall')
                    # hall_booking_obj.booking_status = 9
                    hall_booking_obj.payment_method = 1
                    hall_booking_obj.payment_status = 1
                    hall_booking_obj.paid_amount = Decimal(txn_amt)
                    hall_booking_obj.tds = Decimal(tds_amount_enter)

                    hall_booking_obj.save()

                    paymenttransactionobj.payment_status = 1
                    paymenttransactionobj.save()

                    # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                    #     hall_booking_detail.booking_status = 6
                    #     hall_booking_detail.save()
                    #     for hall_check_avail in HallCheckAvailability.objects.filter(
                    #             hall_booking_detail=hall_booking_detail):
                    #         hall_check_avail.booking_status = 6
                    #         hall_check_avail.save()

                    booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                            payable_amount=hall_booking_obj.total_payable,
                                                            paid_amount=hall_booking_obj.paid_amount,
                                                            payment_status=1,
                                                            payment_date=datetime.datetime.now(),
                                                            tds_amount=Decimal(tds_amount_enter))

                    booking_payment_obj.save()
                    if tds_amount_enter > 0:
                        booking_payment_obj.is_tds = True
                        booking_payment_obj.save()

                    #############################################
                    if hall_booking_obj.user_track:
                        if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                            if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                                user_track_obj.deposit_available = hall_booking_obj.deposit
                                user_track_obj.deposit_status = 0
                                user_track_obj.refund_status = 0
                                user_track_obj.save()

                                exclude_hall_booking_list = HallBooking.objects.filter(
                                    Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                    ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                                for hall_obj in exclude_hall_booking_list:
                                    exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                    if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                        exclude_hall_obj.is_deposit_through_cheque = False
                                        exclude_hall_obj.deposit_status = 0
                                        exclude_hall_obj.save()
                                        HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                            is_deleted=True)
                                    elif exclude_hall_obj.deposit:
                                        if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                            exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj).last()
                                            exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                                total_paid=Sum('paid_amount'))

                                            exclude_hall_obj.deposit = 0
                                            exclude_hall_obj.save()
                                            exclude_hall_obj.total_payable = round(
                                                exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                                0)
                                            exclude_hall_obj.save()
                                            exclude_hall_payment_obj.payable_amount = Decimal(
                                                exclude_hall_obj.total_payable) - Decimal(
                                                exclude_total_paid_dict['total_paid'])
                                            exclude_hall_payment_obj.save()

                    ##################################################

                    transaction.savepoint_commit(sid)
                    # send_mail_count = "FIRST"
                    # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                    # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                    response_data['success'] = 'true'

                elif statusCode == '0398':
                    # Transaction Initiated. Add Entry in Pending Transaction
                    hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
                    tds_amount_enter = request.POST.get('tds_amount_hall')
                    hall_booking_obj.booking_status = 9
                    hall_booking_obj.tds = Decimal(tds_amount_enter)
                    hall_booking_obj.save()

                    paymenttransactionobj.payment_status = 2
                    paymenttransactionobj.save()

                    # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
                    #     hall_booking_detail.booking_status = 8
                    #     hall_booking_detail.save()
                    #     for hall_check_avail in HallCheckAvailability.objects.filter(
                    #             hall_booking_detail=hall_booking_detail):
                    #         hall_check_avail.booking_status = 8
                    #         hall_check_avail.save()

                    booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj, payment_mode=1,
                                                            payable_amount=hall_booking_obj.total_payable,
                                                            paid_amount=hall_booking_obj.paid_amount,
                                                            payment_status=8,
                                                            payment_date=datetime.datetime.now(),
                                                            tds_amount=Decimal(tds_amount_enter))
                    booking_payment_obj.save()
                    if tds_amount_enter > 0:
                        booking_payment_obj.is_tds = True
                        booking_payment_obj.save()


                    #############################################
                    if hall_booking_obj.user_track:
                        if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:
                            if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                                user_track_obj.deposit_available = hall_booking_obj.deposit
                                user_track_obj.deposit_status = 0
                                user_track_obj.refund_status = 0
                                user_track_obj.save()

                                exclude_hall_booking_list = HallBooking.objects.filter(
                                    Q(user_track_id=hall_booking_obj.user_track.id), Q(is_completed=False),
                                    ~Q(booking_status__in=[0, 10])).exclude(id=hall_booking_obj.id)
                                for hall_obj in exclude_hall_booking_list:
                                    exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)

                                    if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                                        exclude_hall_obj.is_deposit_through_cheque = False
                                        exclude_hall_obj.deposit_status = 0
                                        exclude_hall_obj.save()
                                        HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(
                                            is_deleted=True)
                                    elif exclude_hall_obj.deposit:

                                        if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                            exclude_hall_payment_obj = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj).last()
                                            exclude_total_paid_dict = HallPaymentDetail.objects.filter(
                                                hall_booking=exclude_hall_obj, is_deleted=False).aggregate(
                                                total_paid=Sum('paid_amount'))

                                            exclude_hall_obj.deposit = 0
                                            exclude_hall_obj.save()
                                            exclude_hall_obj.total_payable = round(
                                                exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount,
                                                0)
                                            exclude_hall_obj.save()
                                            exclude_hall_payment_obj.payable_amount = Decimal(
                                                exclude_hall_obj.total_payable) - Decimal(
                                                exclude_total_paid_dict['total_paid'])
                                            exclude_hall_payment_obj.save()

                    ##################################################

                    transaction.savepoint_commit(sid)
                    send_mail_count = "FIRST"
                    # add_to_pending(paymenttransactionobj.id)
                    # send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
                    # send_booking_invoice_mail_locationvise(request, hall_booking_obj)
                    response_data['success'] = 'initiated'
                elif statusCode == '0399':
                    # Failed Transaction
                    paymenttransactionobj.payment_status = 3
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'failed'
                elif statusCode == '0396':
                    # Cancelled by User
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.save()

                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'cancelled'
                # code if hash code is not matched and with match statusCode
                pass

            else:
                # code if hash code is not matched and without match statusCode
                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                pass

            # transaction.savepoint_commit(sid)

        except Exception, e:
            log.debug('Error = {0}\n'.format(e))
            print e
            pass

    except Exception, e:
        print e
        transaction.rollback(sid)
        response_data['success'] = 'false'
        pass
    print '\nResponse Data pay_later_payment_response_save = ', response_data
    print '\nResponse OUT | common.py | pay_later_payment_response_save | User = ', request.user
    return HttpResponse(json.dumps(response_data), content_type='application/json')
