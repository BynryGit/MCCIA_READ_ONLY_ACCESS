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

from adminapp.models import Committee,Country,State,City,Servicetax
from eventsapp.models import EventDetails, EventType, EventRegistration,EventParticipantUser
from backofficeapp.models import SystemUserProfile,UserPrivilege,UserRole,Department,Designation
import datetime
from authenticationapp.decorator import role_required

from django.contrib.auth.decorators import login_required


@login_required(login_url='/backofficeapp/login/')
# @role_required(privileges=['Dashboard', 'Membership', 'Hall Booking', 'Event', 'Administrator'],login_url='/backofficeapp/login/',raise_exception=True)
# @role_required(privileges=['Administrator'],login_url='/backofficeapp/login/',raise_exception=True)
# @role_required(privileges=['Administrator'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_landing(request):
    return render(request, 'backoffice/administrator/administrator_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Country'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_country_landing(request):
    return render(request, 'backoffice/administrator/country_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Country'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_country(request):
    return render(request, 'backoffice/administrator/add_country.html')


@csrf_exempt
def save_country_details(request):
    sid = transaction.savepoint()
    try:
        country_name = request.POST.get('country_name')
        if request.method == 'POST':
            if Country.objects.filter(country_name=country_name):
                data = {'success': 'exist'}
            else:
                countryobj = Country(
                    country_name=country_name
                )
                countryobj.save()
                transaction.savepoint_commit(sid)

                data = {'success': 'true'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_country_list(request):
    try:
        print 'backofficeapp | event_home.py | get_delete_events | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'country_name']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        country_list = Country.objects.filter(is_deleted=False)  # .order_by(column_name)
        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                country_list=country_list.filter(is_active=True)
            else:
                country_list = country_list.filter(is_active=False)
        if searchTxt:
            country_list = country_list.filter(Q(country_name__icontains=searchTxt))

        total_record = country_list.count()
        country_list = country_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in country_list:
            i = start + a
            a = a + 1
            if obj.is_active:
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_country_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_country_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=editSlabDetailsModal("+ str(obj.id)+")></a> &nbsp; &nbsp;"
            tempList = []
            tempList.append(str(i))
            # tempList.append(obj.id)
            tempList.append(obj.country_name)
            tempList.append(status)
            tempList.append(action + edit_icon)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def show_country_detail(request):
    data = {}
    country_id = request.GET.get('country_id')
    countryobj = Country.objects.get(id=country_id)
    data = {'abc': countryobj.country_name, 'success': 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_country_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user

        if request.POST:
            country_id = request.POST.get('country_id')
            country_name = request.POST.get('country_name')
            try:
                Country.objects.get(~Q(id=country_id),country_name=country_name)
            except Country.DoesNotExist,e:
                countryobj = Country.objects.get(id=country_id)

                countryobj.country_name = country_name
                countryobj.save()
                transaction.savepoint_commit(sid)
                data = {'success': 'true'}
            except Exception,e:
                print e
                pass
                transaction.rollback(sid)
                data = {'success': 'false'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_country_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_country_id')
        countryobj = Country.objects.get(id=str(request.GET.get('status_country_id')))
        if countryobj.is_active:
            countryobj.is_active = False
        else:
            countryobj.is_active = True

        countryobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['State'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_state_landing(request):
    country_list = Country.objects.filter(is_active = True)
    data = {'country_list': country_list}
    return render(request, 'backoffice/administrator/state_landing.html',data)


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['State'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_state(request):
    country_list = Country.objects.filter(is_active = True)
    data={'country_list':country_list}
    return render(request, 'backoffice/administrator/add_state.html',data)


@csrf_exempt
def save_state_details(request):
    print request.POST
    sid = transaction.savepoint()
    try:
        state_name = request.POST.get('state_name')
        country_id = request.POST.get('country_id')
        if request.method == 'POST':
            if State.objects.filter(country_id=country_id,state_name=state_name):
                data = {'success': 'exist'}
            else:
                stateobj = State(
                    state_name=state_name,
                    country_id=country_id,
                )
                stateobj.save()
                transaction.savepoint_commit(sid)

                data = {'success': 'true'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_state_list(request):
    try:
        print 'backofficeapp | event_home.py | get_delete_events | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'state_name']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        state_list = State.objects.filter(is_deleted=False)  # .order_by(column_name)
        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                state_list=state_list.filter(is_active=True)
            else:
                state_list = state_list.filter(is_active=False)
        if searchTxt:
            state_list = state_list.filter(Q(state_name__icontains=searchTxt))

        total_record = state_list.count()
        state_list = state_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in state_list:
            i = start + a
            a = a + 1
            if obj.is_active:
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_state_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_state_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=editSlabDetailsModal("+ str(obj.id)+")></a> &nbsp; &nbsp;"
            tempList = []
            # tempList.append(obj.id)
            tempList.append(str(i))
            tempList.append(obj.country.country_name)
            tempList.append(obj.state_name)
            tempList.append(status)
            tempList.append(action + edit_icon)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def show_state_detail(request):
    data = {}
    state_id = request.GET.get('state_id')
    stateobj = State.objects.get(id=state_id)
    data = {'abc': stateobj.state_name,'country_id':stateobj.country_id, 'success': 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_state_details(request):

    sid = transaction.savepoint()

    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user

        if request.POST:
            print request.POST
            state_id = request.POST.get('state_id')
            state_name = request.POST.get('state_name')
            country_id = request.POST.get('country_id')
            try:
                State.objects.get(~Q(id=state_id),country_id=country_id,state_name=state_name)
            except State.DoesNotExist,e:
                stateobj = State.objects.get(id=state_id)
                stateobj.state_name = state_name
                stateobj.country_id = country_id
                stateobj.save()
                transaction.savepoint_commit(sid)
                data = {'success': 'true'}
            except Exception,e:
                print e
                pass
                data = {'success': 'false'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_state_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_state_id')
        stateobj = State.objects.get(id=str(request.GET.get('status_state_id')))
        if stateobj.is_active:
            stateobj.is_active = False
        else:
            stateobj.is_active = True

        stateobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['City'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_city_landing(request):
    state_list = State.objects.filter(is_active = True)
    data={'state_list':state_list}
    return render(request, 'backoffice/administrator/city_landing.html',data)


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['City'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_city(request):
    state_list = State.objects.filter(is_active = True)
    data = {'state_list': state_list}
    return render(request, 'backoffice/administrator/add_city.html',data)


@csrf_exempt
def save_city_details(request):
    print request.POST
    sid = transaction.savepoint()
    try:
        city_name = request.POST.get('city_name')
        state_id = request.POST.get('state_id')
        if request.method == 'POST':
            if City.objects.filter(state_id=state_id,city_name=city_name.lower()):
                data = {'success': 'exist'}
            else:
                cityobj = City(
                    city_name=city_name,
                    state_id=state_id,
                )
                cityobj.save()
                transaction.savepoint_commit(sid)

                data = {'success': 'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_city_list(request):
    try:
        print 'backofficeapp | event_home.py | get_delete_events | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'city_name']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        city_list = City.objects.filter(is_deleted=False)  # .order_by(column_name)
        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                city_list=city_list.filter(is_active=True)
            else:
                city_list = city_list.filter(is_active=False)
        if searchTxt:
            city_list = city_list.filter(Q(city_name__icontains=searchTxt))

        total_record = city_list.count()
        city_list = city_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in city_list:
            i = start + a
            a = a + 1
            if obj.is_active:
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_city_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_city_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=editSlabDetailsModal("+ str(obj.id)+")></a> &nbsp; &nbsp;"
            tempList = []
            tempList.append(str(i))
            # tempList.append(obj.id)
            tempList.append(obj.state.state_name if obj.state else 'NA')
            tempList.append(obj.city_name)
            tempList.append(status)
            tempList.append(action + edit_icon)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def show_city_detail(request):
    data = {}
    city_id = request.GET.get('city_id')
    cityobj = City.objects.get(id=city_id)
    data = {'abc': cityobj.city_name,'state_id':cityobj.state_id, 'success': 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_city_details(request):

    sid = transaction.savepoint()

    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user

        if request.POST:
            print request.POST
            city_id = request.POST.get('city_id')
            city_name = request.POST.get('city_name')
            state_id = request.POST.get('state_id')

            cityobj = City.objects.get(id=city_id)
            cityobj.city_name = city_name
            cityobj.state_id = state_id
            cityobj.save()
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


@csrf_exempt
def update_city_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_city_id')
        cityobj = City.objects.get(id=str(request.GET.get('status_city_id')))
        if cityobj.is_active:
            cityobj.is_active = False
        else:
            cityobj.is_active = True

        cityobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Service Tax'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_servicetax_landing(request):
    return render(request, 'backoffice/administrator/servicetax_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Service Tax'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_servicetax(request):
    return render(request, 'backoffice/administrator/add_servicetax.html')


@csrf_exempt
def save_servicetax_details(request):
    print request.POST
    sid = transaction.savepoint()
    try:
        select_state = request.POST.get('select_state')
        if request.method == 'POST':
            if select_state == '0':
                cgst_tax = float(request.POST.get('cgst_tax'))
                sgst_tax = float(request.POST.get('sgst_tax'))
                if Servicetax.objects.filter(cgst=round(cgst_tax,2),sgst=round(sgst_tax,2)):
                    data = {'success': 'exist'}
                else:
                    Servicetax.objects.filter(tax_type=0,is_active=True).update(is_active=False)
                    servicetaxobj = Servicetax(
                        tax= round(round(cgst_tax,2) + round(sgst_tax,2)),
                        cgst=round(cgst_tax,2),
                        sgst=round(sgst_tax,2),
                        tax_type=0
                    )
                    servicetaxobj.save()
                    data = {'success': 'true'}
                    transaction.savepoint_commit(sid)
            else:
                igst_tax = float(request.POST.get('igst_tax'))
                if Servicetax.objects.filter(tax=round(igst_tax,2),tax_type=1, is_active=True):
                    data = {'success': 'exist'}
                else:
                    Servicetax.objects.filter(tax_type=1, is_active=True).update(is_active=False)
                    servicetaxobj = Servicetax(
                        tax= round(igst_tax,2),
                        tax_type=1
                    )
                    servicetaxobj.save()
                    data = {'success': 'true'}
                transaction.savepoint_commit(sid)
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        print e
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_servicetax_list(request):
    try:
        print 'backofficeapp | event_home.py | get_delete_events | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'servicetax_name']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        servicetax_list = Servicetax.objects.filter(is_deleted=False)  # .order_by(column_name)
        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                servicetax_list=servicetax_list.filter(is_active=True)
            else:
                servicetax_list = servicetax_list.filter(is_active=False)
        if searchTxt:
            servicetax_list = servicetax_list.filter(Q(amount__icontains=searchTxt))

        total_record = servicetax_list.count()
        servicetax_list = servicetax_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in servicetax_list:
            i = start + a
            a = a + 1
            if obj.is_active:
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_servicetax_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_servicetax_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=editSlabDetailsModal("+ str(obj.id)+")></a> &nbsp; &nbsp;"
            tempList = []
            tempList.append(str(i))

            # tempList.append(obj.amount)
            if obj.tax_type == 0:
                tempList.append(obj.tax)
                tempList.append('-')
                tempList.append(obj.cgst)
                tempList.append(obj.sgst)
            else:
                tempList.append('-')
                tempList.append(obj.tax)
                tempList.append('-')
                tempList.append('-')


            tempList.append(status)
            tempList.append(action + edit_icon)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def show_servicetax_detail(request):
    data = {}
    servicetax_id = request.GET.get('servicetax_id')
    servicetaxobj = Servicetax.objects.get(id=servicetax_id)
    if servicetaxobj.tax_type ==0:
        data = {'tax_type':'0','cgst':servicetaxobj.cgst,'sgst':servicetaxobj.sgst, 'success': 'true'}
    else:
        data = {'tax_type':'1', 'igst': servicetaxobj.tax, 'success': 'true'}

    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_servicetax_details(request):
    sid = transaction.savepoint()
    try:
        if request.POST:
            servicetax_id = request.POST.get('servicetax_id')
            servicetaxobj = Servicetax.objects.get(id=servicetax_id)
            if servicetaxobj.tax_type == 0:
                cgst_tax = float(request.POST.get('cgst_tax'))
                sgst_tax = float(request.POST.get('sgst_tax'))
                servicetaxobj.tax = round(round(cgst_tax, 2) + round(sgst_tax, 2))
                servicetaxobj.sgst = round(sgst_tax,2)
                servicetaxobj.cgst = round(cgst_tax,2)
                servicetaxobj.save()
            else:
                igst_tax = float(request.POST.get('igst_tax'))
                servicetaxobj.tax = round(igst_tax,2)
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


@csrf_exempt
def update_servicetax_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_servicetax_id')
        servicetaxobj = Servicetax.objects.get(id=str(request.GET.get('status_servicetax_id')))
        if servicetaxobj.is_active:
            servicetaxobj.is_active = False
        else:
            servicetaxobj.is_active = True
            Servicetax.objects.filter(~Q(id=str(request.GET.get('status_servicetax_id'))),tax_type=servicetaxobj.tax_type).update(is_active=False)

        servicetaxobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
# @role_required(privileges=['Administrator'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_user_role_landing(request):
    # if not request.user.is_authenticated():
    #     return render(request, 'login.html')
    # else:

    privilege_list = UserPrivilege.objects.filter(is_deleted=False)
    data = {'privilege_list': privilege_list}

    return render(request, 'backoffice/administrator/user_role_landing.html',data)


@csrf_exempt
def get_user_role_list(request):
    try:
        print 'backofficeapp | adminstrator.py | get_user_role_list | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'role']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        role_list = UserRole.objects.filter(is_deleted=False)  # .order_by(column_name)
        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                role_list=role_list.filter(is_active=True)
            else:
                role_list = role_list.filter(is_active=False)
        if searchTxt:
            role_list = role_list.filter(Q(role__icontains=searchTxt))

        total_record = role_list.count()
        role_list = role_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in role_list:
            i = start + a
            a = a + 1
            if obj.is_active:
                role_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_user_role" onclick=update_user_role_status(' + '"' + str(
                    role_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                role_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_user_role" onclick=update_user_role_status(' + '"' + str(
                    role_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=edit_user_role_modal("+ str(obj.id)+")></a> &nbsp; &nbsp;"

            tempList = []
            tempList.append(str(i))
            tempList.append(obj.role)
            tempList.append(obj.description)
            tempList.append(obj.created_on.strftime('%B %d,%Y'))
            tempList.append(status)
            tempList.append(action + edit_icon)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | adminstrator.py | get_user_role_list | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_user_role_detail(request):
    try:
        print 'views.py|get_role_details'
        data = {}
        final_list = []
        try:
            i = 11
            plist = []
            role_obj = UserRole.objects.get(id=request.GET.get('user_role_id'))
            privilege_obj = role_obj.privilege.all()

            for obj_p in privilege_obj:
                plist.append(obj_p.privilege)

            privilege_list = UserPrivilege.objects.all()

            for pri_obj in privilege_list :
                if pri_obj.privilege in plist:
                    ss1 = "<div class='col-md-4'><div class='md-checkbox'><input type='checkbox' value='"+pri_obj.privilege+"' id='checkbox1_"+str(i)+"' class='md-check privillagesModel' checked>"
                    ss2 = "<label for='checkbox1_"+str(i)+"'> <span></span> <span class='check privillages'></span>"
                    ss3 = "<span class='box'></span>"+pri_obj.privilege+" </label>  </div> </div>"
                    ss = ss1 + ss2 + ss3
                else:
                    ss1 = "<div class='col-md-4'><div class='md-checkbox'><input type='checkbox' value='"+pri_obj.privilege+"' id='checkbox1_"+str(i)+"' class='md-check privillagesModel'>"
                    ss2 = "<label for='checkbox1_"+str(i)+"'> <span></span> <span class='check privillages'></span>"
                    ss3 = "<span class='box'></span>"+pri_obj.privilege+" </label>  </div> </div>"
                    ss = ss1 + ss2 + ss3
                i = i + 1
                final_list.append(ss)

            user_data = {
                         'role' : role_obj.role, 'role_description' : role_obj.description,
                         'final_list':final_list,'role_id':role_obj.id,'status':role_obj.status
                        }
            data = {'success' : 'true', 'user_data' : user_data}
        except Exception as e:
            print 'Exception|views.py|get_role_details', e
            data = {'success':'false', 'message':'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|views.py|get_role_details', e
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
# @role_required(privileges=['Administrator'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_user_role(request):
    privilege_list = UserPrivilege.objects.filter(is_deleted=False)
    data = {'privilege_list': privilege_list}
    return render(request, 'backoffice/administrator/add_user_role.html',data)


@csrf_exempt
def save_user_role_details(request):
    try:
        print 'views.py|save_new_role',request.POST
        privilege_list = request.POST.get('privilege_list')
        privilege_list = privilege_list.split(',')
        try:
            UserRole.objects.get(role=request.POST.get('user_role_name'))
        except UserRole.DoesNotExist,e:
            new_role_obj = UserRole(
                role=request.POST.get('user_role_name'),
                description=request.POST.get('user_role_desc'),
                created_on=datetime.datetime.now()
            )
            new_role_obj.save()
            for list_obj in privilege_list:
                obj = UserPrivilege.objects.get(privilege=list_obj)
                new_role_obj.privilege.add(obj)
                new_role_obj.save()

            data = {'success':'true', 'message':'Role created successfully.'}

        except Exception, e:
            print 'Exception|views.py|save_new_role', e
            data = {
                'success': 'false',
                'message': str(e)
            }
    except Exception, e:
        print 'Exception|views.py|save_new_role', e
        data = {
            'success' : 'false',
            'message' : str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_user_role_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_user_role_id')
        user_role_obj = UserRole.objects.get(id=str(request.GET.get('status_user_role_id')))
        if user_role_obj.is_active:
            user_role_obj.is_active = False
        else:
            user_role_obj.is_active = True

        user_role_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_servicetax_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_user_role(request):
    try:
        print 'views.py|save_new_role',request.POST
        privilege_list = request.POST.get('privilege_list')
        user_role_id = request.POST.get('user_role_id')
        role_obj = UserRole.objects.get(id=user_role_id)
        privilege_list = privilege_list.split(',')

        # role_obj.role=request.POST.get('user_role_name')
        role_obj.role="test"
        role_obj.description=request.POST.get('user_role_desc')
        role_obj.save()
        role_obj.privilege.clear()
        for list_obj in privilege_list:
            obj = UserPrivilege.objects.get(privilege=list_obj)
            role_obj.privilege.add(obj)
            role_obj.save()

        data = {'success':'true', 'message':'Role updated successfully.'}
    except Exception, e:
        print 'Exception|views.py|save_new_role', e
        data = {
            'success' : 'false',
            'message' : str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['User'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_user_landing(request):
    dash_privilege_list = UserPrivilege.objects.filter(module_name='Dashboard', is_deleted=False)
    mem_privilege_list = UserPrivilege.objects.filter(module_name='Membership', is_deleted=False)
    hb_privilege_list = UserPrivilege.objects.filter(module_name='Hall Booking', is_deleted=False)
    event_privilege_list = UserPrivilege.objects.filter(module_name='Event', is_deleted=False)
    visa_privilege_list = UserPrivilege.objects.filter(module_name='Visa',is_deleted=False)
    admin_privilege_list = UserPrivilege.objects.filter(module_name='Administrator', is_deleted=False)
    publication_privilege_list = UserPrivilege.objects.filter(module_name='Publication', is_deleted=False)
    dept_list = Department.objects.all()
    desig_list = Designation.objects.all()
    role_list = UserRole.objects.filter(is_active=True)

    # if not request.user.is_authenticated():
    #     return render(request, 'login.html')
    # else:

    # privilege_list = UserPrivilege.objects.filter(is_deleted=False)
    # data = {'privilege_list': privilege_list}
    data = {'visa_privilege_list':visa_privilege_list,'dept_list': dept_list, 'desig_list': desig_list, 'role_list': role_list,
            'dash_privilege_list': dash_privilege_list, 'mem_privilege_list': mem_privilege_list,
            'hb_privilege_list': hb_privilege_list, 'event_privilege_list': event_privilege_list,
            'admin_privilege_list': admin_privilege_list, 'publication_privilege_list': publication_privilege_list}
    return render(request, 'backoffice/administrator/user_add_landing.html',data)


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['User'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_user_detail(request):
    data={}
    privilege_list = UserPrivilege.objects.filter(is_deleted=False)
    dash_privilege_list = UserPrivilege.objects.filter(module_name='Dashboard',is_deleted=False)
    mem_privilege_list = UserPrivilege.objects.filter(module_name='Membership',is_deleted=False)
    hb_privilege_list = UserPrivilege.objects.filter(module_name='Hall Booking',is_deleted=False)
    event_privilege_list = UserPrivilege.objects.filter(module_name='Event',is_deleted=False)
    visa_privilege_list = UserPrivilege.objects.filter(module_name='Visa',is_deleted=False)
    admin_privilege_list = UserPrivilege.objects.filter(module_name='Administrator',is_deleted=False)
    publication_privilege_list = UserPrivilege.objects.filter(module_name='Publication',is_deleted=False)

    data = {}

    dept_list=Department.objects.all().order_by('department_name')
    desig_list=Designation.objects.all().order_by('designation_name')
    role_list = UserRole.objects.filter(is_active=True)
    data = {'visa_privilege_list': visa_privilege_list, 'dept_list': dept_list, 'desig_list': desig_list,
            'role_list': role_list, 'privilege_list': privilege_list, 'dash_privilege_list': dash_privilege_list,
            'mem_privilege_list': mem_privilege_list, 'hb_privilege_list': hb_privilege_list,
            'event_privilege_list': event_privilege_list, 'admin_privilege_list': admin_privilege_list,
            'publication_privilege_list': publication_privilege_list}    
    return render(request, 'backoffice/administrator/add_user.html',data)


@csrf_exempt
def get_user_detail_list(request):
    try:
        print 'backofficeapp | adminstrator.py | get_user_detail_list | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'role']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        user_list = SystemUserProfile.objects.filter(is_deleted=False)  # .order_by(column_name)

        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                user_list=user_list.filter(is_active=True)
            else:
                user_list = user_list.filter(is_active=False)
        print searchTxt
        if searchTxt:
            user_list = user_list.filter((Q(username__icontains=searchTxt)| Q(name=searchTxt)))

        total_record = user_list.count()
        user_list = user_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        print user_list
        for obj in user_list:
            i = start + a
            a = a + 1
            if obj.is_active:
                user_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_user_detail" onclick=update_user_detail_status(' + '"' + str(
                    user_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                user_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_user_detail" onclick=update_user_detail_status(' + '"' + str(
                    user_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=edit_user_detail_modal("+ str(obj.id)+")></a> &nbsp; &nbsp;"

            tempList = []
            tempList.append(str(i))
            tempList.append(obj.name)
            tempList.append(obj.username)
            if obj.designation:
                tempList.append(obj.designation.designation_name)
            else:
                tempList.append('NA')
            if obj.department:
                tempList.append(obj.department.department_name)
            else:
                tempList.append('NA')
            tempList.append(obj.contact_no)
            tempList.append(obj.email)
            # tempList.append(obj.created_on.strftime('%B %d,%Y'))
            tempList.append(status)
            tempList.append(action + edit_icon)
            tempList.append('')
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | adminstrator.py | get_user_role_list | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_user_details(request):
    print request.POST
    try:
        """Start:We are Creating role run time"""
        # role_obj = UserRole.objects.get(id=int(request.POST.get('select_role')))
        """End:We are Creating role run time"""

        name = request.POST.get('user_name')
        if SystemUserProfile.objects.filter(username=request.POST.get('user_username')).exists():
            data = {'success': 'exist'}
            return HttpResponse(json.dumps(data), content_type='application/json')

        name_list=name.split(' ')
        if len(name_list) > 1:
            first_name=name_list[0]
            last_name=name_list[1]
        else:
            first_name = name_list[0]
            last_name = ''

        user_obj = SystemUserProfile(
            name=request.POST.get('user_name'),
            department_id=request.POST.get('select_dept'),
            designation_id=request.POST.get('select_desig'),
            username=request.POST.get('user_username'),
            contact_no = request.POST.get('user_contact'),
            first_name=first_name,
            last_name=last_name,
            # role=role_obj,

            # user_type="ADMIN" if request.POST.get('user_contact')== 1 else "EVENT",
            email=request.POST.get('user_email'),
            # user_email=request.POST.get('user_email'),
            )
        user_obj.save()

        user_obj.set_password(request.POST.get('user_password'))
        user_obj.save()

        """Start:Create a role for every user if role creation function in use comment this code"""
        try:
            privilege_list = request.POST.get('privilege_list')
            privilege_list = privilege_list.split(',')
            try:
                role_obj = UserRole()
                role_obj.save()
                role_obj.role = 'Role_' + str(role_obj.id)
                role_obj.save()
                for list_obj in privilege_list:
                    obj = UserPrivilege.objects.get(privilege=list_obj)
                    role_obj.privilege.add(obj)
                    role_obj.save()
            except Exception,e:
                print e
                print list_obj
                pass

            user_obj.role = role_obj
            user_obj.save()

        except Exception,e:
            print e
            pass

        """End:Create a role for every user if role creation function in use comment this code"""

        data = {'success':'true'}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|administrator.py|', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_user_detail(request):
    try:
        print 'views.py|show_user_detail'
        data = {}
        final_list = []
        try:
            plist = []
            user_detail_id=request.GET.get('user_detail_id')
            user_obj = SystemUserProfile.objects.get(id=user_detail_id)
            user_Detail={
                'name':user_obj.name,
                'department_id':user_obj.department_id,
                'designation_id':user_obj.designation_id,
                'username':user_obj.username,
                'contact_no':user_obj.contact_no,
                'email':user_obj.email,
                'password':user_obj.password,
            }

            role_obj = user_obj.role
            privilege_obj = role_obj.privilege.all()

            for obj_p in privilege_obj:
                plist.append(obj_p.id)

            data = {'success' : 'true', 'id_list':plist,'user_Detail':user_Detail}
        except Exception as e:
            print 'Exception|views.py|get_role_details', e
            data = {'success':'false', 'message':'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|views.py|get_role_details', e

    # print data
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_user_detail_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_user_detail_id')
        user_obj = SystemUserProfile.objects.get(id=str(request.GET.get('status_user_detail_id')))
        if user_obj.is_active:
            user_obj.is_active = False
        else:
            user_obj.is_active = True

        user_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_user_detail_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_user_detail(request):
    try:
        print 'views.py|save_edit_user_detail'
        privilege_list = request.POST.get('privilege_list')
        privilege_list = privilege_list.split(',')
        user_obj = SystemUserProfile.objects.get(id=str(request.POST.get('user_detail_id')))
        try:
            SystemUserProfile.objects.get(~Q(id=user_obj.id),username=request.POST.get('user_username'))
            data = {'success': 'exist', 'message': 'username exist'}
        except SystemUserProfile.DoesNotExist,e:
            name=request.POST.get('user_name')
            name_list = name.split(' ')
            if len(name_list) > 1:
                first_name = name_list[0]
                last_name = name_list[1]
            else:
                first_name = name_list[0]
                last_name = ''

            user_obj.name = request.POST.get('user_name')
            user_obj.department_id = request.POST.get('select_dept')
            user_obj.designation_id = request.POST.get('select_desig')
            user_obj.username = request.POST.get('user_username')
            user_obj.contact_no = request.POST.get('user_contact')
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = request.POST.get('user_email')
            if request.POST.get('user_password'):
                user_obj.set_password(request.POST.get('user_password'))
            role_obj = user_obj.role
            role_obj.privilege.clear()

            for list_obj in privilege_list:
                obj = UserPrivilege.objects.get(privilege=list_obj)
                role_obj.privilege.add(obj)
                role_obj.save()
            user_obj.save()
            data = {'success': 'true', 'message': 'User updated successfully.'}
        except Exception,e:
            pass
            data = {
                'success': 'false',
                'message': str(e)
            }
    except Exception, e:
        print 'Exception|administrator.py|save_edit_user_detail', e
        data = {
            'success' : 'false',
            'message' : str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')


#--------------------------------------------

# @login_required(login_url='/backofficeapp/login/')
# @role_required(privileges=['Country'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_department_landing(request):
    return render(request, 'backoffice/administrator/department_landing.html')


# @login_required(login_url='/backofficeapp/login/')
# @role_required(privileges=['Country'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_department(request):
    return render(request, 'backoffice/administrator/add_department.html')


@csrf_exempt
def save_department_details(request):
    sid = transaction.savepoint()
    try:
        department_name = request.POST.get('department_name')
        if request.method == 'POST':
            if Department.objects.filter(department_name=department_name):
                data = {'success': 'exist'}
            else:
                departmentobj = Department(
                    department_name=department_name
                )
                departmentobj.save()
                transaction.savepoint_commit(sid)

                data = {'success': 'true'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_department_list(request):
    try:
        print 'backofficeapp | event_home.py | get_delete_events | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'department_name']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        department_list = Department.objects.all()  # .order_by(column_name)
        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                department_list=department_list.filter(is_deleted=False)
            else:
                department_list = department_list.filter(is_deleted=True)
        if searchTxt:
            department_list = department_list.filter(Q(department_name__icontains=searchTxt))

        total_record = department_list.count()
        department_list = department_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in department_list:
            i = start + a
            a = a + 1
            if not(obj.is_deleted):
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_department_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_department_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=editSlabDetailsModal("+ str(obj.id)+")></a> &nbsp; &nbsp;"
            tempList = []
            tempList.append(str(i))
            # tempList.append(obj.id)
            tempList.append(obj.department_name)
            tempList.append(status)
            tempList.append(action + edit_icon)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def show_department_detail(request):
    data = {}
    department_id = request.GET.get('department_id')
    departmentobj = Department.objects.get(id=department_id)
    data = {'abc': departmentobj.department_name, 'success': 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_department_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user

        if request.POST:
            department_id = request.POST.get('department_id')
            department_name = request.POST.get('department_name')
            try:
                Department.objects.get(~Q(id=department_id),department_name=department_name)
            except Department.DoesNotExist,e:
                departmentobj = Department.objects.get(id=department_id)

                departmentobj.department_name = department_name
                departmentobj.save()
                transaction.savepoint_commit(sid)
                data = {'success': 'true'}
            except Exception,e:
                print e
                pass
                transaction.rollback(sid)
                data = {'success': 'false'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_department_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_department_id')
        departmentobj = Department.objects.get(id=str(request.GET.get('status_department_id')))
        if departmentobj.is_deleted:
            departmentobj.is_deleted = False
        else:
            departmentobj.is_deleted = True

        departmentobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# @login_required(login_url='/backofficeapp/login/')
# @role_required(privileges=['Country'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def administrator_designation_landing(request):
    return render(request, 'backoffice/administrator/designation_landing.html')


# @login_required(login_url='/backofficeapp/login/')
# @role_required(privileges=['Country'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_new_designation(request):
    return render(request, 'backoffice/administrator/add_designation.html')


@csrf_exempt
def save_designation_details(request):
    sid = transaction.savepoint()
    try:
        designation_name = request.POST.get('designation_name')
        if request.method == 'POST':
            if Designation.objects.filter(designation_name=designation_name):
                data = {'success': 'exist'}
            else:
                designationobj = Designation(
                    designation_name=designation_name
                )
                designationobj.save()
                transaction.savepoint_commit(sid)

                data = {'success': 'true'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_designation_list(request):
    try:
        print 'backofficeapp | event_home.py | get_delete_events | user'
        dataList = []
        column = request.GET.get('order[0][column]')
        print request.GET.get('order[0][column]')

        searchTxt = request.GET.get('search[value]')
        order = ""

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['id', 'designation_name']

        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        designation_list = Designation.objects.all()  # .order_by(column_name)
        if request.GET.get('sort_var'):
            if request.GET.get('sort_var') == 'Active':
                designation_list=designation_list.filter(is_deleted=False)
            else:
                designation_list = designation_list.filter(is_deleted=True)
        if searchTxt:
            designation_list = designation_list.filter(Q(designation_name__icontains=searchTxt))

        total_record = designation_list.count()
        designation_list = designation_list.order_by(column_name)[start:length]
        i = 0
        a = 1
        for obj in designation_list:
            i = start + a
            a = a + 1
            if not(obj.is_deleted):
                event_status = 'True'
                status = '<label class="label label-success"> Active </label>'
                action = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_designation_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                event_status = 'False'
                status = '<label class="label label-default"> Inactive </label>'
                action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_designation_status(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

            edit_icon = "<a class=icon-pencil onClick=editSlabDetailsModal("+ str(obj.id)+")></a> &nbsp; &nbsp;"
            tempList = []
            tempList.append(str(i))
            # tempList.append(obj.id)
            tempList.append(obj.designation_name)
            tempList.append(status)
            tempList.append(action + edit_icon)
            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_delete_events | user %s. Exception = ', str(
            traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def show_designation_detail(request):
    data = {}
    designation_id = request.GET.get('designation_id')
    designationobj = Designation.objects.get(id=designation_id)
    data = {'abc': designationobj.designation_name, 'success': 'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_designation_details(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user

        if request.POST:
            designation_id = request.POST.get('designation_id')
            designation_name = request.POST.get('designation_name')
            try:
                Designation.objects.get(~Q(id=designation_id),designation_name=designation_name)
            except Designation.DoesNotExist,e:
                designationobj = Designation.objects.get(id=designation_id)

                designationobj.designation_name = designation_name
                designationobj.save()
                transaction.savepoint_commit(sid)
                data = {'success': 'true'}
            except Exception,e:
                print e
                pass
                transaction.rollback(sid)
                data = {'success': 'false'}

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def update_designation_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print request.GET.get('status_designation_id')
        designationobj = Designation.objects.get(id=str(request.GET.get('status_designation_id')))
        if designationobj.is_deleted:
            designationobj.is_deleted = False
        else:
            designationobj.is_deleted = True

        designationobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


def payment(request):
    return render(request,'backoffice/payment.html')


@csrf_exempt
def login_check(request):
    return render(request, 'backoffice/authentication/login.html')

"""
configJson = {
                    'tarCall': false,
                    'features': {
                        'showPGResponseMsg': true,
                        'enableNewWindowFlow': true    //for hybrid applications please disable this by passing false
                    },
                    'consumerData': {
                        'deviceId': 'WEBSH2',	//possible values 'WEBSH1', 'WEBSH2' and 'WEBMD5'
                        'token': 'ca25c3ecb179f82d06059d693b6ad4ad901671ea09e1bdec318d908cead1ed1eab3ca1265e833f98614ef92691d125d9d6eb92599e900c20eb593e95afbeedc5',
                        'returnUrl': 'https://www.tekprocess.co.in/MerchantIntegrationClient/MerchantResponsePage.jsp',
                        'responseHandler': handleResponse,
                        'paymentMode': 'all',
                        'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',  //provided merchant logo will be displayed
                        'merchantId': 'T3239',
                        'currency': 'INR',
                        'consumerId': 'c964634',
                        'consumerMobileNo': '8007271912',
                        'consumerEmailId': 'shubham.pawar@bynry.com',
                        'txnId': '1',   //Unique merchant transaction ID
                        'items': [{
                            'itemId': 'test',
                            'amount': '10',
                            'comAmt': '0'
                        }],
                        'customStyle': {
                            'PRIMARY_COLOR_CODE': '#3977b7',   //merchant primary color code
                            'SECONDARY_COLOR_CODE': '#FFFFFF',   //provide merchant's suitable color code
                            'BUTTON_COLOR_CODE_1': '#1969bb',   //merchant's button background color code
                            'BUTTON_COLOR_CODE_2': '#FFFFFF'   //provide merchant's suitable color code for button text
                        }
                    }
                }
"""

import hashlib


@csrf_exempt
def get_payment_detail(request):
    print request.POST
    # token_string=str("merchantId") +'|' + str(txnId)+'|' + str("50")+ '|' + str('accountNo')+ '|' + str('consumerId') +'|' + str('consumerMobileNo')+ '|' + str('consumerEmailId')+ '|' + str('debitStartDate')+ '|' + str('debitEndDate') + '|' + str('maxAmount') + '|' + str('amountType') + '|' + str('frequency') + '|' + str('cardNumber')+ '|' + str('expMonth') + '|' + str('expYear')+ '|' +  str('cvvCode') + '|' + 'SALT'
    try:

        m = hashlib.sha512()
        # m = hashlib.md5()
        # m.update('T172654')

        token_string = str("T172654") +'|' + str(1234567)+'|' + str("100")+ '|' + str('1111111111')+ '|' + str('123123') +'|' + str('8007271912')+ '|' + str('shubhampawar006@gmail.com')+ '|' + str('21-08-2018')+ '|' + str('21-08-2018') + '|' + str('100') + '|' + str(' ') + '|' + str(' ') + '|' + str('4111111111111111')+ '|' + str('09') + '|' + str('2023')+ '|' +  str('123') + '|' + '2093514954UVQFBK'
        print token_string
        m.update(token_string)
        print m.hexdigest()
        print m
    except Exception,e:
        print e
        pass

    configJson = {
        'tarCall': False,
        'features': {
            'showPGResponseMsg': True,
            'enableNewWindowFlow': True
        },
        'consumerData':{
            'deviceId': 'WEBSH2',
            # 'deviceId': 'WEBMD5',
            # 'token': 'ca25c3ecb179f82d06059d693b6ad4ad901671ea09e1bdec318d908cead1ed1eab3ca1265e833f98614ef92691d125d9d6eb92599e900c20eb593e95afbeedc5',
            'token': m.hexdigest(),
            # 'returnUrl': 'https://www.tekprocess.co.in/MerchantIntegrationClient/MerchantResponsePage.jsp',
            # 'returnUrl': 'http://192.168.0.172:8090',
            'responseHandler':'handleResponse',
            'paymentMode': 'all',
            'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
            'merchantId': 'T172654',
            'currency': 'INR',
            'consumerId': '123123',
            'consumerMobileNo': '8007271912',
            'consumerEmailId': 'shubhampawar006@gmail.com',
            'txnId': '1234567',
            'items': [{
                'itemId': 'test',
                'amount': '100',
                'comAmt': '0'
            }],
            'customStyle': {
                         'PRIMARY_COLOR_CODE': '#3977b7',
                         'SECONDARY_COLOR_CODE': '#FFFFFF',
                         'BUTTON_COLOR_CODE_1': '#1969bb',
                         'BUTTON_COLOR_CODE_2': '#FFFFFF'
            }
        }
    }
    print configJson
    data={'configJson':configJson,'success':'true'}
    return HttpResponse(json.dumps(data), content_type='application/json')


from Paymentapp.models import PaymentTransaction


@csrf_exempt
def get_payment_detail(request):
    try:
        total_amount=100
        max_amount=100
        amount_type='F'
        frequency='ADHO'
        card_number='4111111111111111'
        exp_month='09'
        exp_year='2023'
        cvv_code='123'
        merchant_id='T172654'
        accountNo='1111111111'
        consumerId='123123'
        itemId='MCCI'
        consumerMobileNo='8007271912'
        consumer_name = 'Shubham Pawar'
        consumerEmailId='shubhampawar006@gmail.com'
        salt='2093514954UVQFBK'
        transaction_id = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        try:
            # PaymentTransaction_obj = PaymentTransaction(
            #     transaction_id=transaction_id,
            #     reg_no='1234',
            #     merchant_id=merchant_id,
            #     total_amount=total_amount,
            #     consumer_name=consumer_name,
            #     consumer_mobile_no=consumerMobileNo,
            #     consumer_email=consumerEmailId
            # )
            #
            # PaymentTransaction_obj.save()
            #
            # m = hashlib.sha512()
            #
            # msg = merchant_id + "|"  # consumerData.merchantId|
            # msg += str(transaction_id) + "|"  # consumerData.txnId|
            # msg += str(total_amount) + "|"  # totalamount|
            # msg += "" + "|"  # consumerData.accountNo|
            # msg += "" + "|"  # consumerData.consumerId|
            # msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
            # msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
            # msg += "" + "|"  # consumerData.debitStartDate|
            # msg += "" + "|"  # consumerData.debitEndDate|
            # msg += "" + "|"  # consumerData.maxAmount|
            # msg += "" + "|"  # consumerData.amountType|
            # msg += "" + "|"  # consumerData.frequency|
            # msg += "" + "|"  # consumerData.cardNumber|
            # msg += "" + "|"  # consumerData. expMonth|
            # msg += "" + "|"  # consumerData.expYear|
            # msg += "" + "|"  # consumerData.cvvCode|
            # msg += salt  # salt
            #
            # # print token_string
            # m.update(msg)
            #
            # configJson = {
            #     'tarCall': False,
            #     'features': {
            #         'showPGResponseMsg': True,
            #         'enableNewWindowFlow': True
            #     },
            #     'consumerData': {
            #         'deviceId': 'WEBSH2',
            #         'token': str(m.hexdigest()),
            #         'responseHandler': 'handleResponse',
            #         'paymentMode': 'all',
            #         'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
            #         'merchantId': merchant_id,
            #         'currency': 'INR',
            #         'consumerId': '',
            #         'consumerMobileNo': consumerMobileNo,
            #         'consumerEmailId': consumerEmailId,
            #         'txnId': str(transaction_id),
            #         'cardNumber': '',
            #         'expMonth': '',
            #         'expYear': '',
            #         'cvvCode': '',
            #         'amount_type': '',
            #         'frequency': '',
            #         'amountType': '',
            #         'debitStartDate': '',
            #         'debitEndDate': '',
            #         'maxAmount': '',
            #         'accountNo': '',
            #         'items': [{
            #             'itemId': itemId,
            #             'amount': str(total_amount),
            #             'comAmt': '0'
            #         }],
            #         'customStyle': {
            #             'PRIMARY_COLOR_CODE': '#3977b7',
            #             'SECONDARY_COLOR_CODE': '#FFFFFF',
            #             'BUTTON_COLOR_CODE_1': '#1969bb',
            #             'BUTTON_COLOR_CODE_2': '#FFFFFF'
            #         }
            #     }
            # }

            PaymentTransaction_obj=PaymentTransaction(
                reg_no = '1234',
                merchant_id = merchant_id,
                total_amount = total_amount,
                # account_number = accountNo,
                consumer_name = 'shubham pawar',
                # consumer_id = consumerId,
                consumer_mobile_no = consumerMobileNo,
                consumer_email = consumerEmailId,
                # max_amount = max_amount,
                # amount_type = amount_type,
                # frequency = frequency,
                # card_number = card_number,
                # exp_month = exp_month,
                # exp_year = exp_year,
                # cvv_code = cvv_code,
            )

            PaymentTransaction_obj.save()

            txnId = PaymentTransaction_obj.id

            debitStartDate = datetime.datetime.today().date()
            debitEndDate = datetime.datetime.today().date()

            m = hashlib.sha512()

            msg = "T172654" + "|"  # consumerData.merchantId|
            msg += "12345678901" + "|"  # consumerData.txnId|
            msg += "1" + "|"  # totalamount|
            msg += "" + "|"  # consumerData.accountNo|
            msg += "" + "|"  # consumerData.consumerId|
            msg += "9876543210" + "|"  # consumerData.consumerMobileNo|
            msg += "test@test.com" + "|"  # consumerData.consumerEmailId |
            msg += "" + "|"  # consumerData.debitStartDate|
            msg += "" + "|"  # consumerData.debitEndDate|
            msg += "" + "|"  # consumerData.maxAmount|
            msg += "" + "|"  # consumerData.amountType|
            msg += "" + "|"  # consumerData.frequency|
            msg += "" + "|"  # consumerData.cardNumber|
            msg += "" + "|"  # consumerData. expMonth|
            msg += "" + "|"  # consumerData.expYear|
            msg += "" + "|"  # consumerData.cvvCode|
            msg += "2093514954UVQFBK"

            # print token_string
            m.update(msg)
            print msg
            print m.hexdigest()

            configJson = {
                'tarCall': False,
                'features': {
                    'showPGResponseMsg': True,
                    'enableNewWindowFlow': True
                },
                'consumerData': {
                    'deviceId': 'WEBSH2',
                    # 'deviceId': 'WEBMD5',
                    'token': str(m.hexdigest()),
                    'responseHandler': 'handleResponse',
                    'paymentMode': 'all',
                    'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                    'merchantId':'T172654',
                    'currency': 'INR',
                    'consumerId': '',
                    'consumerMobileNo':'9876543210',
                    'consumerEmailId':'test@test.com',
                    'txnId': '12345678901',
                    'cardNumber': '',
                    'expMonth': '',
                    'expYear': '',
                    'cvvCode': '',
                    'amount_type': '',
                    'frequency':'',
                    'amountType': '',
                    'debitStartDate': '',
                    'debitEndDate': '',
                    'maxAmount': '',
                    'accountNo': '',
                    'items': [{
                        'itemId': 'MCCI',
                        'amount': '1',
                        'comAmt': '0'
                    }],
                    'customStyle': {
                        'PRIMARY_COLOR_CODE': '#3977b7',
                        'SECONDARY_COLOR_CODE': '#FFFFFF',
                        'BUTTON_COLOR_CODE_1': '#1969bb',
                        'BUTTON_COLOR_CODE_2': '#FFFFFF'
                    }
                }
            }

            print configJson
            consumerdata = {'total_amount': total_amount,
                            'max_amount': max_amount,
                            'amount_type': amount_type,
                            'frequency': frequency,
                            'card_number': card_number,
                            'exp_month': exp_month,
                            'exp_year': exp_year,
                            'cvv_code': cvv_code,
                            'merchant_id': merchant_id,
                            'accountNo': accountNo,
                            'consumerId': consumerId,
                            'consumerMobileNo': consumerMobileNo,
                            'consumerEmailId': consumerEmailId,
                            'salt': salt,
                            # 'token_string': token_string,
                            'txnId': 'AA12345',
                            }

            data = {'consumerdata':consumerdata,'configJson': configJson, 'success': 'true'}
        except Exception,e:
            print e
            pass
            data = {'success': 'false'}
    except Exception, e:
        print e
        pass
        data = {'success': 'false'}

    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_payment_detail_response(request):
    print request.POST
    print request.POST.get('User')