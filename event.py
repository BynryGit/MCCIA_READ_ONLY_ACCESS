
# System Imports

import csv, os, django, traceback
from django.http import HttpResponse
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()


# User Imports

from eventsapp.models import EventDetails, EventParticipantUser


def download_event_participant_data():
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=event_participant_report.csv'
        writer = csv.writer(response)

        event_id_list = [129, 130, 134, 139, 140, 228, 229, 238, 239, 240, 241, 242, 244, 245, 247, 252, 253, 255, 259, 261, 264, 266, 267, 268, 269, 270, 271, 272, 275, 276, 277, 336, 381, 384, 388, 389, 390, 391, 392, 393, 396, 397, 398, 402, 403, 404, 387, 399, 405, 406, 410, 411, 409]
        eventregs = EventParticipantUser.objects.filter(event_user__is_deleted=False, event_user__is_active=True, event_user__register_status=0, event_user__event_id__in=event_id_list)

        writer.writerow(['Sr.No.','event Name', 'Name of the Participants', 'Designation', 'Name of the Organization','Memb.No.','Tel. / Mobile','Email','Event Type(Paid / Free)','From Date','TO Date','Address','GST No.','Committee','Contact Person 1','Contact Person 2','EBK Number'])

        i = 0
        # for eventreg in eventregs:
        #     i = i + 1
        #
        #     member_associate_no = 'Non-Member'
        #     if eventreg.event_user.is_member:
        #         member_associate_no = str(eventreg.event_user.user_details.member_associate_no)
        #     if eventreg.event_user.gst_in == 'UP':
        #         gst_no = 'Under Process'
        #     elif eventreg.event_user.gst_in == 'NA':
        #         gst_no = 'Not Applicable'
        #     else:
        #         gst_no = str(eventreg.event_user.gst)
        #     if eventreg.event_user.event.contact_person2:
        #         contact_person2 = str(eventreg.event_user.event.contact_person2.name)
        #     else:
        #         contact_person2 = ''
        #     if eventreg.event_user_name:
        #         event_user_name = str(eventreg.event_user_name.encode('utf-8').strip())
        #     else:
        #         event_user_name = 'NA'
        #     if eventreg.event_user.event.event_mode == 1:
        #         event_mode = 'Paid'
        #     else:
        #         event_mode = 'Free'
        #
        #     writer.writerow([i,
        #                      str(eventreg.event_user.event.event_title.encode('utf-8').strip()) if eventreg.event_user.event.event_title else '',
        #                      str((event_user_name).upper()),
        #                      str(eventreg.designation.encode('utf-8').strip()) if eventreg.designation else '',
        #                      str(eventreg.event_user.name_of_organisation.encode('utf-8').strip()) if eventreg.event_user.name_of_organisation else '',
        #                      str(member_associate_no.encode('utf-8').strip()),
        #                      str(eventreg.contact_no.encode('utf-8').strip()) if eventreg.contact_no else '',
        #                      str(eventreg.email_id.encode('utf-8').strip()) if eventreg.email_id else '',
        #                      event_mode,str(eventreg.event_user.event.from_date.strftime('%d/%m/%Y')),
        #                      str(eventreg.event_user.event.to_date.strftime('%d/%m/%Y')),'',gst_no,str(eventreg.event_user.event.organising_committee.committee.encode('utf-8').strip()),str(eventreg.event_user.event.contact_person1.name.encode('utf-8').strip()),contact_person2,str(eventreg.event_user.reg_no)])

        writer.writerow([1,
                         2,
                         3,
                         4,
                         5,
                         6,
                         7,
                         8,
                         9, 10,
                         11, 12, 13,
                         14,
                         15, 16,
                         17])
        return response
    except Exception, e:
        print e
        print str(traceback.print_exc())


if __name__ == "__main__":
    download_event_participant_data()
    pass
