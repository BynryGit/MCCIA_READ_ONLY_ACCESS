
from django.conf.urls import include, url
from eventsapp.view import events_landing

urlpatterns = [
    url(r'^events-home',events_landing.events_home,name="events_home"),
    url(r'^get-hall-location/', events_landing.get_hall_location, name='get_hall_location'),
    url(r'^get-edit-hall-location/', events_landing.get_edit_hall_location, name='get_edit_hall_location'),
    url(r'^get-event-data',events_landing.get_event_data,name="get_event_data"),
    url(r'^events-details/$',events_landing.events_details,name="events_details"),
    url(r'^get-membership-no/$',events_landing.get_membership_no,name="get_membership_no"),
    url(r'^edit-events-details/$',events_landing.edit_events_details,name="edit_events_details"),
    url(r'^save-event-details/$',events_landing.save_event_details,name="save_event_details"),
    url(r'^confirm-event-registration/$',events_landing.confirm_event_registration,name="confirm_event_registration"),
    url(r'^save-edit-event/$',events_landing.save_edit_event,name="save_edit_event"),
    url(r'^get-total-event-amount/$',events_landing.get_total_event_amount,name="get_total_event_amount"),
    url(r'^get-promocode-applied-amount/$',events_landing.get_promocode_applied_amount,name="get_promocode_applied_amount"),
    url(r'^get-participant-details/$',events_landing.get_participant_details,name="get_participant_details"),
    url(r'^upcoming-event-list',events_landing.upcoming_event_list,name="upcoming_event_list"),
    url(r'^upcoming-event-datatable',events_landing.upcoming_event_datatable,name="upcoming_event_datatable"),

    url(r'^past-event-datatable',events_landing.past_event_datatable,name="past_event_datatable"),
    url(r'^past-event-details',events_landing.past_event_details,name="past_event_details"),

    url(r'^get-non-member-detail',events_landing.get_non_member_detail,name="get_non_member_detail"),
    ]



    