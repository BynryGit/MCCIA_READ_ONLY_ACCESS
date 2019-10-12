from django.conf.urls import include, url
from hallbookingapp.view import hallbooking_landing, hall_booking_confirm

__author__ = 'Priyanka'

urlpatterns = [
    url(r'^hallbooking-landing',hallbooking_landing.landing,name="landing"),
    url(r'^open-hallbooking-page/$',hallbooking_landing.open_hallbooking_page,name="open_hallbooking_page_1"),
    url(r'^open-hallbooking-page/(?P<location_id>\d+)/$',hallbooking_landing.open_hallbooking_page,name="open_hallbooking_page"),
    url(r'^open-hallbooking-page/(?P<location_id>\d+)/(?P<booking_id>\d+)/$',hallbooking_landing.open_hallbooking_page,name="open_loc_bk_page"),

    url(r'^open-hallbooking-form/(?P<hall_id>\d+)/$', hallbooking_landing.open_hallbooking_form,name="open_hallbooking_form"),
    url(r'^open-hallbooking-form/(?P<hall_id>\d+)/(?P<booking_id>\d+)/$', hallbooking_landing.open_hallbooking_form,name="open_bk_form"),
    url(r'^additional-facility-details/$',hallbooking_landing.additional_facility_details, name='additional_facility_details'),
    url(r'^check-hall-status/$', hallbooking_landing.check_hall_status, name="check_hall_status"),

    # Newly added by shubham shirsode for check avalibity
    url(r'^get-hallevent-calender-data/$', hallbooking_landing.get_hallevent_calender_data, name="get_hallevent_calender_data"),
    

    url(r'^hall-booking-confirm/(?P<booking_id>\d+)/$',hall_booking_confirm.hall_booking_confirm,name="hall_booking_confirm"),

    url(r'^terms-condition/$',hallbooking_landing.terms_condition,name="terms_condition"),
    url(r'^advisory/$',hallbooking_landing.advisory,name="advisory"),
    url(r'^certificate-of-origin/$',hallbooking_landing.certificate_of_origin,name="certificate_of_origin"),
    url(r'^library/$',hallbooking_landing.library,name="library"),

    # Get Booking Slot Table
    url(r'^get-slot-table/$',hall_booking_confirm.get_slot_table,name="get_slot_table"),

    # Save Temporary Booking Data
    url(r'^save-temp-booking-data/$',hall_booking_confirm.save_temp_booking_data, name="save_temp_booking_data"),

    url(r'^get-member-detail/$',hallbooking_landing.get_member_detail,name="get_member_detail"),
    url(r'^get-non-member-detail/$',hallbooking_landing.get_non_member_detail,name="get_non_member_detail"),
    
    url(r'^save-booking/$',hall_booking_confirm.save_booking,name="save_booking"),

    # url hall booking landing
    url(r'^get-hall-detail-location/$',hallbooking_landing.get_hall_detail_location,name='get_hall_detail_location'),

    # url for booking form
    url(r'^check-availability/$',hall_booking_confirm.check_availability,name="check_availability"),
    
    #Save Addtional facility data
    url(r'^additional-facility-details-values/$',hallbooking_landing.additional_facility_details_values,name = 'additional_facility_details_values'),
    

    # url for confirm hall booking page
    url(r'^remove-hall-booking/$',hall_booking_confirm.remove_hall_booking,name="remove_hall_booking"),

    # Cancel Hall Booking
    url(r'^cancel-booking/$',hall_booking_confirm.cancel_booking,name="cancel_booking"),

    # Save Offline Booking URL
    url(r'^save-offline-booking/$', hall_booking_confirm.save_offline_booking, name="save_offline_booking"),


    # url(r'^demo-url/$', hall_booking_confirm.demo_url, name="demo_url"),

    url(r'^send_booking_invoice_mail/$', hall_booking_confirm.send_booking_invoice_mail_locationvise, name="send_booking_invoice_mail"),
    #hall booking according to server time
    url(r'^get-server-time/$', hallbooking_landing.get_server_time, name="get_server_time"),
]