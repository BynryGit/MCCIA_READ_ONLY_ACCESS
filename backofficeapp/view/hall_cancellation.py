# System Module
import json
import pdb

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
import traceback
from decimal import Decimal
from datetime import datetime,timedelta

# User Module
from backofficeapp.models import SystemUserProfile
from hallbookingapp.models import HallLocation, HallCancelPolicy, HallBookingDetail, \
    HallBooking, HallPaymentDetail, HallCheckAvailability, UserTrackDetail
from adminapp.models import Servicetax
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


# Render Cancellation Policy Landing Page
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Cancellation Policy'],login_url='/backofficeapp/login/',raise_exception=True)
def cancellation_policy_landing(request):
    print '\nRequest IN & OUT | hall_cancellation.py | cancellation_policy_landing | User = ', request.user
    return render(request, 'backoffice/hall_booking/hall_cancel_policy_landing.html')


# Render Add New Policy Page
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Cancellation Policy'],login_url='/backofficeapp/login/',raise_exception=True)
def add_new_policy_landing(request):
    print '\nRequest IN & OUT | hall_cancellation.py | add_new_policy_landing | User = ', request.user
    return render(request, 'backoffice/hall_booking/add_new_policy.html')


# Save New Cancellation Policy
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Cancellation Policy'],login_url='/backofficeapp/login/',raise_exception=True)
@transaction.atomic
@csrf_exempt
def save_new_cancel_policy(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_cancellation.py | save_new_cancel_policy | User = ', request.user
        new_hall_cancel_policy_obj = HallCancelPolicy(day_range=str(request.POST.get('from_day')) + '-' + str(request.POST.get('to_day')),
                                                      charges=Decimal(request.POST.get('charges')),
                                                      created_by=str(request.user))
        new_hall_cancel_policy_obj.save()
        transaction.savepoint_commit(sid)
        data['success'] = 'true'
        print '\nResponse OUT | hall_cancellation.py | save_new_cancel_policy | User = ', request.user
    except Exception,e:
        print '\nException IN | hall_cancellation.py | save_new_cancel_policy | Excp = ',str(traceback.print_exc())
        transaction.rollback(sid)
        data['success'] = 'false'
    return HttpResponse(json.dumps(data), content_type='application/json')


# Load Cancellation Policy Datatable
def get_hall_cancel_policy_table(request):
    try:
        print '\nRequest IN | hall_cancellation.py | get_hall_cancel_policy_table | User = ', request.user
        data_list = []

        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        if searchTxt:
            pass
        else:
            searchTxt = request.GET.get('search_text')

        policy_list = HallCancelPolicy.objects.all()
        total_records = policy_list.count()
        policy_list = policy_list[start:length] if length != -1 else policy_list[::-1]
        total_record = total_records

        i = 1
        for policy in policy_list:
            temp_list = []
            temp_list.append(i)
            temp_list.append(policy.day_range)
            temp_list.append(str(policy.charges))
            if policy.is_deleted:
                status = '<label class="label label-default"> De-Active </label>'
            else:
                status = '<label class="label label-success"> Active </label>'

            temp_list.append(status)
            temp_list.append('None')
            i = i + 1
            data_list.append(temp_list)

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': data_list}
    except Exception, e:
        print '\nException IN | hall_cancellation.py | get_hall_cancel_policy_table | EXCP = ', str(traceback.print_exc())
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Cancel Single Booking Detail
@transaction.atomic
@csrf_exempt
def cancel_booking_detail(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_cancellation.py | cancel_booking_detail | User = ', request.user
        booking_detail_obj = HallBookingDetail.objects.get(id=request.POST.get('booking_detail_id'))
        hall_booking_obj = booking_detail_obj.hall_booking
        cancel_booking_count = HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_cancelled=False).count()
        hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()
        gst_obj = Servicetax.objects.get(tax_type=0, is_active=True)
        cancel_date = datetime.strptime(str(request.POST.get('cancel_date')), '%d/%m/%Y')

        total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).aggregate(total_paid=Sum('paid_amount'))

        if cancel_booking_count == 1:
            today = datetime.now().date()
            exclude_hall_booking_list = []
            if hall_booking_obj.member:
                exclude_hall_booking_list = HallBookingDetail.objects.filter(
                    hall_booking__member_id=hall_booking_obj.member.id, booking_from_date__gte=today).exclude(hall_booking=hall_booking_obj)
            elif hall_booking_obj.user_track:
                exclude_hall_booking_list = HallBookingDetail.objects.filter(hall_booking__user_track_id=hall_booking_obj.user_track.id, booking_from_date__gte=today).exclude(hall_booking=hall_booking_obj)

            old_deposit = hall_booking_obj.deposit
            hall_booking_obj.deposit = 0
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
            hall_payment_obj.save()
            if len(exclude_hall_booking_list) == 0:
                if total_paid_dict['total_paid'] != 0:
                    hall_booking_obj.refund_amount = hall_booking_obj.refund_amount + old_deposit
                    hall_booking_obj.save()
                if hall_booking_obj.user_track:
                    hall_booking_obj.user_track.deposit_available = 0
                    hall_booking_obj.user_track.save()

        if str(request.POST.get('cancel_type')) == '1' and request.POST.get('hall_shifting') == 'on':
            booking_detail_obj.cancellation_date = cancel_date.date()
            booking_detail_obj.is_cancelled = True
            booking_detail_obj.cancellation_percent = Decimal(25)
            booking_detail_obj.cancellation_type = 1
            booking_detail_obj.cancellation_amount = Decimal(booking_detail_obj.total_rent * 25/100)
            booking_detail_obj.save()
            booking_detail_obj.cancellation_gst = Decimal(booking_detail_obj.cancellation_amount * Decimal(float(gst_obj.tax) / 100))
            booking_detail_obj.save()
            # booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
            # booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
            hall_booking_obj.total_cancellation_amount = hall_booking_obj.total_cancellation_amount + booking_detail_obj.cancellation_amount
            hall_booking_obj.save()
        elif str(request.POST.get('cancel_type')) == '1':
            booking_detail_obj.cancellation_date = cancel_date.date()
            booking_detail_obj.cancellation_type = 1
            booking_detail_obj.cancellation_percent = Decimal(0)
            booking_detail_obj.cancellation_amount = Decimal(0)
            booking_detail_obj.cancellation_gst = Decimal(0)
            booking_detail_obj.save()
        else:
            total_days = (booking_detail_obj.booking_from_date.date() - cancel_date.date()).days
            check_flag = False
            for policy in HallCancelPolicy.objects.filter(is_active=True, is_deleted=False):
                day_range_list = policy.day_range.split('-')
                if total_days in range(int(day_range_list[0]), int(day_range_list[1])+1):
                    check_flag = True
                    booking_detail_obj.cancellation_date = cancel_date.date()
                    booking_detail_obj.cancellation_percent = Decimal(policy.charges)
                    booking_detail_obj.cancellation_amount = Decimal(booking_detail_obj.total_rent * policy.charges / 100)
                    booking_detail_obj.save()
                    booking_detail_obj.cancellation_gst = Decimal(booking_detail_obj.cancellation_amount * Decimal(float(gst_obj.tax) / 100))
                    # booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
                    # booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
                    booking_detail_obj.save()
                    hall_booking_obj.total_cancellation_amount = hall_booking_obj.total_cancellation_amount + booking_detail_obj.cancellation_amount
                    hall_booking_obj.save()
            if check_flag is False:
                booking_detail_obj.cancellation_date = cancel_date.date()
                booking_detail_obj.cancellation_percent = Decimal(0)
                booking_detail_obj.cancellation_amount = Decimal(0)
                booking_detail_obj.cancellation_gst = Decimal(0)
                booking_detail_obj.save()
                hall_booking_obj.total_cancellation_amount = hall_booking_obj.total_cancellation_amount + booking_detail_obj.cancellation_amount
                hall_booking_obj.save()

        booking_detail_obj.cancellation_remark = str(request.POST.get('cancel_remark'))
        booking_detail_obj.is_cancelled = True
        booking_detail_obj.is_active = False
        booking_detail_obj.is_deleted = True
        booking_detail_obj.updated_by = str(request.user)
        booking_detail_obj.updated_date = datetime.now()
        booking_detail_obj.booking_status = 0
        booking_detail_obj.save()
        print '--------------is_cancelled----------',booking_detail_obj.is_cancelled 
        for hall_avail_item in HallCheckAvailability.objects.filter(hall_booking_detail=booking_detail_obj):
            hall_avail_item.booking_status = 0
            hall_avail_item.updated_by = str(request.user)
            hall_avail_item.updated_date = datetime.now()
            hall_avail_item.save()

        refund_amount = booking_detail_obj.total_rent - (booking_detail_obj.cancellation_amount)

        if hall_payment_obj.paid_amount > 0:
            hall_booking_obj.refund_amount = hall_booking_obj.refund_amount + refund_amount
            hall_booking_obj.save()

        hall_booking_obj.updated_by = str(request.user)
        hall_booking_obj.updated_date = datetime.now()
        hall_booking_obj.total_rent = hall_booking_obj.total_rent - refund_amount
        hall_booking_obj.save()
        hall_booking_obj.first_total_rent_for_reference = hall_booking_obj.total_rent
        hall_booking_obj.gst_amount = Decimal(hall_booking_obj.total_rent * Decimal(float(gst_obj.tax) / 100))
        hall_booking_obj.save()
        hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
        hall_booking_obj.save()
        hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
        hall_payment_obj.updated_by = str(request.user)
        hall_payment_obj.updated_date = datetime.now()
        hall_payment_obj.save()

        transaction.savepoint_commit(sid)

        print '\nResponse OUT | hall_cancellation.py | cancel_booking_detail | User = ', request.user
        data['success'] = 'true'
    except Exception, e:
        print '\nException IN | hall_cancellation.py | cancel_booking_detail | EXCP = ', str(traceback.print_exc())
        data['success'] = 'false'
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Cancel Whole Booking
@transaction.atomic
@csrf_exempt
def cancel_hall_booking(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_cancellation.py | cancel_hall_booking | User = ', request.user
        hall_rent_val = request.POST.get('hall_rent_val')
        hall_booking_obj = HallBooking.objects.get(id=request.POST.get('booking_id'))
        hall_payment_obj = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj).last()
        gst_obj = Servicetax.objects.get(tax_type=0, is_active=True)
        cancel_date = datetime.strptime(str(request.POST.get('cancel_date')), '%d/%m/%Y')
        flag = False

        total_paid_dict = HallPaymentDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False).aggregate(total_paid=Sum('paid_amount'))

        today = datetime.now().date()
        exclude_hall_booking_list = []
        if hall_booking_obj.member:
            exclude_hall_booking_list = HallBookingDetail.objects.filter(
                hall_booking__member_id=hall_booking_obj.member.id, booking_from_date__gte=today).exclude(
                hall_booking=hall_booking_obj)
        elif hall_booking_obj.user_track:
            exclude_hall_booking_list = HallBookingDetail.objects.filter(
                hall_booking__user_track_id=hall_booking_obj.user_track.id, booking_from_date__gte=today).exclude(
                hall_booking=hall_booking_obj)

        # old_deposit = hall_booking_obj.deposit
        # if total_paid_dict['total_paid'] == 0:
        #     hall_booking_obj.deposit = 0
        #     hall_booking_obj.save()
        #     if exclude_hall_booking_list.count() == 0:
        #         hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
        #         hall_booking_obj.save()
        #
        #         hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
        #         hall_payment_obj.save()
        #         if hall_booking_obj.user_track:
        #             hall_booking_obj.user_track.deposit_available = 0
        #             hall_booking_obj.user_track.save()
        # else:
        #     hall_booking_obj.deposit = 0
        #     hall_booking_obj.save()
        #     if exclude_hall_booking_list.count() == 0:
        #         hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
        #         hall_booking_obj.save()
        #         hall_booking_obj.refund_amount = hall_booking_obj.refund_amount + old_deposit
        #         hall_booking_obj.save()
        #         hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
        #         hall_payment_obj.save()
        #         if hall_booking_obj.user_track:
        #             hall_booking_obj.user_track.deposit_available = 0
        #             hall_booking_obj.user_track.save()

        old_deposit = hall_booking_obj.deposit
        hall_booking_obj.deposit = 0
        hall_booking_obj.save()
        hall_booking_obj.total_payable = round(hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
        hall_booking_obj.save()
        hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(total_paid_dict['total_paid'])
        hall_payment_obj.save()
        if len(exclude_hall_booking_list) == 0:
            if total_paid_dict['total_paid'] != 0:
                hall_booking_obj.refund_amount = hall_booking_obj.refund_amount + old_deposit
                hall_booking_obj.save()
            if hall_booking_obj.user_track:
                hall_booking_obj.user_track.deposit_available = 0
                hall_booking_obj.user_track.save()

        if str(request.POST.get('cancel_type')) == '1' and request.POST.get('hall_shifting') == 'on':
            for booking_detail_obj in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False):
                booking_detail_obj.cancellation_date = cancel_date.date()
                booking_detail_obj.cancellation_type = 1
                booking_detail_obj.save()
                booking_detail_obj.cancellation_percent = Decimal(25)
                booking_detail_obj.cancellation_amount = Decimal(booking_detail_obj.total_rent * 25/100)
                booking_detail_obj.save()
                booking_detail_obj.cancellation_gst = Decimal(booking_detail_obj.cancellation_amount * Decimal(float(gst_obj.tax) / 100))
                # booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
                # booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
                booking_detail_obj.save()
                hall_booking_obj.total_cancellation_amount = hall_booking_obj.total_cancellation_amount + booking_detail_obj.cancellation_amount
                hall_booking_obj.save()
        elif str(request.POST.get('cancel_type')) == '1':
            for booking_detail_obj in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False):
                flag = True
                booking_detail_obj.cancellation_date = cancel_date.date()
                booking_detail_obj.cancellation_type = 1
                booking_detail_obj.cancellation_percent = Decimal(0)
                booking_detail_obj.cancellation_amount = Decimal(0)
                booking_detail_obj.cancellation_gst = Decimal(0)
                # booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
                # booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
                booking_detail_obj.save()
        else:
            for booking_detail_obj in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False):
                total_days = (booking_detail_obj.booking_from_date.date() - cancel_date.date()).days
                flag = True
                check_flag = False
                for policy in HallCancelPolicy.objects.filter(is_active=True, is_deleted=False):
                    day_range_list = policy.day_range.split('-')
                    if total_days in range(int(day_range_list[0]), int(day_range_list[1]) + 1):
                        check_flag = True
                        booking_detail_obj.cancellation_date = cancel_date.date()
                        booking_detail_obj.cancellation_percent = Decimal(policy.charges)
                        booking_detail_obj.cancellation_amount = Decimal(
                            booking_detail_obj.total_rent * policy.charges / 100)
                        booking_detail_obj.save()
                        booking_detail_obj.cancellation_gst = Decimal(
                            booking_detail_obj.cancellation_amount * Decimal(float(gst_obj.tax) / 100))
                        # booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
                        # booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
                        booking_detail_obj.save()
                        hall_booking_obj.total_cancellation_amount = hall_booking_obj.total_cancellation_amount + booking_detail_obj.cancellation_amount
                        hall_booking_obj.save()
                    if check_flag is False:
                        booking_detail_obj.cancellation_date = cancel_date.date()
                        booking_detail_obj.cancellation_percent = Decimal(0)
                        booking_detail_obj.cancellation_amount = Decimal(0)
                        booking_detail_obj.cancellation_gst = Decimal(0)
                        # booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
                        # booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
                        booking_detail_obj.save()
                        hall_booking_obj.total_cancellation_amount = hall_booking_obj.total_cancellation_amount + booking_detail_obj.cancellation_amount
                        hall_booking_obj.save()

        for booking_detail_obj in HallBookingDetail.objects.filter(hall_booking=hall_booking_obj, is_deleted=False):
            booking_detail_obj.cancellation_remark = str(request.POST.get('cancel_remark'))
            booking_detail_obj.is_cancelled = True
            booking_detail_obj.is_active = False
            booking_detail_obj.is_deleted = True
            booking_detail_obj.updated_by = str(request.user)
            booking_detail_obj.updated_date = datetime.now()
            booking_detail_obj.booking_status = 0
            # booking_detail_obj.booking_from_date - timedelta(hours=5, minutes=30)
            # booking_detail_obj.booking_to_date - timedelta(hours=5, minutes=30)
            booking_detail_obj.save()
            refund_amount = booking_detail_obj.total_rent - (booking_detail_obj.cancellation_amount)
            print '------------total_rent--------',booking_detail_obj.total_rent
            print '-----------cancellation_amount---------',booking_detail_obj.cancellation_amount
            print '--------------------',refund_amount
            if hall_payment_obj.paid_amount > 0:
                hall_booking_obj.refund_amount = refund_amount
                hall_booking_obj.save()
            print '-------------table-------',hall_booking_obj.refund_amount
            hall_booking_obj.updated_by = str(request.user)
            hall_booking_obj.updated_date = datetime.now()
            hall_booking_obj.total_rent = hall_booking_obj.total_rent - refund_amount
            hall_booking_obj.save()
            hall_booking_obj.first_total_rent_for_reference = hall_booking_obj.total_rent
            hall_booking_obj.gst_amount = Decimal(hall_booking_obj.total_rent * Decimal(float(gst_obj.tax) / 100))
            hall_booking_obj.save()
            hall_booking_obj.total_payable = round(
                hall_booking_obj.total_rent + hall_booking_obj.deposit + hall_booking_obj.gst_amount, 0)
            hall_booking_obj.save()
            hall_payment_obj.payable_amount = Decimal(hall_booking_obj.total_payable) - Decimal(
                total_paid_dict['total_paid'])
            hall_payment_obj.save()

            for hall_avail_item in HallCheckAvailability.objects.filter(hall_booking_detail=booking_detail_obj):
                hall_avail_item.booking_status = 0
                hall_avail_item.updated_by = str(request.user)
                hall_avail_item.updated_date = datetime.now()
                hall_avail_item.save()

        hall_payment_obj.updated_by = str(request.user)
        hall_payment_obj.updated_date = datetime.now()
        hall_payment_obj.save()
        hall_booking_obj.booking_status = 0
        hall_booking_obj.save()

        transaction.savepoint_commit(sid)

        print '\nResponse OUT | hall_cancellation.py | cancel_hall_booking | User = ', request.user
        data['success'] = 'true'
        
    except Exception, e:
        print '\nException IN | hall_cancellation.py | cancel_hall_booking | EXCP = ', str(traceback.print_exc())
        data['success'] = 'false'
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')