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
from datetime import date, datetime
import calendar
import urllib2
import random
import traceback

from adminapp.models import Committee
from eventsapp.models import EventDetails, EventType, EventRegistration, EventBannerImage
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import *
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Manage Halls'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def manage_hall_landing(request):
    data = {}
    hallLocationObj = HallLocation.objects.filter(is_deleted=False)

    data = {
        "hallLocationObj": hallLocationObj,

    }
    return render(request, 'backoffice/hall_booking/manage_hall_landing.html',data)


@csrf_exempt
def get_manage_halls_datatable(request):
    try:
        dataList = []
        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""

        select_status = request.GET.get('select_status')
        select_location = request.GET.get('select_location')
        select_hall_name = ''

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        try:
            list = ['id']

            column_name = order + list[int(column)]
        except Exception,e:
            pass

        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))


        hallDetail_obj = HallDetail.objects.filter(is_deleted=False)
        print"hallDetail_obj", hallDetail_obj,select_status,select_location

        if select_status == "0" or select_status == "1":
            if select_location:
                if select_hall_name:
                    hallDetail_objs = hallDetail_obj.filter(Q(hall_name__icontains=select_hall_name),status=int(select_status),hall_location_id = select_location)
                else:
                    hallDetail_objs = hallDetail_obj.filter(status=int(select_status), hall_location_id=select_location)
            else:
                if select_hall_name:
                    hallDetail_objs = hallDetail_obj.filter(Q(hall_name__icontains=select_hall_name),status=int(select_status))
                else:
                    hallDetail_objs = hallDetail_obj.filter(status=int(select_status))

        else:
            if select_location:
                if select_hall_name:
                    hallDetail_objs = hallDetail_obj.filter(Q(hall_name__icontains=select_hall_name),hall_location_id = select_location)
                else:
                    hallDetail_objs = hallDetail_obj.filter(hall_location_id=select_location)
            else:
                if select_hall_name:
                    hallDetail_objs = hallDetail_obj.filter(Q(hall_name__icontains=select_hall_name))
                else:
                    hallDetail_objs = hallDetail_obj.filter()

        if searchTxt:
            hallDetail_objs = hallDetail_objs.filter((Q(hall_name__icontains=searchTxt)))
        else:
            hallDetail_objs = hallDetail_objs.filter()

        total_record = hallDetail_obj.count()

        i = 0

        hallDetail_objs=hallDetail_objs[start:length]
        i=start
        for hallDetail in hallDetail_objs:

            i = i + 1
            tempList = []
            HallPricingObjs = HallPricing.objects.filter(hall_detail=hallDetail, is_deleted=False)
            if str(HallPricingObjs):
                hr8hallPrincingObj = HallPricing.objects.get(hall_detail=hallDetail, hours="8", is_deleted=False)
                hr4hallPrincingObj = HallPricing.objects.get(hall_detail=hallDetail, hours="4", is_deleted=False)
                hr2hallPrincingObj = HallPricing.objects.get(hall_detail=hallDetail, hours="2", is_deleted=False)
                if str(hr8hallPrincingObj):
                    eighthrprincing = 'M :&nbsp; &nbsp;' + str(hr8hallPrincingObj.member_price) + ' N :&nbsp; &nbsp;' + str(
                        hr8hallPrincingObj.nonmember_price)
                else:
                    hr8hallPrincingObj = ""
                if str(hr4hallPrincingObj):
                    fourhrprincing = 'M :&nbsp; &nbsp;' + str(hr4hallPrincingObj.member_price) + ' N :&nbsp; &nbsp;' + str(
                        hr4hallPrincingObj.nonmember_price)
                else:
                    fourhrprincing = ""
                if str(hr2hallPrincingObj):
                    twohrprincing = 'M :' "&nbsp; &nbsp;" + str(hr2hallPrincingObj.member_price) + '  N :&nbsp; &nbsp;' + str(
                        hr2hallPrincingObj.nonmember_price)
                else:
                    twohrprincing = ""
            else:
                hr8hallPrincingObj = ""
                fourhrprincing = ""
                twohrprincing = ""

            action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/backofficeapp/manage-hall-edit/?hall_id=' + str(
                hallDetail.id) + '"></a>&nbsp;&nbsp;'
            print "hallDetail.status",hallDetail.status
            if hallDetail.status == False:
                hallDetail_status = 'Inactive'
                status = '<label class="label label-default"> Inactive </label>'
                action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_hall" onclick=update_hall_details(' + '"' + str(
                    hallDetail_status) + '"' + ',' + str(hallDetail.id) + ')></a>&nbsp; &nbsp;'
            else:
                hallDetail_status = 'Active'
                status = '<label class="label label-success"> Active </label>'
                action2 = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_hall" onclick=update_hall_details(' + '"' + str(
                    hallDetail_status) + '"' + ',' + str(hallDetail.id) + ')></a>&nbsp; &nbsp;'

            tempList.append(i)
            tempList.append(str(hallDetail.hall_location.location))
            tempList.append(str(hallDetail.hall_name))
            tempList.append(hallDetail.capacity)
            tempList.append(hallDetail.seating_style)
            tempList.append(eighthrprincing)
            tempList.append(fourhrprincing)
            tempList.append(twohrprincing)
            tempList.append('M :&nbsp; &nbsp;' + str(hallDetail.extra_member_price) + ' N :&nbsp; &nbsp;' + str(
                    hallDetail.extra_nonmember_price))
            tempList.append(status)
            tempList.append(action1 + action2)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:

        print 'Exception OUT | manage_hall.py  | get_manage_halls_datatable | End', e
        data = {
            'success': 'false',
            'message': str(e)
        }

        print '\n Exception OUT | hall_holidays.py | get_holiday_data | ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Manage Halls'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_hall_details(request):
    data = {}

    hallLocationObj = HallLocation.objects.filter(is_deleted=False)
    hallFunctioningEquipment = HallFunctioningEquipment.objects.filter(is_deleted=False,is_active=True)
    # hallListObj = HallDetail.objects.filter(is_deleted=False)[:1]
    data = {
        "hallLocationObj": hallLocationObj,
        "hallFunctioningEquipment": hallFunctioningEquipment,
        # "hallListObj": hallListObj,
    }
    return render(request, 'backoffice/hall_booking/add_new_hall_details.html', data)

@csrf_exempt
def manage_get_hall_list(request):
    data={}
    i=0
    ss=''
    print request.POST
    try:
        location_id= request.POST.get('location_id')
        halllist = HallDetail.objects.filter(hall_location_id=location_id)
        for hall_obj in halllist:
            ss1 = "<div class='col-md-4'><div class='md-checkbox'>"
            ss2 = "<input type='checkbox' name='select_hall_id' value='"+str(hall_obj.id)+"' id='checkbox1_"+str(hall_obj.id)+"' class='md-check'>"
            ss3 = "<label for='checkbox1_"+str(hall_obj.id)+"'><span></span><span class='check'></span><span class='box'></span>"+ str(hall_obj.hall_name)+" </label></div></div>"
            ss = ss + ss1 + ss2 + ss3

        halllocobj=HallLocation.objects.get(id=location_id)
        address = halllocobj.address if halllocobj.address else ""

        data={'success':'true','hall_list':ss,'address':address}
    except Exception,e:
        print e
        pass

    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def edit_manage_get_hall_list(request):
    data={}
    i=0
    ss=''
    print request.POST
    try:
        location_id= request.POST.get('location_id')
        hall_detail_id= request.POST.get('hall_detail_id')
        halldetailobj =  HallDetail.objects.get(id=hall_detail_id)
        halllist = HallDetail.objects.filter(hall_location_id=location_id).exclude(id=hall_detail_id)
        for hall_obj in halllist:
            try:
                print halldetailobj.hall_merge
                list=[]
                if halldetailobj.hall_merge:
                    list=(halldetailobj.hall_merge).split(',')
            except Exception,e:
                print e
                pass
            check = "checked" if str(hall_obj.id) in list else ''
            ss1 = "<div class='col-md-4'><div class='md-checkbox'>"
            ss2 = "<input type='checkbox' name='select_hall_id' value='"+str(hall_obj.id)+"' id='checkbox1_"+str(hall_obj.id)+"' class='md-check'"+ check +">"
            ss3 = "<label for='checkbox1_"+str(hall_obj.id)+"'><span></span><span class='check'></span><span class='box'></span>"+ str(hall_obj.hall_name)+" </label></div></div>"
            ss = ss + ss1 + ss2 + ss3

        data={'success':'true','hall_list':ss}
    except Exception,e:
        print e
        pass

    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def save_hall_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | manage_hall | save_hall_details | user %s', request.user
        try:
            print request.POST
            equipmentList = []
            if request.POST.get('hallFacility'):
                equipmentList = (request.POST.get('hallFacility')).split(',')

            if request.POST.get('openForOnline') == "true":
                select_OpenForOnline = True
            else:
                select_OpenForOnline = False

            booking_start_time = datetime.strptime(request.POST.get('booking_start_time'), '%I:%M %p').time()
            booking_end_time = datetime.strptime(request.POST.get('booking_end_time'), '%I:%M %p').time()

            hallDetails = HallDetail(
                       hall_location=HallLocation.objects.get(id=request.POST.get('hallLocation')),
                       hall_name=request.POST.get('hallName'),
                       capacity=request.POST.get('hallCapacity'),
                       seating_style=request.POST.get('seatingStyle'),
                       longitude=request.POST.get('longitude_value'),
                       latitude=request.POST.get('lattitude_value'),
                       address=request.POST.get('address'),
                       extra_member_price=request.POST.get('chargesforExtrahrM'),
                       extra_nonmember_price=request.POST.get('chargesforExtrahrNM'),
                       booking_start_time=booking_start_time,
                       booking_end_time=booking_end_time,
                       status=True,
                       is_open_for_online=select_OpenForOnline,
                       )
            hallDetails.save()

            try:
                if request.POST.get('hallImage') != 'undefined':
                    hallDetails.hall_image = request.FILES.get('hallImage')
                else:
                    hallDetails.hall_image.name="/static/assets/images/no_image.png"

                hallDetails.save()
            except Exception,e:
                print e
                pass

            try:
                hallList = request.POST.get("hallList")
                if hallList:
                    hallList= hallList.split(',')
                    hallDetails.hall_merge = ",".join(hallList)
                    hallDetails.is_merge = True
                    hallDetails.save()

            except Exception,e:
                print e
                pass

            for i in equipmentList:
                hallDetails.hall_equipment.add(i)
                hallDetails.save()

                hallEquipementObj = HallEquipment(
                       hall_detail=HallDetail.objects.get(id=hallDetails.id),
                       hall_functioning_equipment=HallFunctioningEquipment.objects.get(id=i),
                       member_charges=request.POST.get('facility_nmcharge_'+i),
                       non_member_charges=request.POST.get('facility_mcharge_'+i),
                       is_active=True,
                    )
                hallEquipementObj.save()

            hallPricing = HallPricing(
                hall_detail=HallDetail.objects.get(id=hallDetails.id),
                                                   hours=8,
                                                   member_price=request.POST.get('chargesfor8hrM'),
                                                   nonmember_price=request.POST.get('chargesfor8hrNM'),
                                                   is_active=True
                                                   )
            hallPricing.save()
            hallPricing = HallPricing(
                hall_detail=HallDetail.objects.get(id=hallDetails.id),
                                                   hours=4,
                                                   member_price=request.POST.get('chargesfor4hrM'),
                                                   nonmember_price=request.POST.get('chargesfor4hrNM'),
                                                   is_active=True
                                                   )
            hallPricing.save()
            hallPricing = HallPricing(
                hall_detail=HallDetail.objects.get(id=hallDetails.id),
                                                   hours=2,
                                                   member_price=request.POST.get('chargesfor2hrM'),
                                                   nonmember_price=request.POST.get('chargesfor2hrNM'),
                                                   is_active=True
                                                   )
            hallPricing.save()


        except Exception, e:
            print 'exception ', str(traceback.print_exc())
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print 'Request OUT | manage_hall | save_hall_details | user %s', request.user
    except Exception, e:
        transaction.rollback(sid)
        print 'exception ', str(traceback.print_exc())
        print 'Exception|manage_hall | save_hall_details |User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@transaction.atomic
def update_hall_status(request):
    try:
        print'Request IN | manage_hall| update_hall_status | = ',request.GET.get('hall_id')
        hallDetail_obj = HallDetail.objects.get(id=str(request.GET.get('hall_id')))
        print "hallDetail_obj",hallDetail_obj.status

        if hallDetail_obj.status == True:
            print "fdhgdkhjdlfjn"
            hallDetail_obj.status = False
        else:
            hallDetail_obj.status = True
        hallDetail_obj.save()
        print hallDetail_obj.status
        data = {'success': 'true'}
    except Exception, e:
        data = {'success': 'false'}
        print '\nException OUT | update_hall_status = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Manage Halls'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def manage_hall_edit(request):
    data = {}
    print  "request.POST.get",request.GET.get("hall_id")
    hallLocationObj = HallLocation.objects.filter(is_deleted=False)
    hallFunctioningEquipment = HallFunctioningEquipment.objects.filter(is_deleted=False,is_active=True)
    hallDetails = HallDetail.objects.get(id=request.GET.get("hall_id"),is_deleted=False)
    hr8hallPrincingObj = HallPricing.objects.get(hall_detail=hallDetails, hours="8", is_deleted=False)
    hr4hallPrincingObj = HallPricing.objects.get(hall_detail=hallDetails, hours="4", is_deleted=False)
    hr2hallPrincingObj = HallPricing.objects.get(hall_detail=hallDetails, hours="2", is_deleted=False)
    hall_list = HallDetail.objects.filter(hall_location=hallDetails.hall_location,is_deleted=False).exclude(id=request.GET.get("hall_id"))
    HallFacilityObjList = HallEquipment.objects.filter(hall_detail = hallDetails)
    data = {
        "hallLocationObj": hallLocationObj,
        "hallFunctioningEquipment": hallFunctioningEquipment,
        "hallDetails" : hallDetails,
        "location_id" :str(hallDetails.hall_location.id),
        "hr8hallPrincingObj":hr8hallPrincingObj,
        "hr4hallPrincingObj":hr4hallPrincingObj,
        "hr2hallPrincingObj":hr2hallPrincingObj,
        "selectHallEquipment" : [hallFunctioningEquipment.id for hallFunctioningEquipment in hallDetails.hall_equipment.all()],
        "img_url":hallDetails.hall_image.url if hallDetails.hall_image else "/static/assets/images/no_image.png",
        "is_image":True if hallDetails.hall_image else False,
        "hall_list":hall_list,
        'HallFacilityObjList':HallFacilityObjList,
    }
    return render(request, 'backoffice/hall_booking/edit_new_hall_details.html', data)



def hall_equipment_list(request):
    data = {}

    print  "request.POST.get",request.GET.get("hall_detail_id")
    selectHall=[]
    #hallFunctioningEquipment = HallFunctioningEquipment.objects.filter(is_deleted=False)
    hallDetails = HallDetail.objects.get(id=request.GET.get("hall_detail_id"),is_deleted=False)
    if hallDetails.hall_merge:
        selectHall=(hallDetails.hall_merge).split(',')

    selectHallEquipmentList = str()

    data = {
        'success':'true',
        "selectHallEquipment" : [hallFunctioningEquipment.id for hallFunctioningEquipment in hallDetails.hall_equipment.all()],
        "selectHall":selectHall
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

@transaction.atomic
@csrf_exempt
def edit_hall_details(request):

    try:
        sid = transaction.savepoint()
        print 'Request IN | manage_hall | edit_hall_details | user %s', request.user,request.POST.get("hall_detail_id")
        try:
            try:
                HallDetail.objects.get(~Q(id=request.POST.get("hall_detail_id")),
                                       hall_location_id=request.POST.get('hallLocation'),
                                       hall_name=request.POST.get('hallName'))

                data = {'success': 'Exist'}
                return HttpResponse(json.dumps(data), content_type='application/json')

            except HallDetail.DoesNotExist,e:
                print request.POST

                hallDetails = HallDetail.objects.get(id=request.POST.get("hall_detail_id"))
                hallDetails.hall_location_id = request.POST.get('hallLocation')
                hallDetails.hall_name = request.POST.get('hallName')
                hallDetails.capacity = request.POST.get('hallCapacity')
                hallDetails.address = request.POST.get('address')
                hallDetails.longitude = request.POST.get('longitude_value')
                hallDetails.latitude = request.POST.get('lattitude_value')
                hallDetails.seating_style = request.POST.get('seatingStyle')
                hallDetails.extra_member_price = request.POST.get('chargesforExtrahrM')
                hallDetails.extra_nonmember_price = request.POST.get('chargesforExtrahrNM')
                hallDetails.status = True
                hallDetails.is_open_for_online = True if request.POST.get('openForOnline') == "true" else False
                hallDetails.booking_start_time = datetime.strptime(request.POST.get('booking_start_time'), '%I:%M %p').time()
                hallDetails.booking_end_time = datetime.strptime(request.POST.get('booking_end_time'), '%I:%M %p').time()
                hallDetails.save()

                try:
                    if request.POST.get('image_flag') == 'change':
                        if request.POST.get('hallImage') != 'undefined':
                            hallDetails.hall_image = request.FILES.get('hallImage')
                            hallDetails.save()
                    elif request.POST.get('image_flag') == 'removed':
                        hallDetails.hall_image.name = "/static/assets/images/no_image.png"
                        hallDetails.save()
                    else:
                        pass
                except Exception, e:
                    print e
                    pass
                try:
                    hallList = request.POST.get("hallList")
                    if hallList:
                        hallList = hallList.split(',')
                        print hallList
                        hallDetails.hall_merge = ",".join(hallList)
                        hallDetails.is_merge = True

                        hallDetails.save()
                    else:
                        hallDetails.hall_merge = None
                        hallDetails.is_merge = False
                        hallDetails.save()
                except Exception, e:
                    print e
                    pass

                equipmentList = []
                if request.POST.get('hallFacility'):
                    equipmentList = (request.POST.get('hallFacility')).split(',')
                
                hallDetails.hall_equipment.clear()
                HallEquipment.objects.filter(hall_detail=hallDetails).delete()
                for i in equipmentList:
                    hallDetails.hall_equipment.add(i)
                    hallDetails.save()

                    hallEquipementObj = HallEquipment(
                           hall_detail=HallDetail.objects.get(id=hallDetails.id),
                           hall_functioning_equipment=HallFunctioningEquipment.objects.get(id=i),
                           member_charges=request.POST.get('facility_nmcharge_'+i) if request.POST.get('facility_nmcharge_'+i) else 0,
                           non_member_charges=request.POST.get('facility_mcharge_'+i) if request.POST.get('facility_mcharge_'+i) else 0,
                           is_active=True,
                        )
                    hallEquipementObj.save()


                hallPricing = HallPricing.objects.get(hall_detail_id=request.POST.get("hall_detail_id"), hours=8)
                hallPricing.member_price = request.POST.get('chargesfor8hrM')
                hallPricing.nonmember_price = request.POST.get('chargesfor8hrNM')
                hallPricing.is_active = True
                hallPricing.save()

                hallPricing = HallPricing.objects.get(hall_detail_id=request.POST.get("hall_detail_id"), hours=4)
                hallPricing.member_price = request.POST.get('chargesfor4hrM')
                hallPricing.nonmember_price = request.POST.get('chargesfor4hrNM')
                hallPricing.is_active = True
                hallPricing.save()

                hallPricing = HallPricing.objects.get(hall_detail_id=request.POST.get("hall_detail_id"), hours=2)
                hallPricing.member_price = request.POST.get('chargesfor2hrM')
                hallPricing.nonmember_price = request.POST.get('chargesfor2hrNM')
                hallPricing.is_active = True
                hallPricing.save()
                transaction.savepoint_commit(sid)

                data = {'success': 'true'}
                return HttpResponse(json.dumps(data), content_type='application/json')


            except Exception,e:
                print e
                pass
                data = {'success': 'false'}
                return HttpResponse(json.dumps(data), content_type='application/json')

        except Exception, e:
            transaction.rollback(sid)
            print 'exception ', str(traceback.print_exc())
            data = {'success': 'false'}
            return HttpResponse(json.dumps(data), content_type='application/json')


    except Exception, e:
        transaction.rollback(sid)
        print 'exception ', str(traceback.print_exc())
        print 'Exception|manage_hall | save_hall_details |User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_hall_facility_list(request):
    data = {}
    hallFunctioningEquipment = HallFunctioningEquipment.objects.filter(is_deleted=False,is_active=True)
    data = {
        'success':'true',
        'hallFunctioningEquipment': hallFunctioningEquipment,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
