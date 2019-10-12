# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
import json
from django.http import HttpResponse

import traceback
import datetime
from hallbookingapp.models import HallBooking,HallBookingDetail,HallLocation,HallDetail
from membershipapp.models import CompanyDetail

@csrf_exempt
def hall_booking_report_landing(request):
    hall_location_list = HallLocation.objects.filter(is_deleted=False)
    companyobjs=CompanyDetail.objects.filter(is_deleted=False).values('id','company_name')
    data = {'hall_location_list': hall_location_list,'companyobjs':companyobjs}
    return render(request, 'backoffice/hall_booking/hall_booking_report.html',data)

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


@csrf_exempt
def get_hall_regs_report_datatable(request):
    try:
        print 'backofficeapp | .py | get_hall_regs_datatable | user'
        dataList = []
        booking_details=[]
        total_record=0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        print searchTxt
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['','id']
        column_name = order + list[int(column)]
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        print request.GET.get('select_payment')
        print request.GET.get('select_payment')
        print request.GET.get('select_payment')
        print request.GET.get('select_payment')
        print request.GET.get('select_payment')

        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59,
                                                                                                   second=59)

        select_company_id=request.GET.get('select_company')

        if request.GET.get('select_company') !='all':
            if request.GET.get('select_payment') !='all':
                if request.GET.get('start_date') and request.GET.get('end_date'):
                    hallbookings = HallBooking.objects.values_list('id').filter(member__company_id=select_company_id,is_deleted=False,payment_status=request.GET.get('select_payment'),from_date__range=[start_date, end_date])
                else:
                    hallbookings = HallBooking.objects.values_list('id').filter(member__company_id=select_company_id,is_deleted=False)
            else:
                if request.GET.get('start_date') and request.GET.get('end_date'):
                    hallbookings = HallBooking.objects.values_list('id').filter(member__company_id=select_company_id,is_deleted=False,from_date__range=[start_date, end_date])
                else:
                    hallbookings = HallBooking.objects.values_list('id').filter(member__company_id=select_company_id,is_deleted=False)
        else:
            if request.GET.get('select_payment') !='all':
                if request.GET.get('start_date') and request.GET.get('end_date'):
                    hallbookings = HallBooking.objects.values_list('id').filter(is_deleted=False,payment_status=request.GET.get('select_payment'),from_date__range=[start_date, end_date])
                else:
                    hallbookings = HallBooking.objects.values_list('id').filter(is_deleted=False,
                                                          payment_status=request.GET.get('select_payment'))
            else:
                if request.GET.get('start_date') and request.GET.get('end_date'):
                    hallbookings = HallBooking.objects.values_list('id').filter(is_deleted=False,from_date__range=[start_date, end_date])
                else:
                    hallbookings = HallBooking.objects.values_list('id').filter(is_deleted=False)


        if request.GET.get('select_location') != "all" :
            booking_details = HallBookingDetail.objects.values_list('hall_booking_id').filter(hall_location_id=request.GET.get('select_location'))
        if request.GET.get('select_hall') != "all" :
            booking_details = booking_details.values_list('hall_booking_id').filter(hall_detail_id=request.GET.get('select_hall'))


        if booking_details:
            hallbookings=set(hallbookings).intersection(set(booking_details))

        hallbookings = filter(None, hallbookings)
        if searchTxt:
            pass

        total_record= len(hallbookings)
        hallbookings = hallbookings[start:length] if length > 1 else hallbookings
        i = 0
        a = 1
        for hallbooking in hallbookings:
            tempList = []
            i = start + a
            a = a + 1
            booking_details = HallBookingDetail.objects.filter(hall_booking_id=hallbooking)
            hall_name=''
            for booking_detail in booking_details:
                hall_name= (hall_name + "\n" if hall_name else '') + booking_detail.hall_detail.hall_name

            tempList.append(str(i))
            tempList.append(booking_detail.hall_booking.from_date.strftime('%B %d,%Y'))
            tempList.append(booking_detail.hall_booking.from_date.strftime('%H:%M:%p'))
            tempList.append(booking_detail.hall_booking.created_date.strftime('%B %d,%Y'))
            tempList.append(booking_detail.hall_booking.booking_no)
            tempList.append(hall_name)
            tempList.append("-")
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')
            tempList.append(booking_detail.hall_booking.contact_person)
            tempList.append(booking_detail.hall_booking.mobile_no)
            tempList.append(booking_detail.hall_booking.email)
            tempList.append(booking_detail.hall_booking.total_payable)
            tempList.append(booking_detail.hall_booking.get_booking_status_display())
            tempList.append('-')

            tempList.append("-")
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')

            tempList.append("-")
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')

            tempList.append("-")
            tempList.append('-')
            tempList.append('-')
            tempList.append('-')

            tempList.append('-')
            tempList.append('-')


            dataList.append(tempList)

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record,'aaData': dataList}
    except Exception as e:
        print 'Exception backofficeapp | event_home.py | get_events_datatable | user %s. Exception = ', str(traceback.
            print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0,'aaData': [ ]}
    return HttpResponse(json.dumps(data), content_type='application/json')