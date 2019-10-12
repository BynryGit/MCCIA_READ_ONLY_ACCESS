import pdb

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import traceback
from django.http import HttpResponse, HttpResponseForbidden
import json
from adminapp.models import Committee, Servicetax
from eventsapp.models import EventDetails, EventRegistration, EventParticipantUser, EventType, EventSpecialAnnouncement, \
    EventParticipantReportTable, EventSponsorImage, PromoCode
from membershipapp.models import UserDetail, NonMemberDetail, CompanyDetail, MembershipInvoice
from hallbookingapp.models import HallDetail
from massmailingapp.models import EmailDetail
import datetime
import dateutil
from dateutil import tz
from django.db.models import Count, Sum, Q, F

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def events_home(request):
    try:
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')
        event_type_list = EventType.objects.filter(is_deleted=False).order_by('event_type')
        event_announcement_list = EventSpecialAnnouncement.objects.filter(end_date__gte=today, status=True,
                                                                          is_deleted=False)
        data = {
            'success': 'true',
            'committee_list': committee_list,
            'event_type_list': event_type_list,
            'event_announcement_list': event_announcement_list
        }
    except Exception as e:
        print 'Exception | event_landing | events_home | user %s. Exception = ', str(traceback.print_exc())
        data = {'success': 'false'}

    return render(request, 'events/events.html', data)


'''Code for calender showing events on given date '''


def get_event_data(request):
    try:
        print 'Request IN | event_landing | get_event_data | user'
        final_list = []
        committee = request.GET.get('committee')
        eventtype = request.GET.get('eventtype')

        from_zone = tz.tzutc()
        to_zone = tz.gettz('Asia/Kolkata')

        event_detail_objs_list = EventDetails.objects.filter(view_status=1, event_status=0, is_deleted=False).order_by(
            'event_title')
        if committee:
            event_detail_objs_list = event_detail_objs_list.filter(organising_committee=committee)
        if eventtype:
            event_detail_objs_list = event_detail_objs_list.filter(event_type=eventtype)

        for obj in event_detail_objs_list:
            # For reflecting release date impact on visibility of event
            release_date = obj.release_date.strftime('%d %B %Y - %H:%M')
            release_date = datetime.datetime.strptime(release_date, '%d %B %Y - %H:%M')
            today_date = datetime.datetime.now()

            if release_date <= today_date:
                obj.view_status = 1
                obj.save()

            to_date = obj.to_date.strftime('%d %B %Y - %H:%M')
            to_date = datetime.datetime.strptime(to_date, '%d %B %Y - %H:%M')

            if to_date <= today_date:
                obj.view_status = 0
                obj.event_status = 1
                obj.save()

            start_date = str(obj.from_date.strftime('%d %B %Y %I:%M %p'))
            end_date = str(obj.to_date.strftime('%d %B %Y %I:%M %p'))

            new_date = start_date + ' -  <br>' + end_date
            if obj.from_date.strftime("%d %M %Y") == obj.to_date.strftime("%d %M %Y"):
                new_date = str(obj.from_date.strftime('%d %B %Y %I:%M %p')) + ' - ' + str(
                    obj.to_date.strftime('%I:%M %p'))

            if obj.event_mode == 0:
                textColor = '#02a078'
            elif obj.event_mode == 1:
                textColor = '#ff6679'
            elif obj.event_mode == 2:
                textColor = '#4a90e2'

            event_dic = {
                'start': start_date,
                'end': end_date,
                'title': obj.event_title,
                'url': '/eventsapp/events-details/?event_detail_id=' + str(obj.id),
                'color': '#eae4e4',
                'textColor': textColor,
                'new_date': new_date,
                'allDay': 'false'
                # 'data': {}
            }
            final_list.append(event_dic)
        data = {
            'success': 'true',
            'final_list': final_list
        }
        print 'Request OUT | event_landing | get_event_data | user', request.user
    except Exception as e:
        print 'Exception | event_landing | get_event_data | user %s. Exception = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


'''Code for details of a event when user click on a particular event'''


def events_details(request):
    try:
        print 'Request IN | event_landing | events_details | user'  # ,is_new=False

        not_approved_member = [invoice_item.userdetail.id for invoice_item in MembershipInvoice.objects.filter(is_paid=True, is_deleted=False,
                                                                userdetail__member_associate_no__isnull=True)]
        new_not_approved_member = UserDetail.objects.filter(id__in=not_approved_member)

        member_list = UserDetail.objects.filter(member_associate_no__isnull=False,membership_type="MM",
                                                is_deleted=False).order_by('company__company_name')
        user_company_objs_list = member_list | new_not_approved_member

        # user_company_objs_list = UserDetail.objects.filter(is_deleted=False, member_associate_no__isnull=False,
        #                                                    valid_invalid_member=True).order_by('company__company_name')
        non_member_company_list = NonMemberDetail.objects.filter(is_deleted=False, is_active=True)
        event_detail_id = request.GET.get('event_detail_id')
        event_deatail_obj = EventDetails.objects.get(id=event_detail_id)

        if not request.user.is_anonymous():
            if request.session['user_type'] == 'backoffice':
                pass
        elif event_deatail_obj.event_status == 1:
            return HttpResponseForbidden()

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        registration_start_date = event_deatail_obj.registration_start_date.strftime('%Y-%m-%d')
        registration_end_date = event_deatail_obj.registration_end_date.strftime('%Y-%m-%d')

        status = ''
        status_flag = 0
        if registration_start_date > today:
            status = 'Registration will start on ' + event_deatail_obj.registration_start_date.strftime('%B %d, %Y')
        elif registration_end_date < today:
            status = 'Event registration is closed'
        elif registration_start_date <= today:
            status_flag = 1
            status = 'Event registration has started'

        when_to_attend = event_deatail_obj.from_date.strftime(
            '%B %d, %Y') + ' To ' + event_deatail_obj.to_date.strftime('%B %d, %Y')
        time_to_attend = event_deatail_obj.from_date.strftime('%I:%M:%p') + ' To ' + event_deatail_obj.to_date.strftime(
            '%I:%M:%p')

        hall_location_flag = 0
        if event_deatail_obj.hall_details:
            hall_location_flag = 1
            hall_location = event_deatail_obj.hall_details.hall_name + '-' + event_deatail_obj.hall_details.hall_location.location
        else:
            hall_location = event_deatail_obj.other_location_address

        contact_person_name2 = ''
        contact_person_number2 = ''
        contact_person_email_id2 = ''
        designation_name2 = ''
        if event_deatail_obj.contact_person2:
            contact_person_name2 = event_deatail_obj.contact_person2.first_name + ' ' + event_deatail_obj.contact_person2.last_name
            contact_person_number2 = event_deatail_obj.contact_person2.contact_no
            contact_person_email_id2 = event_deatail_obj.contact_person2.email
            designation_name2 = event_deatail_obj.contact_person2.designation.designation_name

        sponsorImage_obj_list = EventSponsorImage.objects.filter(event_id=event_deatail_obj.id, is_deleted=False)
        sponsor_image_doc_list = []
        for obj in sponsorImage_obj_list:
            docs_address = 'http://' + get_current_site(request).domain + obj.document_files.url
            sponsor_image_doc_list.append(docs_address)

        event_mode = event_deatail_obj.get_event_mode_display()

        early_bird_date = ''
        if event_deatail_obj.is_early_bird:
            early_bird_date = event_deatail_obj.early_bird_date.strftime(
                '%B %d, %Y') + ' - ' + event_deatail_obj.early_bird_date.strftime('%H:%M:%p')

        data = {
            'id': event_deatail_obj.id,
            'event_title': event_deatail_obj.event_title,
            'status': status,
            'status_flag': status_flag,
            'organised_by': event_deatail_obj.organised_by,
            'when_to_attend': when_to_attend,
            'time_to_attend': time_to_attend,
            'event_location': hall_location,
            'hall_location_flag': hall_location_flag,
            'event_objective' : event_deatail_obj.event_objective,
            # 'to_whom_description': event_deatail_obj.to_whom_description,
            'member_charges': event_deatail_obj.member_charges,
            'non_member_charges': event_deatail_obj.non_member_charges,
            'organising_committee': event_deatail_obj.organising_committee.committee,
            'contact_person_name': event_deatail_obj.contact_person1.first_name + ' ' + event_deatail_obj.contact_person1.last_name,
            'contact_person_number': event_deatail_obj.contact_person1.contact_no,
            'contact_person_email_id': event_deatail_obj.contact_person1.email,
            'designation_name': event_deatail_obj.contact_person1.designation.designation_name,
            'contact_person_name2': contact_person_name2,
            'contact_person_number2': contact_person_number2,
            'contact_person_email_id2': contact_person_email_id2,
            'designation_name2': designation_name2,
            'user_company_objs_list': user_company_objs_list,
            'non_member_company_list': non_member_company_list,
            'sponsor_image_doc_list': sponsor_image_doc_list,
            'event_mode': event_mode,

            'other_charges_name': event_deatail_obj.other_charges_name,
            'other_charges_amount': event_deatail_obj.other_charges_amount,

            'is_early_bird': event_deatail_obj.is_early_bird,
            'early_member_charges': event_deatail_obj.early_member_charges,
            'early_non_member_charges': event_deatail_obj.early_non_member_charges,
            'early_bird_date': early_bird_date,
        }
        print 'Request OUT | event_landing | events_details | user %s', request.user
    except Exception as e:
        print 'Exception | event_landing | events_details | user %s. Exception = ', str(traceback.print_exc())
        data = {}

    if event_mode == 'Open To All':
        return render(request, 'events/events-details-open2all.html', data)
    elif event_mode == 'On Payment':
        return render(request, 'events/events-details.html', data)
    else:
        return render(request, 'events/events-details-invitation.html', data)

'''For locationg map on event registration page'''


def get_hall_location(request):
    locations = []
    try:
        event_obj = EventDetails.objects.get(id=request.GET.get('event_id'))
        hall_obj = HallDetail.objects.get(id=event_obj.hall_details.id)

        try:
            location = {'lat': hall_obj.latitude,
                        'lon': hall_obj.longitude,
                        'zoom': 8,
                        'title': hall_obj.hall_name,
                        'html': '<h5>' + hall_obj.hall_name + '</h5>',
                        'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
                        }
            locations.append(location)
        except Exception, e:
            pass

        data = {
            'success': 'true',
            'locations': locations
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_edit_hall_location(request):
    locations = []
    try:
        event_reg_obj = EventRegistration.objects.get(id=request.GET.get('event_reg_id'))
        event_obj = EventDetails.objects.get(id=event_reg_obj.event.id)
        hall_obj = HallDetail.objects.get(id=event_obj.hall_details.id)

        try:
            location = {'lat': hall_obj.latitude,
                        'lon': hall_obj.longitude,
                        'zoom': 8,
                        'title': hall_obj.hall_name,
                        'html': '<h5>' + hall_obj.hall_name + '</h5>',
                        'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
                        }
            locations.append(location)
        except Exception, e:
            pass

        data = {
            'success': 'true',
            'locations': locations
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_events_details(request):
    try:
        print 'Request IN | event_landing | edit_events_details | user'
        user_company_objs_list = UserDetail.objects.filter(is_deleted=False,
                                                           member_associate_no__isnull=False).order_by(
            'company__company_name')
        event_reg_id = request.GET.get('event_reg_id')

        event_reg_obj = EventRegistration.objects.get(id=event_reg_id)

        when_to_attend = event_reg_obj.event.from_date.strftime(
            '%B %d, %Y') + ' To ' + event_reg_obj.event.to_date.strftime('%B %d, %Y')
        time_to_attend = event_reg_obj.event.from_date.strftime(
            '%H:%M:%p') + ' To ' + event_reg_obj.event.to_date.strftime('%H:%M:%p')

        contact_person_name2 = ''
        contact_person_number2 = ''
        contact_person_email_id2 = ''
        if event_reg_obj.event.contact_person2:
            contact_person_name2 = event_reg_obj.event.contact_person2.first_name + ' ' + event_reg_obj.event.contact_person2.last_name
            contact_person_number2 = event_reg_obj.event.contact_person2.contact_no
            contact_person_email_id2 = event_reg_obj.event.contact_person2.email

        data = {
            'id': event_reg_obj.id,
            'no_of_participant': event_reg_obj.no_of_participant,
            'event_title': event_reg_obj.event.event_title,
            'organised_by': event_reg_obj.event.organised_by,
            'when_to_attend': when_to_attend,
            'time_to_attend': time_to_attend,
            'event_location': event_reg_obj.event.hall_details.hall_location.location,
            'to_whom_description': event_reg_obj.event.to_whom_description,
            'member_charges': event_reg_obj.event.member_charges,
            'non_member_charges': event_reg_obj.event.non_member_charges,
            'organising_committee': event_reg_obj.event.organising_committee.committee,
            'contact_person_name': event_reg_obj.event.contact_person1.first_name + ' ' + event_reg_obj.event.contact_person1.last_name,
            'contact_person_number': event_reg_obj.event.contact_person1.contact_no,
            'contact_person_email_id': event_reg_obj.event.contact_person1.email,
            'user_company_objs_list': user_company_objs_list,
            'is_member': event_reg_obj.is_member,
            'address': event_reg_obj.address,
            'contact_person_name': event_reg_obj.contact_person_name,
            'contact_person_email_id': event_reg_obj.contact_person_email_id,
            'contact_person_number': event_reg_obj.contact_person_number,

            'contact_person_name2': contact_person_name2,
            'contact_person_number2': contact_person_number2,
            'contact_person_email_id2': contact_person_email_id2,

            'office_contact': event_reg_obj.office_contact,
            'name_of_organisation': event_reg_obj.name_of_organisation
        }
        print 'Request OUT | event_landing | edit_events_details | user %s', request.user
    except Exception as e:
        print 'Exception | event_landing | edit_events_details | user %s. Exception = ', str(traceback.print_exc())
        data = {}
    return render(request, 'events/edit-events-details.html', data)


def get_participant_details(request):
    try:
        participant_list = []
        participant_obj_list = EventParticipantUser.objects.filter(event_user_id=request.GET.get('eventreg_id'))
        for obj in participant_obj_list:
            participant_list.append(
                {'id': obj.id, 'event_user_name': obj.event_user_name, 'designation': obj.designation,
                 'contact_no': obj.contact_no, 'email_id': obj.email_id})
        data = {
            'success': 'true',
            'participant_list': participant_list,
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_non_member_detail(request):
    data = {}
    try:
        print '\nRequest IN | event_landing | get_non_member_detail | user = ', request.user
        non_member_obj = NonMemberDetail.objects.get(id=request.GET.get('non_mem_id'))
        
        data = {'success': 'true', 'address': str(non_member_obj.address),
                'non_mem_id': non_member_obj.id,'mail_id':non_member_obj.email,

                }
        print '\nResponse OUT | event_landing | get_non_member_detail | user = ', request.user, request.GET.get(
            'mem_id')
    except Exception:
        data = {'success': 'false'}
        print '\nException IN | event_landing | get_non_member_detail | EXP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


'''Save event registration request from website and send ackowledge mail respectiviely'''

@csrf_exempt
@transaction.atomic
def save_event_details(request):
    sid = transaction.savepoint()
    try:

        print 'Request IN | event_landing | save_event_details | user'

        if request.POST.get('CorrespondenceGSTText'):
            CorrespondenceGSTText = request.POST.get('CorrespondenceGSTText')
        else:
            CorrespondenceGSTText = 'NA'

        is_member = False
        is_other = False
        non_member_obj = ''
        if request.POST.get('member_type') == 'non_member':
            non_member_id = request.POST.get('non_member_id')

            if non_member_id:
                non_member_obj = NonMemberDetail.objects.get(id=non_member_id)
                non_member_obj.address = request.POST.get('address').encode("utf8", "ignore")
                non_member_obj.gst = CorrespondenceGSTText
                non_member_obj.enroll_type = request.POST.get('enroll_type')
                non_member_obj.email = request.POST.get('contact_person_email_id')
                non_member_obj.created_date = datetime.datetime.now()
                non_member_obj.save()
            else:
                if request.POST.get('enroll_type') == 'IN':
                    company_name_str = request.POST.get('Organizationname')
                    company_obj = CompanyDetail(
                        company_name=company_name_str,
                    )
                    company_obj.save()

                    non_member_obj = NonMemberDetail(
                    company=company_obj,
                    address=request.POST.get('address').encode("utf8", "ignore"),
                    gst=CorrespondenceGSTText,
                    enroll_type =request.POST.get('enroll_type'),
                    email=request.POST.get('contact_person_email_id'),
                    )
                    non_member_obj.save()
                else:
                    company_name_str = request.POST.get('Organizationnamecomp')
                    company_obj = CompanyDetail(
                        company_name=company_name_str,
                    )
                    company_obj.save()

                    non_member_obj = NonMemberDetail(
                        company=company_obj,
                        address=request.POST.get('address').encode("utf8", "ignore"),
                        gst=CorrespondenceGSTText,
                        enroll_type=request.POST.get('enroll_type'),
                        email=request.POST.get('contact_person_email_id'),
                    )
                    non_member_obj.save()

            name_of_organisation = non_member_obj.company.company_name
            is_member = False

        elif request.POST.get('member_type') == 'member':
            if request.POST.get('enroll_type')=='IN':
                user_company_obj = UserDetail.objects.get(id=request.POST.get('selectOrganizationname'))
                name_of_organisation = user_company_obj.company.company_name
                is_member = True
            else:
                user_company_obj = UserDetail.objects.get(id=request.POST.get('selectOrganizationnamecomp'))
                name_of_organisation = user_company_obj.company.company_name
                is_member = True
        elif request.POST.get('member_type') == 'other':
            non_member_id = request.POST.get('non_member_id')
            if non_member_id:
                non_member_obj = NonMemberDetail.objects.get(id=non_member_id)
                non_member_obj.address = request.POST.get('address').encode("utf8", "ignore")
                non_member_obj.gst = CorrespondenceGSTText
                non_member_obj.enroll_type = request.POST.get('enroll_type')
                non_member_obj.email = request.POST.get('contact_person_email_id')
                non_member_obj.save()
            else:
                if request.POST.get('enroll_type') == 'IN':
                    company_obj = CompanyDetail(
                        company_name=request.POST.get('Organizationname'),
                    )
                else:
                    company_obj = CompanyDetail(
                        company_name=request.POST.get('Organizationnamecomp'),
                    )
                company_obj.save()

                non_member_obj = NonMemberDetail(
                    company=company_obj,
                    address=request.POST.get('address').encode("utf8", "ignore"),
                    gst=CorrespondenceGSTText,
                    enroll_type=request.POST.get('enroll_type'),
                    email=request.POST.get('contact_person_email_id'),
                )
                non_member_obj.save()

            name_of_organisation = non_member_obj.company.company_name
            is_member = False
            is_other = True
            # non_member_obj = NonMemberDetail.objects.get(id=request.POST.get('Organizationname'))
            # name_of_organisation = non_member_obj.company.company_name            

        # if (request.POST.get('UnderProcess') == "UnderProcess"):
        #     gst_option = "UP"
        # elif (request.POST.get('CorrespondenceGSTText') == "Applicable"):
        #     gst_option = "AP"
        # elif (request.POST.get('correspondence_GST') == "NotApplicable"):
        #     gst_option = "NA"
        if request.POST.get('member_type') == 'member':
            if request.POST.get('enroll_type')=='IN':
                user_company = UserDetail.objects.get(id=request.POST.get('selectOrganizationname'))
            else:
                user_company = UserDetail.objects.get(id=request.POST.get('selectOrganizationnamecomp'))
            membership_no = user_company.member_associate_no
            if membership_no:
                membership_no = user_company.member_associate_no
            else:
                membership_no = 'IA-TMP'
        else:
            membership_no = 'Non Member'

        if (request.POST.get('correspondence_GST') == "on"):
            gst_option = "NA"
        elif (request.POST.get('UnderProcess') == "on"):
            gst_option = "UP"
        else:
            gst_option = "AP"

        if request.POST.get('CorrespondencePanCheck') == "on":
            panNo = "NA"
        else:
            panNo = request.POST.get('CorrespondencePan')

        try:
            event_reg_no_obj = EventRegistration.objects.filter().last()
            reg_no = int(event_reg_no_obj.reg_no[3:]) + 1
            reg_no = str(reg_no).zfill(6)
            reg_no = 'EBK' + str(reg_no)
        except Exception as e:
            print e
            reg_no = 'EBK000001'
            pass

        event_reg_obj = EventRegistration(
            event=EventDetails.objects.get(id=request.POST.get('hidden_eventdetails_id')),
            reg_no=reg_no,
            name_of_organisation=name_of_organisation,
            enroll_type=request.POST.get('enroll_type'),
            address=request.POST.get('address'),
            contact_person_name=request.POST.get('ContactPerson'),
            contact_person_number=request.POST.get('contact_person_number'),
            contact_person_number_two=request.POST.get('contact_person_number2'),
            office_contact=request.POST.get('contact_office_number'),
            contact_person_email_id=request.POST.get('contact_person_email_id'),
            no_of_participant=request.POST.get('industry_participant'),
            total_amount=request.POST.get('hidden_payable_amount'),
            total_fees_amount=request.POST.get('hidden_total_fees'),
            extra_gst_amount=request.POST.get('hidden_total_gst'),
            total_discount_amount=request.POST.get('hidden_discount_part'),
            payment_mode=request.POST.get('radiobtn-2') if request.POST.get('radiobtn-2') else 'Offline',
            user_details=UserDetail.objects.get(id=request.POST.get('selectOrganizationname')) if request.POST.get(
                'selectOrganizationname') else UserDetail.objects.get(id=request.POST.get('selectOrganizationnamecomp')) if request.POST.get('selectOrganizationnamecomp') else None,
            nonmemberdetail=non_member_obj if non_member_obj else None,
            gst=CorrespondenceGSTText,
            gst_in=gst_option,
            pan=panNo,
            is_member=is_member,
            is_other=is_other,
            medium_source=request.POST.get('medium'),
            social_medium_source=request.POST.get('social_medium'),
            is_active=False,
            is_deleted=True
        )
        event_reg_obj.save()

        # saving contact person data to "EventParticipantReportTable" . This activity is for reporting or getting data of participant user (Memeber or Non Member)

        if request.POST.get('member_type') == 'non_member':
            old_mail_list = non_member_obj.extra_email.split(',') if non_member_obj.extra_email else []

        industry_participant = request.POST.get('industry_participant')
        for obj in range(int(industry_participant)):
            event_participant_obj = EventParticipantUser(
                event_user=EventRegistration.objects.get(id=event_reg_obj.id),
                # enroll_type=request.POST.get('enroll_type'),
                event_user_name=request.POST.get('firstname_' + str(obj)),
                designation=request.POST.get('Designation_' + str(obj)),
                department=request.POST.get('Department' + str(obj)),
                contact_no=request.POST.get('ContactNumber_' + str(obj)),
                email_id=request.POST.get('email_' + str(obj))
            )
            event_participant_obj.save()

            if request.POST.get('member_type') == 'non_member':
                if not event_participant_obj.email_id in old_mail_list:
                    if non_member_obj.extra_email != None:
                        non_member_obj.extra_email = str(non_member_obj.extra_email) + ',' + str(
                            event_participant_obj.email_id)
                    else:
                        non_member_obj.extra_email = str(event_participant_obj.email_id)

                    non_member_obj.save()

            participantreportevent_obj = EventParticipantReportTable(
                event_registration=EventRegistration.objects.get(id=event_reg_obj.id),
                reg_no=reg_no,
                address=request.POST.get('address'),
                contact_person_name=request.POST.get('firstname_' + str(obj)),
                designation=request.POST.get('Designation_' + str(obj)),
                department=request.POST.get('Department' + str(obj)),
                contact_person_number=request.POST.get('ContactNumber_' + str(obj)),
                # contact_person_number_two=request.POST.get('contact_person_number2'),
                contact_person_email_id=request.POST.get('email_' + str(obj)),
                is_member=is_member,
            )
            participantreportevent_obj.save()

        transaction.savepoint_commit(sid)

        event_participant_obj_list = EventParticipantUser.objects.filter(event_user_id=event_reg_obj.id)
        event_part_list = []
        for obj in event_participant_obj_list:
            event_part_list.append(
                {'event_user_name': obj.event_user_name, 'designation': obj.designation, 'contact_no': obj.contact_no,
                 'email_id': obj.email_id,'department':obj.department})

        data = {'success': 'true', 'event_reg_id': event_reg_obj.id, 'reg_no': reg_no,'membership_no_val':membership_no,
                'event_part_list': event_part_list}
        print 'Request OUT | event_landing | save_event_details | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, exc:
        data = {'success': 'false'}
        print 'exception', str(traceback.print_exc())
        # transaction.rollback(sid)
        print 'Exception | event_landing | save_event_details | user %s. Exception = ', str(traceback.print_exc())

    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def confirm_event_registration(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | event_landing | confirm_event_registration | user'

        mail = request.GET.get('confirm_mail')

        event_reg_obj = EventRegistration.objects.get(id=request.GET.get('event_reg_id'))
        event_reg_obj.is_active = True
        event_reg_obj.is_deleted = False
        event_reg_obj.save()

        # Start - Code for saving Email id's for Massmailing
        new_email_list = [obj.email_id for obj in EventParticipantUser.objects.filter(event_user=event_reg_obj)]

        if event_reg_obj.user_details:
            # Start - Adding new email in UserDetail Table
            member_obj = UserDetail.objects.get(id=event_reg_obj.user_details.id)
            event_email_list = member_obj.event_email.split(',') if member_obj.event_email else []
            email_to_add_list = (list(set(new_email_list) - set(event_email_list)))

            for new_email in email_to_add_list:
                member_obj.event_email = str(member_obj.event_email) + ',' + str(new_email)
                member_obj.save()
            # End - Adding new email in UserDetail Table

            # Start - Adding new email in EmailDetail Table
            try:
                event_participant_list = EventParticipantUser.objects.filter(event_user=event_reg_obj)
                for event_par in event_participant_list:
                    try:
                        old_email_obj = EmailDetail.objects.get(userdetail=member_obj, email=event_par.email_id)
                        old_email_obj.name = event_par.event_user_name
                        old_email_obj.designation = event_par.designation
                        old_email_obj.cellno = event_par.contact_no
                        old_email_obj.hash_tag = old_email_obj.hash_tag + ',' + str(
                            event_par.event_user.event.organising_committee.committee) if old_email_obj.hash_tag else str(
                            event_par.event_user.event.organising_committee.committee)
                        old_email_obj.save()

                        old_hash_tag_list = old_email_obj.hash_tag.split(',')
                        old_hash_tag_list = set(old_hash_tag_list)
                        str1 = ','.join(old_hash_tag_list)
                        old_email_obj.hash_tag = str1
                        old_email_obj.save()
                    except Exception as e:
                        print e
                        EmailDetail(
                            userdetail=member_obj,
                            name=event_par.event_user_name,
                            email=event_par.email_id,
                            designation=event_par.designation,
                            cellno=event_par.contact_no,
                            hash_tag=str(event_par.event_user.event.organising_committee.committee),
                            is_member=True,
                        ).save()
                        pass

            except Exception as  e:
                print e
        # End - Adding new email in EmailDetail Table

        elif event_reg_obj.nonmemberdetail:
            non_member_obj = NonMemberDetail.objects.get(id=event_reg_obj.nonmemberdetail.id)
            # Start - Adding new email in EmailDetail Table
            try:
                event_participant_list = EventParticipantUser.objects.filter(event_user=event_reg_obj)
                for event_par in event_participant_list:
                    try:
                        old_email_obj = EmailDetail.objects.get(nonmemberdetail=non_member_obj,
                                                                email=event_par.email_id)
                        old_email_obj.name = event_par.event_user_name
                        old_email_obj.designation = event_par.designation
                        old_email_obj.cellno = event_par.contact_no
                        old_email_obj.hash_tag = old_email_obj.hash_tag + ',' + str(
                            event_par.event_user.event.organising_committee.committee) if old_email_obj.hash_tag else str(
                            event_par.event_user.event.organising_committee.committee)
                        old_email_obj.save()

                        old_hash_tag_list = old_email_obj.hash_tag.split(',')
                        old_hash_tag_list = set(old_hash_tag_list)
                        str1 = ','.join(old_hash_tag_list)
                        old_email_obj.hash_tag = str1
                        old_email_obj.save()
                    except Exception as e:
                        print e
                        EmailDetail(
                            nonmemberdetail=non_member_obj,
                            name=event_par.event_user_name,
                            email=event_par.email_id,
                            designation=event_par.designation,
                            cellno=event_par.contact_no,
                            hash_tag=str(event_par.event_user.event.organising_committee.committee),
                            is_member=False,
                        ).save()
                        pass

            except Exception as  e:
                print e
        # End - Adding new email in EmailDetail Table

        # End - Code for saving Email id's for Massmailing
        transaction.savepoint_commit(sid)
        if request.GET.get('confirm_mail') == 'Yes':
            send_event_reg_ack_mail(event_reg_obj)
        else:
            pass
        data = {'success': 'true'}
        print 'Request OUT | event_landing | confirm_event_registration | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | event_landing | confirm_event_registration | user %s. Exception = ', str(
            traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def save_edit_event(request):
    sid = transaction.savepoint()
    try:
        print 'Request IN | event_landing | save_edit_event | user'

        if request.POST.get('member_type') == 'non_member':
            name_of_organisation = request.POST.get('Organizationname')
            is_member = False
        elif request.POST.get('member_type') == 'member':
            user_company_obj = UserDetail.objects.get(id=request.POST.get('selectOrganizationname'))
            name_of_organisation = user_company_obj.company.company_name
            is_member = True

        event_reg_obj = EventRegistration.objects.get(id=request.POST.get('hidden_eventreg_id'))
        if event_reg_obj.is_member:
            user_company_obj = UserDetail.objects.get(id=request.POST.get('selectOrganizationname'))
            name_of_organisation = user_company_obj.company.company_name
        else:
            name_of_organisation = request.POST.get('Organizationname')

        event_reg_obj.name_of_organisation = name_of_organisation
        event_reg_obj.address = request.POST.get('address')
        event_reg_obj.contact_person_name = request.POST.get('ContactPerson')
        event_reg_obj.contact_person_email_id = request.POST.get('contact_person_email_id')
        event_reg_obj.contact_person_number = request.POST.get('contact_person_number')
        event_reg_obj.office_contact = request.POST.get('contact_office_number')

        event_reg_obj.user_details = UserDetail.objects.get(
            id=request.POST.get('selectOrganizationname')) if request.POST.get('selectOrganizationname') else None

        event_reg_obj.save()

        industry_participant = request.POST.get('hidden_industry_participant')
        for obj in range(int(industry_participant)):
            event_participant_obj = EventParticipantUser.objects.get(
                id=request.POST.get('hidden_participant_' + str(obj)))
            event_participant_obj.event_user_name = request.POST.get('firstname_' + str(obj))
            event_participant_obj.designation = request.POST.get('Designation_' + str(obj))
            event_participant_obj.department = request.POST.get('Department' + str(obj))
            event_participant_obj.contact_no = request.POST.get('ContactNumber_' + str(obj))
            event_participant_obj.email_id = request.POST.get('email_' + str(obj))
            event_participant_obj.save()

        transaction.savepoint_commit(sid)

        data = {'success': 'true'}
        print 'Request OUT | event_landing | save_edit_event | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | event_landing | save_edit_event | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


'''This function is to calculate total payable amount by applying all discount like early bird, group discount, member/ non member discount'''


def get_total_event_amount(request):
    print 'Request IN | event_landing | get_total_event_amount | user'
    try:
        eventdetails_id = request.GET.get('eventdetails_id')
        print '**************',eventdetails_id
        event_details_obj = EventDetails.objects.get(id=eventdetails_id)

        if request.GET.get('state_id') == 'maha':
            gstObj = Servicetax.objects.get(tax_type=0, is_active=True)
        else:
            gstObj = Servicetax.objects.get(tax_type=1, is_active=True)

        member_charges = 0
        add_gst = 0

        utc_timezone = tz.tzutc()
        member_charges = float(event_details_obj.member_charges)
        non_member_charges = float(event_details_obj.non_member_charges)

        if event_details_obj.is_early_bird:
            today_date = datetime.datetime.now().replace(tzinfo=utc_timezone)
            if event_details_obj.early_bird_date > today_date:
                member_charges = float(event_details_obj.early_member_charges)
                non_member_charges = float(event_details_obj.early_non_member_charges)

        if request.GET.get('industry_participant_count'):
            if request.GET.get('member_type') == 'non_member':
                member_charges = non_member_charges * float(request.GET.get('industry_participant_count'))
            elif request.GET.get('member_type') == 'other':
                member_charges = float(event_details_obj.other_charges_amount) * float(
                    request.GET.get('industry_participant_count'))
            else:
                membership_obj = UserDetail.objects.get(id=request.GET.get('organization_id'))
                if membership_obj.valid_invalid_member:
                    member_charges = member_charges * float(request.GET.get('industry_participant_count'))
                else:
                    member_charges = non_member_charges * float(request.GET.get('industry_participant_count'))

        # add_gst = (float(gstObj.tax)/100)*member_charges
        # add_gst= round(float(add_gst),2)

        industry_participant_count = request.GET.get('industry_participant_count')
        total_discount = 0
        total_percent_discount = 0
        if request.GET.get('member_type') != 'other':
            if event_details_obj.discount_1:
                discount_part1 = event_details_obj.discount_1.split('-')[0]
                discount_percent1 = event_details_obj.discount_1.split('-')[1]
                if int(industry_participant_count) >= int(discount_part1):
                    total_percent_discount = discount_percent1
                    total_discount = (float(discount_percent1) / 100) * member_charges
                    total_discount = round(float(total_discount), 2)

            if event_details_obj.discount_2:
                discount_part2 = event_details_obj.discount_2.split('-')[0]
                discount_percent2 = event_details_obj.discount_2.split('-')[1]
                if int(industry_participant_count) >= int(discount_part2):
                    total_percent_discount = discount_percent2
                    total_discount = (float(discount_percent2) / 100) * member_charges
                    total_discount = round(float(total_discount), 2)

            if event_details_obj.discount_3:
                discount_part3 = event_details_obj.discount_3.split('-')[0]
                discount_percent3 = event_details_obj.discount_3.split('-')[1]
                if int(industry_participant_count) >= int(discount_part3):
                    total_percent_discount = discount_percent3
                    total_discount = (float(discount_percent3) / 100) * member_charges
                    total_discount = round(float(total_discount), 2)

        # payable_amount = float(member_charges) + float(add_gst)
        total_payable_amount = float(member_charges) - float(total_discount)

        if request.GET.get('industry_participant_count'):
            add_gst = (float(gstObj.tax) / 100) * total_payable_amount
            add_gst = round(float(add_gst), 2)

        total_payable_amount = float(total_payable_amount) + float(add_gst)

        total_percent_discount = str(total_percent_discount) + '%'
        data = {
            'success': 'true',
            'total_fees': member_charges,
            'add_gst': add_gst,
            'total_discount': total_discount,
            'total_percent_discount': total_percent_discount,
            'total_payable_amount': total_payable_amount
        }
        print 'Request OUT | event_landing | get_total_event_amount | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        data = {'success': 'false'}
        print 'Exception | event_landing | get_total_event_amount | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


'''If user avail for promocode then following function is used'''


def get_promocode_applied_amount(request):
    print 'Request IN | event_landing | get_promocode_applied_amount | user'
    try:
        promocode = request.GET.get('promocode')
        eventdetails_id = request.GET.get('eventdetails_id')
        event_details_obj = EventDetails.objects.get(id=eventdetails_id)

        if request.GET.get('state_id') == 'maha':
            gstObj = Servicetax.objects.get(tax_type=0, is_active=True)
        else:
            gstObj = Servicetax.objects.get(tax_type=1, is_active=True)

        member_charges = 0
        add_gst = 0
        promocode_flag = 0

        member_charges = float(event_details_obj.other_charges_amount) * float(
            request.GET.get('industry_participant_count'))
        if request.GET.get('member_type') == 'other':
            try:
                promocode_obj = PromoCode.objects.get(event_details=event_details_obj, promo_code=promocode,
                                                      status=True, is_deleted=False)

                if promocode_obj.percent_discount:
                    total_discount = (float(promocode_obj.percent_discount) / 100) * member_charges
                    total_discount = round(float(total_discount), 2)
                    total_payable_amount = float(member_charges) - float(total_discount)
                else:
                    total_payable_amount = float(member_charges) - float(promocode_obj.discounted_amount)

                member_charges = total_payable_amount

            except Exception as e:
                promocode_flag = 1
                print e

            if request.GET.get('industry_participant_count'):
                add_gst = (float(gstObj.tax) / 100) * member_charges
                add_gst = round(float(add_gst), 2)

            total_payable_amount = float(member_charges) + float(add_gst)

            total_discount = 0
            total_percent_discount = 0

            total_percent_discount = str(total_percent_discount) + '%'
            data = {
                'success': 'true',
                'total_fees': member_charges,
                'add_gst': add_gst,
                'total_discount': total_discount,
                'total_payable_amount': total_payable_amount,
                'promocode_flag': promocode_flag
            }
            print 'Request OUT | event_landing | get_promocode_applied_amount | user %s', request.user
            return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        data = {'success': 'false'}
        print 'Exception | event_landing | get_promocode_applied_amount | user %s. Exception = ', str(
            traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_membership_no(request):
    print 'Request IN | event_landing | get_membership_no | user'
    try:
        membership_obj = UserDetail.objects.get(id=request.GET.get('organization_id'))
        if membership_obj.pan == 'NA':
            pan = ''
        elif membership_obj.pan:
            pan = membership_obj.pan
        else:
            pan = ''

        if membership_obj.gst == 'NA':
            gst = ''
        elif membership_obj.gst:
            gst = membership_obj.gst
        else:
            gst = ''

        data = {
            'success': 'true',
            'member_associate_no':membership_obj.member_associate_no if membership_obj.member_associate_no else 'IA-TMP',
            'correspond_address': membership_obj.correspond_address,
            'contact_person':membership_obj.poc_name,
            'email_id' : membership_obj.correspond_email,
            'mobile_no': membership_obj.correspond_cellno,
            'pan_no':pan,
            'gst_no':gst,
        }
        print 'Request OUT | event_landing | get_membership_no | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')

    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        data = {'success': 'false'}
        print 'Exception | event_landing | get_membership_no | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def upcoming_event_list(request):
    try:
        print 'Request IN | event_landing | upcoming_event_list | user'

        committee_list = Committee.objects.filter(is_deleted=False).order_by('committee')

        data = {
            'success': 'true',
            'committee_list': committee_list
        }

    except Exception as e:
        print 'Exception | event_landing | upcoming_event_list | user %s. Exception = ', str(traceback.print_exc())
        data = {'success': 'false', 'final_list': final_list}

    return render(request, 'events/upcoming-event-list.html', data)


@csrf_exempt
def upcoming_event_datatable(request):
    try:
        print 'event_landing | upcoming_event_datatable | user'
        dataList = []

        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['from_date', '', '', 'organising_committee__committee']
        column_name = order + list[int(column)]
        start = request.GET.get('start')
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        today = datetime.datetime.today().strftime('%Y-%m-%d')

        if request.GET.get('committee'):
            event_detail_objs_list = EventDetails.objects.filter(event_status=0, from_date__gte=today,
                                                                 organising_committee=request.GET.get('committee'),
                                                                 is_deleted=False)  # .order_by(column_name)[start:length]
        else:
            event_detail_objs_list = EventDetails.objects.filter(event_status=0, from_date__gte=today,
                                                                 is_deleted=False)  # .order_by(column_name)[start:length]

        total_record = event_detail_objs_list.count()
        event_detail_objs_list = event_detail_objs_list.order_by(column_name)[start:length]

        for obj in event_detail_objs_list:
            tempList = []

            when_to_attend = obj.from_date.strftime('%B %d, %Y') + ' - ' + obj.to_date.strftime('%B %d, %Y')
            if obj.from_date.strftime('%B %d, %Y') == obj.to_date.strftime('%B %d, %Y'):
                when_to_attend = obj.from_date.strftime('%B %d, %Y')

            time_to_attend = obj.from_date.strftime('%I:%M:%p') + ' - ' + obj.to_date.strftime('%I:%M:%p')

            action = '<a class="registerNow" title="Register Now" href="/eventsapp/events-details/?event_detail_id=' + str(
                obj.id) + '">REGISTER NOW</a>'

            tempList.append(when_to_attend)
            tempList.append(time_to_attend)
            tempList.append(obj.event_title)
            tempList.append(obj.organising_committee.committee)
            tempList.append(obj.get_event_mode_display())
            tempList.append(action)

            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception | event_landing | upcoming_event_datatable | user %s. Exception = ', str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def past_event_datatable(request):
    try:
        print 'event_landing | past_event_datatable | user'
        dataList = []

        total_record = 0
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        list = ['from_date', '', '', 'organising_committee__committee']
        column_name = order + list[int(column)]
        start = request.GET.get('start')
        length = int(request.GET.get('length')) + int(request.GET.get('start'))

        today = datetime.datetime.today().strftime('%Y-%m-%d')

        if request.GET.get('committee'):
            event_detail_objs_list = EventDetails.objects.filter(from_date__lte=today,
                                                                 organising_committee=request.GET.get('committee'),
                                                                 is_deleted=False)
        else:
            event_detail_objs_list = EventDetails.objects.filter(from_date__lte=today, is_deleted=False)

        total_record = event_detail_objs_list.count()
        event_detail_objs_list = event_detail_objs_list.order_by(column_name)[start:length]

        for obj in event_detail_objs_list:
            tempList = []

            when_to_attend = obj.from_date.strftime('%B %d, %Y') + ' - ' + obj.to_date.strftime('%B %d, %Y')
            if obj.from_date.strftime('%B %d, %Y') == obj.to_date.strftime('%B %d, %Y'):
                when_to_attend = obj.from_date.strftime('%B %d, %Y')

            time_to_attend = obj.from_date.strftime('%I:%M:%p') + ' - ' + obj.to_date.strftime('%I:%M:%p')

            action = '<a class="registerNow" title="Details" href="/eventsapp/past-event-details/?event_detail_id=' + str(
                obj.id) + '">DETAILS</a>'

            tempList.append(when_to_attend)
            tempList.append(time_to_attend)
            tempList.append(obj.event_title)
            tempList.append(obj.organising_committee.committee)
            tempList.append(action)

            dataList.append(tempList)
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
    except Exception as e:
        print 'Exception | event_landing | past_event_datatable | user %s. Exception = ', str(traceback.print_exc())
        data = {'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'aaData': []}
    return HttpResponse(json.dumps(data), content_type='application/json')


def past_event_details(request):
    try:
        print 'Request IN | event_landing | past_event_details | user'

        event_detail_id = request.GET.get('event_detail_id')
        event_deatail_obj = EventDetails.objects.get(id=event_detail_id)

        when_to_attend = event_deatail_obj.from_date.strftime('%B %d, %Y') + ' - ' + event_deatail_obj.to_date.strftime(
            '%B %d, %Y')
        if event_deatail_obj.from_date.strftime('%B %d, %Y') == event_deatail_obj.to_date.strftime('%B %d, %Y'):
            when_to_attend = event_deatail_obj.from_date.strftime('%B %d, %Y')

        time_to_attend = event_deatail_obj.from_date.strftime(
            '%H:%M:%p') + ' To ' + event_deatail_obj.from_date.strftime('%H:%M:%p')

        if event_deatail_obj.hall_details:
            hall_location = event_deatail_obj.hall_details.hall_name + '-' + event_deatail_obj.hall_details.hall_location.location
        else:
            hall_location = event_deatail_obj.other_location_address

        data = {
            'event_location': hall_location,
            'when_to_attend': when_to_attend,
            'time_to_attend': time_to_attend,
            'organised_by': event_deatail_obj.organised_by,
            'contact_person_name': event_deatail_obj.contact_person1.first_name + ' ' + event_deatail_obj.contact_person1.last_name,
            'contact_person_number': event_deatail_obj.contact_person1.contact_no,
            'contact_person_email_id': event_deatail_obj.contact_person1.email,
        }

    except Exception as e:
        print 'Exception | event_landing | past_event_details | user %s. Exception = ', str(traceback.print_exc())
        data = {}

    return render(request, 'events/past-event-details.html', data)


from django.template import Context
from django.template.loader import render_to_string, get_template
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import os
from django.conf import settings
import smtplib

charset = 'utf-8'

'''sending acknowledge mail when user done with event registrations'''


def send_event_reg_ack_mail(event_reg_obj):
    try:
        when_to_attend = event_reg_obj.event.from_date.strftime(
            '%B %d, %Y') + ' To ' + event_reg_obj.event.to_date.strftime('%B %d, %Y')
        time_to_attend = event_reg_obj.event.from_date.strftime(
            '%I:%M %p') + ' To ' + event_reg_obj.event.to_date.strftime('%I:%M %p')
        reg_date = event_reg_obj.created_on.strftime('%B %d, %Y')
        payment_mode = event_reg_obj.get_payment_mode_display()
        event_reg_participant_list = EventParticipantUser.objects.filter(event_user=event_reg_obj)
        data = {'event_reg_obj': event_reg_obj, 'when_to_attend': when_to_attend, 'time_to_attend': time_to_attend,
                'reg_date': reg_date, 'payment_mode': payment_mode,
                'event_reg_participant_list': event_reg_participant_list}

        imgpath = os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        fp = open(imgpath, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<img1>')

        gmail_user = "eventreg@mcciapune.com"
        gmail_pwd = "event@2011reg"

        event_part_list = EventParticipantUser.objects.filter(event_user=event_reg_obj)
        mait_to_list = []
        for obj in event_part_list:
            mait_to_list.append(obj.email_id)

        # mait_to_list.append('priyanka.kachare@bynry.com')
        # mait_to_list.append('priyanshu.bhopte@bynry.com')
        TO = mait_to_list

        CC = []
        contact_person1_email = event_reg_obj.event.contact_person1.email
        CC.append(contact_person1_email)
        if event_reg_obj.event.contact_person2:
            contact_person2_email = event_reg_obj.event.contact_person2.email
            CC.append(contact_person2_email)
            CC.append('priyanka.kachare@bynry.com')
            CC.append('priyanshu.bhopte@bynry.com')


        html = get_template('events/event_acknowledgement.html').render(Context(data))
        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html, 'html', _charset=charset)
        msg.attach(htmlfile)
        msg.attach(msgImage)

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)

        subject_line = 'Event Acknowledgement' + ' - ' + event_reg_obj.event.event_title.encode("utf8", "ignore")
        msg['subject'] = str(subject_line)
        msg['from'] = 'mailto: <eventreg@mcciapune.com>'
        msg['to'] = ",".join(TO)
        msg['cc'] = ",".join(CC)
        toaddrs = TO + CC
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()
        print '\nMail Sent'
        return
    except Exception, e:
        print '\nMail NOT Sent', str(traceback.print_exc())
        return
