from django.conf.urls import include, url
from backoffice.membershipapp.view import membership_home



urlpatterns = [
    url(r'^membership-home/', 'backoffice.membershipapp.view.membership_home', name='membership_home'),
    url(r'^membership-details/', 'backoffice.membershipapp.view.membership_details', name='membership_details'),
    url(r'^add-membership-details/', 'backoffice.membershipapp.view.add_membership_details', name='add_membership_details'),
    url(r'^membership-category/', 'backoffice.membershipapp.view.membership_category', name='membership_category'),
    url(r'^add-membership-category/', 'backoffice.membershipapp.view.add_membership_category', name='add_membership_category'),
    url(r'^membership_certificate_dispatched/', 'backoffice.membershipapp.view.membership_certificate_dispatched', name='membership_certificate_dispatched'),
    url(r'^industry-details/', 'backoffice.membershipapp.view.industry_details', name='industry_details'),
    url(r'^add-industry-details/', 'backoffice.membershipapp.view.add_industry_details', name='add_industry_details'),
    url(r'^legal-details/', 'backoffice.membershipapp.view.legal_details', name='legal_details'),
    url(r'^add-legal-details/', 'backoffice.membershipapp.view.add_legal_details', name='add_legal_details'),
    url(r'^executive-committee-members/', 'backoffice.membershipapp.view.executive_committee_members', name='executive_committee_members'),
    url(r'^top3-members/', 'backoffice.membershipapp.view.top3_members', name='top3_members'),
    url(r'^add-top3-members/', 'backoffice.membershipapp.view.add_top3_members', name='add_top3_members'),
    url(r'^slab/', 'backoffice.membershipapp.view.slab', name='slab'),
    url(r'^add-new-slab/', 'backoffice.membershipapp.view.add_new_slab', name='add_new_slab'),
    url(r'^exclude-mailing-members/', 'backoffice.membershipapp.view.exclude_mailing_members', name='exclude_mailing_members'),
]
