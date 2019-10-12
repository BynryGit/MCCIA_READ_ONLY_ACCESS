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

from eventsapp.models import EventDetails



import datetime
# Depending on release date event list will update status : "view_status" 
def update_event_view_status():
	try:
		print 'cronjob | update_event_view_status'
		event_obj_list = EventDetails.objects.filter(event_status=0)
		print '..event_obj_list..',event_obj_list
		today = datetime.datetime.today().strftime('%Y-%m-%d') #from_date__gte=today
		for obj in event_obj_list:
			release_date = obj.release_date.strftime('%Y-%m-%d')
			if release_date == today:
				obj.view_status = 1
				obj.save()

			to_date = obj.to_date.strftime('%Y-%m-%d')
			if to_date < today:
				obj.view_status = 0
				obj.event_status = 1
				obj.save()
		
		#pass    
	except Exception as e:
		print 'Exception | cronjob | update_event_view_status',e