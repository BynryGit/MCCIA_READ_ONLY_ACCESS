
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
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import dateutil.relativedelta
from django.db.models import Count
from PIL import *
import calendar
import urllib2
import random
import traceback

from backofficeapp.models import SystemUserProfile
from mediaapp.models import MCCIABanner, MCCIALinkToShare
from datetime import datetime 
from dateutil import tz 
from django.contrib.sites.shortcuts import get_current_site


@csrf_exempt
def banner_landing(request):
    return render(request, 'backoffice/media/banner_landing.html')  

@csrf_exempt
def add_new_banner(request):
    try:
    	print 'Request In|mediaapp |media.py |add_new_banner |User %s Data'
        data = {
            'success':'true',
        }
    except Exception as e:
        print 'Exception | mediaapp |media.py |add_new_banner| user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}

    return render(request, 'backoffice/media/add_new_banner.html',data)      



@csrf_exempt
def save_new_banner(request):
	try:
		print 'Request In|mediaapp |media.py |save_new_banner |User %s Data'

		from_zone = tz.tzutc()
		to_zone = tz.gettz('Asia/Kolkata')

		if request.POST.get('expire_date'):
			utc_expire_date = dateutil.parser.parse(str(request.POST.get('expire_date')))
			utc_expire_date = utc_expire_date.replace(tzinfo=from_zone)
			final_utc_expire_date = utc_expire_date.astimezone(to_zone) 

		banner_link = '#'
		if request.POST.get('banner_link'):
			banner_link = request.POST.get('banner_link')

		bannerObj = MCCIABanner()
		bannerObj.save()
		bannerObj.document_files = request.FILES['event_banner_file']
		im = Image.open(bannerObj.document_files)
		width , height=im.size
		if width<1500 and height<440:
			return False
		else:
			im1 = im.resize((1500,440),Image.ANTIALIAS)
			im1.save(bannerObj.document_files,quality=95)
		bannerObj.expire_date = final_utc_expire_date if request.POST.get('expire_date') else None
		bannerObj.creation_date = datetime.now()
		bannerObj.banner_link = banner_link
		bannerObj.save()
		data = {'success': 'true'}

		print 'Response Out|mediaapp |media.py |save_new_banner|User %s Data'
	except Exception, exc:
		print 'exception ', str(traceback.print_exc())
		print "Exception In |  mediaapp |media.py |save_new_banner", exc
		data = {'success': 'false', 'error': 'Exception ' + str(exc)}
	return HttpResponse(json.dumps(data), content_type='application/json')     


@csrf_exempt
def get_banner_datatable(request): 
	try:
		print 'mediaapp |media.py | get_banner_datatable | user'
		dataList = []

		total_record=0
		column = request.GET.get('order[0][column]')
		searchTxt = request.GET.get('search[value]')
		order = ""
		if request.GET.get('order[0][dir]') == 'desc':
			order = "-"
		list = ['','','']
		column_name = order + list[int(column)]
		start = request.GET.get('start')
		length = int(request.GET.get('length')) + int(request.GET.get('start'))

		banner_objs_list = MCCIABanner.objects.all()#.order_by(column_name)
		if request.GET.get('select_status') == 'Active':			
			banner_objs_list = banner_objs_list.filter(is_deleted=False)
		elif request.GET.get('select_status') == 'Inactive':			
			banner_objs_list = banner_objs_list.filter(is_deleted=True)

		total_record=banner_objs_list.count()
		# banner_objs_list = banner_objs_list.filter().order_by(column_name)[start:length]


		i = 0
		for obj in banner_objs_list: 
			# For reflecting release date impact on visibility of event
			expire_date = '-'
			if obj.expire_date:
				expire_date1 = obj.expire_date.strftime('%d %B %Y - %H:%M')
				expire_date = datetime.strptime(expire_date1, '%d %B %Y - %H:%M')

				today_date = datetime.today().strftime('%d %B %Y - %H:%M')
				today_date = datetime.strptime(today_date, '%d %B %Y - %H:%M')

				creation_date = obj.creation_date.strftime('%d %B %Y - %H:%M')
				creation_date = datetime.strptime(creation_date, '%d %B %Y - %H:%M')
			
			obj.is_expired = False
			obj.save()

			if expire_date <= today_date:
				obj.is_expired = True
				obj.save()


			i = i + 1 
			tempList = []   

			action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/mediaapp/edit-banner/?banner_id='+str(obj.id)+'"></a>&nbsp;&nbsp;'

			if obj.is_deleted:
				banner_status = 'Inactive'
				status1 = '<label class="label label-default"> Inactive </label>'
				action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_banner" onclick=update_banner(' + '"' + str(
				banner_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
			else:
				banner_status = 'Active'
				status1 = '<label class="label label-success"> Active </label>'
				action2= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_banner" onclick=update_banner(' + '"' + str(
				banner_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

			if obj.is_expired:
				status2 = '<label class="label label-default"> Expired </label>'
			else:
				status2 = '<label class="label label-success"> Not Expired </label>'

			tempList.append(i)
			tempList.append(str(obj.creation_date.strftime('%d %B %Y')))
			tempList.append(str(expire_date1))
			tempList.append(status2)
			tempList.append(status1)
			tempList.append(action1 + action2)

			dataList.append(tempList)
		data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
	except Exception as e:
		print 'Exception mediaapp |media.py | get_banner_datatable | user %s. Exception = ', str(traceback.print_exc())
		data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': []}
	return HttpResponse(json.dumps(data), content_type='application/json')  


@transaction.atomic
def update_banner_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        bannerObj = MCCIABanner.objects.get(id=str(request.GET.get('banner_id')))
        if bannerObj.is_deleted == False:
            bannerObj.is_deleted = True
        else:
            bannerObj.is_deleted = False
        bannerObj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_banner_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')	


@csrf_exempt
def edit_banner(request):
    try:
    	print 'Request In|mediaapp |media.py |edit_banner |User %s Data'

    	bannerObj = MCCIABanner.objects.get(id=request.GET.get('banner_id'))

        banner_address = "https://" + get_current_site(request).domain + bannerObj.document_files.url
        data = {
            'success':'true',
            'banner_id':bannerObj.id,
            'expire_date':bannerObj.expire_date.strftime('%d %B %Y - %H:%M'),
            'banner_address':banner_address,
            'banner_link':bannerObj.banner_link
        }
    except Exception as e:
        print 'Exception | mediaapp |media.py |edit_banner| user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}

    return render(request, 'backoffice/media/edit_banner.html',data)    


@csrf_exempt
def update_banner(request): 
    try:
		print 'Request In|mediaapp |media.py |update_banner|User %s Data'
		from_zone = tz.tzutc()
		to_zone = tz.gettz('Asia/Kolkata')

		if request.POST.get('expire_date'):
			utc_expire_date = dateutil.parser.parse(str(request.POST.get('expire_date')))
			utc_expire_date = utc_expire_date.replace(tzinfo=from_zone)
			final_utc_expire_date = utc_expire_date.astimezone(to_zone) 

		bannerObj = MCCIABanner.objects.get(id=request.POST.get('banner_id'))

		if int(request.POST.get('hidden_banner_val')):
			bannerObj.document_files = request.FILES['event_banner_file']
		bannerObj.expire_date = final_utc_expire_date if request.POST.get('expire_date') else None
		bannerObj.banner_link = request.POST.get('banner_link')
		bannerObj.save()


		print 'Response Out|mediaapp |media.py |update_banner|User %s Data'
		data = {'success': 'true'}
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        print "Exception In |  backofficeapp |event_home.py |update_event", exc
        data = {'success': 'false', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json') 


@csrf_exempt
def link_to_download(request):
    return render(request, 'backoffice/media/link_landing.html')  


@csrf_exempt
def get_link_datatable(request): 
	try:
		print 'mediaapp |media.py | get_link_datatable | user'
		dataList = []

		total_record=0
		column = request.GET.get('order[0][column]')
		searchTxt = request.GET.get('search[value]')
		order = ""
		if request.GET.get('order[0][dir]') == 'desc':
			order = "-"
		list = ['','','']
		column_name = order + list[int(column)]
		start = request.GET.get('start')
		length = int(request.GET.get('length')) + int(request.GET.get('start'))

		link_objs_list = MCCIALinkToShare.objects.all()#.order_by(column_name)
		if request.GET.get('select_status') == 'Active':			
			link_objs_list = link_objs_list.filter(is_deleted=False)
		elif request.GET.get('select_status') == 'Inactive':			
			link_objs_list = link_objs_list.filter(is_deleted=True)

		total_record=link_objs_list.count()
		# link_objs_list = link_objs_list.filter().order_by(column_name)[start:length]


		i = 0
		for obj in link_objs_list: 

			i = i + 1 
			tempList = []   

			action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/mediaapp/edit-link/?link_id='+str(obj.id)+'"></a>&nbsp;&nbsp;'

			if obj.is_deleted:
				link_status = 'Inactive'
				status = '<label class="label label-default"> Inactive </label>'
				action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_link" onclick=update_link(' + '"' + str(
				link_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'
			else:
				link_status = 'Active'
				status = '<label class="label label-success"> Active </label>'
				action2= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_link" onclick=update_link(' + '"' + str(
				link_status) + '"' + ',' + str(obj.id) + ')></a>&nbsp; &nbsp;'

			link_to_share = '<a onclick=copy_function(' + '"' + str(
				obj.link_to_share) + '"' +  ')>'+ obj.link_to_share +' </a>&nbsp;&nbsp;'


	
			tempList.append(i)
			tempList.append(str(obj.creation_date.strftime('%d %B %Y')))
			tempList.append(link_to_share)
			tempList.append(status)
			tempList.append(action1 + action2)

			dataList.append(tempList)
		data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
	except Exception as e:
		print 'Exception mediaapp |media.py | get_link_datatable | user %s. Exception = ', str(traceback.print_exc())
		data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': []}
	return HttpResponse(json.dumps(data), content_type='application/json')  


@csrf_exempt
def create_link(request):
    return render(request, 'backoffice/media/create_link.html')  


@csrf_exempt
def save_new_link(request):
	try:
		print 'Request In|mediaapp |media.py |save_new_link |User %s Data'

		linkObj = MCCIALinkToShare()
		linkObj.save()
		linkObj.document_files = request.FILES['link_file']
		linkObj.creation_date = datetime.now()
		linkObj.save()

		link_to_share = 'https://' + get_current_site(request).domain + linkObj.document_files.url
		linkObj.link_to_share = link_to_share
		linkObj.save()		

		data = {'success': 'true'}

		print 'Response Out|mediaapp |media.py |save_new_link|User %s Data'
	except Exception, exc:
		print 'exception ', str(traceback.print_exc())
		print "Exception In |  mediaapp |media.py |save_new_link", exc
		data = {'success': 'false', 'error': 'Exception ' + str(exc)}
	return HttpResponse(json.dumps(data), content_type='application/json')      


@transaction.atomic
def update_link_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        linkObj = MCCIALinkToShare.objects.get(id=str(request.GET.get('link_id')))
        if linkObj.is_deleted == False:
            linkObj.is_deleted = True
        else:
            linkObj.is_deleted = False
        linkObj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_link_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')	


@csrf_exempt
def edit_link(request):
    try:
    	print 'Request In|mediaapp |media.py |edit_link |User %s Data'

    	linkObj = MCCIALinkToShare.objects.get(id=request.GET.get('link_id'))

        link_address = "https://" + get_current_site(request).domain + linkObj.document_files.url
        data = {
            'success':'true',
            'link_id':linkObj.id,
            'link_address':link_address
        }
    except Exception as e:
        print 'Exception | mediaapp |media.py |edit_link| user %s. Exception = ', str(traceback.print_exc())
        data = {'success':'false'}

    return render(request, 'backoffice/media/edit_link.html',data)    



@csrf_exempt
def update_link(request): 
    try:
		print 'Request In|mediaapp |media.py |update_link|User %s Data'

		linkObj = MCCIALinkToShare.objects.get(id=request.POST.get('link_id'))

		if int(request.POST.get('hidden_link')):
			linkObj.document_files = request.FILES['link_file']
			linkObj.save()	

		link_to_share = 'https://' + get_current_site(request).domain + linkObj.document_files.url
		linkObj.link_to_share = link_to_share
		linkObj.save()	


		print 'Response Out|mediaapp |media.py |update_link|User %s Data'
		data = {'success': 'true'}
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        print "Exception In |  backofficeapp |event_home.py |update_event", exc
        data = {'success': 'false', 'error': 'Exception ' + str(exc)}
    return HttpResponse(json.dumps(data), content_type='application/json')