from decimal import Decimal
from django.shortcuts import render
from dateutil import tz
import os
from django.template import Context
from django.template.loader import render_to_string, get_template
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from MCCIA import settings

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
from django.db import transaction
import pdb
import csv
import json
# importing exceptions
from django.db import IntegrityError
from captcha_form import CaptchaForm
import operator
from datetime import date, timedelta
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import dateutil.relativedelta
from django.db.models import Count, Sum, Q, F
from datetime import date
import calendar
import urllib2
import random
import traceback

from adminapp.models import Committee
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallBooking,HallBookingDetail,HallLocation,HallDetail, HallCheckAvailability, HallPaymentDetail, HallEquipment,BookingDetailHistory, Holiday, HallBookingDepositDetail, UserTrackDetail
from hallbookingapp.view.hall_booking_confirm import send_booking_invoice_mail, send_booking_invoice_mail_locationvise
from adminapp.models import Servicetax
import datetime
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


def cheque_bounce(request):
    hall_location_list=HallLocation.objects.filter(is_deleted=False)
    data={'hall_location_list':hall_location_list}
    return render(request, 'backoffice/hall_booking/cheque_bounce.html',data)


def cheque_details(request,booking_id):
    data = {'booking_id':booking_id}
    return render(request, 'backoffice/hall_booking/cheque_details.html',data)


@csrf_exempt
def get_cheque_datatable(request):
    try:
        print 'backofficeapp | cheque_bounce.py | get_cheque_datatable | user = ', request.user
        dataList = []
        booking_details = []
        booking_details_list = []
        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        # abc_list = ['','id']
        # column_name = order + abc_list
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        start_date = ''
        end_date = ''

        gstObj = Servicetax.objects.get(tax_type=0, is_active=True)

        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = (datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')).replace(hour=23,
                                                                                                     minute=59)  # + datetime.timedelta(days=1)
            original_end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')
            original_start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')

            date_list = []
            if start_date == original_end_date:
                date_list.append(start_date.date())
            else:
                while original_start_date <= original_end_date:
                    date_list.append(original_start_date.date())
                    original_start_date = original_start_date + datetime.timedelta(days=1)
                    pass

            print 'start_date = ', start_date
            print 'end_date = ', end_date
            print 'date_list = ', date_list

        temp_booking_details = []
        if request.GET.get('select_hall') != "all":
            if start_date and end_date:
                temp_booking_details_list = HallBookingDetail.objects.filter(
                    hall_detail_id=int(request.GET.get('select_hall'))).exclude(booking_status__in=[0, 10])
                for item in temp_booking_details_list:
                    if item.booking_from_date.date() in date_list:
                        temp_booking_details.append(item.id)
                booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details)
            else:
                booking_details = HallBookingDetail.objects.filter(hall_detail_id=int(request.GET.get('select_hall')), \
                                                                   ).exclude(booking_status__in=[0, 10])
        else:
            if start_date and end_date:
                temp_booking_details_list = HallBookingDetail.objects.filter(
                    hall_location_id=int(request.GET.get('select_location'))).exclude(booking_status__in=[0, 10])
                for item in temp_booking_details_list:
                    if item.booking_from_date.date() in date_list:
                        # print '\nsecond if date = ',item.booking_from_date.astimezone(to_zone).date()
                        # print '\n 2 second if date = ',item.booking_from_date.date()
                        temp_booking_details.append(item.id)
                booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details)
            else:
                booking_details = HallBookingDetail.objects.filter(
                    hall_location_id=int(request.GET.get('select_location')), \
                    ).exclude(booking_status__in=[0, 10])

        booking_details = booking_details.distinct().values('hall_booking_id')

        if request.GET.get('select_payment'):
            if searchTxt:
                hallbookings = HallBooking.objects.filter(
                    Q(updated_by__icontains=searchTxt) | Q(booking_no__icontains=searchTxt) | Q(
                        name__icontains=searchTxt),
                    is_deleted=False, payment_status=request.GET.get('select_payment')).values('id')
            else:
                hallbookings = HallBooking.objects.filter(is_deleted=False,
                                                          payment_status=request.GET.get('select_payment')).values('id')
        else:
            if searchTxt:
                hallbookings = HallBooking.objects.filter(
                    Q(updated_by__icontains=searchTxt) | Q(booking_no__icontains=searchTxt) | Q(
                        name__icontains=searchTxt), is_deleted=False).values('id')
            else:
                hallbookings = HallBooking.objects.filter(is_deleted=False).values('id')

        booking_detail_list = [d['hall_booking_id'] for d in booking_details]
        hallbookings_list = [d['id'] for d in hallbookings]

        final_list = list(set(booking_detail_list).intersection(hallbookings_list))
        total_record = len(final_list)
        final_list = sorted(final_list, reverse=True)
        final_list = final_list[start:length]

        i = 0
        a = 1
        for hallbooking in final_list:
            tempList = []
            i = start + a
            a = a + 1

            final_booking_details = HallBookingDetail.objects.filter(hall_booking_id=hallbooking)

            hall_name = ''
            action = ''
            if booking_details:
                for booking_detail in final_booking_details:
                    if booking_detail.hall_detail:
                        hall_name = (hall_name + "\n" if hall_name else '') + booking_detail.hall_detail.hall_name
                    else:
                        hall_name = 'NA'

                action = '<a class="fa fa-eye" href="/backofficeapp/cheque-details/' + str(
                    booking_detail.hall_booking.id) + '"></a>'

                tempList.append(str(i))
                tempList.append(booking_detail.hall_booking.booking_no)
                tempList.append(hall_name)
                tempList.append(str(booking_detail.hall_booking.name))
                tempList.append(booking_detail.contact_person)
                tempList.append(booking_detail.mobile_no)
                tempList.append(booking_detail.email)
                tempList.append(booking_detail.hall_booking.get_booking_status_display())
                tempList.append(action)
                dataList.append(tempList)

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | hall_booking_registration.py | get_hall_regs_datatable | user %s. Exception = ', str(
            traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')





@csrf_exempt
def get_cheque_details_datatable(request):
    try:
        print 'backofficeapp | cheque_bounce.py | get_cheque_details_datatable | user = ', request.user
        dataList = []
        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        # abc_list = ['','id']
        # column_name = order + abc_list
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))


        hall_booking_id = request.GET.get('hall_booking_id')
        cheque_details_list = HallPaymentDetail.objects.filter(hall_booking_id=hall_booking_id,
                                                               offline_payment_by=0, is_deleted=False)

        total_record = len(cheque_details_list)
        cheque_details_list = cheque_details_list[start:length]

        for cheque_obj in cheque_details_list:
            tempList = []

            action = '<button onclick="get_cheque_data('+str(cheque_obj.id)+')"  class ="btn btn-danger btn-circle" type = "button" title = "Cancel Cheque" > <i class ="fa fa-times"> </i> </button > &nbsp;'

            if cheque_obj.is_deleted == False:
                status = '<label class="label label-success"> Active </label>'
            else:
                status = '<label class="label label-danger"> Bounced </label>'


            tempList.append(cheque_obj.cheque_no)
            tempList.append(str(cheque_obj.cheque_date.strftime('%d-%m-%Y')))
            tempList.append(cheque_obj.bank_name)
            tempList.append(str(cheque_obj.paid_amount))
            tempList.append(str(cheque_obj.tds_amount))
            tempList.append(status)
            tempList.append(action)
            dataList.append(tempList)

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print  e
        print 'Exception backofficeapp | cheque_bounce.py | get_hall_regs_datatable | user %s. Exception = ', str(
            traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_bounce_cheque_details(request):
    data = {}
    try:
        print '\nRequest IN | cheque_bounce.py | get_bounce_cheque_details | User = ', request.user
        print request.GET.get('pay_cheque_id')

        bounce_cheque_obj = HallPaymentDetail.objects.get(id=request.GET.get('pay_cheque_id'))

        data = {'success': 'true',
                'cheque_no': bounce_cheque_obj.cheque_no,
                'cheque_date': bounce_cheque_obj.cheque_date.strftime('%d/%m/%Y'),
                'bank_name': bounce_cheque_obj.bank_name,
                'paid_amount': str(bounce_cheque_obj.paid_amount),
                'tds_amount': str(bounce_cheque_obj.tds_amount),

                }

        print '\nResponse OUT | cheque_bounce.py | get_bounce_cheque_details | User = ', request.user
    except Exception, e:
        print '\nException IN | cheque_bounce.py | get_bounce_cheque_details | User = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Admin Saves Offline Booking Detail
@csrf_exempt
@transaction.atomic
def update_cheque_details(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | cheque_bounce.py | update_cheque_details | User = ', request.user


        bounce_cheque_obj = HallPaymentDetail.objects.get(id=request.POST.get('pay_cheque_id'))
        bounce_cheque_obj.is_deleted = True
        bounce_cheque_obj.bounce_charge = request.POST.get('modal_extra_amt')
        bounce_cheque_obj.bounce_cheque_remark = request.POST.get('modal_remark')
        bounce_cheque_obj.save()

        hall_booking_obj = HallBooking.objects.get(id=bounce_cheque_obj.hall_booking.id)

        print  '.............hall_booking_obj.......',hall_booking_obj.id

        other_cheque_objs = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj,is_deleted=False,payment_status=10).exclude(id=bounce_cheque_obj.id).last()

        pay_half_gst_amount = round((Decimal(bounce_cheque_obj.bounce_charge) * Decimal(0.09)), 2)
        pay_total_tax = pay_half_gst_amount*2

        print  '>>>>>>>>>>>>>>>>>>>>>>>....',other_cheque_objs
        if other_cheque_objs:
            other_cheque_objs.payable_amount = Decimal(other_cheque_objs.payable_amount) + Decimal(bounce_cheque_obj.paid_amount) + Decimal(bounce_cheque_obj.bounce_charge) + Decimal(pay_total_tax)
            other_cheque_objs.save()

        else:
            new_payment_obj = HallPaymentDetail(
                hall_booking=hall_booking_obj,
                payable_amount=Decimal(bounce_cheque_obj.paid_amount) + Decimal(bounce_cheque_obj.bounce_charge) + Decimal(pay_total_tax),
                created_by=str(request.user)
            )
            new_payment_obj.save()

        hall_booking_obj.total_rent = Decimal(hall_booking_obj.total_rent) + Decimal(bounce_cheque_obj.bounce_charge)
        hall_booking_obj.save()
        half_gst_amount = round((Decimal(hall_booking_obj.total_rent) * Decimal(0.09)), 2)
        total_tax = half_gst_amount*2
        hall_booking_obj.gst_amount = total_tax
        hall_booking_obj.total_payable = round(Decimal(hall_booking_obj.total_rent) + Decimal(hall_booking_obj.deposit) + Decimal(hall_booking_obj.gst_amount), 0)
        hall_booking_obj.save()
        
        
        total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).aggregate(
            total_paid=Sum('paid_amount'))
        
        hall_booking_obj.paid_amount = Decimal(total_paid_dict['total_paid'])
        hall_booking_obj.save()
        hall_booking_obj.payment_status = 8
        hall_booking_obj.save()
        if hall_booking_obj.paid_amount == hall_booking_obj.total_payable:
            hall_booking_obj.payment_status = 1
            hall_booking_obj.save()


        data['success'] = 'true'
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | cheque_bounce.py | update_cheque_details | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | cheque_bounce.py | update_cheque_details | User = ', str(
            traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')