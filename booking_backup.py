import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()

import traceback
from django.http import HttpResponse
from xlrd import open_workbook, xldate_as_tuple
from django.db import transaction

from adminapp.models import *
from membershipapp.models import *
import datetime
from dateutil import tz

from hallbookingapp.models import *

# Start:Use this for local system
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_dir = BASE_DIR + '/MCCIA_BACKOFFICE/Final_data'
# End:Use this for local system

# Start:on server file path
# file_dir='/srv/wsgi/Final_data'
# End:on server file path


"""
Step to add Hall booking Data
1)Add Location data
2)Add Hall Data
3)Add Booking Detail Data
4)Add Booking Header Data #Hallbooking
"""
# location dict key=Previous data hall location id and value is new system location id
# loc_dict={'prvious_hall_location_id':'new_hal_location_id'}
"""
location name - previous location id - new location id
Tilak Road - 1 - 
Bhosari - 2 - 
MCCIA Trade Tower (5th Floor) - 3 - 
Hadpsar -  - 

"""

loc_dict = {
    '1': '2',
    '3': '1',
    '13': '3',
    '17': '4'}

hall_dict = {
    '27': '3',
    '28': '4',
    '36': '5',
    '37': '6',
    '38': '7',
    '39': '8',
    '40': '9',
    '42': '10',
    '44': '11',
    '45': '12',
    '46': '28',
    '48': '13',
    '49': '14',
    '50': '15',
    '67': '16',
    '69': '17',
    '70': '24',
    '71': '25',
    '72': '29',
    '73': '26',
    '74': '27',
    '75': '18',
    '76': '19',
    '77': '20',
    '78': '21',
    '79': '22',
    '80': '23',
    '0': '0',
    '34': '30',
    '65': '31',
    '26': '32',
    '58': '33',
    '65': '34',
}

payment_dict = {'C': 1, 'D': 7, 'I': 2, 'M': 5, 'N': 11, 'P': 3, 'R': 6, 'U': 0, 'S': 4}


@transaction.atomic
def load_booking_detail():
    try:
        sid = transaction.savepoint()
        file_path = [file_dir + '/BookingDetailsss.xlsx']
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            value_list = []
            for row in range(1, number_of_rows):
                # PkBKDetId = int((wb.sheets()[0].cell(row, 0).value))
                FKHallBkId = int((wb.sheets()[0].cell(row, 1).value))
                FkLocId = int((wb.sheets()[0].cell(row, 2).value))
                FKHallId = int((wb.sheets()[0].cell(row, 3).value))

                status = (wb.sheets()[0].cell(row, 9).value)

                Bkdate = (wb.sheets()[0].cell(row, 4)).value
                Bkdate = (Bkdate.split(' '))[0]

                # year, month, day ,hour, minute, second= xldate_as_tuple(int(Bkdate), 0)
                # Bkdate='29/09/2011" format "dd/mm/yyyy"
                # Bkdate = str(day) + '/'+ str(month)+'/'+str(year)
                # print Bkdate
                # print (wb.sheets()[0].cell(row, 5).value)
                booking_date = datetime.datetime.strptime(Bkdate, '%Y-%m-%d').date()

                BkStartTime = (wb.sheets()[0].cell(row, 5).value)
                start_time = datetime.datetime.strptime(BkStartTime, '%I:%M %p').time()
                BKEndTime = (wb.sheets()[0].cell(row, 6).value)
                # if BKEndTime == '02: PM':
                #    BKEndTime ='02:00 PM'

                end_time = datetime.datetime.strptime(BKEndTime, '%I:%M %p').time()

                start_date_time = datetime.datetime.combine(booking_date, start_time)
                end_date_time = datetime.datetime.combine(booking_date, end_time)
                # year, month, day, hour, minute, second = xldate_as_tuple(BkStartTime, 0)
                # start_date=datetime.time(hour,minute)
                # '02:00 PM' format 'HH:MM AM/PM'
                # BkStartTime = start_date.strftime('%I:%M %p')
                # print BkStartTime

                # BKEndTime = (wb.sheets()[0].cell(row, 6).value)
                # status = (wb.sheets()[0].cell(row, 9).value)
                # year, month, day, hour, minute, second = xldate_as_tuple(BKEndTime, 0)
                # end_date = datetime.time(hour, minute)
                # '02:00 PM' format 'HH:MM AM/PM'
                # BKEndTime = end_date.strftime('%I:%M %p')
                # print BKEndTime
                # Bkdates = '29/9/2011'
                # BkStartTimes = '02:00 PM'
                # print Bkdate + ' ' + str(BkStartTime) == Bkdates + ' '+BkStartTimes


                # print Bkdate +' ' + str(BKEndTime)

                # BKEndTime = (wb.sheets()[0].cell(row, 6).value)
                # bk_start_time = datetime.datetime.strptime(Bkdate +' ' + str(BkStartTime), '%Y-%m-%d %I:%M %p')
                # #print bk_start_time
                # #print
                # bk_end_time = datetime.datetime.strptime(Bkdate +' ' + str(BKEndTime), '%d/%m/%Y %I:%M %p')
                # #print bk_end_time

                # from_zone = tz.tzutc()
                # to_zone = tz.gettz('Asia/Kolkata')

                # utc_to_date = bk_start_time.replace(tzinfo=from_zone)
                # final_to_date = utc_to_date.astimezone(to_zone)

                # utc_from_date = bk_end_time.replace(tzinfo=from_zone)
                # final_from_date = utc_from_date.astimezone(to_zone)

                if status == 'N':
                    booking_status = 0
                else:
                    booking_status = 6

                HallBookingDetailobj = HallBookingDetail(
                    hall_location_id=int(loc_dict[str(FkLocId)]),
                    hall_detail_id=int(hall_dict[str(FKHallId)]) if int(hall_dict[str(FKHallId)]) != 0 else None,
                    booking_from_date=start_date_time,
                    booking_to_date=end_date_time,
                    updated_by=FKHallBkId,  # stored the id hall booking id
                    booking_status=booking_status
                )
                HallBookingDetailobj.save()
                if int(hall_dict[str(FKHallId)]) != 0:
                    add_to_check_aval(HallBookingDetailobj, str(int(hall_dict[str(FKHallId)])), booking_status)
        print "Booking detail data Saved"
        transaction.savepoint_commit(sid)

    except Exception, e:
        print e
        print int(hall_dict[str(FKHallId)])
        traceback.print_exc()
        pass
        print "Booking detail data not Saved"
        transaction.rollback(sid)


def add_to_check_aval(HallBookingDetailobj, hall_id, booking_status):
    try:
        hall_obj = HallDetail.objects.get(id=int(hall_id))
        if hall_obj.is_merge:
            hall_id_list = (hall_obj.hall_merge).split(",")
            for i in hall_id_list:
                HallCheckAvailabilityobj = HallCheckAvailability(
                    hall_detail_id=i,
                    hall_booking_detail=HallBookingDetailobj,
                    booking_from_date=HallBookingDetailobj.booking_from_date,
                    booking_to_date=HallBookingDetailobj.booking_to_date,
                    booking_to_time=(HallBookingDetailobj.booking_to_date).time(),
                    booking_from_time=(HallBookingDetailobj.booking_from_date).time(),
                    booking_status=booking_status
                )
                HallCheckAvailabilityobj.save()
        else:
            HallCheckAvailabilityobj = HallCheckAvailability(
                hall_detail=HallBookingDetailobj.hall_detail,
                hall_booking_detail=HallBookingDetailobj,
                booking_from_date=HallBookingDetailobj.booking_from_date,
                booking_to_date=HallBookingDetailobj.booking_to_date,
                booking_to_time=(HallBookingDetailobj.booking_to_date).time(),
                booking_from_time=(HallBookingDetailobj.booking_from_date).time(),
                booking_status=booking_status
            )
            HallCheckAvailabilityobj.save()
    except Exception, e:
        print e
        transaction.rollback(sid)
        pass

    return True


from decimal import Decimal


@transaction.atomic
def load_hallbooking_data():
    try:
        # file_path = ['/home/bynry01/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/a.xlsx']
        file_path = [file_dir + '/BookingHeaders.xlsx']
        i = 0
        abc_list = []
        sid = transaction.savepoint()
        for file in file_path:
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                try:
                    try:
                        HallBooking.objects.get(updated_by=int(row_values[0]))
                    except HallBooking.DoesNotExist, e:
                        try:
                            if row_values[37] != 'NULL':
                                memobj = UserDetail.objects.get(member_associate_no=row_values[37])
                                member_id = memobj.id
                            else:
                                member_id = None
                        except UserDetail.DoesNotExist, e:
                            pass
                            abc_list.append(row_values[37])
                            print "check for mem no", row_values[37]
                            member_id = None
                        except Exception, e:
                            print e
                            pass
                            member_id = None

                        try:
                            hall_booking_obj = HallBooking(
                                member_id=member_id,
                                name=row_values[2],
                                # booking_for='',
                                updated_by=int(row_values[0])
                            )
                            hall_booking_obj.save()
                        except Exception, e:
                            traceback.print_exc()
                            transaction.rollback(sid)
                            print e
                            raise

                        if hall_booking_obj.member:
                            hall_booking_obj.booking_for = 1
                            hall_booking_obj.save()

                        try:
                            if payment_dict[row_values[18]] == 'Cancelled':
                                hall_booking_obj.payment_status = 0
                                hall_booking_obj.booking_status = 0
                                hall_booking_obj.payment_method = 0
                            elif payment_dict[row_values[18]] == 'Paid':
                                hall_booking_obj.payment_status = 1
                                hall_booking_obj.booking_status = 6
                                hall_booking_obj.payment_method = 0

                            elif payment_dict[row_values[18]] == 'Online Pending':
                                hall_booking_obj.payment_status = 2
                                hall_booking_obj.booking_status = 8
                                hall_booking_obj.payment_method = 0
                            elif payment_dict[row_values[18]] == 'Offline Pending':
                                hall_booking_obj.payment_status = 8
                                hall_booking_obj.booking_status = 8
                                hall_booking_obj.payment_method = 0

                            elif payment_dict[row_values[18]] == 'Spot Booking Pending':
                                hall_booking_obj.payment_status = 8
                                hall_booking_obj.booking_status = 8
                                hall_booking_obj.payment_method = 0
                            elif payment_dict[row_values[18]] == 'MCCIA Booking Pending':
                                hall_booking_obj.payment_status = 8
                                hall_booking_obj.booking_status = 8
                                hall_booking_obj.payment_method = 0

                            elif payment_dict[row_values[18]] == 'Confirmed':
                                hall_booking_obj.payment_status = 1
                                hall_booking_obj.booking_status = 6
                                payment_method = 0
                            elif payment_dict[row_values[18]] == 'Settled':
                                hall_booking_obj.payment_status = 1
                                hall_booking_obj.booking_status = 6
                                hall_booking_obj.payment_method = 0

                            elif payment_dict[row_values[18]] == 'Pending':
                                hall_booking_obj.payment_status = 8
                                hall_booking_obj.booking_status = 8
                                hall_booking_obj.payment_method = 0
                            elif payment_dict[row_values[18]] == 'Failed':
                                hall_booking_obj.payment_status = 11
                                hall_booking_obj.booking_status = 0
                                hall_booking_obj.payment_method = 8
                            else:
                                pass

                            hall_booking_obj.save()
                        except Exception, e:
                            transaction.rollback(sid)
                            pass

                        hall_booking_obj.booking_no = str('HBK' + str(str.zfill(str(hall_booking_obj.id), 7)))
                        hall_booking_obj.save()

                        # print hall_booking_obj

                        hall_booking_obj.deposit = Decimal(check_value(row_values[12]))
                        hall_booking_obj.total_rent = Decimal(check_value(row_values[13]))
                        # hall_booking_obj.gst_amount = Decimal(row_values[14]) if row_values[14] != 'NULL' else 0
                        hall_booking_obj.gst_amount = Decimal(check_value(row_values[14]))
                        hall_booking_obj.total_payable = Decimal(check_value(row_values[15]))
                        hall_booking_obj.save()

                        hall_booking_obj.discount = Decimal(check_value(row_values[21]))
                        hall_booking_obj.discount_per = Decimal(check_value(row_values[24]))
                        hall_booking_obj.tds = Decimal(check_value(row_values[32]))
                        hall_booking_obj.shexcesspayment = Decimal(check_value(row_values[22]))
                        hall_booking_obj.educess = Decimal(check_value(row_values[27]))
                        hall_booking_obj.seducess = Decimal(check_value(row_values[28]))
                        hall_booking_obj.shexcesspayment_desc = row_values[23]

                        hall_booking_obj.total_amount = Decimal(check_value(row_values[33]))
                        hall_booking_obj.net_amount = Decimal(check_value(row_values[36]))
                        hall_booking_obj.bill_amount = Decimal(check_value(row_values[42]))
                        hall_booking_obj.bill_no = row_values[40]
                        hall_booking_obj.total_services = row_values[41]
                        hall_booking_obj.save()
                        try:
                            hall_booking_detail_objs = HallBookingDetail.objects.filter(updated_by=int(row_values[0]))
                            for hall_booking_detail_obj in hall_booking_detail_objs:
                                pass

                                hall_booking_detail_obj.hall_booking = hall_booking_obj
                                hall_booking_detail_obj.company = row_values[2]
                                hall_booking_detail_obj.address = row_values[3]
                                hall_booking_detail_obj.contact_person = row_values[4]
                                hall_booking_detail_obj.designation = row_values[35]
                                hall_booking_detail_obj.mobile_no = row_values[6]
                                hall_booking_detail_obj.tel_r = row_values[7]
                                hall_booking_detail_obj.tel_o = row_values[5]
                                hall_booking_detail_obj.email = row_values[8]
                                hall_booking_detail_obj.event_nature = row_values[9]
                                hall_booking_detail_obj.booking_detail_no = ''
                                # hall_booking_detail_obj.total_rent = ''
                                # hall_booking_detail_obj.gst_amount = ''
                                hall_booking_detail_obj.slot = ''
                                # hall_booking_detail_obj.member_price = ''
                                # hall_booking_detail_obj.non_member_price = ''
                                # hall_booking_detail_obj.member_extra_hour_price = ''
                                # hall_booking_detail_obj.non_member_extra_hour_price = ''
                                hall_booking_detail_obj.save()
                        except Exception, e:
                            print e
                            print str(traceback.print_exc())
                            transaction.rollback(sid)
                            pass

                        try:
                            payment_status = 10
                            paid_amount = 0
                            if payment_dict[row_values[18]] == 'Paid':
                                payment_status = 1
                                paid_amount = Decimal(check_value(row_values[15]))

                            HallPaymentDetailobj = HallPaymentDetail(
                                hall_booking=hall_booking_obj,
                                payable_amount=Decimal(check_value(row_values[15])),
                                paid_amount=paid_amount,
                                payment_status=payment_status,
                                cheque_no=row_values[29] if row_values[29] != 'NULL' else '',
                                bank_name=row_values[31] if row_values[31] != 'NULL' else '',
                            )

                            if row_values[29] != 'NULL':
                                if row_values[30] != 'NULL':
                                    Bkdate = ((row_values[30]).split(' '))[0]

                                    ch_dt = datetime.datetime.strptime(Bkdate, '%Y-%m-%d').date()
                                    HallPaymentDetailobj.cheque_date = ch_dt
                                    HallPaymentDetailobj.save()

                            HallPaymentDetailobj.save()
                        except Exception, e:
                            print e
                            transaction.rollback(sid)
                            pass



                except Exception, e:
                    print e
                    traceback.print_exc()
                    pass
                    transaction.rollback(sid)

            transaction.savepoint_commit(sid)


    except Exception, e:
        print e
        traceback.print_exc()
        transaction.rollback(sid)
        # transaction.rollback(sid)
        return HttpResponse(500)


def check_value(check_val):
    if check_val == "NULL":
        return 0
    elif check_val == '':
        return 0
    # print "(check_val)",check_val
    # print "Decimal(check_val)",Decimal(check_val)
    return Decimal(check_val)


def check_date():
    Bkdate = '29/09/2011 00:00:00'
    Bkdate = (Bkdate.split(' '))[0]
    print type(Bkdate)
    BkStartTime = '02:00 PM'
    BKEndTime = '03:00 PM'
    print  datetime.datetime.strptime(Bkdate + ' ' + BkStartTime, '%d/%m/%Y %I:%M %p')
    print  datetime.datetime.strptime(Bkdate + ' ' + BKEndTime, '%d/%m/%Y %I:%M %p')


def add_hall():
    hall_obj = HallDetail.objects.all().last()
    hall_obj.id = None
    hall_obj.save()
    hall_obj = HallDetail.objects.all().last()
    hall_obj.id = None
    hall_obj.save()
    hall_obj = HallDetail.objects.all().last()
    hall_obj.id = None
    hall_obj.save()


def add_dumy_booking():
    hall_id = ''
    hall_location_id = ''


if __name__ == "__main__":
    # load_hall_data()
    # check_date()
    # load_booking_detail()
    # load_hallbooking_data()
    # add_hall()
    pass
    add_dumy_booking()


# username:medhak@mcciapune.com
# pw:awsmccia@2018

# superuser:mccia
# mccia$3

