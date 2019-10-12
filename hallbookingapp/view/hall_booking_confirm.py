import json
import smtplib
import traceback
import pdb
import os
from django.template import Context
from django.template.loader import render_to_string, get_template
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dateutil import tz
from decimal import Decimal
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, timedelta
import dateutil.parser
from math import ceil
from django.db.models import Count, Sum, Q, F

from adminapp.models import Servicetax
from Paymentapp.models import PaymentTransaction, PendingTransaction
from hallbookingapp.models import Hallbooking_company_detail, HallDetail, \
    HallPricing, Holiday, HallCheckAvailability, HallBooking, HallBookingDetail, HallEquipment, HallPaymentDetail, \
    UserTrackDetail
from membershipapp.models import UserDetail
from adminapp.view import constant
from backofficeapp.models import SystemUserProfile
from MCCIA import settings
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

hours = {'1': '13', '2': '14', '3': '15', '4': '16', '5': '17', '6': '18', '7': '19',
         '8': '20', '9': '21', '10': '22', '11': '23', '12': '12'}

charset = 'utf-8'


@csrf_exempt
def hall_booking_confirm(request, booking_id):
    """
    Code for redirecting on confirm booking page and Hallbooking details as a putput data
    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.HallBookingDetail`.

    **Template:**

    :template:`hallbooking/hall_booking_confirm.html`
    """
    data = {}
    data_dict = {}
    try:
        bookingobj = HallBooking.objects.get(id=booking_id)
        hall_payment_obj_list = HallPaymentDetail.objects.filter(hall_booking=bookingobj, is_deleted=False)
        if hall_payment_obj_list:
            return HttpResponseForbidden()

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
                print booking_detail_obj.booking_from_date.strftime('%I %P')
                print booking_detail_obj.booking_from_date
                data['detail_id'] = booking_detail_obj.id
                data['booking_from_time'] = booking_detail_obj.booking_from_date.strftime('%I:%M %P')
                data['booking_to_time'] = booking_detail_obj.booking_to_date.strftime('%I:%M %P')
                data['booking_date'] = booking_detail_obj.booking_from_date.strftime('%a %d, %b %Y')
                data['rent'] = str(booking_detail_obj.total_rent)
                booking_detail_list.append(data)
            company_name = str(bookingobj.name)
            booking_detail_obj = booking_detail_objs.last()
            booking_flow_data['contact_person'] = booking_detail_obj.contact_person
            booking_flow_data['company_name'] = str(bookingobj.name)
            booking_flow_data['address'] = booking_detail_obj.address
            booking_flow_data['email'] = booking_detail_obj.email
            booking_flow_data['mobile_no'] = booking_detail_obj.mobile_no
            booking_flow_data['event_nature'] = booking_detail_obj.event_nature
            booking_flow_data['hall_name'] = booking_detail_obj.hall_detail.hall_name
            booking_flow_data['booking_detail'] = booking_detail_list
            booking_flow_data['deposit_for_online'] = int(booking_detail_obj.hall_booking.deposit)
            booking_flow_data['online_payable_amount'] = booking_detail_obj.hall_booking.total_payable - booking_detail_obj.hall_booking.deposit

            final_data.append(booking_flow_data)
            # final_data.append(booking_flow_data)

        data_dict = {'data': final_data, 'booking_obj': bookingobj, 'deposit_for_online' :booking_flow_data['deposit_for_online'],'online_payable_amount':booking_flow_data['online_payable_amount'], 'company_name':company_name}
    except Exception, e:
        print e
        print 'Exception | hall_booking_confirm.py | hall_booking_confirm | ', str(traceback.print_exc())
    return render(request, 'hallbooking/hall_booking_confirm.html', data_dict)


@csrf_exempt
def remove_hall_booking(request):
    """
    Code for redirecting on confirm booking page and Hallbooking details as a putput data
    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.HallBookingDetail`.

    **Template:**

    :template:`hallbooking/hall_booking_confirm.html`
    """
    data = {}
    try:
        print '\nRequest IN | hall_booking_confirm.py | remove_hall_booking | User = ', request.user
        print request.POST.get('booking_id')
        booking_detail_obj = HallBookingDetail.objects.get(id=request.POST.get('booking_id'))
        hall_booking_obj = HallBooking.objects.get(id=booking_detail_obj.hall_booking.id)
        hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()
        booking_detail_obj.is_active = False
        booking_detail_obj.booking_status = 0
        booking_detail_obj.total_facility_charge = 0
        booking_detail_obj.save()

        try:
            gstObj = Servicetax.objects.get(tax_type=0, is_active=True)

            hall_booking_obj.total_rent = hall_booking_obj.total_rent - booking_detail_obj.total_rent
            hall_booking_obj.first_total_rent_for_reference = hall_booking_obj.first_total_rent_for_reference - booking_detail_obj.total_rent
            hall_booking_obj.save()
            hall_booking_obj.gst_amount = (Decimal(hall_booking_obj.total_rent) * Decimal(gstObj.tax)) / 100
            hall_booking_obj.save()
            # hall_booking_obj.total_payable = hall_booking_obj.total_rent + constant.HALL_DEPOSIT + hall_booking_obj.gst_amount
            hall_booking_obj.total_payable = hall_booking_obj.total_rent + Decimal(
                hall_booking_obj.deposit) + hall_booking_obj.gst_amount
            hall_booking_obj.save()

            if hall_payment_obj:
                hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
                hall_payment_obj.save()

        except Exception, e:
            print '\nException IN remove_hall_booking Calculation = ', str(traceback.print_exc())
            pass

        data = {'success': 'true', 'total_rent': str(round(hall_booking_obj.total_rent, 2)),
                'gst_amount': str(round(hall_booking_obj.gst_amount, 2)),
                'total_payable': str(round(hall_booking_obj.total_payable, 2)),
                'booking_detail_id': request.POST.get('booking_id')}

        print '\nResponse OUT | hall_booking_confirm.py | remove_hall_booking | User = ', request.user
    except Exception, e:
        print '\nException IN | hall_booking_confirm.py | remove_hall_booking | User = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Calculate Total Hall Rent & Return
def get_total_hall_rent(week_day, minutes, hall_detail_obj, flag):
    # pdb.set_trace()
    data = {}
    slot = 2
    total_rent = 0
    total_hour = int(ceil(Decimal(minutes) / Decimal(60)))
    extra_hour = 0
    try:
        print '\nRequest IN | hall_booking_confirm.py | get_total_hall_rent'

        if total_hour >= 8:
            slot = 8
            extra_hour = total_hour - 8
            hall_pricing_obj = HallPricing.objects.get(hall_detail=hall_detail_obj,
                                                       hours=8, is_active=True, is_deleted=False)
        elif total_hour >= 4:
            slot = 4
            extra_hour = total_hour - 4
            hall_pricing_obj = HallPricing.objects.get(hall_detail=hall_detail_obj,
                                                       hours=4, is_active=True, is_deleted=False)
        elif total_hour >= 2:
            slot = 2
            extra_hour = total_hour - 2
            hall_pricing_obj = HallPricing.objects.get(hall_detail=hall_detail_obj,
                                                       hours=2, is_active=True, is_deleted=False)
        else:
            hall_pricing_obj = HallPricing.objects.get(hall_detail=hall_detail_obj,
                                                       hours=2, is_active=True, is_deleted=False)
        if flag:
            if week_day in ['0', '6']:
                if str(hall_detail_obj.hall_location.location).strip() == 'Hadapsar':
                    total_rent = round(
                        hall_pricing_obj.member_price * hall_detail_obj.hall_location.hall_rent_on_holiday, -2)
                    total_rent = round((total_rent + (round(
                        hall_detail_obj.extra_member_price * hall_detail_obj.hall_location.hall_rent_on_holiday,
                        -2) * extra_hour)), 0)
                else:
                    total_rent = round(
                        hall_pricing_obj.member_price * hall_detail_obj.hall_location.hall_rent_on_holiday, 0)
                    total_rent = round((total_rent + (round(
                        hall_detail_obj.extra_member_price * hall_detail_obj.hall_location.hall_rent_on_holiday,
                        0) * extra_hour)), 0)
            else:
                total_rent = round(hall_pricing_obj.member_price + (hall_detail_obj.extra_member_price * extra_hour), 0)
        else:
            if week_day in ['0', '6']:
                if str(hall_detail_obj.hall_location.location).strip() == 'Hadapsar':
                    total_rent = round(
                        hall_pricing_obj.nonmember_price * hall_detail_obj.hall_location.hall_rent_on_holiday, -2)
                    total_rent = round((total_rent + (round(
                        hall_detail_obj.extra_nonmember_price * hall_detail_obj.hall_location.hall_rent_on_holiday,
                        -2) * extra_hour)), 0)
                else:
                    total_rent = round(
                        hall_pricing_obj.nonmember_price * hall_detail_obj.hall_location.hall_rent_on_holiday, 0)
                    total_rent = round((total_rent + (round(
                        hall_detail_obj.extra_nonmember_price * hall_detail_obj.hall_location.hall_rent_on_holiday,
                        0) * extra_hour)), 0)
            else:
                total_rent = round(
                    hall_pricing_obj.nonmember_price + (hall_detail_obj.extra_nonmember_price * extra_hour), 0)

        # total_rent = hall_pricing_obj.nonmember_price + (hall_detail_obj.extra_nonmember_price * extra_hour)
        # if week_day in ['0', '6']:
        #     if str(hall_detail_obj.hall_location.location).strip() == 'Hadapsar':
        #         total_rent = round(int(total_rent * hall_detail_obj.hall_location.hall_rent_on_holiday), -2)
        #     elif str(hall_detail_obj.hall_location.location).strip() == 'Bhosari':
        #         total_rent = round(total_rent, 0)
        #     else:
        #         total_rent = round(total_rent * hall_detail_obj.hall_location.hall_rent_on_holiday, 0)

        data['total_rent'] = total_rent
        data['slot'] = slot
        data['member_price'] = hall_pricing_obj.member_price
        data['nonmember_price'] = hall_pricing_obj.nonmember_price
        data['extra_member_price'] = hall_detail_obj.extra_member_price
        data['extra_nonmember_price'] = hall_detail_obj.extra_nonmember_price

        print '\nResponse OUT | hall_booking_confirm.py | get_total_hall_rent '
    except Exception, e:
        print '\nException | hall_booking_confirm.py | get_total_hall_rent | ', str(traceback.print_exc())
    return data


@csrf_exempt
@transaction.atomic
def save_booking(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_confirm.py | save_booking | User = ', request.user
        print request.POST.get('data_list')
        data_list_dict = json.loads(request.POST.get('data_list'))
        print '\n\nDD = ', data_list_dict

        date_period_list = []
        date_list = []
        from_to_date_list = []
        company_name = ''

        for i in data_list_dict:
            for k, v in i.iteritems():
                if k == 'date_list':
                    date_list = v.getlist()
            # print date_list
        from_hour_list = request.POST.getlist('from_hour_list')
        to_hour_list = request.POST.getlist('to_hour_list')
        from_minute_list = request.POST.getlist('from_minute_list')
        to_minute_list = request.POST.getlist('to_minute_list')
        from_period = request.POST.getlist('from_period_list')
        to_period = request.POST.getlist('to_period_list')

        print date_list, from_hour_list, to_hour_list, from_minute_list, to_minute_list, from_period, to_period

        date_list = request.POST.get('date_list').split(",")
        from_hour_list = request.POST.get('from_hour_list').split(",")
        to_hour_list = request.POST.get('to_hour_list').split(",")
        from_minute_list = request.POST.get('from_minute_list').split(",")
        to_minute_list = request.POST.get('to_minute_list').split(",")
        from_period = request.POST.get('from_period_list').split(",")
        to_period = request.POST.get('to_period_list').split(",")

        user_detail_id = request.POST.get('user_detail_id')
        print user_detail_id

        length = len(date_list)

        # pdb.set_trace()
        hall_obj = HallDetail.objects.get(id=request.POST.get('hall_id'))

        hall_pricing_obj = HallPricing.objects.filter(hall_detail=hall_obj).last()

        if user_detail_id != 'None':
            user_detail_obj = UserDetail.objects.get(id=user_detail_id)
            company_name = str(user_detail_obj.company.company_name)
        else:
            company_name = str(request.POST.get('company_name'))

        # Append Date
        for d in date_list:
            from_zone = tz.tzutc()
            to_zone = tz.gettz('Asia/Kolkata')
            utc_date = dateutil.parser.parse(str(d))
            utc_date = utc_date.replace(tzinfo=from_zone)
            local_date = utc_date.astimezone(to_zone)

            date_period_list.append(local_date.date())

        date_period_list.sort()

        # Append Date Time
        for i in range(0, length):
            from_zone = tz.tzutc()
            to_zone = tz.gettz('Asia/Kolkata')
            utc_date = dateutil.parser.parse(str(date_list[i]))
            utc_date = utc_date.replace(tzinfo=from_zone)
            local_date = utc_date.astimezone(to_zone)

            local_from_time = ''
            local_to_time = ''

            if from_period[i] == "PM":
                local_from_time = time(int(from_hour_list[i]) + 12, int(from_minute_list[i]))
            else:
                if int(from_hour_list[i]) == 12:
                    local_from_time = time(int(00), int(from_minute_list[i]))
                else:
                    local_from_time = time(int(from_hour_list[i]), int(from_minute_list[i]))
            if to_period[i] == "PM":
                local_to_time = time(int(to_hour_list[i]) + 12, int(to_minute_list[i]))
            else:
                if int(to_hour_list[i]) == 12:
                    local_to_time = time(int(00), int(to_minute_list[i]))
                else:
                    local_to_time = time(int(to_hour_list[i]), int(to_minute_list[i]))

            from_time = datetime.strptime(str(local_from_time), '%H:%M:%S')
            to_time = datetime.strptime(str(local_to_time), '%H:%M:%S')
            f_time = datetime.strftime(from_time, '%H,%M')
            t_time = datetime.strftime(to_time, '%H,%M')
            f_time = datetime.strptime(f_time, '%H,%M').time()
            t_time = datetime.strptime(t_time, '%H,%M').time()

            from_date_time = datetime.combine(local_date.date(), f_time)
            to_date_time = datetime.combine(local_date.date(), t_time)

            from_to_date_list.append(from_date_time)
            from_to_date_list.append(to_date_time)

        date_time_dict = {}
        for i in from_to_date_list:
            date_time_dict.setdefault((i.date()), []).append(i.time())

        if len(date_period_list) == 1:
            company_detail_obj = Hallbooking_company_detail(
                company_individual_name=company_name,
                address=str(request.POST.get('address')),
                contact_person=str(request.POST.get('contact_person')),
                designation=str(request.POST.get('designation')),
                mobile_no=str(request.POST.get('mobile_no')), tel_r=str(request.POST.get('contact_detail_tel_r')),
                tel_o=str(request.POST.get('contact_detail_tel_o')), email=str(request.POST.get('email_id')),
                event_nature=str(request.POST.get('event_nature')), deposit=str(request.POST.get('deposit')),
                payment_method=str(request.POST.get('payment_method')),
                total_payable=str(request.POST.get('total_payable')),
                total_rent=str(request.POST.get('total_hall_rent')), gst=str(request.POST.get('gst')),
                from_date=date_period_list[0], to_date=date_period_list[0]
            )

            company_detail_obj.save()
        else:
            company_detail_obj = Hallbooking_company_detail(
                company_individual_name=company_name,
                address=str(request.POST.get('address')),
                contact_person=str(request.POST.get('contact_person')),
                designation=str(request.POST.get('designation')),
                mobile_no=str(request.POST.get('mobile_no')), tel_r=str(request.POST.get('contact_detail_tel_r')),
                tel_o=str(request.POST.get('contact_detail_tel_o')), email=str(request.POST.get('email_id')),
                event_nature=str(request.POST.get('event_nature')), deposit=str(request.POST.get('deposit')),
                payment_method=str(request.POST.get('payment_method')),
                total_payable=str(request.POST.get('total_payable')),
                total_rent=str(request.POST.get('total_hall_rent')), gst=str(request.POST.get('gst')),
                from_date=date_period_list[0], to_date=date_period_list[1]
            )

            company_detail_obj.save()

        if user_detail_id != 'None':
            user_detail_obj = UserDetail.objects.get(id=request.POST.get('user_detail_id'))
            company_detail_obj.member = user_detail_obj
            company_detail_obj.save()

        for key, value in date_time_dict.iteritems():
            hall_booking_detail_obj = Hall_booking_detail(
                booking_from_date=datetime.combine(key, value[0]),
                booking_to_date=datetime.combine(key, value[1]),
                hall_detail=hall_obj, hall_pricing=hall_pricing_obj,
                Hallbooking_company_detail=company_detail_obj
            )
            hall_booking_detail_obj.save()

        transaction.savepoint_commit(sid)
        print '\nResponse OUT | hall_booking_confirm.py | save_booking | User = ', request.user
        data = {'success': 'true'}
    except Exception:
        print 'Exception | hall_booking_confirm.py | Save Booking | ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def check_availability(request):
    data = {}
    date_dict = {}
    try:
        print '\n\n\nrequest.POST = ', request.POST
        print '\nRequest IN | hall_booking_confirm.py | check_availability | User = ', request.user
        print "________________________________________check_availability___________________________________"


        hall_detail_obj = HallDetail.objects.get(id=request.POST.get('hall_id'))

        from_to_date_list = []
        slot_not_avail_list = []

        date_list = request.POST.getlist('from_date_list[]')
        from_hour_list = request.POST.getlist('from_hour_list[]')
        to_hour_list = request.POST.getlist('to_hour_list[]')
        from_minute_list = request.POST.getlist('from_minute_list[]')
        to_minute_list = request.POST.getlist('to_minute_list[]')
        from_period = request.POST.getlist('from_period_list[]')
        to_period = request.POST.getlist('to_period_list[]')
        length = len(date_list)
        to_zone = tz.gettz("Asia/Kolkata")

        for i in range(0, length):
            local_date = datetime.strptime(str(date_list[i]), '%d/%m/%Y')

            local_from_time = ''
            local_to_time = ''

            if from_period[i] == "PM":
                if from_hour_list[i] == '12':
                    local_from_time = time(int(from_hour_list[i]), int(from_minute_list[i]))
                else:
                    local_from_time = time(int(from_hour_list[i]) + 12, int(from_minute_list[i]))
            else:
                if int(from_hour_list[i]) == 12:
                    local_from_time = time(int(00), int(from_minute_list[i]))
                else:
                    local_from_time = time(int(from_hour_list[i]), int(from_minute_list[i]))
            if to_period[i] == "PM":
                if to_hour_list[i] == '12':
                    local_to_time = time(int(to_hour_list[i]), int(to_minute_list[i]))
                else:
                    local_to_time = time(int(to_hour_list[i]) + 12, int(to_minute_list[i]))
            else:
                if int(to_hour_list[i]) == 12:
                    local_to_time = time(int(00), int(to_minute_list[i]))
                else:
                    local_to_time = time(int(to_hour_list[i]), int(to_minute_list[i]))

            from_time = datetime.strptime(str(local_from_time), '%H:%M:%S')
            to_time = datetime.strptime(str(local_to_time), '%H:%M:%S')
            f_time = datetime.strftime(from_time, '%H,%M')
            t_time = datetime.strftime(to_time, '%H,%M')
            f_time = datetime.strptime(f_time, '%H,%M').time()
            t_time = datetime.strptime(t_time, '%H,%M').time()

            from_date_time = datetime.combine(local_date.date(), f_time)
            to_date_time = datetime.combine(local_date.date(), t_time)

            from_to_date_list.append(from_date_time)
            from_to_date_list.append(to_date_time)

        for i in from_to_date_list:
            date_dict.setdefault((i.date()), []).append(i.time())

        for key, value in date_dict.iteritems():
            print '\nKey = ', key
            print '\nValue = ', value

            # Increase & Decrease Time By 1 Hour
            today = datetime.now().date()
            from_today = datetime.combine(today, value[0]) - timedelta(hours=1)
            to_today = datetime.combine(today, value[1]) + timedelta(hours=1)
            from_today = from_today.time()
            to_today = to_today.time()
            print '\nfrom_today = ', from_today, type(from_today)
            print '\nto_today = ', to_today
            if hall_detail_obj.is_merge:
                hall_id_list = (hall_detail_obj.hall_merge).split(",")
                hall_booking_from_list = HallCheckAvailability.objects.filter(hall_detail_id__in=hall_id_list,
                                                                              booking_from_date__icontains=key)
                hall_booking_to_list = HallCheckAvailability.objects.filter(hall_detail_id__in=hall_id_list,
                                                                            booking_to_date__icontains=key)
            else:
                hall_booking_from_list = HallCheckAvailability.objects.filter(hall_detail=hall_detail_obj,
                                                                              booking_from_date__icontains=key)
                hall_booking_to_list = HallCheckAvailability.objects.filter(hall_detail=hall_detail_obj,
                                                                            booking_to_date__icontains=key)

            hall_booking_from_list = hall_booking_from_list.exclude(booking_status__in=[0, 10])
            hall_booking_to_list = hall_booking_to_list.exclude(booking_status__in=[0, 10])

            for i in range(0, len(hall_booking_from_list)):
                # print '\nDB FROM LOCAL TIME = ', hall_booking_from_list[i].booking_from_date.astimezone(to_zone)
                # print '\nDB TO LOCAL TIME = ', hall_booking_to_list[i].booking_to_date.astimezone(to_zone)
                # print '\nTYPE = ', type(hall_booking_to_list[i].booking_to_date.astimezone(to_zone))
                

                if (from_today <= hall_booking_from_list[i].booking_from_date.astimezone(to_zone).time() and
                    to_today <= hall_booking_from_list[i].booking_from_date.astimezone(to_zone).time()) or \
                        (from_today >= hall_booking_to_list[i].booking_to_date.astimezone(to_zone).time() and
                         to_today >= hall_booking_to_list[i].booking_to_date.astimezone(to_zone).time()):
                    print '\nSLOT AVAILABLE'
                else:
                    print '\nSLOT NOT AVAILABLE'
                    slot_not_avail_list.append({'date': str(key.strftime('%d/%m/%Y'))})

        data = {'success': 'true', 'slot_not_avail_list': slot_not_avail_list}
        print '\nResponse OUT | hall_booking_confirm.py | check_availability | User = ', request.user
    except Exception:
        data = {'success': 'false'}
        print '\nException IN | hall_booking_confirm.py | check_availability | User = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')



# Get Booking Slot table with Holiday
@csrf_exempt
def get_slot_table(request):
    data = {}
    try:
        print '\nRequest IN | hall_booking_confirm.py | get_slot_table | User = ', request.user
        output_list = []
        hall_equipment_list = []
        start_date = datetime.strptime(str(request.POST.get('start_date')), '%d/%m/%Y').date()
        end_date = datetime.strptime(str(request.POST.get('end_date')), '%d/%m/%Y').date()

        # if request.POST.get('check_user') == 'm':
        #     hall_equipment_obj_list = HallEquipment.objects.filter(hall_detail_id=request.POST.get('hall_id'),
        #                                                            member_charges__gt=0,
        #                                                            is_active=True, is_deleted=False)
        # else:
        #     hall_equipment_obj_list = HallEquipment.objects.filter(hall_detail_id=request.POST.get('hall_id'),
        #                                                            non_member_charges__gt=0,
        #                                                            is_active=True, is_deleted=False)
        # for item in hall_equipment_obj_list:
        #     hall_equipment_list.append(
        #         {'id': item.id, 'hall_equipment': str(item.hall_functioning_equipment.equipment_name)}
        #     )

        holiday_list = Holiday.objects.filter(holiday_date__gte=start_date, holiday_date__lte=end_date,
                                              status=True, is_deleted=False, holiday_status=False)
        while start_date <= end_date:
            if start_date in [item.holiday_date for item in holiday_list]:
                hall_holiday_obj = Holiday.objects.get(holiday_date=start_date)
                output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES',
                                    'type': str(hall_holiday_obj.get_holiday_type_display()),
                                    'is_booking_available': str(hall_holiday_obj.is_booking_available),
                                    'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
            elif (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
                    start_date.weekday() == 6):
                output_list.append(
                    {'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
                     'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
            else:
                output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
                                    'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

            start_date += timedelta(days=1)

        for i in range(1, 8):
            hall_equipment_list.append(
                {'id': i, 'hall_equipment': 'Video'}
            )

        data['success'] = 'true'
        data['output_list'] = output_list
        data['hall_equipment_list'] = hall_equipment_list
        print '\nResponse OUT | hall_booking_confirm.py | get_slot_table | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_confirm.py | get_slot_table | User = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')






# # Get Booking Slot table with Holiday
# @csrf_exempt
# def get_slot_table(request):
#     data = {}
#     try:
#         print '\nRequest IN | hall_booking_confirm.py | get_slot_table | User = ', request.user
#         output_list = []
#         hall_equipment_list = []
#         start_date = datetime.strptime(str(request.POST.get('start_date')), '%d/%m/%Y').date()
#         end_date = datetime.strptime(str(request.POST.get('end_date')), '%d/%m/%Y').date()
#         hall_id = request.POST.get('hall_id')
#         user_type = request.POST.get('check_user')

#         hall_detail_obj = HallDetail.objects.get(id = hall_id)

#         hall_equipment_obj = HallEquipment.objects.filter(hall_detail__id = hall_detail_obj.id)
#         if hall_equipment_obj:
#             hall_equipment_val = 'value'
#         else:
#             hall_equipment_val = ''

#         day_list = []
#         day_list_val = []
#         hall_booking_obj = HallBookingDetail.objects.filter(hall_detail__id = hall_id, is_deleted=False)
#         for hall_booking_objs in hall_booking_obj:
#             hall_detail_id = hall_booking_objs.hall_detail.id
#         temp_list = []
#         if start_date == end_date:
#             holiday_list = Holiday.objects.filter(Q(holiday_date=start_date,holiday_date_to=start_date)|Q(holiday_date=start_date)|Q(holiday_date_to=start_date),
#                                              status=True, is_deleted=False, holiday_status=False)
#             for holiday_lists in holiday_list:
#                 if start_date <= holiday_lists.holiday_date or holiday_lists.holiday_date_to >= start_date:
#                     temp_list.append(holiday_lists)

#         else:
#             holiday_list = Holiday.objects.filter(Q(holiday_date__gte =start_date,holiday_date_to__lte =end_date),
#                                                  status=True, is_deleted=False, holiday_status=False)
#             for holiday_lists in holiday_list:
#                 if start_date <= holiday_lists.holiday_date and end_date >= holiday_lists.holiday_date_to or start_date <= holiday_lists.holiday_date_to:
#                     temp_list.append(holiday_lists)

#         for dd in holiday_list:
#             from_date = datetime.strptime(str(dd.holiday_date), '%Y-%m-%d').date()
#             to_date = datetime.strptime(str(dd.holiday_date_to), '%Y-%m-%d').date()
#             delta = to_date - from_date

#             for i in range(delta.days + 1):
#                 day = from_date + timedelta(days=i)
#                 day_list.append(day)

#         # matches = []
#         # for c in day_list:
#         #   if c == start_date:
#         #     matches.append(c)
#         # temp_list = []
#         # for holiday_lists in holiday_list:
#         #     if start_date <= holiday_lists.holiday_date and end_date >= holiday_lists.holiday_date_to:
#         #         temp_list.append(holiday_lists)
#         print '==============temp_list==========',temp_list
#         if temp_list:
#             flag = "not equal"
#             for holiday_lists in temp_list:
#                 if end_date < start_date and end_date in day_list:
#                     start_date -= timedelta(days=1)
#                 if holiday_lists.hall_location == hall_detail_obj.hall_location:
#                     print '--------------location equal-------------',
#                     if holiday_lists.hall_detail.hall_name == hall_detail_obj.hall_name:
#                         print '-----------------hall equal--------'
#                         while start_date <= end_date:
#                             # if start_date == end_date:
#                             #     hall_holiday_obj = Holiday.objects.filter(holiday_date=start_date,holiday_date_to=start_date)
#                             # else:
#                             hall_holiday_obj = Holiday.objects.filter(Q(holiday_date__gte =start_date, holiday_date__lte=end_date)|Q(holiday_date__gte =start_date, holiday_date_to__lte=end_date)|Q(holiday_date__lte=start_date,holiday_date_to__gte=start_date),
#                                     hall_location__location=hall_detail_obj.hall_location,hall_detail__hall_name=hall_detail_obj.hall_name)

#                             if hall_holiday_obj:
#                                 for hall_holiday in hall_holiday_obj:
#                                     from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                     to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                     delta = to_date - from_date

#                                     for i in range(delta.days + 1):
#                                         day = from_date + timedelta(days=i)
#                                         day_list_val.append(day)

#                                     if start_date in day_list_val:
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                             'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                             'type': str(hall_holiday.get_holiday_type_display()),
#                                                             'is_booking_available': str(hall_holiday.is_booking_available),
#                                                             'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})
#                                     elif (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                             start_date.weekday() == 6):
#                                         print '************elif 1************'
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                     else:
#                                         print '************else 1************'
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                             'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                             else:
#                                 if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                             start_date.weekday() == 6):
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                 else:
#                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                         'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

#                             start_date += timedelta(days=1)

#                     else:
#                         # flag = "not equal"
#                         print '\n____________not equal hall name______'
#                         # if holiday_lists.holiday_date < start_date and holiday_lists.holiday_date in day_list:
#                         start_date_val = start_date - timedelta(days=1)
#                         if holiday_lists.hall_detail.hall_name == 'All':
#                             print '=================hall name all======='
#                             while start_date <= end_date or start_date_val == end_date:
#                                 print '-----------whileloop',start_date,start_date_val
#                                 if start_date == end_date:
#                                     hall_holiday_obj = Holiday.objects.filter(Q(holiday_date=start_date,holiday_date_to=end_date)|Q(holiday_date__lte=start_date,holiday_date_to=start_date),hall_location__location=hall_detail_obj.hall_location,hall_detail__id=44)
#                                 else:
#                                     hall_holiday_obj = Holiday.objects.filter(Q(holiday_date__gte =start_date, holiday_date__lte=end_date)|Q(holiday_date__gte =start_date, holiday_date_to__lte=end_date)|Q(holiday_date__lte=start_date,holiday_date_to__gte=start_date),hall_detail__id=44)

#                                 if hall_holiday_obj:
#                                     print '----insideif'
#                                     for hall_holiday in hall_holiday_obj:
#                                         from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                         to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                         delta = to_date - from_date

#                                         for i in range(delta.days + 1):
#                                             day = from_date + timedelta(days=i)
#                                             day_list_val.append(day)

#                                         if flag != "equal":
#                                             print '----------in equal------',start_date,day_list_val
#                                             if start_date in day_list_val:
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                                     'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                                     'type': str(hall_holiday.get_holiday_type_display()),
#                                                                     'is_booking_available': str(hall_holiday.is_booking_available),
#                                                                     'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})

#                                             elif (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                     start_date.weekday() == 6):
#                                                 print '************elif 4************'
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                      'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                             else:
#                                                 print '************else 4************'
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                                     'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                         # else:
#                                         #     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                         #                             'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

#                                     start_date_val -= timedelta(days=1)
#                                 else:
#                                     print '-------------------else45'
#                                     while start_date <= end_date:
#                                         if start_date == end_date:
#                                             hall_holiday_obj = Holiday.objects.filter(Q(holiday_date=start_date,holiday_date_to=start_date)|Q(holiday_date__lte=start_date,holiday_date_to=start_date),hall_location__location=hall_detail_obj.hall_location,hall_detail__hall_name=hall_detail_obj.hall_name)
#                                         else:
#                                             hall_holiday_obj = Holiday.objects.filter(Q(holiday_date__gte =start_date, holiday_date__lte=end_date)|Q(holiday_date__gte =start_date, holiday_date_to__lte=end_date)|Q(holiday_date__lte=start_date,holiday_date_to__gte=start_date),hall_location__location=hall_detail_obj.hall_location,hall_detail__hall_name=hall_detail_obj.hall_name)

#                                         if hall_holiday_obj:
#                                             for hall_holiday in hall_holiday_obj:
#                                                 from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                                 to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                                 delta = to_date - from_date

#                                                 for i in range(delta.days + 1):
#                                                     day = from_date + timedelta(days=i)
#                                                     day_list_val.append(day)

#                                                 if start_date in day_list_val:
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                                         'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                                         'type': str(hall_holiday.get_holiday_type_display()),
#                                                                         'is_booking_available': str(hall_holiday.is_booking_available),
#                                                                         'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})

#                                                 elif (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                             start_date.weekday() == 6):
#                                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                                 else:
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                                         'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                         else:
#                                             print '$$$$$$$$$$$$$$$$elif'
#                                             if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                             start_date.weekday() == 6):
#                                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                             else:
#                                                 print '%%%%%%%%%%%else'
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                                 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

#                                         start_date += timedelta(days=1)
#                                 start_date += timedelta(days=1)
#                                 start_date_val -= timedelta(days=1)
#                         else:
#                             print '---------------diifernt hall---------'
#                             while start_date <= end_date:
#                                 if start_date == end_date:
#                                     hall_holiday_obj = Holiday.objects.filter(Q(holiday_date=start_date,holiday_date_to=start_date)|Q(holiday_date_to=start_date),hall_location__location=hall_detail_obj.hall_location,hall_detail__hall_name=hall_detail_obj.hall_name)
#                                 else:
#                                     hall_holiday_obj = Holiday.objects.filter(Q(holiday_date__gte =start_date, holiday_date__lte=end_date)|Q(holiday_date__gte =start_date, holiday_date_to__lte=end_date)|Q(holiday_date__lte=start_date,holiday_date_to__gte=start_date),hall_location__location=hall_detail_obj.hall_location)


#                                 if hall_holiday_obj:
#                                     for hall_holiday in hall_holiday_obj:
#                                         from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                         to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                         delta = to_date - from_date

#                                         for i in range(delta.days + 1):
#                                             day = from_date + timedelta(days=i)
#                                             day_list_val.append(day)
#                                         if hall_holiday.hall_detail.hall_name == 'All':
#                                             if start_date in day_list_val:
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                                     'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                                     'type': str(hall_holiday.get_holiday_type_display()),
#                                                                     'is_booking_available': str(hall_holiday.is_booking_available),
#                                                                     'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})
#                                             elif (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                         start_date.weekday() == 6):
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                          'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                                     print'---------------elseif'
#                                             else:
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                                     'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                         else:
#                                             if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                         start_date.weekday() == 6):
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                          'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                                     print'---------------elseif'
#                                             else:
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                                     'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                 else:
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                             'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

#                                 start_date += timedelta(days=1)

#                 else:
#                     flag = 2
#                     if holiday_lists.hall_location.id == 5:
#                         print '***************all location********',
#                         while start_date <= end_date:
#                             if start_date == end_date:
#                                 hall_holiday_obj = Holiday.objects.filter(Q(holiday_date=start_date,holiday_date_to=start_date)|Q(holiday_date_to=start_date)|Q(holiday_date=start_date),hall_location__id=5)
#                             else:
#                                 hall_holiday_obj = Holiday.objects.filter(Q(holiday_date__gte =start_date, holiday_date_to__lte=end_date)|Q(holiday_date_to=start_date)|Q(holiday_date__gte =start_date, holiday_date=end_date),hall_location__id=5)

#                             if hall_holiday_obj:
#                                 for hall_holiday in hall_holiday_obj:
#                                     print '--------************----',hall_holiday
#                                     from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                     to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                     delta = to_date - from_date

#                                     for i in range(delta.days + 1):
#                                         day = from_date + timedelta(days=i)
#                                         day_list_val.append(day)

#                                     for output_lists in output_list:
#                                         if output_lists['date'] == str(start_date.strftime('%a %d, %b %Y')):
#                                             flag = 1
#                                         else:
#                                             flag = 2

#                                     if flag == 2:
#                                         if hall_holiday.hall_location.id == 5:
#                                             print '-----------5',day_list_val
#                                             if start_date in day_list_val:
#                                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                                     'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                                     'type': str(hall_holiday.get_holiday_type_display()),
#                                                                     'is_booking_available': str(hall_holiday.is_booking_available),
#                                                                     'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})

#                                             else:
#                                                 if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                             start_date.weekday() == 6):
#                                                     print '************elif 99************'
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                          'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                                 # if end_date != start_date_val:
#                                                 #     for output_lists in output_list:
#                                                 #         if output_lists['date'] == str(start_date.strftime('%a %d, %b %Y')):
#                                                 #             start_date += timedelta(days=1)
#                                                 #         else:
#                                                 #             start_date


#                                                 else:
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                                     'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

#                                         else:
#                                             print '-----------------6'
#                                             hall_holiday_obj = Holiday.objects.filter(holiday_date__gte =start_date,hall_location__location=hall_detail_obj.hall_location,hall_detail__hall_name=hall_detail_obj.hall_name)
#                                             if hall_holiday_obj:
#                                                 for hall_holiday in hall_holiday_obj:
#                                                     from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                                     to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                                     delta = to_date - from_date

#                                                     for i in range(delta.days + 1):
#                                                         day = from_date + timedelta(days=i)
#                                                         day_list_val.append(day)

#                                                     if start_date in day_list_val:
#                                                         print '__________output_list____________',output_list
#                                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                                             'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                                             'type': str(hall_holiday.get_holiday_type_display()),
#                                                                             'is_booking_available': str(hall_holiday.is_booking_available),
#                                                                             'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})
#                                                     elif (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                             start_date.weekday() == 6):
#                                                         print '************elif 2************'
#                                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                                     else:
#                                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                                 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                             else:
#                                                 print '--------------------9'
#                                                 if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                                             start_date.weekday() == 6):
#                                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                                 else:
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                             'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                             else:
#                                 if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                             start_date.weekday() == 6):
#                                         print '************elif 22************'
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                 else:
#                                     print '\n------------------------8',start_date,day_list
#                                     if start_date in day_list:
#                                         hall_holiday_obj = Holiday.objects.filter(Q(holiday_date__gte =start_date, holiday_date__lte=end_date)|Q(holiday_date__gte =start_date, holiday_date_to__lte=end_date)|Q(holiday_date__lte=start_date,holiday_date_to__gte=start_date),hall_location__location=hall_detail_obj.hall_location)
#                                         if hall_holiday_obj:
#                                             for hall_holiday in hall_holiday_obj:
#                                                 from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                                 to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                                 delta = to_date - from_date

#                                                 for i in range(delta.days + 1):
#                                                     day = from_date + timedelta(days=i)
#                                                     day_list_val.append(day)

#                                                 if start_date in day_list_val:
#                                                     print '---------------priyanka-----',start_date
#                                                     flag = "equal"
#                                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                                         'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                                         'type': str(hall_holiday.get_holiday_type_display()),
#                                                                         'is_booking_available': str(hall_holiday.is_booking_available),
#                                                                         'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})
#                                                 else:
#                                                     flag = "not equal"

#                                         else:
#                                             output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                         'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                     else:
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                         'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

#                             start_date += timedelta(days=1)


#                     else:
#                         print '_______________else==========='
#                         while start_date <= end_date:
#                             print '////////////////',start_date
#                             if start_date == end_date:
#                                 hall_holiday_obj = Holiday.objects.filter(Q(holiday_date=start_date,holiday_date_to=start_date)|Q(holiday_date__lte=start_date,holiday_date_to=start_date),hall_location__location=hall_detail_obj.hall_location,hall_detail__hall_name=hall_detail_obj.hall_name)
#                             else:
#                                 hall_holiday_obj = Holiday.objects.filter(Q(holiday_date__gte =start_date, holiday_date_to__lte=end_date),hall_location__location=hall_detail_obj.hall_location,hall_detail__hall_name=hall_detail_obj.hall_name)
#                             print '<<<<<<<<<<<<<<<<<<<<<<',hall_holiday_obj
#                             if hall_holiday_obj:
#                                 for hall_holiday in hall_holiday_obj:
#                                     from_date = datetime.strptime(str(hall_holiday.holiday_date), '%Y-%m-%d').date()
#                                     to_date = datetime.strptime(str(hall_holiday.holiday_date_to), '%Y-%m-%d').date()
#                                     delta = to_date - from_date

#                                     for i in range(delta.days + 1):
#                                         day = from_date + timedelta(days=i)
#                                         day_list_val.append(day)
#                                     if start_date in day_list_val:
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')),
#                                                             'to_date': str(end_date.strftime('%a %d, %b %Y')), 'status': 'YES',
#                                                             'type': str(hall_holiday.get_holiday_type_display()),
#                                                             'is_booking_available': str(hall_holiday.is_booking_available),
#                                                             'formatted_date': str(start_date.strftime('%d/%m/%Y')), 'location':holiday_lists.hall_location.id})

#                                     elif (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                             start_date.weekday() == 6):
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                              'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                     else:
#                                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                             'formatted_date': str(start_date.strftime('%d/%m/%Y'))})

#                             else:
#                                 if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                         start_date.weekday() == 6):
#                                     print '************elif 5************'
#                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                          'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                                 else:
#                                     print '************else 5************'
#                                     output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                                         'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                             start_date += timedelta(days=1)
#         else:
#             print '************not match else************'
#             while start_date <= end_date:
#                 if (start_date.weekday() == 5 and (8 <= start_date.day <= 14 or 22 <= start_date.day <= 28)) or (
#                                     start_date.weekday() == 6):
#                                 print '************elif 5************'
#                                 output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'YES', 'type': 'MCCIA Holiday',
#                                      'is_booking_available': 'True', 'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                 else:
#                     print '************else 5************'
#                     while start_date <= end_date:
#                         output_list.append({'date': str(start_date.strftime('%a %d, %b %Y')), 'status': 'NO',
#                                             'formatted_date': str(start_date.strftime('%d/%m/%Y'))})
#                         start_date += timedelta(days=1)
#                 start_date += timedelta(days=1)




#         for i in range(1, 8):
#             hall_equipment_list.append(
#                 {'id': i, 'hall_equipment': 'Video'}
#             )

#         data['success'] = 'true'
#         data['output_list'] = output_list
#         data['hall_equipment_list'] = hall_equipment_list
#         data['hall_id'] = hall_detail_id
#         data['user_type'] = user_type
#         data['hall_equipment'] = hall_equipment_val
#         print '\nResponse OUT | hall_booking_confirm.py | get_slot_table | User = ', request.user
#     except Exception, e:
#         data['success'] = 'false'
#         print '\nException IN | hall_booking_confirm.py | get_slot_table | User = ', str(traceback.print_exc())
#     return HttpResponse(json.dumps(data), content_type='application/json')






# Save Temporary Hall Booking Data
@csrf_exempt
@transaction.atomic
def save_temp_booking_data(request):
    # pdb.set_trace()
    data = {}
    from_zone = tz.tzutc()
    to_zone = tz.gettz('Asia/Kolkata')
    sid = transaction.savepoint()
    booking_detail_no = int(datetime.now().strftime('%Y%m%d%H%M%S'))
    try:
        print '\nRequest IN | hall_booking_confirm.py | save_temp_booking_data | User = ', request.user, request.POST

        from_to_date_list = []
        date_list = request.POST.getlist('from_date_list[]')
        from_hour_list = request.POST.getlist('from_hour_list[]')
        to_hour_list = request.POST.getlist('to_hour_list[]')
        from_minute_list = request.POST.getlist('from_minute_list[]')
        to_minute_list = request.POST.getlist('to_minute_list[]')
        from_period_list = request.POST.getlist('from_period_list[]')
        to_period_list = request.POST.getlist('to_period_list[]')

        length = len(date_list)

        booking_for = 2
        name = ''
        mem_id = None
        if request.POST.get('member_status') == 'm':
            try:
                memberobj = UserDetail.objects.get(id=request.POST.get('company_list'))
                name = memberobj.company.company_name
                mem_id = request.POST.get('company_list')
                booking_for = 1
            except Exception, e:
                pass
        else:
            if not request.user.is_anonymous():
                if request.session['user_type'] == 'backoffice':
                    name = "MCCIA"
                    booking_for = 0
                    login_user = request.user.systemuserprofile
                    login_user_obj = SystemUserProfile.objects.get(username=login_user.username)
            else:
                name = request.POST.get('company_name_text').encode("utf8", "ignore")
                mem_id = None
                booking_for = 2

        booking_id = request.POST.get('booking_id')
        if booking_id:
            hall_booking_obj = HallBooking.objects.get(id=booking_id)
        else:
            hall_booking_obj = HallBooking(
                member_id=mem_id, name=str(name), booking_for=booking_for,
                gst_no=str(request.POST.get('GSTIN')) if request.POST.get('GSTIN') else None
            )
            hall_booking_obj.save()

            # hall_booking_obj.booking_no = str('HBK' + str(str.zfill(str(hall_booking_obj.id), 7)))
            # hall_booking_obj.save()

        user_track_id = request.POST.get('user_track_id')
        if user_track_id:
            user_track_obj = UserTrackDetail.objects.get(id=user_track_id)
            if not request.user.is_anonymous() and request.session['user_type'] == 'backoffice':
                # Update using login obj
                user_track_obj.address=str(login_user_obj.role.role) if login_user_obj.role else 'NA'
                user_track_obj.contact_person=str(login_user_obj.name) if login_user_obj.name else 'NA'
                user_track_obj.designation=str(
                            login_user_obj.designation.designation_name) if login_user_obj.designation else 'NA'
                user_track_obj.mobile_no=str(login_user_obj.contact_no) if login_user_obj.contact_no else 'NA'
                user_track_obj.tel_r=str(login_user_obj.contact_no) if login_user_obj.contact_no else 'NA'
                user_track_obj.email=str(request.user.email) if request.user.email else 'NA'
                user_track_obj.gst=str(request.POST.get('GSTIN')) if request.POST.get('GSTIN') else None
                user_track_obj.save()
                hall_booking_obj.user_track = user_track_obj
                hall_booking_obj.system_user_profile = login_user_obj
                hall_booking_obj.save()
            else:
                # Update user track object same for all fields except mem_id. Update mem_id according to condition.
                user_track_obj.member_id= mem_id if request.POST.get('member_status') == 'm' else None
                user_track_obj.company=name
                user_track_obj.address=request.POST.get('address').encode("utf8", "ignore")
                user_track_obj.contact_person=str(request.POST.get('ContactPerson'))
                user_track_obj.designation=request.POST.get('Designation').encode("utf8", "ignore")
                user_track_obj.mobile_no=str(request.POST.get('Mobile'))
                user_track_obj.tel_r=str(request.POST.get('TelR'))
                user_track_obj.tel_o=str(request.POST.get('Tel'))
                user_track_obj.email=str(request.POST.get('email'))
                user_track_obj.gst=str(request.POST.get('GSTIN')) if request.POST.get('GSTIN') else None
                user_track_obj.save()
                hall_booking_obj.user_track = user_track_obj
                hall_booking_obj.save()
        else:
            if not request.user.is_anonymous() and request.session['user_type'] == 'backoffice':
                #3333 Create user track obj using login user object
                user_track_obj = UserTrackDetail(
                    company=name,
                    address=str(login_user_obj.role.role) if login_user_obj.role else 'NA',
                    contact_person=str(login_user_obj.name) if login_user_obj.name else 'NA',
                    designation=str(
                        login_user_obj.designation.designation_name) if login_user_obj.designation else 'NA',
                    mobile_no=str(login_user_obj.contact_no) if login_user_obj.contact_no else 'NA',
                    tel_r=str(login_user_obj.contact_no) if login_user_obj.contact_no else 'NA',
                    email=str(request.user.email) if request.user.email else 'NA',
                    gst=str(request.POST.get('GSTIN')) if request.POST.get('GSTIN') else None
                )
                user_track_obj.save()
                hall_booking_obj.user_track = user_track_obj
                hall_booking_obj.system_user_profile = login_user_obj
                hall_booking_obj.save()

            else:
                # Create user track object same for all fields except mem_id. Update mem_id according to condition.
                user_track_obj = UserTrackDetail(
                    member_id=mem_id,
                    company=name,
                    address=request.POST.get('address').encode("utf8", "ignore"),
                    contact_person=str(request.POST.get('ContactPerson')),
                    designation=request.POST.get('Designation').encode("utf8", "ignore"),
                    mobile_no=str(request.POST.get('Mobile')),
                    tel_r=str(request.POST.get('TelR')),
                    tel_o=str(request.POST.get('Tel')),
                    email=str(request.POST.get('email')),
                    gst=str(request.POST.get('GSTIN')) if request.POST.get('GSTIN') else None
                        )
                user_track_obj.save()

                hall_booking_obj.user_track = user_track_obj
                hall_booking_obj.save()


        for i in range(0, length):
            local_date = datetime.strptime(str(date_list[i]), '%d/%m/%Y')
            local_from_time = ''
            local_to_time = ''

            if from_period_list[i] == "PM":
                if from_hour_list[i] == '12':
                    local_from_time = time(int(from_hour_list[i]), int(from_minute_list[i]))
                else:
                    local_from_time = time(int(from_hour_list[i]) + 12, int(from_minute_list[i]))
            else:
                if int(from_hour_list[i]) == 12:
                    local_from_time = time(int(00), int(from_minute_list[i]))
                else:
                    local_from_time = time(int(from_hour_list[i]), int(from_minute_list[i]))
            if to_period_list[i] == "PM":
                if to_hour_list[i] == '12':
                    local_to_time = time(int(to_hour_list[i]), int(to_minute_list[i]))
                else:
                    local_to_time = time(int(to_hour_list[i]) + 12, int(to_minute_list[i]))
            else:
                if int(to_hour_list[i]) == 12:
                    local_to_time = time(int(00), int(to_minute_list[i]))
                else:
                    local_to_time = time(int(to_hour_list[i]), int(to_minute_list[i]))

            from_time = datetime.strptime(str(local_from_time), '%H:%M:%S')
            to_time = datetime.strptime(str(local_to_time), '%H:%M:%S')
            f_time = datetime.strftime(from_time, '%H,%M')
            t_time = datetime.strftime(to_time, '%H,%M')
            f_time = datetime.strptime(f_time, '%H,%M').time()
            t_time = datetime.strptime(t_time, '%H,%M').time()

            from_date_time = datetime.combine(local_date.date(), f_time)
            to_date_time = datetime.combine(local_date.date(), t_time)

            # Dictionary: Key = Date and Value = From and To Time
            date_time_dict = {}

            date_time_dict.setdefault((from_date_time.date()), []).append(from_date_time.time())
            date_time_dict.setdefault((to_date_time.date()), []).append(to_date_time.time())

            hall_obj = HallDetail.objects.get(id=request.POST.get('hall_id'))

            check = check_hall_avail_status(date_time_dict, hall_obj)
            if check:

                for key, value in date_time_dict.iteritems():
                    utc_to_date = datetime.combine(key, value[1])
                    utc_from_date = datetime.combine(key, value[0])
                    # utc_to_date = dateutil.parser.parse(datetime.combine(key, value[1]))
                    utc_to_date = utc_to_date.replace(tzinfo=from_zone)
                    final_to_date = utc_to_date.astimezone(to_zone)

                    # utc_from_date = dateutil.parser.parse(datetime.combine(key, value[0]))
                    utc_from_date = utc_from_date.replace(tzinfo=from_zone)
                    final_from_date = utc_from_date.astimezone(to_zone)

                    # Payment Calculation
                    hall_rent_dict = {}
                    if utc_from_date.date() in [item.holiday_date for item in
                                                Holiday.objects.filter(holiday_date__gte=utc_from_date.date(),
                                                                       status=True, is_deleted=False,
                                                                       is_booking_available=True)]:
                        week_day = '6'
                    else:
                        week_day = utc_from_date.strftime('%w')
                    minutes = int(ceil((final_to_date - final_from_date).seconds / 60.0))

                    if request.POST.get('member_status') == 'm':
                        member_obj = UserDetail.objects.get(id=request.POST.get('company_list'))
                        if member_obj.valid_invalid_member:
                            hall_rent_dict = get_total_hall_rent(week_day, minutes, hall_obj, True)
                        else:
                            hall_rent_dict = get_total_hall_rent(week_day, minutes, hall_obj, False)
                    else:
                        hall_rent_dict = get_total_hall_rent(week_day, minutes, hall_obj, False)

                    hall_booking_obj.total_rent = hall_booking_obj.total_rent + int(hall_rent_dict['total_rent'])

                    # if str(hall_obj.hall_location.location).strip() == 'Bhosari':
                    #     hall_booking_obj.deposit = constant.BHOSARI_HALL_DEPOSIT
                    # else:                        
                    # hall_booking_obj.deposit = hall_obj.hall_location.deposit
                    # hall_booking_obj.save()                    
                    gstObj = Servicetax.objects.get(tax_type=0, is_active=True)
                    hall_booking_obj.gst_tax = float(gstObj.tax)
                    hall_booking_obj.save()

                    hall_booking_obj.gst_amount = Decimal(hall_booking_obj.total_rent) * (Decimal(gstObj.tax) / 100)
                    hall_booking_obj.save()

                    hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.gst_amount, 0)
                    hall_booking_obj.save()

                    gst_amount = Decimal(int(hall_rent_dict['total_rent'])) * (Decimal(gstObj.tax) / 100)

                    if not request.user.is_anonymous():
                        if request.session['user_type'] == 'backoffice':
                            hall_booking_detail_obj = HallBookingDetail(
                                hall_location=hall_obj.hall_location, hall_detail=hall_obj,
                                hall_booking=hall_booking_obj,
                                booking_from_date=final_from_date,
                                booking_to_date=final_to_date,
                                booking_from_date_for_reference = final_from_date,
                                booking_to_date_for_reference=final_to_date,
                                address=str(login_user_obj.role.role) if login_user_obj.role else 'NA',
                                contact_person=str(login_user_obj.name) if login_user_obj.name else 'NA',
                                designation=str(
                                    login_user_obj.designation.designation_name) if login_user_obj.designation else 'NA',
                                mobile_no=str(login_user_obj.contact_no) if login_user_obj.contact_no else 'NA',
                                tel_r=str(login_user_obj.contact_no) if login_user_obj.contact_no else 'NA',
                                email=str(request.user.email) if request.user.email else 'NA',
                                event_nature=request.POST.get('NatureoftheEvent').encode("utf8", "ignore"),
                                booking_detail_no=booking_detail_no,
                                total_rent=hall_rent_dict['total_rent'], gst_amount=gst_amount,
                                first_total_rent_for_reference=hall_rent_dict['total_rent'],
                                slot=hall_rent_dict['slot'],
                                member_price=hall_rent_dict['member_price'],
                                non_member_price=hall_rent_dict['nonmember_price'],
                                member_extra_hour_price=hall_rent_dict['extra_member_price'],
                                non_member_extra_hour_price=hall_rent_dict['extra_nonmember_price']
                            )
                            hall_booking_detail_obj.save()
                        else:
                            hall_booking_detail_obj = HallBookingDetail(
                                hall_location=hall_obj.hall_location, hall_detail=hall_obj,
                                hall_booking=hall_booking_obj,
                                booking_from_date=final_from_date,
                                booking_to_date=final_to_date,
                                booking_from_date_for_reference = final_from_date,
                                booking_to_date_for_reference=final_to_date,
                                address=request.POST.get('address').encode("utf8", "ignore"),
                                contact_person=str(request.POST.get('ContactPerson')),
                                designation=request.POST.get('Designation').encode("utf8", "ignore"),
                                mobile_no=str(request.POST.get('Mobile')),
                                tel_r=str(request.POST.get('TelR')),
                                tel_o=str(request.POST.get('Tel')),
                                email=str(request.POST.get('email')),
                                event_nature=request.POST.get('NatureoftheEvent').encode("utf8", "ignore"),
                                booking_detail_no=booking_detail_no,
                                total_rent=hall_rent_dict['total_rent'], gst_amount=gst_amount,
                                first_total_rent_for_reference=hall_rent_dict['total_rent'],
                                slot=hall_rent_dict['slot'],
                                member_price=hall_rent_dict['member_price'],
                                non_member_price=hall_rent_dict['nonmember_price'],
                                member_extra_hour_price=hall_rent_dict['extra_member_price'],
                                non_member_extra_hour_price=hall_rent_dict['extra_nonmember_price']
                            )
                            hall_booking_detail_obj.save()
                    else:
                        hall_booking_detail_obj = HallBookingDetail(
                            hall_location=hall_obj.hall_location, hall_detail=hall_obj, hall_booking=hall_booking_obj,
                            booking_from_date=final_from_date,
                            booking_to_date=final_to_date,
                            booking_from_date_for_reference = final_from_date,
                            booking_to_date_for_reference=final_to_date,
                            address=request.POST.get('address').encode("utf8", "ignore"),
                            contact_person=str(request.POST.get('ContactPerson')),
                            designation=request.POST.get('Designation').encode("utf8", "ignore"),
                            mobile_no=str(request.POST.get('Mobile')),
                            tel_r=str(request.POST.get('TelR')),
                            tel_o=str(request.POST.get('Tel')),
                            email=str(request.POST.get('email')),
                            event_nature=request.POST.get('NatureoftheEvent').encode("utf8", "ignore"),
                            booking_detail_no=booking_detail_no,
                            total_rent=hall_rent_dict['total_rent'], gst_amount=gst_amount,
                            first_total_rent_for_reference=hall_rent_dict['total_rent'],
                            slot=hall_rent_dict['slot'],
                            member_price=hall_rent_dict['member_price'],
                            non_member_price=hall_rent_dict['nonmember_price'],
                            member_extra_hour_price=hall_rent_dict['extra_member_price'],
                            non_member_extra_hour_price=hall_rent_dict['extra_nonmember_price']
                        )
                        hall_booking_detail_obj.save()

                    if hall_obj.is_merge:
                        hall_id_list = (hall_obj.hall_merge).split(",")
                        for i in hall_id_list:
                            hall_check_avail_obj = HallCheckAvailability(
                                hall_detail_id=i,
                                hall_booking_detail=hall_booking_detail_obj,
                                booking_from_date=datetime.combine(key, value[0]),
                                booking_to_date=datetime.combine(key, value[1])
                            )
                            hall_check_avail_obj.save()
                    else:
                        hall_check_avail_obj = HallCheckAvailability(
                            hall_detail=hall_obj, hall_booking_detail=hall_booking_detail_obj,
                            booking_from_date=datetime.combine(key, value[0]),
                            booking_to_date=datetime.combine(key, value[1])
                        )
                        hall_check_avail_obj.save()

        transaction.savepoint_commit(sid)
        if request.POST.get('is_continue') == 'true':
            data = {'success': 'true',
                    'booking_id': hall_booking_obj.id,
                    'booking_no': hall_booking_obj.booking_no,
                    'member_status': 'nm'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            # booking_sb_obj = HallBookingDetail.objects.filter(hall_location__location='MCCIA Trade Tower (5th Floor)',
            #                                                   pi_no__isnull=False).last()
            # booking_tilak_obj = HallBookingDetail.objects.filter(hall_location__location='Tilak Road',
            #                                                      pi_no__isnull=False).last()
            # booking_bhosari_obj = HallBookingDetail.objects.filter(hall_location__location='Bhosari',
            #                                                        pi_no__isnull=False).last()
            # booking_hadapsar_obj = HallBookingDetail.objects.filter(hall_location__location='Hadapsar',
            #                                                         pi_no__isnull=False).last()
            #
            deposit_list = []
            booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).values(
                'hall_location').annotate(dcount=Count('hall_location'))
            for i in booking_detail_list:
                booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj,
                                                                      hall_location=i['hall_location']).last()
                deposit_list.append(booking_detail_obj.hall_location.deposit)

                # hall_location = booking_detail_obj.hall_location.location
            #     if hall_location == 'MCCIA Trade Tower (5th Floor)':
            #         booking_detail_obj.pi_no = int(booking_sb_obj.pi_no) + 1
            #     elif hall_location == 'Tilak Road':
            #         booking_detail_obj.pi_no = int(booking_tilak_obj.pi_no) + 1
            #     elif hall_location == 'Bhosari':
            #         booking_detail_obj.pi_no = int(booking_bhosari_obj.pi_no) + 1
            #     elif hall_location == 'Hadapsar':
            #         booking_detail_obj.pi_no = int(booking_hadapsar_obj.pi_no) + 1
            #
            #     booking_detail_obj.save()

                # hall_booking_obj.deposit = max(deposit_list)  #Deposit SS

            if user_track_obj.deposit_available > 0:  # and user_track_obj.deposit_status==0:
                hall_booking_obj.deposit = 0
            else:
                hall_booking_obj.deposit = max(deposit_list)
                # user_track_obj.deposit_available = max(deposit_list)
                user_track_obj.save()
            hall_booking_obj.save()

            hall_booking_obj.first_total_rent_for_reference = hall_booking_obj.total_rent
            hall_booking_obj.save()

            hall_booking_obj.total_payable = round(
                Decimal(hall_booking_obj.total_rent) + Decimal(hall_booking_obj.deposit) + Decimal(
                    hall_booking_obj.gst_amount), 0)
            hall_booking_obj.save()

            data = {'success': 'false',
                    'booking_id': hall_booking_obj.id,
                    'booking_no': hall_booking_obj.booking_no}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_confirm.py | save_temp_booking_data | User = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Code to check hall avail while saving booking
def check_hall_avail_status(date_dict, hall_detail_obj):
    try:
        to_zone = tz.gettz("Asia/Kolkata")
        for key, value in date_dict.iteritems():
            if hall_detail_obj.is_merge:
                hall_id_list = (hall_detail_obj.hall_merge).split(",")
                hall_booking_from_list = HallCheckAvailability.objects.filter(hall_detail_id__in=hall_id_list,
                                                                              booking_from_date__icontains=key)
                hall_booking_to_list = HallCheckAvailability.objects.filter(hall_detail_id__in=hall_id_list,
                                                                            booking_to_date__icontains=key)
            else:
                hall_booking_from_list = HallCheckAvailability.objects.filter(hall_detail=hall_detail_obj,
                                                                              booking_from_date__icontains=key)
                hall_booking_to_list = HallCheckAvailability.objects.filter(hall_detail=hall_detail_obj,
                                                                            booking_to_date__icontains=key)

            hall_booking_from_list = hall_booking_from_list.exclude(booking_status__in=[0, 10])
            hall_booking_to_list = hall_booking_to_list.exclude(booking_status__in=[0, 10])

            print hall_booking_from_list
            for i in range(0, len(hall_booking_from_list)):
                print '\nfrom time = ', hall_booking_from_list[i].booking_from_date.astimezone(to_zone).time()
                print '\nto_time = ', hall_booking_to_list[i].booking_to_date.astimezone(to_zone).time()
                if (value[0] < hall_booking_from_list[i].booking_from_date.astimezone(to_zone).time() and value[1] <
                    hall_booking_from_list[i].booking_from_date.astimezone(to_zone).time()) or \
                        (value[0] > hall_booking_to_list[i].booking_to_date.astimezone(to_zone).time() and
                         value[1] > hall_booking_to_list[i].booking_to_date.astimezone(to_zone).time()):
                    return True
                else:
                    return False
        return True

    except Exception, e:
        print e

        return False


# User Cancels Hall Booking From Confirmation Page
@csrf_exempt
@transaction.atomic
def cancel_booking(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_confirm.py | cancel_booking | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))

        try:
            HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).update(is_deleted=True)
        except Exception, e:
            pass

        # Change Booking Status in HallBooking, HallBookingDetail, HallCheckAvailability
        hall_booking_obj.booking_status = 0
        hall_booking_obj.save()
        today = datetime.now()
        for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
            hall_booking_detail.booking_status = 0
            hall_booking_detail.is_cancelled = True
            hall_booking_detail.cancellation_date = today
            hall_booking_detail.save()
            for hall_check_avail in HallCheckAvailability.objects.filter(hall_booking_detail=hall_booking_detail):
                hall_check_avail.booking_status = 0
                hall_check_avail.save()

        data['success'] = 'true'
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | hall_booking_confirm.py | cancel_booking | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | hall_booking_confirm.py | cancel_booking | User = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Save Offline Booking
@csrf_exempt
@transaction.atomic
def save_offline_booking(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print '\nRequest IN | hall_booking_confirm.py | save_offline_booking | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
        # hall_booking_obj.booking_status = 8
        # hall_booking_obj.save()
        hall_booking_obj.booking_no = str('HBK' + str(str.zfill(str(hall_booking_obj.id), 7)))
        hall_booking_obj.save()

        booking_sb_obj = HallBookingDetail.objects.filter(hall_location__location='MCCIA Trade Tower (5th Floor)',
                                                          pi_no__isnull=False).last()
        booking_tilak_obj = HallBookingDetail.objects.filter(hall_location__location='Tilak Road',
                                                             pi_no__isnull=False).last()
        booking_bhosari_obj = HallBookingDetail.objects.filter(hall_location__location='Bhosari',
                                                               pi_no__isnull=False).last()
        booking_hadapsar_obj = HallBookingDetail.objects.filter(hall_location__location='Hadapsar',
                                                                pi_no__isnull=False).last()

        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj).values(
            'hall_location').annotate(dcount=Count('hall_location'))
        for i in booking_detail_list:
            booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj,
                                                                  hall_location=i['hall_location']).last()
            hall_location = booking_detail_obj.hall_location.location

            if hall_location == 'MCCIA Trade Tower (5th Floor)':
                booking_detail_obj.pi_no = int(booking_sb_obj.pi_no) + 1
            elif hall_location == 'Tilak Road':
                booking_detail_obj.pi_no = int(booking_tilak_obj.pi_no) + 1
            elif hall_location == 'Bhosari':
                booking_detail_obj.pi_no = int(booking_bhosari_obj.pi_no) + 1
            elif hall_location == 'Hadapsar':
                booking_detail_obj.pi_no = int(booking_hadapsar_obj.pi_no) + 1

            booking_detail_obj.save()

        hall_booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj,
                                                     payable_amount=hall_booking_obj.total_payable,
                                                     created_by=str(request.user)
                                                     )
        hall_booking_payment_obj.save()

        user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
        if request.POST.get('retain_sd_flag') == 'false' and user_track_obj.deposit_available > 0:
            hall_booking_obj.deposit = user_track_obj.deposit_available
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(
                hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
            hall_booking_payment_obj.save()

            hall_booking_obj.deposit_status = 1
            hall_booking_obj.save()
            user_track_obj.deposit_available = 0
            user_track_obj.deposit_status = 1
            user_track_obj.save()

        if request.POST.get('cheque_flag') == 'true':
            hall_booking_obj.deposit = 0
            hall_booking_obj.is_deposit_through_cheque = True
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(
                hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
            hall_booking_payment_obj.save()
            if request.POST.get('retain_sd_flag') == 'true':
                hall_booking_obj.deposit_status = 0
            hall_booking_obj.save()
            user_track_obj.deposit_available = 0
            user_track_obj.deposit_status = 1
            user_track_obj.save()

        # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
        #     hall_booking_detail.booking_status = 8
        #     hall_booking_detail.save()
        #     for hall_check_avail in HallCheckAvailability.objects.filter(hall_booking_detail=hall_booking_detail):
        #         hall_check_avail.booking_status = 8
        #         hall_check_avail.save()

        transaction.savepoint_commit(sid)
        send_mail_count = 'FIRST'
        send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
        send_booking_invoice_mail_locationvise(request, hall_booking_obj)
        data['success'] = 'true'
        print '\nResponse OUT | hall_booking_confirm.py | save_offline_booking | User = ', request.user
    except Exception, e:
        print '\nException IN | hall_booking_confirm.py | save_offline_booking | Excp = ', str(traceback.print_exc())
        transaction.rollback(sid)
        data['success'] = 'false'
    return HttpResponse(json.dumps(data), content_type='application/json')


# save pay later booking
@csrf_exempt
@transaction.atomic
def save_pay_later_booking(request):
    sid = transaction.savepoint()
    data = {}
    try:
        print '\nRequest IN | hall_booking_confirm.py | save_pay_later_booking | User = ', request.user
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
        # hall_booking_obj.booking_status = 8
        # hall_booking_obj.save()


        hall_booking_payment_obj = HallPaymentDetail(hall_booking=hall_booking_obj,
                                                     payable_amount=hall_booking_obj.total_payable,
                                                     created_by=str(request.user),
                                                     # hall_booking__pay_later=True,
                                                     )
        hall_booking_payment_obj.save()



        user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
        if request.POST.get('retain_sd_flag') == 'false' and user_track_obj.deposit_available > 0:
            hall_booking_obj.deposit = user_track_obj.deposit_available
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(
                hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
            hall_booking_payment_obj.save()

            hall_booking_obj.deposit_status = 1
            hall_booking_obj.save()
            user_track_obj.deposit_available = 0
            user_track_obj.deposit_status = 1
            user_track_obj.save()

        if request.POST.get('cheque_flag') == 'true':
            hall_booking_obj.deposit = 0
            hall_booking_obj.is_deposit_through_cheque = True
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(
                hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            hall_booking_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable)
            hall_booking_payment_obj.save()
            if request.POST.get('retain_sd_flag') == 'true':
                hall_booking_obj.deposit_status = 0
            hall_booking_obj.save()
            user_track_obj.deposit_available = 0
            user_track_obj.deposit_status = 1
            user_track_obj.save()

        # for hall_booking_detail in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj):
        #     hall_booking_detail.booking_status = 8
        #     hall_booking_detail.save()
        #     for hall_check_avail in HallCheckAvailability.objects.filter(hall_booking_detail=hall_booking_detail):
        #         hall_check_avail.booking_status = 8
        #         hall_check_avail.save()

        transaction.savepoint_commit(sid)
        send_mail_count = 'FIRST'
        send_booking_invoice_mail(request, hall_booking_obj, send_mail_count)
        send_booking_invoice_mail_locationvise(request, hall_booking_obj)
        data['success'] = 'true'
        print '\nResponse OUT | hall_booking_confirm.py | save_pay_later_booking | User = ', request.user
    except Exception, e:
        print '\nException IN | hall_booking_confirm.py | save_pay_later_booking | Excp = ', str(traceback.print_exc())
        transaction.rollback(sid)
        data['success'] = 'false'
    return HttpResponse(json.dumps(data), content_type='application/json')

# function take input of the datestring like 2018-10-15
def get_financial_year(datestring):
    date = datetime.strptime(datestring, "%Y-%m-%d").date()
    # initialize the current year
    year_of_date = date.year
    # initialize the current financial year start date
    financial_year_start_date = datetime.strptime(str(year_of_date) + "-04-01", "%Y-%m-%d").date()
    if date < financial_year_start_date:
        return str(financial_year_start_date.year - 1)[2:] + '-' + str(financial_year_start_date.year)[2:]
    else:
        return str(financial_year_start_date.year)[2:] + '-' + str(financial_year_start_date.year + 1)[2:]


# Send Mail Just After Hall Booking - Temporary Booking Invoice
def send_booking_invoice_mail(request, hall_booking_obj, send_mail_count):  # hall_booking_obj
    try:
        print '\nRequest IN | hall_booking_confirm.py | send_booking_invoice_mail | User = ', request.user
        print '\n\n', send_mail_count
        ctx = {}
        booking_info_list = []
        to_receiver_list = []
        cc_receiver_list = []
        temp_cc_receiver_list = []
        chck_flag = True
        # hall_booking_obj.invoice_total_rent = final_total
        # hall_booking_obj.save()

        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True,
                                                               is_deleted=False)
        booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).first()
        booking_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).last()
       
        #
        # if booking_payment_obj.payment_mode == 0:
        #     print ("-------offline-----")
        # else:
        #     print("--------online--------")
        email_hall_location = booking_detail_obj.hall_location.location
        if email_hall_location == 'MCCIA Trade Tower (5th Floor)':
            email_username = "hallbkg_mtt@mcciapune.com"
            email_paswd = "hallbkg@2011mtt"
        elif email_hall_location == 'Tilak Road':
            email_username = "hallbkg_tilakrd@mcciapune.com"
            email_paswd = "hallbkg@2011tilakrd"
        elif email_hall_location == 'Bhosari':
            email_username = "hallbkg_bhosari@mcciapune.com"
            email_paswd = "hallbkg@2011bhosari"
        elif email_hall_location == 'Hadapsar':
            email_username = "hallbkg_hadapsar@mcciapune.com"
            email_paswd = "Hall@2018bkghadap"

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
        # to_receiver_list.append('shubhamshirsode1@gmail.com')

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

        current_date = datetime.now().strftime("%Y-%m-%d")
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

            cc_receiver_list.append(str(item.hall_detail.hall_location.contact_person1.email))
            if item.hall_detail.hall_location.contact_person2:
                cc_receiver_list.append(str(item.hall_detail.hall_location.contact_person2.email))
            i = i + 1

        temp_cc_receiver_list = set(cc_receiver_list)
        cc_receiver_list = list(temp_cc_receiver_list)
        cc_receiver_list.append('shubham.bharti@bynry.com')
        cc_receiver_list.append('vijendra.chandel@bynry.com')
        # cc_receiver_list = []   

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
                    datetime.strftime(payment.payment_date, '%d/%m/%Y'))

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
               'booking_detail_obj': booking_detail_obj,'chck_flag_val':chck_flag,
               'result' : result,'remaining_amt' : str(remaining_amt),'total':str(total),
               'booking_info_list': booking_info_list, 'half_gst_amount': format(half_gst_amount, '.2f'),
               'booking_payment_obj': booking_payment_obj, 'send_mail_count': str(send_mail_count),
               'date': str(datetime.strftime(datetime.today(), '%d.%m.%Y'))}

        imgpath = os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        fp = open(imgpath, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<img1>')

        username = email_username
        pswd = email_paswd

        admin_html = get_template('hallbooking/customer_booking_mail.html').render(Context(ctx))

        admin_htmlfile = MIMEText(admin_html, 'html', _charset=charset)

        admin_msg = MIMEMultipart('related')
        admin_msg.attach(admin_htmlfile)
        admin_msg.attach(msgImage)

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(username, pswd)

        TO = to_receiver_list
        CC = cc_receiver_list
        # TO_ADMIN = cc_receiver_list

        admin_msg['subject'] = 'Hall Booking Proforma Invoice - MCCIA'
        admin_msg['from'] = 'mailto: <' + email_username + '>'
        admin_msg['to'] = ",".join(TO)
        admin_toaddrs = TO + CC

        # server.sendmail(cust_msg['from'], cust_toaddrs, cust_msg.as_string())
        server.sendmail(admin_msg['from'], admin_toaddrs, admin_msg.as_string())
        server.quit()
        print '\nResponse OUT | hall_booking_confirm.py | send_booking_invoice_mail | MAIL SENT = ', request.user
    except Exception, e:
        print '\nException IN | hall_booking_confirm.py | send_booking_invoice_mail | EXCP = ', str(
            traceback.print_exc())
    return


# Send Mail Just After Hall Booking - Temporary Booking Invoice
def send_booking_invoice_mail_locationvise(request, hall_booking_obj):
    try:
        # pdb.set_trace()
        print '\nRequest IN | hall_booking_confirm.py | send_booking_invoice_mail_locationvise | '
        ctx = {}

        # exclude_hall_booking_list = HallBooking.objects.filter(Q(user_track_id=hall_booking_obj.user_track.id),~Q(payment_status=1)).exclude(id=hall_booking_obj.id)

        # hall_booking_obj = HallBooking.objects.get(id=85365)
        booking_detail_obj = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).order_by(
            'booking_from_date').first()
        booking_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).last()
        booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_active=True,
                                                               is_deleted=False).values('hall_location').annotate(
            dcount=Count('hall_location'))

        total_paid_by_deposit = 0
        hall_payment_deposit_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj,
                                                                     offline_payment_by=3, is_deleted=False).aggregate(
            total_paid=Sum('paid_amount'))
        if hall_payment_deposit_dict['total_paid']:
            total_paid_by_deposit = Decimal(hall_payment_deposit_dict['total_paid'])
        security_deposit = Decimal(hall_booking_obj.deposit) + total_paid_by_deposit

        for obj in booking_detail_list:
            final_booking_detail_list = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj,
                                                                         hall_location=obj['hall_location'],
                                                                         is_active=True, is_deleted=False)

            booking_info_list = []
            to_receiver_list = []
            cc_receiver_list = []
            temp_to_receiver_list = []

            i = 1

            pi_no_hbk_obj = HallBookingDetail.objects.filter(hall_location=obj['hall_location'],
                                                             hall_booking=hall_booking_obj).last()
            pi_no = pi_no_hbk_obj.pi_no
            hall_location = pi_no_hbk_obj.hall_location.location
            regards_mark = pi_no_hbk_obj.hall_location.contact_person1.name

            current_date = datetime.now().strftime("%Y-%m-%d")
            get_financial = get_financial_year(current_date)

            sb_contact_person = ''
            tilak_contact_person = ''
            bpi_contact_person = ''
            hpi_contact_person = ''

            office_name = ''

            if hall_location == 'MCCIA Trade Tower (5th Floor)':
                office_name = 'SB Road Office'
                sb_contact_person = pi_no_hbk_obj.hall_location.contact_person1.name + ' (SB Road Office) ' + ' ' + pi_no_hbk_obj.hall_location.contact_person1.email + ' ' + pi_no_hbk_obj.hall_location.contact_person1.contact_no
                pi_no = 'PI/' + str(get_financial) + '/' + str(pi_no)
                email_username = "hallbkg_mtt@mcciapune.com"
                email_paswd = "hallbkg@2011mtt"
            elif hall_location == 'Tilak Road':
                office_name = 'Tilak Road Office'
                tilak_contact_person = pi_no_hbk_obj.hall_location.contact_person1.name + ' (Tilak Road Office) ' + ' ' + pi_no_hbk_obj.hall_location.contact_person1.email + ' ' + pi_no_hbk_obj.hall_location.contact_person1.contact_no
                pi_no = 'TPI/' + str(get_financial) + '/' + str(pi_no)
                email_username = "hallbkg_tilakrd@mcciapune.com"
                email_paswd = "hallbkg@2011tilakrd"
            elif hall_location == 'Bhosari':
                office_name = 'Bhosari Office'
                bpi_contact_person = pi_no_hbk_obj.hall_location.contact_person1.name + ' (Bhosari Office) ' + ' ' + pi_no_hbk_obj.hall_location.contact_person1.email + ' ' + pi_no_hbk_obj.hall_location.contact_person1.contact_no
                pi_no = 'BPI/' + str(get_financial) + '/' + str(pi_no)
                email_username = "hallbkg_bhosari@mcciapune.com"
                email_paswd = "hallbkg@2011bhosari"
            elif hall_location == 'Hadapsar':
                office_name = 'Hadapsar Office'
                hpi_contact_person = pi_no_hbk_obj.hall_location.contact_person1.name + ' (Hadapsar Office) ' + ' ' + pi_no_hbk_obj.hall_location.contact_person1.email + ' ' + pi_no_hbk_obj.hall_location.contact_person1.contact_no
                pi_no = 'HPI/' + str(get_financial) + '/' + str(pi_no)
                email_username = "hallbkg_hadapsar@mcciapune.com"
                email_paswd = "Hall@2018bkghadap"

            sd_remark = ''
            final_security_deposit = 0
            if int(security_deposit):
                if hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 0:
                    sd_remark = '(The cheque amount has been retained at MCCIA)'
                elif hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 1:
                    sd_remark = '(The cheque towards SD has been returned)'
                elif hall_booking_obj.user_track:
                    user_track_obj = UserTrackDetail.objects.get(id=hall_booking_obj.user_track.id)
                    if int(user_track_obj.deposit_available):
                        sd_remark = '(Retained with MCCIA)'

            else:
                if hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 0:
                    sd_remark = '(The cheque amount has been retained at MCCIA)'
                elif hall_booking_obj.is_deposit_through_cheque and hall_booking_obj.deposit_status == 1:
                    sd_remark = '(The cheque towards SD has been returned)'

            if booking_detail_obj.hall_location.location == hall_location:
                final_security_deposit = security_deposit
            else:
                final_security_deposit = 0
                sd_remark = '(Added in ' + booking_detail_obj.hall_location.location + ' Proforma Invoice)'

            # Old code
            # sd_remark  = ''
            # final_security_deposit = 0
            # if int(security_deposit):                
            #     if booking_detail_obj.hall_location.location == hall_location:
            #         final_security_deposit = security_deposit
            #     else:
            #         final_security_deposit = 0
            #         sd_remark = '(Added in '+ booking_detail_obj.hall_location.location +' Proforma Invoice)'
            # else:
            #     sd_remark = '(Retained with MCCIA)'

            sub_total = 0
            sub_total_for_discount_calulation = 0
            for item in final_booking_detail_list:
                j = 1
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
                        sub_total_for_discount_calulation = sub_total_for_discount_calulation + float(
                            facility_obj['amount'])
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
                sub_total_for_discount_calulation = sub_total_for_discount_calulation + float(
                    item.first_total_rent_for_reference)

                booking_info_list.append({
                    'sr_no': i,
                    'hall_name': str(item.hall_detail.hall_name) + ' (' + office_name + ')',
                    'booking_date': str(item.booking_from_date.strftime('%d-%B-%Y')),
                    'booking_time': str(item.booking_from_date.strftime('%I:%M %p')) + ' - ' + str(
                        item.booking_to_date_for_reference.strftime('%I:%M %p')),
                    'amount': str(item.first_total_rent_for_reference),
                    'facility_info_list': facility_info_list
                })
                to_receiver_list.append(str(item.hall_detail.hall_location.contact_person1.email))
                if item.hall_detail.hall_location.contact_person2:
                    to_receiver_list.append(str(item.hall_detail.hall_location.contact_person2.email))
                # to_receiver_list.append('shubham.shirsode@bynry.com') 
                i = i + 1

            cc_receiver_list.append('shubham.bharti@bynry.com')
            cc_receiver_list.append('vijendra.chandel@bynry.com')

            temp_to_receiver_list = set(to_receiver_list)
            to_receiver_list = list(temp_to_receiver_list)

            sub_discount_total = 0
            discount_per = 0
            total_discount = 0
            if booking_detail_obj.hall_booking.is_discount:
                discount_per = str(int(booking_detail_obj.hall_booking.discount_per)) + '%'
                total_discount = (Decimal(booking_detail_obj.hall_booking.discount_per) / 100) * (
                    Decimal(sub_total_for_discount_calulation))
                total_discount = round(Decimal(total_discount), 2)
                sub_discount_total = Decimal(sub_total) - Decimal(total_discount)
                half_gst_amount = round((sub_discount_total * Decimal(hall_booking_obj.gst_tax) / (2 * 100)), 2)
                total_tax = half_gst_amount * 2
                final_total = Decimal(sub_discount_total) + Decimal(final_security_deposit) + Decimal(total_tax)
                final_total = round(final_total, 0)
            else:
                half_gst_amount = round((Decimal(sub_total) * Decimal(hall_booking_obj.gst_tax) / (2 * 100)), 2)
                total_tax = half_gst_amount * 2
                final_total = Decimal(sub_total) + Decimal(final_security_deposit) + Decimal(total_tax)
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
                    payment_mode = "Cheque"+'/'+ payment.cheque_no + '/' + payment.bank_name +'/'+  str(datetime.strftime(payment.cheque_date, '%d/%m/%Y'))

                elif payment.offline_payment_by == '2':
                    payment_mode = " NEFT"+'/'+ payment.neft_id

                elif payment.offline_payment_by == '1':
                    payment_mode = "Cash"+'/'+ payment.cash_no

                elif payment.offline_payment_by == '3':
                    payment_mode = "Deposit"

                elif payment.payment_mode == 1:
                    payment_mode = "Online" + '/' + str(
                        datetime.strftime(payment.payment_date, '%d/%m/%Y'))


                record['payment_mode'] = payment_mode
                record['paid_amount'] = str(payment.paid_amount)
                i = i + 1

                result.append(record)

                total = float(payment.paid_amount) + float(total)

            remaining_amt = float(final_total) - float(total)

            ctx['total_discount'] = total_discount
            ctx['sub_discount_total'] = round(sub_discount_total, 0)
            ctx['discount_per'] = discount_per
            ctx['sd_remark'] = sd_remark
            ctx['regards_mark'] = regards_mark
            ctx['result'] = result
            ctx['total'] = total
            ctx['remaining_amt'] = remaining_amt
            ctx['regards_mark'] = regards_mark
            ctx['hpi_contact_person'] = hpi_contact_person
            ctx['bpi_contact_person'] = bpi_contact_person
            ctx['sb_contact_person'] = sb_contact_person
            ctx['tilak_contact_person'] = tilak_contact_person
            ctx['final_total'] = format(final_total, '.2f')
            ctx['security_deposit'] = final_security_deposit
            ctx['total_tax'] = format(total_tax, '.2f')
            ctx['sub_total'] = format(sub_total, '.2f')
            ctx['pi_no'] = pi_no
            ctx['hall_booking_obj'] = hall_booking_obj
            ctx['booking_detail_obj'] = booking_detail_obj
            ctx['booking_info_list'] = booking_info_list
            ctx['half_gst_amount'] = format(half_gst_amount, '.2f')
            ctx['booking_payment_obj'] = booking_payment_obj
            ctx['date'] = str(datetime.strftime(datetime.today(), '%d.%m.%Y'))

            # ctx = {'total_discount':total_discount,'sub_discount_total':round(sub_discount_total,0),'discount_per':discount_per,'sd_remark':sd_remark,'regards_mark':regards_mark,'hpi_contact_person':hpi_contact_person,'bpi_contact_person':bpi_contact_person,'sb_contact_person':sb_contact_person,'tilak_contact_person':tilak_contact_person,'final_total':format(final_total, '.2f'),'security_deposit':final_security_deposit,'total_tax':format(total_tax, '.2f'),'sub_total':format(sub_total, '.2f'),'pi_no':pi_no,'hall_booking_obj': hall_booking_obj, 'booking_detail_obj': booking_detail_obj,
            # 'booking_info_list': booking_info_list, 'half_gst_amount': format(half_gst_amount, '.2f'),
            # 'booking_payment_obj': booking_payment_obj,
            # 'date': str(datetime.strftime(datetime.today(), '%d.%m.%Y'))}

            imgpath = os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
            fp = open(imgpath, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<img1>')
            username = email_username
            pswd = email_paswd

            admin_html = get_template('hallbooking/hall_bkng_invoice.html').render(Context(ctx))
            admin_htmlfile = MIMEText(admin_html, 'html', _charset=charset)
            admin_msg = MIMEMultipart('related')
            admin_msg.attach(admin_htmlfile)
            admin_msg.attach(msgImage)

            server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
            server.ehlo()
            server.starttls()
            server.login(username, pswd)

            TO = to_receiver_list
            CC = cc_receiver_list
            # TO_ADMIN = cc_receiver_list

            admin_msg['subject'] = 'Hall Booking Proforma Invoice - MCCIA'
            admin_msg['from'] = 'mailto: <' + username + '>'
            admin_msg['to'] = ",".join(TO)
            # msg['cc'] = ",".join(CC)
            # cust_toaddrs = TO
            admin_toaddrs = TO + CC

            # server.sendmail(cust_msg['from'], cust_toaddrs, cust_msg.as_string())
            server.sendmail(admin_msg['from'], admin_toaddrs, admin_msg.as_string())
            server.quit()
        print '\nResponse OUT | hall_booking_confirm.py | send_booking_invoice_mail_locationvise | MAIL SENT'
    except Exception, e:
        print '\nException IN | hall_booking_confirm.py | send_booking_invoice_mail_locationvise | EXCP = ', str(
            traceback.print_exc())
    return
