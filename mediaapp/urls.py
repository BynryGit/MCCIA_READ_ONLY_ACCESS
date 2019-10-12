
    
from django.conf.urls import include, url
from mediaapp.view import media

urlpatterns = [    
    #--------------------Media Urls-----------------
    # Upload Banner Url
    url(r'^upload-banner/', media.banner_landing, name='banner_landing'),
    url(r'^add-new-banner/', media.add_new_banner, name='add_new_banner'),
    url(r'^save-new-banner/', media.save_new_banner, name='save_new_banner'),
    url(r'^get-banner-datatable/', media.get_banner_datatable, name='get_banner_datatable'),
    url(r'^update-banner-status/', media.update_banner_status, name='update_banner_status'),
    url(r'^edit-banner/', media.edit_banner, name='edit_banner'),
    url(r'^update-banner/', media.update_banner, name='update_banner'),

    # Create Link to Share Url
    url(r'^link-to-download/', media.link_to_download, name='link_to_download'),
    url(r'^get-link-datatable/', media.get_link_datatable, name='get_link_datatable'),
    url(r'^create-link/', media.create_link, name='create_link'),
    url(r'^save-new-link/', media.save_new_link, name='save_new_link'),
    url(r'^update-link-status/', media.update_link_status, name='update_link_status'),
    url(r'^edit-link/', media.edit_link, name='edit_link'),
	url(r'^update-link/', media.update_link, name='update_link'),
]


