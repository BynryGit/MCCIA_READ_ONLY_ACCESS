import json
import traceback
from datetime import date, datetime

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from adminapp.models import Hall_detail_list,Location,Hall_pricing,Country
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from membershipapp.models import CompanyDetail, UserDetail
from visarecommendationapp.models import Membership_Visa_Recommendations, PlaceOfEmbassy
from hallbookingapp.models import HallLocation
from django.contrib.sites.shortcuts import get_current_site


def visa_backoffice_landing(request):
    """
    Render on Visa_backoffice_landing page

    **Template:**

    :template:`backoffice/visarecommendation/visa_backoffice_landing.html`
    """
    return render(request, 'backoffice/visarecommendation/visa_backoffice_landing.html')

def manage_visa(request):
    """
    Retrive data from HallLocation table and rendering

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.HallLocation`.

    **Template:**

    :template:`backoffice/visarecommendation/manage_visa.html`
    """
    data={}
    try:
        location_list = HallLocation.objects.filter(is_deleted=False).order_by('location')        
        data = {
            'success':'true',
            'location_list':location_list,
        }
    except Exception as e:
        print 'Exception | visa_backoffice | manage_visa | user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}

    return render(request, 'backoffice/visarecommendation/manage_visa.html',data)    

@csrf_exempt
def get_visa_datatable(request):
    """
    Load datatable based on applied filter

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.Membership_Visa_Recommendations`.

    **Template:**

    :template:`None`
    """
    try:
        dataList = []
        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""

        select_status = request.GET.get('select_status')
        select_location = request.GET.get('select_location')

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        try:
            #list = ['id']
            list = ['','','created_date','']

            column_name = order + list[int(column)]
        except Exception,e:
            pass

        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        if int(select_status):
        	visa_obj_list = Membership_Visa_Recommendations.objects.filter(is_completed=True,is_deleted=False)
        else:	
        	visa_obj_list = Membership_Visa_Recommendations.objects.filter(is_completed=False,is_deleted=False)

        if select_location:
            visa_obj_list = visa_obj_list.filter(location_id=select_location)

        if searchTxt:
            visa_obj_list = visa_obj_list.filter((Q(visa_recommendation_no__icontains=searchTxt)| Q(company_name__icontains=searchTxt)))

        total_record = visa_obj_list.count()

        i = 0

        visa_obj_list=visa_obj_list.order_by(column_name)[start:length]
        i=start
        for visa_obj in visa_obj_list:
            i = i + 1
            tempList = []
            
            passport_image_dwnld = '<label class="label label-default"> NA </label>'
            if visa_obj.doc_file:
                passport_image_src = "http://" + get_current_site(request).domain + visa_obj.doc_file.url
                passport_image_dwnld = '<a download href="'+str(passport_image_src)+'" title="Download" <i class="fa fa-download" aria-hidden="true"></i></a>'

            if visa_obj.is_completed :
                approve_action = '<label class="label label-success"> Approved </label>'                        
            else:
                # apprve_action = '<a title="Approve" class="fa fa-check-square-o test_class" onclick=update_visa_details(' +str(
                        # visa_obj.id) + ')></a>'
                approve_action= "<input title='Approve' type='checkbox' class='check_approve' value='"+str(visa_obj.id)+"'>"

            pdf_action = '<a href="/visarecommendationapp/generate-visa-pdf/?visa_id='+str(visa_obj.id)+'" target="_blank" title="Generate PDF" data-toggle="modal"> <i class="icon-printer" aria-hidden="true"></i> </a>'
            edit_action = '<a class="fa fa-pencil-square-o" title="Edit" href="/visarecommendationapp/edit-visa/?visa_id='+str(visa_obj.id)+'"></a>&nbsp;&nbsp;'


            tempList.append(i)
            tempList.append(str(visa_obj.company_name))
            tempList.append(visa_obj.created_date.strftime('%d %B %Y - %H:%M'))
            tempList.append(visa_obj.place_of_embassy.embassy_name)
            tempList.append(visa_obj.person_name)
            tempList.append(visa_obj.visa_recommendation_no)
            tempList.append(visa_obj.mobile_no)

            tempList.append(passport_image_dwnld)
            tempList.append(pdf_action + '&nbsp; &nbsp;' + edit_action)
            tempList.append(approve_action)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:

        print 'Exception OUT | visa_backoffice.py  | get_visa_datatable | End', e
        data = {
            'success': 'false',
            'message': str(e)
        }

        print '\n Exception OUT | hall_holidays.py | get_holiday_data | ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')    


def update_visa_details(request):
    """
    Update Membership_Visa_Recommendations table based on particular id from list of ID

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.Membership_Visa_Recommendations`.

    **Template:**

    :template:`None`
    """
    try:
        print'Request IN | visa_backoffice.py | update_visa_details '

        visa_id_list = request.GET.get('visa_id_list').split(',')
        for obj in visa_id_list:
            visa_obj = Membership_Visa_Recommendations.objects.get(id=obj)
            print "hallDetail_obj",visa_obj.is_completed

            visa_obj.is_completed = True
            visa_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        data = {'success': 'false'}
        print '\nException OUT| visa_backoffice.py | update_visa_details = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


from xhtml2pdf import pisa
import cStringIO as StringIO
from cgi import escape
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def generate_visa_pdf(request):
    """
    Based on particular visa_id, create a template for pdf document

    **Context**

    ``mymodel``
        An instance of :model:'visarecommendationapp.Membership_Visa_Recommendations`.

    **Template:**

    :template:`backoffice/visarecommendation/visa_pdf.html`
    """
    template = get_template('backoffice/visarecommendation/visa_pdf.html')
    visa_obj = Membership_Visa_Recommendations.objects.get(id=request.GET.get('visa_id'))

    if visa_obj.purpose_to_visit == 'BU':
        purpose_to_visit = 'Business'
    else:
        purpose_to_visit = 'Work Visit'
        
    html = template.render(Context(
        {
         'created_date':visa_obj.created_date.strftime('%d %B %Y'),
         'embassy_name':visa_obj.place_of_embassy.embassy_name,
         'city':visa_obj.place_of_embassy.city,
         'company_name':visa_obj.company_name,#.title(),
         'person_name':visa_obj.person_title + ' ' + visa_obj.person_name,#.title(),
         'address':visa_obj.address,#.title(),
         'person_designation':visa_obj.person_designation,#.title(),
         'visiting_from_date' :visa_obj.visiting_from_date.strftime('%B %Y'),
         'visitDurations' :(visa_obj.visitDurations).lower(),
         'total_visit_durations':(visa_obj.total_visit_durations).lower(),
         'person_title':visa_obj.person_title,
         'passport_no':visa_obj.passport_no,
         'passport_valid_from_date':visa_obj.passport_valid_from_date.strftime('%d/%m/%Y'),
         'passport_valid_to_date':visa_obj.passport_valid_to_date.strftime('%d/%m/%Y'),
         'visa_type':(visa_obj.visa_type).lower(),
         'purpose_to_visit':(purpose_to_visit).lower(),
         'enroll_type':visa_obj.mcciamember.enroll_type

         # 'location':visa_obj.location,
         # 'area':visa_obj.area.area,
        }
    ))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))      


def edit_visa(request):
    """
    Display an individual of Membership_Visa_Recommendations for edit perpose

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.PlaceOfEmbassy`.

    **Template:**

    :template:`backoffice/visarecommendation/edit_visa.html`
    """
    data = {}

    countryObj = Country.objects.filter(is_deleted=False)    
    locationObj = HallLocation.objects.filter(is_deleted=False)
    visa_recommend_obj = Membership_Visa_Recommendations.objects.get(id=request.GET.get('visa_id'))
    embassyObj = PlaceOfEmbassy.objects.filter(country_id = visa_recommend_obj.to_which_country.id,is_deleted=False)
    data={
        'countryObj':countryObj,
        'embassyObj':embassyObj,
        'locationObj':locationObj,
        'visa_recommendation_no':visa_recommend_obj.visa_recommendation_no,
        'registration_date':visa_recommend_obj.created_date.strftime("%d-%m-%Y"),
        'to_which_country':visa_recommend_obj.to_which_country.id,
        'place_of_embassy':visa_recommend_obj.place_of_embassy.id,
        'person_title':visa_recommend_obj.person_title,
        'person_name':visa_recommend_obj.person_name,
        'person_designation' : visa_recommend_obj.person_designation,
        'company_name':visa_recommend_obj.company_name,
        'address':visa_recommend_obj.address,
        'mobile_no':visa_recommend_obj.mobile_no,
        'email':visa_recommend_obj.email,
        'purpose_to_visit':visa_recommend_obj.purpose_to_visit,
        'visiting_from_date':visa_recommend_obj.visiting_from_date.strftime("%d-%m-%Y"),
        'visa_type':visa_recommend_obj.visa_type,
        'passport_no':visa_recommend_obj.passport_no,
        'location':visa_recommend_obj.location.id,
        'passport_valid_from_date':visa_recommend_obj.passport_valid_from_date.strftime("%d-%m-%Y"),
        'passport_valid_to_date':visa_recommend_obj.passport_valid_to_date.strftime("%d-%m-%Y"),
        'visitDurations':visa_recommend_obj.visitDurations,
        'total_visit_durations':visa_recommend_obj.total_visit_durations,
        'radio_choice':visa_recommend_obj.radio_choice,
        
    }
    return render(request, 'backoffice/visarecommendation/edit_visa.html',data)     


import datetime
from dateutil import tz 
@transaction.atomic()
@csrf_exempt
def save_edit_visa_recommendation(request):
    """
    Save visa recommendation after edited form

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.Membership_Visa_Recommendations`.


    """
    sid = transaction.savepoint()

    try:
        print 'Request IN | visa_backoffice | save_edit_visa_recommendation | user %s', request.POST.get('txtRDate')
        try:

            from_zone = tz.tzutc()
            to_zone = tz.gettz('Asia/Kolkata')

            visafromDate = datetime.datetime.strptime(request.POST.get('txtFDate'),'%d-%m-%Y')
            passport_valid_from_date = datetime.datetime.strptime(request.POST.get('txtVFDate'),'%d-%m-%Y')
            passport_valid_to_date = datetime.datetime.strptime(request.POST.get('txtVTDate'),'%d-%m-%Y')
            registration_date = datetime.datetime.strptime(request.POST.get('txtRDate'),'%d-%m-%Y').replace(tzinfo=from_zone).astimezone(to_zone)

            try:
                visaRecommendations = Membership_Visa_Recommendations.objects.get(visa_recommendation_no=request.POST.get('visa_recommendation_no'))

                visaRecommendations.to_which_country = Country.objects.get(id=request.POST.get('drpCountry'))
                visaRecommendations.location = HallLocation.objects.get(id=request.POST.get('McciaLocation'))
                visaRecommendations.place_of_embassy = PlaceOfEmbassy.objects.get(id=request.POST.get('drpEmbasy'))
                visaRecommendations.person_title = request.POST.get('PersonTitle')
                visaRecommendations.person_name = request.POST.get('txtName')
                visaRecommendations.person_designation = request.POST.get('txtDesg')
                visaRecommendations.mobile_no = request.POST.get('txtContact')
                visaRecommendations.email = request.POST.get('txtEmail')
                visaRecommendations.purpose_to_visit = request.POST.get('PurposeToVisit')
                visaRecommendations.visiting_from_date = visafromDate
                visaRecommendations.visa_type = request.POST.get('VisaType')
                visaRecommendations.radio_choice = request.POST.get('radioChoices')
                visaRecommendations.passport_no = request.POST.get('passport_no')
                visaRecommendations.passport_valid_from_date = passport_valid_from_date
                visaRecommendations.passport_valid_to_date = passport_valid_to_date
                visaRecommendations.created_date = registration_date                
                visaRecommendations.company_name = request.POST.get('txtCompany')
                visaRecommendations.address = request.POST.get('txtAdd')
                visaRecommendations.visitDurations = request.POST.get('visitDurations')
                visaRecommendations.total_visit_durations = request.POST.get('TotalvisitDurations')
               
                visaRecommendations.save()

                transaction.savepoint_commit(sid)

                data = {'success': 'true'}
                print 'Request OUT | visa_recommendation | save_edit_visa_recommendation | user %s', request.user
                return HttpResponse(json.dumps(data), content_type='application/json')

            except Exception as exc:
                print '>>>>>>>>>Exception>>>>>>>>',exc    
                print 'exception ', str(traceback.print_exc())
                data = {'success': 'false'} 


        except Exception, exc:
            print 'exception ', str(traceback.print_exc())
            transaction.rollback(sid)
            data = {'success': 'false'}            
            print 'exception in Member Visa Recommendation SAVING ', str(traceback.print_exc())



    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | visa_backoffice | save_edit_visa_recommendation | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')    



@csrf_exempt
def manage_embassy(request):
    """
    This function render it on following html page

    **Template:**

    :template:`backoffice/visarecommendation/manage_embassy.html`
    """
    return render(request, 'backoffice/visarecommendation/manage_embassy.html')

@csrf_exempt
def get_embassy_datatable(request):
    """
    Load datatable from PlaceOfEmbassy table

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.PlaceOfEmbassy`.

    """
    try:
        print 'visa_backoffice | get_embassy_datatable | user'
        dataList = []

        total_record=0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['','embassy_name','']
        column_name = order + list[int(column)]
        start = request.GET.get('start')

        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        embassy_list = PlaceOfEmbassy.objects.all()

        if request.GET.get('select_embassy') == 'True':
            embassy_list = embassy_list.filter(is_deleted=False)

        if request.GET.get('select_embassy') == 'False':
            embassy_list = embassy_list.filter(is_deleted=True)
                                
        if request.GET.get('search_embassy_text'):
            embassy_list = embassy_list.filter(Q(embassy_name__icontains=request.GET.get('search_embassy_text')))

        total_record=embassy_list.count()
        embassy_list = embassy_list.filter().order_by(column_name)[start:length]    

        i = 0
        a =1
        for obj in embassy_list:          
            tempList = []   

            action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/visarecommendationapp/edit-embassy-form/?embassy='+str(obj.id)+'"></a>&nbsp;&nbsp;'

            if obj.is_deleted:
                event_status = 'Inactive'
                status = '<label class="label label-default"> Inactive </label>'
                action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_embassy" onclick=update_embassy(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'Active'
                status = '<label class="label label-success"> Active </label>'
                action2= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_embassy" onclick=update_embassy(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            
            i = int(start) + a
            a = a + 1

            tempList.append(str(i))
            tempList.append(obj.embassy_name)
            tempList.append(obj.country.country_name)
            tempList.append(obj.address)
            tempList.append(obj.city)
            tempList.append(status)
            tempList.append(action1 + action2)
            dataList.append(tempList)       
        
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
    except Exception as e:
        print 'Exception visa_backoffice | get_embassy_datatable | user %s. Exception = ', str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')     


@transaction.atomic
def update_embassy_status(request):
    """
    Following function update the status of placeofembassy object

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.PlaceOfEmbassy`.

    """
    data = {}
    sid = transaction.savepoint()
    try:
        embassyobj = PlaceOfEmbassy.objects.get(id=str(request.GET.get('embassy_id')))
        if embassyobj.is_deleted == False:
            embassyobj.is_deleted = True
        else:
            embassyobj.is_deleted = False

        embassyobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_embassy_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')      


@csrf_exempt
def add_embassy_form(request):
    """
    Retrive country list

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.models`.

    **Template:**

    :template:`backoffice/visarecommendation/add_embassy_form.html`
    """
    try:
        country_list = Country.objects.filter(is_deleted=False)

        data = {
            'country_list':country_list,
        }
    except Exception as e:
        print 'Exception | visa_backoffice.py| add_embassy_form | user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}        
      
    return render(request, 'backoffice/visarecommendation/add_embassy_form.html',data)    


@transaction.atomic
@csrf_exempt
def save_new_embassy(request):
    """
    Code to save new embassy

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.PlaceOfEmbassy`.

    """
    sid = transaction.savepoint()
    try:
        print 'Request In|visarecommendation |visa_backoffice.py |save_new_embassy|User %s Data'
        embassy_obj = PlaceOfEmbassy(
            embassy_name = request.POST.get('embassy_name'),
            country = Country.objects.get(id = request.POST.get('select_country')) if request.POST.get('select_country') else None,
            city = request.POST.get('city_name'),
            address = request.POST.get('embassy_address'),
        )
        embassy_obj.save() 

        transaction.savepoint_commit(sid)
        print 'Response Out|visarecommendation |visa_backoffice.py |save_new_embassy|User %s Data'
        data = {'success': 'true'}
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        print "Exception In |  visarecommendation |visa_backoffice.py |save_new_embassy", exc
        data = {'success': 'false', 'error': 'Exception ' + str(exc)}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')  


@csrf_exempt
def edit_embassy_form(request):
    """
    Code for rendering on page with required data

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.PlaceOfEmbassy`.

    **Template:**

    :template:`backoffice/visarecommendation/edit_embassy_form.html`
    """
    try:
        embassy_obj = PlaceOfEmbassy.objects.get(id=request.GET.get('embassy'))
        country_list = Country.objects.filter(is_deleted=False)
        data = {
            'success':'true',   
            'country_list':country_list,        
            'embassy_id': embassy_obj.id,
            'embassy_name':embassy_obj.embassy_name,
            'address' : embassy_obj.address,
            'city' : embassy_obj.city,
            'country_id' : embassy_obj.country.id,
        }
    except Exception as e:
        print 'Exception | visarecommendation |visa_backoffice| edit_embassy_form | user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}        
    
    return render(request, 'backoffice/visarecommendation/edit_embassy_form.html',data)      


@transaction.atomic
@csrf_exempt
def update_embassy_form(request):
    """
    Update embassy data with given inputs

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.PlaceOfEmbassy`.

    """
    data = {}
    sid = transaction.savepoint()
    try:
        embassy_obj = PlaceOfEmbassy.objects.get(id=str(request.POST.get('embassy_id')))
        embassy_obj.embassy_name = request.POST.get('embassy_name')
        embassy_obj.country = Country.objects.get(id = request.POST.get('select_country')) if request.POST.get('select_country') else None
        embassy_obj.address = request.POST.get('embassy_address')
        embassy_obj.city = request.POST.get('city_name')
        embassy_obj.save()

        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_embassy_form = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')