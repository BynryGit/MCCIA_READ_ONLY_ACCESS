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
from hallbookingapp.models import HallSpecialAnnouncement,HallLocation

from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Special Announcement'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def special_announcement_landing(request):
    location_list = HallLocation.objects.filter(is_deleted=False)
    data = {'location_list': location_list}
    return render(request, 'backoffice/hall_booking/special_announcement_landing.html',data)

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Special Announcement'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_announcement(request):
    data={}
    location_list=HallLocation.objects.filter(is_deleted=False)
    data={'location_list':location_list}
    return render(request, 'backoffice/hall_booking/add_new_special_announcement.html',data)


@csrf_exempt
def save_hall_announcement(request):
    data={}
    print request.POST
    sid = transaction.savepoint()
    try:
        location_id = request.POST.get('select_location')
        announcement = request.POST.get('special_announcement')
        if request.method == 'POST':
            if HallSpecialAnnouncement.objects.filter(hall_location_id=location_id, announcement=announcement):
                data = {'success': 'exist'}
            else:
                hallspecialannouncementobj = HallSpecialAnnouncement(
                    hall_location_id=location_id,
                    announcement=announcement
                )
                hallspecialannouncementobj.save()
                transaction.savepoint_commit(sid)
                data = {'success': 'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print e
        transaction.rollback(sid)
        data = {'success': 'false'}

    return HttpResponse(json.dumps(data), content_type='application/json')


def hall_get_announvcement(request):
    try:
        dataList = []
        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        print '...............',searchTxt
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = 0
        list = ['id']
        column_name = order + list[int(column)]
        try:
            try:
                if request.GET.get('sort_var') == "Active":
                    eventObjs = HallSpecialAnnouncement.objects.filter(is_deleted=False,status=True)
                elif request.GET.get('sort_var') == "Inactive":
                    eventObjs = HallSpecialAnnouncement.objects.filter(is_deleted=False,status=False)
                else:
                    eventObjs = HallSpecialAnnouncement.objects.filter(is_deleted=False)
            except Exception, e:
                print e

            if searchTxt:
                eventObjs=eventObjs.filter(Q(announcement__icontains=searchTxt))

            total_record=eventObjs.count()
            eventObjs = eventObjs.order_by(column_name)[start:length]
            i=0
            a=1
            for eventObj in eventObjs:
                i = start + a
                a = a + 1
                tempList = []
                if eventObj.status == True:
                    event_status = 'True'
                    status = '<label class="label label-success"> Active </label>'
                    action= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_announcement_status(' + '"' + str(event_status) + '"' + ',' + str(eventObj.id) + ')></a>&nbsp; &nbsp;'
                else:
                    event_status = 'False'
                    status = '<label class="label label-default"> Inactive </label>'
                    action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_announcement_status(' + '"' + str(
                        event_status) + '"' + ',' + str(eventObj.id) + ')></a>&nbsp; &nbsp;'

                edit_icon = '<a class="icon-pencil" onClick="edit_announcement_open(' + str(eventObj.id) + ')"></a> &nbsp; &nbsp;'

                tempList.append(str(i))
                tempList.append(eventObj.hall_location.location)
                tempList.append(eventObj.announcement)
                tempList.append(status)

                tempList.append(edit_icon + action)
                dataList.append(tempList)

        except Exception, e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|slab_details | get_slab_details_datatable | User:{0} - Excepton:{1}'.format(
                request.user, e)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|slab_details | get_slab_details_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_hall_announcement_details(request):
    data={}
    announcement_id=request.GET.get('announcement_id')
    announcementobj=HallSpecialAnnouncement.objects.get(id=announcement_id)
    data={'abc':announcementobj.announcement,'location_id':announcementobj.hall_location_id,'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_edit_hall_announcement_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user
        if request.POST:
            print request.POST
            announcement_id = request.POST.get('announcement_id')
            location_id = request.POST.get('select_location')
            announcement = request.POST.get('special_announcement')
            announcementobj = HallSpecialAnnouncement.objects.get(id=announcement_id)
            announcementobj.hall_location_id = location_id
            announcementobj.announcement = announcement
            announcementobj.save()

            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@transaction.atomic
def update_hall_announcement_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('announcement_id')
        eventobj = HallSpecialAnnouncement.objects.get(id=str(request.GET.get('announcement_id')))
        if eventobj.status is True:
            eventobj.status = False
        else:
            eventobj.status = True
        eventobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')
