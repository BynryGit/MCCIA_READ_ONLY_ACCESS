from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from backofficeapp.models import SystemUserProfile,UserPrivilege
from membershipapp.models import MembershipUser
import MySQLdb, sys
from django.contrib.auth import login
from django.http import HttpResponse
charset = 'utf-8'
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def sign_in(request):
    data = {}
    try:
        print "--------------------------"
        if request.POST:
            # form = CaptchaForm(request.POST)
            print 'logs: login request with: ', request.POST
            username = request.POST['username']
            password = request.POST['password']
            try:
                user_obj = SystemUserProfile.objects.get(username=username)
                try:
                    user = authenticate(username=username, password=password)
                    if user:
                        if user.is_active:
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
                                login(request, user)
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

                            data = {'success' : 'true','redirect_url':redirect_url}
                            return HttpResponse(json.dumps(data), content_type='application/json')
                        else:
                            data= { 'success':'false', 'message':'User Is Not Active'}
                            return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        data= { 'success' : 'Invalid Password', 'message' :'Invalid Password'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except Exception,e:
                    print e
                    data= { 'success' : 'false', 'message' :'Invalid Username'}
                    return HttpResponse(json.dumps(data), content_type='application/json')

            except SystemUserProfile.DoesNotExist,e:
                data= { 'success':'false', 'message':'Invalid Username'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            except Exception,e:
                print "-----------except-----",e
                data= { 'success':'false', 'message':'Invalid Username'}
                return HttpResponse(json.dumps(data), content_type='application/json')

    except MySQLdb.OperationalError, e:
        print e
        data= {'success' : 'false', 'message':'Internal server'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'Exception ', e
        data= { 'success' : 'false', 'message':'Invalid Username or Password'}
    return HttpResponse(json.dumps(data), content_type='application/json')


from django.template import RequestContext


def signing_out(request):
    logout(request)
    return render_to_response('backoffice/authentication/login.html', dict(
        message_logout='You have successfully logged out.'
    ), context_instance=RequestContext(request))


@csrf_exempt
def member_sign_in(request):
    data = {}
    try:
        print "--------------------------"
        if request.POST:
            # form = CaptchaForm(request.POST)
            # print 'logs: login request with: ', request.POST
            username = request.POST['username'].strip()
            password = request.POST['password']
            try:
                user_obj = MembershipUser.objects.get(username=username)
                # user_obj = MembershipUser.objects.get(username='IA-8020')
                # request.session['login_user'] = user_obj.username
                # request.session['renewal_year'] = str(int(str(user_obj.userdetail.membership_year)[0:4]) + 1) + '-' + str(int(str(user_obj.userdetail.membership_year)[5:9]) + 1)
                # request.session['member_type'] = str(user_obj.userdetail.user_type)
                # request.session['user_type'] = 'frontend'
                # user_obj.backend = 'django.contrib.auth.backends.ModelBackend'
                # login(request, user_obj)
                # data = {'success': 'true'}
                # return HttpResponse(json.dumps(data), content_type='application/json')
                try:
                    user = authenticate(username=username, password=password)
                    if user:
                        if user.is_active and not user_obj.is_deleted:
                            try:
                                request.session['login_user'] = user_obj.username
                                request.session['renewal_year'] = str(int(str(user_obj.userdetail.membership_year)[0:4])+1)+'-'+str(int(str(user_obj.userdetail.membership_year)[5:9])+1)
                                request.session['member_type'] = str(user_obj.userdetail.user_type)
                                request.session['user_type'] = 'frontend'
                                login(request, user)
                            except Exception as e:
                                print e
                            data = {'success': 'true'}
                            return HttpResponse(json.dumps(data), content_type='application/json')
                        else:
                            data = {'success': 'Invalid User', 'message': 'User Is Not Active'}
                            return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        data = {'success': 'Invalid Password', 'message': 'Invalid Password'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except Exception, e:
                    print e
                    data = {'success': 'false', 'message': 'Invalid Username'}
                    return HttpResponse(json.dumps(data), content_type='application/json')

            except MembershipUser.DoesNotExist, e:
                data = {'success': 'Not Found', 'message': 'Invalid Username'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            except Exception, e:
                print "-----------except-----", e
                data = {'success': 'false', 'message': 'Invalid Username'}
                return HttpResponse(json.dumps(data), content_type='application/json')

    except MySQLdb.OperationalError, e:
        print e
        data = {'success': 'false', 'message': 'Internal server'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false', 'message': 'Invalid Username or Password'}
    return HttpResponse(json.dumps(data), content_type='application/json')


from django.shortcuts import redirect


def mem_signing_out(request):
    logout(request)
    return redirect('/')