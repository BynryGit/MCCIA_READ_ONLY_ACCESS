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
from eventsapp.models import EventDetails, EventType, EventRegistration, EventBannerImage
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallFunctioningEquipment
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Equipments'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def hall_equipment_landing(request):
    return render(request, 'backoffice/hall_booking/hall_equipment_landing.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Equipments'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_hall_equipment(request):
    return render(request, 'backoffice/hall_booking/add_new_hall_equipment.html')

@csrf_exempt
def save_new_hall_equipment(request):
    data={}
    print request.POST
    sid = transaction.savepoint()
    try:
        equipment_name = request.POST.get('equipment_name')
        if request.method == 'POST':
            hallequipmentobj = HallFunctioningEquipment(
                equipment_name=equipment_name,
            )
            hallequipmentobj.save()
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

def load_hall_equipment_table(request):
    try:
        dataList = []
        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        print '.............',searchTxt
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
                equipmentObjs = HallFunctioningEquipment.objects.filter(is_deleted=False,is_active=True)
            elif request.GET.get('sort_var') == "0":
                equipmentObjs = HallFunctioningEquipment.objects.filter(is_deleted=False,is_active=False)
            else:
                equipmentObjs = HallFunctioningEquipment.objects.filter(is_deleted=False)

            if searchTxt:
                equipmentObjs=equipmentObjs.filter(Q(equipment_name__icontains=searchTxt))

            total_record=equipmentObjs.count()
            equipmentObjsList = equipmentObjs.order_by(column_name)[start:length]
            i=0
            a=1
            for equObj in equipmentObjsList:
                i = start + a
                a = a + 1
                tempList = []

                if equObj.is_active == True:
                    equipment_status = 'True'
                    status = '<label class="label label-success"> Active </label>'
                    action= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_equipment" onclick=update_equipment_status(' + '"' + str(equipment_status) + '"' + ',' + str(equObj.id) + ')></a>&nbsp; &nbsp;'
                else:
                    equipment_status = 'False'
                    status = '<label class="label label-default"> Inactive </label>'
                    action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_equipment" onclick=update_equipment_status(' + '"' + str(
                        equipment_status) + '"' + ',' + str(equObj.id) + ')></a>&nbsp; &nbsp;'

                edit_icon = '<a class="icon-pencil" onClick="edit_equipment_open(' + str(equObj.id) + ')"></a> &nbsp; &nbsp;'

                tempList.append(str(i))
                tempList.append(equObj.equipment_name)
                tempList.append(equObj.created_date.strftime('%d %B %Y - %H:%M'))
                tempList.append(status)

                tempList.append(edit_icon + action)
                dataList.append(tempList)

        except Exception, e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|Backofficeapp | load_hall_equipment_table | User:{0} - Excepton:{1}'.format(
                request.user, e)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|Backofficeapp | load_hall_equipment_table|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')    


@transaction.atomic
def update_hall_equipment_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('equipment_id')
        equipmentobj = HallFunctioningEquipment.objects.get(id=str(request.GET.get('equipment_id')))
        if equipmentobj.is_active is True:
            equipmentobj.is_active = False
        else:
            equipmentobj.is_active = True
        equipmentobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_hall_equipment_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_hall_equipment_details(request):
    data={}
    equipment_id=request.GET.get('equipment_id')
    equipmentobj=HallFunctioningEquipment.objects.get(id=equipment_id)
    data={'equipment_name':equipmentobj.equipment_name,'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_edit_hall_equipment(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user
        if request.POST:
            print request.POST
            equipment_id = request.POST.get('equipment_id')
            equipment_name = request.POST.get('equipment_name')
            equipmentobj = HallFunctioningEquipment.objects.get(id=equipment_id)
            equipmentobj.equipment_name = equipment_name
            equipmentobj.save()

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