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
from adminapp.models import *
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
@role_required(privileges=['Slab'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def slab(request):
    membership_category_list = MembershipCategory.objects.filter(status=True, is_deleted=False)
    data = {'membership_category_list': membership_category_list }
    return render(request, 'backoffice/membership/slab.html', data)


# TODO Membership Detail Datatable Start ------cycle level
def get_slab_details_datatable(request):
    try:
        print 'Request IN | slab_details | get_slab_details_datatable | user %s', request.user
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

        slab_status = request.GET.get('select_slab_status')
        select_category = request.GET.get('select_category')

        slab_detail_list = ''
        slab_detail_list = MembershipSlab.objects.filter(is_deleted=False)

        if select_category!= 'show_all':
            slab_detail_list = slab_detail_list .filter(membershipCategory__id=select_category, is_deleted=False)

        if slab_status != 'show_all':
            slab_detail_list = MembershipSlab.objects.filter(status=True if slab_status == 'True' else False,
                                                             is_deleted=False)

        slab_detail_list = slab_detail_list.filter(Q(slab__icontains=searchTxt)|
                                                   Q(membershipCategory__membership_category__icontains=searchTxt))

        i = 1
        for membershipSlab in slab_detail_list:
            tempList = []
            if membershipSlab.status is True:
                status = '<label class="label label-success"> Active </label>'
                status_text = "True"
                status_icon = '<a class="icon-trash" data-toggle="modal" data-target=#active_deactive_mem_slab onclick=activeInactiveMemSlab(' + '"' + str(
                    status_text) + '"' + ',' + str(membershipSlab.id) + ')></a>&nbsp;&nbsp;'
            else:
                status = '<label class="label label-default"> Inactive </label>'
                status_text = "False"
                status_icon = '<a class="icon-reload" data-toggle="modal" data-target=#active_deactive_mem_slab onclick=activeInactiveMemSlab(' + '"' + str(
                    status_text) + '"' + ',' + str(membershipSlab.id) + ')></a>&nbsp;&nbsp;'
            edit_icon = '<a class="icon-pencil" onClick="editSlabDetailsModal(' + str(membershipSlab.id) + ')"></a>'

            tempList.append(i)
            tempList.append(membershipSlab.membershipCategory.membership_category)
            tempList.append(membershipSlab.slab)
            tempList.append(membershipSlab.applicableTo)
            tempList.append(membershipSlab.annual_fee)
            tempList.append(membershipSlab.entrance_fee)
            tempList.append(status)
            tempList.append(status_icon + edit_icon)
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
        print 'Exception|slab_details | get_slab_details_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')
# TODO Membership Detail Datatable Initialization End ------cycle level

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Slab'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_slab(request):
    data={}
    membershipCategory=MembershipCategory.objects.filter(status=True, is_deleted=False)
    membershipSlab=MembershipSlab.objects.filter(status=True, is_deleted=False)
    slabCriteria=SlabCriteria.objects.filter(status=True, is_deleted=False)
    data={'membershipCategory':membershipCategory,'membershipSlab':membershipSlab,'slabCriteria':slabCriteria}
    return render(request, 'backoffice/membership/add_new_slab.html',data)


@transaction.atomic
@csrf_exempt
def save_slab_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | slab_details | save_slab_details | user %s', request.user
        if request.method == 'POST':

            membershipSlabObj = MembershipSlab(
                enroll_type = request.POST.get('EnrollType'),
                slab_type = request.POST.get('SlabEnrollType'),
                slab = request.POST.get('slab_name'),
                membershipCategory =MembershipCategory.objects.get(id=request.POST.get('MembershipCategory')),
                applicableTo = request.POST.get('ApplicableTo'),
                annual_fee = request.POST.get('AnnualFees'),
                entrance_fee = request.POST.get('EntranceFees'),
                cr3 = SlabCriteria.objects.get(id=request.POST.get('criteria')),
                status=True,
                is_deleted=False,
            )
            membershipSlabObj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | slab_details | save_slab_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        data = {'success': 'false'}
        print 'Exception | slab_details | save_slab_details | user %s. Exception = ', request.user, e
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_slab_details(request):
    try:
        membershipCategoryList = []
        slabCriteriaList=[]
        print 'Request IN | slab_details | show_slab_details | user %s', request.user, request.GET.get('slab_id')

        slab_id = request.GET.get('slab_id')
        slabObj = MembershipSlab.objects.get(id=slab_id)
        membershipCategoryObj=MembershipCategory.objects.filter(status=True, is_deleted=False)
        for i in membershipCategoryObj:
            membershipCategoryList.append({'id':i.id,'membershipCategory':i.membership_category})

        slabCriteriaObj = SlabCriteria.objects.filter(status=True, is_deleted=False)
        for i in slabCriteriaObj:
            slabCriteriaList.append({'id':i.id,'slab_criteria':str(i.slab_criteria)})

        slabDetails = {
            'slab_id':slabObj.id,          
            'slab': slabObj.slab,
            'membershipCategory': slabObj.membershipCategory.id,
            'membershipCategoryList':membershipCategoryList,
            #'slab_description': slabObj.description,
            'ApplicableTo': str(slabObj.applicableTo),
            'AnnualFees': slabObj.annual_fee,
            'EntranceFees': slabObj.entrance_fee,
            'criteria': str(slabObj.cr3.id),
            'slabCriteriaList': slabCriteriaList,
            'EnrollType': slabObj.enroll_type,
            'SlabEnrollType': slabObj.slab_type,
        }

        data = {'success': 'true', 'slabDetails': slabDetails}
        print 'Request OUT | slab_details | show_slab_details | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        data = {'success': 'false'}
        print 'Exception | user | slab_details | show_slab_details |user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')  
    

@transaction.atomic
@csrf_exempt
def edit_slab_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user

        if request.POST:
            slab_id = request.POST.get('slab_id')
            membership_category_obj = MembershipCategory.objects.get(id=request.POST.get('MembershipCategory'))
            slab_name = request.POST.get('slab_name')
            ApplicableTo = request.POST.get('ApplicableTo')
            criteria = request.POST.get('criteria')
            AnnualFees = request.POST.get('AnnualFees')
            EntranceFees = request.POST.get('EntranceFees')
            slab_type = request.POST.get('SlabEnrollType')
            enroll_type = request.POST.get('EnrollType')

            slabObj = MembershipSlab.objects.get(id=slab_id)
            slabObj.slab = slab_name
            slabObj.slab_type = slab_type
            slabObj.enroll_type = enroll_type
            slabObj.membershipCategory = membership_category_obj
            slabObj.applicableTo = ApplicableTo
            slabObj.cr3 = SlabCriteria.objects.get(id=criteria)
            slabObj.annual_fee = AnnualFees
            slabObj.entrance_fee = EntranceFees
            slabObj.save()

            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            print 'Request OUT | slab_details | edit_slab_details | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        data = {'success': 'false'}
        print 'Exception | slab_details | edit_slab_details | user %s. Exception = ', request.user, e
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_slab_filter_data(request):
    try:
        membershipSlabObjs = MembershipSlab.objects.filter(is_deleted=False)

        for membershipSlabObj in membershipSlabObjs:

            if request.GET.get('sort_var') == 1:
                membershipSlabObj.is_active=True
        data = {'success': 'true'}
        print 'Request OUT | slab_details | get_filter_data | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | slab_details | get_filter_data | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


# Active / Inactive Slab Status
@transaction.atomic
def update_membership_slab_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | slab_details | update_membership_slab_status | user %s', request.user
        membership_slab_obj = MembershipSlab.objects.get(id=request.GET.get('mem_slab_id'))
        if membership_slab_obj.status is True:
            membership_slab_obj.status = False
        else:
            membership_slab_obj.status = True
        membership_slab_obj.save()
        transaction.savepoint_commit(sid)

        data = {'success': 'true'}
        print '\nResponse OUT | slab_details | update_membership_slab_status | user %s', request.user
    except Exception, e:
        data = {'success': 'false'}
        print '\nException IN | slab_details | update_membership_slab_status = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')