from django.conf.urls import include, url
from initiativesapp import views


urlpatterns = [
    url(r'^technology-transfer',views.technology_transfer),
    url(r'^mfg-lean/$',views.mfg_lean_transfer),
    url(r'^electronic-clusture/$',views.electronic_clusture),
    url(r'^apprenticeship/$',views.apprenticeship),
    url(r'^enterpreneurship/$',views.enterpreneurship),
]