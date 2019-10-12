
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
from adminapp.models import Committee, TaskForce
from backofficeapp.models import SystemUserProfile


# -------------New MCCIA---------------


@csrf_exempt
def add_committee(request):
    return render(request, 'backoffice/events/add_committee.html')

@csrf_exempt
def get_committee_datatable(request):
	try:
		print 'backofficeapp | event_home.py | get_committee_datatable | user'
		dataList = []

		total_record=0
		column = request.GET.get('order[0][column]')
		searchTxt = request.GET.get('search[value]')
		order = ""
		if request.GET.get('order[0][dir]') == 'desc':
			order = "-"
		list = ['','committee','']
		column_name = order + list[int(column)]
		start = request.GET.get('start')

		length = int(request.GET.get('length')) + int(request.GET.get('start'))

		committee_list = Committee.objects.all()

		if request.GET.get('select_committee') == 'True':
			committee_list = committee_list.filter(is_deleted=False)

		if request.GET.get('select_committee') == 'False':
			committee_list = committee_list.filter(is_deleted=True)
								
		if request.GET.get('search_committee_text'):
			committee_list = committee_list.filter(Q(committee__icontains=request.GET.get('search_committee_text')))

		total_record=committee_list.count()
		committee_list = committee_list.filter().order_by(column_name)[start:length]	

		i = 0
		a =1
		for obj in committee_list: 			
			tempList = []   

			action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/backofficeapp/edit-committee-form/?committee='+str(obj.id)+'"></a>&nbsp;&nbsp;'

			if obj.is_deleted:
				event_status = 'Inactive'
				status = '<label class="label label-default"> Inactive </label>'
				action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_committtee" onclick=update_committee(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
			else:
				event_status = 'Active'
				status = '<label class="label label-success"> Active </label>'
				action2= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_committtee" onclick=update_committee(' + '"' + str(
                    event_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
			
			i = int(start) + a
			a = a + 1

			tempList.append(str(i))
			tempList.append(obj.committee)
			tempList.append(obj.contact_person1.name)
			contact_person2 = '-'
			if obj.contact_person2:
				contact_person2 = obj.contact_person2.name 
			tempList.append(contact_person2)
			tempList.append(status)
			tempList.append(action1 + action2)
			dataList.append(tempList)		
		
		data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
	except Exception as e:
		print 'Exception backofficeapp | event_home.py | get_committee_datatable | user %s. Exception = ', str(traceback.print_exc())
		data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': []}
	return HttpResponse(json.dumps(data), content_type='application/json') 


@transaction.atomic
def update_committee_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        commiobj = Committee.objects.get(id=str(request.GET.get('committee_id')))
        if commiobj.is_deleted == False:
            commiobj.is_deleted = True
        else:
            commiobj.is_deleted = False

        commiobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_committee_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')	


@csrf_exempt
def add_committee_form(request):
    try:
        taskforce_list = TaskForce.objects.filter(is_deleted=False)
        contact_person_list = SystemUserProfile.objects.filter(user_status='ACTIVE',is_deleted=False)

        data = {
            'taskforce_list':taskforce_list,        
            'contact_person_list':contact_person_list,
        }
    except Exception as e:
        print 'Exception | event_committee.py| add_committee_form | user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}        
      
    return render(request, 'backoffice/events/add_committee_form.html',data)    

@transaction.atomic
@csrf_exempt
def save_new_committee(request):
	sid = transaction.savepoint()
	try:
		print 'Request In|backofficeapp |event_committee.py |save_new_committee|User %s Data'
		committee_obj = Committee(
			committee = request.POST.get('committee_name'),
			task_force = TaskForce.objects.get(id = request.POST.get('task_force')) if request.POST.get('task_force') else None,

			chairman1_name = request.POST.get('chairman1_name'),
			chairman1_company = request.POST.get('chairman1_company'),
            chairman1_designation = request.POST.get('chairman1_designation'),
            chairman1_email = request.POST.get('chairman1_email'),
            chairman1_mobile = request.POST.get('chairman1_mobile'),
            chairman1_telephone = request.POST.get('chairman1_telephone'),
            chairman1_address = request.POST.get('chairman1_address'),

            chairman2_name = request.POST.get('chairman2_name'),
            chairman2_company = request.POST.get('chairman2_company'),
            chairman2_designation = request.POST.get('chairman2_designation'),
            chairman2_email = request.POST.get('chairman2_email'),
            chairman2_mobile = request.POST.get('chairman2_mobile'),
            chairman2_telephone = request.POST.get('chairman2_telephone'),
            chairman2_address = request.POST.get('chairman2_address'),
            contact_person1 = SystemUserProfile.objects.get(id = request.POST.get('office_incharge1')) if request.POST.get('office_incharge1') else None,
            contact_person2 = SystemUserProfile.objects.get(id = request.POST.get('office_incharge2')) if request.POST.get('office_incharge2') else None,
		)
		committee_obj.save() 

		transaction.savepoint_commit(sid)
		print 'Response Out|backofficeapp |event_committee.py |save_new_committee|User %s Data'
		data = {'success': 'true'}
	except Exception, exc:
		print 'exception ', str(traceback.print_exc())
		print "Exception In |  backofficeapp |event_committee.py |save_new_committee", exc
		data = {'success': 'false', 'error': 'Exception ' + str(exc)}
		transaction.rollback(sid)
	return HttpResponse(json.dumps(data), content_type='application/json')  

@csrf_exempt
def edit_committee_form(request):
    try:
		committee_obj = Committee.objects.get(id=request.GET.get('committee'))

		taskforce_list = TaskForce.objects.filter(is_deleted=False)
		contact_person_list = SystemUserProfile.objects.filter(user_status='ACTIVE',is_deleted=False)

		contact_person2_id = committee_obj.contact_person2.id if committee_obj.contact_person2 else None
		data = {
			'success':'true',   
			'taskforce_list':taskforce_list,        
			'contact_person_list':contact_person_list,
			'committee_id': committee_obj.id,
			'committee_name':committee_obj.committee,
			'chairman1_name': committee_obj.chairman1_name,
			'chairman1_company' : committee_obj.chairman1_company,
			'chairman1_designation' : committee_obj.chairman1_designation,
			'chairman1_email' : committee_obj.chairman1_email,
			'chairman1_mobile' : committee_obj.chairman1_mobile,
			'chairman1_telephone': committee_obj.chairman1_telephone,
			'chairman1_address' : committee_obj.chairman1_address,
			'chairman2_name' : committee_obj.chairman2_name,
			'chairman2_company' : committee_obj.chairman2_company,
			'chairman2_designation' : committee_obj.chairman2_designation,
			'chairman2_email' : committee_obj.chairman2_email,
			'chairman2_mobile': committee_obj.chairman2_mobile,
			'chairman2_telephone' : committee_obj.chairman2_telephone,
			'chairman2_address' : committee_obj.chairman2_address,
			'contact_person1_id' : committee_obj.contact_person1.id,
			'contact_person2_id' :  contact_person2_id

		}
    except Exception as e:
        print 'Exception | event_committee.py| edit_committee_form | user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}        
    
    return render(request, 'backoffice/events/edit_committee_form.html',data)    


@transaction.atomic
@csrf_exempt
def update_committee_form(request):
    data = {}
    sid = transaction.savepoint()
    try:
		committee_obj = Committee.objects.get(id=str(request.POST.get('committee_id')))
		committee_obj.committee = request.POST.get('committee_name')
		committee_obj.task_force = TaskForce.objects.get(id = request.POST.get('task_force')) if request.POST.get('task_force') else None
		committee_obj.chairman1_name = request.POST.get('chairman1_name')
		committee_obj.chairman1_company = request.POST.get('chairman1_company')
		committee_obj.chairman1_designation = request.POST.get('chairman1_designation')
		committee_obj.chairman1_email = request.POST.get('chairman1_email')
		committee_obj.chairman1_mobile = request.POST.get('chairman1_mobile')
		committee_obj.chairman1_telephone = request.POST.get('chairman1_telephone')
		committee_obj.chairman1_address = request.POST.get('chairman1_address')
		committee_obj.chairman2_name = request.POST.get('chairman2_name')
		committee_obj.chairman2_company = request.POST.get('chairman2_company')
		committee_obj.chairman2_designation = request.POST.get('chairman2_designation')
		committee_obj.chairman2_email = request.POST.get('chairman2_email')
		committee_obj.chairman2_mobile = request.POST.get('chairman2_mobile')
		committee_obj.chairman2_telephone = request.POST.get('chairman2_telephone')
		committee_obj.chairman2_address = request.POST.get('chairman2_address')
		committee_obj.contact_person1 = SystemUserProfile.objects.get(id = request.POST.get('office_incharge1')) if request.POST.get('office_incharge1') else None
		committee_obj.contact_person2 = SystemUserProfile.objects.get(id = request.POST.get('office_incharge2')) if request.POST.get('office_incharge2') else None

		committee_obj.save()

		transaction.savepoint_commit(sid)
		data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_committee_form = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')	    