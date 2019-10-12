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
# from datetime import date
import datetime
import calendar
import urllib2
import random
import traceback

from adminapp.models import Committee
from eventsapp.models import EventDetails, EventType, EventRegistration, EventBannerImage
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import Holiday,HallLocation,HallDetail
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Holidays'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def holidays_landing(request):
    return render(request, 'backoffice/hall_booking/holidays_landing.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Holidays'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_holidays(request):
    hall_location_list=HallLocation.objects.filter(is_deleted=False)
    data={'hall_location_list':hall_location_list}
    return render(request, 'backoffice/hall_booking/add_new_holiday.html',data)

@csrf_exempt
def save_new_holiday(request):
    try:
        print 'Exception IN | hall_holidays.py  | save_new_holiday | Start',
        holidayDate = request.POST.get('holiday_date')
        bookingdate = int(request.POST.get('bookingavailable'))

        
        try:
            holidayobj = Holiday.objects.get(
                holiday_date=datetime.datetime.strptime(request.POST.get('holiday_date'), '%d/%m/%Y'), holiday_status=0,
                is_deleted=False)

            data = {'success': 'alreadyExist'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception, e:
            print 'Handled Exception | hall_holidays | save_new_holiday | User . Handled Exception = ', e
            pass
        newholiday = Holiday(
            holiday_date= datetime.datetime.strptime(request.POST.get('holiday_date'), '%d/%m/%Y'),
            holiday_status= 0,
            holiday_type=int(request.POST.get('HolidayType')),
            is_booking_available=bookingdate,
        )
        newholiday.is_deleted = False
        newholiday.save()

        data = {
            'success': 'true',
        }
        print '\n Exception OUT | hall_holidays.py | save_new_hall_location | ', str(traceback.print_exc())
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'Exception OUT | hall_holidays.py  | save_new_holiday | End', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    print '\n Exception OUT | hall_holidays.py | save_new_holiday | ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
def edit_new_holiday(request):
    data={}
    try:
        print 'Exception IN | hall_holiday | views.py | edit_save_hall_location'


        holidayobj = Holiday.objects.get( id = request.POST.get('holiyobj_edit_id'))
        holidayobj.holiday_date=datetime.datetime.strptime(request.POST.get('edit_holiday_date'), '%d/%m/%Y')
        holidayobj.is_booking_available = int(request.POST.get('booking_available_edit'))
        holidayobj.holiday_type = int(request.POST.get('HolidayTypeEdit'))
        holidayobj.save()

        data = {'success': 'true',}

    except Exception, e:
             print e, str(traceback.print_exc())
             data = {'success': 'error'}

    return HttpResponse(json.dumps(data), content_type='application/json')



    # hall_holiday_obj = Holiday.objects.get(id=id)
        #
        #
        #
        # print "hall_holiday_obj ========",hall_holiday_obj
        #
        # hall_holiday_obj.holiday_date = datetime.datetime.strptime(request.POST.get('edit_holiday_date'),'%d/%m/%Y'),
        # hall_holiday_obj.is_booking_available = int(request.POST.get('booking_available_edit')),
        # hall_holiday_obj.holiday_type = int(request.POST.get('HolidayTypeEdit')),
        # # print "hall_holiday_obj=========",hall_holiday_obj.holiday_date
        # # print "holiday_type-----------",hall_holiday_obj.holiday_type
        # # print "is_booking_available-----",hall_holiday_obj.is_booking_available
        #
        # hall_holiday_obj.save()
        #
        #
        # data = {
        #     'success': 'true',
        # }

        # print '\n Exception OUT | hallbooking.py | edit_save_hall_location | ', str(traceback.print_exc())
    #     # return HttpResponse(json.dumps(data), content_type='application/json')
    # except Exception, e:
    #     print 'Exception OUT | hallbooking.py  | save_new_hall_location ', e
    #     data = {
    #         'success': 'false',
    #         'message': str(e)
    #     }
    # print '\n Exception OUT | hallbooking.py | edit_save_hall_location | ', str(traceback.print_exc())
    # return HttpResponse(json.dumps(data), content_type='application/json')



@csrf_exempt
def get_holiday_data(request):
    try:
        dataList = []
        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        print searchTxt

        select_status = request.GET.get('select_status')

        holiday_obj = Holiday.objects.filter(is_deleted=False)

        if select_status == "0" or select_status== "1":
            hall_holiday_objs = holiday_obj.filter(holiday_status=int(select_status))
        else:
            hall_holiday_objs = holiday_obj.filter()
        #
        # if searchTxt:
        #     hall_holiday_objs = holiday_obj.filter((Q(holiday_status=searchTxt)))
        # else:
        #     hall_holiday_objs = holiday_obj.filter()

        total_record = holiday_obj.count()

        i = 0

        for hall_holiday in hall_holiday_objs:
            i = i + 1
            tempList = []
            action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/backofficeapp/hall-holiday-edit/?hall_holiday_edit=' + str(
                hall_holiday.id) + '"></a>&nbsp;&nbsp;'
            if hall_holiday.holiday_status == 1:
                holiday_status = 'Inactive'
                status = '<label class="label label-default"> Inactive </label>'
                action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_holiday" onclick=update_holiday_details(' + '"' + str(
                    holiday_status) + '"' + ',' + str(hall_holiday.id) + ')></a>&nbsp; &nbsp;'
            else:
                holiday_status = 'Active'
                status = '<label class="label label-success"> Active </label>'
                action2 = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_holiday" onclick=update_holiday_details(' + '"' + str(
                    holiday_status) + '"' + ',' + str(hall_holiday.id) + ')></a>&nbsp; &nbsp;'

            tempList.append(i)
            tempList.append(hall_holiday.holiday_date.strftime('%d-%m-%Y'))
            tempList.append(status)
            tempList.append(hall_holiday.get_holiday_type_display())
            tempList.append(action1 + action2)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:

        print 'Exception OUT | hall_holidays.py  | get_holiday_data | End', e
        data = {
            'success': 'false',
            'message': str(e)
        }

        print '\n Exception OUT | hall_holidays.py | get_holiday_data | ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def update_holiday_status(request):
    try:
        print'Request IN | hall_holiday | update_holiday_status | = ',request.GET.get('hall_holiday_id')
        holiday_obj = Holiday.objects.get(id=str(request.GET.get('hall_holiday_id')))
        print "holiday_obj",holiday_obj.holiday_status

        if holiday_obj.holiday_status == 1:
            holiday_obj.holiday_status = 0
        else:
            holiday_obj.holiday_status = 1
        holiday_obj.save()
        data = {'success': 'true'}
    except Exception, e:
        data = {'success': 'false'}
        print '\nException OUT | update_location_detail_status = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Holidays'],login_url='/backofficeapp/login/',raise_exception=True)
@transaction.atomic
def hall_holiday_edit(request):
    data={}
    try:
        holiyobj = Holiday.objects.get(id=request.GET.get('hall_holiday_edit'))
        holiday_date = holiyobj.holiday_date.strftime('%d/%m/%Y')
        HolidayType=int(holiyobj.holiday_type)
        booking_available=int(holiyobj.is_booking_available)


        data = {'success' : 'true' , 'holiyobj' : holiyobj, 'holiday_date' : holiday_date,'bookingavailable':booking_available,'HolidayType': HolidayType}
        print"data_recived_onclick_edit_button)",data
    except Exception ,e:
        print '\nException OUT | update_location_detail_status = ', str(traceback.print_exc())
    return render(request, 'backoffice/hall_booking/holiday_edit.html',data)


def edit_hall_list_location(request):
    try:
        hall_list = []
        hall_objs = HallDetail.objects.filter(is_deleted=False, hall_location_id=request.GET.get('select_location')).order_by('hall_name')
        for hall_obj in hall_objs:
            hall_data = {
                'hall_id': hall_obj.id,
                'hall_name': hall_obj.hall_name
            }
            hall_list.append(hall_data)
        data = {'success': 'true', 'hall': hall_list}
    except Exception as exe:
        print exe
        data = {'success': 'false', 'hall': []}
    return HttpResponse(json.dumps(data), content_type='application/json')
    



def get_hall_list_location(request):
    try:
        hall_list = []
        hall_objs = HallDetail.objects.filter(is_deleted=False, hall_location_id=request.GET.get('select_location')).order_by('hall_name')
        for hall_obj in hall_objs:
            hall_data = {
                'hall_id': hall_obj.id,
                'hall_name': hall_obj.hall_name
            }
            hall_list.append(hall_data)
        data = {'success': 'true', 'hall': hall_list}
    except Exception as exe:
        print exe
        data = {'success': 'false', 'hall': []}
    return HttpResponse(json.dumps(data), content_type='application/json')