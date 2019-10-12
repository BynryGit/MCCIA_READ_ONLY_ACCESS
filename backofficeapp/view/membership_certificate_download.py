
# System Packages

import traceback, xlsxwriter, os, logging
from django.contrib.sites.models import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from django.http import HttpResponse, HttpResponseServerError
from datetime import datetime, timedelta, time
from zipfile import ZipFile
from django.conf import settings
from django.db import transaction
charset = 'utf-8'

# User Models

from membershipapp.models import UserDetail, MembershipInvoice, PaymentDetails
from adminapp.models import NameSign
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required
from wkhtmltopdf.views import PDFTemplateResponse


from django.template.loader import get_template
import datetime



try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


def download_membership_certificate_system (request):
    return render(request, 'backoffice/membership/download_membership_certificate_system.html')


@csrf_exempt
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Certificate Download'],login_url='/backofficeapp/login/',raise_exception=True)
def download_certificate_file(request):
    try:
        print '\nRequest IN | membership_certificate_download.py | download_certificate_file | User = ', request.user

        data={}
        file_paths = []
        output_list = []
        payment_obj = None


        folder = str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf'

        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(e)

        log.debug('Pass'.format(request.GET))
        log.debug('Error = {0}\n'.format(request.GET))

        dg_obj = NameSign.objects.get(is_deleted=False, designation=1)
        president_obj = NameSign.objects.get(is_deleted=False, designation=0)

        if request.GET.get('select_type') == 'new':
            acceptance_from_date = datetime.datetime.strptime(str(request.GET.get('acceptance_from')), '%d/%m/%Y').date()
            acceptance_to_date = (
                        datetime.datetime.strptime(str(request.GET.get('acceptance_to')), '%d/%m/%Y') + timedelta(days=1)).date()
            output_list = UserDetail.objects.filter(
                membership_acceptance_date__range=[acceptance_from_date, acceptance_to_date], is_deleted=False)
        else:
            payment_from_date = datetime.datetime.strptime(str(request.GET.get('payment_from')), '%d/%m/%Y').date()
            payment_to_date = (
                        datetime.datetime.strptime(str(request.GET.get('payment_to')), '%d/%m/%Y') + timedelta(days=1)).date()
            output_list = PaymentDetails.objects.filter(
                    payment_date__range=[payment_from_date, payment_to_date], membershipInvoice__is_paid=True,
                    membershipInvoice__invoice_for__in=['RENEW', 'RE-ASSOCIATE']
                    , is_deleted=False).values('membershipInvoice_id').distinct()

        excel_file_data_list = []
        for item in output_list:
            if request.GET.get('select_type') == 'new':
                invoice_obj = MembershipInvoice.objects.filter(userdetail=item, is_paid=True, invoice_for='NEW', is_deleted=False).last()
                if invoice_obj:
                    show_date = invoice_obj.userdetail.membership_acceptance_date
                    date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')
            else:
                invoice_obj = MembershipInvoice.objects.get(id=item['membershipInvoice_id'])
                payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj, is_deleted=False).last()
                show_date = payment_obj.payment_date
                date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')

            if invoice_obj:
                excel_file_data_list.append(invoice_obj)

            log.debug('Error = {0}\n'.format(invoice_obj))
            if invoice_obj:
                if invoice_obj.userdetail.user_type == 'Associate':

                    data = {
                        'company_name': str(invoice_obj.userdetail.company.company_name),
                        'membership_no': str(invoice_obj.userdetail.member_associate_no),
                        'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                        'for_year': str(invoice_obj.financial_year),
                        'type': 'Associate',
                        'dg_sign': 'https://'+str(get_current_site(request)) + '/' + 'sitemedia/'+str(dg_obj.sign),
                        'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(president_obj.sign),
                        'president_obj': president_obj,
                        'dg_obj':dg_obj
                    }
                    log.debug('Error = {0}\n'.format(data))
                    create_pdf(request, data)
                elif invoice_obj.userdetail.user_type == 'Member':
                    data = {
                        'company_name': str(invoice_obj.userdetail.company.company_name),
                        'membership_no': str(invoice_obj.userdetail.member_associate_no),
                        'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                        'for_year': str(invoice_obj.financial_year),
                        'type': 'Member',
                        'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                        'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(
                            president_obj.sign),
                        'president_obj': president_obj,
                        'dg_obj': dg_obj
                    }
                    create_pdf(request,data)
                elif invoice_obj.userdetail.user_type == 'Life Membership':
                    if 'Patron' in invoice_obj.userdetail.membership_slab.slab:
                        data = {
                            'company_name': str(invoice_obj.userdetail.company.company_name),
                            'membership_no': str(invoice_obj.userdetail.member_associate_no),
                            'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                            'type':'Patron',
                            'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                            'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(
                                president_obj.sign),
                            'president_obj': president_obj,
                            'dg_obj': dg_obj

                        }
                        create_pdf(request,data)
                    elif 'Benefactor' in invoice_obj.userdetail.membership_slab.slab:
                        data = {
                            'company_name': str(invoice_obj.userdetail.company.company_name),
                            'membership_no': str(invoice_obj.userdetail.member_associate_no),
                            'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                            'type': 'Benefactor',
                            'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                            'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(
                                president_obj.sign),
                            'president_obj': president_obj,
                            'dg_obj': dg_obj
                        }
                        create_pdf(request,data)
                    else:
                        data = {
                            'company_name': str(invoice_obj.userdetail.company.company_name),
                            'membership_no': str(invoice_obj.userdetail.member_associate_no),
                            'payment_date': date_obj if request.GET.get(
                                'select_type') == 'new' else date_obj,
                            'type': 'Life-Member',
                            'dg_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(dg_obj.sign),
                            'president_sign': 'https://' + str(get_current_site(request)) + '/' + 'sitemedia/' + str(
                                president_obj.sign),
                            'president_obj': president_obj,
                            'dg_obj': dg_obj
                        }
                        create_pdf(request,data)

        # Check if zip file exist, if not create one & write all PDF from PDF Folder
        try:

            os.remove(str(settings.BASE_DIR) + "/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip")
        except OSError:
            pass

        directory = str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf'
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append({
                    'file_path': filepath,
                    'file_name': filename
                })


        # workbook = xlsxwriter.Workbook(str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf/Certificate_Address_Excel.xlsx')
        # worksheet1 = workbook.add_worksheet('Name_Address_Sheet')
        #
        # column_name = ['Company Name', 'CEO Name', 'CEO Contact', 'Other Contact', 'Address', 'City', 'Pin Code']
        #
        # for i in range(len(column_name)):
        #     worksheet1.write_string(0, int(i), column_name[i])
        #
        # i = 1
        # for invoice_obj in excel_file_data_list:
        #     worksheet1.write_string(i, 0, str(invoice_obj.userdetail.company.company_name))
        #     worksheet1.write_string(i, 1, str(invoice_obj.userdetail.ceo_name))
        #     worksheet1.write_string(i, 2, str(invoice_obj.userdetail.ceo_cellno if invoice_obj.userdetail.ceo_cellno else ''))
        #     worksheet1.write_string(i, 3, str(
        #         invoice_obj.userdetail.correspond_std1 if invoice_obj.userdetail.correspond_std1 else '') + ' ' + str(
        #         invoice_obj.userdetail.correspond_landline1 if invoice_obj.userdetail.correspond_landline1 else ''))
        #     worksheet1.write_string(i, 4, str(invoice_obj.userdetail.correspond_address))
        #     worksheet1.write_string(i, 5, str(invoice_obj.userdetail.correspondcity.city_name if invoice_obj.userdetail.correspondcity else ''))
        #     worksheet1.write_string(i, 6,invoice_obj.userdetail.correspond_pincode if invoice_obj.userdetail.correspond_pincode else '')
        #
        #     i = i + 1
        #
        # workbook.close()
        #
        # file_paths.append({
        #
        #     'file_path': str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf/Certificate_Address_Excel.xlsx',
        #     'file_name': 'Certificate_Address_Excel.xlsx'
        # })
        with ZipFile(str(
                settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip',
                     'w') as zip:
            for file_item in file_paths:
                zip.write(file_item['file_path'], file_item['file_name'])

        record_list = []
        for invoice_obje in excel_file_data_list:
            data = {
                'company_name': str(invoice_obje.userdetail.company.company_name),
                'correspond_address': str(invoice_obje.userdetail.correspond_address),
                'City_no': str(invoice_obje.userdetail.correspondcity) + '/' + str(
                    invoice_obje.userdetail.correspond_pincode),
                'cell_no': str(invoice_obje.userdetail.correspond_landline1) + ',' + str(
                    invoice_obje.userdetail.person_cellno),
            }
            record_list.append(data)

        tpl = get_template('backoffice/membership/certificate_courier_page.html')
        response = PDFTemplateResponse(
            request=request,
            template=tpl,
            context={'record_list': record_list},
            filename='Address_for_courier' + '.pdf',
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
        with open(str(settings.BASE_DIR) + "/site-static/membership_certificates/membership_certificate_pdf/" + str(
                response.filename), "wb") as f:
            f.write(response.rendered_content)
        print '\nResponse OUT | membership_certificate_download.py | download_certificate_file_manual | User = ', request.user

        file_paths.append({
            'file_path': str(
                settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf/Address_for_courier.pdf',
            'file_name': 'Address_for_courier.pdf'
        })

        with ZipFile(str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip', 'w') as zip:
            for file_item in file_paths:
                zip.write(file_item['file_path'], file_item['file_name'])

        print '\nResponse OUT | membership_certificate_download.py | download_certificate_file | User = ', request.user

        response = HttpResponse(open(str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip', 'rb'), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=Membership_Certificate.zip'
        return response
    except Exception as exc:
        print '\nException | membership_certificate_download.py | download_certificate_file | EXCP = ', str(traceback.print_exc())
        log.debug('Error = {0}\n'.format(exc))
        log.debug('Error = {0}\n'.format(str(traceback.print_exc())))
        log.exception("message")
        return HttpResponseServerError()


def create_pdf(request, data):
    try:
        # data['company_name'] = str(data['company_name']).strip().title()

        if '/' in data['company_name']:
            data['company_name'] = str(data['company_name']).replace('/', '-')
            data['company_name'] = str(data['company_name']).strip()

        response = None
        if data['type'] == 'Associate':
            tpl = get_template('backoffice/membership/associate_yearly.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context=data,
                filename=str(data['company_name']) +'.pdf',
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
        elif data['type'] == 'Member':
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
        elif data['type'] == 'Patron':
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
        elif data['type'] == 'Benefactor':
            tpl = get_template('backoffice/membership/benefactor_life_membership.html')
            response = PDFTemplateResponse(
                request=data,
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
        elif data['type'] == 'Life-Member':
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

        with open(str(settings.BASE_DIR) + "/site-static/membership_certificates/membership_certificate_pdf/"+str(response.filename), "wb") as f:
            f.write(response.rendered_content)
        return True
    except Exception, e:
        print str(traceback.print_exc())
        return False


@transaction.atomic
@csrf_exempt
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Certificate Download'],login_url='/backofficeapp/login/',raise_exception=True)
def download_certificate_file_manual(request):
    try:
        print '\nRequest IN | membership_certificate_download.py | download_certificate_file_manual | User = ', request.user

        data={}
        file_paths = []
        output_list = []
        payment_obj = None

        folder = str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf'

        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(e)

        log.debug('Pass'.format(request.GET))
        log.debug('Error = {0}\n'.format(request.GET))


        if request.GET.get('select_type') == 'new':
            acceptance_from_date_manual = datetime.datetime.strptime(str(request.GET.get('acceptance_from_manual')), '%d/%m/%Y').date()
            acceptance_to_date_manual= (
                        datetime.datetime.strptime(str(request.GET.get('acceptance_to_manual')), '%d/%m/%Y') + timedelta(days=1)).date()
            output_list = UserDetail.objects.filter(
                membership_acceptance_date__range=[acceptance_from_date_manual, acceptance_to_date_manual], is_deleted=False).order_by("company__company_name")
        else:
            payment_from_date_manual = datetime.datetime.strptime(str(request.GET.get('payment_from_manual')), '%d/%m/%Y').date()
            payment_to_date_manual = (
                        datetime.datetime.strptime(str(request.GET.get('payment_to_manual')), '%d/%m/%Y') + timedelta(days=1)).date()
            output_list = PaymentDetails.objects.filter(
                    payment_date__range=[payment_from_date_manual, payment_to_date_manual], membershipInvoice__is_paid=True,
                    membershipInvoice__invoice_for__in=['RENEW', 'RE-ASSOCIATE']
                    , is_deleted=False).values('membershipInvoice_id').distinct().order_by("userdetail__company__company_name")

        excel_file_data_list = []
        for item in output_list:
            if request.GET.get('select_type') == 'new':
                invoice_obj = MembershipInvoice.objects.filter(userdetail=item, is_paid=True, invoice_for='NEW', is_deleted=False).last()
                if invoice_obj:
                    show_date = invoice_obj.userdetail.membership_acceptance_date
                    date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')
            else:
                invoice_obj = MembershipInvoice.objects.get(id=item['membershipInvoice_id'])
                payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_obj, is_deleted=False).last()
                show_date = payment_obj.payment_date
                date_obj = datetime.datetime.strftime(show_date, '%d/%m/%Y')

            if invoice_obj:
                excel_file_data_list.append(invoice_obj)

            log.debug('Error = {0}\n'.format(invoice_obj))
            if invoice_obj:
                if invoice_obj.userdetail.user_type == 'Associate':

                    data = {
                        'company_name': str(invoice_obj.userdetail.company.company_name),
                        'membership_no': str(invoice_obj.userdetail.member_associate_no),
                        'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                        'for_year': str(invoice_obj.financial_year),
                        'type': 'Associate'
                    }
                    log.debug('Error = {0}\n'.format(data))
                    create_pdf_manual(request, data)
                elif invoice_obj.userdetail.user_type == 'Member':
                    data = {
                        'company_name': str(invoice_obj.userdetail.company.company_name),
                        'membership_no': str(invoice_obj.userdetail.member_associate_no),
                        'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                        'for_year': str(invoice_obj.financial_year),
                        'type': 'Member'

                    }
                    create_pdf_manual(request,data)
                elif invoice_obj.userdetail.user_type == 'Life Membership':
                    if 'Patron' in invoice_obj.userdetail.membership_slab.slab:
                        data = {
                            'company_name': str(invoice_obj.userdetail.company.company_name),
                            'membership_no': str(invoice_obj.userdetail.member_associate_no),
                            'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                            'type':'Patron'
                        }
                        create_pdf_manual(request,data)
                    elif 'Benefactor' in invoice_obj.userdetail.membership_slab.slab:
                        data = {
                            'company_name': str(invoice_obj.userdetail.company.company_name),
                            'membership_no': str(invoice_obj.userdetail.member_associate_no),
                            'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                            'type': 'Benefactor'
                        }
                        create_pdf_manual(request,data)
                    else:
                        data = {
                            'company_name': str(invoice_obj.userdetail.company.company_name),
                            'membership_no': str(invoice_obj.userdetail.member_associate_no),
                            'payment_date': date_obj if request.GET.get('select_type') == 'new' else date_obj,
                            'type': 'Life-Member'
                        }
                        create_pdf_manual(request,data)

        # Check if zip file exist, if not create one & write all PDF from PDF Folder
        try:

            os.remove(str(settings.BASE_DIR) + "/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip")
        except OSError:
            pass

        directory = str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf'
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append({
                    'file_path': filepath,
                    'file_name': filename
                })

        

        with ZipFile(str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip', 'w') as zip:
            for file_item in file_paths:
                zip.write(file_item['file_path'], file_item['file_name'])

        record_list = []
        for invoice_obje in excel_file_data_list:
            if invoice_obje.userdetail.poc_contact and invoice_obje.userdetail.correspond_landline1 and invoice_obje.userdetail.correspond_cellno:
                phone_number = str(invoice_obje.userdetail.poc_contact) + ',' + str(
                    invoice_obje.userdetail.correspond_landline1) + ',' + str(invoice_obje.userdetail.correspond_cellno)
            elif invoice_obje.userdetail.poc_contact and invoice_obje.userdetail.correspond_landline1:
                phone_number = str(invoice_obje.userdetail.poc_contact) + ',' + str(invoice_obje.userdetail.correspond_landline1)
            elif invoice_obje.userdetail.correspond_landline1 and invoice_obje.userdetail.correspond_cellno:
                phone_number = str(invoice_obje.userdetail.correspond_landline1) + ',' + str(
                    invoice_obje.userdetail.correspond_cellno)
            elif invoice_obje.userdetail.poc_contact and invoice_obje.userdetail.correspond_cellno:
                phone_number = str(invoice_obje.userdetail.poc_contact) + ',' + str(invoice_obje.userdetail.correspond_cellno)
            elif invoice_obje.userdetail.poc_contact:
                phone_number = str(invoice_obje.userdetail.poc_contact)
            elif invoice_obje.userdetail.correspond_cellno:
                phone_number = str(invoice_obje.userdetail.correspond_cellno)
            elif invoice_obje.userdetail.correspond_landline1:
                phone_number = str(invoice_obje.userdetail.correspond_landline1)
            else:
                phone_number = ""
            data = {
                'company_name': str(invoice_obje.userdetail.company.company_name),
                'correspond_address': str(invoice_obje.userdetail.correspond_address),
                'City_no':   str(invoice_obje.userdetail.correspondcity)+ '/' +str(invoice_obje.userdetail.correspond_pincode),
                'cell_no': phone_number,
            }
            record_list.append(data)


        tpl = get_template('backoffice/membership/certificate_courier_page.html')
        response = PDFTemplateResponse(
            request=request,
            template=tpl,
            context={'record_list':record_list},
            filename='Address_for_courier'+'.pdf',
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
        with open(str(settings.BASE_DIR) + "/site-static/membership_certificates/membership_certificate_pdf/"+str(response.filename), "wb") as f:
            f.write(response.rendered_content)
        print '\nResponse OUT | membership_certificate_download.py | download_certificate_file_manual | User = ', request.user

        file_paths.append({
                'file_path': str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_pdf/Address_for_courier.pdf',
                'file_name': 'Address_for_courier.pdf'
            })

        with ZipFile(str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip', 'w') as zip:
            for file_item in file_paths:
                zip.write(file_item['file_path'], file_item['file_name'])

        response = HttpResponse(open(str(settings.BASE_DIR) + '/site-static/membership_certificates/membership_certificate_zip/Membership_Certificate.zip', 'rb'), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=Membership_Certificate.zip'
        return response
    except Exception as exc:
        print '\nException | membership_certificate_download.py | download_certificate_file_manual | EXCP = ', str(traceback.print_exc())
        log.debug('Error = {0}\n'.format(exc))
        log.debug('Error = {0}\n'.format(str(traceback.print_exc())))
        log.exception("message")
        return HttpResponseServerError()


def create_pdf_manual(request, data):
    try:
        # data['company_name'] = str(data['company_name']).strip().title()


        if '/' in data['company_name']:
            data['company_name'] = str(data['company_name']).replace('/', '-')
            data['company_name'] = str(data['company_name']).strip()

        response = None
        if data['type'] == 'Associate':
            tpl = get_template('backoffice/membership/manual_associate_yealy.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context=data,
                filename=str(data['company_name']) +'.pdf',
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
        elif data['type'] == 'Member':
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
        elif data['type'] == 'Patron':
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
        elif data['type'] == 'Benefactor':
            tpl = get_template('backoffice/membership/manual_benefactor_life_membership.html')
            response = PDFTemplateResponse(
                request=data,
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
        elif data['type'] == 'Life-Member':
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

        with open(str(settings.BASE_DIR) + "/site-static/membership_certificates/membership_certificate_pdf/"+str(response.filename), "wb") as f:
            f.write(response.rendered_content)
        return True
    except Exception, e:
        print str(traceback.print_exc())
        return False



