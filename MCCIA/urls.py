"""MCCIA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin as djangoadmin
from awardsapp import urls as awardsappurl
from adminapp import urls as adminappurl
from backofficeapp import urls as backofficeappurl
from eventsapp import urls as eventsappurl
from hallbookingapp import urls as hallbookingappurl

from membershipapp import urls as membershipappurl
from publicationapp import urls as publicationappurl
from initiativesapp import urls as initiativesappurl
from committeeapp import urls as committeeappurl
from reportapp import urls as reportappurl
from authenticationapp import urls as authenticateurl
from visarecommendationapp import urls as visarecommendationurl
from Paymentapp import urls as paymenturl
from mediaapp import urls as mediaappurl
from sustainabilityapp import urls as sustainabilityurl
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('admin/doc/', include('django.contrib.admindocs.urls'))
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^django-admin/', include(djangoadmin.site.urls)),

    url(r'^$','membershipapp.view.membership_landing.landing_page',name='landing_page'),
    url(r'^MahaIndustrialPolicy/','membershipapp.view.membership_landing.maha_industry_policy',name='maha_industry_policy'),
    url(r'^MHGOVT-AMNESTY-SCHEME-2019/','membershipapp.view.membership_landing.mh_govt_amnesty_scheme_2019',name='mh_govt_amnesty_scheme_2019'),
    url(r'^mccia-one-pager-2019/','membershipapp.view.membership_landing.mccia_one_pager_2019',name='mccia_one_pager_2019'),
    url(r'^national-guidelines-on-responsible-business-conduct-2019/','membershipapp.view.membership_landing.national_guidelines_on_responsible_business_conduct_2019',name='responsible_business_conduct_2019'),
    url(r'^get-hall-booking-data/','massmail.get_hall_booking_data',name='get_hall_booking_data'),

    url(r'^adminapp/', include(adminappurl)),
    url(r'^awardsapp/', include(awardsappurl)),
    url(r'^backofficeapp/', include(backofficeappurl)),
    url(r'^eventsapp/', include(eventsappurl)),
    url(r'^hallbookingapp/', include(hallbookingappurl)),
    url(r'^membershipapp/', include(membershipappurl)),
    url(r'^publicationapp/', include(publicationappurl)),
    url(r'^initiativesapp/', include(initiativesappurl)),
    url(r'^committeeapp/', include(committeeappurl)),
    url(r'^reportapp/', include(reportappurl)),
    url(r'^contact-us/', 'initiativesapp.views.contact_us'),
    url(r'^authenticate/',include(authenticateurl)),
    url(r'^media-home/', 'initiativesapp.views.media'),
    url(r'^paymentapp/',include(paymenturl)),
    url(r'^visarecommendationapp/',include(visarecommendationurl)),
    url(r'^mediaapp/',include(mediaappurl)),
    url(r'^sustainabilityapp/', include(sustainabilityurl)),
]
# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# print(urlpatterns)

# URL Backup as we are removing namespace from above ulrs
# urlpatterns = [
#     url(r'^$','membershipapp.view.membership_landing.landing_page',name='landing_page'),
#     # path('admin/doc/', include('django.contrib.admindocs.urls'))
#
#
#
#     url(r'^django-admin/', include(djangoadmin.site.urls)),
#     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#     url(r'^adminapp/', include(adminappurl, namespace='adminapp')),
#     url(r'^awardsapp/', include(awardsappurl, namespace='awardsapp')),
#     url(r'^backofficeapp/', include(backofficeappurl, namespace='backofficeapp')),
#     url(r'^eventsapp/', include(eventsappurl,namespace='eventsapp')),
#     url(r'^hallbookingapp/', include(hallbookingappurl,namespace='hallbookingapp')),
#     url(r'^membershipapp/', include(membershipappurl,namespace='membershipapp')),
#     url(r'^publicationapp/', include(publicationappurl,namespace='publicationapp')),
#     url(r'^initiativesapp/', include(initiativesappurl,namespace='initiativesapp')),
#     url(r'^committeeapp/', include(committeeappurl,namespace='committeeapp')),
#     url(r'^contact-us/', 'initiativesapp.views.contact_us'),
#     url(r'^authenticate/',include(authenticateurl,namespace='authenticateurl')),
#     url(r'^media-home/', 'initiativesapp.views.media'),
#     url(r'^paymentapp/',include(paymenturl,namespace='paymenturl')),
#     url(r'^visarecommendationapp/',include(visarecommendationurl,namespace='visarecommendationapp')),
#     url(r'^mediaapp/',include(mediaappurl,namespace='mediaapp')),
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)