
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
import datetime
from eventsapp.models import EventDetails, EventType, EventRegistration,EventParticipantUser

@csrf_exempt
def delete_event_participantt(request):
    return render(request, 'backoffice/events/delete_event_participant.html')


@csrf_exempt
def get_delete_events_registrations(request):
    try:
        print 'backofficeapp | event_home.py | get_delete_events_registrations | user'
        dataList = []
        total_record = 0
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
        event_objs_list = EventRegistration.objects.filter(event__event_status=0)  # .order_by(column_name)
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59, second=59)
            event_objs_list = event_objs_list.filter(event__from_date__range=[start_date, end_date])
        if request.GET.get('select_status'):
            if request.GET.get('select_status')=='0':
                event_objs_list = event_objs_list.filter(register_status=0)
            else:
                event_objs_list = event_objs_list.filter(register_status=2)
        total_record=event_objs_list.count()
        event_objs_list=event_objs_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in event_objs_list:
            tempList=[]
            i = start + a
            a = a + 1

            if obj.register_status:
                event_status = 'Inactive'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_mem_cat(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_mem_cat(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            tempList.append(str(i))
            # tempList.append(obj.id)
            tempList.append(obj.name_of_organisation)
            tempList.append(obj.event.organising_committee.committee)
            tempList.append(obj.event.event_title)
            tempList.append(obj.event.event_type.event_type)
            tempList.append(obj.event.from_date.strftime('%B %d, %Y, %H:%M:%p' )+' - '+obj.event.to_date.strftime('%B %d, %Y, %H:%M:%p' ))

            paid_data = 0
            non_members = 0
            members = 0
            total_fees = 0
            total_stax = 0

            if obj.is_member:
                members=obj.no_of_participant
            else:
                non_members = obj.no_of_participant

            tempList.append(paid_data)
            tempList.append(non_members)
            tempList.append(members)
            tempList.append(total_fees)
            tempList.append(total_stax)
            tempList.append(status)
            tempList.append(action)

            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events_registrations | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def action_delete_event_participent(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('reg_id')
        eventreg=EventRegistration.objects.get(id=str(request.GET.get('reg_id')))
        if eventreg.register_status == 2:
            eventreg.register_status = 0
            eventreg.is_deleted = False
            eventreg.save()
            EventParticipantUser.objects.filter(event_user_id=str(request.GET.get('reg_id'))).update(is_deleted=False,register_status = 0)
        else:
            eventreg.register_status = 2
            eventreg.is_deleted = True
            eventreg.save()
            EventParticipantUser.objects.filter(event_user_id=str(request.GET.get('reg_id'))).update(is_deleted=True,register_status=2)
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | action_delete_event = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')