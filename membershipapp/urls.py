from django.conf.urls import include, url
from membershipapp.view import membership_landing,membership_invoice



urlpatterns = [
    url(r'^membership-home',membership_landing.membership_home,name="membership_home"),
    url(r'^member-benifits',membership_landing.member_benifits,name="member-benifits"),
    url(r'^eligibility-criteria',membership_landing.eligibility_criteria,name="eligibility-criteria"),
    url(r'^about-us/$',membership_landing.about_us,name="about_us"),
    url(r'^landing_page/$',membership_landing.landing_page,name="landing_page"),
    url(r'^membership-form/$',membership_landing.membership_form,name="membership_form"),
    url(r'^membership-form-admin/$',membership_landing.membership_form_admin,name="membership_form_admin"),
    url(r'^get-membership-category/$',membership_landing.get_membership_category,name="get_membership_category"),
    url(r'^get-slab/$',membership_landing.get_slab,name="get_slab"),
    url(r'^get-slab-admin/$',membership_landing.get_slab_admin,name="get_slab_admin"),
    url(r'^member-pre-invoice/$',membership_landing.member_pre_invoice,name="member_pre_invoice"),
    url(r'^member-invoice/$',membership_landing.member_invoice,name="member_invoice"),
    # url(r'^member-invoice-calculation/(?P<slab_id>\d+)/$',membership_invoice.member_invoice,name="member_invoice"),
    url(r'^save-member-invoice-detail/$',membership_landing.save_member_invoice_detail,name="save_member_invoice_detail"),


    url(r'^save-new-member/$',membership_landing.save_new_member,name="save_new_member"),
    url(r'^article-of-associations/$',membership_landing.article_of_association,name="article_of_association"),
    url(r'^get-city/$',membership_landing.get_city,name="get_city"),

    url(r'^elected-member/$', membership_landing.elected_member),
    url(r'^co-members/$', membership_landing.co_members),
    url(r'^chairman-committee/$', membership_landing.chairman_committee),
    url(r'^special-invitees/$', membership_landing.special_invitees),

    # Edit & Renew Member Profile using Member Login
    url(r'^edit-member-profile/$', membership_landing.edit_member_profile, name='edit_member_profile'),
    url(r'^update-member-profile/$', membership_landing.update_member_profile, name='update_member_profile'),
    url(r'^renew-member-profile-page/$', membership_landing.renew_member_profile_page, name='renew_member_profile_page'),
    url(r'^get-renew-invoice/$', membership_landing.get_renew_invoice, name='get_renew_invoice'),
    url(r'^renew-member-request/$', membership_landing.renew_member_request, name='renew_member_request'),
    url(r'^renew-membership-response-save/$', membership_landing.renew_membership_response_save, name='renew_membership_response_save'),

    # Member Ageing / Time Line for Member
    url(r'^member-timeline/$', membership_landing.member_timeline, name='member_timeline'),
    url(r'^get-member-timeline-data/$', membership_landing.get_member_timeline_data, name='get_member_timeline_data'),

]