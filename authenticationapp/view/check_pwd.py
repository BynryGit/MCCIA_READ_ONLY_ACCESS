from django.contrib.auth import login
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash


from django.contrib.auth.models import User
from django.template.loader import render_to_string, get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
charset = 'utf-8'
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from membershipapp.models import UserDetail


def send_account_activation_email(request):
    try:
        gmail_user = "membership@mcciapune.com"
        gmail_pwd = "mem@2011ship"
        TO = []
        CC = []
        to_list=[]


        # text_content = 'Reset password link'
        subject = 'Reset password link'
        template_name = "other/forgotpassword.html"
        # from_email = settings.DEFAULT_FROM_EMAIL
        # recipients = "shubham.pawar@bynry.com"
        # user = User.objects.all().last()
        user_obj = ''
        try:            
            user = User.objects.get(username=request.POST.get('membership_no'))            
            user_obj = UserDetail.objects.get(member_associate_no=request.POST.get('membership_no'))            
        except Exception,e:            
            pass

        kwargs = {
            "uidb64": urlsafe_base64_encode(force_bytes(user.id)).decode(),
            "token": default_token_generator.make_token(user)
        }
        print kwargs
        # activation_url = reverse("authenticateurl:activate_user_account", kwargs=kwargs)
        activation_url = "/authenticate/activate/"+kwargs['uidb64']+"/"+kwargs['token']+"/"

        activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)
        print activate_url

        context = {
            'activate_url': activate_url
        }
        # if user_obj.poc_email or user_obj.company.hoddetail.finance_email:
        #     to_list.append(str(user_obj.ceo_email))
        #     to_list.append(str(user_obj.poc_email))
        #     to_list.append(str(user_obj.company.hoddetail.finance_email))
        # else:
        #     to_list.append(str(user_obj.ceo_email))
        if user_obj.enroll_type == "CO":
            if user_obj.company.ceo_email_confirmation == True:
                if user_obj.poc_email and user_obj.company.hoddetail.finance_email:
                    to_list.append(str(user_obj.ceo_email))
                    to_list.append(str(user_obj.poc_email))
                    to_list.append(str(user_obj.company.hoddetail.finance_email))
                elif user_obj.poc_email:
                    to_list.append(str(user_obj.ceo_email))
                    to_list.append(str(user_obj.poc_email))
                elif user_obj.company.hoddetail.finance_email:
                    to_list.append(str(user_obj.ceo_email))
                    to_list.append(str(user_obj.company.hoddetail.finance_email))
                else:
                    to_list.append(str(user_obj.ceo_email))
            else:
                if user_obj.poc_email and user_obj.company.hoddetail.finance_email:
                    to_list.append(str(user_obj.poc_email))
                    to_list.append(str(user_obj.company.hoddetail.finance_email))
                elif user_obj.poc_email:
                    to_list.append(str(user_obj.poc_email))
                elif user_obj.company.hoddetail.finance_email:
                    to_list.append(str(user_obj.company.hoddetail.finance_email))
        else:
            to_list.append(str(user_obj.ceo_email))
            

        html_content = render_to_string(template_name, context)

        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html_content, 'html', _charset=charset)
        msg.attach(htmlfile)
        TO = to_list

        if user_obj.correspond_email:
            CC.append(str(user_obj.correspond_email).strip())
        try:
            server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)

            subject_line = 'Reset password link'
            msg['subject'] = str(subject_line)
            msg['from'] = 'mailto: <membership@mcciapune.com>'
            msg['to'] = ",".join(TO)
            msg['cc'] = ",".join(CC)
            toaddrs = TO + CC
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


def activate_user_account(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist,e:
        print e
        user = None
    if user and default_token_generator.check_token(user, token):
        data={'uidb64':uidb64,'token':token}
        # user.is_email_verified = True
        # user.is_active = True
        # user.save()
        # user.backend = 'django.contrib.auth.backends.ModelBackend'
        # login(request, user)
        # return redirect('/')
        return render(request, 'other/reset_password.html', data)
    else:
        return HttpResponse("Link is expired.")


@csrf_exempt
def save_new_password(request):
    print request.POST
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
        # data={'uidb64':uidb64,'token':token}
        user.is_email_verified = True
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.set_password(pwd)
        user.save()
        user_obj=user.membershipuser
        request.session['login_user'] = user_obj.username
        request.session['renewal_year'] = str(int(str(user_obj.userdetail.membership_year)[0:4]) + 1) + '-' + str(
            int(str(user_obj.userdetail.membership_year)[5:9]) + 1)
        request.session['member_type'] = str(user_obj.userdetail.user_type)
        request.session['user_type'] = 'frontend'
        login(request, user)
        data = {'success': 'true'}
        return HttpResponse(json.dumps(data), content_type='application/json')
        # return redirect('/')
    else:
        return HttpResponse("Activation link has expired")


def change_password(request):
    data={}
    try:
        print '\nRequest IN | check_pwd | change_password | user %s', request.user
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')
        userobj = request.user
        if userobj.check_password(str(request.POST.get('currentpassword'))):
            if newpassword == confirmpassword:
                try:
                    userobj.set_password(newpassword)
                    userobj.save()
                    update_session_auth_hash(request, request.user)
                except Exception as e:
                    print e
                data = {'success': 'true'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data = {'success': 'Passworddoesnotmatch'}
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'currentpasswordalert'}
            print '\nRequest OUT | check_pwd | change_password | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print e
        data = {'success': 'false'}
        print 'Exception | check_pwd | change_password | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')

# def send_account_activation_email(request):
#     try:
#
#         # imgpath = os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
#         # fp = open(imgpath, 'rb')
#         # msgImage = MIMEImage(fp.read())
#         # fp.close()
#         # msgImage.add_header('Content-ID', '<img1>')
#         template_name = "other/forgotpassword.html"
#
#
#         user = User.objects.all().last()
#         kwargs = {
#             "uidb64": urlsafe_base64_encode(force_bytes(user.id)).decode(),
#             "token": default_token_generator.make_token(user)
#         }
#         # print kwargs
#         # activation_url = reverse("authenticateurl:activate_user_account", kwargs=kwargs)
#
#         # activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)
#         activate_url="http://192.168.0.172:8090/authenticate/activate/"+kwargs['uidb64']+ '/'+ kwargs['token']+ '/'
#         print activate_url
#
#         context = {
#             'activate_url': activate_url
#         }
#         html_content = render_to_string(template_name, context)
#
#
#
#
#         mait_to_list = ['shubham.pawar@bynry.com']
#
#         TO = mait_to_list
#         CC = ['shubhampawar006@gmail.com']
#
#         # html = get_template('events/event_acknowledgement.html').render(Context(data))
#         msg = MIMEMultipart('related')
#         htmlfile = MIMEText(html_content, 'html', _charset=charset)
#         msg.attach(htmlfile)
#         # msg.attach(msgImage)
#
#         server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
#         server.ehlo()
#         server.starttls()
#         server.login(gmail_user, gmail_pwd)
#
#         subject_line = 'password'
#         msg['subject'] = str(subject_line)
#         msg['from'] = 'mailto: <eventreg@mcciapune.com>'
#         msg['to'] = ",".join(TO)
#         msg['cc'] = ",".join(CC)
#         toaddrs = TO + CC
#         server.sendmail(msg['from'], toaddrs, msg.as_string())
#         server.quit()
#         print '\nMail Sent'
#         return
#     except Exception, e:
#         print '\nMail NOT Sent', e
#         return




