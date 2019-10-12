from django.conf.urls import include, url
from Paymentapp.view import common

urlpatterns = [
    # url(r'^get-check-mid-page/', common.get_check_mid_page,name='get_check_mid_page'),

    url(r'^get-payment-detail/', common.get_payment_detail,name='common_response_save'),
    url(r'^common-response-save/', common.common_response_save,name='common_response_save'),

    url(r'^get-event-payment-detail/', common.get_event_payment_detail,name='get_event_payment_detail'),
    url(r'^event-response-save/', common.event_response_save,name='event_response_save'),

    # Hall Booking Payment URL
    url(r'^get-hall-payment-detail/$', common.get_hall_payment_detail, name="get_hall_payment_detail"),
    url(r'^hall-response-save/$', common.hall_response_save, name="hall_response_save"),

    # Membership Payment URL
    url(r'^get-membership-payment-detail/$', common.get_membership_payment_detail, name="get_membership_payment_detail"),
    url(r'^membership-response-save/$', common.membership_response_save, name="membership_response_save"),

    # Customize Payment Link for Hall Booking
    url(r'^pay-mccia-landing/', common.pay_mccia_landing, name='pay_mccia_landing'),
    url(r'^pay-mccia/', common.pay_mccia, name='pay_mccia'),
    url(r'^save-hall-payment-link-response/', common.save_hall_payment_link_response, name='save_hall_payment_link_response'),
    url(r'^pay-online-later-through-mail/', common.pay_online_later_through_mail, name='pay_online_later_through_mail'),
    url(r'^pay-later-payment-response-save/', common.pay_later_payment_response_save, name='pay_later_payment_response_save'),

]

