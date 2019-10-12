from django.conf.urls import include, url
from backofficeapp.view import membership_home, membership_details, event_home, industry_details, legal_details, \
    slab_details, administrator, event_committee, event_type, media, membership_configuration, \
    membership_certificate_download, member_proforma_invoice, awards_landing, renewal_landing

urlpatterns = [

    # Dashboard start
    url(r'^dashboard/', membership_home.dashboard_screen, name='dashboard_screen'),
    # Dashboard end
    # --------------------MemberDetails Urls-----------------
    url(r'^download-all-member-data/', membership_home.download_all_member_data, name='download_all_member_data'),
    url(r'^members-details/', membership_details.members_details, name='members_details'),
    url(r'^get-members-details-datatable/', membership_details.get_members_details_datatable,
        name='get_members_details_datatable'),
    url(r'^delete-membership/', membership_details.delete_membership, name='members_details'),
    url(r'^activate-membership/', membership_details.activate_membership, name='activate_membership'),

    url(r'^show-edit-member-form/', membership_details.show_edit_member_form, name='show_edit_member_form'),
    url(r'^update-member-detail/$', membership_details.update_member_detail, name="update_member_detail"),
    url(r'^show-renew-member-form/$', membership_details.show_renew_member_form, name="renew_member_form"),
    url(r'^get-member-renew-invoice/$', membership_details.get_member_renew_invoice, name="get_member_renew_invoice"),
    url(r'^renew-member/$', membership_details.renew_member, name="renew_member"),
    url(r'^send-manual-renew-letter/(?P<m_id>\d+)/$', membership_details.send_manual_renew_letter,
        name="send_manual_renew_letter"),

    # --------------------Membership Registration Payment-----------------
    url(r'^open-member-payment/', membership_details.open_member_payment, name='open_member_payment'),
    url(r'^get-members-payment-details/', membership_details.get_members_payment_details,
        name='get_members_payment_details'),
    url(r'^add-user-payment/', membership_details.add_user_payment, name='add_user_payment'),
    url(r'^submit-user-acceptance-detail/', membership_details.submit_user_acceptance_detail,
        name='submit_user_acceptance_detail'),
    url(r'^submit-user-receipt-detail/', membership_details.submit_user_receipt_detail,
        name='submit_user_receipt_detail'),
    url(r'^delete-user-payment-entry/', membership_details.delete_user_payment_entry, name='delete_user_payment_entry'),
    url(r'^email-acknowledge/$', membership_details.email_acknowledge),

    url(r'^get-payment-modal/$', membership_details.get_payment_modal, name='get_payment_modal'),
    url(r'^save-payment-receipt/$', membership_details.save_payment_receipt, name='save_payment_receipt'),
    url(r'^add-user-to-confirmed-list/$', membership_details.add_user_to_confirmed_list,
        name='add_user_to_confirmed_list'),
    url(r'^get-edit-payment-modal/$', membership_details.get_edit_payment_modal, name='get_edit_payment_modal'),
    url(r'^update-slab-payment-detail/$', membership_details.update_slab_payment_detail,
        name='update_slab_payment_detail'),
    # --------------------Membership Registration Payment-----------------

    # Print Membership Form
    url(r'^print-user-form/(?P<m_id>\d+)/$', membership_details.print_user_form, name='print_user_form'),
    url(r'^get-user-track-history-page/(?P<m_id>\d+)/$', membership_details.get_user_track_history_page,
        name='get_user_track_history_page'),
    url(r'^get-user-track-history-table/$', membership_details.get_user_track_history_table,
        name='get_user_track_history_table'),

    # ------------------------download-certificate-------------
    url(r'^download-certificate/(?P<m_id>\d+)/$', membership_details.download_certificate, name='download_certificate'),
    url(r'^send-soft-copy-certificate-through-mail/(?P<m_id>\d+)/$',
        membership_details.send_soft_copy_certificate_through_mail, name='send_soft_copy_certificate_through_mail'),
    url(r'^manual-download-certificate/(?P<m_id>\d+)/$', membership_details.manual_download_certificate,
        name='download_certificate'),
    url(r'^hard-copy-certificate-address-download/(?P<m_id>\d+)/$',
        membership_details.hard_copy_certificate_address_download,
        name='hard_copy_certificate_address_download'),

    # --------------------Membership Urls-----------------
    url(r'^backoffice/', membership_home.membership_home, name='membership_home'),
    url(r'^membership-details/', membership_details.membership_details, name='membership_details'),
    url(r'^get-membership-details-datatable/', membership_details.get_membership_details_datatable,
        name='get_membership_details_datatable'),
    url(r'^add-membership-details/', membership_details.add_membership_details, name='add_membership_details'),
    url(r'^save-membership-details/', membership_details.save_membership_details, name='save_membership_details'),
    url(r'^show-membership-details/', membership_details.show_membership_details, name='show_membership_details'),
    url(r'^edit-membership-details/', membership_details.edit_membership_details, name='edit_membership_details'),
    url(r'^update-membership-status/', membership_details.update_membership_status, name='update_membership_status'),
    url(r'^membership-category/', 'backofficeapp.view.membership_home.membership_category', name='membership_category'),
    url(r'^add-membership-category/', 'backofficeapp.view.membership_home.add_membership_category',
        name='add_membership_category'),
    url(r'^membership_certificate_dispatched/', 'backofficeapp.view.membership_home.membership_certificate_dispatched',
        name='membership_certificate_dispatched'),
    url(r'^membership-certificate/', 'backofficeapp.view.membership_home.membership_certificate',
        name='membership_certificate'),
    url(r'^upload-ec-report-file/', 'backofficeapp.view.membership_details.membership_data_upload',
        name='membership_data_upload'),
    url(r'^send-certificate-bulk-mail/', 'backofficeapp.view.membership_details.send_certificate_bulk_mail',
        name='send_certificate_bulk_mail'),
    url(r'^get-bulk-mail-certificate-table/', 'backofficeapp.view.membership_details.get_bulk_mail_certificate_table',
        name='get_bulk_mail_certificate_table'),
    url(r'^create-schedule-bulk-mail/', 'backofficeapp.view.membership_details.create_schedule_bulk_mail',
        name='create_schedule_bulk_mail'),
    url(r'^create-schedule-job-for-mail/', 'backofficeapp.view.membership_details.create_schedule_job_for_mail',
        name='create_schedule_job_for_mail'),

    # -----------------------Industry Details---------------------
    url(r'^industry-details/', industry_details.industry_details, name='industry_details'),
    url(r'^get-industry-details-datatable/', industry_details.get_industry_details_datatable,
        name='get_industry_details_datatable'),
    url(r'^add-industry-details/', industry_details.add_industry_details, name='add_industry_details'),
    url(r'^save-industry-details/', industry_details.save_industry_details, name='save_industry_details'),
    url(r'^show-industry-details/', industry_details.show_industry_details, name='show_industry_details'),
    url(r'^edit-industry-details/', industry_details.edit_industry_details, name='edit_industry_details'),
    url(r'^delete-industry-details/', industry_details.delete_industry_details, name='delete_industry_details'),
    url(r'^activate-industry-details/', industry_details.activate_industry_details, name='activate_industry_details'),
    # -------------------------------------------------------------
    url(r'^legal-details/', legal_details.legal_details, name='legal_details'),
    url(r'^get-legal-details-datatable/', legal_details.get_legal_details_datatable,
        name='get_legal_details_datatable'),
    url(r'^add-legal-details/', legal_details.add_legal_details, name='add_legal_details'),
    url(r'^show_edit_legal_detail/', legal_details.show_edit_legal_detail, name='show_edit_legal_detail'),
    url(r'^update-legal-detail-status/', legal_details.update_legal_detail_status, name='update_legal_detail_status'),
    # ---------------------------------------------------------------
    url(r'^executive-committee-members/', 'backofficeapp.view.membership_home.executive_committee_members',
        name='executive_committee_members'),
    url(r'^top3-members/', 'backofficeapp.view.membership_home.top3_members', name='top3_members'),
    url(r'^add-top3-members/', 'backofficeapp.view.membership_home.add_top3_members', name='add_top3_members'),
    # ---------------------------------------------------------------
    url(r'^slab/', slab_details.slab, name='slab'),
    url(r'^get-slab-details-datatable/', slab_details.get_slab_details_datatable, name='get_slab_details_datatable'),
    url(r'^add-new-slab/', slab_details.add_new_slab, name='add_new_slab'),
    url(r'^get-slab-filter-data/', slab_details.get_slab_filter_data, name='get_slab_filter_data'),
    url(r'^save-slab-details/', slab_details.save_slab_details, name='save_slab_details'),
    url(r'^exclude-mailing-members/', 'backofficeapp.view.membership_home.exclude_mailing_members',
        name='exclude_mailing_members'),
    url(r'^show-slab-details/', slab_details.show_slab_details, name='show_slab_details'),
    url(r'^edit-slab-details/', slab_details.edit_slab_details, name='edit_slab_details'),
    url(r'^update-membership-slab-status/', slab_details.update_membership_slab_status,
        name='update_membership_slab_status'),

    # Update Status of Exeutive Committee , Exclude From Mail & Membership Certificate Dispatch User
    url(r'^update-member/', membership_home.update_member, name='update_member'),

    # Membership Category Add, Show Datatable
    url(r'^save-membership-category/', membership_home.save_membership_category, name='save_membership_category'),
    url(r'^get-membership-category-table/', membership_home.get_membership_category_table,
        name='get_membership_category_table'),
    url(r'^show-edit-membership-category/', membership_home.show_edit_membership_category,
        name='show_edit_membership_category'),
    url(r'^update-membership-category/', membership_home.update_membership_category, name='update_membership_category'),
    url(r'^update-membership-category-status/', membership_home.update_membership_category_status,
        name='update_membership_category_status'),

    # Legal Details Save & Update
    url(r'^save-legal-details/', legal_details.save_legal_details, name='save_legal_details'),
    url(r'^show-edit-legal-detail/', legal_details.show_edit_legal_detail, name='show_edit_legal_detail'),
    url(r'^update-legal-detail/', legal_details.update_legal_detail, name='update_legal_detail'),
    #
    # # pro-forma bulk
    # url(r'^proforma-bulk/', proforma_bulk.proforma_bulk, name='proforma_bulk'),
    # url(r'^get-proforma-datatable/', proforma_bulk.get_proforma_datatable,name='get_proforma_datatable'),
    # url(r'^send-pi-through-email-to-use/', proforma_bulk.send_pi_through_email_to_user, name='send_pi_through_email_to_user'),

    # Executive Committee Member Datatable
    url(r'^get-executive-committee-member-table/', membership_home.get_executive_committee_member_table,
        name='get_executive_committee_member_table'),

    # Valid/Invalid Member
    url(r'^valid-invalid-member/', membership_home.valid_invalid_member, name='valid_invalid_member'),
    url(r'^get-valid-invalid-member-table/', membership_home.get_valid_invalid_member_table,
        name='get_valid_invalid_member_table'),

    # Exclude From Mail Member
    url(r'^get-exclude-mail-member-table/', membership_home.get_exclude_mail_member_table,
        name='get_exclude_mail_member_table'),

    # Membership Certificate Dispatched Datatable
    url(r'^get-membership-certificate-table/', membership_home.get_membership_certificate_table,
        name='get_membership_certificate_table'),
    url(r'^download-membership-certificate/', membership_home.download_membership_certificate,
        name='download_membership_certificate'),

    # Download Payment Details / Labels
    url(r'^download-payment-label/', membership_home.download_payment_label, name='download_payment_label'),
    url(r'^download-payment-file/', membership_home.download_payment_file, name='download_payment_file'),

    # TODO------------Download Membership certificate-----
    url(r'^download-membership-certificate-system/',
        membership_certificate_download.download_membership_certificate_system,
        name='download_membership_certificate_system'),
    url(r'^download-certificate-file/', membership_certificate_download.download_certificate_file,
        name='download_certificate_file'),
    url(r'^download-certificate-file-manual/', membership_certificate_download.download_certificate_file_manual,
        name='download_certificate_file_manual'),

    # url(r'^download-excel-file/', membership_certificate_download.download_excel_file,
    #     name='download_excel_file'),

    # TODO-----Download Membership certificate-----------
    url(r'^membership-configuration/', membership_configuration.membership_configuration_landing,
        name='Membership_Configuration_landing'),
    url(r'^membership-certificate-configuration/', membership_configuration.Membership_certificate_Configuration,
        name='Membership_certificate_Configuration'),
    url(r'^save-sign-name/', membership_configuration.save_sign_name, name='save_sign_name'),
    url(r'^current-dg-president-name/', membership_configuration.current_dg_president_name,
        name='current_dg_president_name'),

    # Download Member Proforma Invoice URLs
    url(r'^download-proforma-invoice/(?P<m_id>\d+)/(?P<m_year>\w+)/$',
        member_proforma_invoice.download_proforma_invoice, name='download_proforma_invoice'),
    url(r'^send-pi-through-email-to-user/(?P<m_id>\d+)/(?P<m_year>\w+)/$',
        member_proforma_invoice.send_pi_through_email_to_user, name='download_proforma_invoice'),

    # --------------------Events Urls-----------------
    url(r'^events/', 'backofficeapp.view.event_home.event_home', name='event_home'),
    url(r'^event-details/', 'backofficeapp.view.event_home.event_details', name='event_details'),
    url(r'^add-new-event/', 'backofficeapp.view.event_home.add_new_event', name='add_new_event'),
    url(r'^get-events-datatable/', 'backofficeapp.view.event_home.get_events_datatable', name='get_events_datatable'),
    url(r'^get-contact-person/', 'backofficeapp.view.event_home.get_contact_person', name='get_contact_person'),
    url(r'^get-program-details/', 'backofficeapp.view.event_home.get_program_details', name='get_program_details'),
    url(r'^get-hall-name/', 'backofficeapp.view.event_home.get_hall_name', name='get_hall_name'),
    url(r'^get-hall-location/', 'backofficeapp.view.event_home.get_hall_location', name='get_hall_location'),

    url(r'^save-new-event/', 'backofficeapp.view.event_home.save_new_event', name='save_new_event'),
    url(r'^upload-event-banner/', 'backofficeapp.view.event_home.upload_event_banner', name='upload_event_banner'),
    url(r'^upload-sponsor-banner/', 'backofficeapp.view.event_home.upload_sponsor_banner',
        name='upload_sponsor_banner'),
    url(r'^upload-sponsor-images/', 'backofficeapp.view.event_home.upload_sponsor_images',
        name='upload_sponsor_images'),
    url(r'^remove-sponsor-images/', 'backofficeapp.view.event_home.remove_sponsor_images',
        name='remove_sponsor_images'),
    url(r'^get-banner-file/', 'backofficeapp.view.event_home.get_banner_file', name='get_banner_file'),
    url(r'^edit-event/', 'backofficeapp.view.event_home.edit_event', name='edit_event'),
    url(r'^update-event/', 'backofficeapp.view.event_home.update_event', name='update_event'),
    url(r'^update-event-detail-status/', 'backofficeapp.view.event_home.update_event_detail_status',
        name='update_event_detail_status'),

    # TODO-------------- hall Booking Urls Start-------------------
    url(r'^hall_booking/', 'backofficeapp.view.hallbooking.hall_booking_landing', name='hall_booking_landing'),
    url(r'^hall-location/', 'backofficeapp.view.hallbooking.hall_location', name='hall_location'),
    url(r'^add-new-hall-location/', 'backofficeapp.view.hallbooking.add_new_hall_location',
        name='add_new_hall_location'),
    url(r'^save-new-hall-location/', 'backofficeapp.view.hallbooking.save_new_hall_location',
        name='save_new_hall_location'),
    url(r'^edit-save-hall-location/', 'backofficeapp.view.hallbooking.edit_save_hall_location',
        name='edit_save_hall_location'),
    url(r'^hall-booking-details/', 'backofficeapp.view.hallbooking.hall_booking_details', name='hall-booking-details'),
    url(r'^get-hall-location-data/', 'backofficeapp.view.hallbooking.get_hall_location_data',
        name='get-hall-location-data'),
    url(r'^update-location-detail-status/', 'backofficeapp.view.hallbooking.update_location_detail_status',
        name='update-location-detail-status'),
    url(r'^hall-location-edit/', 'backofficeapp.view.hallbooking.hall_location_edit', name='hall-location-edit'),
    # TODO-------------hall Booking Urls End---------------------

    # TODO------------Manage Holidays Urls Start--------------------
    url(r'^hall-holidays/', 'backofficeapp.view.hall_holidays.holidays_landing', name='hall-holidays'),
    url(r'^add-new-holidays/', 'backofficeapp.view.hall_holidays.add_new_holidays', name='add-new-holidays'),
    url(r'^save-new-holiday/', 'backofficeapp.view.hall_holidays.save_new_holiday', name='save-new-holiday'),
    url(r'^get-holiday-data/', 'backofficeapp.view.hall_holidays.get_holiday_data', name='get-holiday-data'),
    url(r'^update-holiday-status/', 'backofficeapp.view.hall_holidays.update_holiday_status',
        name='update-holiday-status'),
    url(r'^hall-holiday-edit/', 'backofficeapp.view.hall_holidays.hall_holiday_edit', name='hall-holiday-edit'),

    url(r'^edit-new-holiday/','backofficeapp.view.hall_holidays.edit_new_holiday', name='edit-new-holiday'),
    url(r'^get-hall-list-location/','backofficeapp.view.hall_holidays.get_hall_list_location',name='get_hall_list_location'),
    url(r'^edit-hall-list-location/','backofficeapp.view.hall_holidays.edit_hall_list_location',name='edit_hall_list_location'),

    # TODO -----------Manage Holidays Urls End----------------------

    # TODO---------- hall Equipment start ---------------------------
    url(r'^hall-equipment/', 'backofficeapp.view.hall_equipment.hall_equipment_landing', name='hall-equipment'),
    url(r'^add-new-hall-equipment/', 'backofficeapp.view.hall_equipment.add_new_hall_equipment',
        name='add-new-hall-equipment'),
    url(r'^save-new-hall-equipment/', 'backofficeapp.view.hall_equipment.save_new_hall_equipment',
        name='save-new-holiday'),
    url(r'^load-hall-equipment-table/', 'backofficeapp.view.hall_equipment.load_hall_equipment_table',
        name='load-hall-equipment-table'),
    url(r'^update-hall-equipment-status/', 'backofficeapp.view.hall_equipment.update_hall_equipment_status',
        name='update-hall-equipment-status'),
    url(r'^show-hall-equipment-details/', 'backofficeapp.view.hall_equipment.show_hall_equipment_details',
        name='show-hall-equipment-details'),
    url(r'^save-edit-hall-equipment/', 'backofficeapp.view.hall_equipment.save_edit_hall_equipment',
        name='save_edit_hall_equipment'),

    # TODO---------- hall Equipmet End-------------------------------

    # TODO---------- Manage Hall start -------------------------------
    url(r'^manage-halls/', 'backofficeapp.view.manage_hall.manage_hall_landing', name='manage-halls'),
    url(r'^get-manage-halls-datatable/', 'backofficeapp.view.manage_hall.get_manage_halls_datatable',
        name='get_manage_halls_datatable'),
    url(r'^add-new-hall-details/', 'backofficeapp.view.manage_hall.add_new_hall_details', name='add-new-hall-details'),
    url(r'^save-hall-details/', 'backofficeapp.view.manage_hall.save_hall_details', name='save_hall_details'),
    url(r'^update-hall-status/', 'backofficeapp.view.manage_hall.update_hall_status', name='update_hall_status'),
    url(r'^manage-hall-edit/', 'backofficeapp.view.manage_hall.manage_hall_edit', name='manage_hall_edit'),
    url(r'^hall-equipment-list/', 'backofficeapp.view.manage_hall.hall_equipment_list', name='hall_equipment_list'),
    url(r'^edit-hall-details/', 'backofficeapp.view.manage_hall.edit_hall_details', name='edit_hall_details'),
    url(r'^manage-get-hall-list/', 'backofficeapp.view.manage_hall.manage_get_hall_list', name='manage_get_hall_list'),
    url(r'^edit-manage-get-hall-list/', 'backofficeapp.view.manage_hall.edit_manage_get_hall_list',
        name='edit_manage_get_hall_list'),

    url(r'^get-hall-facility-list/', 'backofficeapp.view.manage_hall.get_hall_facility_list',
        name='get_hall_facility_list'),
    # TODO---------- Manage Hall End----------------------------------

    # TODO----------Hall Booking Registration Start---------------------------
    url(r'^hall-booking-registration/',
        'backofficeapp.view.hall_booking_registration.hall_booking_registration_landing',
        name='hall_booking_registration_landing'),
    url(r'^get-hall-list/', 'backofficeapp.view.hall_booking_registration.get_hall_list', name='get_hall_list'),
    url(r'^get-hall-regs-datatable/', 'backofficeapp.view.hall_booking_registration.get_hall_regs_datatable',
        name='get_hall_regs_datatable'),

    # Open Edit, Accept, Reject Booking & Payment URL Start
    url(r'^open-edit-booking/(?P<booking_id>\d+)/$', 'backofficeapp.view.hall_booking_registration.open_edit_booking',
        name='open_edit_booking'),
    url(r'^reject-booking/', 'backofficeapp.view.hall_booking_registration.reject_booking', name='reject_booking'),
    url(r'^accept-booking/', 'backofficeapp.view.hall_booking_registration.accept_booking', name='accept_booking'),
    url(r'^submit-hall-booking-offline-payment/',
        'backofficeapp.view.hall_booking_registration.submit_hall_booking_offline_payment',
        name='submit_hall_booking_offline_payment'),
    url(r'^send-link-for-online-payment/', 'backofficeapp.view.hall_booking_registration.send_link_for_online_payment',
        name='send_link_for_online_payment'),
    url(r'^pay-payment-online-link/(?P<booking_id>\d+)/(?P<tds_amount_hall_booking>\d+)/$',
        'backofficeapp.view.hall_booking_registration.pay_payment_online_link',
        name='pay_payment_online_link'),

    url(r'^update-booking-deposit/', 'backofficeapp.view.hall_booking_registration.update_booking_deposit',
        name='update_booking_deposit'),
    url(r'^get-cheque-details/', 'backofficeapp.view.hall_booking_registration.get_cheque_details',
        name='get_cheque_details'),
    url(r'^add-cheque-details/', 'backofficeapp.view.hall_booking_registration.add_cheque_details',
        name='add_cheque_details'),

    url(r'^send-booking-proforma-mail/', 'backofficeapp.view.hall_booking_registration.send_booking_proforma_mail',
        name='send_booking_proforma_mail'),
    url(r'^send-booking-proforma-mail-page-render/',
        'backofficeapp.view.hall_booking_registration.send_booking_proforma_mail_page_render',
        name="send_booking_proforma_mail_page_render"),
    url(r'^edit-booking-proforma-mail-page-render/',
        'backofficeapp.view.hall_booking_registration.edit_booking_proforma_mail_page_render',
        name="edit_booking_proforma_mail_page_render"),
    url(r'^update-booking-proforma-mail/', 'backofficeapp.view.hall_booking_registration.update_booking_proforma_mail',
        name="update_booking_proforma_mail"),

    url(r'^open-extra-booking/(?P<booking_id>\d+)/$', 'backofficeapp.view.hall_booking_registration.open_extra_booking',
        name='open_extra_booking'),
    url(r'^get-hall-booking-details/', 'backofficeapp.view.hall_booking_registration.get_hall_booking_details',
        name='get_hall_booking_details'),
    url(r'^add-extra-hour-details/', 'backofficeapp.view.hall_booking_registration.add_extra_hour_details',
        name='add_extra_hour_details'),

    # Open Edit, Accept, Reject Booking URL & Payment End

    # TODO----------Hall Booking Registration End-------------------------------

    # TODO----------Hall Booking Report Start-----------------------------------
    url(r'^hall-booking-report/', 'backofficeapp.view.hall_booking_report.hall_booking_report_landing',
        name='hall-booking-report'),
    url(r'^get-hall-regs-report-datatable/', 'backofficeapp.view.hall_booking_report.get_hall_regs_report_datatable',
        name='get_hall_regs_report_datatable'),
    # TODO----------Hall Booking Report End-------------------------------------

    # TODO---------- Internal Hall Booking start---------------------------
    url(r'^internal-hall-booking/', 'backofficeapp.view.internal_hallbooking_landing.internal_hall_booking_landing',
        name='internal-hall-booking'),
    # url(r'^add-new-announcement/', 'backofficeapp.view.special_announcement.add_new_announcement', name='add-new-announcement'),
    # TODO---------- Internal Hall Booking End------------------------------

    # TODO---------- Special Announcement start---------------------------
    url(r'^special-announcement/', 'backofficeapp.view.special_announcement.special_announcement_landing',
        name='special-announcement'),
    url(r'^add-new-hallannouncement/', 'backofficeapp.view.special_announcement.add_new_announcement',
        name='add-new-announcement'),
    # url(r'^save-hall-announcement/', 'backofficeapp.view.special_announcement.save_hall_announcement_details', name='save_announcement_details'),

    # TODO---------- Special Announcement end-----------------------------
    url(r'^save-hall-announcement/', 'backofficeapp.view.special_announcement.save_hall_announcement',
        name='save_announcement_details'),
    url(r'^hall-get-announvcement/', 'backofficeapp.view.special_announcement.hall_get_announvcement',
        name='hall_get_announvcement'),
    url(r'^show-hall-announcement-details/', 'backofficeapp.view.special_announcement.show_hall_announcement_details',
        name='show_event_announcement_details'),
    url(r'^save-edit-hall-announcement-details/',
        'backofficeapp.view.special_announcement.save_edit_hall_announcement_details',
        name='show_event_announcement_details'),
    url(r'^update-hall-announcement-status/', 'backofficeapp.view.special_announcement.update_hall_announcement_status',
        name='update_event_announcement_status'),
    # TODO---------- Special Announcement end-----------------------------

    # TODO---------- Hall Cancellation Policy Start-----------------------------
    url(r'^cancellation-policy-landing/', 'backofficeapp.view.hall_cancellation.cancellation_policy_landing',
        name='cancellation_policy_landing'),
    url(r'^add-new-policy-landing/', 'backofficeapp.view.hall_cancellation.add_new_policy_landing',
        name='add_new_policy_landing'),
    url(r'^save-new-cancel-policy/', 'backofficeapp.view.hall_cancellation.save_new_cancel_policy',
        name='save_new_cancel_policy'),
    url(r'^get-hall-cancel-policy-table/', 'backofficeapp.view.hall_cancellation.get_hall_cancel_policy_table',
        name='get_hall_cancel_policy_table'),
    url(r'^cancel-booking-detail/', 'backofficeapp.view.hall_cancellation.cancel_booking_detail',
        name='cancel_booking_detail'),
    url(r'^cancel-hall-booking/', 'backofficeapp.view.hall_cancellation.cancel_hall_booking',
        name='cancel_hall_booking'),
    # TODO---------- Hall Cancellation Policy End-----------------------------

    url(r'^event-announcement/', 'backofficeapp.view.event_announcement.event_announcement_landing',
        name='event_announcement_landing'),
    url(r'^add-new-announcement/', 'backofficeapp.view.event_announcement.add_new_announcement',
        name='add_new_announcement'),
    url(r'^save-announcement-details/', 'backofficeapp.view.event_announcement.save_announcement_details',
        name='save_announcement_details'),
    url(r'^get-event-detail/', 'backofficeapp.view.event_announcement.get_event_detail',
        name='save_announcement_details'),
    url(r'^show-event-announcement-details/', 'backofficeapp.view.event_announcement.show_event_announcement_details',
        name='show_event_announcement_details'),
    url(r'^save-edit-event-announcement-details/',
        'backofficeapp.view.event_announcement.save_edit_event_announcement_details',
        name='show_event_announcement_details'),
    url(r'^update-event-announcement-status/', 'backofficeapp.view.event_announcement.update_event_announcement_status',
        name='update_event_announcement_status'),
    url(r'^delete-event/', 'backofficeapp.view.delete_event.delete_event', name='delete_event'),
    url(r'^get-delete-events/', 'backofficeapp.view.delete_event.get_delete_events', name='get_delete_events'),
    url(r'^action-delete-event/', 'backofficeapp.view.delete_event.action_delete_event', name='action_delete_event'),

    # ---------- Manage Blacklisting/ Deposit Url start ---------------------------
    url(r'^user-blacklisting-landing/', 'backofficeapp.view.user_blacklisting.user_blacklisting_landing',
        name='user_blacklisting_landing'),
    url(r'^security-deposite-landing/', 'backofficeapp.view.user_blacklisting.security_deposite_landing',
        name='security_deposite_landing'),
    url(r'^security-deposit-details-datatable/',
        'backofficeapp.view.user_blacklisting.security_deposit_details_datatable',
        name='security_deposit_details_datatable'),
    url(r'^load-blacklisting-table/', 'backofficeapp.view.user_blacklisting.load_blacklisting_table',
        name='load_blacklisting_table'),
    url(r'^update-user-track-status/', 'backofficeapp.view.user_blacklisting.update_user_track_status',
        name='update_user_track_status'),
    url(r'^return-user-deposit/', 'backofficeapp.view.user_blacklisting.return_user_deposit',
        name='return_user_deposit'),
    url(r'^deposit-cheque-details-return/', 'backofficeapp.view.user_blacklisting.deposit_cheque_details_return',
        name='deposit_cheque_details_return'),
    url(r'^get-deposit-status/', 'backofficeapp.view.user_blacklisting.get_deposit_status', name='get_deposit_status'),
    #   ------ Manage Blacklisting/ Deposit Url End-------------------------------

    # Cheque Bounce Urls
    url(r'^cheque-bounce/', 'backofficeapp.view.cheque_bounce.cheque_bounce', name='cheque_bounce'),
    url(r'^cheque-details/(?P<booking_id>\d+)/$', 'backofficeapp.view.cheque_bounce.cheque_details',
        name='cheque_details'),
    url(r'^get-cheque-datatable/', 'backofficeapp.view.cheque_bounce.get_cheque_datatable',
        name='get_cheque_datatable'),
    url(r'^get-cheque-details-datatable/', 'backofficeapp.view.cheque_bounce.get_cheque_details_datatable',
        name='get_cheque_details_datatable'),
    url(r'^get-bounce-cheque-details/', 'backofficeapp.view.cheque_bounce.get_bounce_cheque_details',
        name='get_bounce_cheque_details'),
    url(r'^update-cheque-details/', 'backofficeapp.view.cheque_bounce.update_cheque_details',
        name='update_cheque_details'),

    # --------------------Events Registrations-----------------
    url(r'^event-registrations/', 'backofficeapp.view.event_home.event_registrations', name='event_registrations'),
    url(r'^get-events-registrations-datatable/', 'backofficeapp.view.event_home.get_events_registrations_datatable',
        name='get_events_registrations_datatable'),
    url(r'^update-event-reg-status/', 'backofficeapp.view.event_home.update_event_reg_status',
        name='update_event_reg_status'),
    url(r'^get-event-registrations-details/', 'backofficeapp.view.event_home.get_event_registrations_details',
        name='get_event_registrations_details'),
    url(r'^get-model-registrations-datatable/', 'backofficeapp.view.event_home.get_model_registrations_datatable',
        name='get_model_registrations_datatable'),
    url(r'^save-payment-by-cash/', 'backofficeapp.view.event_home.save_payment_by_cash', name='save_payment_by_cash'),
    url(r'^save-payment-by-cheque/', 'backofficeapp.view.event_home.save_payment_by_cheque',
        name='save_payment_by_cheque'),
    url(r'^save-payment-by-neft/', 'backofficeapp.view.event_home.save_payment_by_neft', name='save_payment_by_neft'),
    url(r'^invites-attendees-data/', 'backofficeapp.view.event_home.invites_attendees_data',
        name='invites_attendees_data'),
    url(r'^get-invites-attendees-datatable/', 'backofficeapp.view.event_home.get_invites_attendees_datatable',
        name='get_invites_attendees_datatable'),
    url(r'^update-invites-attendees-details/', 'backofficeapp.view.event_home.update_invites_attendees_details',
        name='update_invites_attendees_details'),

    # url(r'^get-events-registration-receipt/', 'backofficeapp.view.event_home.get_events_registration_receipt', name='get_events_registration_receipt'),

    url(r'^upcoming-event-download/', 'backofficeapp.view.event_report.upcoming_event_download',
        name='upcoming_event_download'),

    url(r'^event-participant-report/', 'backofficeapp.view.event_report.event_participant_report',
        name='event_participant_report'),

    url(r'^delete-event-participant/', 'backofficeapp.view.delete_event_participent.delete_event_participantt',
        name='delete_event_participant'),
    url(r'^get-delete-events-registrations/',
        'backofficeapp.view.delete_event_participent.get_delete_events_registrations',
        name='get_delete_events_registrations'),
    url(r'^action-delete-event-participent/',
        'backofficeapp.view.delete_event_participent.action_delete_event_participent',
        name='action_delete_event_participent'),

    url(r'^get-events-report-datatable/', 'backofficeapp.view.event_report.get_events_report_datatable',
        name='get_events_report_datatable'),
    url(r'^event-participant-attandance/', 'backofficeapp.view.event_report.event_participant_attandance',
        name='event_participant_attandance'),
    url(r'^download-event-participant-data/', 'backofficeapp.view.event_report.download_event_participant_data',
        name='download_event_participant_data'),

    url(r'^administrator/', administrator.administrator_landing, name='administrator_landing'),
    url(r'^administrator-country-landing/', administrator.administrator_country_landing,
        name='administrator_country_landing'),
    url(r'^add-new-country/', administrator.add_new_country, name='add_new_country'),
    url(r'^save-country-details/', administrator.save_country_details, name='save_country_details'),
    url(r'^update-country-status/', administrator.update_country_status, name='update_country_status'),
    url(r'^get-country-list/', administrator.get_country_list, name='get_country_list'),
    url(r'^show-country-detail/', administrator.show_country_detail, name='show_country_detail'),
    url(r'^save-edit-country-details/', administrator.save_edit_country_details, name='show_country_detail'),

    url(r'^administrator-state-landing/', administrator.administrator_state_landing,
        name='administrator_state_landing'),
    url(r'^add-new-state/', administrator.add_new_state, name='add_new_state'),
    url(r'^save-state-details/', administrator.save_state_details, name='save_state_details'),
    url(r'^update-state-status/', administrator.update_state_status, name='update_state_status'),
    url(r'^get-state-list/', administrator.get_state_list, name='get_state_list'),
    url(r'^show-state-detail/', administrator.show_state_detail, name='show_state_detail'),
    url(r'^save-edit-state-details/', administrator.save_edit_state_details, name='show_state_detail'),

    url(r'^administrator-city-landing/', administrator.administrator_city_landing, name='administrator_city_landing'),
    url(r'^add-new-city/', administrator.add_new_city, name='add_new_city'),
    url(r'^save-city-details/', administrator.save_city_details, name='save_city_details'),
    url(r'^update-city-status/', administrator.update_city_status, name='update_city_status'),
    url(r'^get-city-list/', administrator.get_city_list, name='get_city_list'),
    url(r'^show-city-detail/', administrator.show_city_detail, name='show_city_detail'),
    url(r'^save-edit-city-details/', administrator.save_edit_city_details, name='show_city_detail'),

    url(r'^administrator-servicetax-landing/', administrator.administrator_servicetax_landing,
        name='administrator_servicetax_landing'),
    url(r'^add-new-servicetax/', administrator.add_new_servicetax, name='add_new_servicetax'),
    url(r'^save-servicetax-details/', administrator.save_servicetax_details, name='save_servicetax_details'),
    url(r'^update-servicetax-status/', administrator.update_servicetax_status, name='update_servicetax_status'),
    url(r'^get-servicetax-list/', administrator.get_servicetax_list, name='get_servicetax_list'),
    url(r'^show-servicetax-detail/', administrator.show_servicetax_detail, name='show_servicetax_detail'),
    url(r'^save-edit-servicetax-details/', administrator.save_edit_servicetax_details, name='show_servicetax_detail'),

    url(r'^administrator-user-role/', administrator.administrator_user_role_landing,
        name='administrator_user_role_landing'),
    url(r'^show-user-role-detail/', administrator.show_user_role_detail, name='show_user_role_detail'),
    url(r'^get-user-role-list/', administrator.get_user_role_list, name='get_user_role_list'),
    url(r'^add-new-user-role/', administrator.add_new_user_role, name='add_new_user_role'),
    url(r'^save-user-role-details/', administrator.save_user_role_details, name='save_user_role_details'),
    url(r'^update-user-role-status/', administrator.update_user_role_status, name='update_user_role_status'),
    url(r'^save-edit-user-role-details/', administrator.save_edit_user_role, name='save_edit_user_role'),

    url(r'^administrator-user-landing/', administrator.administrator_user_landing, name='administrator_user_landing'),
    url(r'^add-new-user-detail/', administrator.add_new_user_detail, name='add_new_user_detail'),
    url(r'^get-user-detail-list/', administrator.get_user_detail_list, name='get_user_detail_list'),
    url(r'^save-user-details/', administrator.save_user_details, name='save_user_details'),
    url(r'^show-user-detail/', administrator.show_user_detail, name='show_user_detail'),
    url(r'^update-user-detail-status/', administrator.update_user_detail_status, name='update_user_detail_status'),
    url(r'^save-edit-user-detail/', administrator.save_edit_user_detail, name='save_edit_user_detail'),

    url(r'login/', administrator.login_check),

    url(r'^events-reciept/', membership_home.download_event_reciept, name='show_servicetax_detail'),

    # Commiittee Urls
    url(r'^add-committee/', event_committee.add_committee, name='add_committee'),
    url(r'^get-committee-datatable/', event_committee.get_committee_datatable, name='get_committee_datatable'),
    url(r'^update-committee-status/', event_committee.update_committee_status, name='update_committee_status'),
    url(r'^add-committee-form/', event_committee.add_committee_form, name='add_committee_form'),
    url(r'^save-new-committee/', event_committee.save_new_committee, name='save_new_committee'),
    url(r'^edit-committee-form/', event_committee.edit_committee_form, name='edit_committee_form'),
    url(r'^update-committee-form/', event_committee.update_committee_form, name='update_committee_form'),

    # Event Type
    url(r'^add-event-type/', event_type.add_event_type, name='add_event_type'),
    url(r'^get-event-type-datatable/', event_type.get_event_type_datatable, name='get_event_type_datatable'),
    url(r'^update-event-type-status/', event_type.update_event_type_status, name='update_event_type_status'),
    url(r'^add-event-type-form/', event_type.add_event_type_form, name='add_event_type_form'),
    url(r'^save-new-event-type/', event_type.save_new_event_type, name='save_new_event_type'),
    url(r'^edit-event-type-form/', event_type.edit_event_type_form, name='edit_event_type_form'),
    url(r'^update-event-type-form/', event_type.update_event_type_form, name='update_event_type_form'),

    # Start:Department urls
    url(r'^administrator-department-landing/', administrator.administrator_department_landing,
        name='administrator_department_landing'),
    url(r'^add-new-department/', administrator.add_new_department, name='add_new_department'),
    url(r'^save-department-details/', administrator.save_department_details, name='save_department_details'),
    url(r'^update-department-status/', administrator.update_department_status, name='update_department_status'),
    url(r'^get-department-list/', administrator.get_department_list, name='get_department_list'),
    url(r'^show-department-detail/', administrator.show_department_detail, name='show_department_detail'),
    url(r'^save-edit-department-details/', administrator.save_edit_department_details,
        name='save_edit_department_details'),
    # End:Department urls

    # Start:designation urls
    url(r'^administrator-designation-landing/', administrator.administrator_designation_landing,
        name='administrator_designation_landing'),
    url(r'^add-new-designation/', administrator.add_new_designation, name='add_new_designation'),
    url(r'^save-designation-details/', administrator.save_designation_details, name='save_designation_details'),
    url(r'^update-designation-status/', administrator.update_designation_status, name='update_designation_status'),
    url(r'^get-designation-list/', administrator.get_designation_list, name='get_designation_list'),
    url(r'^show-designation-detail/', administrator.show_designation_detail, name='show_designation_detail'),
    url(r'^save-edit-designation-details/', administrator.save_edit_designation_details,
        name='save_edit_designation_details'),

    url(r'^payment/', administrator.payment, name='payment'),
    url(r'^get-payment-detail/', administrator.get_payment_detail, name='payment'),
    url(r'^get-payment-detail-response/', administrator.get_payment_detail_response,
        name='get_payment_detail_response'),
    # End:designation urls

    # url(r'^get_meter_data/', event_home.get_meter_data, name='get_meter_data'),

    url(r'^media-home/', media.media_home, name='media_home'),
    url(r'^mccia-leadership/', media.mccia_leadership, name='mccia_leadership'),
    url(r'^add-new-leadership/', media.add_new_leadership, name='add_new_leadership'),
    url(r'^add-new-member/', media.add_new_member, name='add_new_member'),
    url(r'^mccia-team/', media.mccia_team, name='mccia_team'),
    url(r'^print-media/', media.print_media, name='print_media'),
    url(r'^print-media-new/', media.print_media_new, name='print_media_new'),
    url(r'^video-gallery/', media.video_gallery, name='video_gallery'),
    url(r'^add-video-links/', media.add_video_links, name='add_video_links'),
    url(r'^electronic-media/', media.electronic_media, name='electronic_media'),
    url(r'^add-electronic-media/', media.add_electronic_media, name='add_electronic_media'),
    url(r'^save-leader-details/', media.save_leader_details, name='save_leader_details'),
    url(r'^get-mccia-leaders-details/', media.get_mccia_leaders_details, name='get_mccia_leaders_details'),
    url(r'^get-mccia-team-details/', media.get_mccia_team_details, name='get_mccia_team_details'),
    url(r'^save-team-details/', media.save_team_details, name='save_team_details'),
    url(r'^save-video-link/', media.save_video_link, name='save_video_link'),
    url(r'^get-video-gallery/', media.get_video_gallery, name='get_video_gallery'),
    url(r'^save-electronic-media/', media.save_electronic_media, name='save_electronic_media'),
    url(r'^get-electronic-media/', media.get_electronic_media, name='get_electronic_media'),

    # Awards url
    url(r'^awards-landing/', awards_landing.awards_landing, name='awards_landing'),
    url(r'^awards-register/', awards_landing.awards_register, name='awards_register'),
    url(r'^get-award-registration-datatable/', awards_landing.get_award_registration_datatable,
        name='get_award_registration_datatable'),
    url(r'^download-award-reg-form/(?P<award_reg_id>\d+)/$', awards_landing.download_award_reg_form,
        name='download_award_reg_form'),
    url(r'^download-award-data/(?P<award_id>\w+)/$', awards_landing.download_award_data, name='download_award_data'),

    # Membership Renewal Configuration, Letter URL
    url(r'^renewal-config-landing/', renewal_landing.renewal_config_landing, name='renewal_config_landing'),
    url(r'^update-renew-mail-letter-landing/', renewal_landing.update_renew_mail_letter_landing,
        name='update_renew_mail_letter_landing'),
    url(r'^upload-renew-schedule-landing/', renewal_landing.upload_renew_schedule_landing,
        name='upload_renew_schedule_landing'),
    url(r'^upload-schedule-file/', renewal_landing.upload_schedule_file, name='upload_schedule_file'),
    url(r'^get-schedule-datatable/', renewal_landing.get_schedule_datatable, name='schedule_datatable-file'),
    url(r'^upload-membership-schedule-landing/', renewal_landing.upload_membership_schedule_landing,
        name='upload_membership_schedule_landing'),
    url(r'^upload-membership-schedule-file/', renewal_landing.upload_membership_schedule_file,
        name='upload_membership_schedule_file'),
    url(r'^get-membership-schedule-datatable/', renewal_landing.get_membership_schedule_datatable,
        name='get_membership_schedule_datatable'),
    url(r'^save-renew-letter-text/', renewal_landing.save_renew_letter_text, name='save_renew_letter_text'),
    url(r'^get-renew-letter-details/', renewal_landing.get_renew_letter_details, name='get_renew_letter_details'),

]
