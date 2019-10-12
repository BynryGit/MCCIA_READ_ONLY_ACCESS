
from django.conf.urls import include, url
from adminapp.view import import_data

urlpatterns = [

    url(r'^load-membership-category-data/', import_data.load_membership_category_data, name='load_membership_category_data'),
    url(r'^load-criteria-data/', import_data.load_criteria_data, name='load_criteria_data'),

    url(r'^load-slab-data/', import_data.load_slab_data,name='load_slab_data'),
    url(r'^load-state-data/', import_data.load_state_data,name='load_state_data'),

    # url(r'^load-embassy-data/', import_data.load_embassy_data,name='load_embassy_data'),

]