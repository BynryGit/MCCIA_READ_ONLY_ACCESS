
# System Packages
import json, traceback, io
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponse
from xhtml2pdf import pisa
import cStringIO as StringIO
from cgi import escape
from django.template.loader import get_template
from django.template import Context
from xlsxwriter import Workbook

# User Model

from awardsapp.models import AwardDetail, AwardFor, AwardRegistration
from adminapp.models import City


# Render Backoffice Award Landing Menu
def awards_landing(request):
    return render(request, 'backoffice/awards/awards_landing.html')


# Render Award Registration Page
def awards_register(request):
    data = {'award_list': AwardDetail.objects.filter(is_deleted=False)}
    return render(request, 'backoffice/awards/awards_register.html', data)


# Show Award Registration Table
def get_award_registration_datatable(request):
    data = {}
    try:
        print '\nRequest IN | awards_landing.py | get_award_registration_datatable | User = ', request.user
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

        award_id = request.GET.get('award_id')
        award_registration_list = AwardRegistration.objects.filter(is_deleted=False)
        if award_id != 'All':
            award_registration_list = award_registration_list.filter(awarddetail_id=award_id)

        award_registration_list = award_registration_list.order_by('-created_date')
        total_records = award_registration_list.count()
        if length != -1:
            award_registration_list = award_registration_list[start:length]

        total_record = total_records

        i = 1
        for award_registration in award_registration_list:
            tempList = []
            tempList.append(i)
            tempList.append(str(award_registration.awarddetail.award_name))
            tempList.append(str(award_registration.company_name).strip())

            download_icon = '<a class="fa fa-download" target="_blank" href=/backofficeapp/download-award-reg-form/' + str(award_registration.id) + '/></a>'
            tempList.append(download_icon)
            i = i + 1

            dataList.append(tempList)

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        print '\nResponse OUT | awards_landing.py | get_award_registration_datatable | User = ', request.user
    except Exception, e:
        print '\nException IN | awards_landing.py | get_award_registration_datatable | EXCP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Download Award Registration Form in PDF
def download_award_reg_form(request, award_reg_id):
    html = ''
    try:
        print '\nRequest IN | awards_landing.py | download_award_reg_form | User = ', request.user
        award_reg_obj = AwardRegistration.objects.get(id=award_reg_id)
        template = get_template('backoffice/awards/award_form.html')
        html = template.render(Context({'award_reg_obj': award_reg_obj}))
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
        if not pdf.err:
            print '\nResponse OUT | awards_landing.py | download_award_reg_form | User = ', request.user
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="' + str(award_reg_obj.company_name) + '.pdf"'
            return response
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    except Exception, e:
        print '\nException IN | awards_landing.py | download_award_reg_form | EXCP = ', str(traceback.print_exc())
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


# Download Award Registration data in Excel
def download_award_data(request, award_id):
    try:
        print '\nRequest IN | awards_landing.py | download_award_data | User = ', request.user
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet_list = []
        i = j = k = l = m = n = 1

        award_detail_obj = None
        if award_id != 'All':
            award_detail_obj = AwardDetail.objects.get(id=award_id)
            worksheet_list.append({
                'award_obj': award_detail_obj,
                'worksheet_obj': workbook.add_worksheet()
            })
        else:
            for award_obj in AwardDetail.objects.all():
                worksheet_list.append({
                    'award_obj': award_obj,
                    'worksheet_obj': workbook.add_worksheet()
                })
        workbook.formats[0].set_font_size(10)
        workbook.formats[0].set_text_wrap()
        cell_format = workbook.add_format({'border': 1})

        bg_deshmukh_column_list = ['Sr #', 'Award Name', 'Company Name', 'Concerned Person Name', 'Address', 'City',
                                   'Pin', 'Telephone No', 'Fax No', 'Year of Establishment',
                                   'Name of Chief of the Organization', 'Designation of Chief of the Organization',
                                   'Briefly describe the projects undertaken under Corporate Social Responsibility',
                                   'Give information on the type of social services extended, the beneficiaries and to extent to which benefits derived by the beneficiaries'
                                   ]

        parkhe_hari_ramabai_column_list = ['Sr #', 'Award Name', 'Company Name', 'Concerned Person Name', 'Address', 'City',
                                           'Pin', 'Telephone No', 'Fax No', 'Year of Establishment',
                                           'Name of Chief of the Organization', 'Designation of Chief of the Organization',
                                           'Name of the PRODUCT / PROCESS / SERVICES tendered for Award',
                                           'Brief Description of product / process which is to be considered for the Award',
                                           'Special Features/ Advantages of the product services',
                                           'The first date of product manufactured / rendering of the services',
                                           'Is the product commercially launched and marketed ? If Yes, since when',
                                           'Turnover Year 1', 'Turnover Amount 1', 'Turnover Year 2', 'Turnover Amount2',
                                           'Turnover Year 3', 'Turnover Amount 3', 'Profit Year 1', 'Profit Amount 1',
                                           'Profit Year 2', 'Profit Amount 2', 'Profit Year 3', 'Profit Amount 3'
                                           ]

        natu_column_list = ['Sr #', 'Award Name', 'Name', 'First Generation Entrepreneur', 'Company Name', 'Date of Commencement',
                            'Starting Capital Rs', 'Address', 'City', 'Pin', 'Telephone No', 'Fax No',
                            'Email', 'MSME Registration Number', 'MSME Registration Date', 'Legal Status', 'Number of Employees',
                            'Name of the PRODUCT / PROCESS / SERVICE', 'Brief Description of product / process / Service',
                            'List of Locations (Business / Manufacturing Units)', 'Gross Block Investment',
                            'Plant & Machinery Investment', 'Net Block Investment', 'Turnover Year 1', 'Turnover Amount 1',
                            'Turnover Year 2', 'Turnover Amount2', 'Turnover Year 3', 'Turnover Amount 3', 'Profit Year 1',
                            'Profit Amount 1', 'Profit Year 2', 'Profit Amount 2', 'Profit Year 3', 'Profit Amount 3',
                            'Patent Registered', 'Awards Recognition', 'List of Certification',
                            'Write up about yourself / your Company & why you consider yourself for the award']

        rathi_column_list = ['Sr #', 'Award Name', 'Company Name', 'Concerned Person Name', 'Address', 'City', 'Pin',
                             'Telephone No', 'Fax No', 'Year of Establishment', 'Name of Chief of the Organization',
                             'Designation of Chief of the Organization', 'Brief description of the green initiatives undertaken by the Company which includes any activity which has helped to reduce pollution, contribution towards green environment, or any other activity which would help to protect to promote a green environment including initiatives to reduce global warming ']

        counter = 0
        if award_id != 'All':
            if 'parkhe' in str(award_detail_obj.award_name).lower():
                for column_item in parkhe_hari_ramabai_column_list:
                    worksheet_list[0]['worksheet_obj'].write_string(0, counter, str(column_item))
                    counter = counter + 1
            elif 'harimalini' in str(award_detail_obj.award_name).lower():
                for column_item in parkhe_hari_ramabai_column_list:
                    worksheet_list[0]['worksheet_obj'].write_string(0, counter, str(column_item))
                    counter = counter + 1
            elif 'ramabai' in str(award_detail_obj.award_name).lower():
                for column_item in parkhe_hari_ramabai_column_list:
                    worksheet_list[0]['worksheet_obj'].write_string(0, counter, str(column_item))
                    counter = counter + 1
            elif 'deshmukh' in str(award_detail_obj.award_name).lower():
                for column_item in bg_deshmukh_column_list:
                    worksheet_list[0]['worksheet_obj'].write_string(0, counter, str(column_item))
                    counter = counter + 1
            elif 'natu' in str(award_detail_obj.award_name).lower():
                for column_item in natu_column_list:
                    worksheet_list[0]['worksheet_obj'].write_string(0, counter, str(column_item))
                    counter = counter + 1
            else:
                for column_item in rathi_column_list:
                    worksheet_list[0]['worksheet_obj'].write_string(0, counter, str(column_item))
                    counter = counter + 1
        else:
            for item in worksheet_list:
                if 'parkhe' in str(item['award_obj'].award_name).lower():
                    counter = 0
                    for column_item in parkhe_hari_ramabai_column_list:
                        item['worksheet_obj'].write_string(0, counter, str(column_item))
                        counter = counter + 1
                elif 'harimalini' in str(item['award_obj'].award_name).lower():
                    counter = 0
                    for column_item in parkhe_hari_ramabai_column_list:
                        item['worksheet_obj'].write_string(0, counter, str(column_item))
                        counter = counter + 1
                elif 'ramabai' in str(item['award_obj'].award_name).lower():
                    counter = 0
                    for column_item in parkhe_hari_ramabai_column_list:
                        item['worksheet_obj'].write_string(0, counter, str(column_item))
                        counter = counter + 1
                elif 'deshmukh' in str(item['award_obj'].award_name).lower():
                    counter = 0
                    for column_item in bg_deshmukh_column_list:
                        item['worksheet_obj'].write_string(0, counter, str(column_item))
                        counter = counter + 1
                elif 'natu' in str(item['award_obj'].award_name).lower():
                    counter = 0
                    for column_item in natu_column_list:
                        item['worksheet_obj'].write_string(0, counter, str(column_item))
                        counter = counter + 1
                elif 'rathi' in str(item['award_obj'].award_name).lower():
                    counter = 0
                    for column_item in rathi_column_list:
                        item['worksheet_obj'].write_string(0, counter, str(column_item))
                        counter = counter + 1

        award_reg_list = AwardRegistration.objects.filter(is_deleted=False)
        if award_id != 'All':
            award_reg_list = award_reg_list.filter(awarddetail_id=award_id)

        for award_reg in award_reg_list:
            if 'parkhe' in str(award_reg.awarddetail.award_name).lower():
                for item in worksheet_list:
                    if award_reg.awarddetail.id == item['award_obj'].id:
                        i = write_parkhe_hari_ramabai_sheet(request, award_reg, item['worksheet_obj'], i)
                        i = i + 1

            elif 'harimalini' in str(award_reg.awarddetail.award_name).lower():
                for item in worksheet_list:
                    if award_reg.awarddetail.id == item['award_obj'].id:
                        j = write_parkhe_hari_ramabai_sheet(request, award_reg, item['worksheet_obj'], j)
                        j = j + 1

            elif 'ramabai' in str(award_reg.awarddetail.award_name).lower():
                for item in worksheet_list:
                    if award_reg.awarddetail.id == item['award_obj'].id:
                        k = write_parkhe_hari_ramabai_sheet(request, award_reg, item['worksheet_obj'], k)
                        k = k + 1

            elif 'deshmukh' in str(award_reg.awarddetail.award_name).lower():
                for item in worksheet_list:
                    if award_reg.awarddetail.id == item['award_obj'].id:
                        l = write_bg_deshmukh_sheet(request, award_reg, item['worksheet_obj'], l)
                        l = l + 1

            elif 'natu' in str(award_reg.awarddetail.award_name).lower():
                for item in worksheet_list:
                    if award_reg.awarddetail.id == item['award_obj'].id:
                        m = write_natu_sheet(request, award_reg, item['worksheet_obj'], m)
                        m = m + 1

            elif 'rathi' in str(award_reg.awarddetail.award_name).lower():
                for item in worksheet_list:
                    if award_reg.awarddetail.id == item['award_obj'].id:
                        n = write_rathi_sheet(request, award_reg, item['worksheet_obj'], n)
                        n = n + 1


        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Award_Registration_'+ str(datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
        print '\nResponse OUT | awards_landing.py | download_award_data | User = ', request.user
        return response
    except Exception, e:
        print '\nException IN | awards_landing.py | download_award_data | EXCP = ', str(traceback.print_exc())
        return False


# Write B G Deshmukh Award Registrations
def write_bg_deshmukh_sheet(request, award_reg, worksheet_obj, i):
    try:
        worksheet_obj.write_string(i, 0, str(i))
        worksheet_obj.write_string(i, 1, str(award_reg.awarddetail.award_name).strip())
        worksheet_obj.write_string(i, 2, str(award_reg.company_name).strip())
        worksheet_obj.write_string(i, 3, str(award_reg.concerned_person_name).strip())
        worksheet_obj.write_string(i, 4, str(award_reg.address).strip())
        worksheet_obj.write_string(i, 5, str(award_reg.city.city_name).strip())
        worksheet_obj.write_string(i, 6, str(award_reg.pin_code).strip())
        worksheet_obj.write_string(i, 7, str(award_reg.telephone_no).strip())
        worksheet_obj.write_string(i, 8, str(award_reg.fax_no).strip())
        worksheet_obj.write_string(i, 9, str(award_reg.establish_year).strip())
        worksheet_obj.write_string(i, 10, str(award_reg.org_chief_name).strip())
        worksheet_obj.write_string(i, 11, str(award_reg.org_chief_designation).strip())
        worksheet_obj.write_string(i, 12, str(award_reg.product_description).strip())
        worksheet_obj.write_string(i, 13, str(award_reg.product_feature_advantage).strip())
    except Exception, e:
        print '\nException IN | awards_landing.py | write_bg_deshmukh_sheet | EXCP = ', str(traceback.print_exc())
    return i


# Write Parkhe, Harimalini, Ramabai Award Registrations
def write_parkhe_hari_ramabai_sheet(request, award_reg, worksheet_obj, i):
    try:
        worksheet_obj.write_string(i, 0, str(i))
        worksheet_obj.write_string(i, 1, str(award_reg.awarddetail.award_name).strip())
        worksheet_obj.write_string(i, 2, str(award_reg.company_name).strip())
        worksheet_obj.write_string(i, 3, str(award_reg.concerned_person_name).strip())
        worksheet_obj.write_string(i, 4, str(award_reg.address).strip())
        worksheet_obj.write_string(i, 5, str(award_reg.city.city_name).strip())
        worksheet_obj.write_string(i, 6, str(award_reg.pin_code).strip())
        worksheet_obj.write_string(i, 7, str(award_reg.telephone_no).strip())
        worksheet_obj.write_string(i, 8, str(award_reg.fax_no).strip())
        worksheet_obj.write_string(i, 9, str(award_reg.establish_year).strip())
        worksheet_obj.write_string(i, 10, str(award_reg.org_chief_name).strip())
        worksheet_obj.write_string(i, 11, str(award_reg.org_chief_designation).strip())
        worksheet_obj.write_string(i, 12, str(award_reg.product).strip())
        worksheet_obj.write_string(i, 13, str(award_reg.product_description).strip())
        worksheet_obj.write_string(i, 14, str(award_reg.product_feature_advantage).strip())
        worksheet_obj.write_string(i, 15, str(award_reg.product_manufacture_date).strip())
        worksheet_obj.write_string(i, 16, str(award_reg.commercial_launch_date).strip())
        worksheet_obj.write_string(i, 17, str(award_reg.to_year_one).strip())
        worksheet_obj.write_string(i, 18, str(award_reg.to_one).strip())
        worksheet_obj.write_string(i, 19, str(award_reg.to_year_two).strip())
        worksheet_obj.write_string(i, 20, str(award_reg.to_two).strip())
        worksheet_obj.write_string(i, 21, str(award_reg.to_year_three).strip())
        worksheet_obj.write_string(i, 22, str(award_reg.to_three).strip())
        worksheet_obj.write_string(i, 23, str(award_reg.profit_year_one).strip())
        worksheet_obj.write_string(i, 24, str(award_reg.profit_one).strip())
        worksheet_obj.write_string(i, 25, str(award_reg.profit_year_two).strip())
        worksheet_obj.write_string(i, 26, str(award_reg.profit_two).strip())
        worksheet_obj.write_string(i, 27, str(award_reg.profit_year_three).strip())
        worksheet_obj.write_string(i, 28, str(award_reg.profit_three).strip())
    except Exception, e:
        print '\nException IN | awards_landing.py | write_parkhe_hari_ramabai_sheet | EXCP = ', str(traceback.print_exc())
    return i


# Write Natu Award Registrations
def write_natu_sheet(request, award_reg, worksheet_obj, i):
    try:
        worksheet_obj.write_string(i, 0, str(i))
        worksheet_obj.write_string(i, 1, str(award_reg.awarddetail.award_name).strip())
        worksheet_obj.write_string(i, 2, str(award_reg.person_name).strip())
        worksheet_obj.write_string(i, 3, str('Yes' if award_reg.first_gen_entp else 'No').strip())
        worksheet_obj.write_string(i, 4, str(award_reg.company_name).strip())
        worksheet_obj.write_string(i, 5, str(award_reg.commencement_date).strip())
        worksheet_obj.write_string(i, 6, str(award_reg.starting_capital).strip())
        worksheet_obj.write_string(i, 7, str(award_reg.address).strip())
        worksheet_obj.write_string(i, 8, str(award_reg.city.city_name).strip())
        worksheet_obj.write_string(i, 9, str(award_reg.pin_code).strip())
        worksheet_obj.write_string(i, 10, str(award_reg.telephone_no).strip())
        worksheet_obj.write_string(i, 11, str(award_reg.fax_no).strip())
        worksheet_obj.write_string(i, 12, str(award_reg.email).strip())
        worksheet_obj.write_string(i, 13, str(award_reg.msme_reg_no).strip())
        worksheet_obj.write_string(i, 14, str(award_reg.msme_reg_date).strip())
        worksheet_obj.write_string(i, 15, str(award_reg.get_legal_status_display()).strip())
        worksheet_obj.write_string(i, 16, str(award_reg.no_of_employees).strip())
        worksheet_obj.write_string(i, 17, str(award_reg.product).strip())
        worksheet_obj.write_string(i, 18, str(award_reg.product_description).strip())
        worksheet_obj.write_string(i, 19, str(award_reg.locations).strip())
        worksheet_obj.write_string(i, 20, str(award_reg.gross_block_investment).strip())
        worksheet_obj.write_string(i, 21, str(award_reg.plant_and_mc_investment).strip())
        worksheet_obj.write_string(i, 22, str(award_reg.net_block_investment).strip())
        worksheet_obj.write_string(i, 23, str(award_reg.to_year_one).strip())
        worksheet_obj.write_string(i, 24, str(award_reg.to_one).strip())
        worksheet_obj.write_string(i, 25, str(award_reg.to_year_two).strip())
        worksheet_obj.write_string(i, 26, str(award_reg.to_two).strip())
        worksheet_obj.write_string(i, 27, str(award_reg.to_year_three).strip())
        worksheet_obj.write_string(i, 28, str(award_reg.to_three).strip())
        worksheet_obj.write_string(i, 29, str(award_reg.profit_year_one).strip())
        worksheet_obj.write_string(i, 30, str(award_reg.profit_one).strip())
        worksheet_obj.write_string(i, 31, str(award_reg.profit_year_two).strip())
        worksheet_obj.write_string(i, 32, str(award_reg.profit_two).strip())
        worksheet_obj.write_string(i, 33, str(award_reg.profit_year_three).strip())
        worksheet_obj.write_string(i, 34, str(award_reg.profit_three).strip())
        worksheet_obj.write_string(i, 35, str('Yes' if award_reg.patent_registered else 'No').strip())
        worksheet_obj.write_string(i, 36, str(award_reg.award_recognition).strip())
        worksheet_obj.write_string(i, 37, str(award_reg.certification_list).strip())
        worksheet_obj.write_string(i, 38, str(award_reg.about_yourself).strip())
    except Exception, e:
        print '\nException IN | awards_landing.py | write_natu_sheet | EXCP = ', str(traceback.print_exc())
    return i


# Write Rathi Award Registrations
def write_rathi_sheet(request, award_reg, worksheet_obj, i):
    try:
        worksheet_obj.write_string(i, 0, str(i))
        worksheet_obj.write_string(i, 1, str(award_reg.awarddetail.award_name).strip())
        worksheet_obj.write_string(i, 2, str(award_reg.company_name).strip())
        worksheet_obj.write_string(i, 3, str(award_reg.concerned_person_name).strip())
        worksheet_obj.write_string(i, 4, str(award_reg.address).strip())
        worksheet_obj.write_string(i, 5, str(award_reg.city.city_name).strip())
        worksheet_obj.write_string(i, 6, str(award_reg.pin_code).strip())
        worksheet_obj.write_string(i, 7, str(award_reg.telephone_no).strip())
        worksheet_obj.write_string(i, 8, str(award_reg.fax_no).strip())
        worksheet_obj.write_string(i, 9, str(award_reg.establish_year).strip())
        worksheet_obj.write_string(i, 10, str(award_reg.org_chief_name).strip())
        worksheet_obj.write_string(i, 11, str(award_reg.org_chief_designation).strip())
        worksheet_obj.write_string(i, 12, str(award_reg.product_description).strip())
    except Exception, e:
        print '\nException IN | awards_landing.py | write_rathi_sheet | EXCP = ', str(traceback.print_exc())
    return i
