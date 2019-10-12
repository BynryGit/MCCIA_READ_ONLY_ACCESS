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
from adminapp.models import *
import traceback



from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Legal Details'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def legal_details(request):

    return render(request, 'backoffice/membership/legal_details.html')


# TODO Membership Detail Datatable Start ------cycle level
def get_legal_details_datatable(request):
    try:
        print '\nRequest IN | legal_details | get_legal_details_datatable | user %s', request.user
        dataList = []
        meterReadings = []


        # Oredering and paging starts

        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        legal_detail_status = request.GET.get('legal_detail_status')
        legal_detail_list = ''

        if legal_detail_status != 'show_all':
            legal_detail_list = LegalStatus.objects.filter(status=True if legal_detail_status == 'True' else False,
                                                           is_deleted=False)
        else:
            legal_detail_list = LegalStatus.objects.filter(is_deleted=False)

        legal_detail_list = legal_detail_list.filter(Q(code__icontains=searchTxt)|
                                                     Q(description__icontains=searchTxt))
        i = 1
        for legalStatus in legal_detail_list:
            tempList = []
            action_two = ''
            legal_status = ''
            status = ''

            if legalStatus.status is True:
                status = '<label class="label label-success">Active</label>'
                legal_status = 'True'
                action_two = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_legal_modal" onclick=update_legal_status(' + '"' + str(
                    legal_status) + '"' + ',' + str(legalStatus.id) + ')></a>&nbsp;&nbsp;'
            else:
                status = '<label class="label label-default">Inactive</label>'
                legal_status = 'False'
                action_two = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_legal_modal" onclick=update_legal_status(' + '"' + str(
                    legal_status) + '"' + ',' + str(legalStatus.id) + ')></a>&nbsp;&nbsp;'

            edit_icon = '<a class="icon-pencil" title="Legal Detail" data-toggle="modal" data-target="#edit_legal_details_modal" onClick="show_edit_legal_modal(' + str(legalStatus.id) + ')"></a>'

            action = action_two + edit_icon
            tempList.append(i)
            tempList.append(legalStatus.code)
            tempList.append(legalStatus.description)
            tempList.append(status)
            tempList.append(action)
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
        print 'Exception|legal_details | get_legal_details_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
# TODO Membership Detail Datatable Initialization End ------cycle level

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Legal Details'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_legal_details(request):

    return render(request, 'backoffice/membership/add_legal_details.html')


@csrf_exempt
@transaction.atomic
def save_legal_details(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nsave_legal_details view'
        legal_detail_obj = LegalStatus(code=str(request.POST.get('legal_code')),
                                       description=str(request.POST.get('legal_desc')))
        legal_detail_obj.save()
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | save_legal_details'
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | save_legal_details = ', e
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_edit_legal_detail(request):
    data = {}
    try:
        legal_detail_obj = LegalStatus.objects.get(id=str(request.GET.get('legal_id')))
        data = {'success': 'true', 'legal_id': legal_detail_obj.id,
                'legal_desc': legal_detail_obj.description, 'legal_code': legal_detail_obj.code}
    except Exception, e:
        print '\nException | show_edit_legal_detail = ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@transaction.atomic
def update_legal_detail(request):
    data = {}
    sid = transaction.savepoint()
    try:
        legal_detail_obj = LegalStatus.objects.get(id=str(request.POST.get('legal_id')))
        legal_detail_obj.code = str(request.POST.get('edit_legal_code'))
        legal_detail_obj.description = str(request.POST.get('edit_legal_desc'))
        legal_detail_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_legal_detail = ', e
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def update_legal_detail_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | legal_details.py | update_legal_detail_status | User = ',request.user
        legal_detail_obj = LegalStatus.objects.get(id=str(request.GET.get('legal_detail_id')))
        if legal_detail_obj.status is True:
            legal_detail_obj.status = False
        else:
            legal_detail_obj.status = True

        legal_detail_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print '\nResponse OUT | legal_details.py | update_legal_detail_status | User = ', request.user
    except Exception, e:
        print '\nException | legal_details.py | update_legal_detail_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')