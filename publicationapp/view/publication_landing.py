from datetime import datetime
import datetime,traceback, json
from django.shortcuts import *
from django.template.loader import get_template
from django.http import HttpResponse
from wkhtmltopdf.views import PDFTemplateResponse
# tables
from publicationapp.models import PublicationFile
from membershipapp.models import UserDetail



def publications_home(request):
    return render(request, 'publications/publications.html')


def publications_details(request):
    return render(request, 'publications/publications-details.html')


def publications_landing_page(request):
    return render(request, 'publications/publications-details.html')


def show_publication_details(request):
    return render(request, 'publications/show_publications.html')

# sampada py file

def get_sampada_details(request):
    data={}
    try:
        dataList = []
        print 'Publicationapp | publication_landing.py | get_sampada_details | user'
        filter_year = request.GET.get('sampada_input')
        year_list= PublicationFile.objects.filter(publish_date__year=filter_year, publication_type=0,is_deleted=False)
        total_record = year_list.count()
        for object in year_list:
            templist = []
            templist.append(object.publish_date.strftime('%B %Y'))
            templist.append('<a class="fa fa-eye" value="file" href="/sitemedia/'+str(object.file_path)+'" title="View" target="_blank"></a>')
            dataList.append(templist)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception,e:
        print '\nException | publication_data=',str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')

# world_of_businesss py file


def get_world_of_business_details(request):
    data = {}
    try:
        datalist = []
        s_date = request.GET.get('from_date')
        t_date = request.GET.get('to_date')
        fromDate = datetime.strptime(s_date, '%m/%d/%Y')
        toDate = datetime.strptime(t_date, '%m/%d/%Y')
        date_list = PublicationFile.objects.filter(publish_date__range=(fromDate, toDate),publication_type=2, is_deleted=False)
        total_record = date_list.count()
        for object in date_list:
            templist = []
            templist.append(object.publish_date.strftime('%d %B %Y'))
            templist.append('<a class="fa fa-eye" href="/sitemedia/' + str(object.file_path) + '"target="_blank"></a>')
            datalist.append(templist)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': datalist}
    except Exception, e:
        print '\nException | get_publication_details = ', str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')

# anual_report py file

def get_anual_report_details(request):
    data = {}
    try:
        datalist = []
        print 'Publicationapp | publication_landing.py | get_publication_details | user'
        input_year = request.GET.get('select_year')
        year_list = PublicationFile.objects.filter (publish_date__year=input_year, publication_type=1,is_deleted=False)
        # print '---------------------',year_list
        total_record = year_list.count()
        for object in year_list:
            templist = []
            templist.append(object.publish_date.strftime('%Y'))
            templist.append('<a class="fa fa-eye" href="/sitemedia/'+str(object.file_path)+'"target="_blank"></a>')
            datalist.append(templist)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': datalist}
    except Exception, e:
        print '\nException | get_publication_details = ', str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


def labels_for_sampada(request):
    try:
        print '\nRequest IN | publication_landing.py | labels_for_sampada | User = ', request.user
        userobjectmember = UserDetail.objects.filter(valid_invalid_member=True,is_deleted=False,member_associate_no__isnull=False).order_by('correspond_pincode').exclude(membership_slab__slab='Cttee. Membership')
        record_list = []
        data ={}
        for invoice_obje in userobjectmember:
            data = {
                'company_name': str(invoice_obje.company.company_name),
                'correspond_address': str(invoice_obje.correspond_address),
                'City_no': str(invoice_obje.correspondcity) + '/' + str(invoice_obje.correspond_pincode),
                'personal_no': str(invoice_obje.ceo_cellno) if str(invoice_obje.ceo_cellno) else ' ',
                'cell_no': str(invoice_obje.correspond_std1) + ' ' +str(invoice_obje.correspond_landline1)  if str(invoice_obje.correspond_std1) + ' ' +str(invoice_obje.correspond_landline1) else '',
            }
            record_list.append(data)

            tpl = get_template('backoffice/publication/labels_for_sampada.html')
            response = PDFTemplateResponse(
                request=request,
                template=tpl,
                context={'record_list': record_list},
                filename='labels_for_sampada' + '.pdf',
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
        print '\nRequest OUT | publication_landing | labels_for_sampada | user = ', request.user
    except Exception, e:
        print '\nException | publication_landing | labels_for_sampada = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return response