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
from eventsapp.models import EventDetails, EventType, EventRegistration,EventParticipantUser
from backofficeapp.models import SystemUserProfile
import datetime
@csrf_exempt
def delete_event(request):
    return render(request, 'backoffice/events/delete_event.html')


@csrf_exempt
def get_delete_events(request):
    try:
        print 'backofficeapp | delete_event.py | get_delete_events | user'
        dataList = []
        total_record = 0

        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'organising_committee__committee', 'event_title']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))


        event_objs_list = EventDetails.objects.filter(is_deleted=False)  # .order_by(column_name)

        if request.GET.get('select_status'):
                event_objs_list = event_objs_list.filter(event_status=int(request.GET.get('select_status')))

        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59, second=59)
            event_objs_list = event_objs_list.filter(from_date__range=[start_date, end_date])


        if searchTxt:
            event_objs_list = event_objs_list.filter(Q(event_title__icontains=searchTxt))

        total_record = event_objs_list.count()
        event_objs_list= event_objs_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in event_objs_list:
            i = start + a
            a = a + 1
            if obj.event_status == 0:
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_mem_cat(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status= 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_mem_cat(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            tempList=[]
            tempList.append(str(i))
            # tempList.append(obj.id)
            tempList.append(obj.organising_committee.committee)
            tempList.append(obj.event_title)
            tempList.append(obj.event_type.event_type)
            tempList.append(obj.from_date.strftime('%B %d, %Y, %H:%M:%p' )+' - '+obj.to_date.strftime('%B %d, %Y, %H:%M:%p' ))
            tempList.append(obj.hall_details.hall_location.location)
            tempList.append(status)
            tempList.append(action)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def action_delete_event(request):
    data = {}
    sid = transaction.savepoint()
    try:
        eventobj = EventDetails.objects.get(id=int(request.GET.get('event_id')))
        if eventobj.event_status == 0:
            eventobj.event_status = 1
            EventRegistration.objects.filter(event=eventobj,is_deleted=False).update(is_active=False,register_status=1)
            EventParticipantUser.objects.filter(event_user__event=eventobj,is_deleted=False).update(is_active=False,register_status=1)
        else:
            eventobj.event_status = 0
            EventRegistration.objects.filter(event=eventobj,is_deleted=False).update(is_active=True,register_status=0)
            EventParticipantUser.objects.filter(event_user__event=eventobj,is_deleted=False).update(is_active=True,register_status=0)

        eventobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print e
        print '\nException | action_delete_event = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')