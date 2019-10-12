from django.conf.urls import include, url
from awardsapp.view import awards_landing, save_award

__author__ = 'Priyanka'

urlpatterns = [
    url(r'^awards-home/$', awards_landing.awards_home, name="awards_home"),
    url(r'^awards-details/$', awards_landing.awards_details, name="awards_details"),
    url(r'^awards-details1/$', awards_landing.awards_details1, name="awards_details_1"),
    url(r'^awards-details2/$', awards_landing.awards_details2, name="awards_details_2"),
    url(r'^awards-details3/$', awards_landing.awards_details3, name="awards_details_3"),
    url(r'^awards-details4/$', awards_landing.awards_details4, name="awards_details_4"),
    url(r'^awards-details5/$', awards_landing.awards_details5, name="awards_details_5"),
    url(r'^awards-details6/$', awards_landing.awards_details6, name="awards_details_5"),

    url(r'^awards-registration/$', awards_landing.awards_registration, name="awards_registration"),
    url(r'^awards-registration/(?P<award_id>\d+)/$', awards_landing.awards_registration, name="awards_registration"),

    url(r'^save-award-registration/$', save_award.save_award_registration, name="save_award_registration"),
       
]
