
# System Modules

import xlrd, random, datetime, smtplib, os, traceback, json, logging
from decimal import Decimal
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.db.models import IntegerField, Sum
from django.shortcuts import *
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.db.models import Q
from num2words import num2words
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from django.conf import settings
from email.mime.text import MIMEText
from xhtml2pdf import pisa
import cStringIO as StringIO
from cgi import escape
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.http import HttpResponse
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required
from wkhtmltopdf.views import PDFTemplateResponse
from email.mime.application import MIMEApplication
from email import encoders
from email.mime.base import MIMEBase
from datetime import timedelta
from django.http import HttpRequest


# User Models

from adminapp.models import *
from membershipapp.models import PaymentDetails, HOD_Detail, CompanyDetail, UserDetail, MembershipInvoice, MembershipUser, MembershipTypeTrack, RenewLetterSchedule
from adminapp.models import NameSign
from member_proforma_invoice import download_proforma_invoice
charset = 'utf-8'

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Details'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def membership_details(request):
    return render(request, 'backoffice/membership/membership_details.html')


# TODO Membership Detail Datatable Start ------cycle level
def get_membership_details_datatable(request):
    try:
        print '\nRequest IN | membership_details | get_membership_details_datatable | user %s', request.user
        dataList = []
        meterReadings = []

        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        membership_detail_status = request.GET.get('membership_detail_status')
        membership_detail_list = ''

        if membership_detail_status != 'show_all':
            membership_detail_list = MembershipDetail.objects.filter(
                is_active=True if membership_detail_status == 'True' else False,
                is_deleted=False)
        else:
            membership_detail_list = MembershipDetail.objects.filter(is_deleted=False)

        membership_detail_list = membership_detail_list.filter(Q(code__icontains=searchTxt) |
                                                               Q(description__icontains=searchTxt))

        i = 1
        for membershipDetail in membership_detail_list:
            tempList = []
            if membershipDetail.is_active is True:
                status = '<label class="label label-success"> Active </label>'
                status_text = "True"
                status_icon = '<a class="icon-trash" data-toggle="modal" data-target=#active_deactive_mem_detail onclick=activeInactiveDetail(' + '"' + str(
                    status_text) + '"' + ',' + str(membershipDetail.id) + ')></a>&nbsp;&nbsp;'
            else:
                status = '<label class="label label-default"> Inactive </label>'
                status_text = "False"
                status_icon = '<a class="icon-reload" data-toggle="modal" data-target=#active_deactive_mem_detail onclick=activeInactiveDetail(' + '"' + str(
                    status_text) + '"' + ',' + str(membershipDetail.id) + ')></a>&nbsp;&nbsp;'
            edit_icon = '<a class="icon-pencil" onClick="editMembershipCategoryModal(' + str(
                membershipDetail.id) + ')"></a>'

            tempList.append(i)
            tempList.append(membershipDetail.code)
            tempList.append(membershipDetail.description)
            tempList.append(status)
            tempList.append(status_icon + edit_icon)
            dataList.append(tempList)
            i = i + 1

        if length == -1:
            sliced_list = dataList[:]
        else:
            sliced_list = dataList[start:length]
        total_records = len(dataList)
        total_record = total_records
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': sliced_list}
    except Exception, e:
        print '\nexception ', str(traceback.print_exc())
        print '\nException|membership_details | get_membership_details_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Change Membership Detail Status
@transaction.atomic
def update_membership_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_details | update_membership_status | user %s', request.user
        membership_detail_obj = MembershipDetail.objects.get(id=request.GET.get('mem_detail_id'))
        if membership_detail_obj.is_active is True:
            membership_detail_obj.is_active = False
        else:
            membership_detail_obj.is_active = True
        membership_detail_obj.save()
        transaction.savepoint_commit(sid)

        data = {'success': 'true'}
        print '\nResponse OUT | membership_details | update_membership_status | user %s', request.user
    except Exception, e:
        data = {'success': 'false'}
        print '\nException IN | membership_details | update_membership_status = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Details'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_membership_details(request):
    return render(request, 'backoffice/membership/add-membership-details.html')


@transaction.atomic
@csrf_exempt
def save_membership_details(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_details | save_membership_details | user %s', request.user

        # try:
        #     userProfile = MembershipCategory.objects.get(employee_id=user_employee_no)
        #     data = {'success': 'employeeid'}
        #     return HttpResponse(json.dumps(data), content_type='application/json')
        # except Exception, e:
        #     print 'Handled Exception | user | save_membership_details | User', request.user, 'Handled Exception = ', e
        #     pass

        membership_detail_obj = MembershipDetail(code=str(request.POST.get('category_code')).strip(),
                                                 description=str(request.POST.get('category_descriptions')).strip())
        membership_detail_obj.save()
        transaction.savepoint_commit(sid)

        data = {'success': 'true'}
        print '\nResponse OUT | membership_details | save_membership_details | user %s', request.user
    except Exception, e:
        data = {'success': 'false'}
        print '\nException | user | membership_details | user %s. Exception = ', request.user, e
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_membership_details(request):
    try:
        print '\nRequest IN | membership_details | show_membership_details | user %s', request.user

        membserhipObj = MembershipDetail.objects.get(id=request.GET.get('category_code_id'))
        membserhipDetails = {
            'category_code_id': membserhipObj.id,
            'membership_code': membserhipObj.code,
            'membership_category': membserhipObj.description,
        }

        data = {'success': 'true', 'membserhipDetails': membserhipDetails}
        print '\nRequest OUT | membership_details | show_membership_details | user %s', request.user
    except Exception, e:
        data = {'success': 'false'}
        print '\nException | user | membership_details | show_membership_details |user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def edit_membership_details(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_details | edit_membership_details | user %s', request.user

        membershipObj = MembershipDetail.objects.get(id=request.POST.get('category_code_id'))
        membershipObj.code = str(request.POST.get('edit_category_code')).strip()
        membershipObj.description = str(request.POST.get('edit_category_descriptions')).strip()
        membershipObj.save()

        transaction.savepoint_commit(sid)

        data = {'success': 'true'}
        print '\nRequest OUT | membership_details | edit_membership_details | user %s', request.user
    except Exception, e:
        data = {'success': 'false'}
        print '\nException | membership_details | edit_membership_details | user %s. Exception = ', request.user, e
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Registration'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def members_details(request):
    data = {}
    try:
        print '\nRequest IN | membership_details.py | members_details | User = ', request.user
        i = 3
        date_list = []
        today_date = datetime.datetime.now().date()
        last_year = today_date.year - 1

        while i > 0:
            date_list.append(str(last_year)+'-'+str(last_year+1))
            last_year = last_year + 1
            i = i - 1

        category_list = MembershipCategory.objects.filter(status=True, is_deleted=False).order_by('membership_category')
        state_list = State.objects.filter(is_active=True, is_deleted=False).order_by('state_name')
        city_list = City.objects.filter(is_active=True, is_deleted=False).order_by('city_name')
        pincode_list = UserDetail.objects.filter(is_deleted=False).values('correspond_pincode').order_by(
            'correspond_pincode').distinct()
        legal_status_list = LegalStatus.objects.filter(status=True, is_deleted=False).order_by('description')
        data = {'category_list': category_list, 'state_list': state_list, 'city_list': city_list,
                'pincode_list': pincode_list, 'legal_status_list': legal_status_list, 'date_list': date_list}

        print '\nResponse OUT | membership_details.py | members_details | User = ', request.user
    except Exception, e:
        print '\nException | membership_details.py | members_details = ', str(traceback.print_exc())
    return render(request, 'backoffice/membership/member_details.html', data)


# TODO Membership Detail Datatable Start ------cycle level
def get_members_details_datatable(request):
    try:
        print '\nRequest IN | members_details | get_members_details_datatable | user %s', request.user
        dataList = []

        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''        
        payment_from = request.GET.get('payment_from')
        payment_to = request.GET.get('payment_to')
        accept_from = request.GET.get('acceptance_from')
        accept_to = request.GET.get('acceptance_to')
        receipt_from = request.GET.get('receipt_from')
        receipt_to = request.GET.get('receipt_to')

        print '\nsearchTxt = ', searchTxt

        if searchTxt:
            pass
        else:
            searchTxt = request.GET.get('search_text')

        member_detail_list = UserDetail.objects.all()

        # if request.GET.get('business_nature') != 'show_all':
        #     member_detail_list = member_detail_list.filter(membership_category=request.GET.get('business_nature'))
        #
        # if request.GET.get('iso') != 'show_all':
        #     member_detail_list = member_detail_list.filter(
        #         company__iso=True if request.GET.get('iso') == 'True' else False)
        #
        # if request.GET.get('scale') != 'show_all':
        #     member_detail_list = member_detail_list.filter(company__company_scale=request.GET.get('scale'))
        #
        # if request.GET.get('state') != 'show_all':
        #     member_detail_list = member_detail_list.filter(correspondstate=request.GET.get('state'))
        #
        # if request.GET.get('city') != 'show_all':
        #     member_detail_list = member_detail_list.filter(correspondcity=request.GET.get('city'))
        #
        # if request.GET.get('pincode') != 'show_all':
        #     member_detail_list = member_detail_list.filter(correspond_pincode=request.GET.get('pincode'))
        #
        # if request.GET.get('mem_associate') != 'show_all':
        #     member_detail_list = member_detail_list.filter(user_type=request.GET.get('mem_associate'))
        #
        # if request.GET.get('legal_status') != 'show_all':
        #     member_detail_list = member_detail_list.filter(company__legalstatus=request.GET.get('legal_status'))

        if request.GET.get('fy') != 'show_all':
            member_detail_list = member_detail_list.filter(membership_year=request.GET.get('fy'))

        if request.GET.get('payment_status') != 'show_all':
            member_detail_list = member_detail_list.filter(payment_method=request.GET.get('payment_status'))

        # if request.GET.get('turnover_from') and request.GET.get('turnover_to'):
        #     member_detail_list = member_detail_list.filter(annual_turnover_rupees__gte=request.GET.get('turnover_from'),
        #                                                    annual_turnover_rupees__lte=request.GET.get('turnover_to'))
        # elif request.GET.get('turnover_from'):
        #     member_detail_list = member_detail_list.filter(annual_turnover_rupees__gte=request.GET.get('turnover_from'))
        # elif request.GET.get('turnover_to'):
        #     member_detail_list = member_detail_list.filter(annual_turnover_rupees__lte=request.GET.get('turnover_to'))

        if accept_from and accept_to:
            member_detail_list = member_detail_list.filter(membership_acceptance_date__gte=datetime.datetime.strftime(
                datetime.datetime.strptime(accept_from, '%d/%m/%Y'), '%Y-%m-%d'),
                membership_acceptance_date__lte=datetime.datetime.strftime(
                    datetime.datetime.strptime(accept_to, '%d/%m/%Y'),
                    '%Y-%m-%d'))
        # elif accept_from:
        #     member_detail_list = member_detail_list.filter(membership_acceptance_date__gte=datetime.datetime.strftime(
        #         datetime.datetime.strptime(accept_from, '%d/%m/%Y'), '%Y-%m-%d'))
        # elif accept_to:
        #     member_detail_list = member_detail_list.filter(membership_acceptance_date__lte=datetime.datetime.strftime(
        #         datetime.datetime.strptime(accept_to, '%d/%m/%Y'), '%Y-%m-%d'))

        payment_detail_list = []
        if payment_from or payment_to:
            if payment_from and payment_to:
                payment_detail_list = PaymentDetails.objects.filter(is_deleted=False, payment_date__gte=datetime.datetime.strftime(datetime.datetime.strptime(payment_from, '%d/%m/%Y'), '%Y-%m-%d'),
                                                                    payment_date__lte=datetime.datetime.strftime(datetime.datetime.strptime(payment_to, '%d/%m/%Y'), '%Y-%m-%d')).values('userdetail_id')
            # elif payment_from:
            #     payment_detail_list = PaymentDetails.objects.filter(is_deleted=False,
            #                                                         payment_date__gte=datetime.datetime.strftime(datetime.datetime.strptime(payment_from, '%d/%m/%Y'),'%Y-%m-%d')).values('userdetail_id').order_by('-userdetail_id').distinct()
            # elif payment_to:
            #     payment_detail_list = PaymentDetails.objects.filter(is_deleted=False,
            #                                                             payment_date__lte=datetime.datetime.strftime(datetime.datetime.strptime(payment_to,'%d/%m/%Y'),'%Y-%m-%d')).values('userdetail_id')
            # member_detail_list = member_detail_list.filter(id__in=[payment_detail['userdetail_id'] for payment_detail in payment_detail_list])

        receipt_detail_list = []
        if receipt_from or receipt_to:
            if receipt_from and receipt_to:
                receipt_detail_list = PaymentDetails.objects.filter(is_deleted=False,receipt_date__gte=datetime.datetime.strftime(datetime.datetime.strptime(receipt_from,'%d/%m/%Y'),'%Y-%m-%d'),
                                                                    receipt_date__lte=datetime.datetime.strftime(datetime.datetime.strptime(receipt_to,'%d/%m/%Y'),'%Y-%m-%d')).values('userdetail_id')
            # elif receipt_from:
            #     receipt_detail_list = PaymentDetails.objects.filter(is_deleted=False,receipt_date__gte=datetime.datetime.strftime(datetime.datetime.strptime(receipt_from,'%d/%m/%Y'),'%Y-%m-%d')).values('userdetail_id')
            # elif receipt_to:
            #     receipt_detail_list = PaymentDetails.objects.filter(is_deleted=False,receipt_date__lte=datetime.datetime.strftime(datetime.datetime.strptime(receipt_to,'%d/%m/%Y'),'%Y-%m-%d')).values('userdetail_id')
            # member_detail_list = member_detail_list.filter(id__in=[receipt_detail['userdetail_id'] for receipt_detail in receipt_detail_list])
        
        if searchTxt:
            # industry_desc_list = IndustryDescription.objects.filter(Q(description__icontains=searchTxt), is_active=True).values('id')
            member_detail_list = member_detail_list.filter(Q(company__company_name__icontains=searchTxt) |
                                                           Q(member_associate_no__icontains=searchTxt) |
                                                            Q(ceo_email__icontains=searchTxt) |
                                                            Q(correspond_email__icontains=searchTxt) |
                                                            Q(person_email__icontains=searchTxt))

        member_detail_list = member_detail_list.order_by('-updated_date')
        total_records = member_detail_list.count()
        if length != -1:
            member_detail_list = member_detail_list[start:length]
        # else:
            # member_detail_list = member_detail_list[::-1]
            # member_detail_list = member_detail_list.order_by('-updated_date')
        total_record = total_records

        i = 1
        for member in member_detail_list:
            try:
                member_invoice_obj = MembershipInvoice.objects.filter(userdetail=member, financial_year=member.membership_year).last()
                try:
                    payment_detail_list = PaymentDetails.objects.filter(userdetail=member,financial_year=member.membership_year, payment_date__isnull=False, is_deleted=False).values(
                        'amount_paid', 'amount_due').aggregate(received_amount=Sum('amount_paid'),
                                                              due_amount=Sum('amount_due'))
                    # print 'ff = ', member.company.company_name
                    # print '\npayment_detail_list = ', payment_detail_list
                except:
                    pass
                if payment_detail_list:
                    amt_recd = str(payment_detail_list['received_amount'])
                    amt_due = str(payment_detail_list['due_amount'])
                    stax = str(member_invoice_obj.tax)
                    if Decimal(amt_recd) == Decimal(member_invoice_obj.amount_payable):
                        amt_due = 0
                    # if member_invoice_obj.is_paid:
                    #     amt_due = 0
                    #     # amt_recd =  str(member_invoice_obj.amount_payable)
                    #     for item in payment_detail_list:
                    #         amt_recd = str(Decimal(amt_recd) + Decimal(item['received_amount']))
                else:
                    amt_recd = 0
                    amt_due = 0
                    stax = 0                
            except Exception, e:
                amt_recd = 0
                amt_due = 0
                stax = 0
                print e
                pass                

            tempList = []
            payment_detail_obj = PaymentDetails.objects.filter(userdetail=member, payment_date__isnull=False,
                                                               financial_year=member.membership_year, is_deleted=False).last()
            current_mem_year = str(member.membership_year)

            start_year = int(str(current_mem_year[0:4]))
            end_year = int(str(current_mem_year[5:9]))

            if member.is_deleted is False:
                status = '<label class="label label-success"> Active </label>'
                delete_icon = '<a class="icon-trash" onClick="deleteMemberModal(' + str(member.id) + ')"></a>&nbsp;&nbsp;'
                if member.user_type == 'Life Membership' or member.member_associate_no is None:
                    renew_icon = ''
                else:
                    renew_icon = '<a onClick="viewRenewScreen(' + str(member.id) + ')">' + str(start_year+1) + '-' + str(end_year+1) + '</a>'
            else:
                status = '<label class="label label-default"> De-active </label>'
                delete_icon = '<a class="icon-reload" onClick="reactivateMemberModal(' + str(member.id) + ')"></a>&nbsp;&nbsp;'
                renew_icon = ''
            edit_icon = '<a class="icon-pencil" onClick="editMemberModal(' + str(member.id) + ')"></a>&nbsp;&nbsp;'
            # delete_icon = '<a class="icon-trash" onClick="deleteMemberModal(' + str(member.id) + ')"></a>'
            payment_icon = '<a class="fa fa-rupee" onClick="viewPaymentModal(' + str(member.id) + ')"></a>&nbsp;&nbsp;'
            history_icon = '<a class="fa fa-history" target="_blank" href=/backofficeapp/get-user-track-history-page/' + str(member.id) + '/></a>'
            print_form = '<a target="_blank" href=/backofficeapp/print-user-form/' + str(member.id) + '/>Print</a>'
            download_certificate = '<a class="fa fa-download" target="_blank" href=/backofficeapp/download-certificate/' + str(member.id) + '/></a>'
            send_soft_copy_certificate = '<a class="fa fa-paper-plane" target="_blank" href=/backofficeapp/send-soft-copy-certificate-through-mail/' + str(
                member.id) + '/></a>'
            manual_download_certificate = '<a class="fa fa-download" target="_blank" href=/backofficeapp/manual-download-certificate/' + str(
                member.id) + '/></a>'
            manual_download_address = '<a class="fa fa-download" title="Download Address" target="_blank" href=/backofficeapp/hard-copy-certificate-address-download/' + str(
                member.id) + '/></a>'

            download_proforma_invoice = '<a class="fa fa-download" data-toggle="modal" data-target="#proforma_invoice_modal" onclick="show_proforma_invoice_modal(' + str(member.id) + ')"></a>'
            send_pi_mail = '<a class="fa fa-paper-plane" data-toggle="modal" data-target="#proforma_invoice_modal_email" onclick="show_proforma_invoice_modal_email(' + str(member.id) + ')"></a>'
            send_renew_letter =  '<a class="fa fa-paper-plane" target="_blank" href=/backofficeapp/send-manual-renew-letter/' + str(
                member.id) + '/></a>'


            actions = edit_icon + delete_icon + payment_icon + renew_icon

            tempList.append(i)
            if payment_detail_obj:
                tempList.append(str(payment_detail_obj.payment_date.strftime('%d %b %Y')))
            else:
                tempList.append(str(member.created_date.strftime('%d %b %Y')))
            tempList.append(str(current_mem_year))

            if member.member_associate_no:
                tempList.append(str(member.member_associate_no))
            else:
                tempList.append('')
            if member.company:

                tempList.append(str(member.company.company_name))
            else:
                tempList.append("")

            next_due = 0
            bk_no = 0
            tempList.append(amt_recd)
            tempList.append(amt_due)
            # tempList.append(stax)
            tempList.append(member.annual_turnover_rupees)
            if print_form:
                tempList.append(edit_icon + ' | ' + delete_icon + ' | ' + print_form)
            else:
                tempList.append(edit_icon + ' | ' + delete_icon)
            if renew_icon:
                tempList.append(payment_icon + '|  ' + renew_icon + ' | ' + history_icon)
            else:
                tempList.append(payment_icon + '|  ' + history_icon)
            tempList.append(member.ceo_email)

            if member.membership_acceptance_date:
                tempList.append(str(datetime.datetime.strftime(member.membership_acceptance_date, '%d %B %Y')))
            else:
                tempList.append('')
            if payment_detail_obj:
                if payment_detail_obj.receipt_date:
                    tempList.append(str(datetime.datetime.strftime(payment_detail_obj.receipt_date, '%d %B %Y')))
                else:
                    tempList.append('')
                if payment_detail_obj.payment_date:
                    tempList.append(str(datetime.datetime.strftime(payment_detail_obj.payment_date, '%d %B %Y')))
                else:
                    tempList.append('')
                if payment_detail_obj.bk_no:
                    bk_no = str(payment_detail_obj.bk_no)
            else:
                tempList.append('')
                tempList.append('')
            tempList.append(member.ceo_cellno)
            tempList.append(download_certificate + ' |&nbsp;' + send_soft_copy_certificate)
            tempList.append(manual_download_certificate + ' |&nbsp;' + manual_download_address)
            tempList.append(download_proforma_invoice + ' |&nbsp;'+ send_pi_mail)
            tempList.append(send_renew_letter)
            tempList.append(next_due)
            tempList.append(bk_no)
            tempList.append(status)
            i = i + 1

            dataList.append(tempList)

        # if length == -1:
        #     sliced_list = dataList[:]
        # else:
        #     sliced_list = dataList[start:length]
        # total_records = len(dataList)
        # total_record = total_records
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print '\nException|membership_details | get_membership_details_datatable = ', str(traceback.print_exc())
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# TODO Membership Detail Datatable Initialization End ------cycle level


@transaction.atomic
@csrf_exempt
def delete_membership(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print 'Request IN | membership_details | delete_membership | user = ', request.user

        if request.POST:
            membershipObj = UserDetail.objects.get(id=request.POST.get('member_id'))
            membershipObj.is_deleted = True
            membershipObj.payment_method = "Deactivate"
            membershipObj.updated_date = datetime.datetime.now()
            membershipObj.updated_by = str(request.user)
            membershipObj.save()

            member_login_obj = MembershipUser.objects.get(userdetail=membershipObj)
            member_login_obj.is_deleted = True
            member_login_obj.updated_by = str(request.user)
            member_login_obj.save()

            transaction.savepoint_commit(sid)

            data['success'] = 'true'
            print 'Request OUT | membership_details | edit_membership_details | user = ', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data['success'] = 'noPost'
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:        
        data['success'] = 'false'
        print 'Exception | membership_details | delete_membership | user. Exception = ', request.user, e
        transaction.rollback(sid)
        return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def activate_membership(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print 'Request IN | membership_details | activate_membership | user = ', request.user

        if request.POST:
            membershipObj = UserDetail.objects.get(id=request.POST.get('active_member_id'))
            membershipObj.is_deleted = False
            if request.POST.get('re_association_status') == 'Yes':
                membershipObj.payment_method = "Offline Pending"
                membershipObj.is_reassociate = True
            else:
                membershipObj.is_reassociate = False
                membershipObj.payment_method = "Confirmed"
            membershipObj.updated_date = datetime.datetime.now()
            membershipObj.updated_by = str(request.user)
            membershipObj.save()

            member_login_obj = MembershipUser.objects.get(userdetail=membershipObj)
            member_login_obj.is_deleted = False
            member_login_obj.updated_by = str(request.user)
            member_login_obj.save()

            transaction.savepoint_commit(sid)

            data['success'] = 'true'
            print 'Request OUT | membership_details | edit_membership_details | user = ', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data['success'] = 'noPost'
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:        
        data['success'] = 'false'
        print 'Exception | membership_details | activate_membership | user. Exception = ', request.user, e
        transaction.rollback(sid)
        return HttpResponse(json.dumps(data), content_type='application/json')


################ user_payment #############################
def open_member_payment(request):
    data = {}
    try:
        print 'Request IN | open_member_payment | edit_membership_details | user %s', request.user
        print "request.GET.get('userDetail_id')----------", request.GET.get('member_id')

        category_list = []
        userDetail = UserDetail.objects.get(id=request.GET.get('member_id'))

        for category_item in MembershipCategory.objects.filter(is_deleted=False):
            category_list.append(
                {'cat_id': category_item.id,
                 'category': category_item.membership_category + ' - ' +category_item.enroll_type
                }
            )

        if userDetail.membership_acceptance_date:
            membership_acceptance_date = str(userDetail.membership_acceptance_date.strftime('%d/%m/%Y'))
        else:
            membership_acceptance_date = ''
        data = {
            'AccepatnceDate': membership_acceptance_date,
            'userDetail': userDetail,
            'category_list': category_list
        }

    except Exception, e:
        print 'Exception | membership_details | open_member_payment | user %s. Exception = ', request.user, e
    return render(request, 'backoffice/membership/member_payment_details.html', data)


def get_members_payment_details(request):
    try:
        print 'Request IN | members_details | get_members_payment_details | user %s', request.user
        dataList = []
        membersList = []
        membersObjs = []

        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        payment_fromDateValue = request.GET.get('payment_from')
        payment_toDateValue = request.GET.get('payment_to')
        receipt_fromDateValue = request.GET.get('receipt_from')
        receipt_toDateValue = request.GET.get('receipt_to')

        paymentDetails = []

        if request.GET.get('payment_from') and request.GET.get('payment_to') and request.GET.get('receipt_from') and request.GET.get('receipt_to'):
            payment_fromDateValue = datetime.datetime.strptime(str(payment_fromDateValue), '%d/%m/%Y').date()
            payment_toDateValue = datetime.datetime.strptime(str(payment_toDateValue), '%d/%m/%Y').date()
            receipt_fromDateValue = datetime.datetime.strptime(str(payment_fromDateValue), '%d/%m/%Y').date()
            receipt_toDateValue = datetime.datetime.strptime(str(payment_toDateValue), '%d/%m/%Y').date()

            paymentDetails = PaymentDetails.objects.filter(userdetail_id=request.GET.get('userDetail_id'),
                    receipt_date__gte=receipt_fromDateValue, receipt_date__lte=receipt_toDateValue,
                    payment_date__gte=payment_fromDateValue, payment_date__lte=payment_toDateValue)

        elif request.GET.get('payment_from') and request.GET.get('payment_to'):
            payment_fromDateValue = datetime.datetime.strptime(str(payment_fromDateValue), '%d/%m/%Y').date()
            payment_toDateValue = datetime.datetime.strptime(str(payment_toDateValue), '%d/%m/%Y').date()

            paymentDetails = PaymentDetails.objects.filter(userdetail_id=request.GET.get('userDetail_id'),
                    payment_date__gte=payment_fromDateValue, payment_date__lte=payment_toDateValue)

        elif request.GET.get('receipt_from') and request.GET.get('receipt_to'):
            receipt_fromDateValue = datetime.datetime.strptime(str(payment_fromDateValue), '%d/%m/%Y').date()
            receipt_toDateValue = datetime.datetime.strptime(str(payment_toDateValue), '%d/%m/%Y').date()

            paymentDetails = PaymentDetails.objects.filter(userdetail_id=request.GET.get('userDetail_id'),
                    receipt_date__gte=receipt_fromDateValue, receipt_date__lte=receipt_toDateValue)

        else:
            paymentDetails = PaymentDetails.objects.filter(userdetail_id=request.GET.get('userDetail_id'))

        paymentDetails = paymentDetails.order_by('-financial_year', '-created_date')
        total_records = paymentDetails.count()
        paymentDetails = paymentDetails[start:length]        
        total_record = total_records
        i = 1
        for paymentDetail in paymentDetails:
            memberinvoice = MembershipInvoice.objects.get(id=paymentDetail.membershipInvoice.id)
            tempList = []

            tempList.append(i)
            if paymentDetail.payment_date:
                payment_date = paymentDetail.payment_date.strftime('%d-%m-%Y')
            else:
                payment_date = "NA"
            tempList.append(payment_date)
            tempList.append(paymentDetail.financial_year)
            if memberinvoice.membership_slab:
                tempList.append(str(memberinvoice.membership_slab.annual_fee))
            else:
                tempList.append(str(memberinvoice.userdetail.membership_slab.annual_fee))
            tempList.append(str(memberinvoice.subscription_charges))
            tempList.append(str(memberinvoice.entrance_fees))
            tempList.append(str(memberinvoice.tax))
            tempList.append(str(paymentDetail.amount_due))
            tempList.append(str(paymentDetail.amount_last_advance))
            tempList.append(str(paymentDetail.amount_next_advance))
            tempList.append(str(paymentDetail.amount_payable))
            tempList.append(str(paymentDetail.amount_paid))

            if paymentDetail.cheque_no:
                payment_status = str(paymentDetail.cheque_no)+'<br>'+str(paymentDetail.cheque_date.strftime('%d-%m-%Y'))+'<br>'+str(paymentDetail.bank_name)
            elif paymentDetail.neft_transfer_id and paymentDetail.neft_transfer_id != 'Paid_Online':
                payment_status = 'NEFT' + '<br>' + str(paymentDetail.neft_transfer_id) if paymentDetail.neft_transfer_id != 0 or paymentDetail.neft_transfer_id != '0'  else 'NEFT'
            elif paymentDetail.user_Payment_Type == 'Cash' and paymentDetail.amount_paid > 0:
                payment_status = str('Cash')
            elif paymentDetail.user_Payment_Type == 'NEFT':                
                payment_status = str('NEFT')
            elif paymentDetail.user_Payment_Type == 'Online':                
                payment_status = str('Online')
            elif paymentDetail.amount_paid > 0:
                payment_status = str('NEFT')
            else:
                payment_status = str('NA')

            if paymentDetail.is_cheque_bounce:                                
                payment_status = payment_status + '<br>' + str(paymentDetail.payment_remark) if paymentDetail.payment_remark else 'Cheque Bounce'
            elif paymentDetail.is_neft_failed:
                payment_status = payment_status + '<br>' + str(paymentDetail.payment_remark) if paymentDetail.payment_remark else 'NEFT Failed'
            elif paymentDetail.is_other:
                payment_status = payment_status + '<br>' + 'Other - ' + str(paymentDetail.payment_remark)

            if paymentDetail.receipt_date:
                payment_status = payment_status + '<br>' + str(paymentDetail.receipt_date.strftime('%d-%m-%Y')) + '<br>'
            if paymentDetail.receipt_no and paymentDetail.receipt_no != 'NULL':
                payment_status = payment_status + str(paymentDetail.receipt_no)            

            tempList.append(payment_status)

            submit_icon = ''
            send_to_confirmed_icon = ''
            edit_payment_icon = ''
            if paymentDetail.amount_paid > 0:
                submit_icon = '<a class="icon-pencil" onClick="SubmitUserPaymentReceipt(' + str(paymentDetail.id) + ')">Submit</a>'
                if paymentDetail.user_Payment_Type == 'Online' and paymentDetail.userdetail.payment_method == 'Online Pending':
                    send_to_confirmed_icon = '<a class="icon-paper-plane" onClick="sendToConfirmed(' + str(paymentDetail.id) + ')">Send</a>'
            else:
                submit_icon = '<a class="icon-pencil" onClick="SubmitUserPaymentModal(' + str(paymentDetail.id) + ')">Submit</a>'
            # delete_icon = '<a class="icon-trash" onClick="deleteMemberModal(' + str(member.id) + ')"></a>'
            delete_icon = '<a class="icon-trash" data-target="#payment_delete_modal" onClick="DeleteUserPaymentModal(' + str(paymentDetail.id) + ')">Delete</a>'

            if send_to_confirmed_icon:
                actions = submit_icon + '<br>' + delete_icon + '<br>' + send_to_confirmed_icon
            else:
                actions = submit_icon + '<br>' + delete_icon

            if memberinvoice.invoice_for == 'NEW':
                edit_payment_icon = '<a class="fa fa-rupee" data-target="#edit_payment_modal" onClick="editPayment(' + str(paymentDetail.id) + ')">Edit</a>'
                actions = actions + '<br>' + edit_payment_icon

            tempList.append(actions)
            dataList.append(tempList)

            i = i + 1
        
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|membership_details | get_members_payment_details = ',str(traceback.print_exc())
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# GET Payment Modal Data
def get_payment_modal(request):
    data = {}
    try:
        print '\nRequest IN | members_details | get_payment_modal | user %s', request.user
        payment_obj = PaymentDetails.objects.get(id=request.GET.get('payment_id'), is_deleted=False)
        data = {'success': 'true', 'amount_payable': str(payment_obj.amount_payable),
                 'last_due_amount': str(payment_obj.amount_due), 'invoice_id': str(payment_obj.membershipInvoice.id),
                'next_advance_amount': str(payment_obj.amount_next_advance)}
        print '\nResponse OUT | members_details | get_payment_modal | user %s', request.user
    except Exception,e:
        data = {'success': 'false'}
        print '\nException IN | members_details | get_payment_modal | user %s', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Save Payment Receipt
@transaction.atomic
@csrf_exempt
def save_payment_receipt(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print '\nRequest IN | members_details | save_payment_receipt | user %s', request.user
        payment_detail_obj = PaymentDetails.objects.get(id=request.POST.get('payment_receipt_id'), is_deleted=False)
        user_obj = UserDetail.objects.get(id=payment_detail_obj.userdetail.id)
        payment_detail_obj.receipt_no = str(request.POST.get('Receipt_No_Submit'))
        payment_detail_obj.receipt_date = datetime.datetime.strptime(str(request.POST.get('Receipt_Date_Submit')), '%d/%m/%Y').date()
        payment_detail_obj.updated_by = str(request.user)
        payment_detail_obj.save()
        user_obj.updated_date = datetime.datetime.now()
        user_obj.updated_by = str(request.user)
        user_obj.save()
        transaction.savepoint_commit(sid)

        # Send Acknowledgement Letter
        # user_detail_obj = UserDetail.objects.get(id=payment_detail_obj.userdetail.id)

        data = {'success': 'true'}
        print '\nResponse OUT | members_details | save_payment_receipt | user %s', request.user
    except Exception,e:
        data = {'success': 'false'}
        print '\nException IN | members_details | save_payment_receipt | user %s', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Add User to Confirmed List
@transaction.atomic
def add_user_to_confirmed_list(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print '\nRequest IN | members_details | add_user_to_confirmed_list | user %s', request.user
        payment_obj = PaymentDetails.objects.get(id=request.GET.get('payment_id'))
        userdetail_obj = UserDetail.objects.get(id=payment_obj.userdetail.id)
        userdetail_obj.payment_method = 'Confirmed'
        userdetail_obj.save()
        transaction.savepoint_commit(sid)
        # send_renew_mail_ack(payment_obj, userdetail_obj)
        data = {'success': 'true'}
        print '\nResponse OUT | members_details | add_user_to_confirmed_list | user %s', request.user
    except Exception,e:
        data = {'success': 'false'}
        print '\nException IN | members_details | add_user_to_confirmed_list | user %s', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Not in Use
@transaction.atomic
@csrf_exempt
def add_user_payment(request):
    sid = transaction.savepoint()

    try:
        print 'Request IN | members_details | add_user_payment | user %s', request.user
        try:
            userDetail = UserDetail.objects.get(id=request.POST.get('member_id'))
            membershipInvoice = MembershipInvoice.objects.get(userdetail_id=request.POST.get('member_id'))

            # membershipInvoice.amount_payable = request.POST.get('AmountPayable')
            user_Payment_Type = request.POST.get("user_Payment_Type")
            print "user_Payment_Type", request.POST.get("PaymentMode")

            if (request.POST.get("PaymentMode") == "OfflinePending"):
                userDetail.payment_method = "Offline Pending"

                if user_Payment_Type == "ByCash":
                    cash_amount = request.POST.get('cash_amount')
                    cheque_no = ''
                    cheque_date = None
                    bank_name = ''
                    NEFT_Transfer = ''
                    user_Payment_Type = "Cash"
                elif user_Payment_Type == "ByCheque":
                    cash_amount = ''
                    cheque_no = request.POST.get('ChequeNo')
                    cheque_date = datetime.datetime.strptime(request.POST.get('ChequeDate'), '%d/%m/%Y')
                    bank_name = request.POST.get('BankName')
                    NEFT_Transfer = ''
                    user_Payment_Type = "Cheque"
                else:
                    cash_amount = ''
                    cheque_no = ''
                    cheque_date = None
                    bank_name = ''
                    NEFT_Transfer = request.POST.get('neft_transfer_id')
                    user_Payment_Type = "NEFT"

            else:
                userDetail.payment_method = "Online Pending"
                cheque_no = ""
                cheque_date = datetime.date.today()
                bank_name = ""
                cash_amount = ""
                NEFT_Transfer = ""
                user_Payment_Type = "Cheque"
            userDetail.save()

            paymentDetails = PaymentDetails(
                                    userdetail_id = userDetail.id,
                                    membershipInvoice_id =membershipInvoice.id,
                                    amount_paid =request.POST.get('AmountPaid'),
                                    amount_last_advance=request.POST.get('NextDueAmount'),
                                    amount_next_advance=request.POST.get('NextAdvAmount'),
                                    cheque_no=request.POST.get('ChequeNo'),
                                    cheque_date=cheque_date,
                                    bank_name=request.POST.get('BankName'),
                                    neft_transfer_id=NEFT_Transfer,
                                    cash_amount= cash_amount,
                                    user_Payment_Type = user_Payment_Type,
                                    receipt_no=request.POST.get('ReceiptNo'),
                                    receipt_date=datetime.datetime.strptime(request.POST.get('ReceiptDate'), '%d/%m/%Y'),
                                    payment_date=datetime.date.today()
                                  )

            paymentDetails.save()
            paymentDetails.amount_due = float(paymentDetails.membershipInvoice.amount_payable) - float(paymentDetails.amount_paid)
            paymentDetails.save()

        except Exception, e:
            print 'exception ', str(traceback.print_exc())
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print 'Request OUT | members_details | add_user_payment | user %s', request.user
    except Exception, e:
        transaction.rollback(sid)
        print 'exception ', str(traceback.print_exc())
        print 'Exception|membership_details | add_user_payment |User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def submit_user_acceptance_detail(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print 'Request IN | members_details | submit_user_acceptance_detail | user ', request.user        
        try:
            user_detail_obj = UserDetail.objects.get(~Q(member_associate_no='NULL'), id=request.POST.get('Member_id'), member_associate_no__isnull=False, member_associate_no=str(request.POST.get('MemberAssociateNo')).strip())            
            if (str(user_detail_obj.user_type).strip() == str(request.POST.get('Membership_type')).strip()) or (str(user_detail_obj.member_associate_no).strip() == str(request.POST.get('MemberAssociateNo')).strip()):
                data['success'] = 'exists'
                print '\nDuplicate'
            else:
                print '\nChanged'                
                acceptance_date = datetime.datetime.strptime(request.POST.get('AcceptanceDate'), '%d/%m/%Y')
                try:
                    member_track_obj = MembershipTypeTrack(userdetail=user_detail_obj, old_company_name=str(user_detail_obj.company.company_name),
                        old_enroll_type=str(user_detail_obj.enroll_type),old_user_type=user_detail_obj.user_type, old_member_associate_no=user_detail_obj.member_associate_no,
                        old_acceptance_date=user_detail_obj.membership_acceptance_date, old_category=user_detail_obj.membership_category,
                        old_slab=user_detail_obj.membership_slab, last_membership_year=user_detail_obj.membership_year,
                        last_renewal_year=user_detail_obj.renewal_year, last_renewal_status=user_detail_obj.renewal_status,
                        new_user_type=str(request.POST.get('Membership_type')).strip(), 
                        new_member_associate_no=str(request.POST.get('MemberAssociateNo')).strip(),
                        new_acceptance_date=acceptance_date, created_by=str(request.user))
                    member_track_obj.save()

                    user_detail_obj.user_type = str(request.POST.get('Membership_type')).strip()
                    m_no_list = str(request.POST.get('MemberAssociateNo')).strip().split('-')
                    mem_no = str(m_no_list[0].strip()) + '-' + str(m_no_list[1].strip())
                    user_detail_obj.member_associate_no = mem_no
                    user_detail_obj.membership_acceptance_date = acceptance_date
                    user_detail_obj.updated_date = datetime.datetime.now()
                    user_detail_obj.save()

                    membership_user_obj = MembershipUser.objects.get(userdetail=user_detail_obj)
                    membership_user_obj.username=user_detail_obj.member_associate_no
                    membership_user_obj.save()
                    transaction.savepoint_commit(sid)
                    data['success'] = 'true'
                except Exception,e:
                    print '\nadding to track history error = ',e
                    log.debug('Error = {0}\n'.format(e))
                    data['success'] = 'false'
                    transaction.rollback(sid)
                        
        except Exception,e:
            print '\n',e            
            try:
                userDetail = UserDetail.objects.get(id=request.POST.get('Member_id'), is_deleted=False)
                userDetail.user_type = request.POST.get('Membership_type')
                m_no_list = str(request.POST.get('MemberAssociateNo')).strip().split('-')
                mem_no = str(m_no_list[0].strip()) + '-' + str(m_no_list[1].strip())
                userDetail.member_associate_no = mem_no
                userDetail.membership_acceptance_date = datetime.datetime.strptime(request.POST.get('AcceptanceDate'),
                                                                                   '%d/%m/%Y')
                userDetail.payment_method = "Confirmed"
                userDetail.save()            
                membership_user_obj = MembershipUser(username=userDetail.member_associate_no)
                membership_user_obj.userdetail = userDetail
                membership_user_obj.set_password('mccia@test')
                membership_user_obj.save()
            except Exception,e:
                print 'MembershipUser duplicate.',e                
                log.debug('Error = {0}\n'.format(e))
                transaction.rollback(sid)
                data['success'] = 'exists'
                return HttpResponse(json.dumps(data), content_type='application/json')
            transaction.savepoint_commit(sid)
            data['success'] = 'true'            
            send_mail_welcome_letter(userDetail)
            pass

        print 'Request OUT | members_details | submit_user_acceptance_detail | user ', request.user
    except Exception, e:        
        log.debug('Error = {0}\n'.format(e))
        print 'exception ', str(traceback.print_exc())
        print 'Exception|membership_details | submit_user_acceptance_detail = ',str(traceback.print_exc())
        data['success'] = 'false'
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


#  Todo Send mail for Welcome Format ---------new html format-----
def send_mail_welcome_letter(userDetail):
    try:
        imgpath=os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        fp = open(imgpath, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<img>')

        ###### ========== password generate #######
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        passlen = 8
        password = "".join(random.sample(s, passlen))
        password = 'mccia@test'

        amount_payable_text = ''
        to_list = []
        ctx = {
            'member_name':userDetail.ceo_name if userDetail.enroll_type == 'CO' else userDetail.company.company_name,
            'member_no':userDetail.member_associate_no,
            'member_address':userDetail.correspond_address,
            'telephone_no':userDetail.ceo_cellno if userDetail.enroll_type == 'CO' else userDetail.correspond_cellno,
            'login_id': userDetail.member_associate_no,
            'password' : password,
            'company_name': userDetail.company.company_name,
            'member_obj': userDetail
        }
        gmail_user = "membership@mcciapune.com"
        gmail_pwd = "mem@2011ship"

        # to_list.append(userDetail.ceo_email)
        if userDetail.poc_email or userDetail.company.hoddetail.finance_email:
            to_list.append(str(userDetail.ceo_email))
            to_list.append(str(userDetail.poc_email))
            to_list.append(str(userDetail.company.hoddetail.finance_email))
        else:
            to_list.append(str(userDetail.ceo_email))


        html=get_template('backoffice/membership/email_welcome_letter.html').render(Context(ctx))
        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html, 'html',_charset=charset)
        msg.attach(htmlfile)
        msg.attach(msgImage)

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        TO = to_list
        CC = ['membership@mcciapune.com', 'vijendra.chandel@bynry.com']
        # CC = ['vijendra.chandel@bynry.com']

        msg['subject'] = 'Your Application is Approved. Welcome to MCCIA.'
        msg['from'] = 'mailto: <membership@mcciapune.com>'
        msg['to'] = ",".join(TO)
        msg['cc'] = ",".join(CC)
        toaddrs = TO + CC
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()
        data = {'success': 'true'}
        print 'Response Out|membership_details.py|send_mail_welcome_letter|Mail is send to', TO
        # return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, exc:
        print 'Exception|membership_details.py|send_mail_welcome_letter|User %s Excepton ',  str(traceback.print_exc())
        data = {'success': 'true', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')

#  Todo Send mail for Welcome Format ----------new html format-------


@transaction.atomic
@csrf_exempt
def submit_user_receipt_detail(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | members_details | submit_user_receipt_detail | user %s', request.user

        membershipInvoice = MembershipInvoice.objects.get(id=request.POST.get('invoice_id'))
        paymentDetails = PaymentDetails.objects.get(userdetail_id=request.POST.get('member_id'), id=request.POST.get('mem_pay_receipt_id'), is_deleted=False)
        amount_paid = 0
        tds_flag = False


        if membershipInvoice.userdetail.is_reassociate:
            membershipInvoice.invoice_for = 'RE-ASSOCIATE'
            membershipInvoice.save()

        if request.POST.get('settle_tds_amount_status') == 'Yestds':
            amount_paid = Decimal(request.POST.get('tds_amount')) + Decimal(request.POST.get('AmountPaid'))
            tds_flag = True
        else:
            amount_paid = Decimal(request.POST.get('AmountPaid'))

        if amount_paid < paymentDetails.amount_payable:
            paymentDetails.amount_paid = str(request.POST.get('AmountPaid'))
            if tds_flag:
                paymentDetails.tds_amount = Decimal(request.POST.get('tds_amount'))
                paymentDetails.is_tds = True

            if request.POST.get('is_cheque_bounce_amount') == 'yes':
                paymentDetails.amount_due = str(paymentDetails.amount_payable - (
                        amount_paid - Decimal(
                    str(request.POST.get('cheque_bounce_amount')))))
                paymentDetails.cheque_bounce_charge = Decimal(str(request.POST.get('cheque_bounce_amount')))
            else:
                paymentDetails.amount_due = str(
                    paymentDetails.amount_payable - amount_paid)
            paymentDetails.payment_date = datetime.date.today()
            paymentDetails.payment_received_status = 'Partial'
            paymentDetails.save()

            # Save MBK Number
            bk_no = 'MBK' + str(paymentDetails.id).zfill(7)
            paymentDetails.bk_no = str(bk_no)
            paymentDetails.save()

            if request.POST.get('settle_amount_status') == 'No':
                new_payment_obj = PaymentDetails(userdetail_id=request.POST.get('member_id'),
                                                 membershipInvoice_id=membershipInvoice.id,
                                                 amount_payable=str(paymentDetails.amount_due),
                                                 financial_year=str(paymentDetails.financial_year),
                                                 payment_received_status='UnPaid')
                new_payment_obj.save()
            else:
                paymentDetails.is_settled = True,
                paymentDetails.settle_amount = Decimal(request.POST.get('settle_amount_rs'))
                # paymentDetails.settle_amount = paymentDetails.amount_due
                paymentDetails.save()

        elif amount_paid > paymentDetails.amount_payable:
            paymentDetails.amount_paid = str(request.POST.get('AmountPaid'))
            if tds_flag:
                paymentDetails.tds_amount = Decimal(request.POST.get('tds_amount'))
                paymentDetails.is_tds = True
            if request.POST.get('is_cheque_bounce_amount') == 'yes':
                paymentDetails.amount_next_advance = paymentDetails.amount_next_advance + (
                    (amount_paid - Decimal(
                    str(request.POST.get('cheque_bounce_amount')))) - paymentDetails.amount_payable)
                paymentDetails.cheque_bounce_charge = Decimal(str(request.POST.get('cheque_bounce_amount')))
            else:
                paymentDetails.amount_next_advance = paymentDetails.amount_next_advance + (amount_paid - paymentDetails.amount_payable)
            paymentDetails.payment_date = datetime.date.today()
            paymentDetails.payment_received_status = 'Paid'
            paymentDetails.save()
            paymentDetails.next_advance_gst_amount = round(float(paymentDetails.amount_next_advance) * 0.18,0)
            paymentDetails.save()

            # Save MBK Number
            bk_no = 'MBK' + str(paymentDetails.id).zfill(7)
            paymentDetails.bk_no = str(bk_no)
            paymentDetails.save()
        else:
            paymentDetails.amount_paid = str(request.POST.get('AmountPaid'))
            paymentDetails.payment_date = datetime.date.today()
            paymentDetails.payment_received_status = 'Paid'
            paymentDetails.cheque_bounce_charge = Decimal(str(request.POST.get('cheque_bounce_amount')))
            if tds_flag:
                paymentDetails.tds_amount = Decimal(request.POST.get('tds_amount'))
                paymentDetails.is_tds = True
            paymentDetails.save()

            # Save MBK Number
            bk_no = 'MBK' + str(paymentDetails.id).zfill(7)
            paymentDetails.bk_no = str(bk_no)
            paymentDetails.save()

        # Save Payment Mode
        if request.POST.get('user_Payment_Type') == 'ByCash':
            paymentDetails.user_Payment_Type = 'Cash'
            paymentDetails.cash_amount = str(request.POST.get('AmountPaid'))
        elif request.POST.get('user_Payment_Type') == 'ByCheque':
            paymentDetails.user_Payment_Type = 'Cheque'
            paymentDetails.cheque_no = str(request.POST.get('ChequeNo'))
            paymentDetails.cheque_date = datetime.datetime.strptime(request.POST.get('ChequeDate'), '%d/%m/%Y').date()
            paymentDetails.bank_name = str(request.POST.get('BankName'))
        else:
            paymentDetails.user_Payment_Type = 'NEFT'
            paymentDetails.neft_transfer_id = str(request.POST.get('neft_transfer_id'))
        paymentDetails.save()

        # Check for Valid / Invalid and Change Renewal Year to Membership Year Flag
        payment_detail_list = PaymentDetails.objects.filter(userdetail_id=request.POST.get('member_id'),
                                                            membershipInvoice=membershipInvoice,
                                                            financial_year=str(membershipInvoice.financial_year),
                                                            is_deleted=False)
        tds_amount_list = payment_detail_list.values('tds_amount')
        amount_paid_list = payment_detail_list.values('amount_paid')
        total_tds = sum(item['tds_amount'] for item in tds_amount_list)
        total_amount_paid = sum(item['amount_paid'] for item in amount_paid_list)
        total_amount_paid = total_amount_paid + total_tds

        user_detail_obj = UserDetail.objects.get(id=request.POST.get('member_id'))
        if membershipInvoice.amount_payable == total_amount_paid or total_amount_paid > membershipInvoice.amount_payable or request.POST.get(
                'settle_amount_status') == 'Yes':
            user_detail_obj.membership_year = str(membershipInvoice.financial_year)
            if membershipInvoice.invoice_for == "RENEW":
                user_detail_obj.renewal_status = 'COMPLETED'
            if user_detail_obj.valid_invalid_member is False:
                user_detail_obj.valid_invalid_member = True
            user_detail_obj.updated_date = datetime.datetime.now()
            user_detail_obj.payment_method = 'Confirmed'
            user_detail_obj.save()
            membershipInvoice.is_paid = True
            if request.POST.get('settle_amount_status') == 'Yes':
                membershipInvoice.is_settled = True
                membershipInvoice.settle_amount = paymentDetails.settle_amount

        if membershipInvoice.amount_payable == total_amount_paid or request.POST.get('settle_tds_amount_status') == 'Yestds':
            if request.POST.get('settle_tds_amount_status') == 'Yestds':
                membershipInvoice.is_tds = True
                membershipInvoice.tds_amount = paymentDetails.tds_amount
            membershipInvoice.save()

        send_renew_mail_ack(request, paymentDetails, user_detail_obj)
        transaction.savepoint_commit(sid)

        data = {'success': 'true'}
        print '\nRequest OUT | members_details | submit_user_receipt_detail | user %s', request.user
    except Exception, e:
        print '\nException IN |membership_details | submit_user_receipt_detail = ',str(traceback.print_exc())
        data = {'success': 'false', 'userdetail_id': str(request.POST.get('member_id'))}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')

def email_acknowledge(request):
    return render(request, 'backoffice/membership/email_welcome_letter.html')


#  Todo Send mail to support for Offline Payment ---------new html format-----
def send_mail_offline_payment(paymentDetails,membershipInvoice,userDetail):
    try:
        print "int(membershipInvoice.amount_payable)",float(paymentDetails.membershipInvoice.amount_payable),paymentDetails.membershipInvoice.amount_payable
        amount_payable_text = num2words(paymentDetails.membershipInvoice.amount_payable, to='cardinal', lang='en_IN')
        print "amount_payable_text-------------", (amount_payable_text)
        imgpath=os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        fp = open(imgpath, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<img1>')

        to_list = []
        ctx = {
            'company_name':userDetail.company.company_name,
            'membership_type':userDetail.user_type,
            'amount_payable': int(membershipInvoice.amount_payable),
            'amount_payable_text':num2words(paymentDetails.membershipInvoice.amount_payable, to='cardinal', lang='en_IN'),
            'financial_year': paymentDetails.financial_year,
            'user_name' : userDetail.ceo_email,
            'user_obj': userDetail
        }

        gmail_user = "membership@mcciapune.com"
        gmail_pwd = "mem@2011ship"

        if userDetail.enroll_type == "CO":
            if userDetail.company.ceo_email_confirmation == True:
                if userDetail.poc_email and userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.ceo_email))
                    to_list.append(str(userDetail.poc_email))
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
                elif userDetail.poc_email:
                    to_list.append(str(userDetail.ceo_email))
                    to_list.append(str(userDetail.poc_email))
                elif userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.ceo_email))
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
                else:
                    to_list.append(str(userDetail.ceo_email))
            else:
                if userDetail.poc_email and userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.poc_email))
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
                elif userDetail.poc_email:
                    to_list.append(str(userDetail.poc_email))
                elif userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
        else:
            to_list.append(str(userDetail.ceo_email))

        html=get_template('backoffice/membership/email_offline_payment.html').render(Context(ctx))
        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html, 'html',_charset=charset)
        msg.attach(htmlfile)
        msg.attach(msgImage)

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        TO = to_list
        CC = ['membership@mcciapune.com', 'vijendra.chandel@bynry.com']
        # CC = ['vijendra.chandel@bynry.com']

        msg['subject'] = 'Membership Acknowledgement'
        msg['from'] = 'mailto: <membership@mcciapune.com>'
        msg['to'] = ",".join(TO)
        msg['cc'] = ",".join(CC)
        toaddrs = TO + CC
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()
        data = {'success': 'true'}
        print 'Response Out|membership_details.py|send_mail_offline_payment|Mail is send to', TO
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, exc:
        print 'Exception|membership_details.py|send_mail_offline_payment|User %s Excepton ',  str(traceback.print_exc())
        data = {'success': 'true', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')

#  Todo Send mail to support for Offline Payment ----------new html format-------


#  Todo Send mail to support for Online Payment---------new html format-----
def send_mail_online_payment(paymentDetails,membershipInvoice,userDetail):
    try:
        amount_payable_text = num2words(int(paymentDetails.membershipInvoice.amount_payable), to='cardinal', lang='en_IN')
        print (amount_payable_text)
        imgpath = os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        fp = open(imgpath, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<img1>')

        to_list = []
        ctx = {
            'comapny_name': userDetail.company.company_name,
            'membership_type': userDetail.user_type,
            'amount_payable': int(membershipInvoice.amount_payable),
            'amount_payable_text': amount_payable_text,
            'financial_year': paymentDetails.financial_year,
            'user_name': userDetail.ceo_email,
            'user_obj': userDetail
        }

        gmail_user = "membership@mcciapune.com"
        gmail_pwd = "mem@2011ship"

        if userDetail.enroll_type == "CO":
            if userDetail.company.ceo_email_confirmation == True:
                if userDetail.poc_email and userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.ceo_email))
                    to_list.append(str(userDetail.poc_email))
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
                elif userDetail.poc_email:
                    to_list.append(str(userDetail.ceo_email))
                    to_list.append(str(userDetail.poc_email))
                elif userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.ceo_email))
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
                else:
                    to_list.append(str(userDetail.ceo_email))
            else:
                if userDetail.poc_email and userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.poc_email))
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
                elif userDetail.poc_email:
                    to_list.append(str(userDetail.poc_email))
                elif userDetail.company.hoddetail.finance_email:
                    to_list.append(str(userDetail.company.hoddetail.finance_email))
        else:
            to_list.append(str(userDetail.ceo_email))


        html=get_template('backoffice/membership/email_online_payment.html').render(Context(ctx))
        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html, 'html',_charset=charset)
        msg.attach(htmlfile)
        msg.attach(msgImage)

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        TO = to_list
        CC = ['membership@mcciapune.com', 'vijendra.chandel@bynry.com']
        # CC = ['vijendra.chandel@bynry.com']

        msg['subject'] = 'Membership Acknowledgement'
        msg['from'] = 'mailto: <membership@mcciapune.com>'
        msg['to'] = ",".join(TO)
        msg['cc'] = ",".join(CC)
        toaddrs = TO + CC
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()
        data = {'success': 'true'}
        print 'Response Out|membership_details.py|send_mail_online_payment|Mail is send to', TO
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, exc:
        print 'Exception|membership_details.py|send_mail_online_payment|User %s Excepton ', str(traceback.print_exc())
        data = {'success': 'true', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')

#  Todo Send mail to support for Online Payment ----------new html format-------


# Send Renewal Acknowlegement Mail
def send_renew_mail_ack(request, paymentDetails, userDetail):
    try:
        if Decimal(paymentDetails.membershipInvoice.entrance_fees) == Decimal(0):
            print '\nRequest IN | membership_details.py | send_renew_mail_ack '
            amount_paid_text = num2words(int(Decimal(paymentDetails.amount_paid)), to='cardinal', lang='en_IN')
            imgpath = os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
            fp = open(imgpath, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<img1>')

            to_list = []
            ctx = {
                'payment_obj': paymentDetails,
                'amount_paid_text': amount_paid_text,
                'user_obj': userDetail
            }

            gmail_user = "membership@mcciapune.com"
            gmail_pwd = "mem@2011ship"

            if userDetail.enroll_type == "CO":
                if userDetail.company.ceo_email_confirmation == True:
                    if userDetail.poc_email and userDetail.company.hoddetail.finance_email:
                        to_list.append(str(userDetail.ceo_email))
                        to_list.append(str(userDetail.poc_email))
                        to_list.append(str(userDetail.company.hoddetail.finance_email))
                    elif userDetail.poc_email:
                        to_list.append(str(userDetail.ceo_email))
                        to_list.append(str(userDetail.poc_email))
                    elif userDetail.company.hoddetail.finance_email:
                        to_list.append(str(userDetail.ceo_email))
                        to_list.append(str(userDetail.company.hoddetail.finance_email))
                    else:
                        to_list.append(str(userDetail.ceo_email))
                else:
                    if userDetail.poc_email and userDetail.company.hoddetail.finance_email:
                        to_list.append(str(userDetail.poc_email))
                        to_list.append(str(userDetail.company.hoddetail.finance_email))
                    elif userDetail.poc_email:
                        to_list.append(str(userDetail.poc_email))
                    elif userDetail.company.hoddetail.finance_email:
                        to_list.append(str(userDetail.company.hoddetail.finance_email))
                    else:
                        to_list.append(str(userDetail.ceo_email))    
            else:
                to_list.append(str(userDetail.ceo_email))


            html=get_template('backoffice/membership/email_renew_ack.html').render(Context(ctx))
            msg = MIMEMultipart('related')
            htmlfile = MIMEText(html, 'html', _charset=charset)

            msg.attach(htmlfile)
            msg.attach(msgImage)
            # if paymentDetails.membershipInvoice.is_paid:
            #     pdf_response = download_certificate(request, userDetail.id)
            #     attachment = MIMEApplication(pdf_response.rendered_content)
            #     attachment['Content-Disposition'] = 'attachment; filename="MCCIA_Membership_Certificate.pdf"'
            #     msg.attach(attachment)

            server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)

            TO = to_list
            CC = ['membership@mcciapune.com','vijendra.chandel@bynry.com']
            # CC = ['vijendra.chandel@bynry.com']

            msg['subject'] = 'Renewal Acknowledgement Receipt'
            msg['from'] = 'mailto: <membership@mcciapune.com>'
            msg['to'] = ",".join(TO)
            msg['cc'] = ",".join(CC)
            toaddrs = TO + CC
            server.sendmail(msg['from'], toaddrs, msg.as_string())
            server.quit()
            data = {'success': 'true'}
            print '\nResponse OUT | membership_details.py | send_renew_mail_ack | Mail is send to', TO
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return            
    except Exception, exc:
        print '\nException | membership_details.py | send_renew_mail_ack | EXCP = ', str(traceback.print_exc())
        data = {'success': 'true', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def delete_user_payment_entry(request):
    data = {}
    sid = transaction.savepoint()
    today_date = datetime.datetime.now().date()
    try:
        print '\nRequest IN | membership_details | delete_user_payment_entry | user %s', request.user        
        if request.POST:            
            payment_detail_obj = PaymentDetails.objects.get(id=request.POST.get('payment_entry_id'))
            invoice_obj = MembershipInvoice.objects.get(id=payment_detail_obj.membershipInvoice.id)
            user_detail_obj = UserDetail.objects.get(id=payment_detail_obj.userdetail.id)
            last_invoice_obj = MembershipInvoice.objects.filter(~Q(financial_year=invoice_obj.financial_year),
                                                             userdetail=user_detail_obj).order_by('financial_year').last()
            payment_detail_list = PaymentDetails.objects.filter(userdetail=payment_detail_obj.userdetail,
                                                                financial_year=payment_detail_obj.financial_year,
                                                                is_deleted=False).order_by('id')
            target_date = datetime.datetime.strptime(str(invoice_obj.financial_year)[0:4] + "-07-01",
                                                     "%Y-%m-%d").date()

            # if payment_detail_obj.payment_received_status == "Paid":                
            payment_detail_obj.is_deleted = True
            if request.POST.get("delete_payment_radio") == "cheque_bounce":
                payment_detail_obj.is_cheque_bounce = True
                payment_detail_obj.payment_remark = str(request.POST.get('delete_remark')) if str(request.POST.get('delete_remark')).strip() and str(request.POST.get('delete_remark')).strip() != '' else 'Cheque Bounce'
            elif request.POST.get("delete_payment_radio") == "neft_failed":
                payment_detail_obj.is_neft_failed = True
                payment_detail_obj.payment_remark = str(request.POST.get('delete_remark')) if str(request.POST.get('delete_remark')).strip() and str(request.POST.get('delete_remark')).strip() != '' else 'NEFT Failed'
            else:
                payment_detail_obj.is_other = True
                payment_detail_obj.payment_remark = str(request.POST.get('delete_remark')) if str(request.POST.get('delete_remark')).strip() and str(request.POST.get('delete_remark')).strip() != '' else 'Remark not provided'
            payment_detail_obj.updated_by = str(request.user)
            payment_detail_obj.updated_date = datetime.datetime.now()
            payment_detail_obj.save()

            # Change is_paid status of MembershipInvoice Table
            invoice_obj.is_paid = False
            invoice_obj.save()

            # Change renewal status in UserDetail Table
            if str(payment_detail_obj.financial_year) == str(user_detail_obj.renewal_year):
                if user_detail_obj.renewal_status == "COMPLETED":
                    user_detail_obj.renewal_status = "STARTED"
                    user_detail_obj.membership_year = last_invoice_obj.financial_year
                    user_detail_obj.save()

            # Get previous Valid - Invalid Status
            user_detail_obj.valid_invalid_member = invoice_obj.valid_invalid_member
            user_detail_obj.updated_date = datetime.datetime.now()
            user_detail_obj.save()

            # Get previous Valid - Invalid Status Using Date method
            # if today_date > target_date:
            #     user_detail_obj.valid_invalid_member = False
            #     user_detail_obj.save()

            # Create another entry in Payment
            new_payment_obj = PaymentDetails(userdetail=payment_detail_obj.userdetail,
                                             membershipInvoice=payment_detail_obj.membershipInvoice,
                                             amount_payable=payment_detail_obj.amount_payable,
                                             amount_last_advance=payment_detail_obj.amount_last_advance,
                                             financial_year=payment_detail_obj.financial_year,
                                             updated_date=datetime.datetime.now(), created_by=str(request.user))
            new_payment_obj.save()

            transaction.savepoint_commit(sid)                    

        data['success'] = 'true'
        print '\nRequest OUT | membership_details | delete_user_payment_entry | user %s', request.user
    except Exception, e:
        transaction.rollback(sid)
        data['success'] = 'false'
        print '\nException | membership_details | delete_user_payment_entry | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


############################ end _ of user payment ################


# Show Edit Slab / Payment Modal
def get_edit_payment_modal(request):
    data = {}
    try:
        print '\nRequest IN | membership_details | get_edit_payment_modal | user =', request.user
        payment_obj = PaymentDetails.objects.get(id=request.GET.get('edit_payment_id'))
        category_list = []
        slab_list = []

        for slab_item in MembershipSlab.objects.filter(is_deleted=False):
            slab_list.append(
                {'slab_id': slab_item.id,
                 'slab_name': slab_item.slab + ' - Rs ' + slab_item.annual_fee + ' - ' + slab_item.applicableTo
                }
            )

        data = {'success': 'true', 'category_list': category_list, 'user_cat': payment_obj.userdetail.membership_category.id,
                'user_to': payment_obj.userdetail.annual_turnover_rupees,
                'user_slab': payment_obj.userdetail.membership_slab.id,
                'slab_list': slab_list}

        print '\nResponse OUT | membership_details | get_edit_payment_modal | user = ', request.user
    except Exception, e:
        print '\nException | membership_details | get_edit_payment_modal = ', traceback.print_exc()
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Update Slab / Payment Detail
@csrf_exempt
@transaction.atomic
def update_slab_payment_detail(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_details | update_slab_payment_detail | user =', request.user
        payment_obj = PaymentDetails.objects.get(id=request.POST.get('edit_payment_id'))
        user_obj = payment_obj.userdetail
        invoice_obj = payment_obj.membershipInvoice
        slab_obj = MembershipSlab.objects.get(id=request.POST.get('edit_slab'))
        gstObj = Servicetax.objects.get(tax_type=0, is_active=True)
        annual_fee = 0

        if slab_obj.membershipCategory.enroll_type == "Life Membership":
            annual_fee = float(slab_obj.annual_fee)
        else:
            if str(request.POST.get('quarter')) == '2018-2019/ full year':
                annual_fee = float(slab_obj.annual_fee)
            elif str(request.POST.get('quarter')) == '2018-2019/ half year':
                annual_fee = float(slab_obj.annual_fee) * 2/4
            elif str(request.POST.get('quarter')) == '2018-2019/ 3 quarters':
                annual_fee = float(slab_obj.annual_fee) * 3/4
            elif str(request.POST.get('quarter')) == '2018-2019/ Last Quarters':
                annual_fee = float(slab_obj.annual_fee) * 1/4
            elif str(request.POST.get('quarter')) == '2019-2020/ full year':
                annual_fee = float(slab_obj.annual_fee)
            elif str(request.POST.get('quarter')) == '2019-2020/ half year':
                annual_fee = float(slab_obj.annual_fee) * 2/4
            elif str(request.POST.get('quarter')) == '2019-2020/ 3 quarters':
                annual_fee = float(slab_obj.annual_fee) * 3/4
            elif str(request.POST.get('quarter')) == '2019-2020/ Last Quarters':
                annual_fee = float(slab_obj.annual_fee) * 1/4

        entrance_fee = slab_obj.entrance_fee
        subscription_charges = slab_obj.annual_fee
        tax_amount = (float(annual_fee) + float(entrance_fee)) * float(gstObj.tax) / 100
        amount_payable = float(annual_fee) + float(entrance_fee) + tax_amount

        invoice_obj.membership_category = user_obj.membership_category = slab_obj.membershipCategory
        invoice_obj.membership_slab = user_obj.membership_slab = slab_obj
        user_obj.annual_turnover_rupees = request.POST.get('edit_to')
        invoice_obj.save()
        user_obj.save()

        if amount_payable > payment_obj.amount_payable:
            invoice_obj.subscription_charges = subscription_charges
            invoice_obj.entrance_fees = entrance_fee
            invoice_obj.tax = tax_amount
            invoice_obj.amount_payable = round(amount_payable,0)
            invoice_obj.is_paid = False
            invoice_obj.save()
            if payment_obj.amount_paid > 0:
                payment_obj.amount_payable = round(amount_payable,0)
                payment_obj.save()
                payment_obj.amount_due = Decimal(payment_obj.amount_payable) - Decimal(payment_obj.amount_paid)
                payment_obj.payment_received_status = 'Partial'
                payment_obj.save()

                new_payment_obj = PaymentDetails(userdetail=payment_obj.userdetail,
                                                 membershipInvoice=invoice_obj,
                                                 amount_payable=str(payment_obj.amount_due),
                                                 financial_year=str(payment_obj.financial_year),
                                                 payment_received_status='UnPaid',
                                                 created_by=str(request.user))
                new_payment_obj.save()
            else:
                payment_obj.amount_payable = round(amount_payable,0)
                payment_obj.save()
        elif amount_payable < payment_obj.amount_payable:
            invoice_obj.subscription_charges = subscription_charges
            invoice_obj.entrance_fees = entrance_fee
            invoice_obj.tax = tax_amount
            invoice_obj.amount_payable = round(amount_payable,0)
            invoice_obj.save()
            payment_obj.amount_payable = round(amount_payable,0)
            payment_obj.save()
            if payment_obj.amount_paid > 0:
                invoice_obj.is_paid = True
                invoice_obj.save()
                payment_obj.amount_next_advance = payment_obj.amount_next_advance + (Decimal(payment_obj.amount_paid) - Decimal(payment_obj.amount_payable))
                payment_obj.payment_received_status = 'Paid'
                payment_obj.save()
                payment_obj.next_advance_gst_amount = round(float(payment_obj.amount_next_advance) * (float(gstObj.tax) / 100), 0)
                payment_obj.save()
            else:
                payment_obj.amount_payable = round(amount_payable,0)
                payment_obj.save()

        payment_obj.updated_by = invoice_obj.updated_by = user_obj.updated_by = str(request.user)
        payment_obj.updated_date = invoice_obj.updated_date = user_obj.updated_date = datetime.datetime.now()
        payment_obj.save()
        invoice_obj.save()
        user_obj.save()        

        transaction.savepoint_commit(sid)
        data['success'] = 'true'
        print '\nResponse OUT | membership_details | update_slab_payment_detail | user = ', request.user
    except Exception, e:
        print '\nException | membership_details | update_slab_payment_detail = ', traceback.print_exc()
        data['success'] = 'false'
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Show Edit Membership Form
def show_edit_member_form(request):
    data = {}
    try:
        print '\nRequest IN | membership_details | show_edit_member_form | user %s', request.user

        member_obj = UserDetail.objects.get(id=request.GET.get('member_id'))

        membershipCategory = MembershipCategory.objects.filter(is_deleted=False)
        industrydescObj = IndustryDescription.objects.filter(is_deleted=False)
        legalstatusObj = LegalStatus.objects.filter(is_deleted=False)
        stateObj = State.objects.filter(is_deleted=False)
        cityObj = City.objects.filter(is_deleted=False).exclude(state__isnull=True)
        fact_cityObj = City.objects.filter(state=member_obj.factorystate, is_deleted=False).exclude(state__isnull=True)
        countryObj = Country.objects.filter(is_deleted=False)
        membershipDescriptionObj = MembershipDescription.objects.filter(is_deleted=False)

        data = {
            'industrydescObj': industrydescObj, 'legalstatusObj': legalstatusObj, 'stateObj': stateObj,
            'cityObj': cityObj, 'countryObj': countryObj, 'membershipDescriptionObj': membershipDescriptionObj,
            'membershipCategory': membershipCategory, 'fact_cityObj': fact_cityObj, 'member_obj': member_obj,
            'export_country_list': str(
                member_obj.company.textexport.split(",")) if member_obj.company.textexport else None,
            'import_country_list': str(
                member_obj.company.textimport.split(",")) if member_obj.company.textimport else None
        }

        print '\nResponse OUT | membership_details | show_edit_member_form | user %s', request.user
    except Exception, e:
        print 'Exception| membership_details | show_edit_member_form | get_membership_details_datatable|', traceback.print_exc()
        data = {'msg': 'error'}
    return render(request, 'backoffice/membership/edit_member_detail.html', data)


# Update Member Detail
@transaction.atomic
@csrf_exempt
def update_member_detail(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_details | update_member_detail | user %s', request.user

        IndustryDescriptionList = []
        MembershipDescriptionList = []
        data = request.POST
    
        # captcha = request.POST.get('g - recaptcha - response')

        # ''' Begin reCAPTCHA validation '''
        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # print "recaptcha_response",recaptcha_response
        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # values = {
        #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # data = urllib.urlencode(values)
        # print data
        # req = urllib2.Request(url, data)
        # print "req", req
        # response = urllib2.urlopen(req)
        # result = json.load(response)
        # ''' End reCAPTCHA validation '''

        # if result['success']:
        #
        #     messages.success(request, 'New comment added with success!')
        # else:
        #     messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        if (request.POST.get('correspondence_GST') == "UnderProcess"):
            gst_option = "UP"
        elif (request.POST.get('correspondence_GST') == "Applicable"):
            gst_option = "AP"
        elif (request.POST.get('correspondence_GST') == "NotApplicable"):
            gst_option = "NA"

        # if request.POST.get('company_scale_radiobtn'):
        if (request.POST.get('radiobtn-1')):
            if (request.POST.get('radiobtn-1') == "Micro"):
                company_scale = "MR"
            elif (request.POST.get('radiobtn-1') == "Small"):
                company_scale = "SM"
            elif (request.POST.get('radiobtn-1') == "MediumScale"):
                company_scale = "MD"
            elif (request.POST.get('radiobtn-1') == "LargeScale"):
                company_scale = "LR"
        else:
            company_scale = "MR"

        userDetail_obj = UserDetail.objects.get(id=request.POST.get('edit_member_id'))
        userDetail_obj.poc_name = request.POST.get("pocName")
        userDetail_obj.poc_contact = request.POST.get("pocContact")
        userDetail_obj.poc_email = request.POST.get("pocEmail")
        userDetail_obj.save()

        userDetail = UserDetail.objects.get(id=request.POST.get('edit_member_id'))

        if str(userDetail.enroll_type).strip() != str(request.POST.get("check_user_type")).strip() or str(userDetail.company.company_name).strip() != str(request.POST.get('CompanyApplicantName')).strip():
            membership_type_track_obj = MembershipTypeTrack(userdetail=userDetail, old_company_name=str(userDetail.company.company_name).strip(),
                                                            old_user_type=userDetail.user_type, old_enroll_type=userDetail.enroll_type,
                                                            old_member_associate_no=userDetail.member_associate_no, old_acceptance_date=userDetail.membership_acceptance_date,
                                                            old_category=userDetail.membership_category, old_slab=userDetail.membership_slab,
                                                            last_membership_year=userDetail.membership_year, last_renewal_year=userDetail.renewal_year, last_renewal_status=userDetail.renewal_status,
                                                            new_user_type=userDetail.user_type, new_member_associate_no=userDetail.member_associate_no, new_acceptance_date=userDetail.membership_acceptance_date,
                                                            created_by=str(request.user))
            membership_type_track_obj.save()

        company_detail = CompanyDetail.objects.get(id=userDetail.company.id)
        hoddetail = ''        

        try:
            if company_detail.hoddetail:
                hoddetail = HOD_Detail.objects.get(id=company_detail.hoddetail.id)
                hoddetail.hr_name = request.POST.get('HRName')
                hoddetail.hr_contact = request.POST.get('HRContact')
                hoddetail.hr_email = request.POST.get('HREmail')
                hoddetail.finance_name = request.POST.get('FinanceName')
                hoddetail.finance_contact = request.POST.get('FinanceContact')
                hoddetail.finance_email = request.POST.get('FinanceEmail')
                hoddetail.marketing_name = request.POST.get('MarketingName')
                hoddetail.marketing_contact = request.POST.get('MarketingContact')
                hoddetail.marketing_email = request.POST.get('MarketingEmail')
                hoddetail.IT_name = request.POST.get('ITName')
                hoddetail.IT_contact = request.POST.get('ITContact')
                hoddetail.IT_email = request.POST.get('ITEmail')
                hoddetail.corp_rel_name = request.POST.get('CorpRelName')
                hoddetail.corp_rel_contact = request.POST.get('CorpRelContact')
                hoddetail.corp_rel_email = request.POST.get('CorpRelEmail')
                hoddetail.tech_name = request.POST.get('TechName')
                hoddetail.tech_contact = request.POST.get('TechContact')
                hoddetail.tech_email = request.POST.get('TechEmail')
                hoddetail.rnd_name = request.POST.get('RandDName')
                hoddetail.rnd_email = request.POST.get('RandDEmail')
                hoddetail.rnd_contact = request.POST.get('RandDContact')
                hoddetail.exim_name = request.POST.get('EXIMName')
                hoddetail.exim_contact = request.POST.get('EXIMContact')
                hoddetail.exim_email = request.POST.get('EXIMEmail')
                hoddetail.stores_name = request.POST.get('StoreName')
                hoddetail.stores_contact = request.POST.get('StoreContact')
                hoddetail.stores_email = request.POST.get('StoreEmail')

                hoddetail.purchase_name = request.POST.get('PurchaseName')
                hoddetail.purchase_contact = request.POST.get('PurchaseContact')
                hoddetail.purchase_email = request.POST.get('PurchaseEmail')

                hoddetail.production_name = request.POST.get('ProductionName')
                hoddetail.production_contact = request.POST.get('ProductionContact')
                hoddetail.production_email = request.POST.get('ProductionEmail')

                hoddetail.quality_name = request.POST.get('QualityName')
                hoddetail.quality_contact = request.POST.get('QualityContact')
                hoddetail.quality_email = request.POST.get('QualityEmail')

                hoddetail.supply_chain_name = request.POST.get('SupplyName')
                hoddetail.supply_chain_contact = request.POST.get('SupplyContact')
                hoddetail.supply_chain_email = request.POST.get('SupplyEmail')

                hoddetail.save()                
            else:
                new_hoddetail_obj = HOD_Detail(hr_name=request.POST.get('HRName'), hr_contact=request.POST.get('HRContact'), hr_email=request.POST.get('HREmail'),
                            finance_name = request.POST.get('FinanceName'),finance_contact = request.POST.get('FinanceContact'), finance_email = request.POST.get('FinanceEmail'),
                            marketing_name=request.POST.get('MarketingName'),marketing_contact=request.POST.get('MarketingContact'),marketing_email=request.POST.get('MarketingEmail'),
                            IT_name=request.POST.get('ITName'), IT_contact=request.POST.get('ITContact'), IT_email=request.POST.get('ITEmail'),
                            corp_rel_name=request.POST.get('CorpRelName'),corp_rel_contact=request.POST.get('CorpRelContact'),corp_rel_email=request.POST.get('CorpRelEmail'),
                            tech_name=request.POST.get('TechName'), tech_contact=request.POST.get('TechContact'), tech_email=request.POST.get('TechEmail'),
                            rnd_name=request.POST.get('RandDName'), rnd_email=request.POST.get('RandDEmail'), rnd_contact=request.POST.get('RandDContact'),
                            exim_name=request.POST.get('EXIMName'), exim_contact=request.POST.get('EXIMContact'), exim_email=request.POST.get('EXIMEmail')
                            ,stores_name = request.POST.get('StoreName'), stores_contact = request.POST.get('StoreContact'), stores_email = request.POST.get('StoreEmail'),
                            purchase_name = request.POST.get('PurchaseName'), purchase_contact = request.POST.get('PurchaseContact'), purchase_email = request.POST.get('PurchaseEmail'),
                            production_name = request.POST.get('ProductionName'), production_contact = request.POST.get('ProductionContact'), production_email = request.POST.get('ProductionEmail'),
                            quality_name = request.POST.get('QualityName'), quality_contact = request.POST.get('QualityContact'), quality_email = request.POST.get('QualityEmail'),
                            supply_chain_name = request.POST.get('SupplyName'), supply_chain_contact = request.POST.get('SupplyContact'), supply_chain_email = request.POST.get('SupplyEmail')
                            )
                new_hoddetail_obj.save()
                company_detail.hoddetail = new_hoddetail_obj
                company_detail.save()
                hoddetail = new_hoddetail_obj
                pass

        except Exception, exc:
            print 'exception in Hod Detail', str(traceback.print_exc())
            pass


        try:

            # if request.POST.get('RandDfacilityAvailable') == "RandDfacilityAvailable":
            #     rnd_facility = True
            # else:
            #     rnd_facility = False
            #
            # if request.POST.get('RecognisedbyGovt') == "RecognisedbyGovt":
            #     govt_recognised = True
            # else:
            #     govt_recognised = False
            #
            # if request.POST.get('ForeignCollaborations') == "ForeignCollaborations":
            #     foreign_collaboration = True
            # else:
            #     foreign_collaboration = False
            # if request.POST.get('100EOU') == "100EOU":
            #     eou = True
            # else:
            #     eou = False
            #
            # if request.POST.get('ISOAwards'):
            #     isodetail = request.POST.get('ISOOtherStdsAwards')
            #     iso_check = True
            # else:
            #     isodetail = "NA"
            #     iso_check = False

            if request.POST.get('factoryAddressField') == "factoryAddressField":
                same_as_above = True
            else:
                same_as_above = False

            if request.POST.get('mailreceiveconfirmbox') == "mailreceiveconfirmbox":
                ceo_email_confirmation = True
            else:
                ceo_email_confirmation = False

            if request.POST.get('turnover_range') == "0":
                turnover_range = 0

            if request.POST.get('turnover_range') == "1":
                turnover_range = 1

            if request.POST.get('turnover_range') == "2":
                turnover_range = 2

            if request.POST.get('turnover_range') == "3":
                turnover_range = 3

            if request.POST.get('turnover_range') == "4":
                turnover_range = 4

            if request.POST.get('turnover_range') == "5":
                turnover_range = 5


            if request.POST.get('employee_range') == "0":
                employee_range = 0

            if request.POST.get('employee_range') == "1":
                employee_range = 1


            if request.POST.get('employee_range') == "2":
                employee_range = 2


            if request.POST.get('employee_range') == "3":
                employee_range = 3


            if request.POST.get('employee_range') == "4":
                employee_range = 4

            if request.POST.get('areaofexperties') == "Engineer":
                area_of_experties = 1
            elif request.POST.get('areaofexperties') == "CA":
                area_of_experties = 2
            elif request.POST.get('areaofexperties') == "Doctors":
                area_of_experties = 3
            elif request.POST.get('areaofexperties') == "Consultant":
                area_of_experties = 4
            elif request.POST.get('areaofexperties') == "Marketing_Professional":
                area_of_experties = 5
            elif request.POST.get('areaofexperties') == "Valuers":
                area_of_experties = 6
            elif request.POST.get('areaofexperties') == "individual_finance_brokers":
                area_of_experties = 7
            elif request.POST.get('areaofexperties') == "real_estate_broker":
                area_of_experties = 8
            elif request.POST.get('areaofexperties') == "lawyers_solicitors":
                area_of_experties = 9
            elif request.POST.get('areaofexperties') == "management_consultant":
                area_of_experties = 10
            elif request.POST.get('areaofexperties') == "trainers":
                area_of_experties = 11
            elif request.POST.get('areaofexperties') == "project_consultants":
                area_of_experties = 12
            elif request.POST.get('areaofexperties') == "others":
                area_of_experties = 13
            else:
                area_of_experties = 0

            print "________area_of_experties___________________",area_of_experties

        except:
            # rnd_facility = False
            # govt_recognised = False
            # foreign_collaboration = False
            # eou = False
            same_as_above = False
            ceo_email_confirmation = False
            turnover_range = 0
            employee_range = 0
            area_of_experties = 0
            pass


        if (request.POST.get("check_user_type") == "CO"):

            if request.POST.get('PlantMcRs'):
                block_inv_plant = request.POST.get('PlantMcRs')
            else:
                block_inv_plant = 0
            if request.POST.get('LandBldgRs'):
                block_inv_land = request.POST.get('LandBldgRs')
            else:
                block_inv_land = 0
            if request.POST.get('TotalRsCr'):
                block_inv_total = request.POST.get('TotalRsCr')
            else:
                block_inv_total = 0

            if request.POST.get('Manager'):
                total_manager = request.POST.get('Manager')
            else:
                total_manager = 0

            if request.POST.get('Staff'):
                total_staff = request.POST.get('Staff')
            else:
                total_staff = 0
            if request.POST.get('Workers'):
                total_workers = request.POST.get('Workers')
            else:
                total_workers = 0
            if request.POST.get('Total'):
                total_employees = request.POST.get('Total')
            else:
                total_employees = 0

            ceo_name = request.POST.get('CEO')
            ceo_contact = request.POST.get('CEOContact')
            person_name = request.POST.get('CEO')
            person_email = request.POST.get('FactoryEmail')
            person_designation = request.POST.get('FactoryWebsite')
            person_cellno = request.POST.get('FactoryContact')
            factory_address = request.POST.get('FactoryAddress')
            if request.POST.get('FactoryState'):
                factorystate = State.objects.get(id=request.POST.get('FactoryState'))
            else:
                factorystate = None
            if request.POST.get('FactoryCity'):                
                factorycity = City.objects.get(id=request.POST.get('FactoryCity'))
            else:
                factorycity = None
            
            factory_pincode = request.POST.get('FactoryPin')
            factory_std1 = request.POST.get('FactorySTD1')
            factory_std2 = request.POST.get('FactorySTD2')
            factory_landline1 = request.POST.get('FactoryLandline2')
            factory_landline2 = request.POST.get('FactoryLandline2')
            factory_cellno = request.POST.get('FactoryContact')
            membership_type = "MM"
            enroll_type = "CO"
        else:            
            block_inv_plant = 0
            block_inv_land = 0
            block_inv_total = 0
            total_manager = 0
            total_staff = 0
            total_workers = 0
            total_employees = 0
            ceo_name = ""
            ceo_contact = ""
            person_name = ""
            person_email = ""
            person_designation = ""
            person_cellno = request.POST.get('CorrespondenceContact')
            factory_address = ""
            if request.POST.get('FactoryState'):
                factorystate = State.objects.get(id=request.POST.get('FactoryState'))
            else:
                factorystate = None
            if request.POST.get('FactoryCity'):                
                factorycity = City.objects.get(id=request.POST.get('FactoryCity'))
            else:
                factorycity = None
            factory_pincode = ""
            factory_std1 = ""
            factory_std2 = ""
            factory_landline1 = ""
            factory_landline2 = ""
            factory_cellno = ""
            membership_type = "MM"
            enroll_type = "IN"

        if request.POST.get('YearofEstablishment'):
            yearOfEstablishment = request.POST.get('YearofEstablishment')
        else:
            yearOfEstablishment = 0

        userDetail = UserDetail.objects.get(id=request.POST.get('edit_member_id'))

        try:
            company_detail = CompanyDetail.objects.get(id=userDetail.company.id)
            company_detail.company_name = request.POST.get('CompanyApplicantName')
            company_detail.description_of_business = request.POST.get('DescriptionofBusiness')
            company_detail.establish_year = yearOfEstablishment
            company_detail.company_scale = company_scale
            company_detail.block_inv_plant = block_inv_plant
            company_detail.block_inv_land = block_inv_land
            company_detail.block_inv_total = block_inv_total
            company_detail.textexport = request.POST.get('TextExport')
            company_detail.textimport = request.POST.get('TextImport')
            # company_detail.rnd_facility = rnd_facility
            # company_detail.govt_recognised = govt_recognised
            # company_detail.iso = iso_check
            # company_detail.iso_detail = isodetail
            # company_detail.foreign_collaboration = foreign_collaboration
            # company_detail.eou = eou
            company_detail.eou_detail = request.POST.get('NameCountries')
            company_detail.total_manager = total_manager
            company_detail.total_staff = total_staff
            company_detail.total_workers = total_workers
            company_detail.total_employees = total_employees
            company_detail.same_as_above = same_as_above
            company_detail.turnover_range = turnover_range
            company_detail.employee_range = employee_range
            company_detail.ceo_email_confirmation = ceo_email_confirmation
            company_detail.industrydescription_other = request.POST.get('otherindustry_discription')
            # industrydescription=IndustryDescription.objects.get(id=request.POST.get('industry_description')),
            company_detail.legalstatus = LegalStatus.objects.get(id=request.POST.get('legalStatus'))

        except Exception, exc:
            print 'exception in Company Detail Saving ', str(traceback.print_exc())

        if request.POST.get('CorrespondenceAadharCheck') == "on":
            aadhar_no = 0
        else:
            aadhar_no = request.POST.get('CorrespondenceAadhar')

        if request.POST.get('CorrespondencePanCheck') == "on":
            panNo = "NA"
        else:
            panNo = request.POST.get('CorrespondencePan')

        if request.POST.get('CorrespondenceGSTText'):
            CorrespondenceGSTText = request.POST.get('CorrespondenceGSTText')
        else:
            CorrespondenceGSTText = 'NA'

        try:
            userDetail = UserDetail.objects.get(id=request.POST.get('edit_member_id'))

            userDetail.ceo_name = ceo_name
            userDetail.ceo_designation = ceo_name
            userDetail.ceo_cellno = ceo_contact
            if (request.POST.get("check_user_type") == "CO"):
                userDetail.ceo_email = request.POST.get('CEOEmail')
            else:
                userDetail.ceo_email=request.POST.get('CEOEmailin')


            userDetail.correspond_address = request.POST.get('CorrespondenceAddress')
            userDetail.correspond_email = request.POST.get('CorrespondenceEmail')
            userDetail.correspondstate = State.objects.get(id=request.POST.get('CorrespondenceState'))
            userDetail.correspondcity = City.objects.get(id=request.POST.get('CorrespondenceCity'))
            userDetail.correspond_cellno = request.POST.get('CorrespondenceContact')
            userDetail.correspond_pincode = request.POST.get('CorrespondencePin')
            userDetail.correspond_std1 = request.POST.get('CorrespondenceStd1')
            userDetail.correspond_std2 = request.POST.get('CorrespondenceStd2')
            userDetail.correspond_landline1 = request.POST.get('CorrespondenceLandline1')
            userDetail.correspond_landline2 = request.POST.get('CorrespondenceLandline2')
            userDetail.website = request.POST.get('CorrespondenceWebsite')
            userDetail.gst = CorrespondenceGSTText
            userDetail.gst_in = gst_option
            userDetail.pan = panNo
            userDetail.aadhar = aadhar_no
            # userDetail.awards = isodetail
            userDetail.person_name = person_name
            userDetail.person_email = person_email
            userDetail.person_designation = person_designation
            userDetail.person_cellno = person_cellno
            userDetail.factory_address = factory_address
            userDetail.factorystate = factorystate
            userDetail.factorycity = factorycity
            userDetail.factory_pincode = factory_pincode
            userDetail.factory_std1 = factory_std1
            userDetail.factory_std2 = factory_std2
            userDetail.factory_landline1 = factory_landline1
            userDetail.factory_landline2 = factory_landline2
            userDetail.factory_cellno = factory_cellno
            userDetail.membership_type = membership_type
            userDetail.enroll_type = enroll_type
            userDetail.area_of_experties = area_of_experties
            userDetail.experties_other =  request.POST.get('otherareaofexperties')
            if request.POST.get('MembershipCategory'):
                userDetail.membership_category = MembershipCategory.objects.get(id=request.POST.get('MembershipCategory'))
            if request.POST.get('MembershipSlab'):
                userDetail.membership_slab = MembershipSlab.objects.get(id=request.POST.get('MembershipSlab'))
            userDetail.annual_turnover_year = request.POST.get('foryear') if request.POST.get('foryear') else ''
            userDetail.annual_turnover_rupees = request.POST.get('Rscrore') if request.POST.get('Rscrore') else ''
            # userDetail.membership_year = str(request.POST.get('MembershipForYear'))[0:9]

        except Exception, exc:
            print 'exception in USER DETAIL SAVING ', str(traceback.print_exc())

        print request.POST.get('entrance_fee')

        if company_detail.hoddetail:
            hoddetail.save()
        else:
            pass
        company_detail.save()
        if hoddetail:
            hod_id = HOD_Detail.objects.get(id=hoddetail.id)
        else:
            hod_id = None
        company_detail.hoddetail = hod_id
        company_detail.save()
        exportList = []
        if request.POST.get('multi-select-export-country'):
            exportList = request.POST.getlist('multi-select-export-country')
            for i in exportList:
                exportcountryobj = Country.objects.get(id=i)
                company_detail.exportcountry.add(exportcountryobj)
            company_detail.save()
        if request.POST.get('multi-select-import-country'):
            importList = request.POST.getlist('multi-select-import-country')
            for i in importList:
                importcountryobj = Country.objects.get(id=i)
                company_detail.importcountry.add(importcountryobj)
                company_detail.save()

        userDetail.updated_date = datetime.datetime.now()
        userDetail.save()
        userDetail.company_id = company_detail.id

        company_detail.industrydescription.clear()        
        for key, value in data.iteritems():
            valueList = []
            print value
            if str(key) == 'IndustryDescription':
                value=request.POST.getlist('IndustryDescription')
                valueList = value                
                for j in value:
                    company_detail.industrydescription.add(j)
                    company_detail.save()        

        # if (request.POST.get("paymentMode") == "Offline"):
        #     userDetail.payment_method = "Offline"
        #     cheque_no = request.POST.get('Cheque_no')
        #     cheque_date = datetime.datetime.strptime(request.POST.get('cheque_date'), '%d/%m/%Y')
        #     bank_name = request.POST.get('bank_name')
        # else:
        #     userDetail.payment_method = "Online"
        #     cheque_no = ""
        #     cheque_date = datetime.date.today()
        #     bank_name = ""
        # userDetail.save()
        # member_invoice_obj = MembershipInvoice.objects.get(userdetail_id=request.POST.get('edit_member_id'))
        # member_invoice_obj.subscription_charges = float(request.POST.get('subsciption_charges'))
        # member_invoice_obj.entrance_fees = float(request.POST.get('entrance_fee'))
        # member_invoice_obj.tax = float(request.POST.get('tax_amount'))
        # member_invoice_obj.amount_payable = float(request.POST.get('payable_amount'))
        # member_invoice_obj.save()

        # paymentDetails_obj = PaymentDetails.objects.get(userdetail_id=request.POST.get('edit_member_id'))
        # paymentDetails_obj.membershipInvoice_id=member_invoice_obj.id
        # cheque_no=cheque_no
        # cheque_date=cheque_date
        # bank_name=bank_name
        # paymentDetails_obj.save()

        transaction.savepoint_commit(sid)
        # member_invoice(request, userDetail.id, userDetail.membership_year)

        data = {'success': 'true'}
        print '\nResponse OUT | membership_details | update_member_detail | user %s', request.user
    except Exception, e:
        print '\nException| membership_details | update_member_detail = ', e
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Show Renew Membership Form
def show_renew_member_form(request):
    data = {}
    try:
        print '\nRequest IN | membership_details | show_renew_member_form | user %s', request.user

        user_detail_obj = UserDetail.objects.get(id=request.GET.get('user_id'))
        membershipCategory = MembershipCategory.objects.filter(status=True)
        industrydescObj = IndustryDescription.objects.filter(is_active=True)
        legalstatusObj = LegalStatus.objects.filter(status=True)

        current_membership_year = int(str(user_detail_obj.membership_year)[5:9])
        renewal_year = str(current_membership_year) + '-' + str(current_membership_year + 1)

        current_year = datetime.datetime.now()
        next_year = current_year + relativedelta(years=+1)

        year_list = []
        i = 0
        to_current_year = datetime.datetime.now()
        prev_year = to_current_year - relativedelta(years=+1)
        while i < 5:
            year_list.append(str(prev_year.year) + '-' + str(to_current_year.year))
            prev_year = prev_year - relativedelta(years=+1)
            to_current_year = to_current_year - relativedelta(years=+1)
            i = i + 1

        data = {
            'industrydescObj': industrydescObj, 'legalstatusObj': legalstatusObj,
            'membershipCategory': membershipCategory, 'member_obj': user_detail_obj,
            'formatted_renewal_year': renewal_year,'year_list': year_list, 'renewal_year': renewal_year
        }
        print '\nResponse OUT | membership_details | show_renew_member_form | User %s ', request.user
    except Exception,e:
        print '\nException IN | membership_details | show_renew_member_form = ', str(traceback.print_exc())
    return render(request, 'backoffice/membership/renew_membership.html', data)


# Get Renewal Membership Invoice
@csrf_exempt
def get_member_renew_invoice(request):
    data = {}    
    try:
        print '\nRequest IN | membership_details | get_member_renew_invoice | User %s ', request.user
        user_detail_obj = UserDetail.objects.get(id=request.POST.get('user_detail_id'))
        category_obj = MembershipCategory.objects.get(id=request.POST.get('category_id'))
        slab_obj = MembershipSlab.objects.get(id=request.POST.get('slab_id'))

        gst_amount = round(float(slab_obj.annual_fee) * 0.18,0)

        payment_detail_obj = PaymentDetails.objects.filter(userdetail=user_detail_obj,
                                                            financial_year=user_detail_obj.membership_year,
                                                            is_deleted=False).last()
        
        due_amount = 0
        advance_amount = 0
        if payment_detail_obj:            
            advance_amount = round(float(payment_detail_obj.amount_next_advance), 0)
            
            amount_payable = 0
            temp_amount_payable = round(float(slab_obj.annual_fee), 0) + gst_amount        

            if advance_amount > temp_amount_payable:
                amount_payable = 0            
            else:
                amount_payable = temp_amount_payable - advance_amount            

            if payment_detail_obj.payment_received_status == 'UnPaid':            

                payment_detail_obj_list = PaymentDetails.objects.filter(userdetail=user_detail_obj,
                                                                   financial_year=user_detail_obj.membership_year,
                                                                   is_deleted=False)
                if payment_detail_obj_list.count() == 1:
                    payment_detail_obj = PaymentDetails.objects.get(userdetail=user_detail_obj,
                                                                   financial_year=user_detail_obj.membership_year,
                                                                   is_deleted=False)
                    due_amount = round(float(payment_detail_obj.amount_payable),0)

                for i in payment_detail_obj_list:
                    if i.amount_due > 0 and i.payment_received_status == 'Partial':
                        due_amount = i.amount_due

            amount_payable = Decimal(amount_payable) + Decimal(due_amount)
        else:
            amount_payable = Decimal(slab_obj.annual_fee) + Decimal(str(gst_amount))


        print '\nResponse OUT | membership_details | get_member_renew_invoice | User %s ', request.user
        data = {'success': 'true', 'category': str(category_obj.membership_category),
                'slab': str(slab_obj.slab), 'renewal_year': str(request.POST.get('renewal_year')),
                'subscription_charge': str(slab_obj.annual_fee), 'gst_amount': str(gst_amount),
                'due_amount': str(due_amount), 'advance_amount': str(advance_amount), 'amount_payable': str(amount_payable)
                }
    except Exception,e:
        data = {'success': 'false'}
        print '\nException IN | membership_details | get_member_renew_invoice = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Save Renewal Invoice Data
@transaction.atomic
@csrf_exempt
def renew_member(request):    
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_details | renew_member | User %s ', request.user        

        user_detail_obj = UserDetail.objects.get(id=request.POST.get('member_id'))
        user_detail_obj.membership_category = MembershipCategory.objects.get(id=str(request.POST.get('membership_category')))
        user_detail_obj.membership_slab = MembershipSlab.objects.get(id=str(request.POST.get('slab_category')))
        user_detail_obj.annual_turnover_year = request.POST.get('annual_to_year')
        user_detail_obj.annual_turnover_rupees = request.POST.get('annual_to')
        user_detail_obj.renewal_year = request.POST.get('membership_renew_year')
        user_detail_obj.renewal_status = 'STARTED'
        user_detail_obj.updated_date = datetime.datetime.now()
        user_detail_obj.save()

        member_invoice_obj = MembershipInvoice(userdetail=user_detail_obj,
                                               subscription_charges=str(request.POST.get('subscription_charges')),
                                               tax=str(request.POST.get('tax_amount')),
                                               without_adv_amount_payable=Decimal(
                                                   str(request.POST.get('subscription_charges'))) + Decimal(
                                                   str(request.POST.get('tax_amount'))),
                                               amount_payable=str(request.POST.get('amount_payable')),
                                               financial_year=str(request.POST.get('membership_renew_year')),
                                               last_due_amount=str(request.POST.get('due_amount')),
                                               last_advance_amount=str(request.POST.get('advance_amount')),
                                               invoice_for='RE-ASSOCIATE' if user_detail_obj.is_reassociate else 'RENEW',
                                               membership_category=user_detail_obj.membership_category,
                                               membership_slab=user_detail_obj.membership_slab,
                                               valid_invalid_member=user_detail_obj.valid_invalid_member)
        member_invoice_obj.save()

        payment_detail_obj = PaymentDetails(userdetail=user_detail_obj,
                                            membershipInvoice=member_invoice_obj,
                                            amount_payable=str(request.POST.get('amount_payable')),
                                            payment_received_status='UnPaid',
                                            financial_year=str(request.POST.get('membership_renew_year')),
                                            amount_last_advance=str(request.POST.get('advance_amount'))
                                            )
        payment_detail_obj.save()

        if Decimal(payment_detail_obj.amount_last_advance) > Decimal(payment_detail_obj.amount_payable):            
            payment_detail_obj.amount_next_advance = Decimal(payment_detail_obj.amount_last_advance) - Decimal(member_invoice_obj.without_adv_amount_payable)
            payment_detail_obj.save()

        user_detail_obj.is_reassociate = False
        user_detail_obj.save()

        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print '\nResponse OUT | membership_details | renew_member | User %s ', request.user
    except Exception,e:
        data = {'success': 'false'}
        print '\nException IN | membership_details | renew_member | User %s ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Print Member Form
def print_user_form(request, m_id):
    try:
        print '\nRequest IN | membership_details | print_user_form | User = ', request.user
        industry_data_list = []
        category_data_list = []
        category_temp_list = []
        legal_data_list = []
        industry_temp_list = []
        export_country_list = []
        import_country_list = []
        payment_obj_list = []
        invoice_obj = None
        payment_obj = None
        check_flag = True
        total_paid = 0

        user_detail_obj = UserDetail.objects.get(id=m_id)
        membershipCategory = MembershipCategory.objects.filter(is_deleted=False)
        industrydescObj = IndustryDescription.objects.filter(is_deleted=False)
        legalstatusObj = LegalStatus.objects.filter(is_deleted=False)

        for industry_item in industrydescObj:
            if industry_item in user_detail_obj.company.industrydescription.all():
                industry_temp_list.append({'status': True, 'industry': str(industry_item.description)})
            else:
                industry_temp_list.append({'status': False, 'industry': str(industry_item.description)})
        industry_data_list = [industry_temp_list[x:x + 5] for x in xrange(0, len(industry_temp_list), 5)]

        for legal_item in legalstatusObj:
            if user_detail_obj.company.legalstatus == legal_item:
                legal_data_list.append({'status': True, 'legal_status': str(legal_item.description)})
            else:
                legal_data_list.append({'status': False, 'legal_status': str(legal_item.description)})

        for category in membershipCategory:
            if user_detail_obj.membership_category == category:
                category_temp_list.append({'status': True, 'category': str(category.membership_category) + '_' + str(category.enroll_type)})
            else:
                category_temp_list.append({'status': False, 'category': str(category.membership_category) + '_' + str(category.enroll_type)})
        category_data_list = [category_temp_list[x:x + 5] for x in xrange(0, len(category_temp_list), 5)]

        try:
            invoice_obj = MembershipInvoice.objects.filter(userdetail=user_detail_obj).last()
            if invoice_obj is None:
                raise ObjectDoesNotExist
            if invoice_obj.invoice_for == 'NEW':
                payment_object_list = PaymentDetails.objects.filter(userdetail=user_detail_obj,membershipInvoice=invoice_obj, is_deleted=False)
                for payment_obj in payment_object_list:
                    total_paid = total_paid + payment_obj.amount_paid
            else:
                payment_obj_list = PaymentDetails.objects.filter(userdetail=user_detail_obj, membershipInvoice=invoice_obj)
                payment_obj = PaymentDetails.objects.filter(userdetail=user_detail_obj, membershipInvoice=invoice_obj).last()
        except Exception:
            check_flag = False
            pass

        if payment_obj_list:
            for payment_obj_item in payment_obj_list:
                total_paid = total_paid + payment_obj_item.amount_paid

        # invoice_obj = MembershipInvoice.objects.filter(userdetail=user_detail_obj).first()
        # payment_obj = PaymentDetails.objects.filter(userdetail=user_detail_obj, membershipInvoice=invoice_obj).first()

        template = get_template('backoffice/membership/print_form.html')
        html = template.render(Context({
            'industry_data_list': industry_data_list,
            'legal_data_list': legal_data_list,
            'category_data_list': category_data_list,
            'user_obj': user_detail_obj,
            'invoice_obj': invoice_obj,
            'payment_obj': payment_obj,
            'check_flag': check_flag,
            'total_paid': total_paid
        }))
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    except Exception,e:
        print '\nException IN | membership_details | print_user_form | Excp = ', str(traceback.print_exc())
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def get_user_track_history_page(request, m_id):
    print '\nRequest IN | membership_details | get_user_track_history_page | User = ',request.user
    data = {'m_id': m_id}
    print '\nResponse OUT | membership_details | get_user_track_history_page | User = ', request.user
    return render(request, 'backoffice/membership/user_history.html', data)


def get_user_track_history_table(request):
    try:
        print '\nRequest IN | members_details | get_user_track_history_table | user = ', request.user
        data_list = []
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        user_history_list = MembershipTypeTrack.objects.filter(userdetail_id=request.GET.get('m_id'))

        user_history_list = user_history_list.order_by('-created_date')
        total_records = user_history_list.count()
        user_history_list = user_history_list[start:length]
        total_record = total_records

        for item in user_history_list:
            temp_list = []
            temp_list.append(item.created_date.strftime('%d-%m-%Y'))
            temp_list.append(item.old_company_name)
            temp_list.append(item.old_user_type)
            temp_list.append(item.old_enroll_type)
            temp_list.append(item.old_member_associate_no)

            data_list.append(temp_list)

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': data_list}
        print '\nResponse OUT | members_details | get_user_track_history_table | user = ', request.user
    except Exception, e:
        print '\nException | membership_details | get_user_track_history_table = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@transaction.atomic
def download_certificate(request, m_id):
    sid = transaction.savepoint()
    response = None
    try:
        print '\nRequest IN | membership_details | download_certificate | user = ', request.user
        dg_obj = NameSign.objects.get(is_deleted=False, designation=1)
        president_obj = NameSign.objects.get(is_deleted=False, designation=0)
        invoice_obj = MembershipInvoice.objects.filter(userdetail_id=m_id,is_paid=True,is_deleted=False).last()
        show_date = None
        data = {}
        if invoice_obj:
            if invoice_obj.invoice_for=='NEW':
                show_date = invoice_obj.userdetail.membership_acceptance_date
                date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')
            else:
                payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj, is_deleted=False,
                                                            payment_received_status__in=['Paid', 'Partial']).last()
                show_date = payment_obj.payment_date
                date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')

        else:
            return HttpResponse('<center><h2>Sorry. Certificate not found.</h2></center>')

        if invoice_obj.userdetail.user_type == 'Associate':
            data={
                'company_name': str(invoice_obj.userdetail.company.company_name),
                'membership_no': str(invoice_obj.userdetail.member_associate_no),
                'payment_date': str(date_obj),
                'for_year': str(invoice_obj.financial_year),
                'type': 'Associate',
                'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                'president_obj': president_obj,
                'dg_obj': dg_obj
            }
            # data['company_name'] = str(data['company_name']).strip().title()

            tpl = get_template('backoffice/membership/associate_yearly.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context=data,
                filename=str(data['company_name']) + '.pdf',
                show_content_in_browser=False,
                cmd_options={
                    'page-width': '21cm',
                    'page-height': '29.7cm',
                    'margin-top': '0cm',
                    'margin-bottom': '0cm',
                    'margin-left': '0cm',
                    'margin-right': '0cm',
                    'no-outline': None                    
                },
            )

        elif invoice_obj.userdetail.user_type == 'Member':
            data = {
                'company_name': str(invoice_obj.userdetail.company.company_name),
                'membership_no': str(invoice_obj.userdetail.member_associate_no),
                'payment_date': str(date_obj),
                'type': 'Member',
                'for_year': str(invoice_obj.financial_year),
                'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                'president_obj': president_obj,
                'dg_obj': dg_obj
            }
            # data['company_name'] = str(data['company_name']).strip().title()

            tpl = get_template('backoffice/membership/membership_yearly.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context=data,
                filename=str(data['company_name']) + '.pdf',
                show_content_in_browser=False,
                cmd_options={
                    'page-width': '21cm',
                    'page-height': '29.7cm',
                    'margin-top': '0cm',
                    'margin-bottom': '0cm',
                    'margin-left': '0cm',
                    'margin-right': '0cm',
                    'no-outline': None                    
                },
            )
        elif invoice_obj.userdetail.user_type == 'Life Membership':
            if 'Patron' in invoice_obj.userdetail.membership_slab.slab:
                data = {
                    'company_name': str(invoice_obj.userdetail.company.company_name),
                    'membership_no': str(invoice_obj.userdetail.member_associate_no),
                    'payment_date': str(date_obj),
                    'type': 'Patron',
                    'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                    'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                    'president_obj': president_obj,
                    'dg_obj': dg_obj

                }
                # data['company_name'] = str(data['company_name']).strip().title()

                tpl = get_template('backoffice/membership/patron_life_membership.html')
                response = PDFTemplateResponse(
                    request=request,
                    template=tpl,
                    context=data,
                    filename=str(data['company_name']) + '.pdf',
                    show_content_in_browser=False,
                    cmd_options={
                        'page-width': '21cm',
                        'page-height': '29.7cm',
                        'margin-top': '0cm',
                        'margin-bottom': '0cm',
                        'margin-left': '0cm',
                        'margin-right': '0cm',
                        'no-outline': None                        
                    },
                )
            elif 'Benefactor' in invoice_obj.userdetail.membership_slab.slab:
                data = {
                    'company_name': str(invoice_obj.userdetail.company.company_name),
                    'membership_no': str(invoice_obj.userdetail.member_associate_no),
                    'payment_date': str(date_obj),
                    'type': 'Benefactor',
                    'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                    'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                    'president_obj': president_obj,
                    'dg_obj': dg_obj
                }
                # data['company_name'] = str(data['company_name']).strip().title()
                tpl = get_template('backoffice/membership/benefactor_life_membership.html')
                response = PDFTemplateResponse(
                    request=request,
                    template=tpl,
                    context=data,
                    filename=str(data['company_name']) + '.pdf',
                    show_content_in_browser=False,
                    cmd_options={
                        'page-width': '21cm',
                        'page-height': '29.7cm',
                        'margin-top': '0cm',
                        'margin-bottom': '0cm',
                        'margin-left': '0cm',
                        'margin-right': '0cm',
                        'no-outline': None                        
                    },
                )

            else:
                data = {
                    'company_name': str(invoice_obj.userdetail.company.company_name),
                    'membership_no': str(invoice_obj.userdetail.member_associate_no),
                    'payment_date': str(date_obj),
                    'type': 'Life-Member',
                    'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                    'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                    'president_obj': president_obj,
                    'dg_obj': dg_obj
                }
                # data['company_name'] = str(data['company_name']).strip().title()

                tpl = get_template('backoffice/membership/life_membership.html')
                response = PDFTemplateResponse(
                    request=request,
                    template=tpl,
                    context=data,
                    filename=str(data['company_name']) + '.pdf',
                    show_content_in_browser=False,
                    cmd_options={
                        'page-width': '21cm',
                        'page-height': '29.7cm',
                        'margin-top': '0cm',
                        'margin-bottom': '0cm',
                        'margin-left': '0cm',
                        'margin-right': '0cm',
                        'no-outline': None                        
                    },
                )
        print '\nRequest OUT | membership_details | download_certificate | user = ', request.user
        # print response.rendered_content
        # print response
        transaction.savepoint_commit(sid)
    except Exception, e:
        print '\nException | membership_details | download_certificate = ', str(traceback.print_exc())
        data = {'success': 'false'}
        log.debug('Error = {0}\n'.format(e))
        transaction.rollback(sid)
    return response



@transaction.atomic
def manual_download_certificate(request, m_id):
    sid = transaction.savepoint()
    response = None
    try:
        print '\nRequest IN | membership_details | manual_download_certificate | user = ', request.user
        dg_obj = NameSign.objects.get(is_deleted=False, designation=1)
        president_obj = NameSign.objects.get(is_deleted=False, designation=0)
        invoice_obj = MembershipInvoice.objects.filter(userdetail_id=m_id,is_paid=True,is_deleted=False).last()
        show_date = None
        data = {}
        if invoice_obj:
            if invoice_obj.invoice_for=='NEW':
                show_date = invoice_obj.userdetail.membership_acceptance_date
                date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')
            else:
                payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj, is_deleted=False,
                                                            payment_received_status__in=['Paid', 'Partial']).last()
                show_date = payment_obj.payment_date
                date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')

        else:
            return HttpResponse('<center><h2>Sorry. Certificate not found.</h2></center>')

        if invoice_obj.userdetail.user_type == 'Associate':
            data={
                'company_name': str(invoice_obj.userdetail.company.company_name),
                'membership_no': str(invoice_obj.userdetail.member_associate_no),
                'payment_date': str(date_obj),
                'for_year': str(invoice_obj.financial_year),
                'type': 'Associate',
                'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                'president_obj': president_obj,
                'dg_obj': dg_obj
            }
            # data['company_name'] = str(data['company_name']).strip().title()

            tpl = get_template('backoffice/membership/manual_associate_yealy.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context=data,
                filename=str(data['company_name']) + '.pdf',
                show_content_in_browser=False,
                cmd_options={
                    'page-width': '21.6cm',
                    'page-height': '28cm',
                    'margin-top': '0cm',
                    'margin-bottom': '0cm',
                    'margin-left': '0cm',
                    'margin-right': '0cm',
                    'no-outline': None
                },
            )

        elif invoice_obj.userdetail.user_type == 'Member':
            data = {
                'company_name': str(invoice_obj.userdetail.company.company_name),
                'membership_no': str(invoice_obj.userdetail.member_associate_no),
                'payment_date': str(date_obj),
                'type': 'Member',
                'for_year': str(invoice_obj.financial_year),
                'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                'president_obj': president_obj,
                'dg_obj': dg_obj
            }
            # data['company_name'] = str(data['company_name']).strip().title()

            tpl = get_template('backoffice/membership/manual_membership_yearly.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context=data,
                filename=str(data['company_name']) + '.pdf',
                show_content_in_browser=False,
                cmd_options={
                    'page-width': '21.6cm',
                    'page-height': '28cm',
                    'margin-top': '0cm',
                    'margin-bottom': '0cm',
                    'margin-left': '0cm',
                    'margin-right': '0cm',
                    'no-outline': None
                },
            )
        elif invoice_obj.userdetail.user_type == 'Life Membership':
            if 'Patron' in invoice_obj.userdetail.membership_slab.slab:
                data = {
                    'company_name': str(invoice_obj.userdetail.company.company_name),
                    'membership_no': str(invoice_obj.userdetail.member_associate_no),
                    'payment_date': str(date_obj),
                    'type': 'Patron',
                    'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                    'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                    'president_obj': president_obj,
                    'dg_obj': dg_obj

                }
                # data['company_name'] = str(data['company_name']).strip().title()

                tpl = get_template('backoffice/membership/manual_patron_life_membership.html')
                response = PDFTemplateResponse(
                    request=request,
                    template=tpl,
                    context=data,
                    filename=str(data['company_name']) + '.pdf',
                    show_content_in_browser=False,
                    cmd_options={
                        'page-width': '21.6cm',
                        'page-height': '28cm',
                        'margin-top': '0cm',
                        'margin-bottom': '0cm',
                        'margin-left': '0cm',
                        'margin-right': '0cm',
                        'no-outline': None
                    },
                )
            elif 'Benefactor' in invoice_obj.userdetail.membership_slab.slab:
                data = {
                    'company_name': str(invoice_obj.userdetail.company.company_name),
                    'membership_no': str(invoice_obj.userdetail.member_associate_no),
                    'payment_date': str(date_obj),
                    'type': 'Benefactor',
                    'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                    'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                    'president_obj': president_obj,
                    'dg_obj': dg_obj
                }
                # data['company_name'] = str(data['company_name']).strip().title()

                tpl = get_template('backoffice/membership/manual_benefactor_life_membership.html')
                response = PDFTemplateResponse(
                    request=request,
                    template=tpl,
                    context=data,
                    filename=str(data['company_name']) + '.pdf',
                    show_content_in_browser=False,
                    cmd_options={
                        'page-width': '21.6cm',
                        'page-height': '28cm',
                        'margin-top': '0cm',
                        'margin-bottom': '0cm',
                        'margin-left': '0cm',
                        'margin-right': '0cm',
                        'no-outline': None
                    },
                )

            else:
                data = {
                    'company_name': str(invoice_obj.userdetail.company.company_name),
                    'membership_no': str(invoice_obj.userdetail.member_associate_no),
                    'payment_date': str(date_obj),
                    'type': 'Life-Member',
                    'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                    'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                    'president_obj': president_obj,
                    'dg_obj': dg_obj
                }
                # data['company_name'] = str(data['company_name']).strip().title()

                tpl = get_template('backoffice/membership/manual_life_membership.html')
                response = PDFTemplateResponse(
                    request=request,
                    template=tpl,
                    context=data,
                    filename=str(data['company_name']) + '.pdf',
                    show_content_in_browser=False,
                    cmd_options={
                        'page-width': '21.6cm',
                        'page-height': '28cm',
                        'margin-top': '0cm',
                        'margin-bottom': '0cm',
                        'margin-left': '0cm',
                        'margin-right': '0cm',
                        'no-outline': None
                    },
                )
        print '\nRequest OUT | membership_details | manual_download_certificate | user = ', request.user
        transaction.savepoint_commit(sid)
    except Exception, e:
        print '\nException | membership_details | manual_download_certificate = ', str(traceback.print_exc())
        data = {'success': 'false'}
        log.debug('Error = {0}\n'.format(e))
        transaction.rollback(sid)
    return response

@transaction.atomic
@csrf_exempt
def membership_data_upload(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print '\nRequest IN | membership_details | membership_data_upload | user = ', request.user
        row_values = []
        membership_no_list = []
        comapny_list = []
        check_flag = True

        upFile = request.FILES["excel_file"]
        workbook = xlrd.open_workbook(file_contents=upFile.read())
        number_of_rows = workbook.sheets()[0].nrows
        number_of_columns = workbook.sheets()[0].ncols

        for row in range(2, number_of_rows):
            value = (workbook.sheets()[0].cell(row, 13).value)
            membership_no_list.append(value)

        duplicate_list = []
        membership_no_list.sort()
        for i in range(len(membership_no_list) - 1):
            if membership_no_list[i] == membership_no_list[i + 1]:
                check_flag = False
                duplicate_list.append({
                    'membership_no': str(membership_no_list[i])
                })

        if not check_flag:
            data = {'success': 'duplicate_mem_no', 'duplicate_list': duplicate_list}
            return HttpResponse(json.dumps(data), content_type='application/json')

        for row in range(2, number_of_rows):
            value = (workbook.sheets()[0].cell(row, 1).value)
            comapny_list.append(value)

        for row in range(2, number_of_rows):
            temp_list = []
            for col in range(number_of_columns):
                value = (workbook.sheets()[0].cell(row, col).value)
                temp_list.append(value)
            row_values.append(temp_list)

        membership_no_check = UserDetail.objects.filter(member_associate_no__in=membership_no_list)
        exits_member = []
        if membership_no_check:
            for member in membership_no_check:
                exits_member.append({
                    'exist_mem_no': str(member.member_associate_no),
                    'exist_company_name': str(member.company.company_name).strip()
                })
                check_flag = False
            # data = {'success': 'mem_no_exist', 'error': 'this data already exits', 'data': exits_member}
            # return HttpResponse(json.dumps(data), content_type='application/json')

        check_user = UserDetail.objects.filter(company__company_name__in=comapny_list,
                                               member_associate_no__isnull=False).exclude(member_associate_no__exact='')
        member_not_null = []
        if check_user:
            for member in check_user:
                temp_check_flag = True
                for dict_item in exits_member:
                    if dict_item['exist_mem_no'] == str(member.member_associate_no).strip() and dict_item['exist_company_name'] == str(member.company.company_name).strip():
                        temp_check_flag = False
                if temp_check_flag:
                    member_not_null.append({
                        'exist_mem_no': str(member.member_associate_no).strip(),
                        'exist_company_name': str(member.company.company_name).strip()

                    })
                check_flag = False
            # data = {'success': 'org_already_has_no', 'error': 'this data already exits', 'match': member_not_null}
            # return HttpResponse(json.dumps(data), content_type='application/json')
        if check_flag:
            for row in row_values:
                company_name =row[1].splitlines()[0]
                membership_no = str(row[13]).strip()
                temp_no_list = membership_no.split('-')
                membership_no_update = str(temp_no_list[0]).strip() + '-' + str(temp_no_list[1]).strip()

                acceptance_date = row[14]
                acceptance_date_update = datetime.datetime.fromordinal(
                    datetime.datetime(1900, 1, 1).toordinal() + int(acceptance_date) - 2).date()

                user_detail_id = MembershipInvoice.objects.filter(userdetail__company__company_name=company_name.strip(),
                                                               is_paid=True, is_deleted=False).values('userdetail_id')
                user_detail_obj = UserDetail.objects.get(id=user_detail_id[0]['userdetail_id'])

                user_detail_obj.member_associate_no = str(membership_no_update)
                user_detail_obj.membership_acceptance_date = acceptance_date_update
                user_detail_obj.payment_method = "Confirmed"
                user_detail_obj.save()

                membership_user_obj = MembershipUser(username=user_detail_obj.member_associate_no)
                membership_user_obj.userdetail = user_detail_obj
                membership_user_obj.set_password('mccia@test')
                membership_user_obj.save()

                data = {'success': 'true'}
                send_mail_welcome_letter(user_detail_obj)

            transaction.savepoint_commit(sid)
        else:
            data = {'success': 'error', 'exits_member': exits_member, 'member_not_null': member_not_null}
    except Exception, e:
        log.debug('Error = {0}\n'.format(e))
        print '\nException | membership_details | membership_data_upload = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')



def send_manual_renew_letter(request,m_id):
    try:
        print '\nRequest IN | membership_details| send_manual_renew_letter '
        obj_manual_data = UserDetail.objects.get(id=m_id)

        m_year = "2019-2020"
        renewletter = RenewLetterSchedule.objects.filter(row_type=0).last()
        scheduleobj = RenewLetterSchedule.objects.filter(row_type=1).last()
        membershipscheduleobj = RenewLetterSchedule.objects.filter(row_type=3).last()


        # ctx = {'renewletter': renewletter}

        to_list = []
        gmail_user = "membership@mcciapune.com"
        gmail_pwd = "mem@2011ship"


        # to_list.append(str(object.ceo_email)+','+ str(object.poc_email))
        if obj_manual_data.enroll_type == "CO":
            if obj_manual_data.company.ceo_email_confirmation == True:
                if obj_manual_data.poc_email and obj_manual_data.company.hoddetail.finance_email:
                    to_list.append(str(obj_manual_data.ceo_email))
                    to_list.append(str(obj_manual_data.poc_email))
                    to_list.append(str(obj_manual_data.company.hoddetail.finance_email))
                elif obj_manual_data.poc_email:
                    to_list.append(str(obj_manual_data.ceo_email))
                    to_list.append(str(obj_manual_data.poc_email))
                elif obj_manual_data.company.hoddetail.finance_email:
                    to_list.append(str(obj_manual_data.ceo_email))
                    to_list.append(str(obj_manual_data.company.hoddetail.finance_email))
                else:
                    to_list.append(str(obj_manual_data.ceo_email))
            else:
                if obj_manual_data.poc_email and obj_manual_data.company.hoddetail.finance_email:
                    to_list.append(str(obj_manual_data.poc_email))
                    to_list.append(str(obj_manual_data.company.hoddetail.finance_email))
                elif obj_manual_data.poc_email:
                    to_list.append(str(obj_manual_data.poc_email))
                elif obj_manual_data.company.hoddetail.finance_email:
                    to_list.append(str(obj_manual_data.company.hoddetail.finance_email))
                else:
                   to_list.append(str(obj_manual_data.ceo_email))
        else:
            to_list.append(str(obj_manual_data.ceo_email))

        msg = MIMEMultipart('related')

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        TO = to_list
        CC = ['membership@mcciapune.com', 'vijendra.chandel@bynry.com']
        # CC = ['vijendra.chandel@bynry.com']

        # body = get_template('backoffice/membership/manual_update_letter.html').render(Context(ctx))
        # body = get_template('backoffice/membership/manual_update_letter.html').render()
        # htmlfile = MIMEText(body, 'html', _charset=charset)
        # msg.attach(htmlfile)

        msg['subject'] = 'Renewal of MCCIA Membership for the FY 2019-2020'

        msg['from'] = 'mailto: <membership@mcciapune.com>'
        msg['to'] = ",".join(TO)
        msg['cc'] = ",".join(CC)

        renewl_letter = MIMEText(renewletter.renew_letter,'html')
        msg.attach(renewl_letter)

        pdf_response = download_proforma_invoice(request, m_id, m_year)
        attachment = MIMEApplication(pdf_response.getvalue(), content_type='application/pdf')
        attachment['Content-Disposition'] = 'inline; filename="PI_' + str(m_year) + '_' + str(
            obj_manual_data.company.company_name).strip() + '.pdf"'
        msg.attach(attachment)

        if obj_manual_data.user_type == "Associate":
            schedule = os.path.join(settings.BASE_DIR +'/'+("sitemedia") +'/'+ str(scheduleobj.renew_schedule))
            with open(schedule, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part['Content-Disposition'] = 'inline; filename="schedule_letter' + '.pdf"'
                msg.attach(part)
        else:
            schedule = os.path.join(settings.BASE_DIR + '/' + ("sitemedia") + '/' + str(membershipscheduleobj.renew_membership_schedule))
            with open(schedule, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part['Content-Disposition'] = 'inline; filename="schedule_letter' + '.pdf"'
                msg.attach(part)

        toaddrs = TO + CC
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()
        # data = {'success': 'true'}
        print '\nResponse OUT | membership_details | send_manual_renew_letter | Mail is send to', TO
        return HttpResponse('<center><h2>Mail Sent.</h2></center>')
    except Exception, exc:
        print '\nException | membership_details| send_manual_renew_letter | EXCP = ', str(traceback.print_exc())
        data = {'success': 'true', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def send_certificate_bulk_mail(request):
    return render(request, 'backoffice/membership/bulk_mail_certificate.html')


def get_bulk_mail_certificate_table(request):
    try:
        print '\nRequest IN | membership_details | get_bulk_mail_certificate_table | user %s', request.user
        dataList = []
        meterReadings = []
        data = {}

        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''
        total_records =''

        select_invoice_for = request.GET.get('select_invoice_for')
        acceptance_from = request.GET.get('acceptance_from')

        print "*******************",select_invoice_for
        print "*************acceptance_from******",acceptance_from
        certificate_bulk_list_mail = ''

        if select_invoice_for == 'show_all':
            certificate_bulk_list_mail = MembershipInvoice.objects.filter(userdetail__member_associate_no__isnull=False, is_paid=True, financial_year='2019-2020', userdetail__is_deleted=False)
            # acceptance_from_date = datetime.datetime.strptime(str(request.GET.get('acceptance_from')),'%d/%m/%Y').date()
            # acceptance_to_date = (datetime.datetime.strptime(str(request.GET.get('acceptance_to')), '%d/%m/%Y') + timedelta(days=1)).date()
            # certificate_bulk_list_mail = PaymentDetails.objects.filter(Q(userdetail__membership_acceptance_date__range=[acceptance_from_date, acceptance_to_date]) | Q(
            #     payment_date__range=[acceptance_from_date, acceptance_to_date]),membershipInvoice__is_paid=True, is_deleted=False)
        elif select_invoice_for =='New':
            acceptance_from_date = datetime.datetime.strptime(str(request.GET.get('acceptance_from')),'%d/%m/%Y').date()
            acceptance_to_date = (datetime.datetime.strptime(str(request.GET.get('acceptance_to')), '%d/%m/%Y') + timedelta(days=1)).date()
            certificate_bulk_list_mail = MembershipInvoice.objects.filter(
                userdetail__membership_acceptance_date__range=[acceptance_from_date, acceptance_to_date], is_deleted=False)
        else:
            payment_from_date = datetime.datetime.strptime(str(request.GET.get('acceptance_from')), '%d/%m/%Y').date()
            payment_to_date = (datetime.datetime.strptime(str(request.GET.get('acceptance_to')), '%d/%m/%Y') + timedelta(days=1)).date()
            certificate_bulk_list_mail = PaymentDetails.objects.filter(payment_date__range=[payment_from_date, payment_to_date], membershipInvoice__is_paid=True,
                membershipInvoice__invoice_for__in=['RENEW', 'RE-ASSOCIATE'], is_deleted=False)

        certificate_bulk_list_mail = certificate_bulk_list_mail.filter(Q(userdetail__company__company_name__icontains=searchTxt))
        total_records = certificate_bulk_list_mail.count()

        if length == -1:
            certificate_bulk_list_mail = certificate_bulk_list_mail[:]
        else:
            certificate_bulk_list_mail = certificate_bulk_list_mail[start:length]

        total_record = certificate_bulk_list_mail.count()


        i = 1
        for bulkmail in certificate_bulk_list_mail:
            if bulkmail.id:
                proforma_checkbox = "<input title='select' type='checkbox' class='check_user' id='select_all' value='" + str(
                    bulkmail.id) + "' >"
            if bulkmail.userdetail.mail_sent == 0:
                status = "Not Sent"

            elif bulkmail.userdetail.mail_sent == 1:
                status = "Sent"

            elif bulkmail.userdetail.mail_sent == 2:
                status = "Failed"

            else:
                status = "Schedule"

            tempList = []
            tempList.append(i)
            tempList.append(bulkmail.userdetail.company.company_name)
            tempList.append(bulkmail.userdetail.member_associate_no)
            tempList.append(bulkmail.userdetail.ceo_email)
            tempList.append(status)
            tempList.append(proforma_checkbox)
            dataList.append(tempList)
            i = i + 1

        data = {'iTotalRecords': total_records, 'iTotalDisplayRecords': total_records, 'aaData': dataList}
    except Exception, e:
        print 'Exception|membership_details | get_bulk_mail_certificate_table|User:{0} - Excepton:{1}'.format(
            request.user, e)
    return HttpResponse(json.dumps(data), content_type='application/json')


def create_schedule_bulk_mail(request):
    # request = HttpRequest()
    # request.method = 'GET'
    # request.META['SERVER_NAME'] = 'localhost'
    # request.META['SERVER_PORT'] = 8000
    try:
        print '\nRequest IN | membership_details| create_schedule_bulk_mail '

        for user_detail_obj in UserDetail.objects.filter(mail_sent=3, is_deleted=False):

            user_detail_obj.mail_sent = 1
            user_detail_obj.save()
            to_list = []

            gmail_user = "membership@mcciapune.com"
            gmail_pwd = "mem@2011ship"

            to_list.append('vijendra.chandel@bynry.com')
            msg = MIMEMultipart('related')

            pdf_response = download_certificate(request,user_detail_obj.id)
            attachment = MIMEApplication(pdf_response.rendered_content)
            attachment['Content-Disposition'] = 'attachment; filename="MCCIA_Membership_Certificate.pdf"'
            msg.attach(attachment)

            server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)

            TO = to_list
            CC = ['membership@mcciapune.com', 'vijendra.chandel@bynry.com']
            # CC = ['vijendra.chandel@bynry.com']

            msg['subject'] = 'Membership Certificate-MCCIA'
            msg['from'] = 'mailto: <membership@mcciapune.com>'
            msg['to'] = ",".join(TO)
            msg['cc'] = ",".join(CC)
            toaddrs = TO + CC
            server.sendmail(msg['from'], toaddrs, msg.as_string())
            server.quit()
            # data = {'success': 'true'}
            print '\nResponse OUT | membership_details | create_schedule_bulk_mail | Mail is send to', TO
        # return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, exc:
        print '\nException | membership_details| create_schedule_bulk_mail | EXCP = ', str(traceback.print_exc())
        print '\nerror = ', exc
    return


def create_schedule_job_for_mail(request):
    data={}
    try:
        print '\nResponse IN | membership_details | create_schedule_job'
        sent_user_mail_ids = request.GET.getlist('sent_user_mail_ids[]')
        print "*******************", sent_user_mail_ids

        for i in sent_user_mail_ids:
            member_obj = MembershipInvoice.objects.get(id=i)
            member_object = member_obj.userdetail
            member_object.mail_sent = 3
            member_object.save()
        create_schedule_bulk_mail(request)
        data = {'success': 'true'}
        print '\nResponse OUT | membership_details | create_schedule_job '
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print '\nException IN | membership_details | create_schedule_job | EXCP = ', str(traceback.print_exc())
    return  HttpResponse(json.dumps(data), content_type='application/json')



def send_soft_copy_certificate_through_mail(request, m_id):
    try:
        print '\nRequest IN | membership_details| send_soft_copy_certificate_through_mail '
        member_obj = UserDetail.objects.get(id=m_id)
        print "username = ", member_obj
        invoice_obj = MembershipInvoice.objects.filter(userdetail_id=m_id, is_paid=True, is_deleted=False).last()
        data = {}
        if invoice_obj:
            to_list = []
            gmail_user = "membership@mcciapune.com"
            gmail_pwd = "mem@2011ship"

            if member_obj.enroll_type == "CO":
                if member_obj.company.ceo_email_confirmation == True:
                    if member_obj.poc_email and member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.ceo_email))
                        to_list.append(str(member_obj.poc_email))
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
                    elif member_obj.poc_email:
                        to_list.append(str(member_obj.ceo_email))
                        to_list.append(str(member_obj.poc_email))
                    elif member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.ceo_email))
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
                    else:
                        to_list.append(str(member_obj.ceo_email))
                else:
                    if member_obj.poc_email and member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.poc_email))
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
                    elif member_obj.poc_email:
                        to_list.append(str(member_obj.poc_email))
                    elif member_obj.company.hoddetail.finance_email:
                        to_list.append(str(member_obj.company.hoddetail.finance_email))
            else:
                to_list.append(str(member_obj.ceo_email))


            msg = MIMEMultipart('related')
            server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)

            TO = to_list
            CC = ['membership@mcciapune.com', 'vijendra.chandel@bynry.com']

            html = get_template('backoffice/membership/certificate_mail_content.html').render(Context)
            htmlfile = MIMEText(html, 'html', _charset=charset)
            msg.attach(htmlfile)

            msg['subject'] = 'MCCIA Certificate of renewal for the year 2019-20'
            msg['from'] = 'mailto: <membership@mcciapune.com>'
            msg['to'] = ",".join(TO)
            msg['cc'] = ",".join(CC)

            pdf_response = download_certificate(request, m_id, )
            attachment = MIMEApplication(pdf_response.rendered_content)
            attachment['Content-Disposition'] = 'inline; filename="MCCIA' + '_' + str(
                member_obj.company.company_name).strip() + '.pdf"'
            msg.attach(attachment)

            toaddrs = TO + CC
            server.sendmail(msg['from'], toaddrs, msg.as_string())
            server.quit()
            print '\nResponse OUT | membership_details | send_soft_copy_certificate_through_mail | Mail is send to', TO
            return HttpResponse('<center><h2>Mail Sent.</h2></center>')

        else:
            return HttpResponse('<center><h2>Sorry. Certificate not found.</h2></center>')
    except Exception, exc:
        print '\nException | membership_details| send_soft_copy_certificate_through_mail | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'true', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def hard_copy_certificate_address_download(request,m_id):
    try:
        print '\nRequest IN | membership_details.py | hard_copy_certificate_address_download | User = ', request.user
        member_obj_address = UserDetail.objects.get(id=m_id)
        record_list = []
        data ={}
        if member_obj_address.poc_contact and member_obj_address.correspond_landline1 and member_obj_address.correspond_cellno:
            phone_number = str(member_obj_address.poc_contact) + ',' + str(member_obj_address.correspond_landline1) +','+ str(member_obj_address.correspond_cellno)
        elif member_obj_address.poc_contact and member_obj_address.correspond_landline1:
            phone_number = str(member_obj_address.poc_contact) + ',' + str(member_obj_address.correspond_landline1)
        elif member_obj_address.correspond_landline1 and member_obj_address.correspond_cellno:
            phone_number = str(member_obj_address.correspond_landline1) +','+ str(member_obj_address.correspond_cellno)
        elif member_obj_address.poc_contact and member_obj_address.correspond_cellno:
            phone_number = str(member_obj_address.poc_contact) + ','+ str(member_obj_address.correspond_cellno)
        elif member_obj_address.poc_contact:
            phone_number = str(member_obj_address.poc_contact)
        elif member_obj_address.correspond_cellno:
            phone_number=  str(member_obj_address.correspond_cellno)
        elif member_obj_address.correspond_landline1:
            phone_number = str(member_obj_address.correspond_landline1)
        else:
            phone_number = ""

        if member_obj_address:
            data = {
                'company_name': str(member_obj_address.company.company_name),
                'correspond_address': str(member_obj_address.correspond_address),
                'City_no': str(member_obj_address.correspondcity) + '/' + str(member_obj_address.correspond_pincode),
                'cell_no': phone_number,

            }
            record_list.append(data)

            tpl = get_template('backoffice/membership/certificate_courier_page.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context={'record_list': record_list},
                filename='Hard copy Certificate Address' + '.pdf',
                show_content_in_browser=False,
                cmd_options={
                    'page-width': '20cm',
                    'page-height': '20cm',
                    'margin-top': '0cm',
                    'margin-bottom': '0cm',
                    'margin-left': '0cm',
                    'margin-right': '0cm',
                    'no-outline': None
                },
            )
        print '\nRequest OUT | membership_details | hard_copy_certificate_address_download | user = ', request.user
    except Exception, exc:
        print '\nException | publication_landing | hard_copy_certificate_address_download = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return response
