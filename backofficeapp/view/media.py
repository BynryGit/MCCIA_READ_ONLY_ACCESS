from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
from membershipapp.models import *
import urllib
import smtplib
from smtplib import SMTPException
from captcha_form import CaptchaForm
from django.shortcuts import *

import dateutil.relativedelta

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb
import csv
import json
# importing exceptions
from django.db import IntegrityError
from captcha_form import CaptchaForm
import operator
from django.db.models import Q
from datetime import date, timedelta
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import dateutil.relativedelta
from django.db.models import Count
from datetime import date
import calendar
import urllib2
import random
import traceback

from adminapp.models import Committee
from eventsapp.models import EventDetails, EventType, EventRegistration, EventBannerImage, EventParticipantUser, EventSponsorImage, PromoCode
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallLocation, HallDetail
from mediaapp.models import MCCIALEADERSHIP, MCCIATeamImage , MCCIATeam, MCCIAVideoLinks


#-------------New MCCIA--------------- 

@csrf_exempt
def media_home(request):
    return render(request, 'backoffice/media/media_landing.html')

@csrf_exempt
def mccia_leadership(request):
    return render(request, 'backoffice/media/mccia_leadership.html')

@csrf_exempt
def add_new_leadership(request):
    return render(request, 'backoffice/media/add_new_leadership.html')

@csrf_exempt
def add_new_member(request):
    return render(request, 'backoffice/media/add_new_member.html')

@csrf_exempt
def mccia_team(request):
    return render(request, 'backoffice/media/mccia_team.html')

@csrf_exempt
def print_media(request):
    return render(request, 'backoffice/media/print_media.html')    

@csrf_exempt
def print_media_new(request):
    return render(request, 'backoffice/media/print_media_new.html')  

@csrf_exempt
def video_gallery(request):
    return render(request, 'backoffice/media/video_gallery.html')     

@csrf_exempt
def add_video_links(request):
    return render(request, 'backoffice/media/add_video_links.html')      

@csrf_exempt
def electronic_media(request):
    return render(request, 'backoffice/media/electronic_media.html')  

@csrf_exempt
def add_electronic_media(request):
    return render(request, 'backoffice/media/add_electronic_media_link.html')    
    


@csrf_exempt
def save_leader_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | leader_details | leader_details | user %s', request.user        

        if request.method == 'POST':         
            MCCIALEADERSHIPObj=MCCIALEADERSHIP(
                leader_designation=request.POST.get('designation'),
                leader_name=request.POST.get('leader_name'),
                leader_post=request.POST.get('leader_post'),
                leader_organisation=request.POST.get('leader_organisation'),
                is_deleted=False,
            )
            MCCIALEADERSHIPObj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | leader_details | leader_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | leader_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_mccia_leaders_details(request):
    try:
        print '\nRequest IN | media | get_mccia_leaders_details | user %s', request.user
        dataList = []
        meterReadings = []
        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        
        mccialeaders_list = ''
        
        mccialeaders_list = MCCIALEADERSHIP.objects.filter(is_deleted=False)
        
        i = 1
        for mccialeader in mccialeaders_list:
            tempList = []
            action_two = ''
            legal_status = ''
            status = ''            

            edit_icon = '<a class="icon-pencil" title="MCCIA Leader Detail" data-toggle="modal" data-target="#edit_legal_details_modal" onClick="show_edit_legal_modal(' + str(mccialeader.id) + ')"></a>'

            action = edit_icon
            tempList.append(i)
            tempList.append(mccialeader.leader_designation)
            tempList.append(mccialeader.leader_name)
            tempList.append(mccialeader.leader_post)
            tempList.append(mccialeader.leader_organisation)
            tempList.append(edit_icon)
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
        print 'exception ', str(traceback.print_exc())
        print 'Exception|media | get_mccia_leaders_details|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_mccia_team_details(request):
    try:
        print '\nRequest IN | media | get_mccia_team_details | user %s', request.user
        dataList = []
        meterReadings = []


        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        
        mcciateam_list = ''
        
        mcciateam_list = MCCIATeam.objects.filter(is_deleted=False)
        
        i = 1
        for mcciamember in mcciateam_list:
            tempList = []
            action_two = ''
            legal_status = ''
            status = ''            

            edit_icon = '<a class="icon-pencil" title="MCCIA Team Detail" data-toggle="modal" data-target="#edit_legal_details_modal" onClick="show_edit_legal_modal(' + str(mcciamember.id) + ')"></a>'

            action = edit_icon
            tempList.append(i)
            tempList.append(mcciamember.member_designation)
            tempList.append(mcciamember.member_name)
            tempList.append(mcciamember.member_post)
            tempList.append(edit_icon)
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
        print 'exception ', str(traceback.print_exc())
        print 'Exception|media | get_mccia_team_details|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_team_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | Media | save_member_details | user %s', request.user        

        if request.method == 'POST':         
            MCCIATeamObj=MCCIATeam(
                member_designation=request.POST.get('member_designation'),
                member_name=request.POST.get('member_name'),
                member_post=request.POST.get('member_post'),
                is_deleted=False,
            )
            MCCIATeamObj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | save_member_details | save_member_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | save_member_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_video_link(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | Media | save_video_link | user %s', request.user        

        if request.method == 'POST':         
            MCCIAVideoLinksObj=MCCIAVideoLinks(
                video_link=request.POST.get('vlink'),
                video_type="Video Gallery",
                is_deleted=False,
            )
            MCCIAVideoLinksObj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | Media | save_video_link | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | save_member_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')    

def get_video_gallery(request):
    try:
        print '\nRequest IN | media | get_video_gallery | user %s', request.user
        dataList = []
        meterReadings = []


        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        
        video_list = ''
        
        video_list = MCCIAVideoLinks.objects.filter(video_type__icontains='Video Gallery',is_deleted=False)
        
        i = 1
        for videos in video_list:
            tempList = []
            action_two = ''
            legal_status = ''
            status = ''            

            edit_icon = '<a class="icon-pencil" title="MCCIA Team Detail" data-toggle="modal" data-target="#edit_legal_details_modal" onClick="show_edit_legal_modal(' + str(videos.id) + ')"></a>'

            action = edit_icon
            tempList.append(i)
            tempList.append(videos.video_link)
            tempList.append(edit_icon)
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
        print 'exception ', str(traceback.print_exc())
        print 'Exception|media | get_video_gallery|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_electronic_media(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | Media | save_electronic_media | user %s', request.user        

        if request.method == 'POST':         
            MCCIAVideoLinksObj=MCCIAVideoLinks(
                video_link=request.POST.get('vlink'),
                video_type="Electronic Media",
                is_deleted=False,
            )
            MCCIAVideoLinksObj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | Media | save_electronic_media | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | save_member_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')    

def get_electronic_media(request):
    try:
        print '\nRequest IN | media | get_electronic_media | user %s', request.user
        dataList = []
        meterReadings = []


        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        
        video_list = ''
        
        video_list = MCCIAVideoLinks.objects.filter(video_type__icontains='Electronic Media',is_deleted=False)
        
        i = 1
        for videos in video_list:
            tempList = []
            action_two = ''
            legal_status = ''
            status = ''            

            edit_icon = '<a class="icon-pencil" title="MCCIA Team Detail" data-toggle="modal" data-target="#edit_legal_details_modal" onClick="show_edit_legal_modal(' + str(videos.id) + ')"></a>'

            action = edit_icon
            tempList.append(i)
            tempList.append(videos.video_link)
            tempList.append(edit_icon)
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
        print 'exception ', str(traceback.print_exc())
        print 'Exception|media | get_electronic_media|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
# @csrf_exempt
# def event_details(request):
#     try:
#         request.session['event_banner_id'] = ''
#         request.session['event_sponsor_id'] = ''
#         committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')        
#         events_list = EventDetails.objects.filter(is_deleted=False).order_by('event_type')
#         event_type_list = EventType.objects.filter(is_deleted=False).order_by('event_type')
#         data = {
#             'success':'true',
#             'committee_list':committee_list,
#             'events_list':events_list,
#             'event_type_list':event_type_list
#         }
#     except Exception as e:
#         print 'Exception | event_landing | events_home | user %s. Exception = ', str(traceback.print_exc())
#         data = {'success':'false'}

#     return render(request, 'backoffice/events/event_details.html',data)    

# @csrf_exempt
# def get_events_datatable(request): 

#     try:
#         print 'backofficeapp | event_home.py | get_events_datatable | user'
#         dataList = []

#         total_record=0
#         column = request.GET.get('order[0][column]')
#         searchTxt = request.GET.get('search[value]')
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['','organising_committee__committee','event_title']
#         column_name = order + list[int(column)]
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))

#         event_detail_objs_list = EventDetails.objects.filter(is_deleted=False)#.order_by(column_name)
#         print '.',event_detail_objs_list
#         if request.GET.get('select_status'):
#             event_detail_objs_list = event_detail_objs_list.filter(event_status=request.GET.get('select_status'))
#         if request.GET.get('committee'):
#             event_detail_objs_list = event_detail_objs_list.filter(organising_committee=request.GET.get('committee'))
#         if request.GET.get('events'):
#             event_detail_objs_list = event_detail_objs_list.filter(id=request.GET.get('events'))
#         if request.GET.get('event_type'):
#             event_detail_objs_list = event_detail_objs_list.filter(event_type=request.GET.get('event_type'))

#         total_record=event_detail_objs_list.count()
#         event_detail_objs_list = event_detail_objs_list.filter().order_by(column_name)[start:length]
        

#         i = 0
#         for obj in event_detail_objs_list: 
#             print obj.id
#             # For reflecting release date impact on visibility of event
#             release_date = obj.release_date.strftime('%d %B %Y - %H:%M')
#             release_date = datetime.strptime(release_date, '%d %B %Y - %H:%M')
#             today_date = datetime.today().strftime('%d %B %Y - %H:%M')
#             today_date = datetime.strptime(today_date, '%d %B %Y - %H:%M')
#             if release_date <= today_date:
#                 obj.view_status = 1
#                 obj.save()

#             to_date = obj.to_date.strftime('%d %B %Y - %H:%M')
#             to_date = datetime.strptime(to_date, '%d %B %Y - %H:%M')

#             if to_date <= today_date:
#                 obj.view_status = 0
#                 obj.event_status = 1
#                 obj.save()


#             i = i + 1 
#             tempList = []   
#             # when_to_attend = obj.from_date.strftime('%B %d, %Y') + ' ' + obj.from_time.strftime('%H:%M:%p') + ' - ' + obj.to_date.strftime('%B %d, %Y') + ' ' + obj.to_time.strftime('%H:%M:%p')
#             when_to_attend = obj.from_date.strftime('%B %d, %Y') + ' - ' + obj.to_date.strftime('%B %d, %Y')

#             action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/backofficeapp/edit-event/?event_detail='+str(obj.id)+'"></a>&nbsp;&nbsp;'

#             if obj.event_status == 1:
#                 event_status = 'Inactive'
#                 status = '<label class="label label-default"> Inactive </label>'
#                 action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_details(' + '"' + str(
#                     event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
#             else:
#                 event_status = 'Active'
#                 status = '<label class="label label-success"> Active </label>'
#                 action2= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_details(' + '"' + str(
#                     event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
                
#             if obj.hall_details:
#                 hall_location = obj.hall_details.hall_location.location
#             else:
#                 hall_location = obj.other_location_address

#             tempList.append(i)
#             tempList.append(obj.organising_committee.committee)
#             tempList.append(obj.event_title)
#             tempList.append(obj.event_type.event_type)
#             tempList.append(when_to_attend)            
#             tempList.append(hall_location)
#             tempList.append(status)
#             tempList.append(action1 + action2)

#             dataList.append(tempList)
#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
#     except Exception as e:
#         print 'Exception backofficeapp | event_home.py | get_events_datatable | user %s. Exception = ', str(traceback.print_exc())
#         data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': []}
#     return HttpResponse(json.dumps(data), content_type='application/json')  

# @transaction.atomic
# def update_event_detail_status(request):
#     data = {}
#     sid = transaction.savepoint()
#     try:
#         eventobj = EventDetails.objects.get(id=str(request.GET.get('event_details_id')))
#         if eventobj.event_status == 0:
#             eventobj.event_status = 1
#             EventRegistration.objects.filter(event=eventobj,is_deleted=False).update(is_active=False,register_status=1)
#             EventParticipantUser.objects.filter(event_user__event=eventobj,is_deleted=False).update(is_active=False,register_status=1)
#         else:
#             eventobj.event_status = 0
#             EventRegistration.objects.filter(event=eventobj,is_deleted=False).update(is_active=True,register_status=0)
#             EventParticipantUser.objects.filter(event_user__event=eventobj,is_deleted=False).update(is_active=True,register_status=0)
#         eventobj.save()
#         transaction.savepoint_commit(sid)
#         data = {'success': 'true'}
#     except Exception,e:
#         print '\nException | update_event_detail_status = ', str(traceback.print_exc())
#         data = {'success': 'false'}
#         transaction.rollback(sid)
#     return HttpResponse(json.dumps(data), content_type='application/json')


# @csrf_exempt
# def add_new_event(request):
#     try:
#         request.session['event_banner_id'] = ''
#         request.session['event_sponsor_id'] = ''
#         committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')        
#         event_type_list = EventType.objects.filter(is_deleted=False).order_by('event_type')
#         system_user_list = SystemUserProfile.objects.filter(is_deleted=False).order_by('username')
#         hall_location_list = HallLocation.objects.filter(is_deleted=False).order_by('location')
#         data = {
#             'success':'true',
#             'committee_list':committee_list,
#             'event_type_list':event_type_list,
#             'system_user_list':system_user_list,
#             'hall_location_list':hall_location_list
#         }
#     except Exception as e:
#         print 'Exception | event_landing | events_home | user %s. Exception = ', str(traceback.print_exc())
#         data ={'success':'false'}        
    
#     return render(request, 'backoffice/events/add_new_event.html',data)

# def get_contact_person(request):
#     try:
#         committee_obj = Committee.objects.get(id=request.GET.get('commitee_id'))
#         contact_person_obj1 = SystemUserProfile.objects.get(id=committee_obj.contact_person1.id, is_deleted=False)
#         try:
#             contact_person_obj2 = SystemUserProfile.objects.get(id=committee_obj.contact_person2.id, is_deleted=False)
#             contact_person_obj2 = contact_person_obj2.id
#         except Exception as e:
#             contact_person_obj2 = ''
#             print e
#             pass
        
#         data ={
#             'success':'true',
#             'contact_person_obj1':contact_person_obj1.id,
#             'contact_person_obj2':contact_person_obj2
#         }
#     except Exception, e:
#         print 'Exception ', e
#         data = {'success':'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')   

# def get_program_details(request):
#     try:
#         event_object = EventDetails.objects.get(id=request.GET.get('event_detail_id'))
#         event_description_indetails = event_object.event_description_indetails
        
#         data ={
#             'success':'true',
#             'event_description_indetails':event_description_indetails
#         }
#     except Exception, e:
#         print 'Exception ', e
#         data = {'success':'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')       


# def get_hall_name(request):
#     try:
#         hall_name_list = []
#         hall_obj_list = HallDetail.objects.filter(hall_location_id=request.GET.get('event_location_id'))
#         for obj in hall_obj_list:            
#             hall_name_list.append(
#                 {'id': obj.id, 'hall_name': obj.hall_name})
#         data ={
#             'success':'true',
#             'hall_name_list':hall_name_list,
#         }
#     except Exception, e:
#         print 'Exception ', e
#         data = {'success':'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')  

# def get_hall_location(request):
#     locations=[]
#     try:
#         hall_obj = HallDetail.objects.get(id=request.GET.get('hall_id'))
        
#         try:
#             location = {'lat': hall_obj.latitude,
#                     'lon': hall_obj.longitude,
#                     'zoom': 8,
#                     'title': hall_obj.hall_name,
#                     'html': '<h5>' + hall_obj.hall_name + '</h5>',
#                     'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
#                     }
#             locations.append(location)
#         except Exception,e:
#             pass

#         print locations
#         data ={
#             'success':'true',
#             'locations':locations
#         }
#     except Exception, e:
#         print 'Exception ', e
#         data = {'success':'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')        
 
# def get_location(request):
#     locations=[]
#     data={}
#     addresslist=[]
#     try:
#         zone=request.GET.get('zone')
#         city=request.GET.get('city')
#         if zone == "All":
#             contact_objs = CSDCenters.objects.filter(city_id=city)
#         else:
#             contact_objs=CSDCenters.objects.filter(zone_id=zone)

#         contactdetail_obj=ContactDetail.objects.all()
#         contacts={}
#         if contact_objs and contactdetail_obj:
#             contactdetail_obj=contactdetail_obj.last()
#             try:
#                 contacts={
#                             'helpline_number':contactdetail_obj.helpline_number if contactdetail_obj.helpline_number else "NA",
#                             'anti_bribery_help':contactdetail_obj.anti_bribery_help if contactdetail_obj.anti_bribery_help else "NA",
#                             'online_complaint':contactdetail_obj.online_complaint if contactdetail_obj.online_complaint else "NA",
#                             'igrc_email':contactdetail_obj.igrc_email if contactdetail_obj.igrc_email else "NA",
#                             'customer_portal':contactdetail_obj.customer_portal if contactdetail_obj.customer_portal else "NA",
#                             'electricity_theft_help_no':contactdetail_obj.electricity_theft_help_no if contactdetail_obj.electricity_theft_help_no else "NA",
#                             'igrc_no':contactdetail_obj.igrc_no if contactdetail_obj.igrc_no else "NA",
#                           }
#             except Exception,e:
#                 pass
#             for contact_obj in contact_objs:
#                 try:
#                     address_one = contact_obj.address  + ',<br/>' if contact_obj.address_two else contact_obj.address
#                     address_two = contact_obj.address_two + ',<br/>' if contact_obj.address_three else contact_obj.address_two
#                     address_three = contact_obj.address_three

#                     address={
#                            'address_one':address_one,
#                            'address_two':address_two,
#                            'address_three':address_three,
#                            'center_name':contact_obj.center_name
#                     }
#                     addresslist.append(address)
#                 except Exception,e:
#                     print e

#                     pass
#                 try:
#                     location = {'lat': contact_obj.latitude,
#                             'lon': contact_obj.longitude,
#                             'zoom': 12,
#                             'title': contact_obj.center_name,
#                             'html': '<h5>' + contact_obj.center_name + '</h5>',
#                             'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
#                             }
#                     locations.append(location)
#                 except Exception,e:
#                     pass

#             data={'success':'true','locations':locations,'address':address,'contacts':contacts,'hideflag':'flase','addresslist':addresslist,}
#         else:
#             data = {'success': 'true','hideflag':'true'}
#         return HttpResponse(json.dumps(data), content_type='application/json')
#     except Exception,e:
#         print e
#         pass


# @csrf_exempt
# def upload_event_banner(request):
#     try:
#         print 'Request In|backofficeapp |event_home.py |upload_event_banner |User %s Data'
#         attachment_file = EventBannerImage()
#         attachment_file.save()
#         attachment_file.document_files = request.FILES['event_file']
#         attachment_file.banner_type = 0
#         attachment_file.save()
#         request.session['event_banner_id'] = attachment_file.id
#         data = {'success': 'true'}

#         print 'Response Out|backofficeapp |event_home.py |upload_event_banner|User %s Data'
#     except Exception, exc:
#         print 'exception ', str(traceback.print_exc())
#         print "Exception In |  backofficeapp |event_home.py |upload_event_banner", exc
#         data = {'success': 'false', 'error': 'Exception ' + str(exc)}
#     return HttpResponse(json.dumps(data), content_type='application/json') 

# @csrf_exempt
# def upload_sponsor_banner(request):
#     try:
#         print 'Request In|backofficeapp |event_home.py |upload_sponsor_banner |User %s Data'
#         attachment_file = EventBannerImage()
#         attachment_file.save()
#         attachment_file.document_files = request.FILES['sponsor_file']
#         attachment_file.banner_type = 1
#         attachment_file.save()
#         request.session['event_sponsor_id'] = attachment_file.id
#         data = {'success': 'true'}

#         print 'Response Out|backofficeapp |event_home.py |upload_sponsor_banner|User %s Data'
#     except Exception, exc:
#         print 'exception ', str(traceback.print_exc())
#         print "Exception In |  backofficeapp |event_home.py |upload_sponsor_banner", exc
#         data = {'success': 'false', 'error': 'Exception ' + str(exc)}
#     return HttpResponse(json.dumps(data), content_type='application/json')  



# from django.contrib.sites.shortcuts import get_current_site
# from urlparse import urlparse
# from os.path import splitext
# def get_banner_file(request):
#     try:
#         print 'Request In|backofficeapp |event_home.py |get_banner_file |User %s Data'

#         if request.session['event_banner_id']:
#             event_banner_obj = EventBannerImage.objects.get(id=request.session['event_banner_id'])
#         else:
#             event_banner_obj = EventBannerImage.objects.get(event_detail_id=request.GET.get('event_details_id'),banner_type=0)
#         parsed = urlparse(event_banner_obj.document_files.url)
#         root, ext = splitext(parsed.path)
#         event_docs_address = "http://" + get_current_site(request).domain + event_banner_obj.document_files.url

#         # if request.session['event_sponsor_id']:
#         #     sponsor_banner_obj = EventBannerImage.objects.get(id=request.session['event_sponsor_id'])
#         # else:
#         #     sponsor_banner_obj = EventBannerImage.objects.get(event_detail_id=request.GET.get('event_details_id'),banner_type=1)
#         # parsed = urlparse(sponsor_banner_obj.document_files.url)
#         # root, ext = splitext(parsed.path)
#         # sponsor_docs_address = "http://" + get_current_site(request).domain + sponsor_banner_obj.document_files.url
        
#         data = {
#             'success': 'true',
#             'event_docs_address': event_docs_address, 
#             'sponsor_docs_address': '',            
#         }
#         print 'Response Out|backofficeapp |event_home.py |get_banner_file|User %s Data'
#     except Exception, e:
#         print "Exception In |  backofficeapp |event_home.py |get_banner_file", e
#         data = {'success': 'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')  



# from datetime import datetime 
# from dateutil import tz 
# @csrf_exempt
# def save_new_event(request):
#     print json.dumps(request.POST, indent=4)
#     #pdb.set_trace()
#     try:
#         print 'Request In|backofficeapp |event_home.py |save_new_event|User %s Data'

#         from_zone = tz.tzutc()
#         to_zone = tz.gettz('Asia/Kolkata')
#         utc_from_date = dateutil.parser.parse(str(request.POST.get('from_date')))
#         utc_from_date = utc_from_date.replace(tzinfo=from_zone)
#         final_from_date = utc_from_date.astimezone(to_zone)

#         utc_to_date = dateutil.parser.parse(str(request.POST.get('to_date')))
#         utc_to_date = utc_to_date.replace(tzinfo=from_zone)
#         final_to_date = utc_to_date.astimezone(to_zone)

#         utc_registr_start_date = dateutil.parser.parse(str(request.POST.get('registr_start_date')))
#         utc_registr_start_date = utc_registr_start_date.replace(tzinfo=from_zone)
#         final_registr_start_date = utc_registr_start_date.astimezone(to_zone)

#         utc_registr_end_date = dateutil.parser.parse(str(request.POST.get('registr_end_date')))
#         utc_registr_end_date = utc_registr_end_date.replace(tzinfo=from_zone)
#         final_registr_end_date = utc_registr_end_date.astimezone(to_zone)

#         utc_release_date = dateutil.parser.parse(str(request.POST.get('release_date')))
#         utc_release_date = utc_release_date.replace(tzinfo=from_zone)
#         final_release_date = utc_release_date.astimezone(to_zone)


#         if request.POST.get('early_bird_date'):
#             utc_early_bird_date = dateutil.parser.parse(str(request.POST.get('early_bird_date')))
#             utc_early_bird_date = utc_early_bird_date.replace(tzinfo=from_zone)
#             final_early_bird_date = utc_early_bird_date.astimezone(to_zone)   

#         is_early_bird = False
#         if request.POST.get('is_early_bird') == 'true':
#             is_early_bird = True

#         # For reflecting release date impact on visibility of event
#         release_date = datetime.strptime(request.POST.get('release_date'), "%d %B %Y - %H:%M")
#         release_date = release_date.strftime('%d %B %Y - %H:%M')
#         today_date = datetime.today().strftime('%d %B %Y - %H:%M')
#         view_status = 0
#         if release_date <= today_date:
#             view_status = 1
        
#         discount_1 = ''
#         discount_2 = ''
#         discount_3 = ''
#         if request.POST.get('disc_part_count1'):
#             discount_1 = request.POST.get('disc_part_count1') + '-' + request.POST.get('disc_perct1')
#         if request.POST.get('disc_part_count2'):
#             discount_2 = request.POST.get('disc_part_count2') + '-' + request.POST.get('disc_perct2')
#         if request.POST.get('disc_part_count3'):
#             discount_3 = request.POST.get('disc_part_count3') + '-' + request.POST.get('disc_perct3')

#         event_obj = EventDetails(
#                 event_description_indetails = request.POST.get('program_detail_id'),
#                 organising_committee = Committee.objects.get(id=request.POST.get('select_committee')),
#                 contact_person1 = SystemUserProfile.objects.get(id = request.POST.get('select_contact1')),
#                 contact_person2 = SystemUserProfile.objects.get(id = request.POST.get('select_contact2')) if request.POST.get('select_contact2') else None,
#                 priority = 0,#request.POST.get('select_priority'),
#                 event_type = EventType.objects.get(id = request.POST.get('select_event_type')),
#                 event_mode = request.POST.get('select_criteria'),
#                 online_payment = request.POST.get('select_payment'),
#                 event_title = request.POST.get('event_title'),
#                 hall_details = HallDetail.objects.get(id = request.POST.get('hall_id')) if request.POST.get('hall_id')!= ' ' else None,
#                 other_location_address = request.POST.get('other_location_address'),
#                 from_date = final_from_date,
#                 to_date = final_to_date,
#                 registration_start_date = final_registr_start_date,
#                 registration_end_date = final_registr_end_date,
#                 release_date = final_release_date,
#                 to_whom_description = request.POST.get('for_whom'),
#                 organised_by = request.POST.get('organised_by'),
#                 member_charges = request.POST.get('member_charges'),
#                 non_member_charges = request.POST.get('non_member_charges'),
#                 other_charges_name = request.POST.get('othercharge_name'),
#                 other_charges_amount = request.POST.get('othercharge_amt') if request.POST.get('othercharge_amt') else 0,

#                 is_early_bird = is_early_bird,
#                 early_member_charges = request.POST.get('early_member_charges') if request.POST.get('early_member_charges') else 0,
#                 early_non_member_charges = request.POST.get('early_non_member_charges') if request.POST.get('early_non_member_charges') else 0,
#                 early_bird_date = final_early_bird_date if request.POST.get('early_bird_date') else None,

#                 discount_1=discount_1,
#                 discount_2=discount_2,
#                 discount_3=discount_3,
#                 expected_members=request.POST.get('expected_member') if request.POST.get('expected_member') else 0,
#                 expected_nonmembers=request.POST.get('expected_nonmember') if request.POST.get('expected_nonmember') else 0,
#                 expected_freemembers=request.POST.get('expected_freemember') if request.POST.get('expected_freemember') else 0,
#                 expected_sponsored_members=request.POST.get('expected_sponsmember') if request.POST.get('expected_sponsmember') else 0,
#                 expected_capacity=request.POST.get('expected_capacity') if request.POST.get('expected_capacity') else 0,
#                 meta_title = request.POST.get('meta_title'),
#                 meta_keyword = request.POST.get('meta_keyword'),
#                 meta_description = request.POST.get('meta_description'),
#                 meta_keyphrases = request.POST.get('meta_key_phrase'),
#                 view_status = view_status,
#                 created_on = datetime.now(),
#             )
#         event_obj.save()        

#         if request.POST.get('promocode_list1'):
#             promocode_list1 = (request.POST.get('promocode_list1')).split(',')
#             promocode_list2 = (request.POST.get('promocode_list2')).split(',')
#             promocode_list3 = (request.POST.get('promocode_list3')).split(',')
#             promocode_list4 = (request.POST.get('promocode_list4')).split(',')
#             length_count=len(promocode_list1)

#             for obj in range(0, length_count):
#                 promocode_obj=PromoCode(
#                     event_details=event_obj,
#                     promo_code=promocode_list2[obj],
#                     for_whom=promocode_list1[obj],
#                     percent_discount=promocode_list3[obj],
#                     discounted_amount=promocode_list4[obj],
#                     #created_by=request.session['first_name'],
#                 )
#                 promocode_obj.save()

#         try:
#             attachment_obj1 = EventBannerImage.objects.get(id=request.session['event_banner_id'])
#             attachment_obj1.event_detail_id=event_obj
#             attachment_obj1.save()

#             # attachment_obj2 = EventBannerImage.objects.get(id=request.session['event_sponsor_id'])
#             # attachment_obj2.event_detail_id=event_obj
#             # attachment_obj2.save()

#         except Exception as e:
#             pass

#         attachment_list = request.POST.get('attachments')
#         save_attachments(attachment_list,event_obj,request)
        
#         print 'Response Out|backofficeapp |event_home.py |save_new_event|User %s Data'
#         data = {'success': 'true'}
#     except Exception, exc:
#         print 'exception ', str(traceback.print_exc())
#         print "Exception In |  backofficeapp |event_home.py |save_new_event", exc
#         data = {'success': 'false', 'error': 'Exception ' + str(exc)}
#     return HttpResponse(json.dumps(data), content_type='application/json')  

# import os
# def save_attachments(attachment_list, event_id,request):
#     try:
#         print 'backofficeapp |event_home.py|save_attachments'
#         attachment_list = attachment_list.split(',')
#         attachment_list = filter(None, attachment_list)
#         for attached_id in attachment_list:
#             attachment_obj = EventSponsorImage.objects.get(id=attached_id)
#             attachment_obj.event_id=event_id
#             attachment_obj.save()
#         data = {'success': 'true'}
#     except Exception, e:
#         print 'Exception|backofficeapp |event_home.py|save_attachments', e
#     return HttpResponse(json.dumps(data), content_type='application/json')


# @csrf_exempt
# def upload_sponsor_images(request):
#     try:
#         print 'backofficeapp|event_home.py|upload_sponsor_images'
#         if request.method == 'POST':
#             attachment_file = EventSponsorImage()
#             attachment_file.save()
#             request.FILES['file[]'].name = 'event_sponsor_image_' + str(attachment_file.id) + '_' + request.FILES[
#                 'file[]'].name
                       
#             attachment_file.document_files = request.FILES['file[]']
#             attachment_file.save()
#             data = {'success': 'true', 'attachid': attachment_file.id}
#         else:
#             data = {'success': 'false'}
#     except MySQLdb.OperationalError, e:
#         print 'Exception|backofficeapp|event_home.py|upload_sponsor_images', e
#         data = {'success': 'invalid request'}
#     return HttpResponse(json.dumps(data), content_type='application/json')

# @csrf_exempt
# def remove_sponsor_images(request):
#     try:
#         print 'backofficeapp|event_home.py|remove_sponsor_images'
#         image_id = request.GET.get('image_id')
#         image = EventSponsorImage.objects.get(id=image_id)
#         image.delete()

#         data = {'success': 'true'}
#     except MySQLdb.OperationalError, e:
#         print 'Exception|backofficeapp|event_home.py|remove_sponsor_images', e
#         data = {'success': 'false'}
#     return HttpResponse(json.dumps(data), content_type='application/json')

# @csrf_exempt
# def edit_event(request):
#     try:
#         request.session['event_banner_id'] = ''
#         request.session['event_sponsor_id'] = ''
#         print '>>>>>>>>>>>>',request.GET.get('event_detail')
#         event_obj = EventDetails.objects.get(id=request.GET.get('event_detail'))
#         committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')        
#         event_type_list = EventType.objects.filter(is_deleted=False).order_by('event_type')
#         system_user_list = SystemUserProfile.objects.filter(is_deleted=False).order_by('username')
#         hall_location_list = HallLocation.objects.filter(is_deleted=False).order_by('location')

#         hall_name_list = []
#         if event_obj.hall_details:
#             hall_name_list = HallDetail.objects.filter(hall_location = event_obj.hall_details.hall_location,is_deleted=False,is_active=True).order_by('hall_name')

#         image_count=0
#         sponsor_images = EventSponsorImage.objects.filter(event_id=event_obj.id,is_deleted=False)
#         docs_address = ''
#         image_id = ''
#         if sponsor_images:
#             image_count = sponsor_images.count()
#             c=1
#             for image in sponsor_images:
#                 if c==1:
#                     c = 2
#                     docs_address = 'http://' + get_current_site(request).domain + image.document_files.url
#                     image_id = str(image.id)
#                 else:

#                     docs_address = docs_address + ',' + 'http://' + get_current_site(request).domain + image.document_files.url
#                     image_id = image_id + ',' + str(image.id)



#         event_banner_obj = EventBannerImage.objects.get(event_detail_id=event_obj,banner_type=0)
#         parsed = urlparse(event_banner_obj.document_files.url)
#         root, ext = splitext(parsed.path)
#         event_docs_address = "http://" + get_current_site(request).domain + event_banner_obj.document_files.url

#         # sponsor_banner_obj = EventBannerImage.objects.get(event_detail_id=event_obj,banner_type=1)
#         # parsed = urlparse(sponsor_banner_obj.document_files.url)
#         # root, ext = splitext(parsed.path)
#         # sponsor_docs_address = "http://" + get_current_site(request).domain + sponsor_banner_obj.document_files.url


#         discount_part1 = event_obj.discount_1.split('-')[0] if event_obj.discount_1 else ''
#         discount_percent1 = event_obj.discount_1.split('-')[1] if event_obj.discount_1 else ''
#         discount_part2 = event_obj.discount_2.split('-')[0] if event_obj.discount_2 else ''
#         discount_percent2 = event_obj.discount_2.split('-')[1] if event_obj.discount_2 else ''
#         discount_part3 = event_obj.discount_3.split('-')[0] if event_obj.discount_3 else ''
#         discount_percent3 = event_obj.discount_3.split('-')[1] if event_obj.discount_3 else ''

#         if event_obj.hall_details:
#            hall_details_id = event_obj.hall_details.id
#            hall_location_id = event_obj.hall_details.hall_location.id
#            hall_location = event_obj.hall_details.hall_location.location
#         else:
#             hall_details_id = ''
#             hall_location_id = ''
#             hall_location = ''

#         print '>>>>>>>>>>>>>>',event_obj.early_bird_date

        
#         is_promocode = False
#         promocode_obj_list = []
#         promocode_obj_list = PromoCode.objects.filter(event_details=event_obj,status=True,is_deleted=False)
#         if promocode_obj_list:
#             is_promocode = True
        
#         print '>>>>>>>>>>>>>>>',is_promocode
#         print '><<<<<<<<<<<<<<<<<<<<<,',promocode_obj_list
#         data = {
#             'success':'true',   
#             'image_list': docs_address,
#             'image_count': image_count,
#             'image_id_list': image_id,
#             'hall_location_id':hall_location_id,
#             'hall_location_list':hall_location_list,
#             'hall_details_id':hall_details_id,
#             'other_location_address':event_obj.other_location_address,
#             'hall_name_list':hall_name_list,
#             'event_detail_id':request.GET.get('event_detail'),        
#             'committee_list':committee_list,
#             'event_type_list':event_type_list,
#             'system_user_list':system_user_list,
#             'committee_id':event_obj.organising_committee.id,
#             'contact_person1_id':event_obj.contact_person1.id,
#             'contact_person2_id':event_obj.contact_person2.id if event_obj.contact_person2 else None,
#             'priority':event_obj.priority,
#             'event_type_id':event_obj.event_type.id,
#             'entry_criteria':event_obj.event_mode,
#             'online_payment':event_obj.online_payment,
#             'expected_capacity':event_obj.expected_capacity,
#             'event_title':event_obj.event_title,
#             'event_location':hall_location,
#             'from_date':event_obj.from_date.strftime('%d %B %Y - %H:%M'),
#             'to_date':event_obj.to_date.strftime('%d %B %Y - %H:%M'),
#             'registration_start_date':event_obj.registration_start_date.strftime('%d %B %Y - %H:%M'),
#             'registration_end_date':event_obj.registration_end_date.strftime('%d %B %Y - %H:%M'),
#             'release_date':event_obj.release_date.strftime('%d %B %Y - %H:%M'),
#             'to_whom_description':event_obj.to_whom_description,
#             'organised_by':event_obj.organised_by,
#             'member_charges':event_obj.member_charges,
#             'non_member_charges':event_obj.non_member_charges,

#             'discount_part1':discount_part1,
#             'discount_percent1':discount_percent1,
#             'discount_part2':discount_part2,
#             'discount_percent2':discount_percent2,
#             'discount_part3':discount_part3,
#             'discount_percent3':discount_percent3,

#             'is_early_bird':event_obj.is_early_bird,
#             'early_member_charges':event_obj.early_member_charges,
#             'early_non_member_charges':event_obj.early_non_member_charges,
#             'early_bird_date':event_obj.early_bird_date.strftime('%d %B %Y - %H:%M') if event_obj.early_bird_date else '',

#             'is_promocode':is_promocode,
#             'promocode_obj_list':promocode_obj_list,

#             'expected_member':event_obj.expected_members,
#             'expected_nonmember':event_obj.expected_nonmembers,
#             'expected_freemember':event_obj.expected_freemembers,
#             'expected_sponsored_member':event_obj.expected_sponsored_members,
#             'other_charges_name':event_obj.other_charges_name,
#             'other_charges_amount':event_obj.other_charges_amount,
#             'event_docs_address':event_docs_address,
#             'sponsor_docs_address':'',
#             'meta_title':event_obj.meta_title,
#             'meta_keyword':event_obj.meta_keyword,
#             'meta_description':event_obj.meta_description,
#             'meta_keyphrases':event_obj.meta_keyphrases
#         }
#     except Exception as e:
#         print 'Exception | event_landing | events_home | user %s. Exception = ', str(traceback.print_exc())
#         data ={'success':'false'}        
    
#     return render(request, 'backoffice/events/edit_event.html',data)


# @csrf_exempt
# def update_event(request): 
#     try:
#         print 'Request In|backofficeapp |event_home.py |update_event|User %s Data'
#         from_zone = tz.tzutc()
#         to_zone = tz.gettz('Asia/Kolkata')
#         utc_from_date = dateutil.parser.parse(str(request.POST.get('from_date')))
#         utc_from_date = utc_from_date.replace(tzinfo=from_zone)
#         final_from_date = utc_from_date.astimezone(to_zone)

#         utc_to_date = dateutil.parser.parse(str(request.POST.get('to_date')))
#         utc_to_date = utc_to_date.replace(tzinfo=from_zone)
#         final_to_date = utc_to_date.astimezone(to_zone)

#         utc_registr_start_date = dateutil.parser.parse(str(request.POST.get('registr_start_date')))
#         utc_registr_start_date = utc_registr_start_date.replace(tzinfo=from_zone)
#         final_registr_start_date = utc_registr_start_date.astimezone(to_zone)

#         utc_registr_end_date = dateutil.parser.parse(str(request.POST.get('registr_end_date')))
#         utc_registr_end_date = utc_registr_end_date.replace(tzinfo=from_zone)
#         final_registr_end_date = utc_registr_end_date.astimezone(to_zone)

#         utc_release_date = dateutil.parser.parse(str(request.POST.get('release_date')))
#         utc_release_date = utc_release_date.replace(tzinfo=from_zone)
#         final_release_date = utc_release_date.astimezone(to_zone)

#         if request.POST.get('early_bird_date'):
#             utc_early_bird_date = dateutil.parser.parse(str(request.POST.get('early_bird_date')))
#             utc_early_bird_date = utc_early_bird_date.replace(tzinfo=from_zone)
#             final_early_bird_date = utc_early_bird_date.astimezone(to_zone)   

#         is_early_bird = False
#         if request.POST.get('is_early_bird') == 'true':
#             is_early_bird = True

#         # For reflecting release date impact on visibility of event
#         release_date = datetime.strptime(request.POST.get('release_date'), "%d %B %Y - %H:%M")
#         release_date = release_date.strftime('%d %B %Y - %H:%M')
#         today_date = datetime.today().strftime('%d %B %Y - %H:%M')
#         view_status = 0
#         if release_date <= today_date:
#             view_status = 1

#         to_date = datetime.strptime(request.POST.get('to_date'), "%d %B %Y - %H:%M")
#         to_date = to_date.strftime('%d %B %Y - %H:%M')

#         event_status = 0
#         if to_date <= today_date:
#             event_status = 1

#         discount_1 = ''
#         discount_2 = ''
#         discount_3 = ''
#         if request.POST.get('disc_part_count1'):
#             discount_1 = request.POST.get('disc_part_count1') + '-' + request.POST.get('disc_perct1')
#         if request.POST.get('disc_part_count2'):
#             discount_2 = request.POST.get('disc_part_count2') + '-' + request.POST.get('disc_perct2')
#         if request.POST.get('disc_part_count3'):
#             discount_3 = request.POST.get('disc_part_count3') + '-' + request.POST.get('disc_perct3')



#         event_obj = EventDetails.objects.get(id=request.POST.get('event_details_id'))

#         event_obj.hall_details = HallDetail.objects.get(id = request.POST.get('hall_id')) if request.POST.get('hall_id') != ' ' else None
#         event_obj.other_location_address = request.POST.get('other_location_address')
#         event_obj.event_description_indetails = request.POST.get('program_detail_id')
#         event_obj.organising_committee = Committee.objects.get(id=request.POST.get('select_committee'))
#         event_obj.contact_person1 = SystemUserProfile.objects.get(id = request.POST.get('select_contact1'))
#         event_obj.contact_person2 = SystemUserProfile.objects.get(id = request.POST.get('select_contact2')) if request.POST.get('select_contact2') else None
#         event_obj.priority = 0#request.POST.get('select_priority')
#         event_obj.event_type = EventType.objects.get(id = request.POST.get('select_event_type'))
#         event_obj.event_mode = request.POST.get('select_criteria')
#         event_obj.online_payment = request.POST.get('select_payment')
#         event_obj.event_title = request.POST.get('event_title')
#         event_obj.event_location = request.POST.get('event_location')
#         event_obj.from_date = final_from_date
#         event_obj.to_date = final_to_date
#         event_obj.registration_start_date = final_registr_start_date
#         event_obj.registration_end_date = final_registr_end_date
#         event_obj.release_date = final_release_date
#         event_obj.to_whom_description = request.POST.get('for_whom')
#         event_obj.organised_by = request.POST.get('organised_by')
#         event_obj.member_charges = request.POST.get('member_charges')
#         event_obj.non_member_charges = request.POST.get('non_member_charges')
#         event_obj.expected_capacity = request.POST.get('expected_capacity') if request.POST.get('expected_capacity') else 0 
#         event_obj.other_charges_name = request.POST.get('othercharge_name')
#         event_obj.other_charges_amount = request.POST.get('othercharge_amt') if request.POST.get('othercharge_amt') else 0 

#         event_obj.is_early_bird = is_early_bird
#         event_obj.early_member_charges = request.POST.get('early_member_charges') if request.POST.get('early_member_charges') else 0
#         event_obj.early_non_member_charges = request.POST.get('early_non_member_charges') if request.POST.get('early_non_member_charges') else 0
#         event_obj.early_bird_date = final_early_bird_date if request.POST.get('early_bird_date') else None

#         event_obj.discount_1 = discount_1
#         event_obj.discount_2 = discount_2
#         event_obj.discount_3 = discount_3
#         event_obj.expected_members = request.POST.get('expected_member') if request.POST.get('expected_member') else 0 
#         event_obj.expected_nonmembers = request.POST.get('expected_nonmember') if request.POST.get('expected_nonmember') else 0 
#         event_obj.expected_freemembers = request.POST.get('expected_freemember') if request.POST.get('expected_freemember') else 0 
#         event_obj.expected_sponsmembers = request.POST.get('expected_sponsmember') if request.POST.get('expected_sponsmember') else 0 
#         event_obj.meta_title = request.POST.get('meta_title')
#         event_obj.meta_keyword = request.POST.get('meta_keyword')
#         event_obj.meta_description = request.POST.get('meta_description')
#         event_obj.meta_keyphrases = request.POST.get('meta_key_phrase')
#         event_obj.view_status = view_status
#         event_obj.event_status = event_status
            
#         event_obj.save()  

#         attachment_list = request.POST.get('attachments')
#         save_edit_attachments(attachment_list, event_obj)

#         PromoCode.objects.filter(event_details_id=event_obj.id,status=True,is_deleted=False).delete()
#         if request.POST.get('promocode_list1'):                    

#             promocode_list1 = (request.POST.get('promocode_list1')).split(',')
#             promocode_list2 = (request.POST.get('promocode_list2')).split(',')
#             promocode_list3 = (request.POST.get('promocode_list3')).split(',')
#             promocode_list4 = (request.POST.get('promocode_list4')).split(',')
#             length_count=len(promocode_list1)

#             for obj in range(0, length_count):
#                 promocode_obj=PromoCode(
#                     event_details=event_obj,
#                     promo_code=promocode_list2[obj],
#                     for_whom=promocode_list1[obj],
#                     percent_discount=promocode_list3[obj],
#                     discounted_amount=promocode_list4[obj],
#                     #created_by=request.session['first_name'],
#                 )
#                 promocode_obj.save()


#         # DELETE banner docs
#         try:
#             if request.session['event_banner_id']:
#                 print '>>>>>>>>...11'
#                 EventBannerImage.objects.filter(event_detail_id=event_obj.id,banner_type=0).delete()
#                 attachment_obj1 = EventBannerImage.objects.get(id=request.session['event_banner_id'])
#                 attachment_obj1.event_detail_id=event_obj
#                 attachment_obj1.save()
#             # if request.session['event_sponsor_id']:
#             #     print ">>>>>>>>...222"
#             #     EventBannerImage.objects.filter(event_detail_id=event_obj.id,banner_type=1).delete()
#             #     attachment_obj2 = EventBannerImage.objects.get(id=request.session['event_sponsor_id'])
#             #     attachment_obj2.event_detail_id=event_obj
#             #     attachment_obj2.save()

#         except Exception as e:
#             pass
 
#         print 'Response Out|backofficeapp |event_home.py |update_event|User %s Data'
#         data = {'success': 'true'}
#     except Exception, exc:
#         print 'exception ', str(traceback.print_exc())
#         print "Exception In |  backofficeapp |event_home.py |update_event", exc
#         data = {'success': 'false', 'error': 'Exception ' + str(exc)}
#     return HttpResponse(json.dumps(data), content_type='application/json') 


# def save_edit_attachments(attachment_list, event_id):
#     try:
#         print 'backofficeapp |event_home.py|save_edit_attachments'
#         attachment_list = attachment_list.split(',')
#         attachment_list = filter(None, attachment_list)
#         EventSponsorImage.objects.filter(event_id=event_id).exclude(id__in=attachment_list).update(event_id=None)
#         for attached_id in attachment_list:
#             attachment_obj = EventSponsorImage.objects.get(id=attached_id)
#             attachment_obj.event_id = event_id
#             attachment_obj.save()

#         data = {'success': 'true'}
#     except Exception, e:
#         print 'Exception|backofficeapp |event_home.py|save_edit_attachments', e
#     return HttpResponse(json.dumps(data), content_type='application/json')


# @csrf_exempt
# def event_registrations(request):
#     committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')
#     event_list = EventDetails.objects.filter(event_status=0,is_deleted=False).order_by('event_title')
#     data={'committee_list':committee_list,'event_list':event_list}
#     return render(request, 'backoffice/events/event_registrations.html',data)        


# @csrf_exempt
# def get_events_registrations_datatable(request):
#     try:
#         print 'backofficeapp | event_home.py | get_events_registrations_datatable | user'
#         dataList = []
#         total_record=0
#         column = request.GET.get('order[0][column]')
#         searchTxt = request.GET.get('search[value]')
#         print searchTxt
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['id', 'event__organising_committee__committee', 'event__event_title']
#         column_name = order + list[int(column)]
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))

#         event_detail_objs_list = EventDetails.objects.filter(is_deleted=False)  # .order_by(column_name)
#         print event_detail_objs_list
#         # if request.GET.get('select_status'):
#         #     event_detail_objs_list = event_detail_objs_list.filter(event_status=request.GET.get('select_status'))
#         if request.GET.get('select_committee'):
#             event_detail_objs_list = event_detail_objs_list.filter(organising_committee=request.GET.get('select_committee'))
#         if request.GET.get('select_event'):
#             event_detail_objs_list = event_detail_objs_list.filter(id=request.GET.get('select_event'))
#         # if request.GET.get('event_type'):
#         #     event_detail_objs_list = event_detail_objs_list.filter(event_type=request.GET.get('event_type'))

#         # if request.GET.get('select_payment'):
#         #     event_detail_objs_list = event_detail_objs_list.filter(id=request.GET.get('select_event'))
#         if request.GET.get('select_payment'):
#             eventregs=EventRegistration.objects.filter(event__id__in=[event.id for event in event_detail_objs_list],payment_status=request.GET.get('select_payment'),is_deleted=False)
#         else:
#             eventregs = EventRegistration.objects.filter(event__id__in=[event.id for event in event_detail_objs_list],is_deleted=False)

#         if request.GET.get('start_date') and request.GET.get('end_date'):
#             start_date = datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
#             end_date = datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59, second=59)
#             eventregs = eventregs.filter(created_on__range=[start_date, end_date])

#         if searchTxt:
#             eventregs = eventregs.filter((Q(reg_no__icontains=searchTxt)|Q(contact_person_name__icontains=searchTxt)))

#         total_record= eventregs.count()

#         eventregs = eventregs.order_by(column_name)[start:length]

#         for eventreg in eventregs:
#             view_action = '<a class="fa fa-file-text-o" title="Details" onclick="OpenDetailsView('+ str(
#                 eventreg.id)+');"></a>&nbsp;&nbsp;'

#             download_action = '<a class="fa fa-file-pdf-o" target="_blank" title="Receipt" href="/backofficeapp/events-reciept/?event_reg_id=' + str(eventreg.id) + '"></a>'


#             edit_action = '<a class="icon-pencil" target="_blank" title="Edit" href="/eventsapp/edit-events-details/?event_reg_id=' + str(
#             eventreg.id) + '"></a>&nbsp;' + '&nbsp;'

#             if eventreg.register_status == 1:
#                 event_reg_status = 'Inactive'
#                 status = '<label class="label label-default"> Inactive </label>'
#                 action2 = '<a class="icon-reload" title="Activate Registration" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_registraions(' + '"' + str(
#                     event_reg_status) + '"' + ',' + str(eventreg.id) + ')></a>&nbsp; &nbsp;'
#             else:
#                 event_reg_status = 'Active'
#                 status = '<label class="label label-success"> Active </label>'
#                 action2= '<a class="icon-trash" title="Cancel Registration" data-toggle="modal" data-target="#active_deactive_events" onclick=update_event_registraions(' + '"' + str(
#                     event_reg_status) + '"' + ',' + str(eventreg.id) + ')></a>&nbsp; &nbsp;'


#             payment_status = '-'
#             print '....1.....',eventreg.id
#             print '.............',eventreg.event.get_event_mode_display()
#             if eventreg.event.get_event_mode_display() == 'On Payment':
#                 payment_status = eventreg.get_payment_status_display() 

#             tempList = []
#             tempList.append(eventreg.id)
#             tempList.append(eventreg.created_on.strftime('%B %d,%Y'))
#             tempList.append(eventreg.reg_no)
#             tempList.append(eventreg.event.event_title)
#             tempList.append(eventreg.name_of_organisation)
#             tempList.append(str(eventreg.no_of_participant))
#             tempList.append(eventreg.total_amount)
#             tempList.append(payment_status)
#             tempList.append(view_action + download_action)
#             tempList.append(edit_action + action2) 
      
#             dataList.append(tempList)
#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
#     except Exception as e:
#         print 'Exception backofficeapp | event_home.py | get_events_registrations_datatable | user %s. Exception = ', str(traceback.
#             print_exc())
#         data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': [ ]}
#     return HttpResponse(json.dumps(data), content_type='application/json')


# @transaction.atomic
# def update_event_reg_status(request):
#     data = {}
#     sid = transaction.savepoint()
#     try:
#         eventobj = EventRegistration.objects.get(id=str(request.GET.get('event_reg_id')))
#         if eventobj.register_status == 0:
#             eventobj.register_status = 1
#         else:
#             eventobj.register_status = 0

#         eventobj.save()
#         transaction.savepoint_commit(sid)
#         data = {'success': 'true'}
#     except Exception,e:
#         print '\nException | update_event_reg_status = ', str(traceback.print_exc())
#         data = {'success': 'false'}
#         transaction.rollback(sid)
#     return HttpResponse(json.dumps(data), content_type='application/json')

# def get_event_registrations_details(request):
#     try:
#         eventreg_id = request.GET.get('eventreg_id')

#         eventreg_obj = EventRegistration.objects.get(id=eventreg_id)

#         membership_no = '-'
#         if eventreg_obj.is_member == True:
#             membership_no = eventreg_obj.user_details.member_associate_no
            
#         event_date = eventreg_obj.event.from_date.strftime('%B %d, %Y %H:%M:%p') + ' To ' + eventreg_obj.event.to_date.strftime('%B %d, %Y %H:%M:%p')

#         payble_amt = eventreg_obj.total_amount 
#         if eventreg_obj.is_member == True:
#             event_fee = eventreg_obj.event.member_charges
#         elif eventreg_obj.is_other == True:
#             event_fee = eventreg_obj.event.other_charges_amount            
#         else:
#             event_fee = eventreg_obj.event.non_member_charges


#         event_fee = float(event_fee)*float(eventreg_obj.no_of_participant)

#         cheque_date = ''
#         if eventreg_obj.cheque_date:
#             cheque_date = eventreg_obj.cheque_date.strftime('%B %d, %Y')

#         payment_status = 'NA'
#         total_discount_amount = 'NA'
#         if eventreg_obj.event.get_event_mode_display() == 'On Payment':
#             payment_status = eventreg_obj.get_payment_status_display() 
#             total_discount_amount = eventreg_obj.total_discount_amount

#         data = {
#             'success':'true',
#             'id':eventreg_obj.id,
#             'event_title':eventreg_obj.event.event_title,
#             'event_date':event_date,
#             'event_location':eventreg_obj.event.hall_details.hall_location.location,
#             'reg_no':eventreg_obj.reg_no,
#             'reg_date':eventreg_obj.created_on.strftime('%B %d, %Y'),
#             'membership_no':membership_no,
#             'name_of_org':eventreg_obj.name_of_organisation,
#             'no_of_participant':eventreg_obj.no_of_participant,
#             'discount':total_discount_amount,
#             'payble_amt':payble_amt,
#             'event_fee':event_fee,
#             'gst_amt':eventreg_obj.extra_gst_amount,
#             'payment_status':payment_status,
#             'payment_method':eventreg_obj.get_payment_method_display(),
#             'event_mode':eventreg_obj.event.get_event_mode_display(),
#             'cash_receipt_no':eventreg_obj.cash_receipt_no,
#             'cheque_no':eventreg_obj.cheque_no,
#             'bank_name':eventreg_obj.bank_name,
#             'cheque_date':cheque_date,
#             'trasanction_id':eventreg_obj.trasanction_id        
#         }
#     except Exception, e:
#         print 'Exception|backofficeapp | event_home.py|get_event_registrations_details', e
#         data = {
#             'success': 'false',
#             'message': str(e)
#         }
#     return HttpResponse(json.dumps(data), content_type='application/json')


# @csrf_exempt
# def get_model_registrations_datatable(request):
#     try:
#         print 'backofficeapp | event_home.py | get_model_registrations_datatable | user'
#         dataList = []
#         total_record=0
#         column = request.GET.get('order[0][column]')
#         searchTxt = request.GET.get('search[value]')
#         print searchTxt
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         list = ['id', 'event__organising_committee__committee', 'event__event_title']
#         column_name = order + list[int(column)]
#         print '>>>>>>>>>>>>>>>>',column_name
#         start = request.GET.get('start')
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))

#         eventregpart_list = EventParticipantUser.objects.filter(event_user=request.GET.get('registration_id'))

#         total_record = eventregpart_list.count()

#         # eventregpart_list = eventregpart_list.order_by(column_name)[start:length]

#         for eventpart in eventregpart_list:
#             tempList = []
#             tempList.append(eventpart.event_user_name)
#             tempList.append(eventpart.contact_no)
#             tempList.append(eventpart.email_id)
#             tempList.append(eventpart.designation)
      
#             dataList.append(tempList)
#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
#     except Exception as e:
#         print 'Exception backofficeapp | event_home.py | get_model_registrations_datatable | user %s. Exception = ', str(traceback.
#             print_exc())
#         data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': [ ]}
#     return HttpResponse(json.dumps(data), content_type='application/json')


# # def get_events_registration_receipt(request):
# #     try:
# #         # pdb.set_trace()
# #         membership_certificate_dispatched_obj = UserDetail.objects.get(id=request.GET.get('mem_cert_dispatch_id'))
# #         data = {'success': 'true'}
# #         template = get_template('backoffice/membership/membership_certificate.html')
# #         html = template.render(data)
# #         result = StringIO.StringIO()
# #         pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
# #         if not pdf.err:
# #             print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
# #             return HttpResponse(result.getvalue(), content_type="application/pdf")
# #         else:
# #             print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
# #             return HttpResponse('We are sorry for inconvenience. We will get this back soon.')
# #     except Exception,e:
# #         print '\nException | get_events_registration_receipt = ',str(traceback.print_exc())


# # # @csrf_exempt
# # def get_meter_data(request):
# #     try:
# #         print 'Request In|backofficeapp |event_home.py |get_meter_data|User %s Data'

# #         print '>>>>>>>>',request.GET.get('event_details_id')

# #     except Exception, exc:
# #         print "Exception In |  backofficeapp |event_home.py |update_event", exc
# #         data = {'success': 'false', 'error': 'Exception ' + str(exc)}
# #     return True
# #     #return HttpResponse(json.dumps(data), content_type='application/json')



# @transaction.atomic
# def save_payment_by_cash(request):
#     sid = transaction.savepoint()
#     try:
#         print 'Request IN | event_home | save_payment_by_cash | user'

#         event_reg_obj = EventRegistration.objects.get(id=request.GET.get('hidden_reg_id'))
#         event_reg_obj.cash_receipt_no = request.GET.get('cash_receipt_no')
#         event_reg_obj.payment_method = 0
#         event_reg_obj.payment_status = 4
#         event_reg_obj.tds_amount = request.GET.get('amt_tds')
#         event_reg_obj.save()

#         transaction.savepoint_commit(sid)


#         data = {'success': 'true'}
#         print 'Request OUT | event_home | save_payment_by_cash | user %s', request.user
#         return HttpResponse(json.dumps(data), content_type='application/json')          
    
#     except Exception, exc:
#         data = {'success': 'false'}
#         print 'Exception | event_home | save_payment_by_cash | user %s. Exception = ', str(traceback.print_exc())
#         transaction.rollback(sid)
#     return HttpResponse(json.dumps(data), content_type='application/json')  

# @transaction.atomic
# def save_payment_by_cheque(request):
#     sid = transaction.savepoint()
#     try:
#         print 'Request IN | event_home | save_payment_by_cheque | user'

#         ch_date = datetime.strptime(request.GET.get('cheque_date'), '%d %B %Y').date()

#         event_reg_obj = EventRegistration.objects.get(id=request.GET.get('hidden_reg_id'))
#         event_reg_obj.cheque_no = request.GET.get('cheque_no')
#         event_reg_obj.bank_name = request.GET.get('bank_name')
#         event_reg_obj.cheque_date = ch_date
#         event_reg_obj.payment_method = 1
#         event_reg_obj.payment_status = 4
#         event_reg_obj.tds_amount = request.GET.get('amt_tds')
#         event_reg_obj.save()

#         transaction.savepoint_commit(sid)


#         data = {'success': 'true'}
#         print 'Request OUT | event_home | save_payment_by_cheque | user %s', request.user
#         return HttpResponse(json.dumps(data), content_type='application/json')          
    
#     except Exception, exc:
#         data = {'success': 'false'}
#         print 'Exception | event_home | save_payment_by_cheque | user %s. Exception = ', str(traceback.print_exc())
#         transaction.rollback(sid)
#     return HttpResponse(json.dumps(data), content_type='application/json')      

# @transaction.atomic
# def save_payment_by_neft(request):
#     sid = transaction.savepoint()
#     try:
#         print 'Request IN | event_home | save_payment_by_neft | user'

#         event_reg_obj = EventRegistration.objects.get(id=request.GET.get('hidden_reg_id'))
#         event_reg_obj.trasanction_id = request.GET.get('transaction_id')
#         event_reg_obj.payment_method = 2
#         event_reg_obj.payment_status = 4
#         event_reg_obj.tds_amount = request.GET.get('amt_tds')
#         event_reg_obj.payment_remark = request.GET.get('remark_payment')
#         event_reg_obj.save()

#         transaction.savepoint_commit(sid)


#         data = {'success': 'true'}
#         print 'Request OUT | event_home | save_payment_by_neft | user %s', request.user
#         return HttpResponse(json.dumps(data), content_type='application/json')          
    
#     except Exception, exc:
#         data = {'success': 'false'}
#         print 'Exception | event_home | save_payment_by_neft | user %s. Exception = ', str(traceback.print_exc())
#         transaction.rollback(sid)
#     return HttpResponse(json.dumps(data), content_type='application/json')      
