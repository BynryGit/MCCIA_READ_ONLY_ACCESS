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
from datetime import datetime
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
from django.shortcuts import render_to_response
from django.template import RequestContext




from adminapp.models import Committee
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallBooking,HallBookingDetail,HallLocation,HallDetail, HallCheckAvailability, HallPaymentDetail, HallEquipment,BookingDetailHistory, Holiday, HallBookingDepositDetail, UserTrackDetail
from hallbookingapp.view.hall_booking_confirm import send_booking_invoice_mail, send_booking_invoice_mail_locationvise
from adminapp.models import Servicetax
import datetime
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required

charset='utf-8'
to_zone = tz.gettz("Asia/Kolkata")

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Bookings Registrations'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def hall_booking_registration_landing(request):
    hall_location_list=HallLocation.objects.filter(is_deleted=False)
    data={'hall_location_list':hall_location_list}
    return render(request, 'backoffice/hall_booking/hall_booking_registration.html',data)

def get_hall_list(request):
    """to get zone wrt branch"""
    try:
        hall_list = []
        hall_objs = HallDetail.objects.filter(is_deleted=False, hall_location_id=request.GET.get('select_location')).order_by('hall_name')
        for hall_obj in hall_objs:
            hall_data = {
                'hall_id': hall_obj.id,
                'hall_name': hall_obj.hall_name
            }
            hall_list.append(hall_data)
        data = {'success': 'true', 'hall': hall_list}
    except Exception as exe:
        print exe
        data = {'success': 'false', 'hall': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


# @csrf_exempt
# def get_hall_regs_datatable(request):
#     try:
#         print 'backofficeapp | hall_booking_registration.py | get_hall_regs_datatable | user = ', request.user
#         dataList = []
#         booking_details=[]
#         booking_details_list=[]
#         total_record=0
#         column = request.GET.get('order[0][column]')
#         searchTxt = request.GET.get('search[value]')        
#         order = ""
#         if request.GET.get('order[0][dir]') == 'desc':
#             order = "-"
#         # abc_list = ['','id']
#         # column_name = order + abc_list
#         start = int(request.GET.get('start'))
#         length = int(request.GET.get('length')) + int(request.GET.get('start'))                
        
#         start_date = ''
#         end_date = ''      

#         gstObj = Servicetax.objects.get(tax_type=0,is_active=True)

#         if request.GET.get('start_date') and request.GET.get('end_date'):
#             start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
#             end_date = (datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')).replace(hour=23, minute=59)# + datetime.timedelta(days=1)
#             original_end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')
#             original_start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')

#             date_list = []
#             if start_date == original_end_date:
#                 date_list.append(start_date.date())
#             else:
#                 while original_start_date <= original_end_date:
#                     date_list.append(original_start_date.date())
#                     original_start_date = original_start_date + datetime.timedelta(days=1)
#                     pass

#             print 'start_date = ',start_date
#             print 'end_date = ',end_date
#             print 'date_list = ',date_list
        
#         temp_booking_details = []
#         if request.GET.get('select_hall') != "all":
#             if start_date and end_date:                
#                 temp_booking_details_list = HallBookingDetail.objects.filter(hall_detail_id=int(request.GET.get('select_hall'))).exclude(booking_status__in=[0,10])                
#                 for item in temp_booking_details_list:
#                     if item.booking_from_date.date() in date_list:                        
#                         temp_booking_details.append(item.id)                    
#                 booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details)
#             else:
#                 booking_details = HallBookingDetail.objects.filter(hall_detail_id=int(request.GET.get('select_hall')),\
#                     ).exclude(booking_status__in=[0,10])
#         else:
#             if start_date and end_date:
#                 temp_booking_details_list = HallBookingDetail.objects.filter(hall_location_id=int(request.GET.get('select_location'))).exclude(booking_status__in=[0,10])
#                 for item in temp_booking_details_list:
#                     if item.booking_from_date.date() in date_list:
#                         # print '\nsecond if date = ',item.booking_from_date.astimezone(to_zone).date()
#                         # print '\n 2 second if date = ',item.booking_from_date.date()
#                         temp_booking_details.append(item.id)        
#                 booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details)                
#             else:
#                 booking_details = HallBookingDetail.objects.filter(hall_location_id=int(request.GET.get('select_location')),\
#                     ).exclude(booking_status__in=[0,10])        
        
#         booking_details = booking_details.distinct().values('hall_booking_id')        

#         if request.GET.get('select_payment'):         
#             if searchTxt:                    
#                 hallbookings = HallBooking.objects.filter(Q(updated_by__icontains=searchTxt) | Q(booking_no__icontains=searchTxt) | Q(name__icontains=searchTxt),
#                                                                              is_deleted=False,payment_status=request.GET.get('select_payment')).values('id')        
#             else:
#                 hallbookings = HallBooking.objects.filter(is_deleted=False,payment_status=request.GET.get('select_payment')).values('id')        
#         else:
#             if searchTxt:
#                 hallbookings = HallBooking.objects.filter(Q(updated_by__icontains=searchTxt) | Q(booking_no__icontains=searchTxt) | Q(name__icontains=searchTxt),is_deleted=False).values('id')                            
#             else:
#                 hallbookings = HallBooking.objects.filter(is_deleted=False).values('id')         
    
#         booking_detail_list = [d['hall_booking_id'] for d in booking_details]        
#         hallbookings_list = [d['id'] for d in hallbookings]  
    
#         final_list = list(set(booking_detail_list).intersection(hallbookings_list))
#         total_record = len(final_list)
#         final_list = sorted(final_list, reverse=True)
#         final_list = final_list[start:length]        
        
#         i = 0
#         a = 1        
#         for hallbooking in final_list:
#             tempList = []
#             i = start + a
#             a = a + 1                          
                                    
#             # if start_date and end_date:
#             #     final_temp_list = []
#             #     temp_list = HallBookingDetail.objects.filter(hall_booking_id=hallbooking)                                                               
#             #     for item in temp_list:
#             #         if item.booking_from_date.date() in date_list:
#             #             final_temp_list.append(item.id)
#             #     final_booking_details = HallBookingDetail.objects.filter(id__in=final_temp_list)
#             # else:
#             final_booking_details = HallBookingDetail.objects.filter(hall_booking_id=hallbooking)            

#             hall_name = ''
#             time_slot = ''
#             action = ''
#             date_slot = ''
#             if booking_details:

#                 for booking_detail in final_booking_details:

#                     # total_extra_charges = booking_detail.hall_booking.total_rent - booking_detail.hall_booking.discounted_total_rent
#                     # print ',..........total_extra_charges.....',total_extra_charges
#                     # gst_total_extra_charges = (Decimal(total_extra_charges) * Decimal(gstObj.tax))  / 100

#                     # print ',..........GST.....',gst_total_extra_charges

#                     # total_extra_charges = total_extra_charges + gst_total_extra_charges
#                     # print '....final..',total_extra_charges


#                     if booking_detail.hall_detail:
#                         hall_name = (hall_name + "\n" if hall_name else '') + booking_detail.hall_detail.hall_name
#                     else:
#                         hall_name = 'NA'
#                     if booking_detail.updated_by:
#                         time_slot = time_slot + str(booking_detail.booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p')) + '-' + \
#                                     str(booking_detail.booking_to_date.astimezone(to_zone).time().strftime('%I:%M %p')) + '\n'
#                     else:
#                         time_slot = time_slot + str(booking_detail.booking_from_date.strftime('%I:%M %p')) + '-' + \
#                                     str(booking_detail.booking_to_date.strftime('%I:%M %p')) + '\n'
#                     date_slot =  date_slot + str(booking_detail.booking_from_date.strftime('%B %d,%Y')) + '\n'                

#                 if booking_detail.hall_booking.booking_status in [2, 3, 4, 5, 6, 7, 8]:
#                     action = '<a class="fa fa-pencil" href="/backofficeapp/open-edit-booking/' + str(booking_detail.hall_booking.id) + '"></a>'
#                 elif booking_detail.hall_booking.payment_status == 1:                    
#                     action = 'PAID'                    
#                 elif booking_detail.hall_booking.booking_status == 9:
#                     hallPayobj = HallPaymentDetail.objects.filter(hall_booking = booking_detail.hall_booking).last()
#                     if hallPayobj:
#                         if hallPayobj.payment_status == 1:
#                             remaining_amount = 0
#                             paid_amount = booking_detail.hall_booking.total_payable
#                         else:
#                             remaining_amount = hallPayobj.payable_amount
#                             paid_amount = Decimal(booking_detail.hall_booking.total_payable) - Decimal(hallPayobj.payable_amount)
#                     else:
#                         remaining_amount = 0
#                         paid_amount = 0

#                     total_hall_rent = Decimal(booking_detail.hall_booking.first_total_rent_for_reference) + (Decimal(booking_detail.hall_booking.first_total_rent_for_reference) * Decimal(gstObj.tax))  / 100
#                     extra_charge = Decimal(booking_detail.hall_booking.extra_hour_charge) + Decimal(booking_detail.hall_booking.total_facility_charge) + Decimal(booking_detail.hall_booking.extra_broken_charge)
#                     extra_charge = Decimal(extra_charge) + (Decimal(extra_charge) * Decimal(gstObj.tax))  / 100

#                     deposit = 0
#                     if booking_detail.hall_booking.user_track:
#                         user_track_obj = UserTrackDetail.objects.get(id=booking_detail.hall_booking.user_track.id)
#                         deposit = user_track_obj.deposit_available
#                     action = '<a class="fa fa-rupee" data-toggle="modal" data-target="#hall_booking_payment_modal"' \
#                              'onclick="show_booking_payment_modal(' + str(booking_detail.hall_booking.id) + \
#                              ',' + str(round(booking_detail.hall_booking.total_payable, 0)) + ',' + str(round(total_hall_rent, 0)) + ',' + str(round(extra_charge, 0)) + ',' + str(round(paid_amount, 0)) + ',' + str(round(remaining_amount, 0)) + ',' + str(round(deposit, 0)) + ')"></a>' 


#                 action_2 = '<a  class="fa fa-cut" title="Deposit/Discount" data-toggle="modal" data-target="#edit_deposit_modal"' \
#                                  'onclick="edit_booking_deposit(' + str(booking_detail.hall_booking.id) + \
#                                  ',' + str(round(booking_detail.hall_booking.deposit, 0)) +',' + str(round(booking_detail.hall_booking.discount_per, 0)) + ')"></a>'

#                 action_3 = '<a class="fa fa-paper-plane" title="Send Mail"  data-toggle="modal" data-target="#send_invoice_mail"  onclick="open_mail_request(' + str(booking_detail.hall_booking.id) + ')"></a>'

#                 action_4 = '<a class="fa fa-cart-plus" href="/backofficeapp/open-extra-booking/' + str(booking_detail.hall_booking.id) + '"></a>'

#                 # tempList.append(str(i))
#                 tempList.append(str(i))
#                 tempList.append(date_slot)
#                 tempList.append(time_slot)
#                 tempList.append(booking_detail.hall_booking.created_date.strftime('%B %d,%Y'))
#                 tempList.append(booking_detail.hall_booking.booking_no)
#                 tempList.append(hall_name)                                        
#                 tempList.append(str(booking_detail.event_nature))
                
#                 if booking_detail.hall_booking.member:
#                     tempList.append(str(booking_detail.hall_booking.member.member_associate_no))
#                 else:
#                     tempList.append("-")

#                 tempList.append(str(booking_detail.hall_booking.name))
#                 tempList.append(booking_detail.contact_person)
#                 tempList.append(booking_detail.mobile_no)
#                 tempList.append(booking_detail.email)
#                 tempList.append(str(booking_detail.hall_booking.total_payable))
#                 tempList.append(booking_detail.hall_booking.get_booking_status_display())
#                 tempList.append(action + '<br>' + action_2 + '<br>' + action_3 + '<br>' + action_4)
#                 dataList.append(tempList)       
        
#         data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
#     except Exception as e:
#         print 'Exception backofficeapp | hall_booking_registration.py | get_hall_regs_datatable | user %s. Exception = ', str(traceback.
#             print_exc())
#         data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
#     return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_hall_regs_datatable(request):
    try:
        print 'backofficeapp | hall_booking_registration.py | get_hall_regs_datatable | user = ', request.user
        dataList = []
        booking_details=[]
        booking_details_list=[]
        total_record=0
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
        booking_start_date = ''
        booking_end_date = ''
        gstObj = Servicetax.objects.get(tax_type=0,is_active=True)

        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = (datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y')).replace(hour=23, minute=59)# + datetime.timedelta(days=1)
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

        if request.GET.get('booking_start_date') and request.GET.get('to_end_date'):
            booking_start_date = datetime.datetime.strptime(request.GET.get('booking_start_date'), '%d/%m/%Y')
            booking_end_date = (datetime.datetime.strptime(request.GET.get('to_end_date'), '%d/%m/%Y')).replace(hour=23, minute=59)# + datetime.timedelta(days=1)
            booking_original_end_date = datetime.datetime.strptime(request.GET.get('to_end_date'), '%d/%m/%Y')
            booking_original_start_date = datetime.datetime.strptime(request.GET.get('booking_start_date'), '%d/%m/%Y')
            booking_date_list = []
            if booking_start_date == booking_original_end_date:
                booking_date_list.append(booking_start_date.date())
            else:
                while booking_original_start_date <= booking_original_end_date:
                    booking_date_list.append(booking_original_start_date.date())
                    booking_original_start_date = booking_original_start_date + datetime.timedelta(days=1)
                    pass
        

        temp_booking_details = []
        if request.GET.get('select_hall') != "all":
            temp_booking_details_list = HallBookingDetail.objects.filter(hall_detail_id=int(request.GET.get('select_hall'))).exclude(booking_status__in=[1,10],pi_no__isnull = False)
            if start_date and end_date:   
                for item in temp_booking_details_list:
                    if start_date and end_date:
                        if item.booking_from_date.date() in date_list:                        
                            temp_booking_details.append(item.id)   
                    booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details)
                
            elif booking_start_date and booking_end_date:
                for item in temp_booking_details_list:            
                    if booking_start_date and booking_end_date:
                        if item.hall_booking.created_date.date() in booking_date_list:                        
                            temp_booking_details.append(item.id)   
                    booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details)
            else:
                booking_details = HallBookingDetail.objects.filter(hall_detail_id=int(request.GET.get('select_hall')),\
                    ).exclude(booking_status__in=[1,10],pi_no__isnull = False)
        else:
            temp_booking_details_list = HallBookingDetail.objects.filter(hall_location_id=int(request.GET.get('select_location'))).exclude(booking_status__in=[1,10],pi_no__isnull = False)
            if start_date and end_date:
                for item in temp_booking_details_list:
                    if item.booking_from_date.date() in date_list:
                        temp_booking_details.append(item.id) 
                booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details) 
                
            elif booking_start_date and booking_end_date:
                for item in temp_booking_details_list:
                    if item.hall_booking.created_date.date() in booking_date_list:
                        temp_booking_details.append(item.id)   
                booking_details = HallBookingDetail.objects.filter(id__in=temp_booking_details)                
            else:
                booking_details = HallBookingDetail.objects.filter(hall_location_id=int(request.GET.get('select_location')),\
                    ).exclude(booking_status__in=[1,10])

        booking_details = booking_details.exclude(pi_no__isnull = True)

        # .exclude(alias__isnull=True)
        booking_details = booking_details.distinct().values('hall_booking_id')
        if request.GET.get('select_payment'):         
            if searchTxt:                    
                hallbookings = HallBooking.objects.filter(Q(updated_by__icontains=searchTxt) | Q(booking_no__icontains=searchTxt) | Q(name__icontains=searchTxt),
                                                                             payment_status=request.GET.get('select_payment')).values('id')        
            else:
                hallbookings = HallBooking.objects.filter(payment_status=request.GET.get('select_payment')).values('id')        
        else:
            if searchTxt:
                hallbookings = HallBooking.objects.filter(Q(updated_by__icontains=searchTxt) | Q(booking_no__icontains=searchTxt) | Q(name__icontains=searchTxt)).values('id')                            
            else:
                hallbookings = HallBooking.objects.all().values('id')         
    
        booking_detail_list = [d['hall_booking_id'] for d in booking_details]        
        hallbookings_list = [d['id'] for d in hallbookings]  
        final_list = list(set(booking_detail_list).intersection(hallbookings_list))

        total_record = len(final_list)
        final_list = sorted(final_list, reverse=True)
        if length != -1:
            final_list = final_list[start:length]        
        else:
            final_list = final_list[::-1]
        
        i = 0
        a = 1        
        for hallbooking in final_list:
            tempList = []
            i = start + a
            a = a + 1                          
                                    
            # if start_date and end_date:
            #     final_temp_list = []
            #     temp_list = HallBookingDetail.objects.filter(hall_booking_id=hallbooking)                                                               
            #     for item in temp_list:
            #         if item.booking_from_date.date() in date_list:
            #             final_temp_list.append(item.id)
            #     final_booking_details = HallBookingDetail.objects.filter(id__in=final_temp_list)
            # else:
            final_booking_details = HallBookingDetail.objects.filter(hall_booking_id=hallbooking)            

            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            get_financial = get_financial_year(current_date)

            for item in final_booking_details:
                hall_location = item.hall_location.location
                if hall_location == 'MCCIA Trade Tower (5th Floor)':
                    office_name = 'SB Road Office'
                    sb_pi_no = 'PI/' + str(get_financial) + '/' + str(item.pi_no)
                    sb_contact_person = item.hall_location.contact_person1.name + ' (SB Road Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
                    booking_no = item.hall_booking.booking_no +'<br>' +sb_pi_no
                elif hall_location == 'Tilak Road':
                    office_name = 'Tilak Road Office'
                    tilak_pi_no = 'TPI/' + str(get_financial) + '/' + str(item.pi_no)
                    tilak_contact_person = item.hall_location.contact_person1.name + ' (Tilak Road Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
                    booking_no = item.hall_booking.booking_no +'<br>' +tilak_pi_no
                elif hall_location == 'Bhosari':
                    office_name = 'Bhosari Office'
                    bpi_pi_no = 'BPI/' + str(get_financial) + '/' + str(item.pi_no)
                    bpi_contact_person = item.hall_location.contact_person1.name + ' (Bhosari Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
                    booking_no = item.hall_booking.booking_no +'<br>' +bpi_pi_no
                elif hall_location == 'Hadapsar':
                    office_name = 'Hadapsar Office'
                    hpi_pi_no = 'HPI/' + str(get_financial) + '/' + str(item.pi_no)
                    hpi_contact_person = item.hall_location.contact_person1.name + ' (Hadapsar Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
                    booking_no = item.hall_booking.booking_no +'<br>' +hpi_pi_no
                else:
                    booking_no = 'None'

            hall_name = ''
            time_slot = ''
            action = ''
            date_slot = ''
            if booking_details:

                for booking_detail in final_booking_details:
                    # total_extra_charges = booking_detail.hall_booking.total_rent - booking_detail.hall_booking.discounted_total_rent
                    # print ',..........total_extra_charges.....',total_extra_charges
                    # gst_total_extra_charges = (Decimal(total_extra_charges) * Decimal(gstObj.tax))  / 100

                    # print ',..........GST.....',gst_total_extra_charges

                    # total_extra_charges = total_extra_charges + gst_total_extra_charges
                    # print '....final..',total_extra_charges


                    if booking_detail.hall_detail:
                        hall_name = (hall_name + "\n" if hall_name else '') + booking_detail.hall_detail.hall_name
                    else:
                        hall_name = 'NA'
                    if booking_detail.updated_by:
                        if booking_detail.is_cancelled:
                            booking_from_date = booking_detail.booking_from_date - timedelta(hours=5, minutes=30)
                            booking_to_date = booking_detail.booking_to_date - timedelta(hours=5, minutes=30)
                        else:
                            booking_from_date = booking_detail.booking_from_date
                            booking_to_date = booking_detail.booking_to_date

                        time_slot = time_slot + str(booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p')) + '-' + \
                                    str(booking_to_date.astimezone(to_zone).time().strftime('%I:%M %p')) + '\n'
                    else:
                        if booking_detail.is_cancelled:
                            booking_from_date = booking_detail.booking_from_date - timedelta(hours=5, minutes=30)
                            booking_to_date = booking_detail.booking_to_date - timedelta(hours=5, minutes=30)
                        else:
                            booking_from_date = booking_detail.booking_from_date
                            booking_to_date = booking_detail.booking_to_date
                            
                        time_slot = time_slot + str(booking_from_date.strftime('%I:%M %p')) + '-' + \
                                    str(booking_to_date.strftime('%I:%M %p')) + '\n'
                    date_slot =  date_slot + str(booking_detail.booking_from_date.strftime('%B %d,%Y')) + '\n'                

                if booking_detail.hall_booking.booking_status in [2, 3, 4, 5, 6, 7, 8]:
                    action = '<a class="fa fa-pencil" href="/backofficeapp/open-edit-booking/' + str(booking_detail.hall_booking.id) + '"></a>'
                elif booking_detail.hall_booking.payment_status == 1:                    
                    action = 'PAID'     
                elif booking_detail.hall_booking.booking_status == 0:
                    action = 'Cancelled'            
                elif booking_detail.hall_booking.booking_status == 9:
                    hallPayobj = HallPaymentDetail.objects.filter(hall_booking = booking_detail.hall_booking).last()
                    if hallPayobj:
                        if hallPayobj.payment_status == 1:
                            remaining_amount = 0
                            paid_amount = booking_detail.hall_booking.total_payable
                        else:
                            remaining_amount = hallPayobj.payable_amount
                            paid_amount = Decimal(booking_detail.hall_booking.total_payable) - Decimal(hallPayobj.payable_amount)
                    else:
                        remaining_amount = 0
                        paid_amount = 0

                    total_hall_rent = Decimal(booking_detail.hall_booking.first_total_rent_for_reference) # + (Decimal(booking_detail.hall_booking.first_total_rent_for_reference) * Decimal(gstObj.tax))  / 100
                    extra_charge = Decimal(booking_detail.hall_booking.extra_hour_charge) + Decimal(booking_detail.hall_booking.total_facility_charge) + Decimal(booking_detail.hall_booking.extra_broken_charge)
                    #extra_charge = Decimal(extra_charge) + (Decimal(extra_charge) * Decimal(gstObj.tax))  / 100

                    total_gst = (total_hall_rent * Decimal(gstObj.tax))  / 100 + (Decimal(extra_charge) * Decimal(gstObj.tax))  / 100

                    deposit = 0
                    if booking_detail.hall_booking.user_track:
                        user_track_obj = UserTrackDetail.objects.get(id=booking_detail.hall_booking.user_track.id)
                        deposit = user_track_obj.deposit_available
                    action = '<a class="fa fa-rupee" data-toggle="modal" data-target="#hall_booking_payment_modal"' \
                             'onclick="show_booking_payment_modal(' + str(booking_detail.hall_booking.id) + \
                             ',' + str(round(booking_detail.hall_booking.total_payable, 0)) + ',' + str(round(total_hall_rent, 0)) + ',' + str(round(extra_charge, 0)) + ',' + str(round(total_gst, 0)) + ',' + str(round(booking_detail.hall_booking.deposit, 0)) + ',' + str(round(paid_amount, 0)) + ',' + str(round(remaining_amount, 0)) + ',' + str(round(booking_detail.hall_booking.refund_amount, 0)) + ',' + str(round(deposit, 0)) + ')"></a>' 

                action_2 = '<a  class="fa fa-cut" title="Deposit/Discount" data-toggle="modal" data-target="#edit_deposit_modal"' \
                                 'onclick="edit_booking_deposit(' + str(booking_detail.hall_booking.id) + \
                                 ',' + str(round(booking_detail.hall_booking.deposit, 0)) +',' + str(round(booking_detail.hall_booking.discount_per, 0)) + ')"></a>'
                if booking_detail.pi_no != None:
                    action_3 = '<a class="fa fa-paper-plane" title="Send Mail"  data-toggle="modal" onclick="open_mail_request(' + str(booking_detail.hall_booking.id) + ')"></a>'
                else:
                    action_3 = ""
                action_4 = '<a class="fa fa-cart-plus" href="/backofficeapp/open-extra-booking/' + str(booking_detail.hall_booking.id) + '"></a>'
                # tempList.append(str(i))
                # if sb_pi_no:
                #     booking_no = booking_detail.hall_booking.booking_no +'<br>' +sb_pi_no
                # elif tilak_pi_no:
                #     booking_no = booking_detail.hall_booking.booking_no +'<br>' +tilak_pi_no
                # elif bpi_pi_no: 
                #     booking_no = booking_detail.hall_booking.booking_no +'<br>' +bpi_pi_no
                # elif hpi_pi_no:
                #     booking_no = booking_detail.hall_booking.booking_no +'<br>' +hpi_pi_no
                # else:
                #     booking_no = booking_detail.hall_booking.booking_no +'<br>' + 'None'

                tempList.append(str(i))
                tempList.append(date_slot)
                tempList.append(time_slot)
                tempList.append(booking_detail.hall_booking.created_date.astimezone(to_zone).strftime('%B %d,%Y %I:%M %p'))
                tempList.append(booking_no)
                tempList.append(hall_name)                                        
                tempList.append(str(booking_detail.event_nature))

                
                if booking_detail.hall_booking.member and booking_detail.hall_booking.member.member_associate_no:
                    if booking_detail.hall_booking.member.valid_invalid_member == False:
                        tempList.append(str(booking_detail.hall_booking.member.member_associate_no)+'<br>' + str('Membership Due'))
                    else:
                        tempList.append(str(booking_detail.hall_booking.member.member_associate_no))
                elif booking_detail.hall_booking.member and not booking_detail.hall_booking.member.member_associate_no:
                    tempList.append(str('IA-TMP'))
                else:
                    tempList.append("-")
                

                tempList.append(str(booking_detail.hall_booking.name))
                tempList.append(booking_detail.contact_person)
                tempList.append(booking_detail.mobile_no)
                tempList.append(booking_detail.email)
                tempList.append(str(booking_detail.hall_booking.total_payable))
                tempList.append(booking_detail.hall_booking.get_booking_status_display())
                tempList.append(action + '<br>' + action_2 + '<br>' + action_3 + '<br>' + action_4)
                dataList.append(tempList)       
        
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | hall_booking_registration.py | get_hall_regs_datatable | user %s. Exception = ', str(traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Open Hall Booking Edit Page
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Bookings Registrations'],login_url='/backofficeapp/login/',raise_exception=True)
def open_edit_booking(request, booking_id):
    data = {}
    data_dict = {}
    try:
        print '\nRequest IN | hall_booking_registration.py | open_edit_booking | User = ', request.user, booking_id
        bookingobj = HallBooking.objects.get(id=booking_id)
        booking_values = HallBookingDetail.objects.filter(hall_booking=bookingobj, is_active=True).values_list(
            'booking_detail_no').distinct()
        final_data = []
        print booking_values
        for booking_value in booking_values:
            print booking_value[0]
            booking_detail_objs = HallBookingDetail.objects.filter(hall_booking=bookingobj,
                                                                   booking_detail_no=booking_value[0], is_active=True)

            booking_detail_list = []
            booking_flow_data = {}
            for booking_detail_obj in booking_detail_objs:
                data = {}                
                data['detail_id'] = booking_detail_obj.id

                if booking_detail_obj.updated_by:   
                    data['booking_from_time'] = str(booking_detail_obj.booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p'))#str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))
                    data['booking_to_time'] = str(booking_detail_obj.booking_to_date.astimezone(to_zone).time().strftime('%I:%M %p'))# booking_detail_obj.booking_to_date.strftime('%I:%M %p')

                else:    
                    data['booking_from_time'] = str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))#str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))
                    data['booking_to_time'] = str(booking_detail_obj.booking_to_date.strftime('%I:%M %p'))# booking_detail_obj.booking_to_date.strftime('%I:%M %p')

                data['booking_date'] = booking_detail_obj.booking_from_date.strftime('%a %d, %b %Y')
                data['rent'] = str(booking_detail_obj.total_rent)
                data['extra_hour'] = str(booking_detail_obj.extra_hour)
                booking_detail_list.append(data)

            booking_detail_obj = booking_detail_objs.last()

            booking_flow_data['contact_person'] = booking_detail_obj.contact_person
            booking_flow_data['company_name'] = str(bookingobj.name)
            booking_flow_data['address'] = booking_detail_obj.address
            booking_flow_data['email'] = booking_detail_obj.email
            booking_flow_data['mobile_no'] = booking_detail_obj.mobile_no
            booking_flow_data['event_nature'] = booking_detail_obj.event_nature
            booking_flow_data['hall_name'] = booking_detail_obj.hall_detail.hall_name
            booking_flow_data['booking_detail'] = booking_detail_list

            final_data.append(booking_flow_data)
            # final_data.append(booking_flow_data)

        data_dict = {'data': final_data, 'booking_obj': bookingobj}
        print '\nResponse OUT | hall_booking_registration.py | open_edit_booking | User = ', request.user
    except Exception, e:
        print '\nException IN | hall_booking_registration.py | open_edit_booking | User = ', str(traceback.print_exc())
    return render(request, 'backoffice/hall_booking/edit_hall_booking.html', data_dict)


# Admin Rejects Hall Booking
@csrf_exempt
@transaction.atomic
def reject_booking(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_registration.py | reject_booking | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))

        # Change Booking Status in HallBooking, HallBookingDetail, HallCheckAvailability
        hall_booking_obj.booking_status = 10
        hall_booking_obj.save()

        for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
            hall_booking_detail.booking_status = 10
            hall_booking_detail.save()
            for hall_check_avail in HallCheckAvailability.objects.filter(hall_booking_detail=hall_booking_detail):
                hall_check_avail.booking_status = 10
                hall_check_avail.save()

        data['success'] = 'true'
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | hall_booking_registration.py | reject_booking | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_registration.py | reject_booking | User = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Admin Accepts Hall Booking
@csrf_exempt
@transaction.atomic
def accept_booking(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_registration.py | accept_booking | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))

        # Change Booking Status in HallBooking, HallBookingDetail, HallCheckAvailability
        hall_booking_obj.booking_status = 9
        hall_booking_obj.save()

        for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
            hall_booking_detail.booking_status = 9
            hall_booking_detail.save()
            for hall_check_avail in HallCheckAvailability.objects.filter(hall_booking_detail=hall_booking_detail):
                hall_check_avail.booking_status = 9
                hall_check_avail.save()

        data['success'] = 'true'
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | hall_booking_registration.py | accept_booking | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_registration.py | accept_booking | User = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Admin Saves Offline Booking Detail
@csrf_exempt
@transaction.atomic
def submit_hall_booking_offline_payment(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_registration.py | submit_hall_booking_offline_payment | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
        hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()
        hall_payment_obj.payment_status = 1
        hall_payment_obj.updated_by = str(request.user)

        if request.POST.get('user_Payment_Type') == 'ByCash':
            hall_payment_obj.paid_amount = Decimal(request.POST.get('cash_amount')) + Decimal(request.POST.get('TDS_amount'))
            hall_payment_obj.tds_amount = Decimal(request.POST.get('TDS_amount'))
            hall_payment_obj.cash_no = request.POST.get('cash_receipt_no')
            if int(request.POST.get('TDS_amount')):
                hall_payment_obj.is_tds = True

            hall_payment_obj.offline_payment_by = 1
            hall_payment_obj.save()            
            if hall_payment_obj.payable_amount > hall_payment_obj.paid_amount:    
                payable_amount = hall_payment_obj.payable_amount - hall_payment_obj.paid_amount
                new_payment_obj = HallPaymentDetail(
                    hall_booking=hall_booking_obj,
                    payable_amount=payable_amount,
                    created_by=str(request.user)
                )
                new_payment_obj.save()

        elif request.POST.get('user_Payment_Type') == 'ByCheque':
            hall_payment_obj.paid_amount = Decimal(request.POST.get('Cheque_amount')) + Decimal(request.POST.get('TDS_amount'))
            hall_payment_obj.tds_amount = Decimal(request.POST.get('TDS_amount'))
            if int(request.POST.get('TDS_amount')):
                hall_payment_obj.is_tds = True

            hall_payment_obj.offline_payment_by = 0
            hall_payment_obj.cheque_no = str(request.POST.get('ChequeNo'))
            hall_payment_obj.cheque_date = datetime.datetime.strptime(request.POST.get('ChequeDate'), '%d/%m/%Y').date()
            hall_payment_obj.bank_name = str(request.POST.get('BankName'))
            hall_payment_obj.save()  

            if hall_payment_obj.payable_amount > hall_payment_obj.paid_amount:    
                payable_amount = hall_payment_obj.payable_amount - hall_payment_obj.paid_amount
                new_payment_obj = HallPaymentDetail(
                    hall_booking=hall_booking_obj,
                    payable_amount=payable_amount,
                    created_by=str(request.user)
                )
                new_payment_obj.save()

        elif request.POST.get('user_Payment_Type') == 'ByNEFT':
            hall_payment_obj.paid_amount = Decimal(request.POST.get('NEFT_amount')) + Decimal(request.POST.get('TDS_amount'))
            hall_payment_obj.tds_amount = Decimal(request.POST.get('TDS_amount'))
            if int(request.POST.get('TDS_amount')):
                hall_payment_obj.is_tds = True


            hall_payment_obj.offline_payment_by = 2
            hall_payment_obj.neft_id = request.POST.get('neft_transfer_id')
            hall_payment_obj.save()  

            if hall_payment_obj.payable_amount > hall_payment_obj.paid_amount:    
                payable_amount = hall_payment_obj.payable_amount - hall_payment_obj.paid_amount
                new_payment_obj = HallPaymentDetail(
                    hall_booking=hall_booking_obj,
                    payable_amount=payable_amount,
                    created_by=str(request.user)
                )
                new_payment_obj.save()                

        else:
            today = datetime.datetime.now().date()
            exclude_hall_booking_list = []
            if hall_booking_obj.member:  
                print '.......1......'              
                exclude_hall_booking_list = HallBookingDetail.objects.filter(hall_booking__member_id=hall_booking_obj.member.id, booking_from_date__gte=today).exclude(hall_booking=hall_booking_obj)
            elif hall_booking_obj.user_track:
                print '.......2......'       
                exclude_hall_booking_list = HallBookingDetail.objects.filter(hall_booking__user_track_id=hall_booking_obj.user_track.id, booking_from_date__gte=today).exclude(hall_booking=hall_booking_obj)       

            if len(exclude_hall_booking_list) == 0:
                hall_payment_obj.offline_payment_by = 3
                hall_payment_obj.paid_amount = Decimal(request.POST.get('deposit_amount')) + Decimal(request.POST.get('TDS_amount'))
                hall_payment_obj.tds_amount = Decimal(request.POST.get('TDS_amount'))
                if int(request.POST.get('TDS_amount')):
                    hall_payment_obj.is_tds = True
                hall_payment_obj.save()  

                # Debiting deposit from hallbooking table
                hall_booking_obj.deposit = Decimal(hall_booking_obj.deposit) - Decimal(hall_payment_obj.paid_amount)
                hall_booking_obj.save()
                hall_booking_obj.refund_amount = hall_booking_obj.refund_amount + hall_booking_obj.deposit
                hall_booking_obj.deposit_status = 1
                hall_booking_obj.save()

                if hall_payment_obj.payable_amount > hall_payment_obj.paid_amount:    
                    payable_amount = hall_payment_obj.payable_amount - hall_payment_obj.paid_amount
                    new_payment_obj = HallPaymentDetail(
                        hall_booking=hall_booking_obj,
                        payable_amount=payable_amount,
                        created_by=str(request.user)
                    )
                    new_payment_obj.save()

                if hall_booking_obj.user_track:
                    user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)     
                    user_track_obj.deposit_available = 0
                    user_track_obj.deposit_status = 1                
                    user_track_obj.save()
            else:
                data['success'] = 'false1'
                return HttpResponse(json.dumps(data), content_type='application/json')                


        total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

        hall_booking_obj.paid_amount = Decimal(total_paid_dict['total_paid'])
        hall_booking_obj.save()
        if hall_booking_obj.paid_amount == hall_booking_obj.total_payable:
            hall_booking_obj.payment_status = 1
            hall_booking_obj.save()

        if hall_booking_obj.user_track:            
            if hall_booking_obj.deposit and hall_booking_obj.is_deposit_through_cheque == False:                        
                if hall_booking_obj.paid_amount >= hall_booking_obj.total_payable:
                    user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)     
                    user_track_obj.deposit_available = hall_booking_obj.deposit  
                    user_track_obj.deposit_status = 0
                    user_track_obj.refund_status = 0
                    user_track_obj.save()     

                    # exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),~Q(payment_status = 1),~Q(booking_status__in=[0,10])).exclude(id=hall_booking_obj.id)       

                    exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),Q(is_completed = False),~Q(booking_status__in=[0,10])).exclude(id=hall_booking_obj.id)       

                    for hall_obj in exclude_hall_booking_list:
                        exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)
                        
                        if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                            exclude_hall_obj.is_deposit_through_cheque = False
                            exclude_hall_obj.deposit_status = 0
                            exclude_hall_obj.save()
                            HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(is_deleted=True)
                        elif exclude_hall_obj.deposit:
                            if exclude_hall_obj.paid_amount < exclude_hall_obj.total_payable:
                                exclude_hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj).last()
                                exclude_total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

                                exclude_hall_obj.deposit = 0
                                exclude_hall_obj.save()
                                exclude_hall_obj.total_payable = round(exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount, 0)
                                exclude_hall_obj.save()
                                exclude_hall_payment_obj.payable_amount = Decimal(exclude_hall_obj.total_payable) - Decimal(exclude_total_paid_dict['total_paid'])
                                exclude_hall_payment_obj.save()

        data['success'] = 'true'
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | hall_booking_registration.py | submit_hall_booking_offline_payment | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_registration.py | submit_hall_booking_offline_payment | User = ', str(traceback.print_exc())
        # transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Admin Update Hall Booking Deposit
@csrf_exempt
@transaction.atomic
def update_booking_deposit(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_registration.py | update_booking_deposit | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
        hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()
        total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))
        if request.POST.get('deposit_amount'):
            hall_booking_obj.deposit = Decimal(request.POST.get('deposit_amount'))
            hall_booking_obj.save()

            hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()

            hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
            hall_payment_obj.save()

        
        if int(request.POST.get('apply_discount')):
            discount_percent = request.POST.get('apply_discount')

            hall_booking_obj.is_discount = True
            total_discount = (Decimal(discount_percent)/100)*(hall_booking_obj.total_rent)
            total_discount= round(Decimal(total_discount),2)
            discounted_total_rent = Decimal(hall_booking_obj.total_rent) - Decimal(total_discount)
            hall_booking_obj.discounted_total_rent = discounted_total_rent
            hall_booking_obj.save()
            half_gst_amount = round((Decimal(hall_booking_obj.discounted_total_rent) * Decimal(0.09)), 2)
            total_tax = half_gst_amount*2
            hall_booking_obj.gst_amount = total_tax
            hall_booking_obj.total_payable = round(Decimal(hall_booking_obj.discounted_total_rent) + Decimal(hall_booking_obj.deposit) + Decimal(hall_booking_obj.gst_amount), 0)
            hall_booking_obj.discount = Decimal(total_discount)
            hall_booking_obj.discount_per = Decimal(discount_percent)

            hall_booking_obj.save()

            hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
            hall_payment_obj.save()
        else:
            hall_booking_obj.is_discount = False
            hall_booking_obj.discounted_total_rent = 0
            hall_booking_obj.discount_per = 0
            half_gst_amount = round((Decimal(hall_booking_obj.total_rent) * Decimal(0.09)), 2)
            total_tax = half_gst_amount*2
            hall_booking_obj.gst_amount = total_tax
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(Decimal(hall_booking_obj.total_rent) + Decimal(hall_booking_obj.deposit) + Decimal(hall_booking_obj.gst_amount), 0)
            hall_booking_obj.save()

            hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
            hall_payment_obj.save()         

        data['success'] = 'true'
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | hall_booking_registration.py | update_booking_deposit | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_registration.py | update_booking_deposit | User = ', str(
            traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def get_cheque_details(request):
    data = {}
    try:
        print '\nRequest IN | hall_booking_registration.py | get_cheque_details | User = ', request.user
        print request.GET.get('booking_id')


        output_list = []
        hall_equipment_list = []

        facility_list = []
        equipment_name_list = []
        check_extra_hour_flag = 0
        check_extra_pre_hour_flag = 0


        hall_booking_obj = HallBooking.objects.get(id=request.GET.get('booking_id'))
        print '......hall_booking_obj.....',hall_booking_obj.is_deposit_through_cheque
                       
        cheque_detail_id = ''
        cheque_remark = ''
        date_of_return = ''
        mobile_no = ''  
        email = ''
        customer_name = ''
        amount = ''
        bank_name = ''
        cheque_date = ''
        cheque_no = ''
        deposit_status = ''

        try:
            cheque_detail_obj = HallBookingDepositDetail.objects.get(hall_booking=hall_booking_obj)
            print '.......',cheque_detail_obj
            cheque_detail_id = cheque_detail_obj.id
            cheque_no = cheque_detail_obj.cheque_no
            cheque_date = cheque_detail_obj.cheque_date.strftime('%d/%m/%Y')
            bank_name = cheque_detail_obj.bank_name
            amount = str(cheque_detail_obj.amount)
            deposit_status = cheque_detail_obj.deposit_status
            if deposit_status == 1:
                print '...........Action taken.....'
                deposit_status = deposit_status
                cheque_remark = "Cheque returned successfully"
                customer_name = cheque_detail_obj.customer_name
                email = cheque_detail_obj.email
                mobile_no = cheque_detail_obj.mobile_no
                date_of_return = cheque_detail_obj.date_of_return.strftime('%d/%m/%Y')
            elif deposit_status == 0:
                deposit_status = deposit_status
                cheque_remark = "Cheque retained at MCCIA"


        except Exception as e:
            print e
            pass

        print '....................',deposit_status
        data = {'success': 'true', 
                'is_deposit_through_cheque' : hall_booking_obj.is_deposit_through_cheque,
                'cheque_detail_id' : cheque_detail_id,
                'cheque_remark' : cheque_remark,
                'cheque_no' :  cheque_no,
                'cheque_date':cheque_date,
                'bank_name':bank_name,
                'amount': amount,
                'customer_name':customer_name,
                'email':email,
                'mobile_no':mobile_no,
                'date_of_return':date_of_return,
                'deposit_status':deposit_status
            }

        print '\nResponse OUT | hall_booking_registration.py | get_cheque_details | User = ', request.user
    except Exception,e:
        print '\nException IN | hall_booking_registration.py | get_cheque_details | User = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')  



@csrf_exempt
@transaction.atomic
def add_cheque_details(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_registration.py | add_cheque_details | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
        hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()
        # total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

        try:
            hall_bookingdeposit_obj = HallBookingDepositDetail.objects.get(hall_booking=hall_booking_obj)
            hall_bookingdeposit_obj.amount = Decimal(request.POST.get('depositCheque_amount'))
            hall_bookingdeposit_obj.cheque_no = request.POST.get('depositCheque_No')
            hall_bookingdeposit_obj.cheque_date = datetime.datetime.strptime(str(request.POST.get('depositCheque_Date')), "%d/%m/%Y")
            hall_bookingdeposit_obj.bank_name = request.POST.get('depositBank_Name')
            hall_bookingdeposit_obj.save()
            
        except Exception as e:
            print e
            hall_bookingdeposit_obj = HallBookingDepositDetail(
                hall_booking = hall_booking_obj,
                amount = Decimal(request.POST.get('depositCheque_amount')),
                cheque_no = request.POST.get('depositCheque_No'),
                cheque_date = datetime.datetime.strptime(str(request.POST.get('depositCheque_Date')), "%d/%m/%Y"),
                bank_name = request.POST.get('depositBank_Name'),
            )
            hall_bookingdeposit_obj.save()
            
        if request.POST.get('checkbox1_flag') == 'true':
            hall_bookingdeposit_obj.customer_name = request.POST.get('custname_Submit')
            hall_bookingdeposit_obj.email = request.POST.get('email_id')
            hall_bookingdeposit_obj.mobile_no = request.POST.get('mobile')
            hall_bookingdeposit_obj.date_of_return = datetime.datetime.strptime(str(request.POST.get('date_of_return')), "%d/%m/%Y")
            hall_bookingdeposit_obj.deposit_status = 1
            hall_bookingdeposit_obj.save()

            hall_booking_obj.deposit = 0
            hall_booking_obj.deposit_status = 1
            hall_booking_obj.save()

        elif request.POST.get('checkbox2_flag') == 'true':
            hall_bookingdeposit_obj.deposit_status = 0
            hall_bookingdeposit_obj.save()

            hall_booking_obj.deposit = hall_bookingdeposit_obj.amount
            hall_booking_obj.deposit_status = 0 
            hall_booking_obj.save()


            if hall_booking_obj.user_track:
                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                user_track_obj.deposit_available = hall_booking_obj.deposit
                user_track_obj.deposit_status = 0
                user_track_obj.refund_status = 0
                user_track_obj.save()

                exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),Q(is_completed = False),~Q(booking_status__in=[0,10])).exclude(id=hall_booking_obj.id)       

                for hall_obj in exclude_hall_booking_list:
                    exclude_hall_obj = HallBooking.objects.get(id=hall_obj.id)
                    
                    if exclude_hall_obj.deposit == 0 and exclude_hall_obj.is_deposit_through_cheque == True:
                        exclude_hall_obj.is_deposit_through_cheque = False
                        exclude_hall_obj.deposit_status = 0
                        exclude_hall_obj.save()
                        HallBookingDepositDetail.objects.filter(hall_booking=exclude_hall_obj).update(is_deleted=True)
                    elif exclude_hall_obj.deposit:

                        exclude_hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj).last()
                        exclude_total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=exclude_hall_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))

                        exclude_hall_obj.deposit = 0
                        exclude_hall_obj.save()
                        exclude_hall_obj.total_payable = round(exclude_hall_obj.total_rent + exclude_hall_obj.deposit + exclude_hall_obj.gst_amount, 0)
                        exclude_hall_obj.save()
                        exclude_hall_payment_obj.payable_amount = Decimal(exclude_hall_obj.total_payable) - Decimal(exclude_total_paid_dict['total_paid'])
                        exclude_hall_payment_obj.save()

        hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
        hall_booking_obj.save()
        # hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
        # hall_payment_obj.save()

        data['success'] = 'true'
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | hall_booking_registration.py | add_cheque_details | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_registration.py | add_cheque_details | User = ', str(
            traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')

#render Proforma Invoice page
def send_booking_proforma_mail_page_render(request):
    try:
        print 'hallbooking | hall_booking_registrations.py | send_booking_proforma_mail_page_render'
        ctx = {}
        booking_info_list = []
        to_receiver_list = []
        cc_receiver_list = []
        temp_cc_receiver_list = []
        booking_id_val = request.GET.get('booking_id')
        hall_booking_obj = HallBooking.objects.get(id=request.GET.get('booking_id'))
        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True,
                                                               is_deleted=False)
        booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).first()
        booking_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).last()
        

        total_paid_by_deposit = 0
        hall_payment_deposit_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj,
                                                                     offline_payment_by=3, is_deleted=False).aggregate(
            total_paid=Sum('paid_amount'))
        if hall_payment_deposit_dict['total_paid']:
            total_paid_by_deposit = Decimal(hall_payment_deposit_dict['total_paid'])
        security_deposit = Decimal(hall_booking_obj.deposit) + total_paid_by_deposit

        if booking_detail_obj.hall_booking.member:
            to_receiver_list.append(str(booking_detail_obj.hall_booking.member.ceo_email))
        to_receiver_list.append(str(booking_detail_obj.email))
        to_receiver_list.append('shubhamshirsode1@gmail.com')

        i = 1
        sb_pi_no = ''
        tilak_pi_no = ''
        bpi_pi_no = ''
        hpi_pi_no = ''

        sb_contact_person = ''
        tilak_contact_person = ''
        bpi_contact_person = ''
        hpi_contact_person = ''
        office_name = ''

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        get_financial = get_financial_year(current_date)

        sub_total = 0
        for item in booking_detail_list:
            j = 1
            hall_location = item.hall_location.location
            if hall_location == 'MCCIA Trade Tower (5th Floor)':
                office_name = 'SB Road Office'
                sb_pi_no = 'PI/' + str(get_financial) + '/' + str(item.pi_no)
                sb_contact_person = item.hall_location.contact_person1.name + ' (SB Road Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
            elif hall_location == 'Tilak Road':
                office_name = 'Tilak Road Office'
                tilak_pi_no = 'TPI/' + str(get_financial) + '/' + str(item.pi_no)
                tilak_contact_person = item.hall_location.contact_person1.name + ' (Tilak Road Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
            elif hall_location == 'Bhosari':
                office_name = 'Bhosari Office'
                bpi_pi_no = 'BPI/' + str(get_financial) + '/' + str(item.pi_no)
                bpi_contact_person = item.hall_location.contact_person1.name + ' (Bhosari Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
            elif hall_location == 'Hadapsar':
                office_name = 'Hadapsar Office'
                hpi_pi_no = 'HPI/' + str(get_financial) + '/' + str(item.pi_no)
                hpi_contact_person = item.hall_location.contact_person1.name + ' (Hadapsar Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no

            facility_info_list = []
            if item.facility_detail:
                facility_detail_list = json.loads(item.facility_detail)
                for facility_obj in facility_detail_list:
                    hour_used = str(facility_obj['hour_used']) + ' Hour Extra'
                    if str(facility_obj['facility_availed']) == 'Extra Hall Hour':
                        hour_used = str(facility_obj['hour_used']) + ' Hour Extra ' + str(
                            item.booking_to_date_for_reference.strftime('%I:%M %p')) + ' - ' + str(
                            item.booking_to_date.strftime('%I:%M %p'))

                    facility_info_list.append({
                        'sr_no': str(i) + '.' + str(j),
                        'facility_name': str(facility_obj['facility_availed']),
                        'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
                        'hour_used': hour_used,
                        'amount': str(facility_obj['amount'])
                    })
                    sub_total = sub_total + float(facility_obj['amount'])
                    j = j + 1

            if int(item.extra_broken_charge):
                facility_info_list.append({
                    'sr_no': str(i) + '.' + str(j),
                    'facility_name': str(item.extra_broken_detail),
                    'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
                    'hour_used': 'NA',
                    'amount': str(item.extra_broken_charge)
                })
                sub_total = sub_total + float(item.extra_broken_charge)

            sub_total = sub_total + float(item.first_total_rent_for_reference)

            booking_info_list.append({
                'sr_no': i,
                'hall_name': str(item.hall_detail.hall_name) + ' (' + office_name + ')',
                'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
                'booking_time': str(item.booking_from_date.strftime('%I:%M %p')) + ' - ' + str(
                    item.booking_to_date_for_reference.strftime('%I:%M %p')),
                'amount': str(item.first_total_rent_for_reference),
                'facility_info_list': facility_info_list
            })
            

        sd_remark = ''
        if not int(security_deposit) and hall_booking_obj.is_deposit_through_cheque:
            sd_remark = '(The cheque towards SD to be paid seperately before the event)'
        else:
            if hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 1:
                sd_remark = '(The cheque towards SD has been returned)'
            elif hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 0:
                sd_remark = '(The cheque amount has been retained at MCCIA)'
            elif hall_booking_obj.user_track:
                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                if int(user_track_obj.deposit_available):
                    sd_remark = '(Retained with MCCIA)'

        sub_discount_total = 0
        discount_got = 0
        discount_per = 0
        if hall_booking_obj.is_discount:
            discount_per = str(int(hall_booking_obj.discount_per)) + '%'

            sub_discount_total = Decimal(hall_booking_obj.discounted_total_rent)
            discount_got = Decimal(sub_total) - Decimal(sub_discount_total)
            half_gst_amount = round(
                (hall_booking_obj.discounted_total_rent * Decimal(hall_booking_obj.gst_tax) / (2 * 100)), 2)
            total_tax = half_gst_amount * 2
            final_total = Decimal(sub_discount_total) + Decimal(security_deposit) + Decimal(total_tax)
            final_total = round(final_total, 0)
        else:
            half_gst_amount = round((hall_booking_obj.total_rent * Decimal(hall_booking_obj.gst_tax) / (2 * 100)), 2)
            total_tax = half_gst_amount * 2
            final_total = Decimal(sub_total) + Decimal(security_deposit) + Decimal(total_tax)
            final_total = round(final_total, 0)

        remaining_amt = 0
        booking_payment_object = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False)

        result = []
        i = 1
        total = 0

        for payment in booking_payment_object:
            record = {}
            payment_mode = ''
            record['sr_no'] = i

            if payment.offline_payment_by == '0':
                payment_mode = "Cheque" + '/' + payment.cheque_no + '/' + payment.bank_name + '/' + str(
                    datetime.strftime(payment.cheque_date, '%d/%m/%Y'))

            elif payment.offline_payment_by == '2':
                payment_mode = " NEFT" + '/' + payment.neft_id

            elif payment.offline_payment_by == '1':
                payment_mode = "Cash" + '/' + payment.cash_no

            elif payment.offline_payment_by == '3':
                payment_mode = "Deposit"

            elif payment.payment_mode == 1:
                payment_mode = "Online" + '/' +  str(
                    datetime.datetime.strftime(payment.payment_date, '%d/%m/%Y'))



            record['payment_mode'] = payment_mode
            record['paid_amount'] = str(payment.paid_amount)
            i=i+1

            result.append(record)

            total = float(payment.paid_amount) + float(total)


        remaining_amt = float(final_total)-float(total)

        ctx = {'sd_remark': sd_remark, 'discount_got': discount_got, 'discount_per': discount_per,
               'sub_discount_total': sub_discount_total, 'hpi_contact_person': hpi_contact_person,
               'bpi_contact_person': bpi_contact_person, 'sb_contact_person': sb_contact_person,
               'tilak_contact_person': tilak_contact_person, 'final_total': format(final_total, '.2f'),
               'security_deposit': format(security_deposit, '.2f'), 'total_tax': format(total_tax, '.2f'),
               'sub_total': format(sub_total, '.2f'), 'sb_pi_no': sb_pi_no, 'tilak_pi_no': tilak_pi_no,
               'bpi_pi_no': bpi_pi_no, 'hpi_pi_no': hpi_pi_no, 'hall_booking_obj': hall_booking_obj,
               'booking_detail_obj': booking_detail_obj, 'booking_id' : booking_id_val,
               'result' : result,'remaining_amt' : str(remaining_amt),'total':str(total),
               'booking_info_list': booking_info_list, 'half_gst_amount': format(half_gst_amount, '.2f'),
               'booking_payment_obj': booking_payment_obj, 
               'date': str(datetime.datetime.strftime(datetime.datetime.today(), '%d.%m.%Y'))}

        return render(request, 'hallbooking/customer_booking_mail.html',ctx)
    except Exception, e:
        print '\nException IN | hall_booking_confirm.py | send_booking_invoice_mail | EXCP = ', str(
            traceback.print_exc())


def edit_booking_proforma_mail_page_render(request):
    try:
        print 'hallbooking | hall_booking_registrations.py | edit_booking_proforma_mail_page_render'
        ctx = {}
        booking_info_list = []
        to_receiver_list = []
        cc_receiver_list = []
        temp_cc_receiver_list = []
        booking_id_val = request.GET.get('booking_id')
        hall_booking_obj = HallBooking.objects.get(id=request.GET.get('booking_id'))
        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True,
                                                               is_deleted=False)
        booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).first()
        booking_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).last()
        

        total_paid_by_deposit = 0
        hall_payment_deposit_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj,
                                                                     offline_payment_by=3, is_deleted=False).aggregate(
            total_paid=Sum('paid_amount'))
        if hall_payment_deposit_dict['total_paid']:
            total_paid_by_deposit = Decimal(hall_payment_deposit_dict['total_paid'])
        security_deposit = Decimal(hall_booking_obj.deposit) + total_paid_by_deposit

        if booking_detail_obj.hall_booking.member:
            to_receiver_list.append(str(booking_detail_obj.hall_booking.member.ceo_email))
        to_receiver_list.append(str(booking_detail_obj.email))
        to_receiver_list.append('shubhamshirsode1@gmail.com')

        i = 1
        sb_pi_no = ''
        tilak_pi_no = ''
        bpi_pi_no = ''
        hpi_pi_no = ''

        sb_contact_person = ''
        tilak_contact_person = ''
        bpi_contact_person = ''
        hpi_contact_person = ''
        office_name = ''

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        get_financial = get_financial_year(current_date)

        sub_total = 0
        for item in booking_detail_list:
            j = 1
            hall_location = item.hall_location.location
            if hall_location == 'MCCIA Trade Tower (5th Floor)':
                office_name = 'SB Road Office'
                sb_pi_no = 'PI/' + str(get_financial) + '/' + str(item.pi_no)
                sb_contact_person = item.hall_location.contact_person1.name + ' (SB Road Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
            elif hall_location == 'Tilak Road':
                office_name = 'Tilak Road Office'
                tilak_pi_no = 'TPI/' + str(get_financial) + '/' + str(item.pi_no)
                tilak_contact_person = item.hall_location.contact_person1.name + ' (Tilak Road Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
            elif hall_location == 'Bhosari':
                office_name = 'Bhosari Office'
                bpi_pi_no = 'BPI/' + str(get_financial) + '/' + str(item.pi_no)
                bpi_contact_person = item.hall_location.contact_person1.name + ' (Bhosari Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no
            elif hall_location == 'Hadapsar':
                office_name = 'Hadapsar Office'
                hpi_pi_no = 'HPI/' + str(get_financial) + '/' + str(item.pi_no)
                hpi_contact_person = item.hall_location.contact_person1.name + ' (Hadapsar Office) ' + ' ' + item.hall_location.contact_person1.email + ' ' + item.hall_location.contact_person1.contact_no

            facility_info_list = []
            if item.facility_detail:
                facility_detail_list = json.loads(item.facility_detail)
                for facility_obj in facility_detail_list:
                    hour_used = str(facility_obj['hour_used']) + ' Hour Extra'
                    if str(facility_obj['facility_availed']) == 'Extra Hall Hour':
                        hour_used = str(facility_obj['hour_used']) + ' Hour Extra ' + str(
                            item.booking_to_date_for_reference.strftime('%I:%M %p')) + ' - ' + str(
                            item.booking_to_date.strftime('%I:%M %p'))

                    facility_info_list.append({
                        'sr_no': str(i) + '.' + str(j),
                        'facility_name': str(facility_obj['facility_availed']),
                        'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
                        'hour_used': hour_used,
                        'amount': str(facility_obj['amount'])
                    })
                    sub_total = sub_total + float(facility_obj['amount'])
                    j = j + 1

            if int(item.extra_broken_charge):
                facility_info_list.append({
                    'sr_no': str(i) + '.' + str(j),
                    'facility_name': str(item.extra_broken_detail),
                    'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
                    'hour_used': 'NA',
                    'amount': str(item.extra_broken_charge)
                })
                sub_total = sub_total + float(item.extra_broken_charge)

            sub_total = sub_total + float(item.first_total_rent_for_reference)

            booking_info_list.append({
                'sr_no': i,
                'hall_name': str(item.hall_detail.hall_name) + ' (' + office_name + ')',
                'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
                'booking_time': str(item.booking_from_date.strftime('%I:%M %p')) + ' - ' + str(
                    item.booking_to_date_for_reference.strftime('%I:%M %p')),
                'amount': str(item.first_total_rent_for_reference),
                'facility_info_list': facility_info_list
            })
            

        sd_remark = ''
        if not int(security_deposit) and hall_booking_obj.is_deposit_through_cheque:
            sd_remark = '(The cheque towards SD to be paid seperately before the event)'
        else:
            if hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 1:
                sd_remark = '(The cheque towards SD has been returned)'
            elif hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 0:
                sd_remark = '(The cheque amount has been retained at MCCIA)'
            elif hall_booking_obj.user_track:
                user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                if int(user_track_obj.deposit_available):
                    sd_remark = '(Retained with MCCIA)'

        sub_discount_total = 0
        discount_got = 0
        discount_per = 0
        if hall_booking_obj.is_discount:
            discount_per = str(int(hall_booking_obj.discount_per)) + '%'

            sub_discount_total = Decimal(hall_booking_obj.discounted_total_rent)
            discount_got = Decimal(sub_total) - Decimal(sub_discount_total)
            half_gst_amount = round(
                (hall_booking_obj.discounted_total_rent * Decimal(hall_booking_obj.gst_tax) / (2 * 100)), 2)
            total_tax = half_gst_amount * 2
            final_total = Decimal(sub_discount_total) + Decimal(security_deposit) + Decimal(total_tax)
            final_total = round(final_total, 0)
        else:
            half_gst_amount = round((hall_booking_obj.total_rent * Decimal(hall_booking_obj.gst_tax) / (2 * 100)), 2)
            total_tax = half_gst_amount * 2
            final_total = Decimal(sub_total) + Decimal(security_deposit) + Decimal(total_tax)
            final_total = round(final_total, 0)

        remaining_amt = 0
        booking_payment_object = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False)

        result = []
        i = 1
        total = 0

        for payment in booking_payment_object:
            record = {}
            payment_mode = ''
            record['sr_no'] = i

            if payment.offline_payment_by == '0':
                payment_mode = "Cheque" + '/' + payment.cheque_no + '/' + payment.bank_name + '/' + str(
                    datetime.strftime(payment.cheque_date, '%d/%m/%Y'))

            elif payment.offline_payment_by == '2':
                payment_mode = " NEFT" + '/' + payment.neft_id

            elif payment.offline_payment_by == '1':
                payment_mode = "Cash" + '/' + payment.cash_no

            elif payment.offline_payment_by == '3':
                payment_mode = "Deposit"

            elif payment.payment_mode == 1:
                payment_mode = "Online" + '/' +  str(
                    datetime.datetime.strftime(payment.payment_date, '%d/%m/%Y'))



            record['payment_mode'] = payment_mode
            record['paid_amount'] = str(payment.paid_amount)
            i=i+1

            result.append(record)

            total = float(payment.paid_amount) + float(total)


        remaining_amt = float(final_total)-float(total)

        ctx = {'sd_remark': sd_remark, 'discount_got': discount_got, 'discount_per': discount_per,
               'sub_discount_total': sub_discount_total, 'hpi_contact_person': hpi_contact_person,
               'bpi_contact_person': bpi_contact_person, 'sb_contact_person': sb_contact_person,
               'tilak_contact_person': tilak_contact_person, 'final_total': format(final_total, '.2f'),
               'security_deposit': format(security_deposit, '.2f'), 'total_tax': format(total_tax, '.2f'),
               'sub_total': format(sub_total, '.2f'), 'sb_pi_no': sb_pi_no, 'tilak_pi_no': tilak_pi_no,
               'bpi_pi_no': bpi_pi_no, 'hpi_pi_no': hpi_pi_no, 'hall_booking_obj': hall_booking_obj,
               'booking_detail_obj': booking_detail_obj, 'booking_id' : booking_id_val,
               'result' : result,'remaining_amt' : str(remaining_amt),'total':str(total),
               'booking_info_list': booking_info_list, 'half_gst_amount': format(half_gst_amount, '.2f'),
               'booking_payment_obj': booking_payment_obj, 
               'date': str(datetime.datetime.strftime(datetime.datetime.today(), '%d.%m.%Y'))}

        return render(request, 'hallbooking/edit_booking_mail.html',ctx)
    except Exception, e:
        print '\nException IN | hall_booking_confirm.py | edit_booking_proforma_mail_page_render | EXCP = ', str(
            traceback.print_exc())

# function take input of the datestring like 2018-10-15
def get_financial_year(datestring):
    date = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
    # initialize the current year
    year_of_date = date.year
    # initialize the current financial year start date
    financial_year_start_date = datetime.datetime.strptime(str(year_of_date) + "-04-01", "%Y-%m-%d").date()
    if date < financial_year_start_date:
        return str(financial_year_start_date.year - 1)[2:] + '-' + str(financial_year_start_date.year)[2:]
    else:
        return str(financial_year_start_date.year)[2:] + '-' + str(financial_year_start_date.year + 1)[2:]



# Admin Sends Proforma Invoice Mail After Updating Deposit
def send_booking_proforma_mail(request):
    data = {}
    try:
        print '\nRequest IN | hall_booking_registration.py | send_booking_proforma_mail | '
        ctx = {}
        booking_info_list = []
        to_receiver_list = []
        cc_receiver_list = []
        temp_cc_receiver_list = []

        hall_booking_obj = HallBooking.objects.get(id=request.GET.get('booking_id'))
        final_total = request.GET.get('final_total')
        # booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True)
        # booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).first()
        # booking_payment_obj = HallPaymentDetail.objects.get(hall_booking=hall_booking_obj)
        send_mail_count = "UPDATED"
        send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
        send_booking_invoice_mail_locationvise(request, hall_booking_obj)

        # if booking_detail_obj.hall_booking.member:
        #     to_receiver_list.append(str(booking_detail_obj.hall_booking.member.ceo_email))
        # to_receiver_list.append(str(booking_detail_obj.email))

        # i = 1
        # for item in booking_detail_list:
        #     booking_info_list.append({
        #         'sr_no': i,
        #         'hall_name': str(item.hall_detail.hall_name),
        #         'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
        #         'booking_time': str(item.booking_from_date.strftime('%I:%M %p')) + ' - ' + str(item.booking_to_date.strftime('%I:%M %p')),
        #         'extra_hours': 0,
        #         'amount': str(item.total_rent)
        #     })
        #     cc_receiver_list.append(str(item.hall_detail.hall_location.contact_person1.email))
        #     i = i + 1

        # # cc_receiver_list.append('maheshk@mcciapune.com')
        # cc_receiver_list.append('shubham.bharti@bynry.com')

        # temp_cc_receiver_list = set(cc_receiver_list)
        # cc_receiver_list = list(temp_cc_receiver_list)

        # half_gst_amount = round((hall_booking_obj.total_rent * Decimal(0.09)), 2)

        # ctx = {'hall_booking_obj': hall_booking_obj, 'booking_detail_obj': booking_detail_obj,
        #        'booking_info_list': booking_info_list, 'half_gst_amount': half_gst_amount,
        #        'booking_payment_obj': booking_payment_obj,
        #        'date': str(datetime.datetime.strftime(datetime.datetime.today(), '%d.%m.%Y'))}

        # imgpath = os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        # fp = open(imgpath, 'rb')
        # msgImage = MIMEImage(fp.read())
        # fp.close()
        # msgImage.add_header('Content-ID', '<img1>')
        # username = "membership@mcciapune.com"
        # pswd = "mem@2011ship"

        # html = get_template('hallbooking/hall_bkng_invoice.html').render(Context(ctx))
        # htmlfile = MIMEText(html, 'html', _charset=charset)
        # msg = MIMEMultipart('related')
        # msg.attach(htmlfile)
        # msg.attach(msgImage)

        # server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        # server.ehlo()
        # server.starttls()
        # server.login(username, pswd)

        # TO = to_receiver_list
        # CC = cc_receiver_list

        # msg['subject'] = 'Updated Booking Mail - MCCIA'
        # msg['from'] = 'mailto: <membership@mcciapune.com>'
        # msg['to'] = ",".join(TO)
        # msg['cc'] = ",".join(CC)
        # toaddrs = TO + CC

        # server.sendmail(msg['from'], toaddrs, msg.as_string())
        # server.quit()
        data['success'] = 'true'
        print '\nResponse OUT | hall_booking_registration.py | send_booking_proforma_mail | INVOICE MAIL SENT'
    except Exception,e:
        print '\nException IN | hall_booking_registration.py | send_booking_proforma_mail | EXCP = ', str(traceback.print_exc())
        data['success'] = 'false'
    return HttpResponse(json.dumps(data), content_type='application/json')



import json
def update_booking_proforma_mail(request):
    data = {}
    try:
        print '\nRequest IN | hall_booking_registration.py | update_booking_proforma_mail | '
        hall_booking_obj = HallBooking.objects.get(id=request.GET.get('booking_id'))
        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True,
                                                               is_deleted=False)
        booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).first()
        booking_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).last()
        discount_value_got = request.GET.get('discount_got')
        total_sub_amount = request.GET.get('sub_total')
        if discount_value_got:
            amount_after_discount = Decimal(total_sub_amount) - Decimal(discount_value_got)
            hall_booking_obj.name = request.GET.get('name')
            hall_booking_obj.discounted_total_rent = amount_after_discount
            hall_booking_obj.discount = request.GET.get('discount_got')
            hall_booking_obj.save()
        else:
            hall_booking_obj.name = request.GET.get('name')
            hall_booking_obj.save()

        booking_detail_obj.address = str(request.GET.get('address'))
        booking_detail_obj.save()
        booking_detail_obj.contact_person = request.GET.get('contact_person')
        booking_detail_obj.email = request.GET.get('email')
        booking_detail_obj.save()

        if request.GET.get('mobile_no') != None:
            contact_no = request.GET.get('mobile_no')
            booking_detail_obj.mobile_no = contact_no
        if request.GET.get('tel_o') != None:
            contact_no = request.GET.get('tel_o')
            booking_detail_obj.tel_o = contact_no
        if request.GET.get('tel_r') != None:
            contact_no = request.GET.get('tel_r')
            booking_detail_obj.tel_r = contact_no
        booking_detail_obj.save()
        hall_booking_obj.invoice_total_rent = request.GET.get('final_total')
        hall_booking_obj.save()
        data = {'success' : 'true'}
    except Exception,e:
        print '\nException IN | hall_booking_registration.py | update_booking_proforma_mail | EXCP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')



import json
@csrf_exempt
def get_hall_booking_details(request):
    data = {}
    try:
        print '\nRequest IN | hall_booking_registration.py | get_hall_booking_details | User = ', request.user
        print request.POST.get('booking_detail_id')


        output_list = []
        hall_equipment_list = []

        facility_list = []
        equipment_name_list = []
        check_extra_hour_flag = 0
        check_extra_pre_hour_flag = 0
        booking_detail_obj = HallBookingDetail.objects.get(id=request.POST.get('booking_detail_id'))
        booking_from_date = booking_detail_obj.booking_from_date.date()
        if booking_from_date in [obj.holiday_date for obj in Holiday.objects.filter(status=True, is_deleted=False, holiday_status=False)]:
            holiday_factor = Decimal(booking_detail_obj.hall_location.hall_rent_on_holiday)
        elif (booking_from_date.weekday() == 5 and (8 <= booking_from_date.day <= 14 or 22 <= booking_from_date.day <= 28)) or (booking_from_date.weekday() == 6):
            holiday_factor = Decimal(booking_detail_obj.hall_location.hall_rent_on_holiday)
        else:
            holiday_factor = Decimal(1)
        if booking_detail_obj.facility_detail:
            facility_detail_list = json.loads(booking_detail_obj.facility_detail)
            for obj1 in facility_detail_list:
                equipment_name_list.append(str(obj1['facility_availed'])) 
                if str(obj1['facility_availed']) == 'Extra Hall Post Hour':
                    check_extra_hour_flag = 1

                if str(obj1['facility_availed']) == 'Extra Hall Pre Hour':
                    check_extra_pre_hour_flag = 1

                facility_list.append({'facility_name':str(obj1['facility_availed']), 'hour_used':str(obj1['hour_used']), 'facility_rate':str(obj1['rate']), 'amount':str(obj1['amount']), 'discount_per':str(obj1['discount']), 'net_amount':str(obj1['net_amount'])})


        hall_booking_obj = HallBooking.objects.get(id=booking_detail_obj.hall_booking.id)

        discount_per = str(hall_booking_obj.discount_per)
        hall_facility_objs_list = HallEquipment.objects.filter(hall_detail=booking_detail_obj.hall_detail.id, member_charges__gt= 0, non_member_charges__gt= 0)
        hall_facility_objs_list = HallEquipment.objects.filter(hall_detail=booking_detail_obj.hall_detail.id, member_charges__gt= 0, non_member_charges__gt= 0).exclude(hall_functioning_equipment__equipment_name__in = equipment_name_list)
        if hall_booking_obj.member:
            extra_hall_price = str(booking_detail_obj.hall_detail.extra_member_price)
            for obj in hall_facility_objs_list:
                member_charges = format(round(holiday_factor * obj.member_charges, 2), '.2f')
                facility_list.append({'facility_name':obj.hall_functioning_equipment.equipment_name, 'hour_used':0, 'facility_rate':str(member_charges), 'amount':0, 'discount':discount_per, 'net_amount':0})
        else:
            extra_hall_price = str(booking_detail_obj.hall_detail.extra_nonmember_price)
            # facility_list = [{'facility_id':obj.id,'facility_name':obj.hall_functioning_equipment.equipment_name,'facility_rate':str(obj.non_member_charges), 'discount_per':discount_per} for obj in hall_facility_objs_list]
            for obj in hall_facility_objs_list:
                non_member_charges = format(round(holiday_factor * obj.non_member_charges, 2), '.2f')
                facility_list.append({'facility_name':obj.hall_functioning_equipment.equipment_name, 'hour_used':0, 'facility_rate':str(non_member_charges), 'amount':0, 'discount_per':discount_per, 'net_amount':0})
        if booking_detail_obj.updated_by:   
            booking_from_time = str(booking_detail_obj.booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p'))#str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))
            booking_to_time = str(booking_detail_obj.booking_to_date.astimezone(to_zone).time().strftime('%I:%M %p'))# booking_detail_obj.booking_to_date.strftime('%I:%M %p')

        else:    
            booking_from_time = str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))#str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))
            booking_to_time = str(booking_detail_obj.booking_to_date.strftime('%I:%M %p'))# booking_detail_obj.booking_to_date.strftime('%I:%M %p')

        extra_hall_amount = booking_detail_obj.extra_hour * Decimal(extra_hall_price)
        data = {'success': 'true', 
                'hall_name' : booking_detail_obj.hall_detail.hall_name,
                'company_name' : booking_detail_obj.hall_booking.name,
                'event_nature' : booking_detail_obj.event_nature,
                'event_date' :  booking_detail_obj.booking_from_date.strftime('%a %d, %b %Y'),
                'booking_from_time':booking_from_time,
                'booking_to_time':booking_to_time,
                'extra_hall_price': format(round(holiday_factor * Decimal(extra_hall_price), 2), '.2f'),
                'discount_per':discount_per,
                'facility_list':facility_list,
                'check_extra_hour_flag':check_extra_hour_flag,
                'check_extra_pre_hour_flag':check_extra_pre_hour_flag,
                'extra_broken_detail':booking_detail_obj.extra_broken_detail if booking_detail_obj.extra_broken_charge != 0 else '',
                'extra_broken_charge':str(booking_detail_obj.extra_broken_charge)
            }

        print '\nResponse OUT | hall_booking_registration.py | get_hall_booking_details | User = ', request.user
    except Exception,e:
        print '\nException IN | hall_booking_registration.py | get_hall_booking_details | User = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')  


# Open Hall Booking Edit Page
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Bookings Registrations'],login_url='/backofficeapp/login/',raise_exception=True)
def open_extra_booking(request, booking_id):
    data = {}
    data_dict = {}
    try:
        print '\nRequest IN | hall_booking_registration.py | open_extra_booking | User = ', request.user, booking_id

        bookingobj = HallBooking.objects.get(id=booking_id)
        cancel_list_count = HallBookingDetail.objects.filter(hall_booking=bookingobj, is_cancelled=False).count()
        booking_values = HallBookingDetail.objects.filter(hall_booking=bookingobj).values_list(
            'booking_detail_no').distinct()
        final_data = []
        for booking_value in booking_values:
            booking_detail_objs = HallBookingDetail.objects.filter(hall_booking=bookingobj,
                                                                   booking_detail_no=booking_value[0])
            cancel_booking_count = HallBookingDetail.objects.filter(hall_booking=bookingobj, booking_detail_no=booking_value[0],
                                                            is_cancelled=True).values('is_cancelled')\
                                                            .annotate(cancel_count=Count('is_cancelled'))
            booking_detail_list = []
            booking_detail_cancel_list = []
            booking_flow_data = {}
            for booking_detail_obj in booking_detail_objs:
                flag = True
                if cancel_booking_count and (booking_detail_objs.count() == int(cancel_booking_count[0]['cancel_count'])):
                    flag = False
                if booking_detail_obj.is_active or flag is False:
                    data = {}
                    data['detail_id'] = booking_detail_obj.id
                    if booking_detail_obj.updated_by:
                        data['booking_from_time'] = str(booking_detail_obj.booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p'))  # str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))
                        data['booking_to_time'] = str(booking_detail_obj.booking_to_date.astimezone(to_zone).time().strftime('%I:%M %p'))  # booking_detail_obj.booking_to_date.strftime('%I:%M %p')
                    else:
                        data['booking_from_time'] = str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))  # str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))
                        data['booking_to_time'] = str(booking_detail_obj.booking_to_date.strftime('%I:%M %p'))  # booking_detail_obj.booking_to_date.strftime('%I:%M %p')
                    data['booking_date'] = booking_detail_obj.booking_from_date.strftime('%a %d, %b %Y')
                    data['rent'] = str(booking_detail_obj.total_rent)
                    data['extra_hour'] = str(booking_detail_obj.extra_hour)
                    data['check_flag'] = flag
                    data['facility_flag'] = 0
                    if booking_detail_obj.extra_hour_charge != 0 or booking_detail_obj.total_facility_charge != 0:
                        data['facility_flag'] = 1

                    booking_detail_list.append(data)
                if booking_detail_obj.is_cancelled:
                    # print '*******booking_from_date**1****',booking_detail_obj.booking_from_date
                    # print '******booking_to_date**1*****',booking_detail_obj.booking_to_date
                    booking_from_date = booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
                    booking_to_date = booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
                    # # data['booking_from_time'] = booking_detail_obj.booking_from_date 
                    # # data['booking_to_time'] = booking_detail_obj.booking_to_date 
                    # print '*******booking_from_date******',booking_from_date
                    # print '******booking_to_date*******',booking_to_date
                    data['booking_from_time'] = str(booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p'))  # str(booking_detail_obj.booking_from_date.strftime('%I:%M %p'))
                    data['booking_to_time'] = str(booking_to_date.astimezone(to_zone).time().strftime('%I:%M %p'))  # booking_detail_obj.booking_to_date.strftime('%I:%M %p')
                    
                    booking_detail_cancel_list.append(data)
                    booking_detail_cancel_list.append({
                        'cancel_booking_date': booking_detail_obj.booking_from_date.strftime('%a %d, %b %Y'),
                        'cancel_booking_from_time': str(booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p')) if booking_detail_obj.updated_by else str(booking_from_date.strftime('%I:%M %p')),
                        'cancel_booking_to_time': str(booking_to_date.astimezone(to_zone).time().strftime('%I:%M %p')) if booking_detail_obj.updated_by else str(booking_to_date.strftime('%I:%M %p')),
                        'cancel_date': booking_detail_obj.cancellation_date.strftime('%a %d, %b %Y'),
                        'cancellation_charges': str(booking_detail_obj.cancellation_amount)
                    })
            # booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date + timedelta(hours=5, minutes=30)
            # booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date +  timedelta(hours=5, minutes=30)
            # booking_detail_obj.save()

            booking_detail_obj = booking_detail_objs.last()

            booking_flow_data['contact_person'] = booking_detail_obj.contact_person
            booking_flow_data['company_name'] = str(bookingobj.name)
            booking_flow_data['address'] = booking_detail_obj.address
            booking_flow_data['email'] = booking_detail_obj.email
            booking_flow_data['mobile_no'] = booking_detail_obj.mobile_no
            booking_flow_data['event_nature'] = booking_detail_obj.event_nature
            booking_flow_data['hall_name'] = booking_detail_obj.hall_detail.hall_name
            booking_flow_data['booking_detail'] = booking_detail_list
            booking_flow_data['cancel_booking_detail'] = booking_detail_cancel_list
            booking_flow_data['booking_no'] = bookingobj.booking_no
            final_data.append(booking_flow_data)

        data_dict = {'data': final_data, 'booking_obj': bookingobj, 'cancel_list_count': cancel_list_count}
        print '\nResponse OUT | hall_booking_registration.py | open_extra_booking | User = ', request.user
    except Exception, e:
        print '\nException IN | hall_booking_registration.py | open_extra_booking | User = ', str(traceback.print_exc())
    return render(request, 'backoffice/hall_booking/open_extra_booking.html', data_dict)
    

# @csrf_exempt
# @transaction.atomic
# def add_extra_hour_details(request):
#     sid = transaction.savepoint()
#     data = {}
#     try:
#         print '\nRequest IN | hall_booking_registration.py | add_extra_hour_details | User = ', request.user
#         print request.POST.get('booking_detail_id')

#         gstObj = Servicetax.objects.get(tax_type=0,is_active=True)

#         if request.POST.get('facility_list'): 
#             facility_list = (request.POST.get('facility_list')).split(',')
#             hour_used_list = (request.POST.get('hour_used_list')).split(',')
#             rate_list = (request.POST.get('rate_list')).split(',')
#             amount_list = (request.POST.get('amount_list')).split(',')
#             discount_list = (request.POST.get('discount_list')).split(',')
#             net_amount_list = (request.POST.get('net_amount_list')).split(',')

#             length_count=len(facility_list)

#             final_facility_list = []
#             extra_hall_time = 0
#             extra_hall_net_amount = 0
#             for obj in range(0, length_count):
#                 if hour_used_list[obj] not in ['','0']:
#                     if facility_list[obj] == 'Extra Hall Hour':
#                         extra_hall_time = Decimal(hour_used_list[obj])
#                         extra_hall_net_amount = Decimal(net_amount_list[obj])

#                     final_facility_list.append({'facility_availed':str(facility_list[obj]),'hour_used':str(hour_used_list[obj]),'rate':str(rate_list[obj]),'amount':str(amount_list[obj]),'discount':str(discount_list[obj]),'net_amount':str(net_amount_list[obj])})
#             net_amount = 0

#             for obj in final_facility_list:
#                 if obj['facility_availed'] != 'Extra Hall Hour':
#                     net_amount = net_amount + Decimal(obj['net_amount'])


#             booking_detail_obj = HallBookingDetail.objects.get(id=request.POST.get('booking_detail_id'))
#             hall_booking_obj = HallBooking.objects.get(id=booking_detail_obj.hall_booking.id)
#             hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()

#             # changes in Hall booking detail for toatl rent
#             booking_detail_obj.extra_hour = extra_hall_time
#             booking_detail_obj.extra_hour_charge = extra_hall_net_amount
#             booking_detail_obj.facility_detail = json.dumps(final_facility_list)
#             booking_detail_obj.total_facility_charge = net_amount
#             booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + extra_hall_net_amount + net_amount
#             booking_detail_obj.save()
#             booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax))  / 100
#             booking_detail_obj.save()
#             booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))         
#             booking_detail_obj.save()

#             # Change booking to date in HallCheckAvailability
#             hall_check_avail = HallCheckAvailability.objects.get(hall_booking_detail=booking_detail_obj)
#             hall_check_avail.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))
#             hall_check_avail.save()
    

#             extra_charges_dict = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).aggregate(hour_sum=Sum('extra_hour_charge'),facility_sum = Sum('total_facility_charge'),hour_count=Sum('extra_hour'))
#             # Changes in HAll booking table for total rent
#             hall_booking_obj.total_rent = hall_booking_obj.first_total_rent_for_reference + Decimal(extra_charges_dict['hour_sum']) + Decimal(extra_charges_dict['facility_sum']) 
#             hall_booking_obj.save()
#             hall_booking_obj.gst_amount = (Decimal(hall_booking_obj.total_rent) * Decimal(gstObj.tax))  / 100
#             hall_booking_obj.save()

#             total_paid_by_deposit = 0
#             hall_payment_deposit_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj,offline_payment_by=3, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))
#             if hall_payment_deposit_dict['total_paid']:
#                 total_paid_by_deposit =  Decimal(hall_payment_deposit_dict['total_paid'])
#             final_deposit = Decimal(hall_booking_obj.deposit) + total_paid_by_deposit

#             hall_booking_obj.total_payable = hall_booking_obj.total_rent + final_deposit + hall_booking_obj.gst_amount
#             hall_booking_obj.save()
#             hall_booking_obj.extra_hour = Decimal(extra_charges_dict['hour_count'])
#             hall_booking_obj.extra_hour_charge = Decimal(extra_charges_dict['hour_sum'])
#             hall_booking_obj.total_facility_charge = Decimal(extra_charges_dict['facility_sum'])            
#             hall_booking_obj.save()

#             # To make final changes in discounted_total_rent as per discount (If any)
#             if hall_booking_obj.is_discount:
#                 discount_percent = hall_booking_obj.discount_per
#                 final_total_rent = Decimal(hall_booking_obj.total_rent) - (Decimal(extra_charges_dict['hour_sum']) + Decimal(extra_charges_dict['facility_sum'])) # first_total_rent_for_reference -(Extra facility/ Hour charges)
#                 total_discount = (Decimal(discount_percent)/100)*(final_total_rent)
#                 total_discount= round(Decimal(total_discount),2)
#                 discounted_total_rent = Decimal(hall_booking_obj.total_rent) - Decimal(total_discount)
#                 hall_booking_obj.discounted_total_rent = discounted_total_rent
#                 hall_booking_obj.save()
#                 hall_booking_obj.gst_amount = (Decimal(hall_booking_obj.discounted_total_rent) * Decimal(gstObj.tax))  / 100
#                 hall_booking_obj.save()
#                 hall_booking_obj.total_payable = hall_booking_obj.discounted_total_rent + final_deposit + hall_booking_obj.gst_amount
#                 hall_booking_obj.discount = Decimal(total_discount)
#                 hall_booking_obj.save()


#             total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))
#             if hall_payment_obj.payment_status == 1:
#                 payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
#                 if payable_amount:
#                     hall_booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj,
#                                                          payable_amount=payable_amount,
#                                                          created_by=str(request.user)
#                                                          )

#                     hall_booking_obj.payment_status = 8
#                     hall_booking_obj.save()

#                     hall_booking_payment_obj.save()
#             else:
#                 hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
#                 hall_payment_obj.save()

#             if final_facility_list:
#                 booking_detail_history_obj = BookingDetailHistory(
#                     hall_booking_detail = booking_detail_obj,
#                     total_rent = booking_detail_obj.total_rent,
#                     discount_percent = hall_booking_obj.discount_per,
#                     extra_hour = extra_hall_time,
#                     extra_hour_charge = extra_hall_net_amount,
#                     facility_detail = final_facility_list,
#                     total_facility_charge = net_amount,
#                     created_by = str(request.user),
#                     updated_by = str(request.user)
#                 )
#                 booking_detail_history_obj.save()

#             transaction.savepoint_commit(sid)        
#         data = {'success': 'true', 'total_rent': str(round(hall_booking_obj.total_rent, 2)),
#                 'gst_amount': str(round(hall_booking_obj.gst_amount, 2)),
#                 'total_payable': str(round(hall_booking_obj.total_payable, 2)),
#                 'booking_detail_id': request.POST.get('booking_id')}

#         print '\nResponse OUT | hall_booking_registration.py | add_extra_hour_details | User = ', request.user
#     except Exception,e:
#         print '\nException IN | hall_booking_registration.py | add_extra_hour_details | User = ', str(traceback.print_exc())
#         data = {'success': 'false'}
#         transaction.rollback(sid)
#     return HttpResponse(json.dumps(data), content_type='application/json')   



@csrf_exempt
@transaction.atomic
def add_extra_hour_details(request):
    sid = transaction.savepoint()
    # pdb.set_trace()
    data = {}
    to_zone = tz.gettz("Asia/Kolkata")
    try:
        print '\nRequest IN | hall_booking_registration.py | add_extra_hour_details | User = ', request.user
        
        print request.POST.get('start_time_val')
       
        gstObj = Servicetax.objects.get(tax_type=0,is_active=True)

        if request.POST.get('facility_list'): 
            facility_list = (request.POST.get('facility_list')).split(',')
            hour_used_list = (request.POST.get('hour_used_list')).split(',')
            rate_list = (request.POST.get('rate_list')).split(',')
            amount_list = (request.POST.get('amount_list')).split(',')
            discount_list = (request.POST.get('discount_list')).split(',')
            net_amount_list = (request.POST.get('net_amount_list')).split(',')

            length_count=len(facility_list)

            final_facility_list = []
            extra_hall_time = 0
            extra_pre_hall_time = 0
            extra_hall_net_amount = 0
            extra_hall_pre_net_amount = 0
            extra_hall_post_net_amount = 0
            extra_broken_detail = ''
            extra_broken_charge = 0            
            for obj in range(0, length_count):
                if hour_used_list[obj] not in ['','0']:
                    if facility_list[obj] == 'Extra Hall Pre Hour':
                        extra_pre_hall_time = Decimal(hour_used_list[obj])
                        extra_hall_pre_net_amount = Decimal(net_amount_list[obj])

                    if facility_list[obj] == 'Extra Hall Post Hour':
                        extra_hall_time = Decimal(hour_used_list[obj])
                        extra_hall_post_net_amount = Decimal(net_amount_list[obj])

                    extra_hall_net_amount = extra_hall_pre_net_amount + extra_hall_post_net_amount

                    if hour_used_list[obj] == 'NA':
                        extra_broken_detail = str(facility_list[obj])
                        extra_broken_charge = Decimal(net_amount_list[obj])                    

                    if hour_used_list[obj] != 'NA':
                        final_facility_list.append({'facility_availed':str(facility_list[obj]),'hour_used':str(hour_used_list[obj]),'rate':str(rate_list[obj]),'amount':str(amount_list[obj]),'discount':str(discount_list[obj]),'net_amount':str(net_amount_list[obj])})
           
            net_amount = 0
            for obj in final_facility_list:
                if obj['facility_availed'] != 'Extra Hall Pre Hour' or obj['facility_availed'] != 'Extra Hall Post Hour':
                    net_amount = net_amount + Decimal(obj['net_amount'])

                
            booking_detail_obj = HallBookingDetail.objects.get(id=request.POST.get('booking_detail_id'))
            hall_booking_obj = HallBooking.objects.get(id=booking_detail_obj.hall_booking.id)
            hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()
            # changes in Hall booking detail for toatl rent
            booking_detail_obj.extra_pre_hour = extra_pre_hall_time
            booking_detail_obj.extra_hour_charge = extra_hall_net_amount
            booking_detail_obj.extra_broken_detail = extra_broken_detail
            booking_detail_obj.extra_broken_charge = extra_broken_charge
            booking_detail_obj.facility_detail = json.dumps(final_facility_list)
            booking_detail_obj.total_facility_charge = net_amount


            # Change booking to date in HallCheckAvailability
            for item in HallCheckAvailability.objects.filter(hall_booking_detail=booking_detail_obj):
                temp_time = booking_detail_obj.booking_to_date_for_reference - timedelta(hours=5, minutes=30)
                temp_pre_time = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=5, minutes=30)
                booking_from_time_val = temp_pre_time - timedelta(hours=int(extra_pre_hall_time)) 
                booking_to_time_val = temp_time + timedelta(hours=int(extra_hall_time)) 
                result_list = check_availability(extra_pre_hall_time,extra_hall_time,booking_to_time_val, booking_from_time_val, booking_detail_obj,temp_time,temp_pre_time)
                print '---------------result_list----------------',result_list
                if result_list[0] != []:
                    if result_list[0][0] == 0 or result_list[0][1] == 0:
                        data = {'success': 'booking_time'}
                        return HttpResponse(json.dumps(data), content_type='application/json') 
                else:
                    item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                    item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                    item.save()
                    booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                    booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                    booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                    booking_detail_obj.save()
                    booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                    booking_detail_obj.save()
                    booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                    booking_detail_obj.save()


                if result_list[0] != [] or result_list[1] != []:
                    flag = 1
                    if 'pre not avail' in result_list[1] or 'post not avail' in result_list[1]:
                        if 'post not avail' in result_list[1]:
                            if result_list[1].count('post avail') > 1:
                                item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                item.save()
                                booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                booking_detail_obj.save()
                                booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                booking_detail_obj.save()
                                booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                booking_detail_obj.save()
                            else:
                                print '------------3'
                                if 'not add' in result_list[2]:
                                    if all_same(result_list[1]):
                                        data = {'success': 'not_available'}
                                        return HttpResponse(json.dumps(data), content_type='application/json')
                                    else:
                                        item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                        item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                        item.save()
                                        booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                        booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                        booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                        booking_detail_obj.save()
                                        booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                        booking_detail_obj.save()
                                        booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                        booking_detail_obj.save()
                                else:
                                    item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                    item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                    item.save()
                                    booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                    booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                    booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                    booking_detail_obj.save()
                                    booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                    booking_detail_obj.save()
                                    booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                    booking_detail_obj.save()

                        elif 'pre not avail' in result_list[1]:
                            if result_list[1].count('pre avail') > 1:
                                item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                item.save()
                                booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                booking_detail_obj.save()
                                booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                booking_detail_obj.save()
                                booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                booking_detail_obj.save()
                            else:
                                print '------------5'
                                if all_same(result_list[0]):
                                    item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                    item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                    item.save()
                                    booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                    booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                    booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                    booking_detail_obj.save()
                                    booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                    booking_detail_obj.save()
                                    booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                    booking_detail_obj.save()
                                else:
                                    if 'pre avail' in result_list[1]:
                                        item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                        item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                        item.save()
                                        booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                        booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                        booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                        booking_detail_obj.save()
                                        booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                        booking_detail_obj.save()
                                        booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                        booking_detail_obj.save()
                                    else:
                                        data = {'success': 'not_available'}
                                        return HttpResponse(json.dumps(data), content_type='application/json')

                        else:
                            if result_list[3] != []:
                                if 'pre not avail' in result_list[1]:
                                    if all_same(result_list[1]):
                                        data = {'success': 'not_available'}
                                        return HttpResponse(json.dumps(data), content_type='application/json')
                                    else:
                                        print '----------------pre add'
                                        flag = 1
                                        item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                        item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                        item.save()
                                        booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                        booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                        booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                        booking_detail_obj.save()
                                        booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                        booking_detail_obj.save()
                                        booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                        booking_detail_obj.save()
                            else:
                                print '---------------89'
                                if 'pre not avail' in result_list[1]:
                                    if result_list[1].count('pre avail') > 1:
                                        print '-----------4'
                                        item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                        item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                        item.save()
                                        booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                        booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                        booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                        booking_detail_obj.save()
                                        booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                        booking_detail_obj.save()
                                        booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                        booking_detail_obj.save()
                                    else:
                                        print '------------5'
                                        if result_list[3] != []:
                                            data = {'success': 'not_available'}
                                            return HttpResponse(json.dumps(data), content_type='application/json')
                                        else:                                 
                                            if 'pre not avail' in result_list[1]:
                                                data = {'success': 'not_available'}
                                                return HttpResponse(json.dumps(data), content_type='application/json')
                                            else:
                                                item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                                item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                                item.save()
                                                booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                                booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                                booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                                booking_detail_obj.save()
                                                booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                                booking_detail_obj.save()
                                                booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                                booking_detail_obj.save()
                                else:
                                    data = {'success': 'not_available'}
                                    return HttpResponse(json.dumps(data), content_type='application/json')
                            
                    else:
                        if 'both side post not avail' in result_list[1]:
                            if result_list[1][-1] == 'both side post avail' and result_list[1][0] == 'both side pre avail':
                                item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                item.save()
                                booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                booking_detail_obj.save()
                                booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                booking_detail_obj.save()
                                booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                booking_detail_obj.save()
                            elif result_list[1][0] == 'both side pre avail' and result_list[1][2] == 'both side pre avail':
                                item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                                item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                                item.save()
                                booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                                booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                                booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                                booking_detail_obj.save()
                                booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                                booking_detail_obj.save()
                                booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                                booking_detail_obj.save()
                            # elif result_list[1][0] == 'both side not pre avail' and result_list[1][1] == 'both side post not avail':
                            #     item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                            #     item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                            #     item.save()
                            #     booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                            #     booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                            #     booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                            #     booking_detail_obj.save()
                            #     booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                            #     booking_detail_obj.save()
                            #     booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                            #     booking_detail_obj.save()
                            else:
                                print '--------------------else'
                                data = {'success': 'not_available'}
                                return HttpResponse(json.dumps(data), content_type='application/json')
                        else:
                            item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                            item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                            item.save()
                            booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                            booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                            booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                            booking_detail_obj.save()
                            booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                            booking_detail_obj.save()
                            booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                            booking_detail_obj.save()
                else:
                    print '-------for 0---------'
                    item.booking_to_date = temp_time + timedelta(hours=int(extra_hall_time))
                    item.booking_from_date = temp_pre_time - timedelta(hours=int(extra_pre_hall_time))
                    item.save()
                    booking_detail_obj.extra_hour = extra_hall_time + extra_pre_hall_time
                    booking_detail_obj.booking_to_date = booking_detail_obj.booking_to_date_for_reference + timedelta(hours=int(extra_hall_time))       
                    booking_detail_obj.booking_from_date = booking_detail_obj.booking_from_date_for_reference - timedelta(hours=int(extra_pre_hall_time))                    
                    booking_detail_obj.save()
                    booking_detail_obj.total_rent = booking_detail_obj.first_total_rent_for_reference + net_amount + extra_broken_charge
                    booking_detail_obj.save()
                    booking_detail_obj.gst_amount = (Decimal(booking_detail_obj.total_rent) * Decimal(gstObj.tax)) / 100
                    booking_detail_obj.save()     
                
            extra_charges_dict = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).aggregate(hour_sum=Sum('extra_hour_charge'),broken_sum=Sum('extra_broken_charge'),facility_sum = Sum('total_facility_charge'),hour_count=Sum('extra_hour'))
            # Changes in HAll booking table for total rent
            # if extra_charges_dict['hour_sum'] != 0.00 and extra_charges_dict['facility_sum'] != 0.00:
            # hall_booking_obj.total_rent = hall_booking_obj.first_total_rent_for_reference + Decimal(extra_charges_dict['hour_sum']) + Decimal(extra_charges_dict['facility_sum'])  + Decimal(extra_charges_dict['broken_sum']) 
            
            if extra_charges_dict['facility_sum']:
               hall_booking_obj.total_rent = hall_booking_obj.first_total_rent_for_reference + Decimal(extra_charges_dict['facility_sum'])  + Decimal(extra_charges_dict['broken_sum']) 
            else:
                hall_booking_obj.total_rent = hall_booking_obj.first_total_rent_for_reference + Decimal(extra_charges_dict['hour_sum'])  + Decimal(extra_charges_dict['broken_sum']) 
            
            hall_booking_obj.save()
            hall_booking_obj.gst_amount = (Decimal(hall_booking_obj.total_rent) * Decimal(gstObj.tax))  / 100
            hall_booking_obj.save()

            total_paid_by_deposit = 0
            hall_payment_deposit_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj,offline_payment_by=3, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))
            if hall_payment_deposit_dict['total_paid']:
                total_paid_by_deposit =  Decimal(hall_payment_deposit_dict['total_paid'])
            final_deposit = Decimal(hall_booking_obj.deposit) + total_paid_by_deposit

            hall_booking_obj.total_payable = hall_booking_obj.total_rent + final_deposit + hall_booking_obj.gst_amount
            hall_booking_obj.save()
            hall_booking_obj.extra_hour = Decimal(extra_charges_dict['hour_count'])
            hall_booking_obj.extra_hour_charge = Decimal(extra_charges_dict['hour_sum'])
            hall_booking_obj.total_facility_charge = Decimal(extra_charges_dict['facility_sum'])            
            hall_booking_obj.extra_broken_charge = Decimal(extra_charges_dict['broken_sum'])            
            hall_booking_obj.save()

            # To make final changes in discounted_total_rent as per discount (If any)
            if hall_booking_obj.is_discount:
                discount_percent = hall_booking_obj.discount_per
                final_total_rent = Decimal(hall_booking_obj.total_rent) - (Decimal(extra_charges_dict['hour_sum']) + Decimal(extra_charges_dict['facility_sum']) + Decimal(extra_charges_dict['broken_sum'])) # first_total_rent_for_reference -(Extra facility/ Hour charges)
                total_discount = (Decimal(discount_percent)/100)*(final_total_rent)
                total_discount= round(Decimal(total_discount),2)
                discounted_total_rent = Decimal(hall_booking_obj.total_rent) - Decimal(total_discount)
                hall_booking_obj.discounted_total_rent = discounted_total_rent
                hall_booking_obj.save()
                hall_booking_obj.gst_amount = (Decimal(hall_booking_obj.discounted_total_rent) * Decimal(gstObj.tax))  / 100
                hall_booking_obj.save()
                hall_booking_obj.total_payable = hall_booking_obj.discounted_total_rent + final_deposit + hall_booking_obj.gst_amount
                hall_booking_obj.discount = Decimal(total_discount)
                hall_booking_obj.save()


            total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted = False).aggregate(total_paid=Sum('paid_amount'))
            if hall_payment_obj.payment_status == 1:
                payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
                if payable_amount:
                    hall_booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj,
                                                         payable_amount=payable_amount,
                                                         created_by=str(request.user)
                                                         )

                    hall_booking_obj.payment_status = 8
                    hall_booking_obj.save()

                    hall_booking_payment_obj.save()
            else:
                hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
                hall_payment_obj.save()

            if final_facility_list:
                booking_detail_history_obj = BookingDetailHistory(
                    hall_booking_detail = booking_detail_obj,
                    total_rent = booking_detail_obj.total_rent,
                    discount_percent = hall_booking_obj.discount_per,
                    extra_hour = extra_hall_time,
                    extra_pre_hour = extra_pre_hall_time,
                    extra_hour_charge = extra_hall_net_amount,
                    extra_broken_charge = extra_broken_charge,
                    facility_detail = final_facility_list,
                    total_facility_charge = net_amount,
                    created_by = str(request.user),
                    updated_by = str(request.user)
                )
                booking_detail_history_obj.save()

            transaction.savepoint_commit(sid)                    

        data = {'success': 'true', 'total_rent': str(round(hall_booking_obj.total_rent, 2)),
                'gst_amount': str(round(hall_booking_obj.gst_amount, 2)),
                'total_payable': str(round(hall_booking_obj.total_payable, 2)),
                'booking_detail_id': request.POST.get('booking_id')}

        print '\nResponse OUT | hall_booking_registration.py | add_extra_hour_details | User = ', request.user
    except Exception,e:
        print '\nException IN | hall_booking_registration.py | add_extra_hour_details | User = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')        


def all_same(items):
    return all(x == items[0] for x in items)

def check_availability(extra_pre_hall_time,extra_hall_time,booking_to_time_val, booking_from_time_val, booking_detail_obj,temp_time_main,temp_pre_time_main):
    slot_not_avail_list = []
    temp_list = []
    temp_both_list = []
    temp_pre_list = []
    temp_post_list = []
    temp_list_pre = []
    temp_list_post = []
    start_time_flag = 0
    flag = 9
    pre_flag = 5
    final_flag = 7
    final_flag_pre = 10
    flag1 = True
    actual_time = True
    pre_post_pre_flag = True
    pre_flag = True
    post_flag = True
    booking_from_time_val = booking_from_time_val + timedelta(hours=5, minutes=30)
    booking_to_time_val = booking_to_time_val  + timedelta(hours=5, minutes=30)
    booking_from_time = booking_from_time_val.time()
    booking_from_date = booking_from_time_val.date()
    booking_to_time = booking_to_time_val.time()
    booking_to_date = booking_to_time_val.date()
    start_time = '07:00 AM'
    end_time = '11:00 PM'
    end_time12 = '12:00 PM'
    main_start_time = datetime.datetime.strptime(start_time, "%I:%M %p").time()
    main_end_time = datetime.datetime.strptime(end_time, "%I:%M %p").time()
    main_end_time12 = datetime.datetime.strptime(end_time12, "%I:%M %p").time()
    if booking_detail_obj:
        hall_booking_from_list = HallCheckAvailability.objects.filter(hall_detail=booking_detail_obj.hall_detail,
                                                                              booking_from_date__icontains=booking_from_date)
        hall_booking_to_list = HallCheckAvailability.objects.filter(hall_detail=booking_detail_obj.hall_detail,
                                                                            booking_to_date__icontains=booking_from_date)
    hall_booking_from_list = hall_booking_from_list.exclude(booking_status__in=[0, 10])
    hall_booking_to_list = hall_booking_to_list.exclude(booking_status__in=[0, 10])
    count = hall_booking_from_list.count()
    if hall_booking_from_list:
        last_obj = hall_booking_from_list.last()
        last_time= last_obj.booking_to_date + timedelta(hours = 1)
        last_from_time= last_obj.booking_from_date - timedelta(hours = 1)
        last_to_time = last_time.astimezone(to_zone).time()
        last_from_time = last_from_time.astimezone(to_zone).time()

    for hall_booking_from in hall_booking_from_list:
        booking_from_date = hall_booking_from.booking_from_date - timedelta(hours = 1)
        booking_to_date = hall_booking_from.booking_to_date + timedelta(hours = 1)
        booking_from_date_time = booking_from_date.astimezone(to_zone).time() 
        booking_to_date_time = booking_to_date.astimezone(to_zone).time()
        
        if (main_start_time < booking_from_time):
            start_time_flag = 1
            temp_list.append(start_time_flag)
        else:
            start_time_flag = 0
            temp_list.append(start_time_flag)
        
        if (main_end_time > booking_to_time):
            start_time_flag = 1
            temp_list.append(start_time_flag)
        else:
            start_time_flag = 0
            temp_list.append(start_time_flag)

        if (main_end_time12 > booking_to_time):
            start_time_flag = 1
            temp_list.append(start_time_flag)
        else:
            start_time_flag = 0
            temp_list.append(start_time_flag)

        if count == 1:
            if(extra_pre_hall_time != 0 and extra_hall_time != 0):
                if(booking_to_date_time >= booking_from_time):
                    pre_post_pre_flag = 'both side pre avail'
                else:
                    pre_post_pre_flag = 'both side not pre avail'

                if(booking_from_date_time <= booking_to_time):
                    pre_post_post_flag = 'both side post avail'
                else:
                    pre_post_post_flag = 'both side post not avail'
                temp_both_list.append(pre_post_pre_flag)
                temp_both_list.append(pre_post_post_flag)

            elif extra_pre_hall_time != 0:
                if(booking_from_time >= booking_to_date_time):
                    pre_flag = 'pre avail'
                else:
                    pre_flag = 'pre not avail'
                temp_pre_list.append(pre_flag)

            elif extra_hall_time != 0:
                if(booking_to_time <= booking_from_date_time):
                    post_flag = 'post avail'
                else:
                    post_flag = 'post not avail'
                temp_post_list.append(post_flag)
                if(last_to_time <= booking_to_time):
                    flag = 'add'
                else:
                    flag = 'not add'
                temp_list_pre.append(flag)
        else:
            if(extra_pre_hall_time != 0 and extra_hall_time != 0):
                if(booking_to_date_time <= booking_from_time):
                    pre_post_pre_flag = 'both side pre avail'
                else:
                    pre_post_pre_flag = 'both side not pre avail'

                if(booking_from_date_time >= booking_to_time):
                    pre_post_post_flag = 'both side post avail'
                else:
                    pre_post_post_flag = 'both side post not avail'
                temp_both_list.append(pre_post_pre_flag)
                temp_both_list.append(pre_post_post_flag)

            elif extra_pre_hall_time != 0:
                if(booking_from_time >= booking_to_date_time):
                    pre_flag = 'pre avail'
                else:
                    pre_flag = 'pre not avail'
                temp_pre_list.append(pre_flag)

            elif extra_hall_time != 0:
                if(booking_to_time <= booking_from_date_time):
                    post_flag = 'post avail'
                else:
                    post_flag = 'post not avail'
                temp_post_list.append(post_flag)
                if(last_to_time <= booking_to_time):
                    flag = 'add'
                else:
                    flag = 'not add'
                temp_list_pre.append(flag)

        # if(booking_to_time <= booking_from_date_time or booking_to_time >= booking_to_date_time):
        #     flag1 = True
        #     temp_list_post.append(flag1)
            
        # else:
        #     flag1 = False
        #     temp_list_post.append(flag1)

        # if (booking_from_time <= booking_to_date_time):
        #     pre_flag = 5
        #     temp_list_pre.append(pre_flag)
        # else:
        #     pre_flag = 6
        #     temp_list_pre.append(pre_flag)

        # booking_from_date1 = hall_booking_from.booking_from_date
        # booking_to_date1 = hall_booking_from.booking_to_date 
        # booking_from_date_time1 = booking_from_date1.astimezone(to_zone).time() 
        # booking_to_date_time1 = booking_to_date1.astimezone(to_zone).time()
        
        # if(booking_to_time  == booking_from_date_time1 ):
        #     final_flag = 8
        # if(booking_from_time  == booking_to_date_time1):
        #     final_flag_pre = 9

    # return temp_list,temp_list_pre,temp_list_post,final_flag,final_flag_pre
                # if all_same(temp_list_pre):
    # if all_same(temp_list_pre) and all_same(temp_post_list):
    #     return temp_list,temp_list_pre,temp_post_list
    if temp_pre_list:
        return temp_list,temp_pre_list
    elif temp_post_list:
        return temp_list,temp_post_list,temp_list_pre
    else:
        return temp_list,temp_both_list



@csrf_exempt
def send_link_for_online_payment(request):
    data = {}
    try:
        print '\nRequest IN | hall_booking_registration.py | send_link_for_online_payment | User = ', request.user
        booking_id = request.POST.get('booking_id')
        hallbookingobjectdetails = HallBookingDetail.objects.get(hall_booking__id=request.POST.get('booking_id'))
        total_amount_to_pay = request.POST.get('online_amount')
        tds_amount_new = request.POST.get('TDS_amount')
        if tds_amount_new:
            tds_amount_hall_booking = tds_amount_new
        else:
            tds_amount_hall_booking = 0


        activation_url = "/backofficeapp/pay-payment-online-link/{}/{}".format(booking_id,tds_amount_hall_booking)
        activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)
        print activate_url

        context = {'booking_id': booking_id, 'total_amount_to_pay':total_amount_to_pay,'activate_url':activate_url}

        to_list = []
        gmail_user = "hallbkg_mtt@mcciapune.com"
        gmail_pwd = "hallbkg@2011mtt"

        to_list.append(str(hallbookingobjectdetails.email))

        msg = MIMEMultipart('related')

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        TO = to_list
        CC = ['vijendra.chandel@bynry.com','maheshk@mcciapune.com']

        html_content = render_to_string('hallbooking/payment_later.html', context)
        htmlfile = MIMEText(html_content, 'html', _charset=charset)
        msg.attach(htmlfile)

        msg['subject'] = 'Online Payment Link - Hallbooking'

        msg['from'] = 'mailto: <hallbkg_mtt@mcciapune.com>'
        msg['to'] = ",".join(TO)
        msg['cc'] = ",".join(CC)


        toaddrs = TO + CC
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()

        data['success'] = 'true'
        print '\nResponse OUT | hall_booking_registration.py | send_link_for_online_payment | User = ', request.user

    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_registration.py | send_link_for_online_payment | User = ', str(
        traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def pay_payment_online_link(request,booking_id,tds_amount_hall_booking):
    hallbooking_object = HallBooking.objects.get(id=booking_id)
    paymentobject = HallPaymentDetail.objects.filter(hall_booking=booking_id).last()

    customer_name = hallbooking_object.name
    paid_amount_count = paymentobject.payable_amount - paymentobject.paid_amount - hallbooking_object.deposit - int(tds_amount_hall_booking)

    context = {'booking_id': booking_id, 'paid_amount_count': paid_amount_count,'customer_name':customer_name,'tds_amount_hall_booking':tds_amount_hall_booking}

    if paid_amount_count <= 0.0:
        return render(request, 'hallbooking/already_paid_online.html')
    else:
        return render_to_response('hallbooking/pay_payment_link.html',context,context_instance=RequestContext(request))



