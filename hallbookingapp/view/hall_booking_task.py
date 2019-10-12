
# System Import

import traceback
from django.db import transaction
from datetime import datetime, timedelta

# User Import

from hallbookingapp.models import HallCheckAvailability, HallBooking, HallBookingDetail, HallPaymentDetail


@transaction.atomic
def cancel_invalid_booking():
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | hall_booking_task | cancel_invalid_booking | Time = ', datetime.now().strftime('%d/%m/%Y %I:%M %p')
        today_date = datetime.today()
        flag = False

        print 'Cancelling Invalid Bookings For = ', today_date.date()

        today_hall_booking = HallBooking.objects.filter(created_date__icontains=today_date.strftime('%Y-%m-%d')).exclude(booking_status__in=[0, 10])
        for hall_booking_item in today_hall_booking:
            try:
                hall_payment_obj_list = HallPaymentDetail.objects.filter(hall_booking=hall_booking_item, is_deleted=False)
                if not hall_payment_obj_list:
                    flag = True
                    hall_booking_item.booking_status = 0
                    hall_booking_item.save()
                    for hall_booking_detail_item in HallBookingDetail.objects.filter(hall_booking=hall_booking_item, is_deleted=False):
                        hall_booking_detail_item.booking_status = 0
                        hall_booking_detail_item.save()
                        for hall_avail_item in HallCheckAvailability.objects.filter(hall_booking_detail=hall_booking_detail_item, is_deleted=False):
                            hall_avail_item.booking_status = 0
                            hall_avail_item.save()
                    print 'CANCELLED HBK_NO = ', hall_booking_item.booking_no, ' CANCELLED HB ID = ', hall_booking_item.id
            except Exception, e:
                print '\nINNER EXCP = ', str(traceback.print_exc())
                transaction.rollback(sid)

        if flag:
            print 'No Invalid Bookings found today = ', today_date.date()

        print '\nResponse OUT | hall_booking_task | cancel_invalid_booking '
        transaction.savepoint_commit(sid)
    except Exception, e:
        print '\nException IN | hall_booking_task | cancel_invalid_booking | EXCP = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return
