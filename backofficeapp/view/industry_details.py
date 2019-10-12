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

from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Industry Details'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def industry_details(request):
    return render(request, 'backoffice/membership/industry_details.html')


@csrf_exempt
def save_industry_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | industry_details | save_industry_details | user %s', request.user

        industry_code = request.POST.get('industry_code')
        industry_description = request.POST.get('industry_descriptions')

        if request.method == 'POST':         

            industryDetailsObj=IndustryDescription(
                code=str(request.POST.get('industry_code')).strip(),
                description=str(request.POST.get('industry_descriptions')).strip(),
                is_active=True,
                is_deleted=False,
            )
            industryDetailsObj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | industry_details | save_industry_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


# TODO Membership Detail Datatable Start ------cycle level
def get_industry_details_datatable(request):
    try:
        print 'Request IN | membership_details | get_industry_details_datatable | user %s', request.user
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

        industry_detail_status = request.GET.get('select_industry_detail_status')

        industry_detail_list = ''

        if industry_detail_status != 'show_all':
            industry_detail_list = IndustryDescription.objects.filter(is_active=True if industry_detail_status == 'True' else False,
                                                                      is_deleted=False)
        else:
            industry_detail_list = IndustryDescription.objects.filter(is_deleted=False)

        industry_detail_list = industry_detail_list.filter(Q(code__icontains=searchTxt) |
                                                           Q(description__icontains=searchTxt))

        i = 1
        for industryDescription in industry_detail_list:
            # move all data for rendering
            tempList = []
            if industryDescription.is_active == True:
                status = '<label class="label label-success"> Active </label>'
                delete_icon = '<a class="icon-trash" onClick="deleteIndustryDetailModal(' + str(industryDescription.id) + ')"></a>&nbsp;&nbsp;'
            else:
                status = '<label class="label label-default"> Inactive </label>'
                delete_icon = '<a class="icon-reload" onClick="activateIndustryDetailModal(' + str(industryDescription.id) + ')"></a>&nbsp;&nbsp;'
            edit_icon = '<a class="icon-pencil" onClick="editIndustryDescriptionModal(' + str(industryDescription.id) + ')"></a>'

            action = delete_icon + edit_icon
            tempList.append(i)
            tempList.append(industryDescription.code)
            tempList.append(industryDescription.description)
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
        print 'Exception|membership_details | get_industry_details_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
# TODO Membership Detail Datatable Initialization End ------cycle level

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Industry Details'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_industry_details(request):
    return render(request, 'backoffice/membership/add_industry_details.html')
    
    
def show_industry_details(request):
    try:

        print 'Request IN | industry_details | show_industry_details | user %s', request.user, request.GET.get('industry_code_id')

        industry_code_id = request.GET.get('industry_code_id')

        industryObj = IndustryDescription.objects.get(id=industry_code_id)
        industryDetails = {
            'industry_code_id':industryObj.id,
            'industry_code': industryObj.code,
            'industry_category': industryObj.description,
        }

        print 'Request OUT | user | show_industry_details | user %s', request.user

        data = {'success': 'true', 'industryDetails': industryDetails}
        print 'Request OUT | industry_details | show_industry_details | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        data = {'success': 'false'}
        print 'Exception | user | industry_details | show_industry_details |user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')  
    

@csrf_exempt
def edit_industry_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | industry_details | edit_industry_details | user %s', request.user

        if request.POST:

            industry_code_id = request.POST.get('industry_code_id')
            edit_industry_code = str(request.POST.get('edit_industry_code')).strip()
            edit_industry_descriptions = str(request.POST.get('edit_industry_descriptions')).strip()

            industryObj = IndustryDescription.objects.get(id=industry_code_id)
            industryObj.code = edit_industry_code
            industryObj.description = edit_industry_descriptions
            industryObj.save()

            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | industry_details | edit_industry_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | industry_details | edit_industry_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')      
    
@csrf_exempt
def delete_industry_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | industry_details | delete_industry_details | user %s', request.user
        if request.POST:
            industry_code_id = request.POST.get('industry_id')            
            print industry_code_id
            
            industryObj = IndustryDescription.objects.get(id=industry_code_id)
            industryObj.is_active = False
            industryObj.save()
            
            transaction.savepoint_commit(sid)
            data = {'success': 'true'}
            print 'Request OUT | industry_details | delete_industry_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | industry_details | delete_industry_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')  

@csrf_exempt
def activate_industry_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | industry_details | activate_industry_details | user %s', request.user
        if request.POST:
            industry_code_id = request.POST.get('industry_id')            
            print industry_code_id
            
            industryObj = IndustryDescription.objects.get(id=industry_code_id)
            industryObj.is_active = True
            industryObj.save()
            
            transaction.savepoint_commit(sid)
            data = {'success': 'true'}
            print 'Request OUT | industry_details | activate_industry_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | industry_details | activate_industry_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')     