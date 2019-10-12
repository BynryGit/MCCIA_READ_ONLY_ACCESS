from django.conf.urls import include, url
from committeeapp import views


urlpatterns = [
    url(r'^agriculture',views.agriculture),
    url(r'^defence',views.defence),
    url(r'^electronics',views.electronics),
    url(r'^food-processing',views.food_processing),
    url(r'^infrastructure',views.infrastructure),
    url(r'^sme',views.sme),
    url(r'^women-entrepreneurs',views.women_entrepreneurs),
    url(r'^IT-ITES',views.IT_ITES),
    url(r'^hr',views.hr_ir),
    url(r'^energy',views.energy),
    url(r'^education',views.education_skill_development),
    url(r'^civil-aviation',views.civil_aviation),
    url(r'^ahmednagar',views.ahmednagar),
    url(r'^corporate-legislation',views.corporate_legislation),
    url(r'^foreign-trade',views.foreign_trade),
    url(r'^higher-education-skill-development',views.higher_education_skill_development),
    url(r'^innovation-incubation',views.innovation_incubation),
    url(r'^taxation',views.taxation),
]
