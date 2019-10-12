from django.contrib.auth.decorators import login_required
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

from authenticationapp.decorator import role_required
from membershipapp.models import *
import urllib
import smtplib
from smtplib import SMTPException
from captcha_form import CaptchaForm
from django.shortcuts import *
import os

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
from django.contrib.sites.shortcuts import get_current_site
from adminapp.models import Committee
from eventsapp.models import EventDetails, EventType, EventRegistration,EventParticipantUser
from backofficeapp.models import SystemUserProfile

@csrf_exempt
def event_participant_report(request):
    committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')
    event_obj_list = EventDetails.objects.filter(is_deleted=False).order_by('event_title')
    event_list = [{'id':obj.id,'event_title':obj.event_title,'from_date':obj.from_date.strftime('%B %d, %Y')} for obj in event_obj_list]
    data={'committee_list':committee_list,'event_list':event_list}
    return render(request, 'backoffice/events/event_participant_report.html',data)

import datetime
@csrf_exempt
def get_events_report_datatable(request):
    try:
        print 'backofficeapp | event_home.py | get_events_datatable | user\n\n\n'
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
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        event_detail_objs_list = EventDetails.objects.filter(is_deleted=False)  # .order_by(column_name)
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
            eventregs=EventRegistration.objects.filter(register_status=0,event__id__in=[event.id for event in event_detail_objs_list],payment_status=request.GET.get('select_payment'),is_deleted=False)
        else:
            eventregs = EventRegistration.objects.filter(register_status=0,event__id__in=[event.id for event in event_detail_objs_list],is_deleted=False)


        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59, second=59)
            eventregs = eventregs.filter(created_on__range=[start_date, end_date])

        if searchTxt:
            eventregs = eventregs.filter((Q(reg_no__icontains=searchTxt)|Q(contact_person_name__icontains=searchTxt)))

        total_record= eventregs.count()

        eventregs = eventregs.order_by(column_name)[start:length]
        i = 0
        a = 1
        for eventreg in eventregs:
            tempList = []
            i = start + a
            a = a + 1
            tempList.append(str(i))
            tempList.append(eventreg.reg_no)
            tempList.append(eventreg.created_on.strftime('%B %d,%Y'))
            tempList.append('-')
            tempList.append(eventreg.name_of_organisation)
            tempList.append(eventreg.address)
            tempList.append(str(eventreg.no_of_participant))
            tempList.append(str(eventreg.contact_person_name))
            tempList.append(str(eventreg.contact_person_email_id))
            tempList.append(str(eventreg.contact_person_number))
            tempList.append(eventreg.get_payment_status_display())
            tempList.append(eventreg.payment_mode)
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_events_datatable | user %s. Exception = ', str(traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': [ ]}
    return HttpResponse(json.dumps(data), content_type='application/json')


import csv
@csrf_exempt
def event_participant_attandance(request):
    event_id = request.POST.get('select_event')
    eventdetail_obj = EventDetails.objects.get(id=event_id)
    eventregs = EventParticipantUser.objects.filter(event_user__is_deleted=False, event_user__is_active=True,
                                                    event_user__register_status=0, event_user__event_id=event_id)
    response = HttpResponse(content_type='text/csv')
    print request.POST
    response['Content-Disposition'] = 'attachment; filename="Event_attandance_sheet_of_'+str(eventdetail_obj.event_title).strip()+'.csv"'
    writer = csv.writer(response)

    # writer.writerow(['', '', '','','','','ATTENDANCE SHEET FOR PAID PROGRAMS','','',''])
    # writer.writerow(['Title of the Event', 'Committe', 'Faculty','Date','','',''])
    # writer.writerow([str(eventdetail_obj.event_title), str(eventdetail_obj.organising_committee.committee), '','','','',''])
    writer.writerow(['Sr.No.','event Name', 'Name of the Participants', 'Designation', 'Name of the Organization','Memb.No.','Tel. / Mobile','Email','Payment Status','Amount','Event Type(Paid / Free)','From Date','TO Date','Sign','Address','GST No.','Committee','Contact Person 1','Contact Person 2','EBK Number'])


    i=0
    for eventreg in eventregs:
        i=i+1        

        member_associate_no = 'Non-Member'
        if eventreg.event_user.is_member:
            member_associate_no = str(eventreg.event_user.user_details.member_associate_no)
        if eventreg.event_user.gst_in== 'UP':
            gst_no = 'Under Process'
        elif eventreg.event_user.gst_in== 'NA':
            gst_no = 'Not Applicable'
        else:
            gst_no = str(eventreg.event_user.gst)
        if eventreg.event_user.event.contact_person2:
            contact_person2 = str(eventreg.event_user.event.contact_person2.name)
        else:
            contact_person2 = ''
        if eventreg.event_user_name:
            event_user_name = str(eventreg.event_user_name)
        else:
            event_user_name = 'NA'
        if eventreg.event_user.event.event_mode == 1:
            event_mode = 'Paid'
        else:
            event_mode = 'Free'

        amount = eventreg.event_user.total_amount/eventreg.event_user.no_of_participant

        writer.writerow([i,str(eventreg.event_user.event.event_title),str((event_user_name).upper()),str(eventreg.designation),  str(eventreg.event_user.name_of_organisation),str(member_associate_no),
                         str(eventreg.contact_no),str(eventreg.email_id),str(eventreg.event_user.get_payment_status_display()),amount,event_mode,str(eventreg.event_user.event.from_date.strftime('%d/%m/%Y')),
                         str(eventreg.event_user.event.to_date.strftime('%d/%m/%Y')),'',str(eventreg.event_user.address),gst_no,str(eventreg.event_user.event.organising_committee.committee),str(eventreg.event_user.event.contact_person1.name),contact_person2,str(eventreg.event_user.reg_no)])

    # writer.writerow([str(k[0]), str(k[1]), str(dates[i])])
    return response


charset = 'utf-8'
from django.template import Context
from django.template.loader import render_to_string, get_template
def upcoming_event_download(request):
    try:
        print 'backofficeapp | event_report.py | upcoming_event_download | user\n\n\n'
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        event_detail_objs_list = EventDetails.objects.filter(event_status=0,from_date__gte=today,is_deleted=False).order_by('from_date')#.order_by(column_name)[start:length]

        tempList = []   
        for obj in event_detail_objs_list:              
            when_to_attend = obj.from_date.strftime('%B %d, %Y') + ' - ' + obj.to_date.strftime('%B %d, %Y')
            if obj.from_date.strftime('%B %d, %Y') == obj.to_date.strftime('%B %d, %Y'):
                when_to_attend = obj.from_date.strftime('%B %d, %Y')

            time_to_attend = obj.from_date.strftime('%I:%M:%p') + ' - ' + obj.to_date.strftime('%I:%M:%p')

            action = 'https://' + get_current_site(request).domain + "/eventsapp/events-details/?event_detail_id="+str(obj.id)

            data1 ={
                'when_to_attend':when_to_attend,
                'time_to_attend':time_to_attend,
                'event_title':str(obj.event_title),
                'event_mode':str(obj.get_event_mode_display()),
                'to_whom_description':str(obj.event_objective) if obj.event_objective else str(obj.to_whom_description),            
                'action':action
            }
            tempList.append(data1)

        data = {'FinalList':tempList,'today_date':datetime.datetime.now().strftime('%B %d, %Y'),}

        html=get_template('backoffice/events/upcoming_event_calender.html').render(Context(data))
        response = HttpResponse(html, content_type='application/liquid')
        return response
    except Exception,e:
        print 'backofficeapp | event_report.py | upcoming_event_download | Exception\n\n\n',e
        return HttpResponse(500)        


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Report'], login_url='/backofficeapp/login/', raise_exception=True)
def download_event_participant_data(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=event_participant_report.csv'
        writer = csv.writer(response)
        from_date = datetime.datetime.strptime('01/04/'+str(datetime.datetime.now().year), '%d/%m/%Y')
        to_date = datetime.datetime.now()
        date_list = []
        event_id_list = []        

        while from_date <= to_date:
            date_list.append(from_date.date())
            from_date = from_date + timedelta(days=1)

        event_list = EventDetails.objects.filter(is_deleted=False, current_event_stat=0)
        for event_item in event_list:
            if event_item.from_date.date() in date_list:
                event_id_list.append(event_item.id)

        eventregs = EventParticipantUser.objects.filter(event_user__is_deleted=False, event_user__is_active=True, event_user__register_status=0, event_user__event_id__in=event_id_list)

        
        # event_id_list = [129, 130, 134, 139, 140, 228, 229, 238, 239, 240, 241, 242, 244, 245, 247, 252, 253, 255, 259, 261, 264, 266, 267, 268, 269, 270, 271, 272, 275, 276, 277, 336, 381, 384, 388, 389, 390, 391, 392, 393, 396, 397, 398, 402, 403, 404, 387, 399, 405, 406, 410, 411, 409]
        # eventregs = EventParticipantUser.objects.filter(event_user__is_deleted=False, event_user__is_active=True, event_user__register_status=0, event_user__event_id__in=event_id_list)

        writer.writerow(['Sr.No.','event Name', 'Name of the Participants', 'Designation', 'Name of the Organization','Memb.No.','Tel. / Mobile','Email','Event Type(Paid / Free)','From Date','TO Date','Address','GST No.','Committee','Contact Person 1','Contact Person 2','EBK Number', 'Invitee/Attendee'])

        i = 0
        for eventreg in eventregs:
            i = i + 1

            member_associate_no = 'Non-Member'
            if eventreg.event_user.is_member:
                member_associate_no = str(eventreg.event_user.user_details.member_associate_no)
            if eventreg.event_user.gst_in == 'UP':
                gst_no = 'Under Process'
            elif eventreg.event_user.gst_in == 'NA':
                gst_no = 'Not Applicable'
            else:
                gst_no = str(eventreg.event_user.gst)
            if eventreg.event_user.event.contact_person2:
                contact_person2 = str(eventreg.event_user.event.contact_person2.name)
            else:
                contact_person2 = ''
            if eventreg.event_user_name:
                event_user_name = str(eventreg.event_user_name.encode('utf-8').strip())
            else:
                event_user_name = 'NA'
            if eventreg.event_user.event.event_mode == 1:
                event_mode = 'Paid'
            else:
                event_mode = 'Free'

            writer.writerow([i,
                             str(eventreg.event_user.event.event_title.encode("utf8", "ignore").strip()) if eventreg.event_user.event.event_title else '',
                             str((event_user_name).upper()),
                             str(eventreg.designation.encode("utf8", "ignore").strip()) if eventreg.designation else '',
                             str(eventreg.event_user.name_of_organisation.encode("utf8", "ignore").strip()) if eventreg.event_user.name_of_organisation else '',
                             str(member_associate_no.encode("utf8", "ignore").strip()),
                             str(eventreg.contact_no.encode("utf8", "ignore").strip()) if eventreg.contact_no else '',
                             str(eventreg.email_id.encode("utf8", "ignore").strip()) if eventreg.email_id else '',
                             event_mode,
                             str(eventreg.event_user.event.from_date.strftime('%d/%m/%Y')),
                             str(eventreg.event_user.event.to_date.strftime('%d/%m/%Y')),'',gst_no,
                             str(eventreg.event_user.event.organising_committee.committee.encode("utf8", "ignore").strip()),
                             str(eventreg.event_user.event.contact_person1.name.encode("utf8", "ignore").strip()),
                             contact_person2,str(eventreg.event_user.reg_no),
                             str('Attendee' if eventreg.is_attendees else 'Invitee' if eventreg.is_invitee else 'Registration')])

        return response
    except Exception, e:
        print e
        print str(traceback.print_exc())
