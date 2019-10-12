
import traceback
import StringIO
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.template.loader import get_template
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
from eventsapp.models import EventType

# -------------New MCCIA---------------


@csrf_exempt
def add_event_type(request):
    return render(request, 'backoffice/events/add_event_type.html')


@csrf_exempt
def get_event_type_datatable(request):
	try:
		print 'backofficeapp | event_type.py | get_event_type_datatable | user'
		dataList = []

		total_record=0
		column = request.GET.get('order[0][column]')
		searchTxt = request.GET.get('search[value]')
		order = ""
		if request.GET.get('order[0][dir]') == 'desc':
			order = "-"
		list = ['','event_type','']
		column_name = order + list[int(column)]
		start = request.GET.get('start')

		length = int(request.GET.get('length')) + int(request.GET.get('start'))

		event_type_list = EventType.objects.all()

		if request.GET.get('select_type') == 'True':
			event_type_list = event_type_list.filter(is_deleted=False)

		if request.GET.get('select_type') == 'False':
			event_type_list = event_type_list.filter(is_deleted=True)
								
		if request.GET.get('search_type_text'):
			event_type_list = event_type_list.filter(Q(event_type__icontains=request.GET.get('search_type_text')))

		total_record=event_type_list.count()
		event_type_list = event_type_list.filter().order_by(column_name)[start:length]	

		i = 0
		a =1
		for obj in event_type_list: 			
			tempList = []   

			action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/backofficeapp/edit-event-type-form/?type='+str(obj.id)+'"></a>&nbsp;&nbsp;'

			if obj.is_deleted:
				event_type_status = 'Inactive'
				status = '<label class="label label-default"> Inactive </label>'
				action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_type" onclick=update_event_type(' + '"' + str(
                    event_type_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
			else:
				event_type_status = 'Active'
				status = '<label class="label label-success"> Active </label>'
				action2= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_type" onclick=update_event_type(' + '"' + str(
                    event_type_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
			
			i = int(start) + a
			a = a + 1

			tempList.append(str(i))
			tempList.append(obj.event_type)
			tempList.append(status)
			tempList.append(action1 + action2)
			dataList.append(tempList)		
		
		data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
	except Exception as e:
		print 'Exception backofficeapp | event_type.py | get_event_type_datatable | user %s. Exception = ', str(traceback.print_exc())
		data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': []}
	return HttpResponse(json.dumps(data), content_type='application/json') 

@transaction.atomic
def update_event_type_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        typeobj = EventType.objects.get(id=str(request.GET.get('type_id')))
        if typeobj.is_deleted == False:
            typeobj.is_deleted = True
        else:
            typeobj.is_deleted = False

        typeobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_event_type_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')		

@csrf_exempt
def add_event_type_form(request):
    return render(request, 'backoffice/events/add_event_type_form.html')      


@transaction.atomic
@csrf_exempt
def save_new_event_type(request):
	sid = transaction.savepoint()
	try:
		print 'Request In|backofficeapp |event_type.py |save_new_event_type|User %s Data'
		event_obj = EventType(
		event_type = request.POST.get('event_type'),
		)
		event_obj.save() 
    
		transaction.savepoint_commit(sid)
		print 'Response Out|backofficeapp |event_type.py |save_new_event_type|User %s Data'
		data = {'success': 'true'}
	except Exception, exc:
		print 'exception ', str(traceback.print_exc())
		print "Exception In |  backofficeapp |event_type.py |save_new_event_type", exc
		data = {'success': 'false', 'error': 'Exception ' + str(exc)}
		transaction.rollback(sid)
	return HttpResponse(json.dumps(data), content_type='application/json')      


@csrf_exempt
def edit_event_type_form(request):
    try:
        type_obj = EventType.objects.get(id=request.GET.get('type'))
        data = {
            'success':'true',   
            'type_id': type_obj.id,
            'event_type':type_obj.event_type,        
        }
    except Exception as e:
        print 'Exception | event_type.py | edit_event_type_form | user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}        
    
    return render(request, 'backoffice/events/edit_event_type_form.html',data) 	


@transaction.atomic
@csrf_exempt
def update_event_type_form(request):
    data = {}
    sid = transaction.savepoint()
    try:
        type_obj = EventType.objects.get(id=str(request.POST.get('type_id')))
        type_obj.event_type = request.POST.get('event_type')
        type_obj.save()

        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_event_type_form = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')	     