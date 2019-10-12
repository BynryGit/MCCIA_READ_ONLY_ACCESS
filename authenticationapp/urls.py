from django.conf.urls import include, url
from authenticationapp import views
from authenticationapp.view import check_pwd,backoffice_password


urlpatterns = [
url(r'^sign_in/', views.sign_in,name='login'),
url(r'^backoffice-forgot-password/', backoffice_password.backoffice_forgot_password,name='backoffice_forgot_password'),
url(r'^member-sign_in/', views.member_sign_in,name='member_login'),
url(r'^log-out/', views.signing_out,name='signing_out'),
url(r'^mem-log-out/', views.mem_signing_out,name='mem_signing_out'),
url(r'^save-new-password/', check_pwd.save_new_password,name='save_new_password'),
url(r'^save-new-backoffice-password/', backoffice_password.save_new_backoffice_password,name='save_new_backoffice_password'),
url(r'^send-mail/', check_pwd.send_account_activation_email,name='send_account_activation_email'),
url(r'^change-password/', check_pwd.change_password,name='change_password'),
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',check_pwd.activate_user_account, name='activate_user_account'),
url(r'^activate-backoffice-user-account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',backoffice_password.activate_backoffice_user_account, name='activate_backoffice_user_account'),
url(r'^change-backoffice-password/', backoffice_password.change_backoffice_password,name='change-backoffice_password'),

]