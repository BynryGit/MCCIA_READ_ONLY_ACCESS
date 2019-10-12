from django.conf.urls import include, url
from accountapp.view import account_membership


urlpatterns = [
	url(r'^accounts-landing/', account_membership.account, name='accounts_landing'),

	 # Download Payment Details / Labels
    url(r'^download-account-label/', account_membership.download_account_label, name='download_account_label'),
    #url(r'^download-account-file/', account_membership.download_account_file, name='download_account_file'),

   ]
