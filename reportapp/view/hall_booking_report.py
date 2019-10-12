# System Module Import
import json
import traceback
import io
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from xlsxwriter import Workbook
from authenticationapp.decorator import role_required
from datetime import datetime, timedelta
from hallbookingapp.models import HallLocation

# User Module Import

from hallbookingapp.models import HallBooking, HallBookingDetail, HallPaymentDetail, HallDetail, UserTrackDetail


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Booking Report'], login_url='/backofficeapp/login/', raise_exception=True)
def hall_booking_report_landing(request):
    return render(request, 'backoffice/report/hall_booking_report/hall_booking_report_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Booking Utilization & Revenue Report'], login_url='/backofficeapp/login/',
               raise_exception=True)
def hall_booking_utilization_revenue_report_landing(request):
    hall_location_list = HallLocation.objects.filter(is_deleted=False)
    data = {'hall_location_list': hall_location_list}
    return render(request, 'backoffice/report/hall_booking_report/hall_utilization_and_revenue_report.html',data)


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Booking Utilization & Revenue Report'], login_url='/backofficeapp/login/',
               raise_exception=True)
def download_utilization_revenue_details(request):
    try:
        print "Request IN | hall_booking_report.py | download_utilization_revenue_details | User = ", request.user
        from_date = datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y').date()
        to_date = datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y').date()
        location = request.GET.get('location')

        if from_date >= to_date:
            data = {'success': 'invalid_date'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        date_list = []
        temp_booking_details = []
        while from_date <= to_date:
            date_list.append(from_date)
            from_date = from_date + timedelta(days=1)

        temp_booking_details_list = HallBookingDetail.objects.all().exclude(booking_status__in=[0, 10])
        for item in temp_booking_details_list:
            if item.booking_from_date.date() in date_list:
                temp_booking_details.append(item)

        if location != 'All':
            booking_details = HallBookingDetail.objects.filter(id__in=[item.id for item in temp_booking_details],hall_location_id=int(location)).values('hall_detail_id').distinct()
        else:
            booking_details = HallBookingDetail.objects.filter(
                id__in=[item.id for item in temp_booking_details]).values('hall_detail_id').distinct().order_by('hall_location')
        if booking_details:
            data = {"success" : "true"}
        else:
            data = {"success" : "no data"}
    except Exception,e:
        print "\nException IN | hall_booking_report.py | download_utilization_revenue_details | User = ",str(traceback.print_exc())
        data = {"success" : "false"}
    return HttpResponse(json.dumps(data),content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Booking Utilization & Revenue Report'], login_url='/backofficeapp/login/',
              raise_exception=True)
def download_utilization_revenue_report_file(request):
   try:
       print '\nRequest IN | hall_booking_report.py | download_utilization_revenue_report_file | User = ', request.user
       if request.GET.get('from_date') and request.GET.get('to_date'):
           from_date = datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y').date()
           to_date = datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y').date()
           location = request.GET.get('location')
           total_days = to_date-from_date
           no_of_days = total_days.days

           date_list = []
           temp_booking_details = []
           i = 1
           j = 2
           k = 3
           mem_total_sum = 0
           nmem_total_sum = 0

           output = io.BytesIO()
           workbook = Workbook(output, {'in_memory': True})
           worksheet1 = workbook.add_worksheet('Hall_Utilization_Revenue')
           merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter',})

           if location != 'All':
               location_name = HallLocation.objects.filter(id=int(location))
               for name in location_name:
                   title_text = 'Hall Utilization and Revenue Details for '+str(name)+' Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
                       to_date.strftime('%d/%m/%Y'))
           else:
               title_text = 'Hall Utilization and Revenue Details Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
                   to_date.strftime('%d/%m/%Y'))
           worksheet1.merge_range('A1:L1', title_text, merge_format)
           worksheet1.set_column('A:A', 3)
           worksheet1.set_column('B:B', 10)


           while from_date <= to_date:
               date_list.append(from_date)
               from_date = from_date + timedelta(days=1)

           temp_booking_details_list = HallBookingDetail.objects.all().exclude(booking_status__in=[0,10])
           for item in temp_booking_details_list:
               if item.booking_from_date.date() in date_list:
                   temp_booking_details.append(item)

           booking_detail_obj_list = HallBookingDetail.objects.filter(id__in=[item.id for item in temp_booking_details])

           if location != 'All':
               booking_details = HallBookingDetail.objects.filter(
                   id__in=[item.id for item in temp_booking_details],hall_location_id=int(location)).values('hall_detail_id').distinct()
           else:
               booking_details = HallBookingDetail.objects.filter(id__in=[item.id for item in temp_booking_details]).values('hall_detail_id').distinct().order_by('hall_location')

           merge_cell_format = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1,
                                                    'align': 'center', 'valign': 'vcenter', 'bold': 1})
           cell_format = workbook.add_format({'text_wrap': True, 'font_size': 10, 'border': 1})

           worksheet1.merge_range('A2:A3', 'Sr No.', merge_cell_format)
           worksheet1.merge_range('B2:B3', 'Hall', merge_cell_format)
           worksheet1.merge_range('C2:C3', 'Location', merge_cell_format)
           worksheet1.merge_range('D2:E2', 'Revenue', merge_cell_format)
           worksheet1.merge_range('F2:H2', 'No. of Booking', merge_cell_format)
           worksheet1.merge_range('I2:K2', 'Hours Used', merge_cell_format)
           worksheet1.merge_range('L2:L3', 'Utilization %', merge_cell_format)
           worksheet1.write_string(j, 3, 'M', merge_cell_format)
           worksheet1.write_string(j, 4, 'NM', merge_cell_format)
           worksheet1.write_string(j, 5, 'I', merge_cell_format)
           worksheet1.write_string(j, 6, 'M', merge_cell_format)
           worksheet1.write_string(j, 7, 'NM', merge_cell_format)
           worksheet1.write_string(j, 8, 'I', merge_cell_format)
           worksheet1.write_string(j, 9, 'M', merge_cell_format)
           worksheet1.write_string(j, 10, 'NM', merge_cell_format)

           for b in booking_details:
               mem_rev = 0
               nmem_rev = 0
               h_i = 0
               h_m = 0
               h_nm = 0
               total_hours_i = timedelta(hours=0)
               total_hours_m = timedelta(hours=0)
               total_hours_nm = timedelta(hours=0)
               if b['hall_detail_id']:
                   hall_detail_obj = HallDetail.objects.get(id=int(b['hall_detail_id']))
                   internal_booking_count = booking_detail_obj_list.filter(hall_detail=hall_detail_obj, hall_booking__booking_for=0, is_deleted=False).count()
                   member_booking_count = booking_detail_obj_list.filter(hall_detail=hall_detail_obj, hall_booking__booking_for=1, is_deleted=False).count()
                   non_member_booking_count = booking_detail_obj_list.filter(hall_detail=hall_detail_obj, hall_booking__booking_for=2, is_deleted=False).count()
                   for hall in booking_detail_obj_list.filter(hall_detail=hall_detail_obj,is_deleted=False):
                       if hall.hall_booking.booking_for == 0:
                           total_hours_i = total_hours_i + hall.booking_to_date - hall.booking_from_date
                           total_sec = total_hours_i.total_seconds()
                           h_i = total_sec//3600
                       elif hall.hall_booking.booking_for == 1:
                           total = hall.total_rent
                           mem_rev = mem_rev + total
                           total_hours_m = total_hours_m + hall.booking_to_date - hall.booking_from_date
                           total_sec = total_hours_m.total_seconds()
                           h_m = total_sec // 3600
                       elif hall.hall_booking.booking_for == 2:
                           total = hall.total_rent
                           nmem_rev = nmem_rev + total
                           total_hours_nm = total_hours_nm + hall.booking_to_date - hall.booking_from_date
                           total_sec = total_hours_nm.total_seconds()
                           h_nm = total_sec // 3600
                   total_hrs = h_i+h_m+h_nm
                   utilization = (total_hrs / 8) / no_of_days * 100
                   worksheet1.write_number(k, 0, int(i), cell_format)
                   worksheet1.write_string(k, 1, str(hall_detail_obj.hall_name), cell_format)
                   worksheet1.write_string(k, 2, str(hall_detail_obj.hall_location.location), cell_format)
                   worksheet1.write_number(k, 3, int(mem_rev), cell_format)
                   worksheet1.write_number(k, 4, int(nmem_rev), cell_format)
                   worksheet1.write_number(k, 5, int(internal_booking_count), cell_format)
                   worksheet1.write_number(k, 6, int(member_booking_count), cell_format)
                   worksheet1.write_number(k, 7, int(non_member_booking_count), cell_format)
                   worksheet1.write_number(k, 8, int(h_i), cell_format)
                   worksheet1.write_number(k, 9, int(h_m), cell_format)
                   worksheet1.write_number(k, 10, int(h_nm), cell_format)
                   worksheet1.write_number(k, 11, int(utilization), cell_format)
                   i = i + 1
                   k = k + 1
                   mem_total_sum = mem_total_sum + mem_rev
                   nmem_total_sum = nmem_total_sum + nmem_rev
           l=k
           worksheet1.write_string(l, 2, str('Total'), merge_cell_format)
           worksheet1.write_number(l, 3, int(mem_total_sum), merge_cell_format)
           worksheet1.write_number(l, 4, int(nmem_total_sum), merge_cell_format)
           workbook.close()
           output.seek(0)
           response = HttpResponse(output.read(),
                                   content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
           response['Content-Disposition'] = 'attachment; filename=Hall_Utilization_Revenue_Report.xlsx'
           print '\nResponse OUT | hall_booking_report.py | download_utilization_revenue_report_file | User = ', request.user
           return response
       else:
           return HttpResponse(status=400)
   except Exception, e:
       print '\nException IN | hall_booking_report.py | download_utilization_revenue_report_file | EXCP = ', str(
           traceback.print_exc())
       return False


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Booking Utilization & Revenue Report'], login_url='/backofficeapp/login/',
               raise_exception=True)
def blacklisting_member_report_landing(request):
    return render(request, 'backoffice/report/hall_booking_report/blacklisting_report.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Booking Utilization & Revenue Report'], login_url='/backofficeapp/login/',
               raise_exception=True)
def download_blacklisted_member_details(request):
    try:
        print "Request IN | hall_booking_report.py | download_blacklisted_member_details | User = ", request.user
        from_date = datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y').date()
        to_date = datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y').date()

        if from_date > to_date:
            data = {'success': 'invalid_date'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            blacklist_details_list = UserTrackDetail.objects.filter(is_deleted=False, is_blacklisted=True,
                                                                 blacklisted_date__range=[from_date, to_date])
        if blacklist_details_list:
            data = {"success": "true"}
        else:
            data = {"success": "no data"}
    except Exception, e:
        print "\nException In | hall_booking_report.py | download_blacklisted_member_details | EXCE =", str(traceback.print_exc())
        data = {"success": "false"}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Hall Booking Utilization & Revenue Report'], login_url='/backofficeapp/login/',
              raise_exception=True)
def download_blacklisted_member_file(request):
   try:
       print '\nRequest IN | hall_booking_report.py | download_blacklisted_member_report_file | User = ', request.user
       if request.GET.get('from_date') and request.GET.get('to_date'):
           from_date = datetime.strptime(str(request.GET.get('from_date')), '%d/%m/%Y').date()
           to_date = datetime.strptime(str(request.GET.get('to_date')), '%d/%m/%Y').date()


           output = io.BytesIO()
           workbook = Workbook(output, {'in_memory': True})
           worksheet1 = workbook.add_worksheet('Blacklisted Member Report')
           workbook.formats[0].set_font_size(10)
           workbook.formats[0].set_border(1)
           workbook.formats[0].set_text_wrap()
           merge_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
           cell_header_format = workbook.add_format(
               {'font_size': 8, 'border': 1, 'text_wrap': True, 'bold': 1, 'align': 'center', 'valign': 'vcenter',
                'border_color': '#000000'})
           cell_format = workbook.add_format(
               {'font_size': 10, 'border': 1, 'text_wrap': True, 'border_color': '#000000'})
           worksheet1.set_column('A:A', 2)
           worksheet1.set_column('B:B', 25)
           worksheet1.set_column('C:C', 6)
           worksheet1.set_column('D:D', 11)
           worksheet1.set_column('E:E', 20)
           worksheet1.set_column('F:F', 20)

           title_text = 'Blacklisted Member Details Between ' + str(from_date.strftime('%d/%m/%Y')) + ' to ' + str(
               to_date.strftime('%d/%m/%Y'))
           worksheet1.merge_range('A1:F1', title_text, merge_format)

           column_name = ['Sr No', 'Name', 'Member', 'Date', 'Blacklisted by', 'Remark']

           for i in range(len(column_name)):
               worksheet1.write_string(1, int(i), column_name[i], cell_header_format)
           i = 2
           j = 1

           blacklist_obj = None
           blacklist_obj = UserTrackDetail.objects.filter(is_deleted=False, is_blacklisted=True,
                                                      blacklisted_date__range=[from_date, to_date])
           for blacklist_members in blacklist_obj:
               if blacklist_members.blacklisted_date:
                  blaclist_date = blacklist_members.blacklisted_date.strftime('%d/%m/%Y')
               else:
                   blaclist_date = ''
               if blacklist_members.member:
                   status = 'YES'
               else:
                   status = 'NO'
               worksheet1.write_number(i, 0, int(j), cell_format)
               worksheet1.write_string(i, 1, str(blacklist_members.company if blacklist_members.company else ''), cell_format)
               worksheet1.write_string(i, 2, str(str(status)),cell_format)
               worksheet1.write_string(i, 3, str(str(blaclist_date)),cell_format)
               worksheet1.write_string(i, 4, str(blacklist_members.blacklisted_by if blacklist_members.blacklisted_by else ''), cell_format)
               worksheet1.write_string(i, 5, str(blacklist_members.blacklist_remark if blacklist_members.blacklist_remark else ''), cell_format)
               i = i + 1
               j = j + 1

           workbook.close()
           output.seek(0)
           response = HttpResponse(output.read(),
                                   content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
           response['Content-Disposition'] = 'attachment; filename=Blacklisted_Member_Report' + str(
               datetime.now().date().strftime('%d_%m_%Y')) + '.xlsx'
           print '\nResponse OUT hall_booking_report.py | download_blacklisted_member_report_file | User = '
           return response
   except Exception, e:
       print '\nException IN hall_booking_report.py | download_blacklisted_member_report_file | EXCP = ', str(traceback.print_exc())
       data = {'success': 'false'}
       return HttpResponse(json.dumps(data), content_type='application/json')