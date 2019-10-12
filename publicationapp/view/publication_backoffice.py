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
from datetime import datetime
import datetime
from authenticationapp.decorator import role_required

from django.contrib.auth.decorators import login_required

from publicationapp.models import PublicationFile


def publications_backoffice_landing_page(request):
    return render(request, 'backoffice/publication/publications_backoffice_landing.html')

def upload_publication(request):
    return render(request, 'backoffice/publication/publication_landing.html')

def add_new_publication(request):
    return render(request, 'backoffice/publication/add_new_publication.html')

@csrf_exempt
def save_new_publication(request):
    # pdb.set_trace()
    print request.POST
    sid = transaction.savepoint()
    try:
        select_magazine = request.POST.get('select_magazine')
        publish_date = request.POST.get('publish_date')
        publish_date_new = datetime.datetime.strptime(publish_date,"%d/%m/%Y")
        if request.method == 'POST':
            if select_magazine == '0':
                publication_file_obj = PublicationFile(
                    publication_type = request.POST.get('select_magazine'),
                    publish_date=publish_date_new
                )
                publication_file_obj.save()

                if request.FILES:
                    publication_file_obj.file_path = request.FILES['publication_file']
                publication_file_obj.save()

                if request.FILES:
                    publication_file_obj.cover_path = request.FILES['publication_image']
                publication_file_obj.save()

                data = {'success': 'true'}
                transaction.savepoint_commit(sid)

            elif select_magazine == '1':
                publication_file_obj = PublicationFile(
                    publication_type=request.POST.get('select_magazine'),
                    publish_date=publish_date_new
                )
                publication_file_obj.save()

                if request.FILES:
                    publication_file_obj.file_path = request.FILES['publication_file']
                publication_file_obj.save()

                if request.FILES:
                    publication_file_obj.cover_path = request.FILES['publication_image']
                publication_file_obj.save()

                data = {'success': 'true'}
                transaction.savepoint_commit(sid)

            else:
                publication_file_obj = PublicationFile(
                    publication_type=request.POST.get('select_magazine'),
                    volume_no = request.POST.get('volume_number'),
                    issue_no = request.POST.get('issue_number'),
                    publish_date=publish_date_new
                )
                publication_file_obj.save()


                if request.FILES:
                    publication_file_obj.file_path = request.FILES['publication_file']
                publication_file_obj.save()


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
        print 'Exception | user | Publication_backoffice | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


# TODO Data Table for load data in data table
@csrf_exempt
def get_publication_datatable(request):
    try:
        print 'Publicationapp | publication_backoffice.py | get_publication_datatable | user'
        dataList = []

        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['', '', '']
        column_name = order + list[int(column)]
        start = request.GET.get('start')
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        publication_obj_list = PublicationFile.objects.all()  # .order_by(column_name)
        if request.GET.get('select_status') == 'Active':
            publication_obj_list = publication_obj_list.filter(is_deleted=False)
        elif request.GET.get('select_status') == 'Inactive':
            publication_obj_list = publication_obj_list.filter(is_deleted=True)

        total_record = publication_obj_list.count()
        # banner_objs_list = banner_objs_list.filter().order_by(column_name)[start:length]

        i = 0
        for publication_obj in publication_obj_list:
            i = i + 1
            tempList = []

            # action1 = '<a class="fa fa-pencil-square-o" title="Edit" href="/mediaapp/edit-banner/?banner_id=' + str(
            #     obj.id) + '"></a>&nbsp;&nbsp;'

            if publication_obj.is_deleted:
                publication_status = 'Inactive'
                status1 = '<label class="label label-default"> Inactive </label>'
                action2 = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_publication" onclick=update_publication(' + '"' + str(
                    publication_status) + '"' + ',' + str(publication_obj.id) + ')></a>&nbsp; &nbsp;'
            else:
                publication_status = 'Active'
                status1 = '<label class="label label-success"> Active </label>'
                action2 = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_publication" onclick=update_publication(' + '"' + str(
                    publication_status) + '"' + ',' + str(publication_obj.id) + ')></a>&nbsp; &nbsp;'

            tempList.append(i)
            tempList.append(str(publication_obj.get_publication_type_display()))
            tempList.append(str(publication_obj.publish_date.strftime('%d %B %Y')))
            tempList.append(str(status1))
            tempList.append(action2)

            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception Publicationapp | Publication_backoffice.py | get_publication_datatable | user %s. Exception = ', str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def update_publication_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print 'Publicationapp | publication_backoffice.py | update_publication_status | user'

        publicationObj = PublicationFile.objects.get(id=str(request.GET.get('publication_id')))
        if publicationObj.is_deleted == False:
            publicationObj.is_deleted = True
        else:
            publicationObj.is_deleted = False
        publicationObj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_publication_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')