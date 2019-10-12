from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import traceback
from django.http import HttpResponse
import json
from eventsapp.models import EventSpecialAnnouncement
from django.db.models import Q
import datetime
@csrf_exempt
def event_announcement_landing(request):
    return render(request, 'backoffice/events/event_announcement_landing.html')

@csrf_exempt
def add_new_announcement(request):
    return render(request, 'backoffice/events/add_announcement.html')

@csrf_exempt
def save_announcement_details(request):
    print request.POST
    sid = transaction.savepoint()

    try:


        event_description = request.POST.get('category_descriptions')
        end_date = datetime.datetime.strptime(request.POST.get('end_date'), '%d/%m/%Y')
        print end_date
        if request.method == 'POST':
            eventObj = EventSpecialAnnouncement(
                announcement=event_description,
                end_date=end_date,
                status=True,
                is_deleted=False,
            )
            eventObj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | user | membership_details | user %s. Exception = ', request.user, e
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_event_detail(request):
    try:
        dataList = []
        meterReadings = []


        # Oredering and paging starts
        column = request.GET.get('order[0][column]')  # for ordering
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = 0
        list = ['id']
        column_name = order + list[int(column)]

        try:
            try:
                if request.GET.get('sort_var') == "Active":
                    eventObjs = EventSpecialAnnouncement.objects.filter(is_deleted=False,status=True)
                elif request.GET.get('sort_var') == "Inactive":
                    eventObjs = EventSpecialAnnouncement.objects.filter(is_deleted=False,status=False)
                else:
                    eventObjs = EventSpecialAnnouncement.objects.filter(is_deleted=False)
            except Exception, e:
                print e


            if searchTxt:
                eventObjs=eventObjs.filter(Q(announcement__icontains=searchTxt))

            total_record=eventObjs.count()
            eventObjs = eventObjs.order_by(column_name)[start:length]
            i=0
            a=1
            for eventObj in eventObjs:
                if not eventObj.end_date:
                    eventObj.end_date=datetime.datetime.now()
                    eventObj.save()
                i = start + a
                a = a + 1
                tempList = []
                if eventObj.status == True:
                    event_status = 'True'
                    status = '<label class="label label-success"> Active </label>'
                    action= '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_mem_cat(' + '"' + str(event_status) + '"' + ',' + str(eventObj.id) + ')></a>&nbsp; &nbsp;'
                else:
                    event_status = 'False'
                    status = '<label class="label label-default"> Inactive </label>'
                    action = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_announcement" onclick=update_mem_cat(' + '"' + str(
                        event_status) + '"' + ',' + str(eventObj.id) + ')></a>&nbsp; &nbsp;'

                edit_icon = '<a class="icon-pencil" onClick="editSlabDetailsModal(' + str(eventObj.id) + ')"></a> &nbsp; &nbsp;'

                tempList.append(str(i))
                tempList.append(eventObj.announcement)
                tempList.append(eventObj.end_date.strftime('%B %d,%Y'))
                tempList.append(status)
                tempList.append(edit_icon + action)
                dataList.append(tempList)

        except Exception, e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|slab_details | get_slab_details_datatable | User:{0} - Excepton:{1}'.format(
                request.user, e)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|slab_details | get_slab_details_datatable|User:{0} - Excepton:{1}'.format(
            request.user, e)
        data = {'msg': 'error'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def show_event_announcement_details(request):
    data={}
    evenet_id=request.GET.get('event_id')
    eventobj=EventSpecialAnnouncement.objects.get(id=evenet_id)
    end_date=eventobj.end_date.strftime('%d/%m/%Y')
    print end_date
    data={'abc':eventobj.announcement,'success':'true','end_date':end_date}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_event_announcement_details(request):

    sid = transaction.savepoint()

    try:
        print 'Request IN | slab_details | edit_slab_details | user %s', request.user

        if request.POST:
            print request.POST
            event_id = request.POST.get('event_id')
            end_date = datetime.datetime.strptime(request.POST.get('end_date'), '%d/%m/%Y').replace(hour=23, minute=59, second=59)
            category_descriptions = request.POST.get('category_descriptions')
            eventobj = EventSpecialAnnouncement.objects.get(id=event_id)
            eventobj.announcement = category_descriptions
            eventobj.end_date = end_date
            eventobj.save()
            transaction.savepoint_commit(sid)

            data = {'success': 'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'success': 'noPost'}
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, e:
        transaction.rollback(sid)
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@transaction.atomic
def update_event_announcement_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '...................',request.GET.get('event_announcement_id')
        eventobj = EventSpecialAnnouncement.objects.get(id=str(request.GET.get('event_announcement_id')))
        if eventobj.status is True:
            eventobj.status = False
        else:
            eventobj.status = True

        eventobj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception,e:
        print '\nException | update_event_announcement_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')

