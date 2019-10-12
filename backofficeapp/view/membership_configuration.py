
# System Packages
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from django.db import transaction
import json
from django.http import HttpResponse

# User Models
from adminapp.models import  NameSign
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


def membership_configuration_landing (request):
    return render(request, 'backoffice/membership/membership_configuration_landing.html')



def Membership_certificate_Configuration (request):
    dg_obj = NameSign.objects.get(is_deleted=False, designation=1)
    president_obj = NameSign.objects.get(is_deleted=False, designation=0)
    data = {
        'dg_obj': dg_obj,
        'president_obj': president_obj,
    }
    return render(request, 'backoffice/membership/membership_certificate_Configuration.html', data)


@transaction.atomic
@csrf_exempt
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership certificate configuration'],login_url='/backofficeapp/login/',raise_exception=True)
def save_sign_name(request):
    data={}
    try:
        print '\nRequest IN | membership_configuration.py | save_sign_name | User = ', request.user
        nameSingob=NameSign(
            name=request.POST.get('name'),
            sign=request.FILES['sign_file'],
            designation=int(request.POST.get('type'))
            )
        nameSingob.save()

        data = {'success': 'true'}
        print 'Response out|membership_configuration|save_sign_name|User %s Data'
    except Exception as exc:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|membership_configuration|save_sign_name|User %s Excepton ', exc
        data = {'message': 'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')



@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership certificate configuration'],login_url='/backofficeapp/login/',raise_exception=True)
def current_dg_president_name(request):
    data={}
    try:
        print '\nRequest IN | membership_configuration.py | current_dg_president_name | User = ', request.user
        dg_obj = NameSign.objects.get(is_deleted= False, designation=1)
        president_obj = NameSign.objects.get(is_deleted=False, designation=0)

        data= {
            'dg_obj' : dg_obj,
            'president_obj' : president_obj,
        }

        print 'Response out|membership_configuration|current_dg_president_name|User %s Data'
    except Exception as exc:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|membership_configuration|current_dg_president_name|User %s Excepton ', exc
        data = {'message': 'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')