import smtplib
import json
charset = 'utf-8'
from django.db import transaction
from captcha_form import CaptchaForm
from backofficeapp.models import SystemUserProfile,UserPrivilege
from membershipapp.models import MembershipUser
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string, get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash



def backoffice_forgot_password(request):
    try:
        gmail_user = "membership@mcciapune.com"
        gmail_pwd = "mem@2011ship"
        TO = []
        template_name = "other/forgotpassword.html"
        user_obj = ''
        try:
            user_obj = SystemUserProfile.objects.get(username=request.POST.get('uname'))
        except Exception,e:
            pass

        kwargs = {
            "uidb64": urlsafe_base64_encode(force_bytes(user_obj.id)).decode(),
            "token": default_token_generator.make_token(user_obj)
        }
        activation_url = "/authenticate/activate-backoffice-user-account/"+kwargs['uidb64']+"/"+kwargs['token']+"/"
        activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)

        context = {
            'activate_url': activate_url
        }
        html_content = render_to_string(template_name, context)

        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html_content, 'html', _charset=charset)
        msg.attach(htmlfile)
        TO.append(user_obj.email)
        try:
            server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            subject_line = 'Attention Required - Reset Password Link'
            msg['subject'] = str(subject_line)
            msg['from'] = 'mailto: <membership@mcciapune.com>'
            msg['to'] = ",".join(TO)
            toaddrs = TO
            server.sendmail(msg['from'], toaddrs, msg.as_string())
            server.quit()
            print '\nMail Sent'
            data = {'success': 'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception, e:
            pass
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception,e:
        pass
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


def activate_backoffice_user_account(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist,e:
        print e
        user = None
    if user and default_token_generator.check_token(user, token):
        data={'uidb64':uidb64,'token':token}
        return render(request, 'other/reset_backoffice_password.html', data)
    else:
        return HttpResponse("Link is expired.")


@csrf_exempt
def save_new_backoffice_password(request):
    uidb64=request.POST.get('uidb64')
    token=request.POST.get('token')
    pwd=request.POST.get('password')
    re_enter_pass = request.POST.get('reenter_password')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print user
    except User.DoesNotExist,e:
        print e
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.set_password(pwd)
        user.save()
        username=user.username
        try:
            user_obj = SystemUserProfile.objects.get(username=username)
            try:
                user1 = authenticate(username=username, password=pwd)
                if user1:
                    if user1.is_active:
                        privilege_obj = UserPrivilege.objects.filter(userrole=user_obj.role)
                        privilege_list = []
                        for privilege in privilege_obj:
                            if not privilege.module_name in privilege_list:
                                if privilege.module_name:
                                    privilege_list.append(str(privilege.module_name))

                            privilege_list.append(str(privilege.privilege))
                        request.session['privileges'] = privilege_list
                        try:
                            request.session['login_user'] = user_obj.username
                            request.session['first_name'] = user_obj.name
                            request.session['user_type'] = 'backoffice'
                            login(request, user1)
                            # if 'Dashboard' in request.session['privileges']:
                            #     redirect_url = '/backoffice/'
                            if 'Membership' in request.session['privileges']:
                                redirect_url = '/backofficeapp/backoffice/'
                            elif 'Hall Booking' in request.session['privileges']:
                                redirect_url = '/backofficeapp/hall_booking/'
                            elif 'Event' in request.session['privileges']:
                                redirect_url = '/backofficeapp/events/'
                            elif 'Visa' in request.session['privileges']:
                                redirect_url = '/visarecommendationapp/visa-backoffice-landing/'
                            elif 'Administrator' in request.session['privileges']:
                                redirect_url = '/backofficeapp/administrator/'
                            elif 'Publication' in request.session['privileges']:
                                redirect_url = '/publicationapp/publication-landing/'
                            else:
                                redirect_url = '/backofficeapp/login/'

                        except Exception as e:
                            print e

                        data = {'success': 'true', 'redirect_url': redirect_url}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        data = {'success': 'false', 'message': 'User Is Not Active'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    data = {'success': 'Invalid Password', 'message': 'Invalid Password'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            except Exception, e:
                print e
                data = {'success': 'false', 'message': 'Invalid Username'}
                return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception, e:
            print "-----------except-----", e
            data = {'success': 'false', 'message': 'Invalid Username'}
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("Password Reset link has expired")


@transaction.atomic
@csrf_exempt
def change_backoffice_password(request):
    data={}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | backoffice_password | change_backoffice_password | user = ', request.user                
        user_obj = request.user        
        if user_obj.check_password(str(request.POST.get('current_pass')).strip()):
	        user_obj.set_password(str(request.POST.get('new_pass')).strip())
	        user_obj.save()
	        update_session_auth_hash(request, request.user)
	    	data['success'] = 'true'
	    	print 'password match and session is updated'
        else:
        	data['success'] = 'wrong_password'
        	print 'password does not match'
		transaction.savepoint_commit(sid)
    except Exception, e:                
        data['success'] = 'false'
        print '\nException | backoffice_password | change_backoffice_password | user Exception = ',e
        transaction.rollback(sid)
    print '\nResponse OUT | backoffice_password | change_backoffice_password | user = ',request.user
    return HttpResponse(json.dumps(data), content_type='application/json')

#     @csrf_exempt
# def change_password(request):
# 	details=request.POST
# 	userObj=request.user
# 	if userObj.check_password(request.POST.get('current_pswd')):
# 		userObj.set_password(request.POST.get('new_pswd'))
# 		userObj.save()
# 		update_session_auth_hash(request, request.user)
# 		data = {"success": "true"}
# 		return HttpResponse(json.dumps(data), content_type='application/json')
# 	else
# 		data1={"success":"false"}
# 		return HttpResponse(json.dumps(data1), content_type='application/json')