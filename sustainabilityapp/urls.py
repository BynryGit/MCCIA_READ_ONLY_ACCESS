from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^sustainability-desk/$', views.sustainability_desk, name="sustainability_desk"),
    url(r'^sustainability-tab/$', views.sustainability_tab, name="sustainability_tab"),
]
