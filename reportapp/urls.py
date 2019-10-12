from django.conf.urls import include, url

from reportapp.view import membership_report, hall_booking_report

urlpatterns = [
    # Membership Report URLS
    url(r'^membership-report-landing/', membership_report.membership_report_landing, name='membership_report_landing'),
    url(r'^membership-ec-report-landing/', membership_report.membership_ec_report_landing,
        name='membership_ec_report_landing'),
    url(r'^download-ec-report-file/', membership_report.download_ec_report_file, name='download_ec_report_file'),
    url(r'^download-ec-report-count/',membership_report.download_ec_report_count, name ='download_ec_report_count'),
    url(r'^membership-account-report-landing/', membership_report.membership_account_report_landing,
        name='membership_account_report_landing'),
    url(r'^account-report-file-count/',membership_report.account_report_file_count, name = 'account_report_file_count'),
    url(r'^download-account-report-file/', membership_report.download_account_report_file, name='download_account_report_file'),
    url(r'^membership-data-download/', membership_report.membership_data_download, name='membership_data_download'),
    url(r'^download-members-data/',membership_report.download_members_data, name = 'download_members_data'),
    url(r'^membership-detail-reports/',membership_report.membership_online_renewal, name= 'membership_online_renewal'),
    url(r'^check-membership-online-renewal-count/',membership_report.check_membership_online_renewal_count),
    url(r'^renewal-new-member-report-landing/',membership_report.membership_online_renewal_download),
    url(r'^membership-change-company-name/',membership_report.membership_change_company_name,name='membership_change_company_name'),
    url(r'^change-company-name-details-datatable/',membership_report.change_company_name_details_datatable,name='change_company_name_details_datatable'),
    url(r'^download-company-name-details/',membership_report.download_company_name_details),
    url(r'^change-company-name-excel/',membership_report.change_company_name_excel),
    # url(r'^upload-ec-report-file/', membership_report.membership_data_upload, name='membership_data_upload'),
    url(r'^membership-subscription-report/',membership_report.membership_subscription_report,name='membership_subscription_report'),
    # TODO cheque details
    url(r'^membership-cheque-bounce-report/',membership_report.membership_cheque_bounce_report,name='membership_cheque_bounce_report'),
    url(r'^bounce-cheque-details-datatable/',membership_report.bounce_cheque_details_datatable,name='bounce_cheque_details_datatable'),
    url(r'^download-cheque-details/',membership_report.download_cheque_details,name='download_cheque_details'),
    url(r'^downloadcheque-detail-excel/',membership_report.download_cheque_detail_excel,name='download_cheque_detail_excel'),

    url(r'^check-membership-subscription-count/',membership_report.check_membership_subscription_count,name='check_membership_subscription_count'),
    url(r'^membership-subscription-report/',membership_report.membership_subscription_report,name='membership_subscription_report'),
    url(r'^check-membership-industry-report-count/',membership_report.check_membership_industry_report_count,name='check_membership_industry_report_count'),
    url(r'^membership-industry-report/',membership_report.membership_industry_report,name='membership_industry_report'),
    url(r'^membership-comparative-analysis-report/',membership_report.membership_comparative_analysis_report, name='membership_comparative_analysis_report'),
    url(r'^comparative-analysis-datatable/',membership_report.comparative_analysis_datatable, name='comparative_analysis_datatable'),
    url(r'^download-comparative-analysis-excel/',membership_report.download_comparative_analysis_excel, name = 'download_comparative_analysis_excel'),

    # Hall Booking Report URLS
    url(r'^hall-booking-report-landing/',hall_booking_report.hall_booking_report_landing, name = 'hall_booking_report_landing'),
    # Hall Booking Utilization Report URLS
    url(r'^hall-booking-utilization-revenue-report-landing/',hall_booking_report.hall_booking_utilization_revenue_report_landing, name = 'hall_booking_utilization_revenue_report_landing'),
    url(r'^download-utilization-revenue-details/',hall_booking_report.download_utilization_revenue_details, name = 'download_utilization_revenue_details'),
    url(r'^download-utilization-revenue-report-file/',hall_booking_report.download_utilization_revenue_report_file, name = 'download_utilization_revenue_report_file'),

    # Hall Booking Blacklisting Report URLS
    url(r'^blacklisting-member-report-landing/',hall_booking_report.blacklisting_member_report_landing, name = 'blacklisting_member_report_landing'),
    url(r'^download-blacklisted-member-details/',hall_booking_report.download_blacklisted_member_details, name = 'download_blacklisted_member_details'),
    url(r'^download-blacklisted-member-file/',hall_booking_report.download_blacklisted_member_file, name = 'download_blacklisted_member_file'),
    url(r'^get-member-report-data/', membership_report.get_member_report_data, name='get_member_report_data'),
]
