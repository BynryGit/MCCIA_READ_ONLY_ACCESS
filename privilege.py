import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()
import datetime
from backofficeapp.models import UserPrivilege


def new_add_privilege():
    UserPrivilege.objects.all().delete()
    today_date = datetime.datetime.now()
    data={
        'Dashboard':['Dashboard'],
        'Membership':['Membership Details','Industry Details','Slab','Legal Details','Membership Category',' Executive Committee Member','Valid / Invalid Member','Exclude Mail Member','Top 3 Members','Membership Certificate Dispatched','Membership Registration'],
        'Hall Booking':['Hall Locations','Holidays','Hall Equipments','Manage Halls','Hall Bookings Registrations','Hall Bookings Registrations Report','Internal Hall Booking','Hall Special Announcement'],
        'Event':['Events Details','Events Registrations','Event Special Announcement','Events Participant Report','Delete Events','Delete Event Participants','Event Committees','Event Type'],
        'Administrator':['Country','State','City','Service Tax','User','Department','Designation']
    }
    for key, value in data.iteritems():
        for privilege in value:
            try:
                UserPrivilege.objects.get(module_name=key,privilege=privilege)
            except Exception, e:
                userPrivilege = UserPrivilege(
                    privilege=privilege,
                    module_name=key,
                    created_by='admin',
                    created_on=today_date,
                    is_deleted=False,
                )
                userPrivilege.save()
                pass

if __name__ == "__main__":
    new_add_privilege()

