
# System Package

import json
import traceback
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
import itertools
from dateutil import tz
from django.db import transaction
from datetime import datetime, time, timedelta
from math import ceil
from decimal import Decimal
# User Models

from adminapp.models import Location,Hall_pricing
from membershipapp.models import CompanyDetail, UserDetail, MembershipInvoice
from hallbookingapp.models import Hall_booking_detail,HallLocation,HallDetail,HallPricing, HallCheckAvailability, HallBooking, HallEquipment, Holiday, UserTrackDetail, HallBookingDetail
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def landing(request):
    """
    Code for rendering.

    **Template:**

    :template:`landing_page.html`
    """
    return render(request,'landing_page.html')




def is_second_fourth(s):
    d = s
    return (d.weekday() == 5 and (8 <= d.day <= 14 or 22 <= d.day <= 28)) or (d.weekday() == 6)

def open_hallbooking_page(request,location_id=None, booking_id=None):
    """
    Code for displaying hall Details card on landing paage, and render on follwing HTML page
    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.HallDetail`.

    **Template:**

    :template:`hallbooking/hall_booking.html`
    """
    data={}
    hallpricings = ''
    halllist= []
    try:
        print '\nRequest IN | hallbooking_landing.py | open_hallbooking_page | User = ',request.user

        # Code for showing Book Now btn ON/OFF based on time #Start
        book_now_flag = 0
        today = datetime.now().date()
        
        if today in [item.holiday_date for item in Holiday.objects.filter(holiday_date__gte=today, status=True, is_deleted=False, holiday_status=False)]:
            book_now_flag = 0 
        elif (today.weekday() == 5 and (8 <= today.day <= 14 or 22 <= today.day <= 28)) or (today.weekday() == 6):
            book_now_flag = 0
        else:
            book_now_flag = 0
            booking_start_time = datetime.strptime('10:00 AM', '%I:%M %p').time()
            booking_end_time = datetime.strptime('04:00 PM', '%I:%M %p').time()
            current_time = datetime.now().time()
            if booking_start_time <= current_time <= booking_end_time:
                book_now_flag = 1
        # Code for showing Book Now btn ON/OFF based on time #End

        not_approved_member = [invoice_item.userdetail.id for invoice_item in MembershipInvoice.objects.filter(is_paid=True, is_deleted=False,
                                                                userdetail__member_associate_no__isnull=True)]
        new_not_approved_member = UserDetail.objects.filter(id__in=not_approved_member)

        member_list = UserDetail.objects.filter(member_associate_no__isnull=False,membership_type="MM",
                                                is_deleted=False).order_by('company__company_name')
        final_member_list = member_list | new_not_approved_member
        non_member_list = UserTrackDetail.objects.filter(is_blacklisted=False, is_deleted=False)

        user_detail_id = ''
        if not request.user.is_anonymous() and request.session['user_type'] != 'backoffice':
            user_detail_id = request.user.membershipuser.userdetail.id
            pass

        if location_id:
            hall_location = HallLocation.objects.get(id=location_id)
            halldetaillistobj = HallDetail.objects.filter(is_deleted=False, hall_location_id=location_id)
        else:
            hall_location = HallLocation.objects.filter(is_deleted=False).first()
            halldetaillistobj = HallDetail.objects.filter(is_deleted=False, hall_location_id=hall_location.id)

        if request.user.is_anonymous():
            halldetaillistobj = halldetaillistobj.filter(is_open_for_online=True)
        elif request.session['user_type'] != 'backoffice':
            halldetaillistobj = halldetaillistobj.filter(is_open_for_online=True)

        hall_detail_obj = halldetaillistobj.first()

        hallpricings = HallPricing.objects.filter(is_deleted=False)
        locationObj = HallLocation.objects.filter(is_deleted=False)
        
        contact_data=[]
        if hall_location:
            if hall_location.contact_person1:
                contact_dict = {}
                contact_dict['name']=hall_location.contact_person1.name
                contact_dict['phone']=hall_location.contact_person1.contact_no
                contact_dict['email']=hall_location.contact_person1.email
                contact_data.append(contact_dict)

            if hall_location.contact_person2:
                contact_dict = {}
                contact_dict['name']=hall_location.contact_person2.name
                contact_dict['phone']=hall_location.contact_person2.contact_no
                contact_dict['email']=hall_location.contact_person2.email
                contact_data.append(contact_dict)


        hall_detail_data=[]
        
        for halldetaillist in halldetaillistobj:
            hall_detail_dict = {}

            paid_facility_list = []
            free_facility_list = []
            hall_facility_list = HallEquipment.objects.filter(hall_detail=halldetaillist.id)
            for obj in hall_facility_list:
                if obj.member_charges != 0 and obj.non_member_charges != 0:
                    paid_facility_list.append(obj.hall_functioning_equipment.equipment_name)
                else:
                    free_facility_list.append(obj.hall_functioning_equipment.equipment_name)


            hallpricings=HallPricing.objects.filter(is_deleted=False,hall_detail=halldetaillist.id).order_by('hours')
            price_dict = {}
            for hallpricing in hallpricings:
                price_dict[hallpricing.hours]=[hallpricing.member_price,hallpricing.nonmember_price]

            price_dict['Extra'] = [halldetaillist.extra_member_price, halldetaillist.extra_nonmember_price]

            price_dict=sorted(price_dict.items())

            hall_detail_dict['hall_name']=halldetaillist.hall_name
            hall_detail_dict['id']=halldetaillist.id
            hall_detail_dict['paid_facility_list']=paid_facility_list
            hall_detail_dict['free_facility_list']=free_facility_list
            hall_detail_dict['capacity']=halldetaillist.capacity
            hall_detail_dict['seating_style']=halldetaillist.seating_style
            hall_detail_dict['hall_imag']=halldetaillist.hall_image.url
            hall_detail_dict['hall_charges']=price_dict
            hall_detail_dict['start_time'] = str(halldetaillist.booking_start_time.strftime('%I:%M %p'))
            hall_detail_dict['end_time'] = str(halldetaillist.booking_end_time.strftime('%I:%M %p'))

            hall_detail_data.append(hall_detail_dict)            
        data = {'non_member_list':non_member_list,'book_now_flag': book_now_flag,'contact_data':contact_data, 'locationObj': locationObj,
                'hall_location':hall_location,'hall_detail_dict':hall_detail_data,
                'booking_id': booking_id, "member_list": final_member_list, 'user_detail_id': user_detail_id,
                'hall_detail_obj': hall_detail_obj
                }
        print '\nResponse OUT | hallbooking_landing.py | open_hallbooking_page | User = ',request.user
    except Exception,e:
        print '\nException IN | hallbooking_landing.py | open_hallbooking_page | Excp = ',e
        pass
    # abc={'hall_detail_dict':hall_detail_data}
    return render(request, 'hallbooking/hall_booking.html',data)


def get_non_member_detail(request):
    """
    Code for getting nom member details which is stored in UserTrackDetails

    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.UserTrackDetail`.

    """
    data = {}
    try:
        print '\nRequest IN | hallbooking_landing | get_non_member_detail | user = ', request.user
        user_detail_obj = UserTrackDetail.objects.get(id=request.GET.get('non_mem_id'))
        data = {'success': 'true', 'address': str(user_detail_obj.address),
                'user_track_id' : user_detail_obj.id,
                'contact_person': str(user_detail_obj.contact_person),
                'designation': str(user_detail_obj.designation),
                'mobile_no': str(user_detail_obj.mobile_no),
                'email': str(user_detail_obj.email),
                'gst': str(user_detail_obj.gst),
            }
        print '\nResponse OUT | hallbooking_landing | get_non_member_detail | user = ', request.user, request.GET.get('mem_id')
    except Exception:
        data = {'success': 'false'}
        print '\nException IN | hallbooking_landing | get_non_member_detail | EXP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def get_hall_detail_location(request):
    """
    Code runs when user click on location wise hall details on landing page of hallbooking

    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.HallDetails`.

    """
    try:

        user_detail_id = ''
        user_type = 'anonymous'

        if not request.user.is_anonymous() and request.session['user_type'] == 'backoffice':
            user_type = 'backoffice'            

        if not request.user.is_anonymous() and request.session['user_type'] != 'backoffice':
            user_detail_id = request.user.membershipuser.userdetail.id
            pass

        # Code for showing Book Now btn ON/OFF based on time #Start
        book_now_flag = 0
        today = datetime.now().date()
        if today in [item.holiday_date for item in Holiday.objects.filter(holiday_date__gte=today, status=True, is_deleted=False, holiday_status=False)]:
            book_now_flag = 0
        elif (today.weekday() == 5 and (8 <= today.day <= 14 or 22 <= today.day <= 28)) or (today.weekday() == 6):
            book_now_flag = 0
        else:
            booking_start_time = datetime.strptime('10:00 AM', '%I:%M %p').time()
            booking_end_time = datetime.strptime('04:00 PM', '%I:%M %p').time()
            current_time = datetime.now().time()
            if booking_start_time <= current_time <= booking_end_time:
                book_now_flag = 1
        # Code for showing Book Now btn ON/OFF based on time #End       

        location_id=request.POST.get('location_id')
        if location_id:
            hall_location = HallLocation.objects.get(id=location_id)
            halldetaillistobj = HallDetail.objects.filter(is_deleted=False, hall_location_id=location_id)
        else:
            hall_location = HallLocation.objects.filter(is_deleted=False).first()
            halldetaillistobj = HallDetail.objects.filter(is_deleted=False, hall_location_id=hall_location.id)
            location_id = hall_location.id
        hall_detail_data = []

        if request.user.is_anonymous():
            halldetaillistobj = halldetaillistobj.filter(is_open_for_online=True)
        elif request.session['user_type'] != 'backoffice':
            halldetaillistobj = halldetaillistobj.filter(is_open_for_online=True)

        hall_detail_obj = halldetaillistobj.first()

        contact_data = []
        if hall_location:
            if hall_location.contact_person1:
                contact_dict = {}
                contact_dict['name'] = hall_location.contact_person1.name
                contact_dict['phone'] = hall_location.contact_person1.contact_no
                contact_dict['email'] = hall_location.contact_person1.email
                contact_data.append(contact_dict)

            if hall_location.contact_person2:
                contact_dict = {}
                contact_dict['name'] = hall_location.contact_person2.name
                contact_dict['phone'] = hall_location.contact_person2.contact_no
                contact_dict['email'] = hall_location.contact_person2.email
                contact_data.append(contact_dict)

        for halldetaillist in halldetaillistobj:
            hall_detail_dict = {}

            # equi_list = halldetaillist.hall_equipment.all()
            hallpricings = HallPricing.objects.filter(is_deleted=False, hall_detail=halldetaillist.id).order_by('hours')
            price_dict = {}

            for hallpricing in hallpricings:
                price_dict[hallpricing.hours] = [hallpricing.member_price, hallpricing.nonmember_price]

            price_dict['Extra'] = [halldetaillist.extra_member_price, halldetaillist.extra_nonmember_price]

            # price_dict = sorted(price_dict.items())
            # elist = []

            # for equi in equi_list:
            #     elist.append(equi.equipment_name)

            paid_facility_list = []
            free_facility_list = []
            hall_facility_list = HallEquipment.objects.filter(hall_detail=halldetaillist.id)
            for obj in hall_facility_list:
                if obj.member_charges != 0 and obj.non_member_charges != 0:
                    paid_facility_list.append(obj.hall_functioning_equipment.equipment_name)
                else:
                    free_facility_list.append(obj.hall_functioning_equipment.equipment_name)            


            hall_detail_dict['hall_name'] = halldetaillist.hall_name
            hall_detail_dict['id'] = halldetaillist.id
            # hall_detail_dict['hall_equipment'] = elist
            hall_detail_dict['paid_facility_list']=paid_facility_list
            hall_detail_dict['free_facility_list']=free_facility_list
            hall_detail_dict['capacity'] = halldetaillist.capacity
            hall_detail_dict['seating_style'] = halldetaillist.seating_style
            hall_detail_dict['hall_imag'] = halldetaillist.hall_image.url
            hall_detail_dict['hall_charges'] = price_dict
            hall_detail_dict['start_time'] = str(halldetaillist.booking_start_time.strftime('%I:%M %p'))
            hall_detail_dict['end_time'] = str(halldetaillist.booking_end_time.strftime('%I:%M %p'))

            hall_detail_data.append(hall_detail_dict)
        data={'success': 'true','hall_data': hall_detail_data,'user_detail_id': user_detail_id,
              'location_id': location_id,'contact_data': contact_data, 'user_type': user_type,
              'hall_start_time': str(hall_detail_obj.booking_start_time.strftime('%I:%M %p')),
              'hall_end_time': str(hall_detail_obj.booking_end_time.strftime('%I:%M %p')),
              'book_now_flag': book_now_flag}

        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception,e:
        print e
        pass
        data = {'success': 'false', 'hall_data': [], 'location_id': location_id}
        return HttpResponse(json.dumps(data), content_type='application/json')


def get_hallevent_calender_data(request):
    """
    Code runs when user click on check hall availibility, it shows hall wise calender

    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.HallCheckAvailability`.

    """
    try:
        print 'Request IN | hallbooking_landing | get_hallevent_calender_data | user'
        final_list = []
        halldeatil_id = request.GET.get('halldeatil_id')
        to_zone = tz.gettz("Asia/Kolkata")
        hallavailability_obj_list = []

        # from_zone = tz.tzutc()
        # to_zone = tz.gettz('Asia/Kolkata')

        halldeatil_obj = HallDetail.objects.get(id=request.GET.get('halldeatil_id'))
        if halldeatil_obj.is_merge:
            hall_merge_id_list = halldeatil_obj.hall_merge.split(',')  
            print 'hall_merge_id_list = ',hall_merge_id_list
            hallavailability_obj_list = HallCheckAvailability.objects.filter(hall_detail_id__in=hall_merge_id_list).exclude(booking_status__in=[0,10])            
        else:
            hallavailability_obj_list = HallCheckAvailability.objects.filter(hall_detail=halldeatil_obj,is_active=True,is_deleted=False)        
            hallavailability_obj_list = hallavailability_obj_list.exclude(booking_status__in=[0,10])
            print 'here--------------------------------------'

        for obj in hallavailability_obj_list:              
            start_date = str(obj.booking_from_date.astimezone(to_zone).strftime('%d %B %Y %I:%M %p'))
            end_date = str(obj.booking_to_date.astimezone(to_zone).strftime('%d %B %Y %I:%M %p'))

            new_date = start_date + ' -  <br>' + end_date
            if obj.booking_from_date.strftime("%d %M %Y") == obj.booking_to_date.strftime("%d %M %Y"):
                new_date = str(obj.booking_from_date.astimezone(to_zone).strftime('%d %B %Y %I:%M %p')) + ' - ' + str(obj.booking_to_date.astimezone(to_zone).strftime('%I:%M %p'))

            if obj.id == 25577:
                print '------------------------found-----------------------'
            
            # if obj.event_mode == 0:
            #     textColor = '#02a078'
            # elif obj.event_mode == 1:
            #     textColor = '#ff6679'
            # elif obj.event_mode == 2:
            #     textColor = '#4a90e2'

            textColor = '#4a90e2'            

            hall_event_dic = {
                'start':start_date,
                'end': end_date,
                'title': obj.hall_detail.hall_name,
                'url': '#',#/eventsapp/events-details/?event_detail_id='+str(obj.id),
                'color': '#eae4e4',
                'textColor': textColor,
                'new_date':new_date
                #'data': {}
            }
            final_list.append(hall_event_dic)
        data = {
            'success':'true',
            'final_list':final_list
        }        
        print 'Request OUT | event_landing | get_event_data | user',request.user
    except Exception as e:
        print 'Exception | event_landing | get_event_data | user %s. Exception = ', str(traceback.print_exc())
        data ={'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')  


def open_hallbooking_form(request, hall_id=None, booking_id=None):
    """
    Code runs when user click on Book Now button then it open hall booking form

    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.HallDetail`.

    """
    data = {}
    try:
        print '\nRequest IN | hallbooking_landing | open_hallbooking_form | user = ', request.user
        user_detail_id = 'not_login'
        hall_booking_obj = 'no_obj'

        hall_detail_obj = HallDetail.objects.get(id=hall_id)

        member_list = UserDetail.objects.filter(member_associate_no__isnull=False, membership_type="MM", is_deleted=False)
        if not request.user.is_anonymous():
            user_detail_id = request.user.membershipuser.userdetail.id

        if booking_id:
            hall_booking_obj = HallBooking.objects.get(id=booking_id)

        data = {"hall_detail_obj": hall_detail_obj, "member_list": member_list,
                'user_detail_id': user_detail_id, 'hall_booking_obj': hall_booking_obj
                }
        print data

        print '\nResponse OUT | hallbooking_landing | open_hallbooking_form | user = ', request.user
        return render(request, 'hallbooking/hall_bookings_form.html', data)
    except Exception,e:
        print '\nException IN | hallbooking_landing | open_hallbooking_form | EXP = ', str(traceback.print_exc())
        return HttpResponse(status=500)


def additional_facility_details(request):
    data = {}
    from_zone = tz.tzutc()
    to_zone = tz.gettz('Asia/Kolkata')
    sid = transaction.savepoint()
    booking_detail_no = int(datetime.now().strftime('%Y%m%d%H%M%S'))
    try:
        data_list = []
        equipment_name_list = []
        facility_list = []
        hall_equipment_list = []
        hall_equipment_rate = []
        hall_equipment_dict = {}
        print "request in | hallbookingapp | view | hallbooking_landing.py | additional_facility_details"
        user_type = request.GET.get('user_type_val')
        from_hour = request.GET.get('from_hour')
        to_hour = request.GET.get('to_hour')
        from_minute =  request.GET.get('from_minute')
        to_minute =  request.GET.get('to_minute')
        hall_id = request.GET.get('hall_id')
        from_date = request.GET.get('fromdate')
        to_date = request.GET.get('todate')
        from_period = request.GET.get('from_period')
        to_period = request.GET.get('to_period')
        company_name = request.GET.get('companyindividualname')
        date_value = request.GET.get('date_value')
        event_date = datetime.now()
        hall_detail_id = HallDetail.objects.get(id = hall_id)
        hall_facility_list = hall_detail_id.hall_equipment.all()
        hall_equipment_obj = HallEquipment.objects.filter(hall_detail = hall_detail_id.id)
        for hall_equipment in hall_equipment_obj:
            if user_type == 'nm':
                hall_equipment_val = float(hall_equipment.non_member_charges)
            else:
                hall_equipment_val = float(hall_equipment.member_charges)
            hall_equipment_dict = {
                    'facility_list':str(hall_equipment.hall_functioning_equipment.equipment_name) , 
                    'hall_rate':float(hall_equipment_val),
                    'from_hour' : str(from_hour),
                    'from_minute' : str(from_minute),
                    'to_minute' : str(to_minute),
                    'to_hour' : str(to_hour),
                    'from_period' : str(from_period),
                    'to_period' : str(to_period),

            }
            hall_equipment_list.append(hall_equipment_dict)

        length = len(from_date)
        if length:
            local_date = datetime.strptime(str(from_date), '%d/%m/%Y')
            local_from_time = ''
            local_to_time = ''

            if from_period == "PM":
                if from_hour == '12':
                    local_from_time = time(int(from_hour), int(from_minute))
                else:
                    local_from_time = time(int(from_hour) + 12, int(from_minute))
            else:
                if int(from_hour) == 12:
                    local_from_time = time(int(00), int(from_minute))
                else:
                    local_from_time = time(int(from_hour), int(from_minute))
            if to_period == "PM":
                if to_hour == '12':
                    local_to_time = time(int(to_hour), int(to_minute))
                else:
                    local_to_time = time(int(to_hour) + 12, int(to_minute))
            else:
                if int(to_hour) == 12:
                    local_to_time = time(int(00), int(to_minute))
                else:
                    local_to_time = time(int(to_hour), int(to_minute))

            from_time = datetime.strptime(str(local_from_time), '%H:%M:%S')
            to_time = datetime.strptime(str(local_to_time), '%H:%M:%S')
            f_time = datetime.strftime(from_time, '%H,%M')
            t_time = datetime.strftime(to_time, '%H,%M')
            f_time = datetime.strptime(f_time, '%H,%M').time()
            t_time = datetime.strptime(t_time, '%H,%M').time()

            from_date_time = datetime.combine(local_date.date(), f_time)
            to_date_time = datetime.combine(local_date.date(), t_time)

            date_time_dict = {}

            date_time_dict.setdefault((from_date_time.date()), []).append(from_date_time.time())
            date_time_dict.setdefault((to_date_time.date()), []).append(to_date_time.time())

            hall_obj = HallDetail.objects.get(id=request.GET.get('hall_id'))

            
            for key, value in date_time_dict.iteritems():
                utc_to_date = datetime.combine(key, value[1])
                utc_from_date = datetime.combine(key, value[0])
                utc_to_date = utc_to_date.replace(tzinfo=from_zone)
                final_to_date = utc_to_date.astimezone(to_zone)

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

                if request.GET.get('user_type_val') == 'm':
                    member_obj = UserDetail.objects.get(id=request.POST.get('company_list'))
                    if member_obj.valid_invalid_member:
                        hall_rent_dict = get_total_hall_rent(week_day, minutes, hall_obj, True)
                    else:
                        hall_rent_dict = get_total_hall_rent(week_day, minutes, hall_obj, False)
                else:
                    hall_rent_dict = get_total_hall_rent(week_day, minutes, hall_obj, False)
        data = {
                'success': 'true', 
                'hall_name' : hall_detail_id.hall_name,
                'hall_equipment':hall_equipment_list,
                'event_nature': str(request.GET.get('NatureoftheEvent')),
                'event_date': event_date.strftime('%I:%M %p'),
                'booking_from_time' : from_date,
                'hall_detail_id' : hall_detail_id.id,
                'booking_to_time': to_date,
                'company_name_val':company_name,
                'hall_rent' : hall_rent_dict['total_rent'],
                'date_value' : date_value
                }
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception ,e:
        print "Responce Out | hallbookingapp | view | hallbooking_landing.py | additional_facility_details",str(traceback.print_exc())
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def additional_facility_details_values(request):
    data = {}
    facility_list = {}
    facility_detail = []
    # print '\n\n\n'
    # print json.dumps(request.POST, indent=4)
    # print '\n\n\n'
    try:
        print '\nRequest IN | hallbooking_landing.py | additional_facility_details_values | User = ',request.POST
        # json_obj =  json.loads(request.POST)
        a = request.POST
        length = len(a)
        print '---------------',length
        index = length/8
        print '-------index----------',type(index)
        for ai in a:
            print '---------',request.POST.getlist('facility_data_list[index][booking_from_time]')
        hall_id = request.POST.get('hall_id')
        booking_date = request.POST.get('booking_date')
        booking_from_time = request.POST.get('booking_from_time')
        booking_to_time = request.POST.get('booking_to_time')
        facility_from_time = request.POST.get('hall_id')
        facility_to_time = request.POST.get('booking_date')
        facility_name = request.POST.get('facility_name')
        facility_rate = request.POST.get('facility_rate')


        index = 0
        # for facility_data_lists in facility_data_list:
            # a=facility_data_list[index][hall_id]
            # print '--------------a======',a
        # myvalues = [i['hall_id'] for i in mylist]
        # [d['booking_date'] for d in facility_data_list]
        # print '-------------\n\n',len(mylist)
        
        # for a in request.POST:
        # print '--------------------\n',facility_data_list[0][hall_id]
        # json_obj =  json.load(request.POST)
        # from_to_date_list = []
        # facility_detail = {}
        # final_facility_list = []

        # final_facility_list.append({'facility_availed':str(facility_list[obj]),'hour_used':str(hour_used_list[obj]),'rate':str(rate_list[obj]),'amount':str(amount_list[obj]),'discount':str(discount_list[obj]),'net_amount':str(net_amount_list[obj])})
        data = {
                'success' : 'true',
            }
    except Exception:
        data = {'success': 'false'}
        print '\nException IN | hallbooking_landing.py | additional_facility_details_values| EXP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')



# Calculate Total Hall Rent & Return
def get_total_hall_rent(week_day, minutes, hall_detail_obj, flag):
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


def terms_condition(request):
    """
    It renders on following page

    **Template:**

    :template:`hallbooking/terms_condition.html`
    """
    return render(request, 'hallbooking/terms_condition.html')


def check_hall_status(request):
    """
    It renders on following page

    **Template:**

    :template:`hallbooking/check_hall_availbility_status.html`
    """
    return render(request, 'hallbooking/check_hall_availbility_status.html')


def get_member_detail(request):
    """
    It takes out data of member from UserDetail table

    **Context**

    ``mymodel``
        An instance of :model:`hallbookingapp.UserDetail`.

    """
    data = {}
    try:
        print '\nRequest IN | hallbooking_landing | get_member_detail | user = ', request.user, request.GET.get('mem_id')
        user_detail_obj = UserDetail.objects.get(id=request.GET.get('mem_id'))

        address = str(user_detail_obj.correspond_address)
        membership_no = user_detail_obj.member_associate_no if user_detail_obj.member_associate_no else 'IA-TMP'
        user_track_id = ''   

        try:
            user_track_obj = UserTrackDetail.objects.get(member=user_detail_obj)
            user_track_id = user_track_obj.id
            contact_person = str(user_track_obj.contact_person)
            designation = str(user_detail_obj.person_designation)
            mobile_no = str(user_detail_obj.person_cellno)
            email = str(user_detail_obj.person_email)
            gst = str(user_detail_obj.gst)

        except Exception as e:
            contact_person = ''
            designation = ''
            mobile_no = ''
            email = ''
            gst = ''     
            print e
            pass

        data = {'success': 'true', 'address': address,
                'user_track_id' : user_track_id,
                'membership_no': membership_no,
                'contact_person': contact_person,
                'designation': designation,
                'mobile_no': mobile_no,
                'email': email,
                'gst': gst,
            }

        print '\nResponse OUT | hallbooking_landing | get_member_detail | user = ', request.user, request.GET.get('mem_id')
    except Exception:
        data = {'success': 'false'}
        print '\nException IN | hallbooking_landing | get_member_detail | EXP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def advisory(request):
    """
    It renders on following page

    **Template:**

    :template:`services/advisory.html`
    """
    return render(request, 'services/advisory.html')

def certificate_of_origin(request):
    """
    It renders on following page

    **Template:**

    :template:`services/Certificate-of-Origin.html`
    """
    return render(request, 'services/Certificate-of-Origin.html')


def library(request):
    """
    It renders on following page

    **Template:**

    :template:`services/library.html`
    """
    return render(request, 'services/library.html')


def get_server_time(request):
    data ={}
    try:
        print "request in | hallbookingapp | view | hallbooking_landing.py | get_server_time"
        server_time = datetime.today().strftime("%a %b %d %Y %H:%M:%S")
        data = {
            'success': 'true',
            'server_time': server_time
        }
    except Exception, e:
        print "Response Out | hallbookingapp | view | hallbooking_landing.py | get_server_time"
    return HttpResponse(json.dumps(data), content_type='application/json')
