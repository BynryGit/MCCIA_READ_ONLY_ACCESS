
# System Packages
import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import *
from django.http import HttpResponse
charset = 'utf-8'
from django.contrib.auth.decorators import login_required
from authenticationapp.decorator import role_required

# User Model
from membershipapp.models import RenewLetterSchedule


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Update Renew Mail Letter', 'Upload Renew Schedule'], login_url='/backofficeapp/login/', raise_exception=True)
def renewal_config_landing(request):
    print '\nRequest IN | renewal_landing.py | renewal_config_landing | User = ', request.user
    print '\nResponse OUT | renewal_landing.py | renewal_config_landing | User = ', request.user
    return render(request, 'backoffice/membership/renewal_config_landing.html')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Update Renew Mail Letter'], login_url='/backofficeapp/login/', raise_exception=True)
def update_renew_mail_letter_landing(request):
    print '\nRequest IN | renewal_landing.py | update_renew_mail_letter_landing | User = ', request.user
    get_renew_letter_details(request)
    print '\nResponse OUT | renewal_landing.py | update_renew_mail_letter_landing | User = ', request.user
    return render(request, 'backoffice/membership/renew_mail_letter_landing.html')



@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Update Renew Mail Letter', 'Upload Renew Schedule'], login_url='/backofficeapp/login/', raise_exception=True)
def upload_renew_schedule_landing(request):
    print '\nRequest IN | renewal_landing.py | upload_renew_schedule_landing | User = ', request.user
    print '\nResponse OUT | renewal_landing.py | upload_renew_schedule_landing | User = ', request.user
    return render(request, 'backoffice/membership/upload_renew_schedule_landing.html')

@csrf_exempt
def upload_schedule_file(request):
    data = {}
    try:
        print '\nRequest IN | renewal_landing.py | upload_schedule_file | User = ', request.user


        if RenewLetterSchedule.objects.filter(row_type=1):
            print "___________________________if____________"
            a = RenewLetterSchedule.objects.filter(row_type=1)
            for i in a:
                i.is_deleted=True
                i.save()
            scheduleobject = RenewLetterSchedule(
                renew_schedule=request.FILES['schedule_file'],
                row_type=1,
            )
            scheduleobject.save()
        else:
            print "___________________________else____________"
            scheduleobject = RenewLetterSchedule(
                renew_schedule=request.FILES['schedule_file'],
                row_type =1,
            )
            scheduleobject.save()
        data = {'success': 'true'}
        print 'Response out|renewal_landing|upload_schedule_file|User %s Data'
    except Exception as exc:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|renewal_landing|upload_schedule_file|User %s Excepton ', exc
        data = {'message': 'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')



def get_schedule_datatable(request):
    data ={}
    try:
        print '\nRequest IN | renewal_landing | get_schedule_datatable | user %s', request.user
        dataList = []

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        renewalscheduleobj = RenewLetterSchedule.objects.filter(row_type=1).order_by('is_deleted')

        i = 1
        for renewschedule in renewalscheduleobj:
            tempList = []
            if renewschedule.is_deleted is False:
                status = '<label class="label label-success">Active</label>'
            else:
                status = '<label class="label label-default">Inactive</label>'

            schedule_file = str(renewschedule.renew_schedule).split('/')

            tempList.append(i)
            tempList.append (schedule_file)
            tempList.append('<a class="fa fa-eye" href="/sitemedia/' + str(renewschedule.renew_schedule) + '"target="_blank"></a>')
            tempList.append(status)
            dataList.append(tempList)
            i = i + 1

        if length == -1:
            sliced_list = dataList[:]
        else:
            sliced_list = dataList[start:length]
        total_records = len(dataList)
        total_record = total_records
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': sliced_list}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|renewal_landing | get_schedule_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_renew_letter_text(request):
    data = {}
    try:
        print '\nRequest IN | renewal_landing.py | save_renew_letter_text | User = ', request.user

        renewlettertext = RenewLetterSchedule(
            renew_letter=request.POST.get('renew_letter_detail'),
            row_type=0,
              )
        renewlettertext.save()

        data = {'success': 'true'}
        print 'Response out|renewal_landing|save_renew_letter_text|User %s Data'
    except Exception as exc:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|renewal_landing|save_renew_letter_text|User %s Excepton ', exc
        data = {'message': 'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_renew_letter_details(request):
    data = {}
    try:
        print '\nRequest IN | renewal_landing.py | get_renew_letter_details | User = ', request.user
        renew_object = RenewLetterSchedule.objects.filter(row_type=0).last()
        renew_object_text = renew_object.renew_letter
        data = {
            'success': 'true',
            'renew_object_text': renew_object_text
        }
    except Exception, e:
        print '\nRequest IN | renewal_landing.py | get_renew_letter_details | User = ', request.user
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Update Renew Mail Letter', 'Upload Renew Schedule'], login_url='/backofficeapp/login/', raise_exception=True)
def upload_membership_schedule_landing(request):
    print '\nRequest IN | renewal_landing.py | upload_membership_schedule_landing | User = ', request.user
    print '\nResponse OUT | renewal_landing.py | upload_membership_schedule_landing | User = ', request.user
    return render(request, 'backoffice/membership/upload_membership_schedule_landing.html')



@csrf_exempt
def upload_membership_schedule_file(request):
    data = {}
    try:
        print '\nRequest IN | renewal_landing.py | upload_membership_schedule_file | User = ', request.user
        if RenewLetterSchedule.objects.filter(row_type=3):
            membership_scheduleobject = RenewLetterSchedule.objects.filter(row_type=3)
            for j in membership_scheduleobject:
                j.is_deleted=True
                j.save()
            membershipscheduleobject = RenewLetterSchedule(
                renew_membership_schedule=request.FILES["membership_schedule_file"],
                row_type=3,
            )
            membershipscheduleobject.save()
        else:
            membershipscheduleobject = RenewLetterSchedule(
                renew_membership_schedule=request.FILES["membership_schedule_file"],
                row_type=3,
            )
            membershipscheduleobject.save()
        data = {'success': 'true'}
        print 'Response out|renewal_landing|upload_membership_schedule_file|User %s Data'
    except Exception as exc:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|renewal_landing|upload_membership_schedule_file|User %s Excepton ', exc
        data = {'message': 'Server Error'}
    return HttpResponse(json.dumps(data), content_type='application/json')



def get_membership_schedule_datatable(request):
    data ={}
    try:
        print '\nRequest IN | renewal_landing | get_membership_schedule_datatable | user %s', request.user
        dataList = []

        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        renewalmembershipscheduleobj = RenewLetterSchedule.objects.filter(row_type=3).order_by('is_deleted')

        i = 1
        for renewmembershipschedule in renewalmembershipscheduleobj:
            tempList = []
            if renewmembershipschedule.is_deleted is False:
                status = '<label class="label label-success">Active</label>'
            else:
                status = '<label class="label label-default">Inactive</label>'

            schedule_file = str(renewmembershipschedule.renew_membership_schedule).split('/')

            tempList.append(i)
            tempList.append (schedule_file)
            tempList.append('<a class="fa fa-eye" href="/sitemedia/' + str(renewmembershipschedule.renew_membership_schedule) + '"target="_blank"></a>')
            tempList.append(status)
            dataList.append(tempList)
            i = i + 1

        if length == -1:
            sliced_list = dataList[:]
        else:
            sliced_list = dataList[start:length]
        total_records = len(dataList)
        total_record = total_records
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': sliced_list}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|renewal_landing | get_membership_schedule_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')

