from django.conf.urls import include, url
from visarecommendationapp.view import visa_recommendation_web, visa_backoffice

__author__ = 'Shubham S'

urlpatterns = [
    url(r'^visa-pre-condition/$', visa_recommendation_web.visa_pre_condition, name="visa_pre_condition"),
    url(r'^visa-recommendations/$', visa_recommendation_web.visa_recommendations, name="visa_recommendations"),
    url(r'^save-visa-recommendation-detail/$', visa_recommendation_web.save_visa_recommendation_detail, name="save_visa_recommendation_detail"),
    url(r'^get-embassy-location/$', visa_recommendation_web.get_embassy_location, name="save_visa_recommendation_detail"),

    url(r'^visa-backoffice-landing/$', visa_backoffice.visa_backoffice_landing, name='visa-backoffice-landing'),
    url(r'^manage-visa/$', visa_backoffice.manage_visa, name='manage_visa'),
    url(r'^get-visa-datatable/$', visa_backoffice.get_visa_datatable, name='get_visa_datatable'),
    url(r'^update-visa-details/$', visa_backoffice.update_visa_details, name='update_visa_details'),
    url(r'^generate-visa-pdf/$', visa_backoffice.generate_visa_pdf, name='generate_visa_pdf'),
    url(r'^edit-visa/$', visa_backoffice.edit_visa, name='edit_visa'),
    url(r'^save-edit-visa-recommendation/$', visa_backoffice.save_edit_visa_recommendation, name='save_edit_visa_recommendation'),

    url(r'^manage-embassy/$', visa_backoffice.manage_embassy, name='manage_embassy'),
    url(r'^get-embassy-datatable/$', visa_backoffice.get_embassy_datatable, name='get_embassy_datatable'),
    url(r'^update-embassy-status/$', visa_backoffice.update_embassy_status, name='update_embassy_status'),
    url(r'^add-embassy-form/', visa_backoffice.add_embassy_form, name='add_embassy_form'),
    url(r'^save-new-embassy/', visa_backoffice.save_new_embassy, name='save_new_embassy'),
    url(r'^edit-embassy-form/', visa_backoffice.edit_embassy_form, name='edit_embassy_form'),
    url(r'^update-embassy-form/', visa_backoffice.update_embassy_form, name='update_embassy_form'),
]
