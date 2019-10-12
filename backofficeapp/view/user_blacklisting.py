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
from datetime import timedelta, datetime
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import dateutil.relativedelta
from django.db.models import Count
import calendar
import urllib2
import random
import traceback

from hallbookingapp.models import UserTrackDetail, UserTrackDepositDetail
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required
import datetime


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Special Announcement'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def user_blacklisting_landing(request):
    return render(request, 'backoffice/hall_booking/blacklisting_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Special Announcement'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def security_deposite_landing(request):
    return render(request, 'backoffice/hall_booking/security_deposite_landing.html')

def load_blacklisting_table(request):
    try:
        dataList = []
        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
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
            if request.GET.get('sort_var') == "1":
                user_track_objs = UserTrackDetail.objects.filter(is_deleted=False,is_blacklisted=False)
            elif request.GET.get('sort_var') == "0":
                user_track_objs = UserTrackDetail.objects.filter(is_deleted=False,is_blacklisted=True)
            else:
                user_track_objs = UserTrackDetail.objects.filter(is_deleted=False)

            if searchTxt:
                user_track_objs=user_track_objs.filter(Q(company__icontains=searchTxt))

            total_record=user_track_objs.count()
            user_track_objsList = user_track_objs.order_by(column_name)[start:length]
            i=0
            a=1
            for userObj in user_track_objsList:
                i = start + a
                a = a + 1
                tempList = []
                if userObj.is_blacklisted == False:
                    blacklisting_status = 'True'
                    status = '<label class="label label-success"> Active </label>'
                    action= '<a class="icon-trash" title="Blacklist" data-toggle="modal" data-target="#active_deactive_user" onclick=update_user_status(' + '"' + str(blacklisting_status) + '"' + ',' + str(userObj.id) + ')></a>&nbsp; &nbsp;'
                else:
                    blacklisting_status = 'False'
                    status = '<label class="label label-default"> Blacklisted </label>'
                    action = '<a class="icon-reload" title="Activate" data-toggle="modal" data-target="#active_deactive_user" onclick=update_user_status(' + '"' + str(
                        blacklisting_status) + '"' + ',' + str(userObj.id) + ')></a>&nbsp; &nbsp;'

                edit_icon = '<a title="Return Deposit" class="fa fa-paper-plane" onClick="return_deposit_open(' + str(userObj.id) + ',' + str(userObj.deposit_available) + ',' + str(userObj.refund_status) + ')"></a> &nbsp; &nbsp;'

                tempList.append(str(i))
                tempList.append(userObj.company)
                tempList.append(userObj.contact_person)
                tempList.append(str(userObj.deposit_available))
                tempList.append(userObj.updated_date.strftime('%d %B %Y - %H:%M'))
                tempList.append(status)
                tempList.append(edit_icon + action)
                dataList.append(tempList)

        except Exception, e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|Backofficeapp | load_blacklisting_table | User:{0} - Excepton:{1}'.format(
                request.user, e)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|Backofficeapp | load_blacklisting_table|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')    


def security_deposit_details_datatable(request):
    try:
        print '\nRequest IN | backofficeapp | view | user_blacklisting.py | security_deposit_details_datatable | ', 
        dataList = []
        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
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
            if request.GET.get('sort_var') == "1":
                user_track_objs = UserTrackDetail.objects.filter(is_deleted=False)
            elif request.GET.get('sort_var') == "0":
                user_track_objs = UserTrackDetail.objects.filter(is_deleted=False)
            else:
                user_track_objs = UserTrackDetail.objects.filter(is_deleted=False)
            if searchTxt:
                user_track_objs=user_track_objs.filter(Q(company__icontains=searchTxt))

            total_record=user_track_objs.count()
            user_track_objsList = user_track_objs.order_by(column_name)[start:length]
            i=1
            a=1
            for userObj in user_track_objsList:
                tempList = []
                tempList.append(str(i))
                tempList.append(userObj.company)
                tempList.append(userObj.contact_person)
                tempList.append(str(userObj.deposit_available))
                tempList.append(userObj.updated_date.strftime('%d %B %Y - %H:%M'))
                tempList.append('')
                tempList.append('')
                dataList.append(tempList)
                i = i + 1
        except Exception, e:
            print 'exception ', str(traceback.print_exc())
            print '\Exception Out | backofficeapp | view | user_blacklisting.py | security_deposit_details_datatable |'.format(
                request.user, e)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print '\Exception Out | backofficeapp | view | user_blacklisting.py | security_deposit_details_datatable | ', str(traceback.print_exc())
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')    



@transaction.atomic
def update_user_track_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('user_id')
        userTrackobj = UserTrackDetail.objects.get(id=str(request.GET.get('user_id')))
        if userTrackobj.is_blacklisted is True:
            userTrackobj.is_blacklisted = False
            reactivated_date = datetime.datetime.strptime(request.GET.get('reactivated_date'), '%d/%m/%Y')
            userTrackobj.reactivated_date = reactivated_date
            userTrackobj.reactivated_remark = request.GET.get('reactivated_remark')
        else:
            userTrackobj.is_blacklisted = True
            userTrackobj.blacklisted_by = str(request.user)
            date = datetime.datetime.strptime(request.GET.get('blacklist_date'), '%d/%m/%Y')
            userTrackobj.blacklisted_date = date
            userTrackobj.blacklist_remark = request.GET.get('blacklist_remark')
        userTrackobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_user_track_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
@transaction.atomic
def return_user_deposit(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | user_blacklisting | return_user_deposit | user %s', request.POST

        if request.POST:
            user_track_id = request.POST.get('user_track_id')
            userTrackobj = UserTrackDetail.objects.get(id=user_track_id)
            userTrackobj.deposit_status = 1
            userTrackobj.deposit_available = 0
            userTrackobj.deposit_remark = request.POST.get('deposit_remark')
            userTrackobj.refund_status = 1
            userTrackobj.save()

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
    print data
    return HttpResponse(json.dumps(data), content_type='application/json')    


@csrf_exempt
def deposit_cheque_details_return(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | user_blacklisting | deposit_cheque_details_return | user %s', request.user
        if request.POST:

            userTrack_obj = UserTrackDetail.objects.get(id=request.POST.get('user_track_id'))
            userTrackDetail_obj = UserTrackDepositDetail(
                user_track=userTrack_obj,
                cheque_no=request.POST.get('depositCheque_No'),
                cheque_date=datetime.strptime(str(request.POST.get('depositCheque_Date')), "%d/%m/%Y"),
                bank_name=request.POST.get('depositBank_Name'),
                amount=request.POST.get('depositCheque_amount'),
                deposit_remark = userTrack_obj.deposit_remark,
                created_by=request.user
            )
            userTrackDetail_obj.save()

            userTrack_obj.deposit_status = 1
            userTrack_obj.refund_status = 2
            userTrack_obj.save()


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



@csrf_exempt
def get_deposit_status(request):
    data = {}
    try:
        print '\nRequest IN | user_blacklisting.py | get_deposit_status | User = ', request.user

        userTrack_obj = UserTrackDetail.objects.get(id=request.GET.get('user_id'))

        try:
            deposit_track_obj = UserTrackDepositDetail.objects.filter(user_track=userTrack_obj).last()
            cheque_no = deposit_track_obj.cheque_no
            cheque_date = deposit_track_obj.cheque_date.strftime('%d/%m/%Y')
            bank_name = deposit_track_obj.bank_name
            amount = deposit_track_obj.amount         
        except Exception as e:
            cheque_no = ''
            cheque_date = ''
            bank_name = ''
            amount = 0      
            print e

        print '>>>>>>>>>>>>>>>>>>>>>>>>>>',amount
        data = {'success': 'true', 
                'deposit_available' : str(userTrack_obj.deposit_available),
                'refund_status' : userTrack_obj.refund_status,
                'deposit_remark' : userTrack_obj.deposit_remark if userTrack_obj.deposit_remark else '',

                'cheque_no' :  cheque_no,
                'cheque_date':cheque_date,
                'bank_name':bank_name,
                'amount':str(amount),
            }

        print '\nResponse OUT | user_blacklisting.py | get_deposit_status | User = ', request.user
    except Exception,e:
        print '\nException IN | user_blacklisting.py | get_deposit_status | User = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')      