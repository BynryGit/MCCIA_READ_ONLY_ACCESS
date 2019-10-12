
# System Module Import
import smtplib
from email.mime.multipart import MIMEMultipart
from django.template import Context
import MySQLdb
import traceback
import json
import dateutil.relativedelta
from django.shortcuts import *
from django.db.models import Q
from django.http import HttpResponse
from email.mime.image import MIMEImage
from django.conf import settings
from email.mime.text import MIMEText
from django.template.loader import get_template
import logging
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from urlparse import urlparse
from os.path import splitext
from datetime import datetime
from dateutil import tz
charset='utf-8'

# Custom User Model Import

from adminapp.models import Committee
from eventsapp.models import EventDetails, EventType, EventRegistration, EventBannerImage, EventParticipantUser, EventSponsorImage, PromoCode
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallLocation, HallDetail


try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


@csrf_exempt
def event_home(request):
    return render(request, 'backoffice/events/events.html')


@csrf_exempt
def event_details(request):
    try:
        request.session['event_banner_id'] = ''
        request.session['event_sponsor_id'] = ''
        committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')
        event_type_list = EventType.objects.filter(is_deleted=False).order_by('event_type')
        event_list = [{'id': obj.id, 'event_title': obj.event_title, 'from_date': obj.from_date.strftime('%B %d, %Y')}
                      for obj in EventDetails.objects.filter(is_deleted=False).order_by('event_type')]
        data = {
            'success':'true',
            'committee_list':committee_list,
            'events_list':event_list,
            'event_type_list':event_type_list
        }
    except Exception as e:
        print 'Exception | event_landing | events_home | user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}

    return render(request, 'backoffice/events/event_details.html',data)    


@csrf_exempt
def get_events_datatable(request): 

    try:
        print 'backofficeapp | event_home.py | get_events_datatable | user'
        dataList = []

        total_record=0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['','organising_committee__committee','event_title']
        column_name = order + list[int(column)]
        start = request.GET.get('start')
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        event_detail_objs_list = EventDetails.objects.filter(is_deleted=False)#.order_by(column_name)
        
        if request.GET.get('select_status'):
            event_detail_objs_list = event_detail_objs_list.filter(event_status=int(request.GET.get('select_status')))
        if request.GET.get('committee'):
            event_detail_objs_list = event_detail_objs_list.filter(organising_committee=request.GET.get('committee'))
        if request.GET.get('events'):
            event_detail_objs_list = event_detail_objs_list.filter(id=request.GET.get('events'))
        if request.GET.get('event_type'):
            event_detail_objs_list = event_detail_objs_list.filter(event_type=request.GET.get('event_type'))

        total_record=event_detail_objs_list.count()
        event_detail_objs_list = event_detail_objs_list.filter().order_by('-id')

        # i = 0
        # for obj in event_detail_objs_list:
        #     # For reflecting release date impact on visibility of event
        #     if obj.release_date:
        #         release_date = obj.release_date.strftime('%d %B %Y - %H:%M')
        #         release_date = datetime.strptime(release_date, '%d %B %Y - %H:%M')
        #     else:
        #         release_date = datetime.now()
        #     today_date = datetime.now()

        i = 0
        for obj in event_detail_objs_list:
            # For reflecting release date impact on visibility of event
            if obj.release_date:
                release_date = obj.release_date.strftime('%d %B %Y - %H:%M')
                release_date = datetime.strptime(release_date, '%d %B %Y - %H:%M')
                today_date = datetime.now()

                if release_date <= today_date:
                    obj.view_status = 1
                    obj.save()

                to_date = obj.to_date.strftime('%d %B %Y - %H:%M')
                to_date = datetime.strptime(to_date, '%d %B %Y - %H:%M')
                if to_date <= today_date:
                    obj.view_status = 0
                    obj.event_status = 1
                    obj.save()

            i = i + 1 
            tempList = []   
            # when_to_attend = obj.from_date.strftime('%B %d, %Y') + ' ' + obj.from_time.strftime('%H:%M:%p') + ' - ' + obj.to_date.strftime('%B %d, %Y') + ' ' + obj.to_time.strftime('%H:%M:%p')
            when_to_attend = obj.from_date.strftime('%B %d, %Y') + ' - ' + obj.to_date.strftime('%B %d, %Y')

            action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/backofficeapp/edit-event/?event_detail='+str(obj.id)+'"></a>&nbsp;&nbsp;'

            if obj.event_status == 1:
                event_status = 'Inactive'
                status = '<label class="label label-default"> Past Event </label>'
                action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_details(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'Active'
                status = '<label class="label label-success"> Future Event </label>'
                action2= '<a class="icon-trash" title="Delete Event" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_details(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
                
            if obj.hall_details:
                hall_location = obj.hall_details.hall_location.location
            else:
                hall_location = obj.other_location_address

            # tempList.append(i)
            # tempList.append(obj.organising_committee.committee)
            # tempList.append(obj.event_title)
            # if obj.event_type:
            #     tempList.append(obj.event_type.event_type)
            # else:
            #     tempList.append('')
            # tempList.append(when_to_attend)
            # tempList.append(hall_location)
            # tempList.append(status)
            # tempList.append(action1 + action2)


            tempList.append(i)
            tempList.append(obj.organising_committee.committee)
            tempList.append(obj.event_title)
            tempList.append(obj.event_type.event_type if obj.event_type else '')
            tempList.append(when_to_attend)
            tempList.append(hall_location)
            tempList.append(status)
            tempList.append(action1 + action2)

            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_events_datatable | user %s. Exception = ', str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')  


@transaction.atomic
@csrf_exempt
def update_event_detail_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | event_home.py | update_event_detail_status | User = ', request.user
        eventobj = EventDetails.objects.get(id=str(request.POST.get('event_details_id')))
        if request.POST.get('check_ajax') == 'yes':
            print '------------yes'
            if eventobj.event_status == 0:
                eventobj.event_status = 1
                eventobj.view_status = 0
                # eventobj.is_deleted = True
                if request.POST.get('delete_event_radio') == 'cancel':
                    eventobj.current_event_stat = 1
                elif request.POST.get('delete_event_radio') == 'postpone':
                    eventobj.current_event_stat = 2
                eventobj.save()
                EventRegistration.objects.filter(event=eventobj,is_deleted=False).update(is_active=False,register_status=1)
                email_list = EventParticipantUser.objects.filter(event_user__event=eventobj,is_deleted=False).values('email_id')
                if email_list:
                    for item in email_list:
                        send_mailto_participant(request, item['email_id'], eventobj)
                EventParticipantUser.objects.filter(event_user__event=eventobj,is_deleted=False).update(is_active=False,register_status=1)
        else:
            print '--------no---------'
            eventobj.event_status = 0
            eventobj.view_status = 1
            eventobj.is_deleted = False
            eventobj.current_event_stat = 0
            EventRegistration.objects.filter(event=eventobj,is_deleted=False).update(is_active=True,register_status=0)
            EventParticipantUser.objects.filter(event_user__event=eventobj,is_deleted=False).update(is_active=True,register_status=0)
            eventobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print '\nResponse IN | event_home.py | update_event_detail_status | User = ', request.user
    except Exception,e:
        print '\nException IN | event_home.py | update_event_detail_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def send_mailto_participant(request, email_id, event_detail_obj):
    try:
        to_list = []
        cc_list = []
        imgpath=os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        fp = open(imgpath, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<img>')

        gmail_user = "eventreg@mcciapune.com"
        gmail_pwd = "event@2011reg"

        to_list.append(email_id)
        ctx = {'event_detail_obj': event_detail_obj,
               'event_delete_reason': request.POST.get('delete_event_radio')}

        cc_list.append(event_detail_obj.contact_person1.email)
        if event_detail_obj.contact_person2 and event_detail_obj.contact_person2.email:
            cc_list.append(event_detail_obj.contact_person2.email)

        html=get_template('backoffice/events/event_delete_email.html').render(Context(ctx))
        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html, 'html',_charset=charset)
        msg.attach(htmlfile)
        msg.attach(msgImage)

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        to = to_list
        cc = cc_list

        if request.POST.get('delete_event_radio') == 'cancel':
            if event_detail_obj.hall_details:
                msg['subject'] = 'Cancel - ' + event_detail_obj.event_title + ' scheduled on ' + event_detail_obj.from_date.strftime(
                    '%d %B %Y') + ' at ' + event_detail_obj.hall_details.hall_name + ', ' + event_detail_obj.hall_details.hall_location.location + ', Pune.'
            else:
                msg[
                    'subject'] = 'Cancel - ' + event_detail_obj.event_title + ' scheduled on ' + event_detail_obj.from_date.strftime(
                    '%d %B %Y') + ' at ' + event_detail_obj.other_location_address
        else:
            if event_detail_obj.hall_details:
                msg['subject'] = 'Postpone - ' + event_detail_obj.event_title + ' scheduled on ' + event_detail_obj.from_date.strftime(
                    '%d %B %Y') + ' at ' + event_detail_obj.hall_details.hall_name + ', ' + event_detail_obj.hall_details.hall_location.location + ', Pune.'
            else:
                msg[
                    'subject'] = 'Postpone - ' + event_detail_obj.event_title + ' scheduled on ' + event_detail_obj.from_date.strftime(
                    '%d %B %Y') + ' at ' + event_detail_obj.other_location_address

        msg['from'] = 'mailto: <eventreg@mcciapune.com>'
        msg['to'] = ",".join(to)
        msg['cc'] = ",".join(cc)
        toaddrs = to + cc
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()
    except Exception, e:
        print e


@csrf_exempt
def add_new_event(request):
    try:
        request.session['event_banner_id'] = ''
        request.session['event_sponsor_id'] = ''
        committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')        
        event_type_list = EventType.objects.filter(is_deleted=False).order_by('event_type')
        system_user_list = SystemUserProfile.objects.filter(is_deleted=False).order_by('username')
        hall_location_list = HallLocation.objects.filter(is_deleted=False).order_by('location')

        data = {
            'success':'true',
            'committee_list':committee_list,
            'event_type_list':event_type_list,
            'system_user_list':system_user_list,
            'hall_location_list':hall_location_list
        }
    except Exception as e:
        print 'Exception | event_landing | events_home | user %s. Exception = ', str(traceback.print_exc())
        data ={'success':'false'}        
    
    return render(request, 'backoffice/events/add_new_event.html',data)


def get_contact_person(request):
    try:
        committee_obj = Committee.objects.get(id=request.GET.get('commitee_id'))
        contact_person_obj1 = SystemUserProfile.objects.get(id=committee_obj.contact_person1.id, is_deleted=False)
        try:
            contact_person_obj2 = SystemUserProfile.objects.get(id=committee_obj.contact_person2.id, is_deleted=False)
            contact_person_obj2 = contact_person_obj2.id
        except Exception as e:
            contact_person_obj2 = ''
            print e
            pass
        
        data ={
            'success':'true',
            'contact_person_obj1':contact_person_obj1.id,
            'contact_person_obj2':contact_person_obj2
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')   


def get_program_details(request):
    try:
        event_object = EventDetails.objects.get(id=request.GET.get('event_detail_id'))
        event_description_indetails = event_object.event_description_indetails
        
        data ={
            'success':'true',
            'event_description_indetails':event_description_indetails
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')       


def get_hall_name(request):
    try:
        hall_name_list = []
        hall_obj_list = HallDetail.objects.filter(hall_location_id=request.GET.get('event_location_id'))
        for obj in hall_obj_list:            
            hall_name_list.append(
                {'id': obj.id, 'hall_name': obj.hall_name})
        data ={
            'success':'true',
            'hall_name_list':hall_name_list,
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')  


def get_hall_location(request):
    locations=[]
    try:
        hall_obj = HallDetail.objects.get(id=request.GET.get('hall_id'))
        
        try:
            location = {'lat': hall_obj.latitude,
                    'lon': hall_obj.longitude,
                    'zoom': 8,
                    'title': hall_obj.hall_name,
                    'html': '<h5>' + hall_obj.hall_name + '</h5>',
                    'icon': 'https://maps.google.com/mapfiles/ms/icons/red-dot.png'
                    }
            locations.append(location)
        except Exception,e:
            pass

        print locations
        data ={
            'success':'true',
            'locations':locations
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')        


def get_location(request):
    locations=[]
    data={}
    addresslist=[]
    try:
        zone=request.GET.get('zone')
        city=request.GET.get('city')
        if zone == "All":
            contact_objs = CSDCenters.objects.filter(city_id=city)
        else:
            contact_objs=CSDCenters.objects.filter(zone_id=zone)

        contactdetail_obj=ContactDetail.objects.all()
        contacts={}
        if contact_objs and contactdetail_obj:
            contactdetail_obj=contactdetail_obj.last()
            try:
                contacts={
                            'helpline_number':contactdetail_obj.helpline_number if contactdetail_obj.helpline_number else "NA",
                            'anti_bribery_help':contactdetail_obj.anti_bribery_help if contactdetail_obj.anti_bribery_help else "NA",
                            'online_complaint':contactdetail_obj.online_complaint if contactdetail_obj.online_complaint else "NA",
                            'igrc_email':contactdetail_obj.igrc_email if contactdetail_obj.igrc_email else "NA",
                            'customer_portal':contactdetail_obj.customer_portal if contactdetail_obj.customer_portal else "NA",
                            'electricity_theft_help_no':contactdetail_obj.electricity_theft_help_no if contactdetail_obj.electricity_theft_help_no else "NA",
                            'igrc_no':contactdetail_obj.igrc_no if contactdetail_obj.igrc_no else "NA",
                          }
            except Exception,e:
                pass
            for contact_obj in contact_objs:
                try:
                    address_one = contact_obj.address  + ',<br/>' if contact_obj.address_two else contact_obj.address
                    address_two = contact_obj.address_two + ',<br/>' if contact_obj.address_three else contact_obj.address_two
                    address_three = contact_obj.address_three

                    address={
                           'address_one':address_one,
                           'address_two':address_two,
                           'address_three':address_three,
                           'center_name':contact_obj.center_name
                    }
                    addresslist.append(address)
                except Exception,e:
                    print e

                    pass
                try:
                    location = {'lat': contact_obj.latitude,
                            'lon': contact_obj.longitude,
                            'zoom': 12,
                            'title': contact_obj.center_name,
                            'html': '<h5>' + contact_obj.center_name + '</h5>',
                            'icon': 'https://maps.google.com/mapfiles/ms/icons/red-dot.png'
                            }
                    locations.append(location)
                except Exception,e:
                    pass

            data={'success':'true','locations':locations,'address':address,'contacts':contacts,'hideflag':'flase','addresslist':addresslist,}
        else:
            data = {'success': 'true','hideflag':'true'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception,e:
        print e
        pass


@csrf_exempt
def upload_event_banner(request):
    try:
        print 'Request In|backofficeapp |event_home.py |upload_event_banner |User %s Data'
        attachment_file = EventBannerImage()
        attachment_file.save()
        attachment_file.document_files = request.FILES['event_file']
        attachment_file.banner_type = 0
        attachment_file.save()
        request.session['event_banner_id'] = attachment_file.id
        data = {'success': 'true'}

        print 'Response Out|backofficeapp |event_home.py |upload_event_banner|User %s Data'
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        print "Exception In |  backofficeapp |event_home.py |upload_event_banner", exc
        data = {'success': 'false', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json') 


@csrf_exempt
def upload_sponsor_banner(request):
    try:
        print 'Request In|backofficeapp |event_home.py |upload_sponsor_banner |User %s Data'
        attachment_file = EventBannerImage()
        attachment_file.save()
        attachment_file.document_files = request.FILES['sponsor_file']
        attachment_file.banner_type = 1
        attachment_file.save()
        request.session['event_sponsor_id'] = attachment_file.id
        data = {'success': 'true'}

        print 'Response Out|backofficeapp |event_home.py |upload_sponsor_banner|User %s Data'
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        print "Exception In |  backofficeapp |event_home.py |upload_sponsor_banner", exc
        data = {'success': 'false', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')  


def get_banner_file(request):
    try:
        print 'Request In|backofficeapp |event_home.py |get_banner_file |User %s Data'

        if request.session['event_banner_id']:
            event_banner_obj = EventBannerImage.objects.get(id=request.session['event_banner_id'])
        else:
            event_banner_obj = EventBannerImage.objects.get(event_detail_id=request.GET.get('event_details_id'),banner_type=0)
        parsed = urlparse(event_banner_obj.document_files.url)
        root, ext = splitext(parsed.path)
        event_docs_address = "http://" + get_current_site(request).domain + event_banner_obj.document_files.url

        # if request.session['event_sponsor_id']:
        #     sponsor_banner_obj = EventBannerImage.objects.get(id=request.session['event_sponsor_id'])
        # else:
        #     sponsor_banner_obj = EventBannerImage.objects.get(event_detail_id=request.GET.get('event_details_id'),banner_type=1)
        # parsed = urlparse(sponsor_banner_obj.document_files.url)
        # root, ext = splitext(parsed.path)
        # sponsor_docs_address = "http://" + get_current_site(request).domain + sponsor_banner_obj.document_files.url
        
        data = {
            'success': 'true',
            'event_docs_address': event_docs_address, 
            'sponsor_docs_address': '',            
        }
        print 'Response Out|backofficeapp |event_home.py |get_banner_file|User %s Data'
    except Exception, e:
        print "Exception In |  backofficeapp |event_home.py |get_banner_file", e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')  


@transaction.atomic
@csrf_exempt
def save_new_event(request):
    print json.dumps(request.POST, indent=4)
    #pdb.set_trace()
    sid = transaction.savepoint()
    try:
        print 'Request In| backofficeapp |event_home.py |save_new_event|User %s Data'
        print "______________________________________",request.POST.get('select_entry_level')
        print "___________________________________",request.POST.get('select_event_sponsored')
        print "_______________________________",request.POST.get('entry_criteria')

        from_zone = tz.tzutc()
        to_zone = tz.gettz('Asia/Kolkata')
        utc_from_date = dateutil.parser.parse(str(request.POST.get('from_date')))
        utc_from_date = utc_from_date.replace(tzinfo=from_zone)
        final_from_date = utc_from_date.astimezone(to_zone)

        utc_to_date = dateutil.parser.parse(str(request.POST.get('to_date')))
        utc_to_date = utc_to_date.replace(tzinfo=from_zone)
        final_to_date = utc_to_date.astimezone(to_zone)

        utc_registr_start_date = dateutil.parser.parse(str(request.POST.get('registr_start_date')))
        utc_registr_start_date = utc_registr_start_date.replace(tzinfo=from_zone)
        final_registr_start_date = utc_registr_start_date.astimezone(to_zone)

        utc_registr_end_date = dateutil.parser.parse(str(request.POST.get('registr_end_date')))
        utc_registr_end_date = utc_registr_end_date.replace(tzinfo=from_zone)
        final_registr_end_date = utc_registr_end_date.astimezone(to_zone)

        utc_release_date = dateutil.parser.parse(str(request.POST.get('release_date')))
        utc_release_date = utc_release_date.replace(tzinfo=from_zone)
        final_release_date = utc_release_date.astimezone(to_zone)

        if request.POST.get('early_bird_date'):
            utc_early_bird_date = dateutil.parser.parse(str(request.POST.get('early_bird_date')))
            utc_early_bird_date = utc_early_bird_date.replace(tzinfo=from_zone)
            final_early_bird_date = utc_early_bird_date.astimezone(to_zone)   

        is_early_bird = False
        if request.POST.get('is_early_bird') == 'true':
            is_early_bird = True

        # For reflecting release date impact on visibility of event
        release_date = datetime.strptime(request.POST.get('release_date'), "%d %B %Y - %H:%M")
        today_date = datetime.now()
        view_status = 0
        if release_date <= today_date:
            view_status = 1
        
        discount_1 = ''
        discount_2 = ''
        discount_3 = ''
        if request.POST.get('disc_part_count1'):
            discount_1 = request.POST.get('disc_part_count1') + '-' + request.POST.get('disc_perct1')
        if request.POST.get('disc_part_count2'):
            discount_2 = request.POST.get('disc_part_count2') + '-' + request.POST.get('disc_perct2')
        if request.POST.get('disc_part_count3'):
            discount_3 = request.POST.get('disc_part_count3') + '-' + request.POST.get('disc_perct3')

        event_objective_id = request.POST.get('event_objective')
        print '------------------',request.POST.get('expected_freemember')
        if int(request.POST.get('select_event_type')) == 8:
            event_val = EventType(
                event_type = request.POST.get('oter_select_event_type')
                )
            event_val.save()
        event_obj = EventDetails(
                event_description_indetails = request.POST.get('program_detail_id'),
                organising_committee = Committee.objects.get(id=request.POST.get('select_committee')),
                contact_person1 = SystemUserProfile.objects.get(id = request.POST.get('select_contact1')),
                contact_person2 = SystemUserProfile.objects.get(id = request.POST.get('select_contact2')) if request.POST.get('select_contact2') else None,
                priority = 0,#request.POST.get('select_priority'),
                event_type = EventType.objects.get(id = request.POST.get('select_event_type')),
                event_mode = request.POST.get('select_criteria'),
                event_level= request.POST.get('select_entry_level'),
                is_event_sponsored = request.POST.get('select_event_sponsored'),
                online_payment = request.POST.get('select_payment'),
                event_title = request.POST.get('event_title'),
                hall_details = HallDetail.objects.get(id = request.POST.get('hall_id')) if request.POST.get('hall_id')!= ' ' else None,
                other_location_address = request.POST.get('other_location_address'),
                from_date = final_from_date,
                to_date = final_to_date,
                registration_start_date = final_registr_start_date,
                registration_end_date = final_registr_end_date,
                release_date = final_release_date,
                to_whom_description = request.POST.get('for_whom'),
                organised_by = request.POST.get('organised_by'),
                event_objective = request.POST.get('event_objective'),
                member_charges = request.POST.get('member_charges'),
                non_member_charges = request.POST.get('non_member_charges'),
                other_charges_name = request.POST.get('othercharge_name'),
                other_charges_amount = request.POST.get('othercharge_amt') if request.POST.get('othercharge_amt') else 0,

                is_early_bird = is_early_bird,
                early_member_charges = request.POST.get('early_member_charges') if request.POST.get('early_member_charges') else 0,
                early_non_member_charges = request.POST.get('early_non_member_charges') if request.POST.get('early_non_member_charges') else 0,
                early_bird_date = final_early_bird_date if request.POST.get('early_bird_date') else None,

                discount_1=discount_1,
                discount_2=discount_2,
                discount_3=discount_3,
                expected_members=request.POST.get('expected_member') if request.POST.get('expected_member') else 0,
                # expected_nonmembers=request.POST.get('expected_nonmember') if request.POST.get('expected_nonmember') else 0,
                # expected_freemembers=request.POST.get('expected_freemember') if request.POST.get('expected_freemember')!='undefined' else 0,
                # expected_sponsored_members=request.POST.get('expected_sponsmember') if request.POST.get('expected_sponsmember')!='undefined' else 0,
                # expected_capacity=request.POST.get('expected_capacity') if request.POST.get('expected_capacity') else 0,
                meta_title = request.POST.get('meta_title'),
                meta_keyword = request.POST.get('meta_keyword'),
                meta_description = request.POST.get('meta_description'),
                meta_keyphrases = request.POST.get('meta_key_phrase'),
                view_status = view_status,
                created_on = datetime.now(),
            )
        event_obj.save()  
        event_obj.event_no = 'E' + str(event_obj.from_date.strftime('%d%m%y')) + str(event_obj.id)
        event_obj.save()

        if request.POST.get('promocode_list1'):
            promocode_list1 = (request.POST.get('promocode_list1')).split(',')
            promocode_list2 = (request.POST.get('promocode_list2')).split(',')
            promocode_list3 = (request.POST.get('promocode_list3')).split(',')
            promocode_list4 = (request.POST.get('promocode_list4')).split(',')
            length_count=len(promocode_list1)

            for obj in range(0, length_count):
                promocode_obj=PromoCode(
                    event_details=event_obj,
                    promo_code=promocode_list2[obj],
                    for_whom=promocode_list1[obj],
                    percent_discount=promocode_list3[obj],
                    discounted_amount=promocode_list4[obj],
                    #created_by=request.session['first_name'],
                )
                promocode_obj.save()

        try:
            attachment_obj1 = EventBannerImage.objects.get(id=request.session['event_banner_id'])
            attachment_obj1.event_detail_id=event_obj
            attachment_obj1.save()

            # attachment_obj2 = EventBannerImage.objects.get(id=request.session['event_sponsor_id'])
            # attachment_obj2.event_detail_id=event_obj
            # attachment_obj2.save()

        except Exception as e:
            pass

        attachment_list = request.POST.get('attachments')
        save_attachments(attachment_list,event_obj,request)
        
        print 'Response Out|backofficeapp |event_home.py |save_new_event|User %s Data'
        data = {'success': 'true'}
        transaction.savepoint_commit(sid)
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        print "Exception In |  backofficeapp |event_home.py |save_new_event", exc
        data = {'success': 'false', 'error': 'Exception ' + str(exc)}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')  

import os
def save_attachments(attachment_list, event_id,request):
    try:
        print 'backofficeapp |event_home.py|save_attachments'
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        for attached_id in attachment_list:
            attachment_obj = EventSponsorImage.objects.get(id=attached_id)
            attachment_obj.event_id=event_id
            attachment_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        print 'Exception|backofficeapp |event_home.py|save_attachments', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def upload_sponsor_images(request):
    try:
        print 'backofficeapp|event_home.py|upload_sponsor_images'
        if request.method == 'POST':
            attachment_file = EventSponsorImage()
            attachment_file.save()
            request.FILES['file[]'].name = 'event_sponsor_image_' + str(attachment_file.id) + '_' + request.FILES[
                'file[]'].name
                       
            attachment_file.document_files = request.FILES['file[]']
            attachment_file.save()
            data = {'success': 'true', 'attachid': attachment_file.id}
        else:
            data = {'success': 'false'}
    except MySQLdb.OperationalError, e:
        print 'Exception|backofficeapp|event_home.py|upload_sponsor_images', e
        data = {'success': 'invalid request'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def remove_sponsor_images(request):
    try:
        print 'backofficeapp|event_home.py|remove_sponsor_images'
        image_id = request.GET.get('image_id')
        image = EventSponsorImage.objects.get(id=image_id)
        image.delete()

        data = {'success': 'true'}
    except MySQLdb.OperationalError, e:
        print 'Exception|backofficeapp|event_home.py|remove_sponsor_images', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def edit_event(request):
    try:
        request.session['event_banner_id'] = ''
        request.session['event_sponsor_id'] = ''
        event_obj = EventDetails.objects.get(id=request.GET.get('event_detail'))
        committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')        
        event_type_list = EventType.objects.filter(is_deleted=False).order_by('event_type')
        system_user_list = SystemUserProfile.objects.filter(is_deleted=False).order_by('username')
        hall_location_list = HallLocation.objects.filter(is_deleted=False).order_by('location')

        hall_name_list = []
        if event_obj.hall_details:
            hall_name_list = HallDetail.objects.filter(hall_location = event_obj.hall_details.hall_location,is_deleted=False,is_active=True).order_by('hall_name')

        image_count=0
        sponsor_images = EventSponsorImage.objects.filter(event_id=event_obj.id,is_deleted=False)
        docs_address = ''
        image_id = ''
        if sponsor_images:
            image_count = sponsor_images.count()
            c=1
            for image in sponsor_images:
                if c==1:
                    c = 2
                    docs_address = 'http://' + get_current_site(request).domain + image.document_files.url
                    image_id = str(image.id)
                else:

                    docs_address = docs_address + ',' + 'http://' + get_current_site(request).domain + image.document_files.url
                    image_id = image_id + ',' + str(image.id)



        try:
            event_banner_obj = EventBannerImage.objects.get(event_detail_id=event_obj,banner_type=0)
            parsed = urlparse(event_banner_obj.document_files.url)
            root, ext = splitext(parsed.path)
            event_docs_address = "http://" + get_current_site(request).domain + event_banner_obj.document_files.url
        except Exception, e:
            event_docs_address = ''

        # sponsor_banner_obj = EventBannerImage.objects.get(event_detail_id=event_obj,banner_type=1)
        # parsed = urlparse(sponsor_banner_obj.document_files.url)
        # root, ext = splitext(parsed.path)
        # sponsor_docs_address = "http://" + get_current_site(request).domain + sponsor_banner_obj.document_files.url


        discount_part1 = event_obj.discount_1.split('-')[0] if event_obj.discount_1 else ''
        discount_percent1 = event_obj.discount_1.split('-')[1] if event_obj.discount_1 else ''
        discount_part2 = event_obj.discount_2.split('-')[0] if event_obj.discount_2 else ''
        discount_percent2 = event_obj.discount_2.split('-')[1] if event_obj.discount_2 else ''
        discount_part3 = event_obj.discount_3.split('-')[0] if event_obj.discount_3 else ''
        discount_percent3 = event_obj.discount_3.split('-')[1] if event_obj.discount_3 else ''

        if event_obj.hall_details:
           hall_details_id = event_obj.hall_details.id
           hall_location_id = event_obj.hall_details.hall_location.id
           hall_location = event_obj.hall_details.hall_location.location
        else:
            hall_details_id = ''
            hall_location_id = ''
            hall_location = ''
        
        is_promocode = False
        promocode_obj_list = []
        promocode_obj_list = PromoCode.objects.filter(event_details=event_obj,status=True,is_deleted=False)
        if promocode_obj_list:
            is_promocode = True
        
        data = {
            'success':'true',   
            'image_list': docs_address,
            'image_count': image_count,
            'image_id_list': image_id,
            'hall_location_id':hall_location_id,
            'hall_location_list':hall_location_list,
            'hall_details_id':hall_details_id,
            'other_location_address':event_obj.other_location_address,
            'hall_name_list':hall_name_list,
            'event_detail_id':request.GET.get('event_detail'),        
            'committee_list':committee_list,
            'event_type_list':event_type_list,
            'system_user_list':system_user_list,
            'committee_id':event_obj.organising_committee.id,
            'contact_person1_id':event_obj.contact_person1.id,
            'contact_person2_id':event_obj.contact_person2.id if event_obj.contact_person2 else None,
            'priority':event_obj.priority,
            'event_type_id':event_obj.event_type.id,
            'entry_criteria':event_obj.event_mode,
            'online_payment':event_obj.online_payment,
            'is_event_sponsored': event_obj.is_event_sponsored,
            'event_level': event_obj.event_level,
            # 'expected_capacity':event_obj.expected_capacity,
            'event_title':event_obj.event_title,
            'event_location':hall_location,
            'from_date':event_obj.from_date.strftime('%d %B %Y - %H:%M'),
            'to_date':event_obj.to_date.strftime('%d %B %Y - %H:%M'),
            'registration_start_date':event_obj.registration_start_date.strftime('%d %B %Y - %H:%M'),
            'registration_end_date':event_obj.registration_end_date.strftime('%d %B %Y - %H:%M'),
            'release_date':event_obj.release_date.strftime('%d %B %Y - %H:%M'),
            'to_whom_description':event_obj.to_whom_description,
            'organised_by':event_obj.organised_by,
            'event_objective': event_obj.event_objective if event_obj.event_objective else '',
            'member_charges':event_obj.member_charges,
            'non_member_charges':event_obj.non_member_charges,

            'discount_part1':discount_part1,
            'discount_percent1':discount_percent1,
            'discount_part2':discount_part2,
            'discount_percent2':discount_percent2,
            'discount_part3':discount_part3,
            'discount_percent3':discount_percent3,

            'is_early_bird':event_obj.is_early_bird,
            'early_member_charges':event_obj.early_member_charges,
            'early_non_member_charges':event_obj.early_non_member_charges,
            'early_bird_date':event_obj.early_bird_date.strftime('%d %B %Y - %H:%M') if event_obj.early_bird_date else '',

            'is_promocode':is_promocode,
            'promocode_obj_list':promocode_obj_list,

            'expected_member':event_obj.expected_members,
            'expected_nonmember':event_obj.expected_nonmembers,
            'expected_freemember':event_obj.expected_freemembers,
            'expected_sponsored_member':event_obj.expected_sponsored_members,
            'other_charges_name':event_obj.other_charges_name,
            'other_charges_amount':event_obj.other_charges_amount,
            'event_docs_address':event_docs_address,
            'sponsor_docs_address':'',
            'meta_title':event_obj.meta_title,
            'meta_keyword':event_obj.meta_keyword,
            'meta_description':event_obj.meta_description,
            'meta_keyphrases':event_obj.meta_keyphrases
        }
    except Exception as e:
        log.debug('Error = {0}\n'.format(e))
        print 'Exception | event_landing | events_home | user %s. Exception = ', str(traceback.print_exc())
        data ={'success':'false'}        
    
    return render(request, 'backoffice/events/edit_event.html',data)


@csrf_exempt
def update_event(request): 
    try:
        print 'Request In|backofficeapp |event_home.py |update_event|User %s Data'
        print "_____________________________________", request.POST.get('select_event_sponsored')
        from_zone = tz.tzutc()
        to_zone = tz.gettz('Asia/Kolkata')
        utc_from_date = dateutil.parser.parse(str(request.POST.get('from_date')))
        utc_from_date = utc_from_date.replace(tzinfo=from_zone)
        final_from_date = utc_from_date.astimezone(to_zone)

        utc_to_date = dateutil.parser.parse(str(request.POST.get('to_date')))
        utc_to_date = utc_to_date.replace(tzinfo=from_zone)
        final_to_date = utc_to_date.astimezone(to_zone)

        utc_registr_start_date = dateutil.parser.parse(str(request.POST.get('registr_start_date')))
        utc_registr_start_date = utc_registr_start_date.replace(tzinfo=from_zone)
        final_registr_start_date = utc_registr_start_date.astimezone(to_zone)

        utc_registr_end_date = dateutil.parser.parse(str(request.POST.get('registr_end_date')))
        utc_registr_end_date = utc_registr_end_date.replace(tzinfo=from_zone)
        final_registr_end_date = utc_registr_end_date.astimezone(to_zone)

        utc_release_date = dateutil.parser.parse(str(request.POST.get('release_date')))
        utc_release_date = utc_release_date.replace(tzinfo=from_zone)
        final_release_date = utc_release_date.astimezone(to_zone)

        if request.POST.get('early_bird_date'):
            utc_early_bird_date = dateutil.parser.parse(str(request.POST.get('early_bird_date')))
            utc_early_bird_date = utc_early_bird_date.replace(tzinfo=from_zone)
            final_early_bird_date = utc_early_bird_date.astimezone(to_zone)   

        is_early_bird = False
        if request.POST.get('is_early_bird') == 'true':
            is_early_bird = True

        # For reflecting release date impact on visibility of event
        release_date = datetime.strptime(request.POST.get('release_date'), "%d %B %Y - %H:%M")
        today_date = datetime.now()
        to_date = datetime.strptime(request.POST.get('to_date'), "%d %B %Y - %H:%M")

        view_status = 0
        if release_date <= today_date:
            view_status = 1

        event_status = 0
        if to_date <= today_date:
            view_status = 0
            event_status = 1

        discount_1 = ''
        discount_2 = ''
        discount_3 = ''
        if request.POST.get('disc_part_count1'):
            discount_1 = request.POST.get('disc_part_count1') + '-' + request.POST.get('disc_perct1')
        if request.POST.get('disc_part_count2'):
            discount_2 = request.POST.get('disc_part_count2') + '-' + request.POST.get('disc_perct2')
        if request.POST.get('disc_part_count3'):
            discount_3 = request.POST.get('disc_part_count3') + '-' + request.POST.get('disc_perct3')

        event_obj = EventDetails.objects.get(id=request.POST.get('event_details_id'))
        event_obj.hall_details = HallDetail.objects.get(id = request.POST.get('hall_id')) if request.POST.get('hall_id') != ' ' else None
        event_obj.other_location_address = request.POST.get('other_location_address')
        event_obj.event_description_indetails = request.POST.get('program_detail_id')
        event_obj.organising_committee = Committee.objects.get(id=request.POST.get('select_committee'))
        event_obj.contact_person1 = SystemUserProfile.objects.get(id = request.POST.get('select_contact1'))
        event_obj.contact_person2 = SystemUserProfile.objects.get(id = request.POST.get('select_contact2')) if request.POST.get('select_contact2') else None
        event_obj.priority = 0#request.POST.get('select_priority')
        event_obj.event_type = EventType.objects.get(id = request.POST.get('select_event_type'))
        # event_obj.event_type = EventType.objects.get(id = request.POST.get('oter_select_event_type'))
        event_obj.event_mode = request.POST.get('select_criteria')
        event_obj.online_payment = request.POST.get('select_payment')
        event_obj.event_level = request.POST.get('select_entry_level')
        event_obj.is_event_sponsored = request.POST.get('select_event_sponsored')
        event_obj.event_title = request.POST.get('event_title')
        event_obj.event_location = request.POST.get('event_location')
        event_obj.from_date = final_from_date
        event_obj.to_date = final_to_date
        event_obj.registration_start_date = final_registr_start_date
        event_obj.registration_end_date = final_registr_end_date
        event_obj.release_date = final_release_date
        event_obj.to_whom_description = request.POST.get('for_whom')
        event_obj.organised_by = request.POST.get('organised_by')
        event_obj.event_objective = request.POST.get('event_objective')
        event_obj.member_charges = request.POST.get('member_charges')
        event_obj.non_member_charges = request.POST.get('non_member_charges')
        # event_obj.expected_capacity = request.POST.get('expected_capacity') if request.POST.get('expected_capacity') else 0 
        event_obj.other_charges_name = request.POST.get('othercharge_name')
        event_obj.other_charges_amount = request.POST.get('othercharge_amt') if request.POST.get('othercharge_amt') else 0 

        event_obj.is_early_bird = is_early_bird
        event_obj.early_member_charges = request.POST.get('early_member_charges') if request.POST.get('early_member_charges') else 0
        event_obj.early_non_member_charges = request.POST.get('early_non_member_charges') if request.POST.get('early_non_member_charges') else 0
        event_obj.early_bird_date = final_early_bird_date if request.POST.get('early_bird_date') else None

        event_obj.discount_1 = discount_1
        event_obj.discount_2 = discount_2
        event_obj.discount_3 = discount_3
        event_obj.expected_members = request.POST.get('expected_member') if request.POST.get('expected_member') else 0 
        event_obj.expected_nonmembers = request.POST.get('expected_nonmember') if request.POST.get('expected_nonmember') else 0 
        event_obj.expected_freemembers = request.POST.get('expected_freemember') if request.POST.get('expected_freemember') else 0 
        event_obj.expected_sponsmembers = request.POST.get('expected_sponsmember') if request.POST.get('expected_sponsmember') else 0 
        event_obj.meta_title = request.POST.get('meta_title')
        event_obj.meta_keyword = request.POST.get('meta_keyword')
        event_obj.meta_description = request.POST.get('meta_description')
        event_obj.meta_keyphrases = request.POST.get('meta_key_phrase')
        event_obj.view_status = view_status
        event_obj.event_status = event_status
            
        event_obj.save()  

        attachment_list = request.POST.get('attachments')
        save_edit_attachments(attachment_list, event_obj)

        PromoCode.objects.filter(event_details_id=event_obj.id,status=True,is_deleted=False).delete()
        if request.POST.get('promocode_list1'):                    

            promocode_list1 = (request.POST.get('promocode_list1')).split(',')
            promocode_list2 = (request.POST.get('promocode_list2')).split(',')
            promocode_list3 = (request.POST.get('promocode_list3')).split(',')
            promocode_list4 = (request.POST.get('promocode_list4')).split(',')
            length_count=len(promocode_list1)

            for obj in range(0, length_count):
                promocode_obj=PromoCode(
                    event_details=event_obj,
                    promo_code=promocode_list2[obj],
                    for_whom=promocode_list1[obj],
                    percent_discount=promocode_list3[obj],
                    discounted_amount=promocode_list4[obj],
                    #created_by=request.session['first_name'],
                )
                promocode_obj.save()


        # DELETE banner docs
        try:
            if request.session['event_banner_id']:
                print '>>>>>>>>...11'
                EventBannerImage.objects.filter(event_detail_id=event_obj.id,banner_type=0).delete()
                attachment_obj1 = EventBannerImage.objects.get(id=request.session['event_banner_id'])
                attachment_obj1.event_detail_id=event_obj
                attachment_obj1.save()
            # if request.session['event_sponsor_id']:
            #     print ">>>>>>>>...222"
            #     EventBannerImage.objects.filter(event_detail_id=event_obj.id,banner_type=1).delete()
            #     attachment_obj2 = EventBannerImage.objects.get(id=request.session['event_sponsor_id'])
            #     attachment_obj2.event_detail_id=event_obj
            #     attachment_obj2.save()

        except Exception as e:
            pass
 
        print 'Response Out|backofficeapp |event_home.py |update_event|User %s Data'
        data = {'success': 'true'}
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        print "Exception In |  backofficeapp |event_home.py |update_event", exc
        data = {'success': 'false', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json') 


def save_edit_attachments(attachment_list, event_id):
    try:
        print 'backofficeapp |event_home.py|save_edit_attachments'
        attachment_list = attachment_list.split(',')
        attachment_list = filter(None, attachment_list)
        EventSponsorImage.objects.filter(event_id=event_id).exclude(id__in=attachment_list).update(event_id=None)
        for attached_id in attachment_list:
            attachment_obj = EventSponsorImage.objects.get(id=attached_id)
            attachment_obj.event_id = event_id
            attachment_obj.save()

        data = {'success': 'true'}
    except Exception, e:
        print 'Exception|backofficeapp |event_home.py|save_edit_attachments', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def event_registrations(request):
    committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')
    event_obj_list = EventDetails.objects.filter(is_deleted=False).order_by('event_title') #event_status=0,
    event_list = [{'id':obj.id,'event_title':obj.event_title,'from_date':obj.from_date.strftime('%B %d, %Y')} for obj in event_obj_list]
    data={'committee_list':committee_list,'event_list':event_list}


    return render(request, 'backoffice/events/event_registrations.html',data)        


@csrf_exempt
def get_events_registrations_datatable(request):
    try:
        print 'backofficeapp | event_home.py | get_events_registrations_datatable | user'
        dataList = []
        total_record=0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'event__organising_committee__committee', 'event__event_title']
        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        event_detail_objs_list = EventDetails.objects.filter(is_deleted=False)  # .order_by(column_name)  #event_status=0,
        # if request.GET.get('select_status'):
        #     event_detail_objs_list = event_detail_objs_list.filter(event_status=request.GET.get('select_status'))
        if request.GET.get('select_committee'):
            event_detail_objs_list = event_detail_objs_list.filter(organising_committee=request.GET.get('select_committee'))
        if request.GET.get('select_event'):
            event_detail_objs_list = event_detail_objs_list.filter(id=request.GET.get('select_event'))
        # if request.GET.get('event_type'):
        #     event_detail_objs_list = event_detail_objs_list.filter(event_type=request.GET.get('event_type'))

        # if request.GET.get('select_payment'):
        #     event_detail_objs_list = event_detail_objs_list.filter(id=request.GET.get('select_event'))
        if request.GET.get('select_payment'):
            eventregs=EventRegistration.objects.filter(event__id__in=[event.id for event in event_detail_objs_list],payment_status=request.GET.get('select_payment'),is_deleted=False)
        else:
            eventregs = EventRegistration.objects.filter(event__id__in=[event.id for event in event_detail_objs_list],is_deleted=False)

        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59, second=59)
            eventregs = eventregs.filter(created_on__range=[start_date, end_date])

        if searchTxt:
            eventregs = eventregs.filter((Q(reg_no__icontains=searchTxt)|Q(contact_person_name__icontains=searchTxt)))

        total_record= eventregs.count()

        eventregs = eventregs.order_by(column_name)
        eventregs = sorted(eventregs, reverse=True)


        if length == -1:
            eventregs = eventregs[start:]
        else:
            eventregs = eventregs[start:length]
        

        for eventreg in eventregs:
            view_action = '<a class="fa fa-file-text-o" title="Details" onclick="OpenDetailsView('+ str(
                eventreg.id)+');"></a>&nbsp;&nbsp;'

            download_action = '<a class="fa fa-file-pdf-o" target="_blank" title="Receipt" href="/backofficeapp/events-reciept/?event_reg_id=' + str(eventreg.id) + '"></a>'


            edit_action = '<a class="icon-pencil" target="_blank" title="Edit" href="/eventsapp/edit-events-details/?event_reg_id=' + str(
            eventreg.id) + '"></a>&nbsp;' + '&nbsp;'

            if eventreg.register_status == 1:
                event_reg_status = 'Inactive'
                status = '<label class="label label-default"> Inactive </label>'
                action2 = '<a class="icon-reload" title="Activate Registration" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_registraions(' + '"' + str(
                    event_reg_status) + '"' + ',' + str(eventreg.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_reg_status = 'Active'
                status = '<label class="label label-success"> Active </label>'
                action2= '<a class="icon-trash" title="Cancel Registration" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_registraions(' + '"' + str(
                    event_reg_status) + '"' + ',' + str(eventreg.id) + ')></a>&nbsp; &nbsp;'


            payment_status = '-'
            if eventreg.event.get_event_mode_display() == 'On Payment':
                payment_status = eventreg.get_payment_status_display() + '-' + eventreg.payment_mode

            tempList = []
            tempList.append(eventreg.id)
            tempList.append(eventreg.created_on.strftime('%B %d,%Y'))
            tempList.append(eventreg.reg_no)
            tempList.append(eventreg.event.event_title)
            tempList.append(eventreg.name_of_organisation)
            tempList.append(str(eventreg.no_of_participant))
            tempList.append(eventreg.total_amount)
            tempList.append(payment_status)
            tempList.append(view_action + download_action)
            tempList.append(edit_action + action2) 
      
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_events_registrations_datatable | user %s. Exception = ', str(traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': [ ]}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def update_event_reg_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        eventobj = EventRegistration.objects.get(id=str(request.GET.get('event_reg_id')))
        if eventobj.register_status == 0:
            eventobj.register_status = 1
        else:
            eventobj.register_status = 0

        eventobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_event_reg_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_event_registrations_details(request):
    try:
        eventreg_id = request.GET.get('eventreg_id')

        eventreg_obj = EventRegistration.objects.get(id=eventreg_id)

        membership_no = '-'
        if eventreg_obj.is_member == True:
            membership_no = eventreg_obj.user_details.member_associate_no if eventreg_obj.user_details.member_associate_no else "IA-TMP"
            
        event_date = eventreg_obj.event.from_date.strftime('%B %d, %Y %H:%M:%p') + ' To ' + eventreg_obj.event.to_date.strftime('%B %d, %Y %H:%M:%p')

        payble_amt = eventreg_obj.total_amount 
        if eventreg_obj.is_member == True:
            event_fee = eventreg_obj.event.member_charges
        elif eventreg_obj.is_other == True:
            event_fee = eventreg_obj.event.other_charges_amount            
        else:
            event_fee = eventreg_obj.event.non_member_charges


        event_fee = float(event_fee)*float(eventreg_obj.no_of_participant)

        cheque_date = ''
        if eventreg_obj.cheque_date:
            cheque_date = eventreg_obj.cheque_date.strftime('%B %d, %Y')

        payment_status = 'NA'
        total_discount_amount = 'NA'
        if eventreg_obj.event.get_event_mode_display() == 'On Payment':
            payment_status = eventreg_obj.get_payment_status_display() 
            total_discount_amount = eventreg_obj.total_discount_amount

        if eventreg_obj.event.hall_details:
            hall_location = eventreg_obj.event.hall_details.hall_location.location
        else:
            hall_location = eventreg_obj.event.other_location_address


        data = {
            'success':'true',
            'id':eventreg_obj.id,
            'event_title':eventreg_obj.event.event_title,
            'event_date':event_date,
            'event_location':hall_location,
            'reg_no':eventreg_obj.reg_no,
            'reg_date':eventreg_obj.created_on.strftime('%B %d, %Y'),
            'membership_no':membership_no,
            'name_of_org':eventreg_obj.name_of_organisation,
            'no_of_participant':eventreg_obj.no_of_participant,
            'discount':total_discount_amount,
            'payble_amt':payble_amt,
            'event_fee':event_fee,
            'gst_amt':eventreg_obj.extra_gst_amount,
            'payment_status':payment_status,
            'payment_method':eventreg_obj.get_payment_method_display(),
            'event_mode':eventreg_obj.event.get_event_mode_display(),
            'cash_receipt_no':eventreg_obj.cash_receipt_no,
            'cheque_no':eventreg_obj.cheque_no,
            'bank_name':eventreg_obj.bank_name,
            'cheque_date':cheque_date,
            'trasanction_id':eventreg_obj.trasanction_id        
        }
    except Exception, e:
        print 'Exception|backofficeapp | event_home.py|get_event_registrations_details', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_model_registrations_datatable(request):
    try:
        print 'backofficeapp | event_home.py | get_model_registrations_datatable | user'
        dataList = []
        total_record=0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        print searchTxt
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'event__organising_committee__committee', 'event__event_title']
        column_name = order + list[int(column)]
        start = request.GET.get('start')
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        eventregpart_list = EventParticipantUser.objects.filter(event_user=request.GET.get('registration_id'))

        total_record = eventregpart_list.count()

        # eventregpart_list = eventregpart_list.order_by(column_name)[start:length]

        for eventpart in eventregpart_list:
            tempList = []
            tempList.append(eventpart.event_user_name)
            tempList.append(eventpart.contact_no)
            tempList.append(eventpart.email_id)
            tempList.append(eventpart.designation)
      
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_model_registrations_datatable | user %s. Exception = ', str(traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': [ ]}
    return HttpResponse(json.dumps(data), content_type='application/json')


# def get_events_registration_receipt(request):
#     try:
#         # pdb.set_trace()
#         membership_certificate_dispatched_obj = UserDetail.objects.get(id=request.GET.get('mem_cert_dispatch_id'))
#         data = {'success': 'true'}
#         template = get_template('backoffice/membership/membership_certificate.html')
#         html = template.render(data)
#         result = StringIO.StringIO()
#         pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
#         if not pdf.err:
#             print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
#             return HttpResponse(result.getvalue(), content_type="application/pdf")
#         else:
#             print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
#             return HttpResponse('We are sorry for inconvenience. We will get this back soon.')
#     except Exception,e:
#         print '\nException | get_events_registration_receipt = ',str(traceback.print_exc())


# # @csrf_exempt
# def get_meter_data(request):
#     try:
#         print 'Request In|backofficeapp |event_home.py |get_meter_data|User %s Data'

#         print '>>>>>>>>',request.GET.get('event_details_id')

#     except Exception, exc:
#         print "Exception In |  backofficeapp |event_home.py |update_event", exc
#         data = {'success': 'false', 'error': 'Exception ' + str(exc)}
#     return True
#     #return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def save_payment_by_cash(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | event_home | save_payment_by_cash | user'

        event_reg_obj = EventRegistration.objects.get(id=request.GET.get('hidden_reg_id'))
        event_reg_obj.cash_receipt_no = request.GET.get('cash_receipt_no')
        event_reg_obj.payment_method = 0
        event_reg_obj.payment_status = 4
        event_reg_obj.tds_amount = request.GET.get('amt_tds')
        event_reg_obj.save()

        transaction.savepoint_commit(sid)


        data = {'success': 'true'}
        print 'Request OUT | event_home | save_payment_by_cash | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')          
    
    except Exception, exc:
        data = {'success': 'false'}
        print 'Exception | event_home | save_payment_by_cash | user %s. Exception = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')  


@transaction.atomic
def save_payment_by_cheque(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | event_home | save_payment_by_cheque | user'

        ch_date = datetime.strptime(request.GET.get('cheque_date'), '%d %B %Y').date()

        event_reg_obj = EventRegistration.objects.get(id=request.GET.get('hidden_reg_id'))
        event_reg_obj.cheque_no = request.GET.get('cheque_no')
        event_reg_obj.bank_name = request.GET.get('bank_name')
        event_reg_obj.cheque_date = ch_date
        event_reg_obj.payment_method = 1
        event_reg_obj.payment_status = 4
        event_reg_obj.tds_amount = request.GET.get('amt_tds')
        event_reg_obj.save()

        transaction.savepoint_commit(sid)


        data = {'success': 'true'}
        print 'Request OUT | event_home | save_payment_by_cheque | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')          
    
    except Exception, exc:
        data = {'success': 'false'}
        print 'Exception | event_home | save_payment_by_cheque | user %s. Exception = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')      


@transaction.atomic
def save_payment_by_neft(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | event_home | save_payment_by_neft | user'

        event_reg_obj = EventRegistration.objects.get(id=request.GET.get('hidden_reg_id'))
        event_reg_obj.trasanction_id = request.GET.get('transaction_id')
        event_reg_obj.payment_method = 2
        event_reg_obj.payment_status = 4
        event_reg_obj.tds_amount = request.GET.get('amt_tds')
        event_reg_obj.payment_remark = request.GET.get('remark_payment')
        event_reg_obj.save()

        transaction.savepoint_commit(sid)

        data = {'success': 'true'}
        print 'Request OUT | event_home | save_payment_by_neft | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')          
    
    except Exception, exc:
        data = {'success': 'false'}
        print 'Exception | event_home | save_payment_by_neft | user %s. Exception = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')      


@csrf_exempt
def invites_attendees_data(request):
    event_obj_list = EventDetails.objects.filter(is_deleted=False).order_by('event_title')  # event_status=0,
    event_list = [{'id': obj.id, 'event_title': obj.event_title, 'from_date': obj.from_date.strftime('%B %d, %Y')} for obj in event_obj_list]
    data = {'event_list': event_list}
    return render(request, 'backoffice/events/invites_attendees.html',data)


@csrf_exempt
def get_invites_attendees_datatable(request):
    try:
        print 'backofficeapp | event_home.py | get_invites_attendees_datatable | user'
        dataList = []
        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'event_user__event__event_title']
        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        select_event = request.GET.get('select_event')
        event_detail_objs_list = EventDetails.objects.filter(is_deleted=False)
        if select_event != 'All':
            event_detail_objs_list = event_detail_objs_list.filter(id=select_event)

        eventregs = EventParticipantUser.objects.filter(event_user__event__id__in=[event.id for event in event_detail_objs_list],
                                                     is_deleted=False).order_by('event_user__event__event_title')

        if searchTxt:
            eventregs = eventregs.filter((Q(event_user__reg_no__icontains=searchTxt) | Q(event_user__contact_person_name__icontains=searchTxt)))

        total_record = eventregs.count()

        if length == -1:
            eventregs = eventregs[start:]
        else:
            eventregs = eventregs[start:length]

        i = 1
        for eventreg in eventregs:
            if eventreg.is_invitee:
                edit_invites = "<input title='Mark Invitees' type='checkbox' class='check_invites' value='"+str(eventreg.id)+"' checked>"
            else:
                edit_invites = "<input title='Mark Invitees' type='checkbox' class='check_invites' value='" + str(eventreg.id) + "'>"
            if eventreg.is_attendees:
                edit_attendees = "<input title='Mark Attendees' type='checkbox' class='check_attendees' value='"+str(eventreg.id)+"' >"
            else:
                edit_attendees = "<input title='Mark Attendees' type='checkbox' class='check_attendees' value='" + str(eventreg.id) + "'checked>"

            tempList = []
            tempList.append(i)
            tempList.append(eventreg.created_on.strftime('%B %d,%Y'))
            tempList.append(eventreg.event_user.reg_no)
            tempList.append(eventreg.event_user.event.event_title)
            tempList.append(eventreg.event_user.name_of_organisation)
            tempList.append(str(eventreg.event_user_name))

            tempList.append(edit_invites)
            tempList.append(edit_attendees)
            i = i + 1

            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_invites_attendees_datatable | user %s. Exception = ', str(
            traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def update_invites_attendees_details(request):
    sid = transaction.savepoint()
    data = {}
    print '\nRequest IN | event_home.py | update_invites_attendees_details | user = ',request.user

    try:
        invites_id_list = request.GET.getlist('invites_id_list[]')
        attendees_id_list = request.GET.getlist('attendees_id_list[]')
        print request.GET
        print invites_id_list
        for event_reg_id in invites_id_list:
            event_reg_obj = EventParticipantUser.objects.get(id=event_reg_id)
            event_reg_obj.is_invitee = True
            event_reg_obj.save()

        for event_reg_id in attendees_id_list:
            event_reg_obj = EventParticipantUser.objects.get(id=event_reg_id)
            event_reg_obj.is_attendees = False
            event_reg_obj.save()
        transaction.savepoint_commit(sid)
        data['success'] = 'true'
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | event_home.py | update_invites_attendees_details | EXCP = ', str(traceback.print_exc())
        transaction.rollback(sid)
    print '\nResponse OUT | event_home.py | update_invites_attendees_details | user = ', request.user
    return HttpResponse(json.dumps(data), content_type='application/json')
