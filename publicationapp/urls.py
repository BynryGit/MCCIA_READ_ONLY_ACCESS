from django.conf.urls import include, url
from publicationapp.view import publication_landing, publication_backoffice



urlpatterns = [
    url(r'^publication-landing',publication_backoffice.publications_backoffice_landing_page,name="publications_landing_page"),
    url(r'^upload-publication',publication_backoffice.upload_publication,name="upload-publication"),
    url(r'^add-new-publication',publication_backoffice.add_new_publication,name="add-new-publication"),
    url(r'^save-new-publication',publication_backoffice.save_new_publication,name="save-new-publication"),
    url(r'^get-publication-datatable',publication_backoffice.get_publication_datatable,name="get-publication-datatable"),
    url(r'^update-publication-status',publication_backoffice.update_publication_status,name="update_publication_status"),
    url(r'^show-publication-details',publication_landing.show_publication_details,name="show_publication_details"),
    url(r'^get-anual-report-details', publication_landing.get_anual_report_details, name="get_anual_report_details"),
    url(r'^get-sampada-details', publication_landing.get_sampada_details, name="get_sampada_details"),
    url(r'^get-world-of-business-details', publication_landing.get_world_of_business_details, name="get_world_of_business_details"),
    url(r'^labels-for-sampada', publication_landing.labels_for_sampada,name="labels_for_sampada"),

    # url(r'^publications-home',publication_landing.,),
    # url(r'^publications-details/$',publication_landing.publications_details,name="publications_details"),
]
