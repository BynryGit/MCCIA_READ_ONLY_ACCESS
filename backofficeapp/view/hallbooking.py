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
from django.core.serializers.json import DjangoJSONEncoder

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
import sys

from adminapp.models import Committee
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallLocation

from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required





@csrf_exempt
def hall_booking_landing(request):
    return render(request, 'backoffice/hall_booking/hall_booking_landing.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Locations'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def hall_location(request):
    return render(request, 'backoffice/hall_booking/hall_location.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Locations'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_hall_location(request):
    try:
        system_user_list = SystemUserProfile.objects.filter(is_deleted=False)
        print "system_user_list =========",system_user_list

        data = {
            'success': 'true',
            'system_user_list': system_user_list
        }
        print "data===add_new_consumer==", data

    except Exception, e:
         print 'Exception | hallbooking | views.py | add_new_hall_location', e
    return render(request, 'backoffice/hall_booking/add_new_hall_location.html',data)

@csrf_exempt
def hall_booking_details(request):
    return render(request, 'backoffice/hall_booking/hall_location.html')

@csrf_exempt
def save_new_hall_location(request):
    try:
        print request.POST
        print 'Exception IN|hallbooking | views.py | save_new_hall_location'
        try:
            a=HallLocation.objects.get(
                location=request.POST.get('hall_location'),
                is_deleted=False)
            print a
            data = {'success': 'alreadyExist'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except HallLocation.DoesNotExist,e:
            if request.POST.get('deposit_holiday_factor'):
                deposit_holiday_factor = request.POST.get('deposit_holiday_factor')
            else:
                deposit_holiday_factor = 0.00

            new_hall_location = HallLocation(
                location=request.POST.get('hall_location'),
                terms_condition=request.POST.get('terms_condition'),
                contact_person1_id=request.POST.get('contact_person1'),
                contact_person2_id=request.POST.get('contact_person2') if request.POST.get('contact_person2') else None,
                deposit=request.POST.get('deposit'),
                address=request.POST.get('address'),
                hall_rent_on_holiday=request.POST.get('hall_rent_holiday'),
                deposit_holiday_factor=deposit_holiday_factor,
                meta_title=request.POST.get('meta_title'),
                meta_keywords=request.POST.get('meta_keyword'),
                meta_description=request.POST.get('meta_description'),
                meta_keyphrases=request.POST.get('meta_key_phrase')
            )
            new_hall_location.save()

            data = {
                'success': 'true',
            }

            return HttpResponse(json.dumps(data), content_type='application/json')

        except Exception, e:
            print e
            data = {
                'success': 'false',
                'message': str(e)
            }

    except Exception, e:
        print e
        data = {
            'success': 'false',
            'message': str(e)
        }

    return HttpResponse(json.dumps(data), content_type='application/json')



def get_hall_location_data(request):
    try:
        print 'backofficeapp | hall booking.py | get_hall_location_data | user'
        dataList = []
        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')

        # order = ""
        # if request.GET.get('order[0][dir]') == 'desc':
        #     order = "-"
        # list = ['','']
        # column_name = order + list[int(column)]
        # start = request.GET.get('start')
        # length = int(request.GET.get('length')) + int(request.GET.get('start'))

        select_status = request.GET.get('select_status')

        hall_loc_obj_list = HallLocation.objects.all()

        if select_status == "Inactive":
            hall_loc_obj_list = hall_loc_obj_list.filter(is_deleted=True)
        elif select_status == "Active":
            hall_loc_obj_list = hall_loc_obj_list.filter(is_deleted=False)

        if searchTxt:
            hall_loc_obj_list = hall_loc_obj_list.filter(Q(location__icontains=searchTxt))

        total_record = hall_loc_obj_list.count()

        i= 0
        for hall_loc in hall_loc_obj_list:
            i = i+1
            tempList = []
            action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/backofficeapp/hall-location-edit/?hall_location_edit=' + str(
                hall_loc.id) + '"></a>&nbsp;&nbsp;'

            if hall_loc.is_deleted:
                location_status = 'Inactive'
                status = '<label class="label label-default"> Inactive </label>'
                action2 = '<a class="icon-reload" data-toggle="modal" data-target=#active_deactive_location onclick=update_location_details(' + '"' + str(location_status) + '"' + ',' + str(hall_loc.id) + ')></a>'
            else:
                location_status = 'Active'
                status = '<label class="label label-success"> Active </label>'
                action2 = '<a class="icon-trash" data-toggle="modal" data-target=#active_deactive_location onclick=update_location_details(' + '"' + str(
                    location_status) + '"' + ',' + str(hall_loc.id) + ')></a>'

            tempList.append(i)
            tempList.append(hall_loc.location)
            tempList.append(hall_loc.deposit)
            tempList.append(hall_loc.hall_rent_on_holiday)
            tempList.append(status)
            tempList.append(action1 + action2)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print 'Exception OUT | hallbooking | get_hall_location_data | End', str(traceback.print_exc())
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


@transaction.atomic
def update_location_detail_status(request):
    print '\nException IN | update_location_detail_status =', request.user
    data = {}
    sid = transaction.savepoint()
    try:
        halllocobj = HallLocation.objects.get(id=str(request.GET.get('hall_location_id')))

        if halllocobj.is_deleted:
            halllocobj.is_deleted = False
        else:
            halllocobj.is_deleted = True

        halllocobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException OUT | update_location_detail_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Locations'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def hall_location_edit(request):
    try:
        halllocobj = HallLocation.objects.get(id=request.GET.get('hall_location_edit'))
        system_user_list = SystemUserProfile.objects.filter(is_deleted=False)
        data = {
            'hall_location_id': request.GET.get('hall_location_edit'),
            'system_user_list': system_user_list,
            'hall_location_edit':halllocobj,
        }
        print "=======data===========",data
    except Exception, e:
        print 'Exception OUT | hall_location | hall_location_edit | user %s. Exception = ', str(traceback.print_exc())
    return render(request, 'backoffice/hall_booking/edit_hall_location.html', data)


@csrf_exempt
def edit_save_hall_location(request):
    # pdb.set_trace()
    try:
        print 'Exception IN | hallbooking | views.py | edit_save_hall_location---------'

        id = request.POST.get('hall_location_edit_id')
        try:
            HallLocation.objects.get(~Q(id=id),location=request.POST.get('edit_hall_location_detail'))
            data = {'success': 'Alreadyexist'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except HallLocation.DoesNotExist,e:
            pass

            contact_person1 = request.POST.get('edit_contact_person1')
            contact_person2 = request.POST.get('edit_contact_person2')
            halllocobj=HallLocation.objects.get(id=id)
            halllocobj.location = request.POST.get('edit_hall_location_detail')
            halllocobj.contact_person1_id =  contact_person1 if contact_person1 else None
            halllocobj.contact_person2_id =  contact_person2 if contact_person2 else None
            halllocobj.terms_condition = request.POST.get('edit_terms_condition')
            halllocobj.deposit = request.POST.get('edit_deposit')
            halllocobj.address = request.POST.get('edit_address')
            halllocobj.hall_rent_on_holiday = request.POST.get('edit_hall_rent_holiday')
            halllocobj.deposit_holiday_factor = request.POST.get('edit_deposit_holiday_factor')

            halllocobj.meta_title = request.POST.get('edit_meta_title')
            halllocobj.meta_keywords = request.POST.get('edit_meta_keyword')
            halllocobj.meta_description = request.POST.get('edit_meta_description')
            halllocobj.meta_keyphrases = request.POST.get('edit_meta_key_phrase')
            halllocobj.save()
            data = {
                'success': 'true',
            }
            print '\n Exception OUT | hallbooking.py | edit_save_hall_location | ', str(traceback.print_exc())
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception,e:
            print e
            data = {
                'success': 'false',
            }
    except Exception, e:
        print 'Exception OUT | hallbooking.py  | edit_save_hall_location ', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    print '\n Exception OUT | hallbooking.py | edit_save_hall_location | ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')