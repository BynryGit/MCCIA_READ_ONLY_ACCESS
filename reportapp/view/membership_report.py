# System Module Import

import traceback, io, json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from xlsxwriter import Workbook
from authenticationapp.decorator import role_required
from datetime import datetime, timedelta
from django.db.models import Q
import logging
import pdb
from django.utils.translation import ugettext
import operator
import xlrd
# User Module Import

from membershipapp.models import UserDetail, MembershipInvoice, PaymentDetails, CompanyDetail, MembershipTypeTrack, \
    MembershipUser
from adminapp.models import Servicetax, IndustryDescription
from backofficeapp.view.membership_details import send_mail_welcome_letter

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_report_landing(request):
    return render(request, 'backoffice/report/membership_report/membership_report_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership EC Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_ec_report_landing(request):
    return render(request, 'backoffice/report/membership_report/membership_ec_report_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Account Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_account_report_landing(request):
    return render(request, 'backoffice/report/membership_report/membership_account_report_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_online_renewal(request):
    industry_list = []
    industry_obj = IndustryDescription.objects.filter(is_deleted=False)
    for industry_objs in industry_obj:
        industry_obj_data = {
            'id': industry_objs.id,
            'industry_name': industry_objs.description
        }
        industry_list.append(industry_obj_data)
    data = {'industry': industry_list}
    return render(request, 'backoffice/report/membership_report/membership_online_renewal.html', data)


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_change_company_name(request):
    return render(request, 'backoffice/report/membership_report/membership_change_company_name_report.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_cheque_bounce_report(request):
    return render(request, 'backoffice/report/membership_report/membership_cheque_bounce_report.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_subscription_report(request):
    return render(request, 'backoffice/report/membership_report/membership_subscription_report.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_comparative_analysis_report(request):
    return render(request, 'backoffice/report/membership_report/membership_comparative_analysis_report.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership EC Report'], login_url='/backofficeapp/login/', raise_exception=True)
def download_ec_report_count(request):
    try:
        print "reportapp | membership_report.py | download_ec_report_count "
        apply_from_date = datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y').date()
        apply_to_date = datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y').date()
        if apply_to_date < apply_from_date:
            data = {"success": "validate"}
        else:
            payment_list = PaymentDetails.objects.filter(
                userdetail__created_date__range=[apply_from_date, apply_to_date],
                membershipInvoice__invoice_for='NEW', is_deleted=False,
                amount_paid__gt=0, userdetail__member_associate_no__isnull=True).order_by(
                'userdetail__company__company_name')

            if payment_list:
                data = {"success": "true"}
            else:
                data = {"success": "no data"}
    except Exception, e:
        print "\nException In | membership_report.py | download_ec_report_count EXCE =", str(traceback.print_exc())
        data = {"success": "false"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def download_ec_report_file(request):
    try:
        print '\nRequest IN | membership_report.py | download_ec_report_file | User = ', request.user
        if request.GET.get('apply_from_date') and request.GET.get('apply_to_date'):
            apply_from_date = datetime.strptime(str(request.GET.get('apply_from_date')), '%d/%m/%Y').date()
            apply_to_date = (datetime.strptime(str(request.GET.get('apply_to_date')), '%d/%m/%Y')).date()
            payment_list = PaymentDetails.objects.filter(
                userdetail__created_date__range=[apply_from_date, apply_to_date],
                membershipInvoice__invoice_for='NEW', is_deleted=False,
                amount_paid__gt=0, userdetail__member_associate_no__isnull=True).order_by(
                'userdetail__company__company_name')
            output = io.BytesIO()
            workbook = Workbook(output, {'in_memory': True})
            worksheet1 = workbook.add_worksheet('Applicant_Detail')
            merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
            cell_header_format = workbook.add_format(
                {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})

            title_text = 'EC Report for New Membership Applicant Between ' + str(
                apply_from_date.strftime('%d/%m/%Y')) + ' to ' + str(apply_to_date.strftime('%d/%m/%Y'))
            worksheet1.merge_range('A1:P1', title_text, merge_format)

            column_name = ['Sr #', 'Name & Address', 'Activity', 'Name of Director', 'Year of Establishment',
                           'Annual T.O.(cr.)', 'Annual Subscription', 'Remark', 'Payment Method', 'Pro-rata',
                           'Entrance Fee',
                           'Tax', 'Total Paid', 'Membership No', 'Acceptance Date', 'Type', 'Number Of Employee']

            cell_format = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1})
            cell_format2 = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1})
            cell_format3 = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1})
            bold = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1, 'bold': True})

            cell_format.set_align('vcenter')
            cell_format2.set_align('vcenter')
            cell_format3.set_align('vcenter')
            cell_format3.set_align('center')
            cell_format2.set_rotation(90)

            worksheet1.set_column('A:A', 3)
            worksheet1.set_column('B:B', 24)
            worksheet1.set_column('C:C', 16)
            worksheet1.set_column('D:D', 18)
            worksheet1.set_column('E:E', 5)
            worksheet1.set_column('F:F', 5)
            worksheet1.set_column('G:G', 5)
            worksheet1.set_column('H:H', 5)

            for i in range(len(column_name)):
                if i in [4, 5, 6, 7]:
                    worksheet1.write_string(1, int(i), column_name[i], cell_header_format)
                else:
                    worksheet1.write_string(1, int(i), column_name[i], cell_header_format)

            i = 2
            j = 1
            for payment_obj in payment_list:
                print "----------------------------", payment_obj.userdetail.company.employee_range
                print "----------------------------", payment_obj.userdetail.company.total_employees
                worksheet1.write_string(i, 0, str(j), cell_format)
                # worksheet1.write_string(i, 1, str(payment_obj.userdetail.company.company_name) + '\n' + str(
                #     payment_obj.userdetail.correspond_address), cell_format)

                worksheet1.write_rich_string(i, 1, bold, str(payment_obj.userdetail.company.company_name), '\n',
                                             cell_format, str(payment_obj.userdetail.correspond_address), cell_format)

                worksheet1.write_string(i, 2, str(', '.join([industry_obj.description.strip() for industry_obj in
                                                             payment_obj.userdetail.company.industrydescription.all()])),
                                        cell_format)
                if payment_obj.userdetail.enroll_type == 'CO':
                    worksheet1.write_string(i, 3, str(payment_obj.userdetail.ceo_name) + '\n' + str(
                        payment_obj.userdetail.ceo_email) + '\n' + str(payment_obj.userdetail.ceo_cellno), cell_format)
                else:
                    worksheet1.write_string(i, 3, str(payment_obj.userdetail.company.company_name) + '\n' + str(
                        payment_obj.userdetail.ceo_email) + '\n' + str(payment_obj.userdetail.person_cellno),
                                            cell_format)
                worksheet1.write_string(i, 4, str(
                    payment_obj.userdetail.company.establish_year if payment_obj.userdetail.company.establish_year else ''),
                                        cell_format)
                worksheet1.write_string(i, 5, str(
                    payment_obj.userdetail.annual_turnover_rupees if payment_obj.userdetail.annual_turnover_rupees else ''),
                                        cell_format)
                worksheet1.write_string(i, 6, str(payment_obj.userdetail.membership_slab.annual_fee), cell_format)
                worksheet1.write_string(i, 7, '', cell_format)
                worksheet1.write_string(i, 8, str(payment_obj.user_Payment_Type), cell_format)
                worksheet1.write_string(i, 9, str(int(round(payment_obj.membershipInvoice.subscription_charges, 0))),
                                        cell_format)
                worksheet1.write_string(i, 10, str(int(round(payment_obj.membershipInvoice.entrance_fees, 0))),
                                        cell_format)
                worksheet1.write_string(i, 11, str(int(round(payment_obj.membershipInvoice.tax, 0))), cell_format)
                worksheet1.write_string(i, 12, str(int(round(payment_obj.amount_paid, 0))), cell_format)
                worksheet1.write_string(i, 13, str(
                    payment_obj.userdetail.member_associate_no if payment_obj.userdetail.member_associate_no else ''),
                                        cell_format)
                worksheet1.write_string(i, 14, str(
                    payment_obj.userdetail.membership_acceptance_date if payment_obj.userdetail.membership_acceptance_date else ''),
                                        cell_format)
                if payment_obj.userdetail.user_type == 'Life Membership':
                    worksheet1.write_string(i, 15, 'Life Member', cell_format)
                elif payment_obj.userdetail.user_type == 'Associate':
                    worksheet1.write_string(i, 15, 'Associate', cell_format)
                else:
                    worksheet1.write_string(i, 15, 'Member', cell_format)
                # worksheet1.write_string(i, 16, str(payment_obj.userdetail.company.total_employees)if payment_obj.userdetail.company.total_employees else '', cell_format)
                if payment_obj.userdetail.enroll_type == "CO":
                    if payment_obj.userdetail.company.employee_range or payment_obj.userdetail.company.employee_range == 0:
                        if payment_obj.userdetail.company.employee_range == 0:
                            worksheet1.write_string(i, 16, str("0-10"), cell_format)
                        elif payment_obj.userdetail.company.employee_range == 1:
                            worksheet1.write_string(i, 16, str("10-100"), cell_format)
                        elif payment_obj.userdetail.company.employee_range == 2:
                            worksheet1.write_string(i, 16, str("100-500"), cell_format)
                        elif payment_obj.userdetail.company.employee_range == 3:
                            worksheet1.write_string(i, 16, str("500-1000"), cell_format)
                        else:
                            worksheet1.write_string(i, 16, str("1000+"), cell_format)
                    else:
                        worksheet1.write_string(i, 16, str(payment_obj.userdetail.company.total_employees), cell_format)
                else:
                    worksheet1.write_string(i, 16, str("0"), cell_format)

                i = i + 1
                j = j + 1

            workbook.close()
            output.seek(0)

            response = HttpResponse(output.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename=New_Membership_Applicant.xlsx'
            print '\nResponse OUT | membership_report.py | download_ec_report_file | User = ', request.user
            return response
        else:
            return HttpResponse(status=400)
    except Exception, e:
        print '\nException IN | membership_report.py | download_ec_report_file | EXCP = ', str(traceback.print_exc())
        return False


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Account Report'], login_url='/backofficeapp/login/', raise_exception=True)
def account_report_file_count(request):
    try:
        print '\nRequest IN | membership_report.py | account_report_file_count | User = ', request.user

        invoice_list = []
        from_date = datetime.strptime(str(request.GET.get('date_range_from')), '%d/%m/%Y').date()
        to_date = datetime.strptime(str(request.GET.get('date_range_to')), '%d/%m/%Y').date()

        gst_obj = Servicetax.objects.get(tax_type=0)
        igst_obj = Servicetax.objects.get(tax_type=1)

        if to_date < from_date:
            data = {"success": "validate"}
        else:
            if request.GET.get('new_renew') == 'new':
                if request.GET.get('payment_method') == 'all':
                    invoice_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        userdetail__member_associate_no__isnull=False,
                        financial_year=request.GET.get('financial_year'),
                        amount_paid__gt=0, is_deleted=False).exclude(
                        userdetail__member_associate_no__exact='').order_by(
                        'userdetail__company__company_name').distinct().values('membershipInvoice_id')


                else:
                    invoice_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        userdetail__member_associate_no__isnull=False,
                        financial_year=request.GET.get('financial_year'),
                        user_Payment_Type=request.GET.get('payment_method'), amount_paid__gt=0,
                        is_deleted=False).exclude(
                        userdetail__member_associate_no__exact='').order_by(
                        'userdetail__company__company_name').distinct().values('membershipInvoice_id')
            else:
                if request.GET.get('payment_method') == 'all':
                    invoice_list = PaymentDetails.objects.filter(
                        payment_date__range=[from_date, to_date],
                        financial_year=request.GET.get('financial_year'),
                        userdetail__member_associate_no__isnull=False,
                        membershipInvoice__invoice_for__in=['RENEW', 'RE-ASSOCIATE'],
                        amount_paid__gt=0, is_deleted=False).exclude(
                        userdetail__member_associate_no__exact='').order_by(
                        'userdetail__company__company_name').distinct().values('membershipInvoice_id')
                else:
                    invoice_list = PaymentDetails.objects.filter(
                        payment_date__range=[from_date, to_date],
                        userdetail__member_associate_no__isnull=False,
                        financial_year=request.GET.get('financial_year'),
                        membershipInvoice__invoice_for__in=['RENEW', 'RE-ASSOCIATE'],
                        user_Payment_Type=request.GET.get('payment_method'), amount_paid__gt=0,
                        is_deleted=False).exclude(
                        userdetail__member_associate_no__exact='').order_by(
                        'userdetail__company__company_name').distinct().values('membershipInvoice_id')
            if invoice_list:
                data = {"success": "true"}
            else:
                data = {"success": "no data"}

    except Exception, e:
        print '\nException IN | membership_report.py | account_report_file_count | EXCP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Account Report'], login_url='/backofficeapp/login/', raise_exception=True)
def download_account_report_file(request):
    try:
        print '\nRequest IN | membership_report.py | download_account_report_file | User = ', request.user

        invoice_list = []
        from_date = datetime.strptime(str(request.GET.get('date_range_from')), '%d/%m/%Y').date()
        to_date = (datetime.strptime(str(request.GET.get('date_range_to')), '%d/%m/%Y')).date()
        report_type = request.GET.get('new_renew')
        gst_obj = Servicetax.objects.get(tax_type=0)
        igst_obj = Servicetax.objects.get(tax_type=1)

        if request.GET.get('new_renew') == 'new':
            if request.GET.get('payment_method') == 'all':
                invoice_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    userdetail__member_associate_no__isnull=False,
                    financial_year=request.GET.get('financial_year'),
                    amount_paid__gt=0, is_deleted=False).exclude(userdetail__member_associate_no__exact='').order_by(
                    'userdetail__company__company_name').distinct().values('membershipInvoice_id')
            else:
                invoice_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    userdetail__member_associate_no__isnull=False,
                    financial_year=request.GET.get('financial_year'),
                    user_Payment_Type=request.GET.get('payment_method'), amount_paid__gt=0, is_deleted=False).exclude(
                    userdetail__member_associate_no__exact='').order_by(
                    'userdetail__company__company_name').distinct().values('membershipInvoice_id')

        else:
            if request.GET.get('payment_method') == 'all':
                invoice_list = PaymentDetails.objects.filter(
                    payment_date__range=[from_date, to_date],
                    userdetail__member_associate_no__isnull=False,
                    financial_year=request.GET.get('financial_year'),
                    membershipInvoice__invoice_for__in=['RENEW', 'RE-ASSOCIATE'],
                    amount_paid__gt=0, is_deleted=False).exclude(userdetail__member_associate_no__exact='').order_by(
                    'userdetail__company__company_name').distinct().values('membershipInvoice_id')
                print '\nLen = ', len(invoice_list)
            else:
                invoice_list = PaymentDetails.objects.filter(
                    payment_date__range=[from_date, to_date],
                    userdetail__member_associate_no__isnull=False,
                    financial_year=request.GET.get('financial_year'),
                    membershipInvoice__invoice_for__in=['RENEW', 'RE-ASSOCIATE'],
                    user_Payment_Type=request.GET.get('payment_method'), amount_paid__gt=0, is_deleted=False).exclude(
                    userdetail__member_associate_no__exact='').order_by(
                    'userdetail__company__company_name').distinct().values('membershipInvoice_id')

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        workbook.formats[0].set_font_size(10)
        workbook.formats[0].set_border(1)
        workbook.formats[0].set_text_wrap()
        receipt_worksheet = workbook.add_worksheet('Receipt_Detail')
        invoice_worksheet = workbook.add_worksheet('Invoice_Detail')
        print_worksheet = workbook.add_worksheet('Print')

        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter',
             'border_color': '#000000'})
        if request.GET.get('payment_method') == 'all':
            title_text = ('New Member') + ' ' + 'Report Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
                to_date.strftime('%d/%m/%Y'))+ (' For FY ') + str(request.GET.get('financial_year')) if report_type == 'new' else ('Renewal') + ' ' + ' Report Between ' + str(
                from_date.strftime('%d/%m/%Y')) + ' to ' + str(to_date.strftime('%d/%m/%Y')) + (' For FY ') + str(request.GET.get('financial_year'))
        else:
            title_text = ('New Member') + ' ' + request.GET.get('payment_method') + ' Report Between ' + str(
                from_date.strftime('%d/%m/%Y')) + ' to ' + str(
                to_date.strftime('%d/%m/%Y')) + (' For FY ') + str(request.GET.get('financial_year')) if report_type == 'new' else ('Renewal') + ' ' + request.GET.get(
                'payment_method') + ' Report Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
                to_date.strftime('%d/%m/%Y')) + (' For FY ') + str(request.GET.get('financial_year'))
        # title_text = 'New Members Account Report Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to '+str(to_date.strftime('%d/%m/%Y'))if report_type == 'new' else 'Renew Members Account Report Between ' +str(from_date.strftime('%d/%m/%Y')) + ' to '+str(to_date.strftime('%d/%m/%Y'))
        receipt_worksheet.merge_range('A1:T1', title_text, merge_format)
        invoice_worksheet.merge_range('A1:AC1', title_text, merge_format)
        print_worksheet.merge_range('A1:J1', title_text, merge_format)

        receipt_column = ['DateIssued', 'Client', 'Cost Category for Client', 'Cost Centre for Client',
                          'Account Head', 'Amount', 'Narration', 'List of Transaction Type',
                          'Instrument Number', 'Instrument Date', 'Bank', 'Cash Receipt', 'Bank Receipt',
                          'CEO Email', 'Corresponding Email', 'Finance Email', 'GSTIN', 'Address', 'City', 'Pincode']
        invoice_column = ['DateIssued', 'Membership no', 'Debtor', 'State Name', 'Place of Supply',
                          'Income Account Head',
                          'Stock Item', 'Quantity', 'Rate', 'Basic Amount', 'Central Goods and Service Tax',
                          'State Goods and Service Tax', 'Integrated Goods and Service Tax', 'Total',
                          'Round off', 'Invoice Value', 'Narration', 'Cost Category for Income',
                          'Cost Centre for Income', 'Cost Category for Client', 'Cost Centre for Client',
                          'Sales', 'CEO Email', 'Corresponding Email', 'Finance Email', 'GSTIN', 'Address', 'City',
                          'Pincode']
        print_column = ['Sr No.', 'Membership no', 'Client', 'Total Payable', 'Paid Amount', 'TDS Amount',
                        'Payment Mode', 'Cheque Number', 'Cheque Date', 'Bank']

        for i in range(len(receipt_column)):
            receipt_worksheet.write_string(1, int(i), receipt_column[i], cell_header_format)

        for i in range(len(invoice_column)):
            invoice_worksheet.write_string(1, int(i), invoice_column[i], cell_header_format)

        cell_format = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1, 'border_color': '#000000'})
        cell_format2 = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1, 'border_color': '#000000'})
        cell_format.set_align('vcenter')
        cell_format2.set_align('vcenter')
        cell_format2.set_rotation(90)

        invoice_worksheet.set_column('A:A', 4)
        invoice_worksheet.set_column('B:B', 10)

        print_worksheet.set_column('A:A', 4)
        print_worksheet.set_column('B:B', 10)
        print_worksheet.set_column('C:C', 35)
        print_worksheet.set_column('D:D', 10)
        print_worksheet.set_column('E:E', 7)
        print_worksheet.set_column('F:F', 8)
        print_worksheet.set_column('G:G', 10)
        print_worksheet.set_column('H:H', 18)

        for i in range(len(print_column)):
            if i in []:
                print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)
            else:
                print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)

        i = 2
        j = 2
        k = 2
        for item in invoice_list:
            invoice_obj = MembershipInvoice.objects.get(id=item['membershipInvoice_id'])
            i = write_receipt_worksheet(request, invoice_obj, receipt_worksheet, from_date, to_date, i, cell_format)
            j = write_invoice_worksheet(request, invoice_obj, gst_obj, igst_obj, invoice_worksheet, from_date, to_date,
                                        j, cell_format)
            k = write_print_worksheet(request, invoice_obj, print_worksheet, from_date, to_date, k, cell_format)

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # response['Content-Disposition'] = 'attachment; filename=' + (str('Account_Receipt_For_Membership_' + datetime.today().date().strftime('%d_%m_%Y') + '.xlsx') if request.GET.get('select_type') == 'receipt' else str('Account_Invoice_For_Membership_' + datetime.today().date().strftime('%d_%m_%Y') + '.xlsx'))
        response[
            'Content-Disposition'] = 'attachment; filename=' + title_text + ' as on ' + datetime.today().date().strftime(
            '%d_%m_%Y') + '.xlsx'
        print '\nResponse OUT | membership_report.py | download_account_report_file | User = ', request.user
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | download_account_report_file | EXCP = ', str(
            traceback.print_exc())
        return False


def write_receipt_worksheet(request, invoice_obj, receipt_worksheet, from_date, to_date, i, cell_format):
    try:
        if request.GET.get('new_renew') == 'renew':
            payment_dict = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                         payment_date__range=[from_date, to_date],
                                                         amount_paid__gt=0, is_deleted=False).values(
                'user_Payment_Type', 'cheque_no').annotate(paid_amount=Sum('amount_paid'))
        else:
            payment_dict = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                         amount_paid__gt=0, is_deleted=False).values(
                'user_Payment_Type', 'cheque_no').annotate(paid_amount=Sum('amount_paid'))

        for payment_item in payment_dict:
            receipt_worksheet.write_string(i, 0, str(datetime.today().date().strftime('%d/%m/%Y')), cell_format)
            receipt_worksheet.write_string(i, 1, str(invoice_obj.userdetail.company.company_name), cell_format)
            receipt_worksheet.write_string(i, 2, str('Debtors'), cell_format)
            receipt_worksheet.write_string(i, 3, str('BILLS RECEIVABLE MEMBERSHIP'), cell_format)
            receipt_worksheet.write_string(i, 4, str(''), cell_format)
            receipt_worksheet.write_number(i, 5, int(payment_item['paid_amount']), cell_format)
            receipt_worksheet.write_string(i, 6, str('BEING AMT RECD TW   MEMBERSHIP FEE'), cell_format)
            if payment_item['user_Payment_Type'] == 'Cash':
                receipt_worksheet.write_string(i, 7, str('CASH'), cell_format)
            elif payment_item['user_Payment_Type'] == 'NEFT':
                receipt_worksheet.write_string(i, 7, str('NEFT'), cell_format)
            elif payment_item['user_Payment_Type'] == 'Online':
                receipt_worksheet.write_string(i, 7, str('ONLINE'), cell_format)
            else:
                receipt_worksheet.write_string(i, 7, str('CHEQUE'), cell_format)
            if payment_item['user_Payment_Type'] == 'Cheque':
                payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                            user_Payment_Type='Cheque',
                                                            cheque_no=payment_item['cheque_no'],
                                                            amount_paid__gt=0, is_deleted=False).last()
                receipt_worksheet.write_string(i, 8, str(payment_obj.cheque_no if payment_obj.cheque_no else ''),
                                               cell_format)
                receipt_worksheet.write_string(i, 9, str(
                    payment_obj.cheque_date.strftime('%d/%m/%Y') if payment_obj.cheque_date else ''), cell_format)
                receipt_worksheet.write_string(i, 10, str(payment_obj.bank_name if payment_obj.bank_name else ''),
                                               cell_format)
            else:
                receipt_worksheet.write_string(i, 8, str(''), cell_format)
                receipt_worksheet.write_string(i, 9, str(''), cell_format)
                receipt_worksheet.write_string(i, 10, str(''), cell_format)
            receipt_worksheet.write_string(i, 11, str(''), cell_format)
            receipt_worksheet.write_string(i, 12, str(''), cell_format)
            receipt_worksheet.write_string(i, 13,
                                           str(
                                               invoice_obj.userdetail.ceo_email if invoice_obj.userdetail.ceo_email else ''),
                                           cell_format)
            receipt_worksheet.write_string(i, 14, str(
                invoice_obj.userdetail.correspond_email if invoice_obj.userdetail.correspond_email else ''),
                                           cell_format)
            receipt_worksheet.write_string(i, 15, str(
                invoice_obj.userdetail.company.hoddetail.finance_email if invoice_obj.userdetail.company.hoddetail and invoice_obj.userdetail.company.hoddetail.finance_email else ''),
                                           cell_format)
            receipt_worksheet.write_string(i, 16, str(
                invoice_obj.userdetail.gst if invoice_obj.userdetail.gst and invoice_obj.userdetail.gst != 'NA' else ''),
                                           cell_format)
            receipt_worksheet.write_string(i, 17, str(invoice_obj.userdetail.correspond_address), cell_format)
            receipt_worksheet.write_string(i, 18, str(invoice_obj.userdetail.correspondcity.city_name), cell_format)
            receipt_worksheet.write_string(i, 19, str(invoice_obj.userdetail.correspond_pincode), cell_format)

            i = i + 1
        return i
    except Exception, e:
        print str(traceback.print_exc()), '\n', e


def write_invoice_worksheet(request, invoice_obj, gst_obj, igst_obj, invoice_worksheet, from_date, to_date, j,
                            cell_format):
    try:
        if request.GET.get('new_renew') == 'renew':
            payment_dict = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                         payment_date__range=[from_date, to_date],
                                                         amount_paid__gt=0, is_deleted=False).aggregate(
                paid_amount=Sum('amount_paid'))
        else:
            payment_dict = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                         amount_paid__gt=0, is_deleted=False).aggregate(
                paid_amount=Sum('amount_paid'))
        payable_amount = invoice_obj.amount_payable
        paid_amount = payment_dict['paid_amount']
        current_fy = str(invoice_obj.financial_year[2:4]) + '-' + str(invoice_obj.financial_year[7:9])

        if invoice_obj.invoice_for == 'NEW' and invoice_obj.entrance_fees > 0:
            invoice_worksheet.write_string(j, 0, str(datetime.today().date().strftime('%d/%m/%Y')), cell_format)
            invoice_worksheet.write_string(j, 1, str(invoice_obj.userdetail.member_associate_no).strip(), cell_format)
            invoice_worksheet.write_string(j, 2, str(invoice_obj.userdetail.company.company_name), cell_format)
            if invoice_obj.userdetail.correspondstate and invoice_obj.userdetail.correspondstate.state_name == 'Maharashtra':
                invoice_worksheet.write_string(j, 3, 'Maharashtra, Code:27', cell_format)
            else:
                invoice_worksheet.write_string(j, 3, str(
                    invoice_obj.userdetail.correspondstate.state_name if invoice_obj.userdetail.correspondstate else ''),
                                               cell_format)
            invoice_worksheet.write_string(j, 4, str(
                invoice_obj.userdetail.correspondstate.state_name if invoice_obj.userdetail.correspondstate else ''),
                                           cell_format)

            invoice_worksheet.write_string(j, 5, 'ONE TIME ENTRANCE FEES', cell_format)
            invoice_worksheet.write_string(j, 6, '', cell_format)
            invoice_worksheet.write_string(j, 7, '', cell_format)
            invoice_worksheet.write_string(j, 8, '', cell_format)
            invoice_worksheet.write_string(j, 9, str(invoice_obj.entrance_fees), cell_format)
            cgst_amount = invoice_obj.entrance_fees * Decimal(gst_obj.cgst) / 100
            sgst_amount = invoice_obj.entrance_fees * Decimal(gst_obj.sgst) / 100
            total_amount = invoice_obj.entrance_fees + cgst_amount + sgst_amount
            cgst_amount = '%.2f' % cgst_amount
            sgst_amount = '%.2f' % sgst_amount
            total_amount = '%.2f' % total_amount
            invoice_worksheet.write_string(j, 10, str(cgst_amount), cell_format)
            invoice_worksheet.write_string(j, 11, str(sgst_amount), cell_format)
            if invoice_obj.userdetail.correspondstate and invoice_obj.userdetail.correspondstate.state_name != 'Maharashtra':
                igst_amount = invoice_obj.entrance_fees * Decimal(igst_obj.tax) / 100
                igst_amount = '%.2f' % igst_amount
                invoice_worksheet.write_string(j, 10, '', cell_format)
                invoice_worksheet.write_string(j, 11, '', cell_format)
                invoice_worksheet.write_string(j, 12, str(igst_amount), cell_format)
            else:
                invoice_worksheet.write_string(j, 10, str(cgst_amount), cell_format)
                invoice_worksheet.write_string(j, 11, str(sgst_amount), cell_format)
                invoice_worksheet.write_string(j, 12, '', cell_format)
            invoice_worksheet.write_string(j, 13, str(total_amount), cell_format)
            number_dec = float(str(float(total_amount) - int(float(total_amount)))[1:])
            invoice_worksheet.write_string(j, 14, str(number_dec if number_dec > 0 else ''), cell_format)
            invoice_worksheet.write_string(j, 15, str(total_amount), cell_format)
            invoice_worksheet.write_string(j, 16, 'BILL RAISED TOWARDS MEMBERSHIP  FEE', cell_format)
            invoice_worksheet.write_string(j, 17, '', cell_format)
            invoice_worksheet.write_string(j, 18, '', cell_format)
            invoice_worksheet.write_string(j, 19, 'Debtors', cell_format)
            invoice_worksheet.write_string(j, 20, 'BILLS RECEIVABLE MEMBERSHIP', cell_format)
            invoice_worksheet.write_string(j, 21, '', cell_format)
            invoice_worksheet.write_string(j, 22,
                                           str(
                                               invoice_obj.userdetail.ceo_email if invoice_obj.userdetail.ceo_email else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 23, str(
                invoice_obj.userdetail.correspond_email if invoice_obj.userdetail.correspond_email else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 24, str(
                invoice_obj.userdetail.company.hoddetail.finance_email if invoice_obj.userdetail.company.hoddetail and invoice_obj.userdetail.company.hoddetail.finance_email else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 25, str(
                invoice_obj.userdetail.gst if invoice_obj.userdetail.gst and invoice_obj.userdetail.gst != 'NA' else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 26, str(invoice_obj.userdetail.correspond_address), cell_format)
            invoice_worksheet.write_string(j, 27, str(invoice_obj.userdetail.correspondcity.city_name), cell_format)
            invoice_worksheet.write_string(j, 28, str(invoice_obj.userdetail.correspond_pincode), cell_format)
            j = j + 1

        while paid_amount != Decimal(0):
            if paid_amount > payable_amount:
                paid_amount = paid_amount - payable_amount
                amount = payable_amount
            elif paid_amount == payable_amount:
                paid_amount = paid_amount - payable_amount
                amount = payable_amount
            else:
                amount = paid_amount
                paid_amount = Decimal(0)

            invoice_worksheet.write_string(j, 0, str(datetime.today().date().strftime('%d/%m/%Y')), cell_format)
            invoice_worksheet.write_string(j, 1, str(invoice_obj.userdetail.member_associate_no).strip(), cell_format)
            invoice_worksheet.write_string(j, 2, str(invoice_obj.userdetail.company.company_name), cell_format)
            if invoice_obj.userdetail.correspondstate and invoice_obj.userdetail.correspondstate.state_name == 'Maharashtra':
                invoice_worksheet.write_string(j, 3, 'Maharashtra, Code:27', cell_format)
            else:
                invoice_worksheet.write_string(j, 3, str(
                    invoice_obj.userdetail.correspondstate.state_name if invoice_obj.userdetail.correspondstate else ''),
                                               cell_format)
            invoice_worksheet.write_string(j, 4, str(
                invoice_obj.userdetail.correspondstate.state_name if invoice_obj.userdetail.correspondstate else ''),
                                           cell_format)

            if invoice_obj.userdetail.user_type == 'Life Membership':
                invoice_worksheet.write_string(j, 5, 'LIFE MEMBERSHIP FEES', cell_format)
            else:
                invoice_worksheet.write_string(j, 5, str(current_fy) + ' MEMBERSHIP FEES', cell_format)
            invoice_worksheet.write_string(j, 6, '', cell_format)
            invoice_worksheet.write_string(j, 7, '', cell_format)
            invoice_worksheet.write_string(j, 8, '', cell_format)

            if invoice_obj.amount_payable == amount:
                invoice_worksheet.write_string(j, 9, str(invoice_obj.subscription_charges), cell_format)
                cgst_amount = invoice_obj.subscription_charges * Decimal(gst_obj.cgst) / 100
                sgst_amount = invoice_obj.subscription_charges * Decimal(gst_obj.sgst) / 100
                total_amount = invoice_obj.subscription_charges + cgst_amount + sgst_amount
                cgst_amount = '%.2f' % cgst_amount
                sgst_amount = '%.2f' % sgst_amount
                total_amount = '%.2f' % total_amount
                if invoice_obj.userdetail.correspondstate and invoice_obj.userdetail.correspondstate.state_name != 'Maharashtra':
                    igst_amount = invoice_obj.subscription_charges * Decimal(igst_obj.tax) / 100
                    igst_amount = '%.2f' % igst_amount
                    invoice_worksheet.write_string(j, 10, '', cell_format)
                    invoice_worksheet.write_string(j, 11, '', cell_format)
                    invoice_worksheet.write_string(j, 12, str(igst_amount), cell_format)
                else:
                    invoice_worksheet.write_string(j, 10, str(cgst_amount), cell_format)
                    invoice_worksheet.write_string(j, 11, str(sgst_amount), cell_format)
                    invoice_worksheet.write_string(j, 12, '', cell_format)
                invoice_worksheet.write_string(j, 13, str(total_amount), cell_format)
                number_dec = float(str(float(total_amount) - int(float(total_amount)))[1:])
                invoice_worksheet.write_string(j, 14, str(number_dec if number_dec > 0 else ''), cell_format)
                invoice_worksheet.write_string(j, 15, str(invoice_obj.amount_payable), cell_format)
            else:
                before_gst_amount = amount / (1 + Decimal(gst_obj.tax) / Decimal(100.0))
                invoice_worksheet.write_string(j, 9, str(before_gst_amount), cell_format)
                cgst_amount = before_gst_amount * Decimal(gst_obj.cgst) / 100
                sgst_amount = before_gst_amount * Decimal(gst_obj.sgst) / 100
                total_amount = before_gst_amount + cgst_amount + sgst_amount
                cgst_amount = '%.2f' % cgst_amount
                sgst_amount = '%.2f' % sgst_amount
                total_amount = '%.2f' % total_amount
                if invoice_obj.userdetail.correspondstate and invoice_obj.userdetail.correspondstate.state_name != 'Maharashtra':
                    igst_amount = before_gst_amount * Decimal(igst_obj.tax) / 100
                    igst_amount = '%.2f' % igst_amount
                    invoice_worksheet.write_string(j, 10, '', cell_format)
                    invoice_worksheet.write_string(j, 11, '', cell_format)
                    invoice_worksheet.write_string(j, 12, str(igst_amount), cell_format)
                else:
                    invoice_worksheet.write_string(j, 10, str(cgst_amount), cell_format)
                    invoice_worksheet.write_string(j, 11, str(sgst_amount), cell_format)
                    invoice_worksheet.write_string(j, 12, '', cell_format)
                invoice_worksheet.write_string(j, 13, str(total_amount), cell_format)
                number_dec = float(str(float(total_amount) - int(float(total_amount)))[1:])
                invoice_worksheet.write_string(j, 14, str(number_dec if number_dec > 0 else ''), cell_format)
                invoice_worksheet.write_string(j, 15, str(total_amount), cell_format)
            invoice_worksheet.write_string(j, 16, 'BILL RAISED TOWARDS MEMBERSHIP  FEE', cell_format)
            invoice_worksheet.write_string(j, 17, '', cell_format)
            invoice_worksheet.write_string(j, 18, '', cell_format)
            invoice_worksheet.write_string(j, 19, 'Debtors', cell_format)
            invoice_worksheet.write_string(j, 20, 'BILLS RECEIVABLE MEMBERSHIP', cell_format)
            invoice_worksheet.write_string(j, 21, '', cell_format)
            invoice_worksheet.write_string(j, 22,
                                           str(
                                               invoice_obj.userdetail.ceo_email if invoice_obj.userdetail.ceo_email else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 23, str(
                invoice_obj.userdetail.correspond_email if invoice_obj.userdetail.correspond_email else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 24, str(
                invoice_obj.userdetail.company.hoddetail.finance_email if invoice_obj.userdetail.company.hoddetail and invoice_obj.userdetail.company.hoddetail.finance_email else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 25, str(
                invoice_obj.userdetail.gst if invoice_obj.userdetail.gst and invoice_obj.userdetail.gst != 'NA' else ''),
                                           cell_format)
            invoice_worksheet.write_string(j, 26, str(invoice_obj.userdetail.correspond_address), cell_format)
            invoice_worksheet.write_string(j, 27, str(invoice_obj.userdetail.correspondcity.city_name), cell_format)
            invoice_worksheet.write_string(j, 28, str(invoice_obj.userdetail.correspond_pincode), cell_format)

            current_fy_split = current_fy.split('-')
            current_fy = str(int(current_fy_split[0]) + 1) + '-' + str(int(current_fy_split[1]) + 1)
            j = j + 1
        return j
    except Exception, e:
        print str(traceback.print_exc()), '\n', e


def write_print_worksheet(request, invoice_obj, print_worksheet, from_date, to_date, k, cell_format):
    try:
        m = 1
        if request.GET.get('new_renew') == 'renew':
            payment_dict = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                         payment_date__range=[from_date, to_date],
                                                         amount_paid__gt=0, is_deleted=False).values(
                'user_Payment_Type',
                'cheque_no', 'cheque_date', 'bank_name', 'amount_payable', 'tds_amount').annotate(
                paid_amount=Sum('amount_paid'))
        else:
            payment_dict = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                         amount_paid__gt=0, is_deleted=False).values(
                'user_Payment_Type',
                'cheque_no', 'cheque_date', 'bank_name', 'amount_payable', 'tds_amount').annotate(
                paid_amount=Sum('amount_paid'))

        for payment_item in payment_dict:
            print_worksheet.write_number(k, 0, int(k - 1), cell_format)
            print_worksheet.write_string(k, 1, str(invoice_obj.userdetail.member_associate_no), cell_format)
            print_worksheet.write_string(k, 2, str(invoice_obj.userdetail.company.company_name), cell_format)
            print_worksheet.write_number(k, 3, int(payment_item['amount_payable']), cell_format)
            print_worksheet.write_number(k, 4, int(payment_item['paid_amount']), cell_format)
            print_worksheet.write_number(k, 5, int(payment_item['tds_amount']), cell_format)
            if payment_item['user_Payment_Type'] == 'Cash':
                print_worksheet.write_string(k, 6, 'CASH', cell_format)
            elif payment_item['user_Payment_Type'] == 'NEFT':
                print_worksheet.write_string(k, 6, 'NEFT', cell_format)
            elif payment_item['user_Payment_Type'] == 'Online':
                print_worksheet.write_string(k, 6, 'ONLINE', cell_format)
            else:
                print_worksheet.write_string(k, 6, 'CHEQUE', cell_format)
            if payment_item['user_Payment_Type'] == 'Cheque':
                print_worksheet.write_string(k, 7, str(payment_item['cheque_no'] if payment_item['cheque_no'] else ''),
                                             cell_format)
                print_worksheet.write_string(k, 8, str(
                    payment_item['cheque_date'].strftime('%d/%m/%Y') if payment_item['cheque_date'] else ''),
                                             cell_format)
                print_worksheet.write_string(k, 9, str(payment_item['bank_name'] if payment_item['bank_name'] else ''),
                                             cell_format)
            else:
                print_worksheet.write_string(k, 7, '', cell_format)
                print_worksheet.write_string(k, 8, '', cell_format)
                print_worksheet.write_string(k, 9, '', cell_format)
            k = k + 1
        return k
    except Exception, e:
        print str(traceback.print_exc()), '\n', e


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Data Download'], login_url='/backofficeapp/login/', raise_exception=True)
def membership_data_download(request):
    try:
        print '\nRequest IN | membership_report.py | membership_data_download | User = ', request.user
        members_obj_list = UserDetail.objects.filter(payment_method='Confirmed').order_by('company__company_name')
        today = datetime.today()
        end_date = datetime.strptime('31/03/' + str(today.year), '%d/%m/%Y')
        current_fy = ''
        company_scale_dict = {'MR': 'MICRO', 'SM': 'SMALL', 'MD': 'MEDIUM', 'LR': 'LARGE'}

        if today <= end_date:
            current_fy = str(int(today.year) - 1) + '-' + str(today.year)
        else:
            current_fy = str(today.year) + '-' + str(int(today.year) + 1)

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Members_Detail')
        workbook.formats[0].set_font_size(10)
        workbook.formats[0].set_border(1)
        workbook.formats[0].set_text_wrap()
        cell_format = workbook.add_format({'font_color': 'green', 'font_size': 10, 'border': 1, 'text_wrap': True})
        cell_format2 = workbook.add_format({'font_color': 'red', 'font_size': 10, 'border': 1, 'text_wrap': True})

        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        worksheet1.set_column('A:A', 5)
        worksheet1.set_column('B:B', 5)
        worksheet1.set_column('C:C', 13)
        worksheet1.set_column('D:D', 27)
        worksheet1.set_column('E:E', 19)
        worksheet1.set_column('F:F', 24)
        worksheet1.set_column('G:G', 10)
        worksheet1.set_column('H:H', 5)
        worksheet1.set_column('I:I', 9)
        worksheet1.set_column('J:J', 12)
        worksheet1.set_column('K:K', 24)
        worksheet1.set_column('S:S', 17)
        title_text = 'Membership Details Report'
        worksheet1.merge_range('A1:T1', title_text, merge_format)

        column_name = ['SUB.CAT', 'STATUS', 'M_NO', 'NAME', 'CEO', 'CEO_EMAIL', 'ADDRESS', 'CITY',
                       'PIN', 'TEL', 'CORRESPOND_EMAIL', 'WEBSITE', 'YEAR_OF_ESTABLISHMENT', 'SCALE', 'ACP_DATE',
                       'FINANCIAL_YEAR', 'AMOUNT_PAYABLE', 'AMOUNT_PAID', 'INDUSTRY', 'BUSINESS_DESCRIPTION']

        for i in range(len(column_name)):
            worksheet1.write_string(1, int(i), column_name[i], cell_header_format)

        i = 2
        j = 1
        for member_obj in members_obj_list:
            try:
                invoice_obj = MembershipInvoice.objects.get(userdetail=member_obj,
                                                            financial_year=current_fy, is_deleted=False)
            except Exception, e:
                invoice_obj = None
                invoice_obj_list = MembershipInvoice.objects.filter(userdetail=member_obj,
                                                                    financial_year=current_fy, is_deleted=False)
                for invoice_obj_item in invoice_obj_list:
                    if invoice_obj_item.is_paid:
                        invoice_obj = invoice_obj_item

            payment_detail = PaymentDetails.objects.filter(userdetail=member_obj, financial_year=current_fy,
                                                           payment_date__isnull=False, is_deleted=False).values(
                'amount_paid', 'amount_due').aggregate(received_amount=Sum('amount_paid'),
                                                       due_amount=Sum('amount_due'))

            if invoice_obj and invoice_obj.membership_slab:
                worksheet1.write_string(i, 0, str(int(float(invoice_obj.membership_slab.annual_fee))))
            elif member_obj and member_obj.membership_slab:
                worksheet1.write_string(i, 0, str(int(float(member_obj.membership_slab.annual_fee))))
            else:
                worksheet1.write_string(i, 0, str(0))

            if invoice_obj and invoice_obj.is_paid:
                worksheet1.write_string(i, 1, 'PAID', cell_format)
            else:
                worksheet1.write_string(i, 1, 'DUES', cell_format2)
            worksheet1.write_string(i, 2, str(member_obj.member_associate_no))
            worksheet1.write_string(i, 3, str(member_obj.company.company_name))
            worksheet1.write_string(i, 4, str(
                member_obj.ceo_name if member_obj.enroll_type == 'CO' else member_obj.company.company_name))
            worksheet1.write_string(i, 5, str(member_obj.ceo_email))
            worksheet1.write_string(i, 6, str(member_obj.correspond_address))
            worksheet1.write_string(i, 7, str(member_obj.correspondcity.city_name if member_obj.correspondcity else ''))
            worksheet1.write_string(i, 8, str(member_obj.correspond_pincode if member_obj.correspond_pincode else ''))
            worksheet1.write_string(i, 9, str(member_obj.correspond_std1 if member_obj.correspond_std1 else '') + str(
                member_obj.correspond_landline1 if member_obj.correspond_landline1 else ''))
            worksheet1.write_string(i, 10, str(member_obj.correspond_email if member_obj.correspond_email else ''))
            worksheet1.write_string(i, 11, str(member_obj.website if member_obj.website else ''))
            worksheet1.write_string(i, 12,
                                    str(member_obj.company.establish_year if member_obj.company.establish_year else ''))
            worksheet1.write_string(i, 13, str(company_scale_dict[str(member_obj.company.company_scale).strip()]))
            worksheet1.write_string(i, 14, str(member_obj.membership_acceptance_date.strftime(
                '%d/%m/%Y') if member_obj.membership_acceptance_date else ''))
            worksheet1.write_string(i, 15, str(member_obj.membership_year))
            worksheet1.write_string(i, 16, str(invoice_obj.amount_payable if invoice_obj else ''))
            worksheet1.write_string(i, 17,
                                    str(payment_detail['received_amount']) if payment_detail['received_amount'] and
                                                                              payment_detail[
                                                                                  'received_amount'] != 'None' else '')
            worksheet1.write_string(i, 18, str(
                ','.join([industry_obj.description for industry_obj in member_obj.company.industrydescription.all()])))
            worksheet1.write_string(i, 19, str(
                member_obj.company.description_of_business if member_obj.company.description_of_business else ''))

            i = i + 1
            j = j + 1

        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Members_Data_' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | membership_data_download | User = ', request.user
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | membership_data_download | EXCP = ', str(traceback.print_exc())

        return False


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Data Download'], login_url='/backofficeapp/login/', raise_exception=True)
def download_members_data(request):
    try:
        print '\nRequest IN | membership_report.py | membership_data_download | User = ', request.user
        members_obj_list = UserDetail.objects.filter(payment_method='Confirmed').order_by('company__company_name')
        today = datetime.today()
        end_date = datetime.strptime('31/03/' + str(today.year), '%d/%m/%Y')
        current_fy = ''
        company_scale_dict = {'MR': 'MICRO', 'SM': 'SMALL', 'MD': 'MEDIUM', 'LR': 'LARGE'}

        if today <= end_date:
            current_fy = str(int(today.year) - 1) + '-' + str(today.year)
        else:
            current_fy = str(today.year) + '-' + str(int(today.year) + 1)

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Members_Detail_Data')
        workbook.formats[0].set_font_size(10)
        workbook.formats[0].set_border(1)
        workbook.formats[0].set_text_wrap()
        cell_format = workbook.add_format(
            {'font_color': 'green', 'font_size': 10, 'border': 1, 'text_wrap': True, 'border_color': '#000000'})
        cell_format2 = workbook.add_format(
            {'font_color': 'red', 'font_size': 10, 'border': 1, 'text_wrap': True, 'border_color': '#000000'})

        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        worksheet1.set_column('A:A', 5)
        worksheet1.set_column('B:B', 5)
        worksheet1.set_column('C:C', 13)
        worksheet1.set_column('D:D', 10)
        worksheet1.set_column('E:E', 19)
        worksheet1.set_column('F:F', 24)
        worksheet1.set_column('G:G', 10)
        worksheet1.set_column('H:H', 12)
        worksheet1.set_column('I:I', 12)
        worksheet1.set_column('J:J', 12)
        worksheet1.set_column('K:K', 15)
        worksheet1.set_column('S:S', 13)
        worksheet1.set_column('T:T', 17)
        worksheet1.set_column('AL:AL', 15)
        worksheet1.set_column('AN:AN', 15)
        worksheet1.set_column('AM:AM', 20)
        title_text = 'Membership Details Data Report'
        worksheet1.merge_range('A1:BO1', title_text, merge_format)

        column_name = ['Sr.No.', 'Sub.Cat', 'Status', 'Membership No.', 'Company Name', 'CEO Name', 'CEO Contact',
                       'CEO Email', 'POC Name', 'POC Contact', 'POC Email', 'Address', 'State',
                       'City', 'Pincode', 'Contact', 'Email', 'Website', 'PAN', 'Aadhar', 'GST IN', 'Mem Category',
                       'Turnover',
                       'Establish Year', 'Inv Plant', 'Inv Land', 'Total Inv', 'Export', 'Import', 'ISO Details',
                       'EOU Details', 'Scale', 'Acceptance Date', 'Memb. Year', 'Total Payable', 'Total Paid',
                       'Total Empolyee', 'Industry', 'Business Description', 'Legal Status', 'HR Name', 'HR Contact',
                       'HR Email',
                       'Finance Name', 'Finance Contact', 'Finance Email', 'Marketing Name', 'Marketing Contact',
                       'Marketing Email', 'IT Name', 'IT Contact', 'IT Email', 'Corp_Rel Name', 'Corp_Rel Contact',
                       'Corp_Rel Email',
                       'Tech Name', 'Tech Contact', 'Tech Email', 'R & D Name', 'R & D Contact', 'R & D Email',
                       'Exim Name', 'Exim Contact', 'Exim Email']

        for i in range(len(column_name)):
            worksheet1.write_string(1, int(i), column_name[i], cell_header_format)

        i = 2
        j = 1
        k = 1
        for member_obj in members_obj_list:
            try:
                invoice_obj = MembershipInvoice.objects.get(userdetail=member_obj,
                                                            financial_year=current_fy, is_deleted=False)
            except Exception, e:
                invoice_obj = None
                invoice_obj_list = MembershipInvoice.objects.filter(userdetail=member_obj,
                                                                    financial_year=current_fy, is_deleted=False)
                for invoice_obj_item in invoice_obj_list:
                    if invoice_obj_item.is_paid:
                        invoice_obj = invoice_obj_item

            payment_detail = PaymentDetails.objects.filter(userdetail=member_obj, financial_year=current_fy,
                                                           payment_date__isnull=False, is_deleted=False).values(
                'amount_paid', 'amount_due').aggregate(received_amount=Sum('amount_paid'),
                                                       due_amount=Sum('amount_due'))

            worksheet1.write_number(i, 0, k)
            if invoice_obj and invoice_obj.membership_slab:
                worksheet1.write_string(i, 1, str(int(float(invoice_obj.membership_slab.annual_fee))))
            elif member_obj and member_obj.membership_slab:
                worksheet1.write_string(i, 1, str(int(float(member_obj.membership_slab.annual_fee))))
            else:
                worksheet1.write_string(i, 1, str(0))

            if invoice_obj and invoice_obj.is_paid:
                worksheet1.write_string(i, 2, 'PAID', cell_format)
            else:
                worksheet1.write_string(i, 2, 'DUES', cell_format2)
            worksheet1.write_string(i, 3, str(member_obj.member_associate_no))
            worksheet1.write_string(i, 4, str(member_obj.company.company_name))
            worksheet1.write_string(i, 5, str(
                member_obj.ceo_name if member_obj.enroll_type == 'CO' else member_obj.company.company_name))
            worksheet1.write_string(i, 6, str(member_obj.ceo_cellno) if member_obj.ceo_cellno else '')
            worksheet1.write_string(i, 7, str(member_obj.ceo_email) if member_obj.ceo_email else '')
            if member_obj.company.hoddetail:
                worksheet1.write_string(i, 8, str(member_obj.poc_name) if member_obj.poc_name else '')
                worksheet1.write_string(i, 9, str(member_obj.poc_contact) if member_obj.poc_contact else '')
                worksheet1.write_string(i, 10, str(member_obj.poc_email) if member_obj.poc_email else '')
            worksheet1.write_string(i, 11, str(member_obj.correspond_address))
            if member_obj.correspondstate:
                worksheet1.write_string(i, 12, str(
                    member_obj.correspondstate.state_name) if member_obj.correspondstate.state_name else '')
                worksheet1.write_string(i, 13,
                                        str(member_obj.correspondcity.city_name if member_obj.correspondcity else ''))
            worksheet1.write_string(i, 14, str(member_obj.correspond_pincode if member_obj.correspond_pincode else ''))
            worksheet1.write_string(i, 15, str(member_obj.correspond_std1 if member_obj.correspond_std1 else '') + str(
                member_obj.correspond_landline1 if member_obj.correspond_landline1 else ''))
            worksheet1.write_string(i, 16, str(member_obj.correspond_email if member_obj.correspond_email else ''))
            worksheet1.write_string(i, 17, str(member_obj.website if member_obj.website else ''))
            worksheet1.write_string(i, 18, str(member_obj.pan if member_obj.pan else ''))
            worksheet1.write_string(i, 19, str(member_obj.aadhar if member_obj.aadhar else ''))
            worksheet1.write_string(i, 20, str(member_obj.gst if member_obj.gst else 'NA'))
            worksheet1.write_string(i, 21,
                                    str(member_obj.membership_category if member_obj.membership_category else ''))
            worksheet1.write_string(i, 22,
                                    str(member_obj.annual_turnover_rupees if member_obj.annual_turnover_rupees else ''))
            worksheet1.write_string(i, 23,
                                    str(member_obj.company.establish_year if member_obj.company.establish_year else ''))
            worksheet1.write_string(i, 24, str(
                member_obj.company.block_inv_plant if member_obj.company.block_inv_plant else ''))
            worksheet1.write_string(i, 25,
                                    str(member_obj.company.block_inv_land if member_obj.company.block_inv_land else ''))
            worksheet1.write_string(i, 26, str(
                member_obj.company.block_inv_total if member_obj.company.block_inv_total else ''))
            worksheet1.write_string(i, 27, str(member_obj.company.textexport if member_obj.company.textexport else ''))
            worksheet1.write_string(i, 28, str(member_obj.company.textimport if member_obj.company.textimport else ''))
            worksheet1.write_string(i, 29, str(member_obj.company.iso_detail if member_obj.company.iso_detail else ''))
            worksheet1.write_string(i, 30, str(member_obj.company.eou_detail if member_obj.company.eou_detail else ''))
            worksheet1.write_string(i, 31, str(company_scale_dict[str(member_obj.company.company_scale).strip()]))
            worksheet1.write_string(i, 32, str(member_obj.membership_acceptance_date.strftime(
                '%d/%m/%Y') if member_obj.membership_acceptance_date else ''))
            worksheet1.write_string(i, 33, str(member_obj.membership_year))
            worksheet1.write_string(i, 34, str(invoice_obj.amount_payable if invoice_obj else ''))
            worksheet1.write_string(i, 35,
                                    str(payment_detail['received_amount']) if payment_detail['received_amount'] and
                                                                              payment_detail[
                                                                                  'received_amount'] != 'None' else '')

            # worksheet1.write_string(i, 36, str(member_obj.company.total_employees if member_obj.company.total_employees else ''))
            if member_obj.enroll_type == "CO":
                if member_obj.company.employee_range or member_obj.company.employee_range == 0:
                    if member_obj.company.employee_range == 0:
                        worksheet1.write_string(i, 36, str("0-10"), cell_format)
                    elif member_obj.company.employee_range == 1:
                        worksheet1.write_string(i, 36, str("10-100"), cell_format)
                    elif member_obj.company.employee_range == 2:
                        worksheet1.write_string(i, 36, str("100-500"), cell_format)
                    elif member_obj.company.employee_range == 3:
                        worksheet1.write_string(i, 36, str("500-1000"), cell_format)
                    elif member_obj.company.employee_range == 4:
                        worksheet1.write_string(i, 36, str("1000+"), cell_format)
                    else:
                        worksheet1.write_string(i, 36, str("0-10"), cell_format)
                else:
                    worksheet1.write_string(i, 36, str(member_obj.company.total_employees), cell_format)
            else:
                worksheet1.write_string(i, 36, str("0"), cell_format)

            worksheet1.write_string(i, 37, str(
                ','.join([industry_obj.description for industry_obj in member_obj.company.industrydescription.all()])))
            worksheet1.write_string(i, 38, str(
                member_obj.company.description_of_business if member_obj.company.description_of_business else ''))
            if member_obj.company.legalstatus:
                worksheet1.write_string(i, 39, str(
                    member_obj.company.legalstatus.description if member_obj.company.legalstatus.description else ''))
            if member_obj.company.hoddetail:
                worksheet1.write_string(i, 40, str(
                    member_obj.company.hoddetail.hr_name if member_obj.company.hoddetail.hr_name else ''))
                worksheet1.write_string(i, 41, str(
                    member_obj.company.hoddetail.hr_contact if member_obj.company.hoddetail.hr_contact else ''))
                worksheet1.write_string(i, 42, str(
                    member_obj.company.hoddetail.hr_email if member_obj.company.hoddetail.hr_email else ''))
                worksheet1.write_string(i, 43, str(
                    member_obj.company.hoddetail.finance_name if member_obj.company.hoddetail.finance_name else ''))
                worksheet1.write_string(i, 44, str(
                    member_obj.company.hoddetail.finance_contact if member_obj.company.hoddetail.finance_contact else ''))
                worksheet1.write_string(i, 45, str(
                    member_obj.company.hoddetail.finance_email if member_obj.company.hoddetail.finance_email else ''))

                worksheet1.write_string(i, 46, str(
                    member_obj.company.hoddetail.marketing_name if member_obj.company.hoddetail.marketing_name else ''))
                worksheet1.write_string(i, 47, str(
                    member_obj.company.hoddetail.marketing_contact if member_obj.company.hoddetail.marketing_contact else ''))
                worksheet1.write_string(i, 48, str(
                    member_obj.company.hoddetail.marketing_email if member_obj.company.hoddetail.marketing_email else ''))

                worksheet1.write_string(i, 49, str(
                    member_obj.company.hoddetail.IT_name if member_obj.company.hoddetail.IT_name else ''))
                worksheet1.write_string(i, 50, str(
                    member_obj.company.hoddetail.IT_contact if member_obj.company.hoddetail.IT_contact else ''))
                worksheet1.write_string(i, 51, str(
                    member_obj.company.hoddetail.IT_email if member_obj.company.hoddetail.IT_email else ''))

                worksheet1.write_string(i, 52, str(
                    member_obj.company.hoddetail.corp_rel_name if member_obj.company.hoddetail.corp_rel_name else ''))
                worksheet1.write_string(i, 53, str(
                    member_obj.company.hoddetail.corp_rel_contact if member_obj.company.hoddetail.corp_rel_contact else ''))
                worksheet1.write_string(i, 54, str(
                    member_obj.company.hoddetail.corp_rel_email if member_obj.company.hoddetail.corp_rel_email else ''))

                worksheet1.write_string(i, 55, str(
                    member_obj.company.hoddetail.tech_name if member_obj.company.hoddetail.tech_name else ''))
                worksheet1.write_string(i, 56, str(
                    member_obj.company.hoddetail.tech_contact if member_obj.company.hoddetail.tech_contact else ''))
                worksheet1.write_string(i, 57, str(
                    member_obj.company.hoddetail.tech_email if member_obj.company.hoddetail.tech_email else ''))

                worksheet1.write_string(i, 58, str(
                    member_obj.company.hoddetail.rnd_name if member_obj.company.hoddetail.rnd_name else ''))
                worksheet1.write_string(i, 59, str(
                    member_obj.company.hoddetail.rnd_contact if member_obj.company.hoddetail.rnd_contact else ''))
                worksheet1.write_string(i, 60, str(
                    member_obj.company.hoddetail.rnd_email if member_obj.company.hoddetail.rnd_email else ''))

                worksheet1.write_string(i, 61, str(
                    member_obj.company.hoddetail.exim_name if member_obj.company.hoddetail.exim_name else ''))
                worksheet1.write_string(i, 62, str(
                    member_obj.company.hoddetail.exim_contact if member_obj.company.hoddetail.exim_contact else ''))
                worksheet1.write_string(i, 63, str(
                    member_obj.company.hoddetail.exim_email if member_obj.company.hoddetail.exim_email else ''))

            i = i + 1
            j = j + 1
            k = k + 1

        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Members_Detail_Data' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | membership_data_download | User = ', request.user
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | membership_data_download | EXCP = ', str(traceback.print_exc())

        return False


# TODO Membership company name change
@login_required(login_url='/backofficeapp/login/')
def change_company_name_details_datatable(request):
    try:
        dataList = []
        print '\nRequest IN | membership_report.py | change_comapny_name_details_datatable | User = ', request.user
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

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        j = 1
        k = 1

        if searchTxt:
            old_company_list = MembershipTypeTrack.objects.filter(
                Q(userdetail__company__company_name__icontains=searchTxt) | Q(
                    userdetail__member_associate_no__icontains=searchTxt) | Q(old_company_name__icontains=searchTxt),
                is_deleted=False, old_company_name__isnull=False).exclude(old_company_name__exact='').values(
                'userdetail_id').distinct()
            old_company_obj_list = MembershipTypeTrack.objects.filter(
                Q(userdetail__company__company_name__icontains=searchTxt) | Q(
                    userdetail__member_associate_no__icontains=searchTxt) | Q(old_company_name__icontains=searchTxt),
                is_deleted=False, old_company_name__isnull=False).exclude(
                old_company_name__exact='')

        else:
            old_company_list = MembershipTypeTrack.objects.filter(is_deleted=False,
                                                                  old_company_name__isnull=False).exclude(
                old_company_name__exact='').values('userdetail_id').distinct()
            old_company_obj_list = MembershipTypeTrack.objects.filter(is_deleted=False,
                                                                      old_company_name__isnull=False).exclude(
                old_company_name__exact='')

        for old_company_item in old_company_list:
            temp_track_list = None
            if from_date and to_date:
                from_date = datetime.strptime(from_date, '%d/%m/%Y')
                to_date = datetime.strptime(to_date, '%d/%m/%Y')
                temp_track_list = old_company_obj_list.filter(created_date__range=[from_date, to_date],
                                                              userdetail_id=old_company_item['userdetail_id'])
            else:
                temp_track_list = old_company_obj_list.filter(userdetail_id=old_company_item['userdetail_id'])

            track_list_count = temp_track_list.count()
            if temp_track_list:
                for i in range(0, track_list_count):
                    temp_list = []
                    try:
                        if temp_track_list[i].old_company_name != temp_track_list[i].userdetail.company.company_name:
                            temp_list = []
                            temp_list.append(j)
                            temp_list.append(str(temp_track_list[i].userdetail.member_associate_no).strip())
                            temp_list.append(str(temp_track_list[i + 1].old_company_name).strip())
                            temp_list.append(str(temp_track_list[i].old_company_name).strip())
                            temp_list.append(temp_track_list[i].created_date.date())
                    except Exception, e:
                        temp_list = []
                        temp_list.append(j)
                        temp_list.append(str(temp_track_list[i].userdetail.member_associate_no).strip())
                        temp_list.append(str(temp_track_list[i].userdetail.company.company_name).strip())
                        temp_list.append(str(temp_track_list[i].old_company_name).strip())
                        temp_list.append(temp_track_list[i].created_date.date())
                        pass
                    if temp_list:
                        dataList.append(temp_list)
                        j = j + 1
        dataList.sort(key=lambda dataList: dataList[4], reverse=True)
        for list_item in dataList:
            list_item[0] = k
            list_item[4] = list_item[4].strftime('%d/%m/%Y')
            k = k + 1
        total_records = len(dataList)
        if length != -1:
            dataList = dataList[start:length]
        total_record = total_records
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print '\nexception ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
def download_company_name_details(request):
    try:
        print "\nreportapp | membership_report.py | download_company_name_details "
        requested_val = request.GET.get('requested_value')
        temp_from_date = from_date = datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y')
        to_date = datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y')

        date_list = []
        while temp_from_date <= to_date:
            date_list.append(temp_from_date.date())
            temp_from_date = temp_from_date + timedelta(days=1)

        new_old_company_obj_list = []
        old_company_obj_list = MembershipTypeTrack.objects.filter(old_company_name__isnull=False,
                                                                  is_deleted=False).exclude(old_company_name__exact='')
        if from_date > to_date:
            data = {'success': 'invalid_date'}
        else:
            for item in old_company_obj_list:
                if item.created_date.date() in date_list:
                    new_old_company_obj_list.append(item)

        if new_old_company_obj_list:
            data = {"success": "true"}
        else:
            data = {"sucess": "no data"}
    except Exception, e:
        print "\nException In | membership_report.py | download_company_name_details EXCE =", str(traceback.print_exc())
        data = {"success": "false"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def change_company_name_excel(request):
    try:
        print '\nRequest IN | membership_report.py | change_company_name_excel | User = ', request.user
        requested_val = request.GET.get('requested_value')
        temp_from_date = from_date = (datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y'))
        to_date = (datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y'))
        date_list = []
        dataList = []

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Old New Company Name')
        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format = workbook.add_format({'font_size': 10, 'border': 1, 'text_wrap': True})
        worksheet1.set_column('A:A', 4)
        worksheet1.set_column('B:B', 10)
        worksheet1.set_column('C:C', 30)
        worksheet1.set_column('D:D', 30)
        worksheet1.set_column('E:E', 15)

        title_text = 'Change Of Company Name Report Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
            to_date.strftime('%d/%m/%Y'))
        worksheet1.merge_range('A1:E1', title_text, merge_format)

        column_name = ['Sr.No.', 'Membership No.', 'New Company Name', 'Old Company Name', 'Date']

        for i in range(len(column_name)):
            worksheet1.write_string(1, int(i), column_name[i], cell_header_format)

        while temp_from_date <= to_date:
            date_list.append(temp_from_date.date())
            temp_from_date = temp_from_date + timedelta(days=1)

        old_company_list = MembershipTypeTrack.objects.filter(is_deleted=False, old_company_name__isnull=False).exclude(
            old_company_name__exact='').values('userdetail_id').distinct()
        old_company_obj_list = MembershipTypeTrack.objects.filter(is_deleted=False,
                                                                  old_company_name__isnull=False).exclude(
            old_company_name__exact='')

        i = 2
        j = 1
        l = 1
        m = 1

        for old_company_item in old_company_list:
            temp_track_list = old_company_obj_list.filter(userdetail_id=old_company_item['userdetail_id'])
            track_list_count = temp_track_list.count()
            if temp_track_list:
                for k in range(0, track_list_count):
                    temp_list = []
                    try:
                        if temp_track_list[k].old_company_name != temp_track_list[k].userdetail.company.company_name:
                            temp_list = []
                            temp_list.append(j)
                            temp_list.append(str(temp_track_list[k].userdetail.member_associate_no).strip())
                            temp_list.append(str(temp_track_list[k + 1].old_company_name).strip())
                            temp_list.append(str(temp_track_list[k].old_company_name).strip())
                            temp_list.append(temp_track_list[k].created_date.date())
                    except Exception, e:
                        temp_list = []
                        temp_list.append(j)
                        temp_list.append(str(temp_track_list[k].userdetail.member_associate_no).strip())
                        temp_list.append(str(temp_track_list[k].userdetail.company.company_name).strip())
                        temp_list.append(str(temp_track_list[k].old_company_name).strip())
                        temp_list.append(temp_track_list[k].created_date.date())
                        pass
                    if temp_list:
                        dataList.append(temp_list)
                        j = j + 1

        dataList.sort(key=lambda dataList: dataList[4], reverse=True)
        for item in dataList:
            if item[4] in date_list:
                worksheet1.write_number(i, 0, l, cell_format)
                worksheet1.write_string(i, 1, str(item[1]), cell_format)
                worksheet1.write_string(i, 2, item[2], cell_format)
                worksheet1.write_string(i, 3, item[3], cell_format)
                worksheet1.write_string(i, 4, item[4].strftime('%d/%m/%Y'), cell_format)
                l = l + 1
                i = i + 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Old_New_Company_Report' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | change_company_name_excel | User = '
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | change_company_name_excel | EXCP = ', str(traceback.print_exc())
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


# Download reports for new and renewal members
@login_required(login_url='/backofficeapp/login/')
def check_membership_online_renewal_count(request):
    try:
        print '\Request IN | membership_report.py | check_membership_online_renewal_count | User = ', request.user
        from_date = datetime.strptime(str(request.GET.get('date_from')), '%d/%m/%Y').date()
        to_date = (datetime.strptime(str(request.GET.get('date_to')), '%d/%m/%Y')).date()
        report_type = request.GET.get('report_type')
        payment_type = request.GET.get('payment_type')
        if to_date < from_date:
            data = {"success": "validate"}
        else:
            if request.GET.get('report_type') == 'RENEW':
                if payment_type == 'Offline':
                    invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                    membershipInvoice__is_paid=True,
                                                                    membershipInvoice__invoice_for__in=['RENEW',
                                                                                                        'RE-ASSOCIATE'],
                                                                    user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                                                                    is_deleted=False).values(
                        'membershipInvoice_id').distinct()
                elif payment_type == 'Online':
                    invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                    membershipInvoice__is_paid=True,
                                                                    membershipInvoice__invoice_for__in=['RENEW',
                                                                                                        'RE-ASSOCIATE'],
                                                                    user_Payment_Type='Online',
                                                                    is_deleted=False).values(
                        'membershipInvoice_id').distinct()
                else:
                    invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                    membershipInvoice__is_paid=True,
                                                                    membershipInvoice__invoice_for__in=['RENEW',
                                                                                                        'RE-ASSOCIATE'],
                                                                    is_deleted=False).values(
                        'membershipInvoice_id').distinct()
            elif request.GET.get('report_type') == 'NEW':
                if payment_type == 'Offline':
                    invoice_id_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                        user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                        is_deleted=False).values('membershipInvoice_id').distinct()
                elif payment_type == 'Online':
                    invoice_id_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                        user_Payment_Type='Online',
                        is_deleted=False).values('membershipInvoice_id').distinct()
                else:
                    invoice_id_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', is_deleted=False).values(
                        'membershipInvoice_id').distinct()

            elif request.GET.get('report_type') == 'All':
                if payment_type == 'Offline':
                    invoice_id_list = PaymentDetails.objects.filter(
                        Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                            payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                        is_deleted=False)
                elif payment_type == 'Online':
                    invoice_id_list = PaymentDetails.objects.filter(
                        Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                            payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                        user_Payment_Type='Online',
                        is_deleted=False).values('membershipInvoice_id').distinct()
                else:
                    invoice_id_list = PaymentDetails.objects.filter(
                        Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                            payment_date__range=[from_date, to_date]),
                        membershipInvoice__is_paid=True, is_deleted=False).values('membershipInvoice_id').distinct()

            if invoice_id_list:
                data = {'success': 'true'}
            else:
                data = {'success': 'no_data'}
    except Exception, e:
        print '\nException IN | membership_report.py | check_membership_online_renewal_count | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def membership_online_renewal_download(request):
    try:
        print '\nRequest IN | membership_report.py | membership_online_renewal_download | User = ', request.user
        from_date = datetime.strptime(str(request.GET.get('date_from')), '%d/%m/%Y').date()
        to_date = (datetime.strptime(str(request.GET.get('date_to')), '%d/%m/%Y')).date()
        report_type = request.GET.get('report_type')
        payment_type = request.GET.get('payment_type')
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Members_Details')
        print_worksheet = workbook.add_worksheet('Members_Details_Print')

        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format = workbook.add_format({'font_size': 10, 'border': 1, 'text_wrap': True})
        worksheet1.set_column('A:A', 4)
        worksheet1.set_column('B:B', 8)
        worksheet1.set_column('C:C', 9)
        worksheet1.set_column('D:D', 10)
        worksheet1.set_column('E:E', 13)
        worksheet1.set_column('F:F', 13)
        worksheet1.set_column('G:G', 10)
        worksheet1.set_column('H:H', 13)
        worksheet1.set_column('I:I', 10)
        worksheet1.set_column('J:J', 10)
        worksheet1.set_column('K:K', 8)
        worksheet1.set_column('L:L', 6)
        worksheet1.set_column('N:N', 10)
        worksheet1.set_column('W:W', 10)
        worksheet1.set_column('X:X', 15)
        worksheet1.set_column('Y:Y', 15)
        worksheet1.set_column('Z:Z', 17)
        worksheet1.set_column('AA:AA', 10)
        worksheet1.set_column('AB:AB', 21)

        title_text = str('Renewal Member Details Report ') + ' between ' + str(
            from_date.strftime('%d/%m/%Y')) + ' to ' + str(
            to_date.strftime('%d/%m/%Y')) if report_type == 'RENEW' else str(
            'New Member Details Report') + ' between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
            to_date.strftime('%d/%m/%Y'))
        title_text_all = 'New and Renew Members Report between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
            to_date.strftime('%d/%m/%Y'))
        if report_type != 'All':
            worksheet1.merge_range('A1:AA1', title_text, merge_format)
            print_worksheet.merge_range('A1:H1', title_text, merge_format)
        else:
            worksheet1.merge_range('A1:AA1', title_text_all, merge_format)
            print_worksheet.merge_range('A1:I1', title_text_all, merge_format)

        column_name = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership No.', 'Company Name', 'CEO Name',
                       'CEO Contact', 'CEO Email',
                       'POC Name', 'POC Contact', 'POC Email', 'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN',
                       'Financial Year', 'Turnover', 'Category', 'Total Payable',
                       'Total Paid', 'GST Amount', 'Entrance Fee', 'Payment Mode', 'Bank Name', 'Payment Details',
                       'Cheque Date', 'Industry']

        column_name_all = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership No.', 'Type', 'Company Name',
                           'CEO Name', 'CEO Contact', 'CEO Email',
                           'POC Name', 'POC Contact', 'POC Email', 'Other Contact', 'Address', 'City', 'Pincode',
                           'GSTIN', 'Financial Year', 'Turnover', 'Category', 'Total Payable',
                           'Total Paid', 'GST Amount', 'Payment Mode', 'Bank Name', 'Payment Details', 'Cheque Date',
                           'Industry']

        column_name_renew = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership No.', 'Company Name', 'CEO Name',
                             'CEO Contact', 'CEO Email', 'POC Name', 'POC Contact', 'POC Email',
                             'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN', 'Financial Year', 'Turnover',
                             'Category', 'Total Payable',
                             'Total Paid', 'GST Amount', 'Payment Mode', 'Bank Name', 'Payment Details', 'Cheque Date',
                             'Industry']

        print_column = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership No.', 'Company Name', 'Financial Year',
                        'Payment Mode', 'Total Payable',
                        'Total Paid']

        print_column_renewal = ['Sr.No.', 'Payment Date', 'Membership No.', 'Company Name', 'Financial Year',
                                'Payment Mode', 'Total Payable',
                                'Total Paid']

        if report_type == 'NEW':
            for i in range(len(column_name)):
                worksheet1.write_string(1, int(i), column_name[i], cell_header_format)
        elif report_type == 'RENEW':
            for i in range(len(column_name_renew)):
                worksheet1.write_string(1, int(i), column_name_renew[i], cell_header_format)
        else:
            for i in range(len(column_name_all)):
                worksheet1.write_string(1, int(i), column_name_all[i], cell_header_format)

        cell_format2 = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1})
        cell_format2.set_align('vcenter')
        cell_format2.set_rotation(90)

        print_worksheet.set_column('A:A', 4)
        print_worksheet.set_column('B:B', 9)
        print_worksheet.set_column('C:C', 10)
        print_worksheet.set_column('D:D', 10)
        print_worksheet.set_column('E:E', 20)
        print_worksheet.set_column('F:F', 8)
        print_worksheet.set_column('G:G', 8)
        print_worksheet.set_column('H:H', 6)
        print_worksheet.set_column('I:I', 6)

        if report_type == 'RENEW':
            for i in range(len(print_column_renewal)):
                if i in []:
                    print_worksheet.write_string(1, int(i), print_column_renewal[i], cell_header_format)
                else:
                    print_worksheet.write_string(1, int(i), print_column_renewal[i], cell_header_format)
        else:
            for i in range(len(print_column)):
                if i in []:
                    print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)
                else:
                    print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)

        invoice_id_list = None
        if report_type == 'RENEW':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                                                                is_deleted=False).order_by('payment_date').values(
                    'membershipInvoice_id').distinct()
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                user_Payment_Type='Online',
                                                                is_deleted=False).order_by('payment_date').values(
                    'membershipInvoice_id').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                is_deleted=False).order_by('payment_date').values(
                    'membershipInvoice_id').distinct()
        elif request.GET.get('report_type') == 'NEW':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                    user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                    is_deleted=False).order_by('userdetail__membership_acceptance_date').values(
                    'membershipInvoice_id').distinct()
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', user_Payment_Type='Online',
                    is_deleted=False).order_by('userdetail__membership_acceptance_date').values(
                    'membershipInvoice_id').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', is_deleted=False).values(
                    'membershipInvoice_id').distinct()

        elif request.GET.get('report_type') == 'All':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]), is_deleted=False,
                    membershipInvoice__is_paid=True).values('membershipInvoice_id').distinct()
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]),
                    membershipInvoice__is_paid=True, user_Payment_Type='Online', is_deleted=False).values(
                    'membershipInvoice_id').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]),
                    membershipInvoice__is_paid=True, is_deleted=False).values('membershipInvoice_id').distinct()

        k = 2
        i = 2
        j = 1
        flag = ''
        for invoice_id in invoice_id_list:
            if report_type == 'RENEW':
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])
            elif report_type == 'NEW':
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])
            else:
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])

            amount_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj.id, is_deleted=False).aggregate(
                Sum('amount_paid'))
            amount = 0
            if amount_obj['amount_paid__sum']:
                amount = float(amount_obj['amount_paid__sum'])

            payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj.id, is_deleted=False).last()

            if payment_obj.userdetail.member_associate_no:
                if payment_obj.user_Payment_Type == 'Cheque':
                    flag = 'CHEQUE'
                elif payment_obj.user_Payment_Type == 'NEFT' and payment_obj.neft_transfer_id != 'Paid_Online':
                    flag = 'NEFT'
                elif payment_obj.user_Payment_Type == 'Cash':
                    flag = 'CASH'
                else:
                    flag = 'ONLINE'

                user_industry_list = payment_obj.userdetail.company.industrydescription.all()
                industrydescription = (', '.join([str(item.description).strip() for item in user_industry_list]))

                worksheet1.write_number(i, 0, int(j), cell_format)
                worksheet1.write_string(i, 1, str(
                    payment_obj.payment_date.strftime('%d/%m/%Y') if payment_obj.payment_date else ''), cell_format)
                worksheet1.write_string(i, 2, str(payment_obj.userdetail.membership_acceptance_date.strftime(
                    '%d/%m/%Y') if payment_obj.userdetail.membership_acceptance_date else ''), cell_format)
                worksheet1.write_string(i, 3, str(
                    payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                        cell_format)
                worksheet1.write_string(i, 4, str(
                    payment_obj.userdetail.company.company_name) if payment_obj.userdetail.company.company_name else '',
                                        cell_format)
                worksheet1.write_string(i, 5,
                                        str(payment_obj.userdetail.ceo_name) if payment_obj.userdetail.ceo_name else '',
                                        cell_format)
                worksheet1.write_string(i, 6, str(
                    payment_obj.userdetail.ceo_cellno) if payment_obj.userdetail.ceo_cellno else '', cell_format)
                worksheet1.write_string(i, 7, str(
                    payment_obj.userdetail.ceo_email) if payment_obj.userdetail.ceo_email else '', cell_format)
                worksheet1.write_string(i, 8,
                                        str(payment_obj.userdetail.poc_name) if payment_obj.userdetail.poc_name else '',
                                        cell_format)
                worksheet1.write_string(i, 9, str(
                    payment_obj.userdetail.poc_contact) if payment_obj.userdetail.poc_contact else '', cell_format)
                worksheet1.write_string(i, 10, str(
                    payment_obj.userdetail.poc_email) if payment_obj.userdetail.poc_email else '', cell_format)
                worksheet1.write_string(i, 11, str(
                    payment_obj.userdetail.correspond_cellno) if payment_obj.userdetail.correspond_cellno else '',
                                        cell_format)
                worksheet1.write_string(i, 12, str(payment_obj.userdetail.correspond_address), cell_format)
                worksheet1.write_string(i, 13, str(payment_obj.userdetail.correspondcity), cell_format)
                worksheet1.write_string(i, 14, str(payment_obj.userdetail.correspond_pincode), cell_format)
                worksheet1.write_string(i, 15, str(payment_obj.userdetail.gst) if payment_obj.userdetail.gst else '',
                                        cell_format)
                worksheet1.write_string(i, 16, str(payment_obj.membershipInvoice.financial_year), cell_format)
                worksheet1.write_string(i, 17, str(payment_obj.userdetail.annual_turnover_rupees), cell_format)
                worksheet1.write_string(i, 18, str(payment_obj.membershipInvoice.membership_category), cell_format)
                worksheet1.write_number(i, 19, int(payment_obj.membershipInvoice.amount_payable), cell_format)
                worksheet1.write_number(i, 20, int(amount), cell_format)
                worksheet1.write_number(i, 21, int(
                    payment_obj.membershipInvoice.tax) if payment_obj.membershipInvoice.tax else '', cell_format)
                if report_type == 'NEW':
                    worksheet1.write_number(i, 22, int(payment_obj.userdetail.membership_slab.entrance_fee),
                                            cell_format)
                    worksheet1.write_string(i, 23,
                                            str(payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '',
                                            cell_format)
                    worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                            cell_format)
                    worksheet1.write_string(i, 25, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                            cell_format)
                    worksheet1.write_string(i, 26, str(
                        payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '', cell_format)
                    worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    if flag == 'CHEQUE':
                        worksheet1.write_string(i, 23, str('Cheque'), cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 25, str(payment_obj.cheque_no), cell_format)
                        worksheet1.write_string(i, 26, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    elif flag == 'NEFT':
                        worksheet1.write_string(i, 23, str('NEFT'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(
                            payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    elif flag == 'CASH':
                        worksheet1.write_string(i, 23, str('Cash'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    else:
                        worksheet1.write_string(i, 23, str('Online'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                elif report_type == 'RENEW':
                    worksheet1.write_string(i, 22,
                                            str(payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '',
                                            cell_format)
                    worksheet1.write_string(i, 23, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                            cell_format)
                    worksheet1.write_string(i, 24, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                            cell_format)
                    worksheet1.write_string(i, 25, str(
                        payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '', cell_format)
                    worksheet1.write_string(i, 26, str(industrydescription), cell_format)
                    if flag == 'CHEQUE':
                        worksheet1.write_string(i, 22, str('Cheque'), cell_format)
                        worksheet1.write_string(i, 23, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.cheque_no if payment_obj.cheque_no else ''),
                                                cell_format)
                        worksheet1.write_string(i, 25, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 26, str(industrydescription), cell_format)
                    elif flag == 'NEFT':
                        worksheet1.write_string(i, 22, str('NEFT'), cell_format)
                        worksheet1.write_string(i, 23, str(''), cell_format)
                        worksheet1.write_string(i, 24, str(
                            payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(industrydescription), cell_format)
                    elif flag == 'CASH':
                        worksheet1.write_string(i, 22, str('Cash'), cell_format)
                        worksheet1.write_string(i, 23, str(''), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(industrydescription), cell_format)
                    else:
                        worksheet1.write_string(i, 22, str('Online'), cell_format)
                        worksheet1.write_string(i, 23, str(''), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(industrydescription), cell_format)
                else:
                    if payment_obj.userdetail.member_associate_no:
                        worksheet1.write_number(i, 0, int(j), cell_format)
                        worksheet1.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y') if payment_obj.payment_date else ''),
                                                cell_format)
                        worksheet1.write_string(i, 2, str(payment_obj.userdetail.membership_acceptance_date.strftime(
                            '%d/%m/%Y') if payment_obj.userdetail.membership_acceptance_date else ''), cell_format)
                        worksheet1.write_string(i, 3, str(
                            payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                                cell_format)
                        worksheet1.write_string(i, 4, str(
                            payment_obj.membershipInvoice.invoice_for) if payment_obj.membershipInvoice.invoice_for else '',
                                                cell_format)
                        worksheet1.write_string(i, 5, str(
                            payment_obj.userdetail.company.company_name) if payment_obj.userdetail.company.company_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 6, str(
                            payment_obj.userdetail.ceo_name) if payment_obj.userdetail.ceo_name else '', cell_format)
                        worksheet1.write_string(i, 7, str(
                            payment_obj.userdetail.ceo_cellno) if payment_obj.userdetail.ceo_cellno else '',
                                                cell_format)
                        worksheet1.write_string(i, 8, str(
                            payment_obj.userdetail.ceo_email) if payment_obj.userdetail.ceo_email else '', cell_format)
                        worksheet1.write_string(i, 9, str(
                            payment_obj.userdetail.poc_name) if payment_obj.userdetail.poc_name else '', cell_format)
                        worksheet1.write_string(i, 10, str(
                            payment_obj.userdetail.poc_contact) if payment_obj.userdetail.poc_contact else '',
                                                cell_format)
                        worksheet1.write_string(i, 11, str(
                            payment_obj.userdetail.poc_email) if payment_obj.userdetail.poc_email else '', cell_format)
                        worksheet1.write_string(i, 12, str(
                            payment_obj.userdetail.correspond_cellno) if payment_obj.userdetail.correspond_cellno else '',
                                                cell_format)
                        worksheet1.write_string(i, 13, str(payment_obj.userdetail.correspond_address), cell_format)
                        worksheet1.write_string(i, 14, str(payment_obj.userdetail.correspondcity), cell_format)
                        worksheet1.write_string(i, 15, str(payment_obj.userdetail.correspond_pincode), cell_format)
                        worksheet1.write_string(i, 16,
                                                str(payment_obj.userdetail.gst) if payment_obj.userdetail.gst else '',
                                                cell_format)
                        worksheet1.write_string(i, 17, str(payment_obj.membershipInvoice.financial_year), cell_format)
                        worksheet1.write_string(i, 18, str(payment_obj.userdetail.annual_turnover_rupees), cell_format)
                        worksheet1.write_string(i, 19, str(payment_obj.membershipInvoice.membership_category),
                                                cell_format)
                        worksheet1.write_number(i, 20, int(payment_obj.membershipInvoice.amount_payable), cell_format)
                        worksheet1.write_number(i, 21, int(amount), cell_format)
                        worksheet1.write_number(i, 22, int(
                            payment_obj.membershipInvoice.tax) if payment_obj.membershipInvoice.tax else '',
                                                cell_format)
                        worksheet1.write_string(i, 23, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 25, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                                cell_format)
                        worksheet1.write_string(i, 26, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                        if flag == 'CHEQUE':
                            worksheet1.write_string(i, 23, str('Cheque'), cell_format)
                            worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                    cell_format)
                            worksheet1.write_string(i, 25, str(payment_obj.cheque_no), cell_format)
                            worksheet1.write_string(i, 26, str(
                                payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                    cell_format)
                            worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                        elif flag == 'NEFT':
                            worksheet1.write_string(i, 23, str('NEFT'), cell_format)
                            worksheet1.write_string(i, 24, str(''), cell_format)
                            worksheet1.write_string(i, 25, str(
                                payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                            worksheet1.write_string(i, 27, str(industrydescription), cell_format)

                        elif flag == 'CASH':
                            worksheet1.write_string(i, 23, str('Cash'), cell_format)
                            worksheet1.write_string(i, 24, str(''), cell_format)
                            worksheet1.write_string(i, 25, str(''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                            worksheet1.write_string(i, 27, str(industrydescription), cell_format)

                        else:
                            worksheet1.write_string(i, 23, str('Online'), cell_format)
                            worksheet1.write_string(i, 24, str(''), cell_format)
                            worksheet1.write_string(i, 25, str(''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                            worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    else:
                        pass
                if payment_obj.userdetail.member_associate_no:
                    if report_type == 'RENEW':
                        print_worksheet.write_number(i, 0, int(j), cell_format)
                        print_worksheet.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y') if payment_obj.payment_date else ''),
                                                     cell_format)
                        print_worksheet.write_string(i, 2, str(payment_obj.userdetail.member_associate_no), cell_format)
                        print_worksheet.write_string(i, 3, str(payment_obj.userdetail.company.company_name),
                                                     cell_format)
                        print_worksheet.write_string(i, 4, str(payment_obj.membershipInvoice.financial_year),
                                                     cell_format)
                        print_worksheet.write_string(i, 5, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        print_worksheet.write_number(i, 6, int(payment_obj.membershipInvoice.amount_payable),
                                                     cell_format)
                        print_worksheet.write_number(i, 7, int(amount), cell_format)
                    else:
                        print_worksheet.write_number(i, 0, int(j), cell_format)
                        print_worksheet.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y') if payment_obj.payment_date else ''),
                                                     cell_format)
                        print_worksheet.write_string(i, 2, str(
                            payment_obj.userdetail.membership_acceptance_date.strftime(
                                '%d/%m/%Y') if payment_obj.userdetail.membership_acceptance_date else ''), cell_format)
                        print_worksheet.write_string(i, 3, str(payment_obj.userdetail.member_associate_no), cell_format)
                        print_worksheet.write_string(i, 4, str(payment_obj.userdetail.company.company_name),
                                                     cell_format)
                        print_worksheet.write_string(i, 5, str(payment_obj.membershipInvoice.financial_year),
                                                     cell_format)
                        print_worksheet.write_string(i, 6, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        print_worksheet.write_number(i, 7, int(payment_obj.membershipInvoice.amount_payable),
                                                     cell_format)
                        print_worksheet.write_number(i, 8, int(amount), cell_format)

                i = i + 1
                j = j + 1
                k = k + 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Members_Details' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | membership_online_renewal_download | User = '
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | membership_online_renewal_download | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


# Download subscription reports for new and renewal members
@login_required(login_url='/backofficeapp/login/')
def check_membership_subscription_count(request):
    try:
        print '\Request IN | membership_report.py | check_membership_subscription_count | User = ', request.user
        from_date = datetime.strptime(str(request.GET.get('date_from')), '%d/%m/%Y').date()
        to_date = (datetime.strptime(str(request.GET.get('date_to')), '%d/%m/%Y')).date()
        report_type = request.GET.get('report_type')
        payment_type = request.GET.get('payment_type')
        invoice_id_list = PaymentDetails.objects.filter(is_deleted=False)
        if to_date < from_date:
            data = {"success": "validate"}
        else:
            if request.GET.get('report_type') == 'RENEW':
                if payment_type == 'Offline':
                    invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                    membershipInvoice__is_paid=True,
                                                                    membershipInvoice__invoice_for__in=['RENEW',
                                                                                                        'RE-ASSOCIATE'],
                                                                    user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                                                                    is_deleted=False).values(
                        'membershipInvoice_id').distinct()
                elif payment_type == 'Online':
                    invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                    membershipInvoice__is_paid=True,
                                                                    membershipInvoice__invoice_for__in=['RENEW',
                                                                                                        'RE-ASSOCIATE'],
                                                                    user_Payment_Type='Online',
                                                                    is_deleted=False).values(
                        'membershipInvoice_id').distinct()
                else:
                    invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                    membershipInvoice__is_paid=True,
                                                                    membershipInvoice__invoice_for__in=['RENEW',
                                                                                                        'RE-ASSOCIATE'],
                                                                    is_deleted=False).values(
                        'membershipInvoice_id').distinct()
            elif request.GET.get('report_type') == 'NEW':
                if payment_type == 'Offline':
                    invoice_id_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                        user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                        is_deleted=False).values('membershipInvoice_id').distinct()
                elif payment_type == 'Online':
                    invoice_id_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                        user_Payment_Type='Online',
                        is_deleted=False).values('membershipInvoice_id').distinct()
                else:
                    invoice_id_list = PaymentDetails.objects.filter(
                        userdetail__membership_acceptance_date__range=[from_date, to_date],
                        membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', is_deleted=False).values(
                        'membershipInvoice_id').distinct()

            elif request.GET.get('report_type') == 'All':
                if payment_type == 'Offline':
                    invoice_id_list = PaymentDetails.objects.filter(
                        Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                            payment_date__range=[from_date, to_date]), is_deleted=False)
                elif payment_type == 'Online':
                    invoice_id_list = PaymentDetails.objects.filter(
                        Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                            payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                        user_Payment_Type='Online',
                        is_deleted=False).values('membershipInvoice_id').distinct()
                else:
                    invoice_id_list = PaymentDetails.objects.filter(
                        Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                            payment_date__range=[from_date, to_date]),
                        membershipInvoice__is_paid=True, is_deleted=False).values('membershipInvoice_id').distinct()

            if invoice_id_list:
                data = {'success': 'true'}
            else:
                data = {'success': 'no_data'}
    except Exception, e:
        print '\nException IN | membership_report.py | check_membership_subscription_count | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def membership_subscription_report(request):
    try:
        print '\nRequest IN | membership_report.py | membership_subscription_report | User = ', request.user
        from_date = datetime.strptime(str(request.GET.get('date_from')), '%d/%m/%Y').date()
        to_date = (datetime.strptime(str(request.GET.get('date_to')), '%d/%m/%Y')).date()
        report_type = request.GET.get('report_type')
        payment_type = request.GET.get('payment_type')
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Subscription_Report')
        print_worksheet = workbook.add_worksheet('Subscription_Report_Print')

        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format = workbook.add_format({'font_size': 10, 'border': 1, 'text_wrap': True})

        worksheet1.set_column('A:A', 4)
        worksheet1.set_column('B:B', 9)
        worksheet1.set_column('C:C', 8)
        worksheet1.set_column('D:D', 9)
        worksheet1.set_column('E:E', 10)
        worksheet1.set_column('F:F', 16)
        worksheet1.set_column('G:G', 12)
        worksheet1.set_column('H:H', 12)
        worksheet1.set_column('I:I', 10)
        worksheet1.set_column('J:J', 20)
        worksheet1.set_column('O:O', 8)
        worksheet1.set_column('P:P', 15)
        worksheet1.set_column('X:X', 16)
        worksheet1.set_column('Y:Y', 16)
        worksheet1.set_column('Z:Z', 20)
        worksheet1.set_column('AA:AA', 20)
        worksheet1.set_column('AB:AB', 15)
        worksheet1.set_column('AC:AC', 20)

        title_text = 'Subscription Wise ' + (str('Renewal Members Report ') if report_type == 'RENEW' else str(
            'New Members Report ')) + 'between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
            to_date.strftime('%d/%m/%Y'))
        title_text_all = 'Subscription Wise New and Renew Members Report between ' + str(
            from_date.strftime('%d/%m/%Y')) + ' to ' + str(to_date.strftime('%d/%m/%Y'))
        if report_type != 'All':
            worksheet1.merge_range('A1:X1', title_text, merge_format)
            print_worksheet.merge_range('A1:J1', title_text, merge_format)
        else:
            worksheet1.merge_range('A1:X1', title_text_all, merge_format)
            print_worksheet.merge_range('A1:J1', title_text_all, merge_format)

        column_name = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership Slab', 'Membership No.', 'Company Name',
                       'CEO Name', 'CEO Contact', 'CEO Email', 'POC Name', 'POC Contact', 'POC Email',
                       'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN', 'Financial Year', 'Turnover', 'Category',
                       'Total Payable',
                       'Total Paid', 'GST Amount', 'Entrance Fee', 'Payment Mode', 'Bank Name', 'Payment Details',
                       'Cheque Date', 'Industry']

        column_name_all = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership Slab', 'Membership No.', 'Type',
                           'Company Name', 'CEO Name', 'CEO Contact', 'CEO Email', 'POC Name', 'POC Contact',
                           'POC Email',
                           'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN', 'Financial Year', 'Turnover',
                           'Category', 'Total Payable',
                           'Total Paid', 'GST Amount', 'Payment Mode', 'Bank Name', 'Payment Details', 'Cheque Date',
                           'Industry']

        column_name_renew = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership Slab', 'Membership No.',
                             'Company Name', 'CEO Name', 'CEO Contact', 'CEO Email', 'POC Name', 'POC Contact',
                             'POC Email',
                             'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN', 'Financial Year', 'Turnover',
                             'Category', 'Total Payable',
                             'Total Paid', 'GST Amount', 'Payment Mode', 'Bank Name', 'Payment Details', 'Cheque Date',
                             'Industry']

        print_column = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership Slab', 'Membership No.',
                        'Company Name', 'Financial Year', 'Payment Mode',
                        'Total Payable', 'Total Paid']

        print_column_renewal = ['Sr.No.', 'Payment Date', 'Membership Slab', 'Membership No.', 'Company Name',
                                'Financial Year', 'Payment Mode',
                                'Total Payable', 'Total Paid']

        if report_type == 'NEW':
            for i in range(len(column_name)):
                worksheet1.write_string(1, int(i), column_name[i], cell_header_format)
        elif report_type == 'RENEW':
            for i in range(len(column_name_renew)):
                worksheet1.write_string(1, int(i), column_name_renew[i], cell_header_format)
        else:
            for i in range(len(column_name_all)):
                worksheet1.write_string(1, int(i), column_name_all[i], cell_header_format)

        cell_format2 = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1})
        cell_format2.set_align('vcenter')
        cell_format2.set_rotation(90)

        print_worksheet.set_column('A:A', 4)
        print_worksheet.set_column('B:B', 9)
        print_worksheet.set_column('C:C', 9)
        print_worksheet.set_column('D:D', 10)
        print_worksheet.set_column('E:E', 10)
        print_worksheet.set_column('F:F', 15)
        print_worksheet.set_column('G:G', 8)
        print_worksheet.set_column('H:H', 8)
        print_worksheet.set_column('I:I', 8)

        if report_type == 'RENEW':
            for i in range(len(print_column_renewal)):
                if i in []:
                    print_worksheet.write_string(1, int(i), print_column_renewal[i], cell_header_format)
                else:
                    print_worksheet.write_string(1, int(i), print_column_renewal[i], cell_header_format)
        else:
            for i in range(len(print_column)):
                if i in []:
                    print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)
                else:
                    print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)

        invoice_id_list = None
        if report_type == 'RENEW':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                                                                is_deleted=False).values('membershipInvoice_id',
                                                                                         'membershipInvoice__membership_slab__annual_fee').distinct()

            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                user_Payment_Type='Online',
                                                                is_deleted=False).values('membershipInvoice_id',
                                                                                         'membershipInvoice__membership_slab__annual_fee').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                is_deleted=False).values('membershipInvoice_id',
                                                                                         'membershipInvoice__membership_slab__annual_fee').distinct()
        elif request.GET.get('report_type') == 'NEW':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                    user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                    is_deleted=False).values('membershipInvoice_id',
                                             'membershipInvoice__membership_slab__annual_fee').distinct()
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', user_Payment_Type='Online',
                    is_deleted=False).values('membershipInvoice_id',
                                             'membershipInvoice__membership_slab__annual_fee').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', is_deleted=False).values(
                    'membershipInvoice_id', 'membershipInvoice__membership_slab__annual_fee').distinct()


        elif request.GET.get('report_type') == 'All':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]), is_deleted=False).values('membershipInvoice_id',
                                                                                            'membershipInvoice__membership_slab__annual_fee').distinct()
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                    user_Payment_Type='Online',
                    is_deleted=False).values('membershipInvoice_id',
                                             'membershipInvoice__membership_slab__annual_fee').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]),
                    membershipInvoice__is_paid=True, is_deleted=False).values('membershipInvoice_id',
                                                                              'membershipInvoice__membership_slab__annual_fee').distinct()

        if invoice_id_list:
            invoice_id_list = sorted(invoice_id_list,
                                     key=lambda x: int(x["membershipInvoice__membership_slab__annual_fee"]),
                                     reverse=True)
            for item in invoice_id_list:
                del (item['membershipInvoice__membership_slab__annual_fee'])

        i = 2
        j = 1
        k = 2
        flag = ''
        for invoice_id in invoice_id_list:
            if report_type == 'RENEW':
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])

            elif report_type == 'NEW':
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])
            else:
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])

            amount_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj.id, is_deleted=False).aggregate(
                Sum('amount_paid'))
            amount = 0
            if amount_obj['amount_paid__sum']:
                amount = float(amount_obj['amount_paid__sum'])

            payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj.id, is_deleted=False).last()

            if payment_obj.userdetail.member_associate_no:
                if payment_obj.user_Payment_Type == 'Cheque':
                    flag = 'CHEQUE'
                elif payment_obj.user_Payment_Type == 'NEFT' and payment_obj.neft_transfer_id != 'Paid_Online':
                    flag = 'NEFT'
                elif payment_obj.user_Payment_Type == 'Cash':
                    flag = 'CASH'
                else:
                    flag = 'ONLINE'

                user_industry_list = payment_obj.userdetail.company.industrydescription.all()
                industrydescription = (', '.join([str(item.description).strip() for item in user_industry_list]))

                worksheet1.write_number(i, 0, int(j), cell_format)
                worksheet1.write_string(i, 1, str(
                    payment_obj.payment_date.strftime('%d/%m/%Y')) if payment_obj.payment_date else '', cell_format)
                worksheet1.write_string(i, 2, str(payment_obj.userdetail.membership_acceptance_date.strftime(
                    '%d/%m/%Y')) if payment_obj.userdetail.membership_acceptance_date else '', cell_format)
                worksheet1.write_string(i, 3, str(
                    payment_obj.userdetail.membership_slab.annual_fee) if payment_obj.userdetail.membership_slab.annual_fee else '',
                                        cell_format)
                worksheet1.write_string(i, 4, str(payment_obj.userdetail.member_associate_no), cell_format)
                worksheet1.write_string(i, 5, str(payment_obj.userdetail.company.company_name), cell_format)
                worksheet1.write_string(i, 6,
                                        str(payment_obj.userdetail.ceo_name) if payment_obj.userdetail.ceo_name else '',
                                        cell_format)
                worksheet1.write_string(i, 7, str(
                    payment_obj.userdetail.ceo_cellno) if payment_obj.userdetail.ceo_cellno else '', cell_format)
                worksheet1.write_string(i, 8, str(
                    payment_obj.userdetail.ceo_email) if payment_obj.userdetail.ceo_email else '', cell_format)
                worksheet1.write_string(i, 9,
                                        str(payment_obj.userdetail.poc_name) if payment_obj.userdetail.poc_name else '',
                                        cell_format)
                worksheet1.write_string(i, 10, str(
                    payment_obj.userdetail.poc_contact) if payment_obj.userdetail.poc_contact else '', cell_format)
                worksheet1.write_string(i, 11, str(
                    payment_obj.userdetail.poc_email) if payment_obj.userdetail.poc_email else '', cell_format)
                worksheet1.write_string(i, 12, str(
                    payment_obj.userdetail.correspond_cellno) if payment_obj.userdetail.correspond_cellno else '',
                                        cell_format)
                worksheet1.write_string(i, 13, str(payment_obj.userdetail.correspond_address), cell_format)
                worksheet1.write_string(i, 14, str(payment_obj.userdetail.correspondcity), cell_format)
                worksheet1.write_string(i, 15, str(payment_obj.userdetail.correspond_pincode), cell_format)
                worksheet1.write_string(i, 16, str(payment_obj.userdetail.gst) if payment_obj.userdetail.gst else '',
                                        cell_format)
                worksheet1.write_string(i, 17, str(payment_obj.membershipInvoice.financial_year), cell_format)
                worksheet1.write_string(i, 18, str(payment_obj.userdetail.annual_turnover_rupees), cell_format)
                worksheet1.write_string(i, 19, str(payment_obj.membershipInvoice.membership_category), cell_format)
                worksheet1.write_number(i, 20, int(payment_obj.membershipInvoice.amount_payable), cell_format)
                worksheet1.write_number(i, 21, int(amount), cell_format)
                worksheet1.write_number(i, 22, int(
                    payment_obj.membershipInvoice.tax) if payment_obj.membershipInvoice.tax else '', cell_format)

                if report_type == 'NEW':
                    worksheet1.write_number(i, 23, int(payment_obj.userdetail.membership_slab.entrance_fee),
                                            cell_format)
                    worksheet1.write_string(i, 24, str(payment_obj.user_Payment_Type), cell_format)
                    worksheet1.write_string(i, 25, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                            cell_format)
                    worksheet1.write_string(i, 26, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                            cell_format)
                    worksheet1.write_string(i, 27, str(
                        payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '', cell_format)
                    worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                    if flag == 'CHEQUE':
                        worksheet1.write_string(i, 24, str('Cheque'), cell_format)
                        worksheet1.write_string(i, 25, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 26, str(payment_obj.cheque_no), cell_format)
                        worksheet1.write_string(i, 27, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                    elif flag == 'NEFT':
                        worksheet1.write_string(i, 24, str('NEFT'), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(
                            payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                        worksheet1.write_string(i, 27, str(''), cell_format)
                        worksheet1.write_string(i, 28, str(industrydescription), cell_format)

                    elif flag == 'CASH':
                        worksheet1.write_string(i, 24, str('Cash'), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(''), cell_format)
                        worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                    else:
                        worksheet1.write_string(i, 24, str('Online'), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(''), cell_format)
                        worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                        worksheet1.write_string(i, 29, str(
                            payment_obj.userdetail.poc_name) if payment_obj.userdetail.poc_name else '', cell_format)
                        worksheet1.write_string(i, 30, str(
                            payment_obj.userdetail.poc_contact) if payment_obj.userdetail.poc_contact else '',
                                                cell_format)
                        worksheet1.write_string(i, 31, str(
                            payment_obj.userdetail.poc_email) if payment_obj.userdetail.poc_email else '', cell_format)

                elif report_type == 'RENEW':
                    worksheet1.write_string(i, 23, str(payment_obj.user_Payment_Type), cell_format)
                    worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                            cell_format)
                    worksheet1.write_string(i, 25, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                            cell_format)
                    worksheet1.write_string(i, 26, str(
                        payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '', cell_format)
                    worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    if flag == 'CHEQUE':
                        worksheet1.write_string(i, 23, str('Cheque'), cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 25, str(payment_obj.cheque_no if payment_obj.cheque_no else ''),
                                                cell_format)
                        worksheet1.write_string(i, 26, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)

                    elif flag == 'NEFT':
                        worksheet1.write_string(i, 23, str('NEFT'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(
                            payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    elif flag == 'CASH':
                        worksheet1.write_string(i, 23, str('Cash'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                    else:
                        worksheet1.write_string(i, 23, str('Online'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(industrydescription), cell_format)
                else:
                    if payment_obj.userdetail.member_associate_no:
                        worksheet1.write_number(i, 0, int(j), cell_format)
                        worksheet1.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y')) if payment_obj.payment_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 2, str(payment_obj.userdetail.membership_acceptance_date.strftime(
                            '%d/%m/%Y')) if payment_obj.userdetail.membership_acceptance_date else '', cell_format)
                        worksheet1.write_string(i, 3, str(
                            payment_obj.userdetail.membership_slab.annual_fee) if payment_obj.userdetail.membership_slab.annual_fee else '',
                                                cell_format)
                        worksheet1.write_string(i, 4, str(
                            payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                                cell_format)
                        worksheet1.write_string(i, 5, str(
                            payment_obj.membershipInvoice.invoice_for) if payment_obj.membershipInvoice.invoice_for else '',
                                                cell_format)
                        worksheet1.write_string(i, 6, str(payment_obj.userdetail.company.company_name), cell_format)
                        worksheet1.write_string(i, 7, str(
                            payment_obj.userdetail.ceo_name) if payment_obj.userdetail.ceo_name else '', cell_format)
                        worksheet1.write_string(i, 8, str(
                            payment_obj.userdetail.ceo_cellno) if payment_obj.userdetail.ceo_cellno else '',
                                                cell_format)
                        worksheet1.write_string(i, 9, str(
                            payment_obj.userdetail.ceo_email) if payment_obj.userdetail.ceo_email else '', cell_format)
                        worksheet1.write_string(i, 10, str(
                            payment_obj.userdetail.poc_name) if payment_obj.userdetail.poc_name else '', cell_format)
                        worksheet1.write_string(i, 11, str(
                            payment_obj.userdetail.poc_contact) if payment_obj.userdetail.poc_contact else '',
                                                cell_format)
                        worksheet1.write_string(i, 12, str(
                            payment_obj.userdetail.poc_email) if payment_obj.userdetail.poc_email else '', cell_format)
                        worksheet1.write_string(i, 13, str(
                            payment_obj.userdetail.correspond_cellno) if payment_obj.userdetail.correspond_cellno else '',
                                                cell_format)
                        worksheet1.write_string(i, 14, str(payment_obj.userdetail.correspond_address), cell_format)
                        worksheet1.write_string(i, 15, str(payment_obj.userdetail.correspondcity), cell_format)
                        worksheet1.write_string(i, 16, str(payment_obj.userdetail.correspond_pincode), cell_format)
                        worksheet1.write_string(i, 17,
                                                str(payment_obj.userdetail.gst) if payment_obj.userdetail.gst else '',
                                                cell_format)
                        worksheet1.write_string(i, 18, str(payment_obj.membershipInvoice.financial_year), cell_format)
                        worksheet1.write_string(i, 19, str(payment_obj.userdetail.annual_turnover_rupees), cell_format)
                        worksheet1.write_string(i, 20, str(payment_obj.membershipInvoice.membership_category),
                                                cell_format)
                        worksheet1.write_number(i, 21, int(payment_obj.membershipInvoice.amount_payable), cell_format)
                        worksheet1.write_number(i, 22, int(amount), cell_format)
                        worksheet1.write_number(i, 23, int(
                            payment_obj.membershipInvoice.tax) if payment_obj.membershipInvoice.tax else '',
                                                cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.user_Payment_Type), cell_format)
                        worksheet1.write_string(i, 25, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 26, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                                cell_format)
                        worksheet1.write_string(i, 27, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                        if flag == 'CHEQUE':
                            worksheet1.write_string(i, 24, str('Cheque'), cell_format)
                            worksheet1.write_string(i, 25, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                    cell_format)
                            worksheet1.write_string(i, 26, str(payment_obj.cheque_no), cell_format)
                            worksheet1.write_string(i, 27, str(
                                payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                    cell_format)
                            worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                        elif flag == 'NEFT':
                            worksheet1.write_string(i, 24, str('NEFT'), cell_format)
                            worksheet1.write_string(i, 25, str(''), cell_format)
                            worksheet1.write_string(i, 26, str(
                                payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                            worksheet1.write_string(i, 27, str(''), cell_format)
                            worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                        elif flag == 'CASH':
                            worksheet1.write_string(i, 24, str('Cash'), cell_format)
                            worksheet1.write_string(i, 25, str(''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                            worksheet1.write_string(i, 27, str(''), cell_format)
                            worksheet1.write_string(i, 28, str(industrydescription), cell_format)
                        else:
                            worksheet1.write_string(i, 24, str('Online'), cell_format)
                            worksheet1.write_string(i, 25, str(''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                            worksheet1.write_string(i, 27, str(''), cell_format)
                            worksheet1.write_string(i, 28, str(industrydescription), cell_format)

                if payment_obj.userdetail.member_associate_no:
                    if report_type == 'RENEW':
                        print_worksheet.write_number(i, 0, int(j), cell_format)
                        print_worksheet.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y')) if payment_obj.payment_date else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 2, str(
                            payment_obj.userdetail.membership_slab.annual_fee) if payment_obj.userdetail.membership_slab.annual_fee else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 3, str(
                            payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 4, str(
                            payment_obj.userdetail.company.company_name) if payment_obj.userdetail.company.company_name else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 5, str(
                            payment_obj.membershipInvoice.financial_year) if payment_obj.membershipInvoice.financial_year else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 6, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        print_worksheet.write_number(i, 7, int(payment_obj.membershipInvoice.amount_payable),
                                                     cell_format)
                        print_worksheet.write_number(i, 8, int(amount), cell_format)
                    else:
                        print_worksheet.write_number(i, 0, int(j), cell_format)
                        print_worksheet.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y')) if payment_obj.payment_date else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 2, str(
                            payment_obj.userdetail.membership_acceptance_date.strftime(
                                '%d/%m/%Y')) if payment_obj.userdetail.membership_acceptance_date else '', cell_format)
                        print_worksheet.write_string(i, 3, str(
                            payment_obj.userdetail.membership_slab.annual_fee) if payment_obj.userdetail.membership_slab.annual_fee else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 4, str(
                            payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 5, str(
                            payment_obj.userdetail.company.company_name) if payment_obj.userdetail.company.company_name else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 6, str(
                            payment_obj.membershipInvoice.financial_year) if payment_obj.membershipInvoice.financial_year else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 7, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        print_worksheet.write_number(i, 8, int(payment_obj.membershipInvoice.amount_payable),
                                                     cell_format)
                        print_worksheet.write_number(i, 9, int(amount), cell_format)
                i = i + 1
                j = j + 1
                k = k + 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Subscription Report ' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | membership_subscription_report | User = '
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | membership_subscription_report | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


# Download Industry reports for new and renewal members
@login_required(login_url='/backofficeapp/login/')
def check_membership_industry_report_count(request):
    try:
        print '\nRequest IN | membership_report.py | check_membership_industry_report_count | User = ', request.user
        from_date = datetime.strptime(str(request.GET.get('date_from')), '%d/%m/%Y').date()
        to_date = (datetime.strptime(str(request.GET.get('date_to')), '%d/%m/%Y')).date()
        report_type = request.GET.get('report_type')
        payment_type = request.GET.get('payment_type')
        industry_type = request.GET.get('industry_type')

        industry_obj_list = IndustryDescription.objects.filter(id__in=request.GET.getlist('industry_type_array[]'))

        if to_date < from_date:
            data = {"success": "validate"}
        else:
            if industry_type != 'All':
                if request.GET.get('report_type') == 'RENEW':
                    if payment_type == 'Offline':
                        invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                        membershipInvoice__is_paid=True,
                                                                        membershipInvoice__invoice_for__in=['RENEW',
                                                                                                            'RE-ASSOCIATE'],
                                                                        user_Payment_Type__in=['Cheque', 'Cash',
                                                                                               'NEFT'],
                                                                        userdetail__company__industrydescription__in=industry_obj_list,
                                                                        is_deleted=False).values(
                            'membershipInvoice_id').distinct()
                    elif payment_type == 'Online':
                        invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                        membershipInvoice__is_paid=True,
                                                                        membershipInvoice__invoice_for__in=['RENEW',
                                                                                                            'RE-ASSOCIATE'],
                                                                        user_Payment_Type='Online',
                                                                        userdetail__company__industrydescription__in=industry_obj_list,
                                                                        is_deleted=False).values(
                            'membershipInvoice_id').distinct()
                    else:
                        invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                        membershipInvoice__is_paid=True,
                                                                        membershipInvoice__invoice_for__in=['RENEW',
                                                                                                            'RE-ASSOCIATE'],
                                                                        is_deleted=False,
                                                                        userdetail__company__industrydescription__in=industry_obj_list).values(
                            'membershipInvoice_id').distinct()
                elif request.GET.get('report_type') == 'NEW':
                    if payment_type == 'Offline':
                        invoice_id_list = PaymentDetails.objects.filter(
                            userdetail__membership_acceptance_date__range=[from_date, to_date],
                            membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                            user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                            userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False).values(
                            'membershipInvoice_id').distinct()
                    elif payment_type == 'Online':
                        invoice_id_list = PaymentDetails.objects.filter(
                            userdetail__membership_acceptance_date__range=[from_date, to_date],
                            membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                            user_Payment_Type='Online',
                            userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False).values(
                            'membershipInvoice_id').distinct()
                    else:
                        invoice_id_list = PaymentDetails.objects.filter(
                            userdetail__membership_acceptance_date__range=[from_date, to_date],
                            membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', is_deleted=False,
                            userdetail__company__industrydescription__in=industry_obj_list).values(
                            'membershipInvoice_id').distinct()

                elif request.GET.get('report_type') == 'All':
                    if payment_type == 'Offline':
                        invoice_id_list = PaymentDetails.objects.filter(
                            Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                                payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                            userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False)
                    elif payment_type == 'Online':
                        invoice_id_list = PaymentDetails.objects.filter(
                            Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                                payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                            user_Payment_Type='Online',
                            userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False).values(
                            'membershipInvoice_id').distinct()
                    else:
                        invoice_id_list = PaymentDetails.objects.filter(
                            Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                                payment_date__range=[from_date, to_date]),
                            userdetail__company__industrydescription__in=industry_obj_list,
                            membershipInvoice__is_paid=True, is_deleted=False).values('membershipInvoice_id').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', is_deleted=False,
                    userdetail__company__industrydescription__in=industry_obj_list).values(
                    'membershipInvoice_id').distinct()

            if invoice_id_list:
                data = {'success': 'true'}
            else:
                data = {'success': 'no_data'}
    except Exception, e:
        print '\nException IN | membership_report.py | check_membership_industry_report_count | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def membership_industry_report(request):
    try:
        print '\nRequest IN | membership_report.py | membership_industry_report | User = ', request.user
        industry_type = []
        industry_type1 = []
        from_date = datetime.strptime(str(request.GET.get('date_from')), '%d/%m/%Y').date()
        to_date = (datetime.strptime(str(request.GET.get('date_to')), '%d/%m/%Y')).date()
        report_type = request.GET.get('report_type')
        payment_type = request.GET.get('payment_type')
        industry_type1 = request.GET.get('industry_type')

        temp_list = str(request.GET.get('industry_id_array'))
        temp_industry_id_list = temp_list.split(',')
        temp_industry_id_list = [int(x) for x in temp_industry_id_list]

        industry_obj_list = IndustryDescription.objects.filter(id__in=temp_industry_id_list)

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Industry Report')
        print_worksheet = workbook.add_worksheet('Industry_Report_Print')

        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format = workbook.add_format({'font_size': 10, 'border': 1, 'text_wrap': True})

        column_name = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership Slab', 'Membership No.', 'Company Name',
                       'CEO Name', 'CEO Contact', 'CEO Email', 'POC Name', 'POC Contact', 'POC Email',
                       'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN', 'Financial Year', 'Category',
                       'Total Payable',
                       'Total Paid', 'GST Amount', 'Entrance Fee', 'Payment Mode', 'Bank Name', 'Payment Details',
                       'Cheque Date', 'Industry Description']

        column_name_all = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership Slab', 'Membership No.', 'Type',
                           'Company Name', 'CEO Name', 'CEO Contact', 'CEO Email', 'POC Name', 'POC Contact',
                           'POC Email',
                           'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN', 'Financial Year', 'Category',
                           'Total Payable',
                           'Total Paid', 'GST Amount', 'Payment Mode', 'Bank Name', 'Payment Details', 'Cheque Date',
                           'Industry Description']

        column_name_renew = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership Slab', 'Membership No.',
                             'Company Name', 'CEO Name', 'CEO Contact', 'CEO Email', 'POC Name', 'POC Contact',
                             'POC Email',
                             'Other Contact', 'Address', 'City', 'Pincode', 'GSTIN', 'Financial Year', 'Category',
                             'Total Payable',
                             'Total Paid', 'GST Amount', 'Payment Mode', 'Bank Name', 'Payment Details', 'Cheque Date',
                             'Industry Description']

        print_column = ['Sr.No.', 'Payment Date', 'Acceptance Date', 'Membership No.', 'Company Name', 'Financial Year',
                        'Payment Mode', 'Total Payable',
                        'Total Paid', 'Industry Description']

        print_column_renewal = ['Sr.No.', 'Payment Date', 'Membership No.', 'Company Name', 'Financial Year',
                                'Payment Mode', 'Total Payable',
                                'Total Paid', 'Industry Description']

        worksheet1.set_column('A:A', 4)
        worksheet1.set_column('B:B', 9)
        worksheet1.set_column('C:C', 9)
        worksheet1.set_column('D:D', 9)
        worksheet1.set_column('E:E', 15)
        worksheet1.set_column('F:F', 16)
        worksheet1.set_column('G:G', 12)
        worksheet1.set_column('H:H', 12)
        worksheet1.set_column('I:I', 10)
        worksheet1.set_column('J:J', 20)
        worksheet1.set_column('O:O', 8)
        worksheet1.set_column('P:P', 15)
        worksheet1.set_column('V:V', 15)
        worksheet1.set_column('W:W', 16)
        worksheet1.set_column('Y:Y', 16)
        worksheet1.set_column('Z:Z', 23)
        worksheet1.set_column('AA:AA', 23)

        title_text = 'Industry Wise ' + (
            str('Renewal Report ') if report_type == 'RENEW' else str('New Report')) + ' Between ' + str(
            from_date.strftime('%d/%m/%Y')) + ' to ' + str(to_date.strftime('%d/%m/%Y'))
        title_text_all = 'Industry Wise New and Renew Members Report Between ' + str(
            from_date.strftime('%d/%m/%Y')) + ' to ' + str(to_date.strftime('%d/%m/%Y'))
        if report_type != 'All':
            worksheet1.merge_range('A1:Y1', title_text, merge_format)
            print_worksheet.merge_range('A1:I1', title_text, merge_format)
        else:
            worksheet1.merge_range('A1:Z1', title_text_all, merge_format)
            print_worksheet.merge_range('A1:I1', title_text_all, merge_format)

        if report_type == 'NEW':
            for i in range(len(column_name)):
                worksheet1.write_string(1, int(i), column_name[i], cell_header_format)
        elif report_type == 'RENEW':
            for i in range(len(column_name_renew)):
                worksheet1.write_string(1, int(i), column_name_renew[i], cell_header_format)
        else:
            for i in range(len(column_name_all)):
                worksheet1.write_string(1, int(i), column_name_all[i], cell_header_format)

        cell_format2 = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1})
        cell_format2.set_align('vcenter')
        cell_format2.set_rotation(90)

        print_worksheet.set_column('A:A', 4)
        print_worksheet.set_column('B:B', 10)
        print_worksheet.set_column('C:C', 10)
        print_worksheet.set_column('D:D', 20)
        print_worksheet.set_column('E:E', 10)
        print_worksheet.set_column('F:F', 8)
        print_worksheet.set_column('G:G', 8)
        print_worksheet.set_column('H:H', 8)
        print_worksheet.set_column('I:I', 15)
        if report_type == 'RENEW':
            for i in range(len(print_column_renewal)):
                if i in []:
                    print_worksheet.write_string(1, int(i), print_column_renewal[i], cell_header_format)
                else:
                    print_worksheet.write_string(1, int(i), print_column_renewal[i], cell_header_format)
        else:
            for i in range(len(print_column)):
                if i in []:
                    print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)
                else:
                    print_worksheet.write_string(1, int(i), print_column[i], cell_header_format)

        invoice_id_list = None
        if report_type == 'RENEW':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                                                                userdetail__company__industrydescription__in=industry_obj_list,
                                                                is_deleted=False).order_by('payment_date').values(
                    'membershipInvoice_id').distinct()
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                user_Payment_Type='Online',
                                                                userdetail__company__industrydescription__in=industry_obj_list,
                                                                is_deleted=False).order_by('payment_date').values(
                    'membershipInvoice_id').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date],
                                                                membershipInvoice__is_paid=True,
                                                                membershipInvoice__invoice_for__in=['RENEW',
                                                                                                    'RE-ASSOCIATE'],
                                                                is_deleted=False,
                                                                userdetail__company__industrydescription__in=industry_obj_list).order_by(
                    'payment_date').values('membershipInvoice_id').distinct()
        elif request.GET.get('report_type') == 'NEW':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW',
                    user_Payment_Type__in=['Cheque', 'Cash', 'NEFT'],
                    userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False).order_by(
                    'userdetail__membership_acceptance_date').values('membershipInvoice_id').distinct()
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', user_Payment_Type='Online',
                    userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False).order_by(
                    'userdetail__membership_acceptance_date').values('membershipInvoice_id').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(
                    userdetail__membership_acceptance_date__range=[from_date, to_date],
                    membershipInvoice__is_paid=True, membershipInvoice__invoice_for='NEW', is_deleted=False,
                    userdetail__company__industrydescription__in=industry_obj_list).values(
                    'membershipInvoice_id').distinct()

        elif request.GET.get('report_type') == 'All':
            if payment_type == 'Offline':
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                    userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False)
            elif payment_type == 'Online':
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]), membershipInvoice__is_paid=True,
                    user_Payment_Type='Online',
                    userdetail__company__industrydescription__in=industry_obj_list, is_deleted=False).values(
                    'membershipInvoice_id').distinct()
            else:
                invoice_id_list = PaymentDetails.objects.filter(
                    Q(userdetail__membership_acceptance_date__range=[from_date, to_date]) | Q(
                        payment_date__range=[from_date, to_date]),
                    userdetail__company__industrydescription__in=industry_obj_list, membershipInvoice__is_paid=True,
                    is_deleted=False).values('membershipInvoice_id').distinct()

        i = 2
        j = 1
        k = 2
        flag = ''
        for invoice_id in invoice_id_list:
            if report_type == 'RENEW':
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])

            elif report_type == 'NEW':
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])
            else:
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id['membershipInvoice_id'])

            amount_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj.id, is_deleted=False).aggregate(
                Sum('amount_paid'))
            amount = 0
            if amount_obj['amount_paid__sum']:
                amount = float(amount_obj['amount_paid__sum'])

            payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj.id, is_deleted=False).last()
            if payment_obj.userdetail.member_associate_no:
                if payment_obj.user_Payment_Type == 'Cheque':
                    flag = 'CHEQUE'
                elif payment_obj.user_Payment_Type == 'NEFT' and payment_obj.neft_transfer_id != 'Paid_Online':
                    flag = 'NEFT'
                elif payment_obj.user_Payment_Type == 'Cash':
                    flag = 'CASH'
                else:
                    flag = 'ONLINE'

                user_industry_list = payment_obj.userdetail.company.industrydescription.all()
                industry_description_list = []

                for industry_item in industry_obj_list:
                    if industry_item.id in [user_item.id for user_item in user_industry_list]:
                        industry_description_list.append(industry_item)

                worksheet1.write_number(i, 0, int(j), cell_format)
                worksheet1.write_string(i, 1, str(payment_obj.payment_date.strftime('%d/%m/%Y')), cell_format)
                worksheet1.write_string(i, 2, str(payment_obj.userdetail.membership_acceptance_date.strftime(
                    '%d/%m/%Y')) if payment_obj.userdetail.membership_acceptance_date else '', cell_format)
                worksheet1.write_string(i, 3, str(payment_obj.userdetail.membership_slab.annual_fee), cell_format)
                worksheet1.write_string(i, 4, str(payment_obj.userdetail.member_associate_no), cell_format)
                worksheet1.write_string(i, 5, str(payment_obj.userdetail.company.company_name), cell_format)
                worksheet1.write_string(i, 6,
                                        str(payment_obj.userdetail.ceo_name) if payment_obj.userdetail.ceo_name else '',
                                        cell_format)
                worksheet1.write_string(i, 7, str(
                    payment_obj.userdetail.ceo_cellno) if payment_obj.userdetail.ceo_cellno else '', cell_format)
                worksheet1.write_string(i, 8, str(
                    payment_obj.userdetail.ceo_email) if payment_obj.userdetail.ceo_email else '', cell_format)
                worksheet1.write_string(i, 9,
                                        str(payment_obj.userdetail.poc_name) if payment_obj.userdetail.poc_name else '',
                                        cell_format)
                worksheet1.write_string(i, 10, str(
                    payment_obj.userdetail.poc_contact) if payment_obj.userdetail.poc_contact else '', cell_format)
                worksheet1.write_string(i, 11, str(
                    payment_obj.userdetail.poc_email) if payment_obj.userdetail.poc_email else '', cell_format)
                worksheet1.write_string(i, 12, str(
                    payment_obj.userdetail.correspond_cellno) if payment_obj.userdetail.correspond_cellno else '',
                                        cell_format)
                worksheet1.write_string(i, 13, str(payment_obj.userdetail.correspond_address), cell_format)
                worksheet1.write_string(i, 14, str(payment_obj.userdetail.correspondcity), cell_format)
                worksheet1.write_string(i, 15, str(payment_obj.userdetail.correspond_pincode), cell_format)
                worksheet1.write_string(i, 16, str(payment_obj.userdetail.gst) if payment_obj.userdetail.gst else '',
                                        cell_format)
                worksheet1.write_string(i, 17, str(payment_obj.membershipInvoice.financial_year), cell_format)
                worksheet1.write_string(i, 18, str(payment_obj.membershipInvoice.membership_category), cell_format)
                worksheet1.write_number(i, 19, int(payment_obj.membershipInvoice.amount_payable), cell_format)
                worksheet1.write_number(i, 20, int(amount), cell_format)
                worksheet1.write_number(i, 21, int(
                    payment_obj.membershipInvoice.tax) if payment_obj.membershipInvoice.tax else '', cell_format)
                if report_type == 'NEW':
                    worksheet1.write_number(i, 22, int(
                        payment_obj.userdetail.membership_slab.entrance_fee) if payment_obj.userdetail.membership_slab.entrance_fee else '',
                                            cell_format)
                    worksheet1.write_string(i, 23, str(payment_obj.user_Payment_Type), cell_format)
                    worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                            cell_format)
                    worksheet1.write_string(i, 25, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                            cell_format)
                    worksheet1.write_string(i, 26, str(
                        payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '', cell_format)
                    worksheet1.write_string(i, 27, str(
                        ', '.join([str(item.description).strip() for item in industry_description_list])), cell_format)
                    if flag == 'CHEQUE':
                        worksheet1.write_string(i, 23, str('Cheque'), cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 25, str(payment_obj.cheque_no), cell_format)
                        worksheet1.write_string(i, 26, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 27, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)
                    elif flag == 'NEFT':
                        worksheet1.write_string(i, 23, str('NEFT'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(
                            payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)

                    elif flag == 'CASH':
                        worksheet1.write_string(i, 23, str('Cash'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)
                    else:
                        worksheet1.write_string(i, 23, str('Online'), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)
                elif report_type == 'RENEW':
                    worksheet1.write_string(i, 22,
                                            str(payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '',
                                            cell_format)
                    worksheet1.write_string(i, 23, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                            cell_format)
                    worksheet1.write_string(i, 24, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                            cell_format)
                    worksheet1.write_string(i, 25, str(
                        payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '', cell_format)
                    worksheet1.write_string(i, 26, str(
                        ', '.join([str(item.description).strip() for item in industry_description_list])), cell_format)

                    if flag == 'CHEQUE':
                        worksheet1.write_string(i, 22, str('Cheque'), cell_format)
                        worksheet1.write_string(i, 23, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.cheque_no), cell_format)
                        worksheet1.write_string(i, 25, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        worksheet1.write_string(i, 26, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)

                    elif flag == 'NEFT':
                        worksheet1.write_string(i, 22, str('NEFT'), cell_format)
                        worksheet1.write_string(i, 23, str(''), cell_format)
                        worksheet1.write_string(i, 24, str(
                            payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)

                    elif flag == 'CASH':
                        worksheet1.write_string(i, 22, str('Cash'), cell_format)
                        worksheet1.write_string(i, 23, str(''), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)

                    else:
                        worksheet1.write_string(i, 22, str('Online'), cell_format)
                        worksheet1.write_string(i, 23, str(''), cell_format)
                        worksheet1.write_string(i, 24, str(''), cell_format)
                        worksheet1.write_string(i, 25, str(''), cell_format)
                        worksheet1.write_string(i, 26, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)
                else:
                    if payment_obj.userdetail.member_associate_no:
                        worksheet1.write_number(i, 0, int(j), cell_format)
                        worksheet1.write_string(i, 1, str(payment_obj.payment_date.strftime('%d/%m/%Y')), cell_format)
                        worksheet1.write_string(i, 2, str(payment_obj.userdetail.membership_acceptance_date.strftime(
                            '%d/%m/%Y')) if payment_obj.userdetail.membership_acceptance_date else '', cell_format)
                        worksheet1.write_string(i, 3, str(payment_obj.userdetail.membership_slab.annual_fee),
                                                cell_format)
                        worksheet1.write_string(i, 4, str(
                            payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                                cell_format)
                        worksheet1.write_string(i, 5, str(
                            payment_obj.membershipInvoice.invoice_for) if payment_obj.membershipInvoice.invoice_for else '',
                                                cell_format)
                        worksheet1.write_string(i, 6, str(payment_obj.userdetail.company.company_name), cell_format)
                        worksheet1.write_string(i, 7, str(
                            payment_obj.userdetail.ceo_name) if payment_obj.userdetail.ceo_name else '', cell_format)
                        worksheet1.write_string(i, 8, str(
                            payment_obj.userdetail.ceo_cellno) if payment_obj.userdetail.ceo_cellno else '',
                                                cell_format)
                        worksheet1.write_string(i, 9, str(
                            payment_obj.userdetail.ceo_email) if payment_obj.userdetail.ceo_email else '', cell_format)
                        worksheet1.write_string(i, 10, str(
                            payment_obj.userdetail.poc_name) if payment_obj.userdetail.poc_name else '', cell_format)
                        worksheet1.write_string(i, 11, str(
                            payment_obj.userdetail.poc_contact) if payment_obj.userdetail.poc_contact else '',
                                                cell_format)
                        worksheet1.write_string(i, 12, str(
                            payment_obj.userdetail.poc_email) if payment_obj.userdetail.poc_email else '', cell_format)
                        worksheet1.write_string(i, 13, str(
                            payment_obj.userdetail.correspond_cellno) if payment_obj.userdetail.correspond_cellno else '',
                                                cell_format)
                        worksheet1.write_string(i, 14, str(payment_obj.userdetail.correspond_address), cell_format)
                        worksheet1.write_string(i, 15, str(payment_obj.userdetail.correspondcity), cell_format)
                        worksheet1.write_string(i, 16, str(payment_obj.userdetail.correspond_pincode), cell_format)
                        worksheet1.write_string(i, 17,
                                                str(payment_obj.userdetail.gst) if payment_obj.userdetail.gst else '',
                                                cell_format)
                        worksheet1.write_string(i, 18, str(payment_obj.membershipInvoice.financial_year), cell_format)
                        worksheet1.write_string(i, 19, str(payment_obj.membershipInvoice.membership_category),
                                                cell_format)
                        worksheet1.write_number(i, 20, int(payment_obj.membershipInvoice.amount_payable), cell_format)
                        worksheet1.write_number(i, 21, int(amount), cell_format)
                        worksheet1.write_number(i, 22, int(
                            payment_obj.membershipInvoice.tax) if payment_obj.membershipInvoice.tax else '',
                                                cell_format)
                        worksheet1.write_string(i, 23, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                cell_format)
                        worksheet1.write_string(i, 25, str(payment_obj.cheque_no) if payment_obj.cheque_no else '',
                                                cell_format)
                        worksheet1.write_string(i, 26, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                cell_format)
                        if flag == 'CHEQUE':
                            worksheet1.write_string(i, 23, str('Cheque'), cell_format)
                            worksheet1.write_string(i, 24, str(payment_obj.bank_name) if payment_obj.bank_name else '',
                                                    cell_format)
                            worksheet1.write_string(i, 25, str(payment_obj.cheque_no), cell_format)
                            worksheet1.write_string(i, 26, str(
                                payment_obj.cheque_date.strftime('%d/%m/%Y')) if payment_obj.cheque_date else '',
                                                    cell_format)
                        elif flag == 'NEFT':
                            worksheet1.write_string(i, 23, str('NEFT'), cell_format)
                            worksheet1.write_string(i, 24, str(''), cell_format)
                            worksheet1.write_string(i, 25, str(
                                payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                        elif flag == 'CASH':
                            worksheet1.write_string(i, 23, str('Cash'), cell_format)
                            worksheet1.write_string(i, 24, str(''), cell_format)
                            worksheet1.write_string(i, 25, str(''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                        else:
                            worksheet1.write_string(i, 23, str('Online'), cell_format)
                            worksheet1.write_string(i, 24, str(''), cell_format)
                            worksheet1.write_string(i, 25, str(''), cell_format)
                            worksheet1.write_string(i, 26, str(''), cell_format)
                        worksheet1.write_string(i, 27, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                cell_format)

                if payment_obj.userdetail.member_associate_no:
                    if report_type == 'RENEW':
                        print_worksheet.write_number(i, 0, int(j), cell_format)
                        print_worksheet.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y')) if payment_obj.payment_date else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 2, str(
                            payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 3, str(
                            payment_obj.userdetail.company.company_name) if payment_obj.userdetail.company.company_name else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 4, str(
                            payment_obj.membershipInvoice.financial_year) if payment_obj.membershipInvoice.financial_year else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 5, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        print_worksheet.write_number(i, 6, int(payment_obj.membershipInvoice.amount_payable),
                                                     cell_format)
                        print_worksheet.write_number(i, 7, int(amount), cell_format)
                        print_worksheet.write_string(i, 8, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                     cell_format)
                    else:
                        print_worksheet.write_number(i, 0, int(j), cell_format)
                        print_worksheet.write_string(i, 1, str(
                            payment_obj.payment_date.strftime('%d/%m/%Y')) if payment_obj.payment_date else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 2, str(
                            payment_obj.userdetail.membership_acceptance_date.strftime(
                                '%d/%m/%Y')) if payment_obj.userdetail.membership_acceptance_date else '', cell_format)
                        print_worksheet.write_string(i, 3, str(
                            payment_obj.userdetail.member_associate_no) if payment_obj.userdetail.member_associate_no else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 4, str(
                            payment_obj.userdetail.company.company_name) if payment_obj.userdetail.company.company_name else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 5, str(
                            payment_obj.membershipInvoice.financial_year) if payment_obj.membershipInvoice.financial_year else '',
                                                     cell_format)
                        print_worksheet.write_string(i, 6, str(
                            payment_obj.user_Payment_Type) if payment_obj.user_Payment_Type else '', cell_format)
                        print_worksheet.write_number(i, 7, int(payment_obj.membershipInvoice.amount_payable),
                                                     cell_format)
                        print_worksheet.write_number(i, 8, int(amount), cell_format)
                        print_worksheet.write_string(i, 9, str(
                            ', '.join([str(item.description).strip() for item in industry_description_list])),
                                                     cell_format)

                i = i + 1
                j = j + 1
                k = k + 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Industry Report' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | membership_industry_report | User = '
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | membership_industry_report | EXCP = ', str(traceback.print_exc())
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


# TODO cheque details datatable
@login_required(login_url='/backofficeapp/login/')
def bounce_cheque_details_datatable(request):
    try:
        dataList = []
        print 'reportapp | membershipreport.py | bounce_cheque_details_datatable'
        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[1][dir]') == 'asc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        status = request.GET.get('status')

        cheque_details_list = PaymentDetails.objects.filter(is_deleted=True, user_Payment_Type='Cheque')
        # cheque_details_list = PaymentDetails.objects.filter(is_deleted=True,user_Payment_Type='Cheque',
        #                                                     is_cheque_bounce=True,membershipInvoice__is_paid=False)
        if searchTxt:
            cheque_details_list = cheque_details_list.filter(Q(userdetail__member_associate_no__icontains=searchTxt) |
                                                             Q(userdetail__company__company_name__icontains=searchTxt))
        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%d/%m/%Y').date()
            to_date = datetime.strptime(to_date, '%d/%m/%Y').date()
            cheque_details_list = cheque_details_list.filter(payment_date__range=[from_date, to_date])

        if status != 'All':
            if status == 'not_paid':
                cheque_details_list = cheque_details_list.filter(membershipInvoice__is_paid=False)
            if status == 'paid':
                cheque_details_list = cheque_details_list.filter(membershipInvoice__is_paid=True)
        # else:
        #     cheque_details_list = PaymentDetails.objects.filter(is_deleted=True, user_Payment_Type='Cheque',
        #                                                         is_cheque_bounce=True)

        cheque_details_list = cheque_details_list.order_by('-payment_date')
        total_record = cheque_details_list.count()
        if length != -1:
            cheque_details_list = cheque_details_list[start:length]
        else:
            cheque_details_list = cheque_details_list[::-1]
        i = 1
        for cheque_obj in cheque_details_list:
            if cheque_obj.cheque_date:
                cheque_date = str(cheque_obj.cheque_date.strftime('%d/%m/%Y'))
            else:
                cheque_date = ''
            if cheque_obj.payment_date:
                payment_date = str(cheque_obj.payment_date.strftime('%d/%m/%Y'))
            else:
                payment_date = ''
            tempList = []
            if cheque_obj.membershipInvoice.is_paid:
                status = 'Paid'
            else:
                status = 'Not Paid'
            tempList.append(i)
            tempList.append(payment_date)
            tempList.append(cheque_obj.userdetail.member_associate_no)
            tempList.append(cheque_obj.userdetail.company.company_name)
            tempList.append(cheque_obj.cheque_no)
            tempList.append(cheque_date)
            tempList.append(cheque_obj.bank_name)
            tempList.append(str(cheque_obj.amount_paid))
            tempList.append(status)
            dataList.append(tempList)
            i = i + 1
        total_records = len(dataList)
        total_record = total_record
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print '\nexception ', traceback.print_exc()
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
def download_cheque_details(request):
    try:
        print "reportapp | membership_report.py | download_cheque_details "
        requested_val = request.GET.get('requested_value')
        from_date = (datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y'))
        to_date = (datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y'))
        payment_status = request.GET.get('payment_status')
        cheque_details_list = None

        if from_date > to_date:
            data = {'success': 'invalid_date'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            if payment_status != 'All':
                cheque_details_list = PaymentDetails.objects.filter(is_deleted=True, user_Payment_Type='Cheque',
                                                                    membershipInvoice__is_paid=False if payment_status == 'not_paid' else True,
                                                                    payment_date__range=[from_date, to_date])
            else:
                cheque_details_list = PaymentDetails.objects.filter(is_deleted=True, user_Payment_Type='Cheque',
                                                                    payment_date__range=[from_date, to_date])
        if cheque_details_list:
            data = {"success": "true"}
        else:
            data = {"success": "no data"}
    except Exception, e:
        print "\nException In | membership_report.py | download_cheque_details EXCE =", str(traceback.print_exc())
        data = {"success": "false"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def download_cheque_detail_excel(request):
    try:
        print '\nRequest IN | membership_report.py | download_cheque_detail_excel | User = '
        requested_val = request.GET.get('requested_value')
        from_date = (datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y'))
        to_date = (datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y'))
        payment_status = request.GET.get('payment_status')

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Cheque Bounce Report')
        workbook.formats[0].set_font_size(10)
        workbook.formats[0].set_border(1)
        workbook.formats[0].set_text_wrap()
        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter',
             'border_color': '#000000'})
        cell_format = workbook.add_format({'font_size': 10, 'border': 1, 'text_wrap': True, 'border_color': '#000000'})
        worksheet1.set_column('A:A', 2)
        worksheet1.set_column('B:B', 10)
        worksheet1.set_column('C:C', 20)
        worksheet1.set_column('D:D', 18)
        worksheet1.set_column('E:E', 7)
        worksheet1.set_column('F:F', 7)
        worksheet1.set_column('G:G', 7)
        worksheet1.set_column('H:H', 7)

        title_text = 'Cheque Bounce Details Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
            to_date.strftime('%d/%m/%Y'))
        worksheet1.merge_range('A1:M1', title_text, merge_format)
        # cell_format2 = workbook.add_format({'font_color': 'red', 'font_size': 10, 'border': 1, 'text_wrap': True})
        # date_format = workbook.add_format({'font_color': 'red', 'font_size': 10, 'border': 1, 'text_wrap': True})

        column_name = ['Sr.No', 'Membership No', 'Company Name', 'Email', 'Subscription Amount', 'Entrance Fee',
                       'GST Amount', 'Total Payable', 'Payment Date', 'Chq Amount', 'Chq Date', 'Cheque No',
                       'Bank Name',
                       'Status']

        for i in range(len(column_name)):
            worksheet1.write_string(1, int(i), column_name[i], cell_header_format)
        i = 2
        j = 1

        cheque_obj = None
        if payment_status != 'All':
            cheque_obj = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date], is_deleted=True,
                                                       user_Payment_Type='Cheque',
                                                       membershipInvoice__is_paid=False if payment_status == 'not_paid' else True)
        else:
            cheque_obj = PaymentDetails.objects.filter(payment_date__range=[from_date, to_date], is_deleted=True,
                                                       user_Payment_Type='Cheque')
        for bounce_cheque_obj in cheque_obj:
            ceo_email = str(bounce_cheque_obj.userdetail.ceo_email if bounce_cheque_obj.userdetail.ceo_email else '')
            personal_email = str(bounce_cheque_obj.userdetail.person_email if
                                 bounce_cheque_obj.userdetail.person_email else '')
            if bounce_cheque_obj.userdetail.company.hoddetail:
                if bounce_cheque_obj.userdetail.company.hoddetail.finance_email:
                    f_email = str(bounce_cheque_obj.userdetail.company.hoddetail.finance_email)
                else:
                    f_email = ''
            else:
                f_email = ''
            finance_email = f_email
            correspond_email = str(bounce_cheque_obj.userdetail.correspond_email if
                                   bounce_cheque_obj.userdetail.correspond_email else '')
            poc_email = str(bounce_cheque_obj.userdetail.poc_email if bounce_cheque_obj.userdetail.poc_email else '')
            individual_email = str(str(ceo_email) + ';') if ceo_email else '' + str(
                str(personal_email) + ';') if personal_email else ''
            company_email = str(str(finance_email) + ';') if finance_email else '' + str(
                str(poc_email) + ';') if poc_email else '' + str(
                str(correspond_email) + ';') if correspond_email else ''
            if bounce_cheque_obj.userdetail.enroll_type == 'CO':
                email = company_email
            else:
                email = individual_email
            worksheet1.write_string(i, 0, str(j), cell_format)
            worksheet1.write_string(i, 1, str(bounce_cheque_obj.userdetail.member_associate_no), cell_format)
            worksheet1.write_string(i, 2, str(bounce_cheque_obj.userdetail.company.company_name), cell_format)
            worksheet1.write_string(i, 3, email, cell_format)
            worksheet1.write_string(i, 4, str(int(round(bounce_cheque_obj.membershipInvoice.subscription_charges, 0))),
                                    cell_format)
            worksheet1.write_string(i, 5, str(int(round(bounce_cheque_obj.membershipInvoice.entrance_fees, 0))),
                                    cell_format)
            worksheet1.write_string(i, 6, str(int(round(bounce_cheque_obj.membershipInvoice.tax, 0))), cell_format)
            worksheet1.write_string(i, 7, str(int(round(bounce_cheque_obj.amount_payable, 0))), cell_format)
            worksheet1.write_string(i, 8, str(str(bounce_cheque_obj.payment_date.strftime('%d/%m/%Y'))), cell_format)
            worksheet1.write_string(i, 9, str(int(round(bounce_cheque_obj.amount_paid, 0))), cell_format)
            worksheet1.write_string(i, 10, str(
                str(bounce_cheque_obj.cheque_date.strftime('%d/%m/%Y'))) if bounce_cheque_obj.cheque_date else '',
                                    cell_format)
            worksheet1.write_string(i, 11, str(bounce_cheque_obj.cheque_no) if bounce_cheque_obj.cheque_no else '',
                                    cell_format)
            worksheet1.write_string(i, 12, str(bounce_cheque_obj.bank_name) if bounce_cheque_obj.bank_name else '',
                                    cell_format)
            worksheet1.write_string(i, 13, str('Paid') if bounce_cheque_obj.membershipInvoice.is_paid else 'Not Paid',
                                    cell_format)
            i = i + 1
            j = j + 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Cheque_Bounce_Report' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | downloadcheque_detail_excel | User = '
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | downloadcheque_detail_excel | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
def comparative_analysis_datatable(request):
    try:
        data_list = []
        print '\nRequest IN | membership_report.py | comparative_analysis_datatable | User = ', request.user
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

        i = 5
        date_list = []
        current_year = datetime.now().date().year + 1

        while i > 0:
            date_list.append(str(current_year - 1) + '-' + str(current_year))
            current_year = current_year - 1
            i = i - 1

        counter = 1
        for year_item in date_list:
            temp_list = []
            invoice_list = MembershipInvoice.objects.filter(is_paid=True, financial_year=year_item, is_deleted=False)
            temp_list.append(counter)
            temp_list.append(year_item)
            temp_list.append(invoice_list.filter(invoice_for='NEW').count())
            temp_list.append(invoice_list.filter(invoice_for='RENEW').count())
            temp_list.append(invoice_list.filter(invoice_for='RE-ASSOCIATE').count())
            data_list.append(temp_list)
            counter = counter + 1

        total_records = len(data_list)
        total_record = total_records
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': data_list}
    except Exception, e:
        print '\nException IN | membership_report.py | comparative_analysis_datatable | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def download_comparative_analysis_excel(request):
    try:
        print '\nRequest IN | membership_report.py | download_comparative_analysis_excel | User = ', request.user

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Comparative Analysis Report')
        merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format = workbook.add_format({'font_size': 10, 'border': 1, 'text_wrap': False})

        title_text = 'Comparative Analysis Report'
        worksheet1.merge_range('A1:E1', title_text, merge_format)

        column_name = ['Sr.No.', 'Year', 'New Members', 'Renew Members', 'Re-Associate Members']

        for i in range(len(column_name)):
            worksheet1.write_string(1, int(i), column_name[i], cell_header_format)

        i = 5
        date_list = []
        current_year = datetime.now().date().year + 1

        while i > 0:
            date_list.append(str(current_year - 1) + '-' + str(current_year))
            current_year = current_year - 1
            i = i - 1

        i = 2
        counter = 1
        for year_item in date_list:
            invoice_list = MembershipInvoice.objects.filter(is_paid=True, financial_year=year_item, is_deleted=False)
            worksheet1.write_number(i, 0, counter, cell_format)
            worksheet1.write_string(i, 1, str(year_item), cell_format)
            worksheet1.write_number(i, 2, invoice_list.filter(invoice_for='NEW').count(), cell_format)
            worksheet1.write_number(i, 3, invoice_list.filter(invoice_for='RENEW').count(), cell_format)
            worksheet1.write_number(i, 4, invoice_list.filter(invoice_for='RE-ASSOCIATE').count(), cell_format)

            i = i + 1
            counter = counter + 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Comparative_Analysis' + str(
            datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | membership_report.py | download_comparative_analysis_excel | User = ', request.user
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | download_comparative_analysis_excel | EXCP = ', str(
            traceback.print_exc())
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def get_member_report_data(request):
    try:
        print '\nRequest IN | membership_report.py | get_member_report_data | User = ', request.user
        current_year = str(datetime.now().year) + '-' + str(datetime.now().year + 1)
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Sheet1')
        cell_header_format = workbook.add_format(
            {'font_size': 8, 'border': 1, 'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        cell_format = workbook.add_format({'font_size': 10, 'border': 1, 'text_wrap': False})
        date_format = workbook.add_format(
            {'num_format': 'dd/mm/yyyy', 'font_size': 10, 'border': 1, 'text_wrap': False})

        column_name = ['Sr #', 'Slab', 'Company Name', 'Acceptance Date', 'User Type', 'Status', 'Financial Year',
                       'Payment Date', 'Turnover Range', 'Employee Range', 'Total Paid', 'Industry']

        for i in range(len(column_name)):
            worksheet1.write_string(0, int(i), column_name[i], cell_header_format)

        member_list = UserDetail.objects.filter(payment_method='Confirmed',
                                                is_deleted=False)

        i = 1
        for member_obj in member_list:
            if member_obj.user_type != 'Life Membership':
                invoice_list = MembershipInvoice.objects.filter(financial_year=current_year,
                                                                userdetail=member_obj,
                                                                is_deleted=False)
                if invoice_list and invoice_list.count() == 1:
                    invoice_obj = MembershipInvoice.objects.get(id=invoice_list[0].id)

                    paid_amount = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                                is_deleted=False).aggregate(
                        amount_paid_sum=Sum('amount_paid'))
                    payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj, is_deleted=False).last()

                    worksheet1.write_number(i, 0, i, cell_format)
                    worksheet1.write_number(i, 1, float(invoice_obj.membership_slab.annual_fee), cell_format)
                    worksheet1.write_string(i, 2, str(member_obj.company.company_name), cell_format)

                    if member_obj.membership_acceptance_date:
                        worksheet1.write_datetime(i, 3, member_obj.membership_acceptance_date, date_format)
                    else:
                        worksheet1.write_string(i, 3, str(''), cell_format)
                    worksheet1.write_string(i, 4, str(member_obj.user_type), cell_format)

                    if member_obj.user_type != 'Life Membership':
                        if invoice_obj.is_paid and invoice_obj.invoice_for in ['RENEW', 'RE-ASSOCIATE']:
                            worksheet1.write_string(i, 5, str('RENEWED'), cell_format)
                        elif invoice_obj.is_paid and invoice_obj.invoice_for == 'NEW':
                            worksheet1.write_string(i, 5, str('NEW'), cell_format)
                        elif not invoice_obj.is_paid and invoice_obj.invoice_for != 'NEW':
                            worksheet1.write_string(i, 5, str('NOT RENEWED'), cell_format)
                        elif not invoice_obj.is_paid and invoice_obj.invoice_for == 'NEW':
                            worksheet1.write_string(i, 5, str('NOT NEW'), cell_format)
                    else:
                        worksheet1.write_string(i, 5, str('LIFE MEMBER'), cell_format)
                    worksheet1.write_string(i, 6, str(invoice_obj.financial_year), cell_format)

                    if payment_obj and payment_obj.payment_date:
                        worksheet1.write_datetime(i, 7, payment_obj.payment_date, date_format)
                    else:
                        worksheet1.write_string(i, 7, str(''), cell_format)

                    if invoice_obj.turnover_range:
                        worksheet1.write_string(i, 8, str(invoice_obj.get_turnover_range_display()), cell_format)
                    else:
                        worksheet1.write_string(i, 8, str(member_obj.annual_turnover_rupees), cell_format)

                    if invoice_obj.employee_range:
                        worksheet1.write_string(i, 9, str(invoice_obj.get_employee_range_display()), cell_format)
                    else:
                        worksheet1.write_string(i, 9, str(member_obj.company.total_employees), cell_format)

                    worksheet1.write_number(i, 10, float(paid_amount['amount_paid_sum']) if paid_amount[
                        'amount_paid_sum'] else 0, cell_format)
                    worksheet1.write_string(i, 11, str(', '.join(
                        [str(item.description).strip() for item in member_obj.company.industrydescription.all()])),
                                            cell_format)

                    i = i + 1

                elif invoice_list and invoice_list.count() > 1:
                    invoice_obj = None
                    for invoice_item in invoice_list:
                        if invoice_item.is_paid:
                            invoice_obj = invoice_item
                            break
                    if invoice_obj:
                        paid_amount = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                                    is_deleted=False).aggregate(
                            amount_paid_sum=Sum('amount_paid'))
                        payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj,
                                                                    is_deleted=False).last()

                        worksheet1.write_number(i, 0, i, cell_format)
                        worksheet1.write_number(i, 1, float(invoice_obj.membership_slab.annual_fee), cell_format)
                        worksheet1.write_string(i, 2, str(member_obj.company.company_name), cell_format)

                        if member_obj.membership_acceptance_date:
                            worksheet1.write_datetime(i, 3, member_obj.membership_acceptance_date, date_format)
                        else:
                            worksheet1.write_string(i, 3, str(''), cell_format)

                        worksheet1.write_string(i, 4, str(member_obj.user_type), cell_format)

                        if member_obj.user_type != 'Life Membership':
                            if invoice_obj.is_paid and invoice_obj.invoice_for in ['RENEW', 'RE-ASSOCIATE']:
                                worksheet1.write_string(i, 5, str('RENEWED'), cell_format)
                            elif invoice_obj.is_paid and invoice_obj.invoice_for == 'NEW':
                                worksheet1.write_string(i, 5, str('NEW'), cell_format)
                            elif not invoice_obj.is_paid and invoice_obj.invoice_for != 'NEW':
                                worksheet1.write_string(i, 5, str('NOT RENEWED'), cell_format)
                            elif not invoice_obj.is_paid and invoice_obj.invoice_for == 'NEW':
                                worksheet1.write_string(i, 5, str('NOT NEW'), cell_format)
                        else:
                            worksheet1.write_string(i, 5, str('LIFE MEMBER'), cell_format)
                        worksheet1.write_string(i, 6, str(invoice_obj.financial_year), cell_format)

                        if payment_obj and payment_obj.payment_date:
                            worksheet1.write_datetime(i, 7, payment_obj.payment_date, date_format)
                        else:
                            worksheet1.write_string(i, 7, str(''), cell_format)

                        if invoice_obj.turnover_range:
                            worksheet1.write_string(i, 8, str(invoice_obj.get_turnover_range_display()), cell_format)
                        else:
                            worksheet1.write_string(i, 8, str(member_obj.annual_turnover_rupees), cell_format)

                        if invoice_obj.employee_range:
                            worksheet1.write_string(i, 9, str(invoice_obj.get_employee_range_display()), cell_format)
                        else:
                            worksheet1.write_string(i, 9, str(member_obj.company.total_employees), cell_format)

                        worksheet1.write_number(i, 10, float(paid_amount['amount_paid_sum']) if paid_amount[
                            'amount_paid_sum'] else 0, cell_format)
                        worksheet1.write_string(i, 11, str(', '.join(
                            [str(item.description).strip() for item in member_obj.company.industrydescription.all()])),
                                                cell_format)

                        i = i + 1
                    else:
                        worksheet1.write_number(i, 0, i, cell_format)
                        worksheet1.write_number(i, 1, float(member_obj.membership_slab.annual_fee), cell_format)
                        worksheet1.write_string(i, 2, str(member_obj.company.company_name), cell_format)

                        if member_obj.membership_acceptance_date:
                            worksheet1.write_datetime(i, 3, member_obj.membership_acceptance_date, date_format)
                        else:
                            worksheet1.write_string(i, 3, str(''), cell_format)

                        worksheet1.write_string(i, 4, str(member_obj.user_type), cell_format)
                        worksheet1.write_string(i, 5, str('NOT RENEWED'), cell_format)
                        worksheet1.write_string(i, 6, str(current_year), cell_format)
                        worksheet1.write_string(i, 7, '', cell_format)
                        worksheet1.write_string(i, 8, str(member_obj.annual_turnover_rupees), cell_format)
                        worksheet1.write_string(i, 9, str(member_obj.company.total_employees), cell_format)
                        worksheet1.write_number(i, 10, float(0), cell_format)
                        worksheet1.write_string(i, 11, str(', '.join(
                            [str(item.description).strip() for item in member_obj.company.industrydescription.all()])),
                                                cell_format)

                        i = i + 1
                else:
                    worksheet1.write_number(i, 0, i, cell_format)
                    worksheet1.write_number(i, 1, float(member_obj.membership_slab.annual_fee), cell_format)
                    worksheet1.write_string(i, 2, str(member_obj.company.company_name), cell_format)

                    if member_obj.membership_acceptance_date:
                        worksheet1.write_datetime(i, 3, member_obj.membership_acceptance_date, date_format)
                    else:
                        worksheet1.write_string(i, 3, str(''), cell_format)

                    worksheet1.write_string(i, 4, str(member_obj.user_type), cell_format)
                    worksheet1.write_string(i, 5, str('NOT RENEWED'), cell_format)
                    worksheet1.write_string(i, 6, str(current_year), cell_format)
                    worksheet1.write_string(i, 7, '', cell_format)
                    worksheet1.write_string(i, 8, str(member_obj.annual_turnover_rupees), cell_format)
                    worksheet1.write_string(i, 9, str(member_obj.company.total_employees), cell_format)
                    worksheet1.write_number(i, 10, float(0), cell_format)
                    worksheet1.write_string(i, 11, str(', '.join(
                        [str(item.description).strip() for item in member_obj.company.industrydescription.all()])),
                                            cell_format)

                    i = i + 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Report_Data.xlsx'
        print '\nResponse OUT | membership_report.py | get_member_report_data | User = ', request.user
        return response
    except Exception, e:
        print '\nException IN | membership_report.py | get_member_report_data | EXCP = ', str(traceback.print_exc())
        data = {'success': 'false'}
        log.debug('Error = {0}\n'.format(e))
    return HttpResponse(json.dumps(data), content_type='application/json')
