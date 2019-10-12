
# System Module

import os, sys
import django
from django.db.models import Q, Sum
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()
from django.contrib.auth.decorators import login_required
from authenticationapp.decorator import role_required
from xlsxwriter import Workbook
from datetime import datetime
from hallbookingapp.models import HallBooking,HallBookingDetail,HallLocation,HallDetail, HallCheckAvailability, HallPaymentDetail, HallEquipment,BookingDetailHistory, Holiday, HallBookingDepositDetail, UserTrackDetail
import io
import traceback
from django.http import HttpResponse
from django.db import transaction

# User Models

from adminapp.models import *
from membershipapp.models import *
from eventsapp.models import EventDetails, EventRegistration, EventParticipantUser
from massmailingapp.models import CompanyDetail as MMCompanyDetail, PersonDetail, EmailDetail
from backofficeapp.models import SystemUserProfile
import datetime
from dateutil import tz
from xlrd import open_workbook, xldate_as_tuple

# Start:Use this for local system
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_dir = BASE_DIR + '/MCCIA_BACKOFFICE/Final_data'
to_zone = tz.gettz('Asia/Kolkata')


def check_data():
    try:
        file_path = ['/home/admin12/Test_project/Mass_Mailing/Total participant Report- 24.12.2018.xlsx']
        i = 0
        user_slab_list = []
        active_member = 0
        inactive_member = 0
        member_attendees_attended_count = 0
        total_member_count = 0
        total_non_member_count = 0
        member_no_email_count = 0
        member_attended_count = 0

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[1].nrows
            number_of_columns = wb.sheets()[1].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            company_name_list = []
            count_var_user = 0
            count_var_city = 0
            i = 1

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(12):
                    value = (wb.sheets()[1].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                try:
                    member_flag = False
                    if row_values[5].encode('utf-8').strip() == 'NM':
                        total_non_member_count = total_non_member_count + 1
                    else:
                        member_flag = True
                        total_member_count = total_member_count + 1
                        if row_values[7]:
                            # print '\nInput = ',row_values[7]
                            email_list = row_values[7].encode('utf-8').split(',')
                            for email_item in email_list:
                                user_obj_list = UserDetail.objects.filter(
                                    Q(ceo_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(person_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(correspond_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(company__hoddetail__hr_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(company__hoddetail__finance_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(company__hoddetail__marketing_email__icontains=email_item.encode(
                                        'utf-8').strip()) |
                                    Q(company__hoddetail__IT_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(company__hoddetail__corp_rel_email__icontains=email_item.encode(
                                        'utf-8').strip()) |
                                    Q(company__hoddetail__tech_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(company__hoddetail__rnd_email__icontains=email_item.encode('utf-8').strip()) |
                                    Q(company__hoddetail__exim_email__icontains=email_item.encode('utf-8').strip()))
                                print email_item, user_obj_list
                                if user_obj_list:
                                    member_attended_count = member_attended_count + 1
                                else:
                                    member_attendees_attended_count = member_attendees_attended_count + 1
                        else:
                            # print '\nNo Mail = ', row_values[7]
                            member_no_email_count = member_no_email_count + 1

                    # First tried code start

                    # mem_no = ''
                    # if row_values[5]:
                    #     temp_mem_no_list = row_values[5].split('-')
                    #     if len(temp_mem_no_list) > 1:
                    #         mem_no = temp_mem_no_list[0] + '-' + temp_mem_no_list[1]
                    #     else:
                    #         mem_no = temp_mem_no_list
                    #     # print 'mem_no = ',mem_no
                    # if row_values[5].encode('utf-8').strip() == 'NM':
                    #     non_member_count = non_member_count + 1
                    # else:
                    #     if row_values[5] == 'M':
                    #         mem_no = row_values[3].encode('utf-8').strip()
                    #         print '\nmem_no = ', mem_no
                    #         mem_obj = UserDetail.objects.filter(company__company_name__icontains=mem_no)
                    #         if mem_obj:
                    #             print mem_obj.count()
                    #     else:
                    #         mem_obj = UserDetail.objects.filter(member_associate_no=mem_no)
                    #     print row_values[5], mem_obj.count()
                    #     actual_member_count = actual_member_count + mem_obj.count()
                    #     member_count = member_count + 1
                    #
                    # if str(row_values[7]):
                    #     email_list = row_values[7].encode('utf-8').split(',')
                    #     if len(email_list) > 1:
                    #         for email_item in email_list:
                    #             user_obj_list = UserDetail.objects.filter(Q(ceo_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(person_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(correspond_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__hr_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__finance_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__marketing_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__IT_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__corp_rel_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__tech_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__rnd_email__icontains=email_item.encode('utf-8').strip()) |
                    #                                                       Q(company__hoddetail__exim_email__icontains=email_item.encode('utf-8').strip()))
                    #             if user_obj_list:
                    #                 for user_item in user_obj_list:
                    #                     if user_item.valid_invalid_member:
                    #                         active_member = active_member + 1
                    #                     else:
                    #                         inactive_member = inactive_member + 1
                    #             else:
                    #                 temp_user_obj_list = UserDetail.objects.filter(member_associate_no=row_values[5].encode('utf-8').strip())
                    #                 if temp_user_obj_list:
                    #                     attended_member = attended_member + 1
                    # else:
                    #     temp_user_obj_list_two = UserDetail.objects.filter(member_associate_no=row_values[5].encode('utf-8').strip())
                    #     if temp_user_obj_list_two:
                    #         attended_member = attended_member + 1

                    # First tried code end
                except Exception, e:
                    print e
                    # transaction.rollback(sid)

        # transaction.savepoint_commit(sid)
        print '\nDone'
        print '\nTotal Non Member Count = ', total_non_member_count
        print '\nTotal Member Count = ', total_member_count
        print '\nTotal Member attended Count = ', member_attended_count
        print "\nTotal Member's attendees attended Count = ", member_attendees_attended_count
        print "\nTotal Member's with NO MAIL ID Count = ", member_no_email_count
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        # transaction.rollback(sid)
    return


# For Mass Mailing
def update_event_no():
    try:
        for event_item in EventDetails.objects.all():
            print 'E' + str(event_item.from_date.strftime('%d%m%y')) + str(event_item.id)
            event_item.event_no = 'E' + str(event_item.from_date.strftime('%d%m%y')) + str(event_item.id)
            event_item.save()
            print event_item.event_no
        print '\nDone'
    except Exception, e:
        print e


@transaction.atomic
def save_data():
    sid = transaction.savepoint()
    try:
        # file_path = ['/home/admin12/Test_project/Mass_Mailing/Total participant Report- 24.12.2018.xlsx']
        # file_path = ['/home/admin12/Test_project/Mass_Mailing/Email list HR IR 21.12.2018.xlsx']
        file_path = [
            '/home/admin12/Test_project/Mass_Mailing/Attendance sheets  - April 18 Onwards for GST & Promotional Activity & CLS.xls']
        i = 0
        user_slab_list = []
        active_member = 0
        inactive_member = 0
        member_attendees_attended_count = 0
        total_member_count = 0
        total_non_member_count = 0
        member_no_email_count = 0
        member_attended_count = 0

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[1].nrows
            number_of_columns = wb.sheets()[1].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            company_name_list = []
            count_var_user = 0
            count_var_city = 0
            i = 1

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(13):
                    value = (wb.sheets()[1].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                try:
                    member_flag = False
                    person_obj = ''
                    # if row_values[7].encode('utf-8').strip():
                    print '\nEmail = ', row_values[7].encode('utf-8').strip()
                    temp_email_list = row_values[7].split(',')
                    # print temp_email_list, len(temp_email_list)
                    if temp_email_list and temp_email_list[0] != '':
                        if temp_email_list[0].strip() not in [person_item.email for person_item in
                                                              PersonDetail.objects.all()]:
                            new_person_detail_obj = PersonDetail(name=row_values[1].strip(),
                                                                 email=temp_email_list[0].strip(),
                                                                 designation=row_values[2].strip(),
                                                                 cellno=row_values[6].strip(),
                                                                 created_by='admin')
                            new_person_detail_obj.save()
                            if row_values[9]:
                                hash_tag_list = row_values[9].split(',')
                                hash_tag_list = ','.join(map(str, hash_tag_list))
                                new_person_detail_obj.hash_tag = hash_tag_list
                                new_person_detail_obj.save()
                            if len(temp_email_list) > 1:
                                extra_email_list = ','.join(map(str, temp_email_list[1:]))
                                new_person_detail_obj.extra_email = extra_email_list
                                new_person_detail_obj.save()
                            person_obj = new_person_detail_obj
                            print 'Added Person Object = ', person_obj
                        else:
                            try:
                                person_detail_obj = PersonDetail.objects.get(email=temp_email_list[0].strip())
                                person_obj = person_detail_obj
                                print 'GOT Person Object in DB = ', person_obj
                            except Exception, e:
                                print 'Person not found = '
                    else:
                        try:
                            new_person_detail_obj = PersonDetail(name=row_values[1].strip(),
                                                                 email=None,
                                                                 designation=row_values[2].strip(),
                                                                 cellno=row_values[6].strip(),
                                                                 created_by='admin')
                            new_person_detail_obj.save()
                            if row_values[9]:
                                hash_tag_list = row_values[9].split(',')
                                hash_tag_list = ','.join(map(str, hash_tag_list))
                                new_person_detail_obj.hash_tag = hash_tag_list
                                new_person_detail_obj.save()
                            person_obj = new_person_detail_obj
                            print 'Added Person Object with No Mail = ', person_obj
                        except Exception, e:
                            print row_values
                            print str(traceback.print_exc())

                    try:
                        company_obj = ''
                        if row_values[5].encode('utf-8').strip() == 'NM':
                            if row_values[3].encode('utf-8').strip() == 'Individual':
                                try:
                                    company_exist_obj = MMCompanyDetail.objects.get(company_name=row_values[1].strip())
                                    company_obj = company_exist_obj
                                except Exception, e:
                                    print 'Company Not Exists. Adding New IN Company.'
                                    new_mm_company_detail = MMCompanyDetail(company_name=row_values[1].strip(),
                                                                            gst=row_values[4].strip(),
                                                                            enroll_type='IN', created_by='admin')
                                    new_mm_company_detail.save()
                                    company_obj = new_mm_company_detail
                                    pass
                            else:
                                try:
                                    company_exist_obj = MMCompanyDetail.objects.get(company_name=row_values[3].strip())
                                    company_obj = company_exist_obj
                                except Exception, e:
                                    print 'Company Not Exists. Adding New CO Company.'
                                    new_mm_company_detail = MMCompanyDetail(company_name=row_values[3].strip(),
                                                                            gst=row_values[4].strip(),
                                                                            enroll_type='CO', created_by='admin')
                                    new_mm_company_detail.save()
                                    company_obj = new_mm_company_detail
                                    pass
                        else:
                            if row_values[5].encode('utf-8').strip() == 'M':
                                if row_values[3].encode('utf-8').strip() == 'Individual':
                                    try:
                                        company_exist_obj = MMCompanyDetail.objects.get(
                                            company_name=row_values[1].strip())
                                        company_obj = company_exist_obj
                                    except Exception, e:
                                        print 'Member Company Not Exists. Adding New IN Company.'
                                        new_mm_company_detail = MMCompanyDetail(company_name=row_values[1].strip(),
                                                                                gst=row_values[4].strip(),
                                                                                is_member=True,
                                                                                enroll_type='IN', created_by='admin')
                                        new_mm_company_detail.save()
                                        company_obj = new_mm_company_detail
                                        pass
                                else:
                                    try:
                                        company_exist_obj = MMCompanyDetail.objects.get(
                                            company_name=row_values[3].strip())
                                        company_obj = company_exist_obj
                                    except Exception, e:
                                        print 'Member Company Not Exists. Adding New CO Company.'
                                        new_mm_company_detail = MMCompanyDetail(company_name=row_values[3].strip(),
                                                                                gst=row_values[4].strip(),
                                                                                is_member=True,
                                                                                enroll_type='CO', created_by='admin')
                                        new_mm_company_detail.save()
                                        company_obj = new_mm_company_detail
                                        pass
                                try:
                                    userdetail_obj = UserDetail.objects.get(company__company_name=row_values[3].strip())
                                    company_obj.userdetail = userdetail_obj
                                    company_obj.save()
                                    for industry_item in userdetail_obj.company.industrydescription.all():
                                        company_obj.industrydescription.add(industry_item)
                                        company_obj.save()
                                except Exception, e:
                                    # print '\nFIRST M MANYTOMANY ERROR = ', str(traceback.print_exc())
                                    print 'FIRST M MANYTOMANY ERROR'
                                    pass

                            elif row_values[5].encode('utf-8').strip() == 'MCCIA':
                                try:
                                    company_exist_obj = MMCompanyDetail.objects.get(company_name=row_values[3].strip())
                                    company_obj = company_exist_obj
                                except Exception, e:
                                    print 'Company Not Exists. Adding New CO Company - MCCIA.'
                                    new_mm_company_detail = MMCompanyDetail(company_name=row_values[3].strip(),
                                                                            gst=row_values[4].strip(),
                                                                            is_member=False, is_mccia=True,
                                                                            enroll_type='CO', created_by='admin')
                                    new_mm_company_detail.save()
                                    company_obj = new_mm_company_detail
                                    person_obj.is_mccia_person = True
                                    person_obj.save()
                                    pass
                            else:
                                if row_values[3].encode('utf-8').strip() == 'Individual':
                                    try:
                                        company_exist_obj = MMCompanyDetail.objects.get(
                                            company_name=row_values[1].strip())
                                        company_obj = company_exist_obj
                                    except Exception, e:
                                        print 'Member Mem-No Company Not Exists. Adding New IN Company.'
                                        new_mm_company_detail = MMCompanyDetail(company_name=row_values[1].strip(),
                                                                                gst=row_values[4].strip(),
                                                                                is_member=True,
                                                                                enroll_type='IN', created_by='admin')
                                        new_mm_company_detail.save()
                                        company_obj = new_mm_company_detail
                                        pass
                                else:
                                    try:
                                        company_exist_obj = MMCompanyDetail.objects.get(
                                            company_name=row_values[3].strip())
                                        company_obj = company_exist_obj
                                    except Exception, e:
                                        print 'Member Mem-No Company Not Exists. Adding New CO Company.'
                                        new_mm_company_detail = MMCompanyDetail(company_name=row_values[3].strip(),
                                                                                gst=row_values[4].strip(),
                                                                                is_member=True,
                                                                                enroll_type='CO', created_by='admin')
                                        new_mm_company_detail.save()
                                        company_obj = new_mm_company_detail
                                        pass
                                try:
                                    userdetail_obj = UserDetail.objects.get(member_associate_no=row_values[5].strip())
                                    company_obj.userdetail = userdetail_obj
                                    company_obj.company_name = userdetail_obj.company.company_name.strip()
                                    company_obj.save()
                                    same_company_obj_count = MMCompanyDetail.objects.filter(
                                        userdetail=userdetail_obj).count()
                                    if same_company_obj_count > 1:
                                        # company_exists = company_obj if company_obj.userdetail in [company_item.userdetail for company_item in MMCompanyDetail.objects.all()] else None
                                        company_exists = MMCompanyDetail.objects.filter(
                                            userdetail=userdetail_obj).first()
                                        # if company_exists:
                                        company_obj.delete()
                                        company_obj = company_exists
                                    else:
                                        for industry_item in userdetail_obj.company.industrydescription.all():
                                            company_obj.industrydescription.add(industry_item)
                                            company_obj.save()
                                except Exception, e:
                                    # print '\nSECOND MEM-NO MANYTOMANY ERROR = ', str(traceback.print_exc())
                                    print 'SECOND MEM-NO MANYTOMANY ERROR '
                                    pass

                        person_obj.companydetail = company_obj
                        person_obj.updated_by = 'file_3'
                        person_obj.save()
                        # company_obj.save()
                        print 'Saved Person/Company'
                    except Exception, e:
                        print str(traceback.print_exc())
                        transaction.rollback(sid)

                    # For Event

                    # try:
                    #     event_detail_obj = EventDetails.objects.get(event_no=row_values[12].strip())
                    #     person_obj.eventdetail.add(event_detail_obj)
                    #     person_obj.save()
                    # except Exception, e:
                    #     print e
                    #     transaction.rollback(sid)

                except Exception, e:
                    print str(traceback.print_exc())
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\nDone'
        # print '\nTotal Non Member Count = ', total_non_member_count
        # print '\nTotal Member Count = ', total_member_count
        # print '\nTotal Member attended Count = ', member_attended_count
        # print "\nTotal Member's attendees attended Count = ", member_attendees_attended_count
        # print "\nTotal Member's with NO MAIL ID Count = ", member_no_email_count
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


# Check Mail ID matching with Members Database
def check_mails_matching_members():
    try:
        file_path = ['/home/admin12/Test_project/Mass_Mailing/Total participant Report- 24.12.2018.xlsx']
        # file_path = ['/home/admin12/Test_project/Mass_Mailing/Email list HR IR 21.12.2018.xlsx']

        email_list = []
        count_var = 0
        # for file_item in file_path:
        #     print file_item
        #     wb = open_workbook(file_item)
        #     values = []
        #     print wb.sheet_names()
        #     number_of_rows = wb.sheets()[1].nrows
        #     number_of_columns = wb.sheets()[1].ncols
        #     print 'number_of_rows', number_of_rows
        #     print 'number_of_columns', number_of_columns
        #
        #     count_var = 0
        #
        #     for row in range(2, number_of_rows):
        #         row_values = []
        #         for col in range(13):
        #             value = (wb.sheets()[1].cell(row, col).value)
        #             row_values.append(value)
        #         # print row_values
        #         try:
        #             if row_values[7].encode('utf-8').strip() and row_values[7] != '':
        #                 # email_list.append(row_values[7].encode('utf-8').lower().strip())
        #                 print row_values[7]
        #                 temp_email_list = row_values[7].split(',')
        #                 for email_item in temp_email_list:
        #                     email_list.append(email_item.lower().strip())
        #                     # if email_item.strip().lower() in [item.ceo_email.lower().strip() or item.person_email.lower().strip() or item.correspond_email.lower().strip() or item.company.hoddetail.hr_email.lower().strip() or item.company.hoddetail.finance_email.lower().strip() or item.company.hoddetail.marketing_email.lower().strip() or item.company.hoddetail.IT_email.lower().strip() or item.company.hoddetail.corp_rel_email.lower().strip() or item.company.hoddetail.tech_email.lower().strip() or item.company.hoddetail.rnd_email.lower().strip() or item.company.hoddetail.exim_email.lower().strip() for item in UserDetail.objects.filter(~Q(member_associate_no='NULL'), member_associate_no__isnull=False)]:
        #                     #     count_var = count_var + 1
        #
        #         except Exception, e:
        #             # print str(traceback.print_exc())
        #             # transaction.rollback(sid)
        #             pass

        # transaction.savepoint_commit(sid)
        for email_item in PersonDetail.objects.filter(email__isnull=False):
            email_list.append(email_item.email.lower().strip())
        member_list = []
        for item in UserDetail.objects.filter(~Q(member_associate_no='NULL'), member_associate_no__isnull=False):
            if item.correspond_email:
                member_list.append(item.correspond_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.hr_email:
                    member_list.append(item.company.hoddetail.hr_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.finance_email:
                    member_list.append(item.company.hoddetail.finance_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.marketing_email:
                    member_list.append(item.company.hoddetail.marketing_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.IT_email:
                    member_list.append(item.company.hoddetail.IT_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.corp_rel_email:
                    member_list.append(item.company.hoddetail.corp_rel_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.tech_email:
                    member_list.append(item.company.hoddetail.tech_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.rnd_email:
                    member_list.append(item.company.hoddetail.rnd_email.lower().strip())
            if item.company.hoddetail:
                if item.company.hoddetail.exim_email.lower().strip():
                    member_list.append(item.company.hoddetail.exim_email.lower().strip())
            if item.ceo_email:
                member_list.append(item.ceo_email.lower().strip())
            if item.person_email:
                member_list.append(item.person_email.lower().strip())

        a_set = set(member_list)
        b_set = set(email_list)

        if (a_set & b_set):
            print (a_set & b_set)

        print '\nDone'
        print '\ncount_var = ', count_var
        # print '\nTotal Member Count = ', total_member_count
        # print '\nTotal Member attended Count = ', member_attended_count
        # print "\nTotal Member's attendees attended Count = ", member_attendees_attended_count
        # print "\nTotal Member's with NO MAIL ID Count = ", member_no_email_count
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        # transaction.rollback(sid)
    return


# Add Missing Events in system
@transaction.atomic
def add_event_data():
    sid = transaction.savepoint()
    try:
        file_path = ['/home/admin12/Test_project/Mass_Mailing/Events_add.xlsx']

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[1].nrows
            number_of_columns = wb.sheets()[1].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(122, number_of_rows):
                row_values = []
                for col in range(6):
                    value = (wb.sheets()[1].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                # return
                try:
                    event_obj = EventDetails(event_title=row_values[0].strip(),
                                             from_date=datetime.datetime.strptime(str(row_values[1]).strip(),
                                                                                  '%d.%m.%Y').replace(tzinfo=to_zone),
                                             organising_committee=Committee.objects.get(
                                                 committee=str(row_values[5]).strip()))
                    event_obj.save()
                    if row_values[2]:
                        event_obj.to_date = datetime.datetime.strptime(str(row_values[2]).strip(), '%d.%m.%Y').replace(
                            tzinfo=to_zone)
                        event_obj.save()
                    event_obj.event_no = 'E' + str(event_obj.from_date.strftime('%d%m%y')) + str(event_obj.id)
                    event_obj.contact_person1 = SystemUserProfile.objects.get(id=str(int(float(row_values[3]))).strip())
                    if row_values[4]:
                        event_obj.contact_person2 = SystemUserProfile.objects.get(
                            id=str(int(float(row_values[4]))).strip())
                    event_obj.save()
                    print event_obj.event_title,event_obj.event_no
                except Exception, e:
                    print str(traceback.print_exc())
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\nDone'

    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


# Map Events using event_no in system with a single e-mail
# Not in use
@transaction.atomic
def map_event_with_participant():
    sid = transaction.savepoint()
    try:
        file_path = ['/home/admin12/Test_project/Mass_Mailing/Varsha_Mam/Total participant Report- 17.1.2019.xlsx']
        i = 0

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[1].nrows
            number_of_columns = wb.sheets()[1].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            company_name_list = []
            count_var_user = 0
            count_var_city = 0
            i = 1

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(13):
                    value = (wb.sheets()[1].cell(row, col).value)
                    row_values.append(value)
                print row_values
                # return
                try:
                    print '\n\nerererererrrrrrrrrrrrrrrrrrrrrrr = ', row_values[12]
                    if row_values[12]:
                        event_obj = EventDetails.objects.get(event_no=row_values[12].strip())
                        print '\n=================event_obj ======================== ', event_obj

                        # Company Detail Code
                        try:
                            company_obj = None
                            if row_values[5].strip() == 'NM':
                                try:
                                    company_obj = MMCompanyDetail.objects.get(company_name=row_values[3].strip())
                                except Exception, e:
                                    company_obj = MMCompanyDetail(company_name=row_values[3].strip(),
                                                                  gst=row_values[4].strip() if row_values[4] else '')
                                    company_obj.save()
                                    pass
                            elif row_values[5].strip() == 'M':
                                try:
                                    company_obj = MMCompanyDetail.objects.get(company_name=row_values[3].strip())
                                    # Update if company_obj.membership_no is not present
                                except Exception, e:
                                    company_obj = MMCompanyDetail(company_name=row_values[3].strip(),
                                                                  gst=row_values[4].strip() if row_values[4] else '',
                                                                  is_member=True)
                                    company_obj.save()
                                    pass
                            elif row_values[5].strip() == 'MCCIA':
                                try:
                                    company_obj = MMCompanyDetail.objects.get(company_name='MCCIA')
                                    # Update if company_obj.membership_no is not present
                                except Exception, e:
                                    company_obj = MMCompanyDetail(company_name='MCCIA',
                                                                  is_mccia=True)
                                    company_obj.save()
                                    pass
                            else:
                                try:
                                    company_obj = MMCompanyDetail.objects.get(membership_no=row_values[5].strip())
                                except Exception, e:
                                    try:
                                        member_obj = UserDetail.objects.get(member_associate_no=row_values[5].strip())
                                        company_obj = MMCompanyDetail(
                                            userdetail=member_obj, company_name=member_obj.company.company_name.strip(),
                                            company_scale=member_obj.company.company_scale,
                                            gst=member_obj.gst if member_obj.gst else '',
                                            enroll_type=member_obj.enroll_type, is_member=True,
                                            membership_no=member_obj.member_associate_no
                                        )
                                        company_obj.save()
                                        for industry_item in member_obj.company.industrydescription.all():
                                            company_obj.industrydescription.add(industry_item)
                                            company_obj.save()
                                    except Exception, e:
                                        company_obj = MMCompanyDetail(company_name=row_values[3].strip(),
                                                                      gst=row_values[4].strip() if row_values[
                                                                          4] else '',
                                                                      is_member=True)
                                        company_obj.save()
                                        pass
                                    pass

                            print '============================Company====================', company_obj.company_name
                            # Person Detail Code
                            if row_values[7].strip():
                                temp_list = row_values[7].split(',')
                                for email_item in temp_list:
                                    try:
                                        person_obj = PersonDetail.objects.get(email=str(email_item).lower().strip())
                                        person_obj.eventdetail.add(event_obj)
                                        person_obj.save()
                                        # if person_obj.is_member is False:
                                        if row_values[1].strip():
                                            person_obj.name = row_values[1].strip()
                                        if row_values[2].strip():
                                            person_obj.designation = row_values[2].strip()
                                        if row_values[6]:
                                            person_obj.cellno = row_values[6]
                                        if row_values[9].strip():
                                            person_obj.hash_tag = str(person_obj.hash_tag) + ',' + str(
                                                row_values[9].strip())
                                        person_obj.companydetail = company_obj
                                        person_obj.updated_by = str(person_obj.updated_by) + ', Updated_Varsha_Mahajan'
                                        person_obj.save()
                                    except Exception, e:
                                        person_obj = PersonDetail(
                                            name=row_values[1].strip() if row_values[1].strip() else '',
                                            email=str(email_item).strip().lower(),
                                            designation=row_values[2].strip() if row_values[2].strip() else '',
                                            cellno=row_values[6] if row_values[6] else '',
                                            is_member=company_obj.is_member,
                                            is_mccia_person=company_obj.is_mccia,
                                            companydetail=company_obj,
                                            updated_by='Newly_Added',
                                            created_by='Varsha_Mahajan'
                                        )
                                        person_obj.save()
                                        person_obj.eventdetail.add(event_obj)
                                        person_obj.save()
                                        # print e
                                        pass
                        except Exception, e:
                            print 'Person Obj not found. = ', e, str(traceback.print_exc())
                            print row_values[7].strip(), len(row_values[7].strip())
                            # print file_item
                            transaction.rollback(sid)
                            # pass
                except Exception, e:
                    # print str(traceback.print_exc())
                    transaction.rollback(sid)

                    # try:
                    #     event_detail_obj = EventDetails.objects.get(event_no=row_values[12].strip())
                    #     person_obj.eventdetail.add(event_detail_obj)
                    #     person_obj.save()
                    # except Exception, e:
                    #     print e
                    #     transaction.rollback(sid)

                # except Exception, e:
                #     print str(traceback.print_exc())
                #     transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\nDone'
    except Exception, e:
        # print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


def check_imported_data():
    try:
        person_detail_list = PersonDetail

    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())

    return


# Import Members Data
# Not in use
@transaction.atomic
def import_members_data():
    sid = transaction.savepoint()
    person_email_list = []
    count = 0
    try:
        for person_obj in PersonDetail.objects.all():
            person_email_list.append(person_obj.email.lower().strip())
        for member_obj in UserDetail.objects.all():
            company_obj = ''
            try:
                company_obj = MMCompanyDetail.objects.get(userdetail=member_obj)
            except Exception:
                new_company_obj = MMCompanyDetail(userdetail=member_obj,
                                                  company_name=member_obj.company.company_name.strip(),
                                                  company_scale=member_obj.company.company_scale,
                                                  gst=member_obj.gst.strip() if member_obj.gst and member_obj.gst != 'NA' else None,
                                                  enroll_type=member_obj.enroll_type,
                                                  is_member=True,
                                                  membership_no=member_obj.member_associate_no.strip() if member_obj.member_associate_no else None,
                                                  created_by='Mem_in_Per')
                new_company_obj.save()
                if member_obj.company.industrydescription:
                    for industry_obj in member_obj.company.industrydescription.all():
                        new_company_obj.industrydescription.add(industry_obj)
                        new_company_obj.save()
                company_obj = new_company_obj
                pass

            if member_obj.ceo_email:
                if str(member_obj.ceo_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.ceo_name.strip() if member_obj.enroll_type == 'CO' else member_obj.company.company_name.strip(),
                        email=str(member_obj.ceo_email).lower().strip(),
                        designation='CEO',
                        cellno=member_obj.ceo_cellno if member_obj.enroll_type == 'CO' else member_obj.person_cellno,
                        is_member=True, companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.correspond_email:
                if str(member_obj.correspond_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(name=None,
                                                  email=str(member_obj.correspond_email).lower().strip(),
                                                  designation=None, cellno=None, companydetail=company_obj,
                                                  is_member=True, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.hr_email:
                if str(member_obj.company.hoddetail.hr_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(name=member_obj.company.hoddetail.hr_name.strip(),
                                                  email=str(member_obj.company.hoddetail.hr_email).lower().strip(),
                                                  designation='HR',
                                                  cellno=member_obj.company.hoddetail.hr_contact.strip(),
                                                  is_member=True, companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.finance_email:
                if str(member_obj.company.hoddetail.finance_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.company.hoddetail.finance_name.strip(),
                        email=str(member_obj.company.hoddetail.finance_email).lower(),
                        designation='Finance',
                        is_member=True, cellno=member_obj.company.hoddetail.finance_contact.strip(),
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.marketing_email:
                if str(member_obj.company.hoddetail.marketing_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.company.hoddetail.marketing_name.strip(),
                        email=str(member_obj.company.hoddetail.marketing_email).lower().strip(),
                        designation='Marketing',
                        is_member=True, cellno=member_obj.company.hoddetail.marketing_contact.strip(),
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.IT_email:
                if str(member_obj.company.hoddetail.IT_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.company.hoddetail.IT_name.strip(),
                        email=str(member_obj.company.hoddetail.IT_email).lower().strip(),
                        designation='IT',
                        is_member=True, cellno=member_obj.company.hoddetail.IT_contact.strip(),
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.corp_rel_email:
                if str(member_obj.company.hoddetail.corp_rel_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.company.hoddetail.corp_rel_name.strip(),
                        email=str(member_obj.company.hoddetail.corp_rel_email).lower().strip(),
                        designation='Corporate Relation',
                        is_member=True, cellno=member_obj.company.hoddetail.corp_rel_contact.strip(),
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.tech_email:
                if str(member_obj.company.hoddetail.tech_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.company.hoddetail.tech_name.strip(),
                        email=str(member_obj.company.hoddetail.tech_email).lower().strip(),
                        designation='TECH',
                        is_member=True, cellno=member_obj.company.hoddetail.tech_contact.strip(),
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.rnd_email:
                if str(member_obj.company.hoddetail.rnd_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.company.hoddetail.rnd_name.strip(),
                        email=str(member_obj.company.hoddetail.rnd_email).lower().strip(),
                        designation='R&D',
                        is_member=True, cellno=member_obj.company.hoddetail.rnd_contact.strip(),
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.company.hoddetail and member_obj.company.hoddetail.exim_email:
                if str(member_obj.company.hoddetail.exim_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=member_obj.company.hoddetail.exim_name.strip(),
                        email=str(member_obj.company.hoddetail.exim_email).lower().strip(),
                        designation='EXIM', is_member=True,
                        cellno=member_obj.company.hoddetail.exim_contact.strip(),
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)

            if member_obj.person_email:
                if str(member_obj.person_email).lower().strip() not in person_email_list:
                    new_person_obj = PersonDetail(
                        name=None,
                        email=str(member_obj.person_email).lower().strip(),
                        designation=None,
                        cellno=None, is_member=True,
                        companydetail=company_obj, created_by='Mem_in_Per')
                    new_person_obj.save()
                    person_email_list.append(new_person_obj.email)
            count = count + 1
            print 'Count = ', count
            print 'Company = ', company_obj.company_name, ' Email = ', new_person_obj.email
        transaction.savepoint_commit(sid)
        print '\nDone'
        return True
    except Exception, e:
        print '\nError = ', e, str(traceback.print_exc())
        transaction.rollback(sid)
        return False


# Import Non-Member Data
@transaction.atomic
def import_nonmember_data():
    sid = transaction.savepoint()
    try:
        file_path = ['/home/admin12/Test_project/Mass_Mailing/Sendinblue_Non_Member.xlsx']

        count = 0
        total_count = 0
        found_count = 0

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(3):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                try:
                    total_count = total_count + 1
                    try:
                        person_obj = PersonDetail.objects.get(email=str(row_values[0]).lower().strip())
                        found_count = found_count + 1
                    except Exception:
                        new_person_obj = PersonDetail(email=str(row_values[0]).lower().strip(),
                                                      created_by='Nonmember_nocompany_sendinblue')
                        new_person_obj.save()
                        print 'Email = ', new_person_obj.email
                        pass
                    count = count + 1
                    print 'Count = ', count
                except Exception, e:
                    print str(traceback.print_exc())
                    transaction.rollback(sid)

                    # try:
                    #     event_detail_obj = EventDetails.objects.get(event_no=row_values[12].strip())
                    #     person_obj.eventdetail.add(event_detail_obj)
                    #     person_obj.save()
                    # except Exception, e:
                    #     print e
                    #     transaction.rollback(sid)

                # except Exception, e:
                #     print str(traceback.print_exc())
                #     transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\nDone'
        print 'Total = ', total_count
        print 'Found = ', found_count
        return True
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
        return False


@transaction.atomic
def insert_event_participant_data():
    sid = transaction.savepoint()
    try:
        # file_path = ['/home/admin12/Test_project/Merged_All/Merged_All.xlsx']
        file_path = ['/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/Event_Data/All_Merged_After_22_Feb_19.xlsx']        
        i = 0

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            company_name_list = []
            count_var_user = 0
            count_var_city = 0
            i = 1

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                # return
                try:
                    # print '\n\nerererererrrrrrrrrrrrrrrrrrrrrrr = ', row_values[12]
                    if row_values[12]:
                        event_obj = EventDetails.objects.get(event_no=row_values[12].strip())
                        if row_values[10].strip() == 'Free':
                            event_obj.event_mode = 0
                        else:
                            event_obj.event_mode = 1
                        event_obj.save()                        

                        # print '\n=================event_obj ======================== ', event_obj

                        # Company Detail Code
                        try:
                            final_object = None
                            company_obj = None
                            # For Non Member Start
                            if row_values[5].strip() == 'NM':
                                try:
                                    company_obj = CompanyDetail.objects.get(company_name=row_values[1].replace(u'\xa0', u'').strip() if row_values[3].strip() == 'Individual' else row_values[3].replace(u'\xa0', u'').strip(),
                                                                            is_member=False)
                                    non_member_obj = NonMemberDetail.objects.get(company=company_obj)
                                    final_object = non_member_obj
                                    temp_email_list = row_values[7].split(',')
                                    for item in temp_email_list:
                                        if non_member_obj.extra_email:
                                            if item not in non_member_obj.extra_email.split(','):
                                                non_member_obj.extra_email = str(non_member_obj.extra_email) + ',' + str(item).lower().strip()
                                                non_member_obj.save()
                                        else:
                                            non_member_obj.extra_email = str(item).lower().strip()
                                            non_member_obj.save()
                                    for email_item in temp_email_list:
                                        try:
                                            email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                       is_member=False)
                                            email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                            email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                            email_detail_obj.cellno = row_values[6]
                                            if email_detail_obj.hash_tag:
                                                email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(row_values[9].strip())
                                            else:
                                                email_detail_obj.hash_tag = str(row_values[9].strip())
                                            email_detail_obj.save()
                                        except Exception, e:
                                            new_email_detail_obj = EmailDetail(
                                                name = row_values[1].strip() if row_values[1].strip() else '',
                                                email=str(email_item).lower().strip(),
                                                designation = row_values[2].strip() if row_values[2] else '',
                                                cellno = row_values[6],
                                                nonmemberdetail=non_member_obj,
                                                hash_tag=str(row_values[9].strip()),
                                                created_by='shubham'
                                            )
                                            new_email_detail_obj.save()
                                            pass
                                except Exception, e:
                                    temp_email_list = row_values[7].split(',')
                                    non_member_object = None
                                    for non_member_item in NonMemberDetail.objects.all():
                                        result = False
                                        if non_member_item.extra_email:
                                            result = [True for item in temp_email_list if str(item).lower().strip() in non_member_item.extra_email.split(',')]
                                        else:
                                            result = True if non_member_item.email in temp_email_list else False
                                        if result:
                                            non_member_object = non_member_item
                                            break
                                    if non_member_object:
                                        for item in temp_email_list:
                                            if non_member_object.extra_email:
                                                if item not in non_member_object.extra_email.split(','):
                                                    non_member_object.extra_email = str(non_member_object.extra_email) + ',' + str(item).lower().strip()
                                                    non_member_object.save()
                                            else:
                                                non_member_object.extra_email = str(item).lower().strip()
                                                non_member_object.save()
                                        if non_member_object.company:
                                            company_obj = non_member_object.company
                                        else:
                                            company_obj = CompanyDetail(company_name=row_values[1].replace(u'\xa0', u'').strip() if row_values[3].strip() == 'Individual' else row_values[3].replace(u'\xa0', u'').strip(),
                                                                        gst=row_values[4].strip() if row_values[4] else '', created_by='shubham')
                                            company_obj.save()
                                            non_member_object.company = company_obj
                                            non_member_object.save()
                                    else:
                                        company_obj = CompanyDetail(company_name=row_values[1].replace(u'\xa0', u'').strip() if row_values[3].strip() == 'Individual' else row_values[3].replace(u'\xa0', u'').strip(),
                                                                    gst=row_values[4].strip() if row_values[4] else '', created_by='shubham')
                                        company_obj.save()
                                        for index, item in enumerate(temp_email_list):
                                            if index == 0:
                                                new_non_member_obj = NonMemberDetail(
                                                    email=str(item).lower().strip(),
                                                    extra_email=str(item).lower().strip(),
                                                    company=company_obj,
                                                    enroll_type='IN' if row_values[3].strip() == 'Individual' else 'CO',
                                                    created_by='shubham'
                                                )
                                                new_non_member_obj.save()
                                            else:
                                                new_non_member_obj.extra_email = str(new_non_member_obj.extra_email) + ',' + str(item).lower().strip()
                                                new_non_member_obj.save()
                                            non_member_object = new_non_member_obj

                                    final_object = non_member_object
                                    for email_item in temp_email_list:
                                        try:
                                            email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                       is_member=False)
                                            email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                            email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                            email_detail_obj.cellno = row_values[6]
                                            if email_detail_obj.hash_tag:
                                                email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(row_values[9].strip())
                                            else:
                                                email_detail_obj.hash_tag = str(row_values[9].strip())
                                            email_detail_obj.save()
                                        except Exception, e:
                                            new_email_detail_obj = EmailDetail(
                                                name = row_values[1].strip() if row_values[1].strip() else '',
                                                email=str(email_item).lower().strip(),
                                                designation = row_values[2].strip() if row_values[2] else '',
                                                cellno = row_values[6],
                                                nonmemberdetail=non_member_object,
                                                hash_tag=str(row_values[9].strip()),
                                                created_by='shubham'
                                            )
                                            new_email_detail_obj.save()
                                            pass
                                    pass

                            # For Non Member End

                            # For Member without Membership Number Start

                            elif row_values[5].strip() == 'M':
                                try:
                                    company_obj = CompanyDetail.objects.get(company_name=row_values[1].replace(u'\xa0', u'').strip() if row_values[3].strip() == 'Individual' else row_values[3].replace(u'\xa0', u'').strip(),
                                                                            is_member=True)
                                    # Update if company_obj.membership_no is not present

                                    final_object = company_obj
                                    temp_email_list = row_values[7].split(',')
                                    for item in temp_email_list:
                                        if item not in company_obj.member_event_email.split(','):
                                            company_obj.member_event_email = str(company_obj.member_event_email) + ',' + str(item).lower().strip()
                                            company_obj.save()
                                    for email_item in temp_email_list:
                                        try:
                                            nm_email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                          is_member=False)
                                            nm_email_detail_obj.is_deleted = True
                                            nm_email_detail_obj.save()
                                        except Exception as e:
                                            pass

                                        try:
                                            email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                       is_member=True)
                                            email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                            email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                            email_detail_obj.cellno = row_values[6]
                                            if email_detail_obj.hash_tag:
                                                email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(row_values[9].strip())
                                            else:
                                                email_detail_obj.hash_tag = str(row_values[9].strip())
                                            email_detail_obj.save()
                                        except Exception, e:
                                            new_email_detail_obj = EmailDetail(
                                                name=row_values[1].strip() if row_values[1].strip() else '',
                                                email=str(email_item).lower().strip(),
                                                designation=row_values[2].strip() if row_values[2] else '',
                                                cellno=row_values[6],
                                                companydetail=company_obj,
                                                hash_tag=str(row_values[9].strip()),
                                                is_member=True,
                                                created_by='shubham'
                                            )
                                            new_email_detail_obj.save()
                                            pass
                                except Exception, e:
                                    temp_email_list = row_values[7].split(',')
                                    member_object = None
                                    for member_item in CompanyDetail.objects.all():
                                        result = False
                                        if member_item.member_event_email:
                                            result = [True for item in temp_email_list if str(item).lower().strip() in member_item.member_event_email.split(',')]
                                        else:
                                            result = True if member_item.member_event_email in temp_email_list else False
                                        if result:
                                            member_object = member_item
                                            break
                                    if member_object:
                                        for item in temp_email_list:
                                            if member_object.member_event_email:
                                                if item not in member_object.member_event_email.split(','):
                                                    member_object.member_event_email = str(member_object.member_event_email) + ',' + str(item).lower().strip()
                                                    member_object.save()
                                            else:
                                                member_object.member_event_email = str(item).lower().strip()
                                                member_object.save()
                                    else:
                                        company_obj = CompanyDetail(company_name=row_values[1].replace(u'\xa0', u'').strip() if row_values[3].strip() == 'Individual' else row_values[3].replace(u'\xa0', u'').strip(),
                                                                    gst=row_values[4].strip() if row_values[4] else '',is_member=True,
                                                                    enroll_type='IN' if row_values[3].strip() == 'Individual' else 'CO', created_by='shubham')
                                        company_obj.save()
                                        member_object = company_obj

                                        for item in temp_email_list:
                                            if member_object.member_event_email:
                                                if item not in member_object.member_event_email.split(','):
                                                    member_object.member_event_email = str(member_object.member_event_email) + ',' + str(item).lower().strip()
                                                    member_object.save()
                                            else:
                                                member_object.member_event_email = str(item).lower().strip()
                                                member_object.save()

                                    final_object = member_object
                                    for email_item in temp_email_list:
                                        try:
                                            nm_email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                          is_member=False)
                                            nm_email_detail_obj.is_deleted = True
                                            nm_email_detail_obj.save()
                                        except Exception as e:
                                            pass
                                        try:
                                            email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                       is_member=True)
                                            email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                            email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                            email_detail_obj.cellno = row_values[6]
                                            if email_detail_obj.hash_tag:
                                                email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(row_values[9].strip())
                                            else:
                                                email_detail_obj.hash_tag = str(row_values[9].strip())
                                            email_detail_obj.save()
                                        except Exception, e:
                                            new_email_detail_obj = EmailDetail(
                                                name=row_values[1].strip() if row_values[1].strip() else '',
                                                email=str(email_item).lower().strip(),
                                                designation=row_values[2].strip() if row_values[2] else '',
                                                cellno=row_values[6],
                                                companydetail=member_object,
                                                hash_tag=str(row_values[9].strip()),
                                                created_by='shubham'
                                            )
                                            new_email_detail_obj.save()
                                            pass
                                    pass

                            # For Member without Membership Number Start

                            # For MCCIA Company Start

                            elif row_values[5].strip() == 'MCCIA':
                                try:
                                    company_obj = CompanyDetail.objects.get(company_name='MCCIA', is_member=False)
                                    final_object = company_obj
                                    temp_email_list = row_values[7].split(',')
                                    for item in temp_email_list:
                                        if company_obj.member_event_email:
                                            if item not in company_obj.member_event_email.split(','):
                                                company_obj.member_event_email = str(company_obj.member_event_email) + ',' + str(item).lower().strip()
                                                company_obj.save()
                                        else:
                                            company_obj.member_event_email = str(item).lower().strip()
                                            company_obj.save()
                                        try:
                                            email_detail_obj = EmailDetail.objects.get(email=str(item).lower().strip(),
                                                                                       is_member=False)
                                            email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                            email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                            email_detail_obj.cellno = row_values[6]
                                            if email_detail_obj.hash_tag:
                                                email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(row_values[9].strip())
                                            else:
                                                email_detail_obj.hash_tag = str(row_values[9].strip())
                                            email_detail_obj.save()
                                        except Exception, e:
                                            new_email_detail_obj = EmailDetail(
                                                name=row_values[1].strip() if row_values[1].strip() else '',
                                                email=str(item).lower().strip(),
                                                designation=row_values[2].strip() if row_values[2] else '',
                                                cellno=row_values[6],
                                                companydetail=company_obj,
                                                hash_tag=str(row_values[9].strip()),
                                                is_member=False,
                                                is_mccia_person=True,
                                                created_by='shubham'
                                            )
                                            new_email_detail_obj.save()
                                            pass
                                except Exception, e:
                                    company_obj = CompanyDetail(company_name='MCCIA',
                                                                gst=row_values[4].strip() if row_values[4] else '',
                                                                is_member=False,enroll_type='CO', created_by='shubham')
                                    company_obj.save()
                                    member_object = company_obj
                                    final_object = member_object
                                    for item in temp_email_list:
                                        if company_obj.member_event_email:
                                            if item not in company_obj.member_event_email.split(','):
                                                company_obj.member_event_email = str(company_obj.member_event_email) + ',' + str(item).lower().strip()
                                                company_obj.save()
                                        else:
                                            company_obj.member_event_email = str(item).lower().strip()
                                            company_obj.save()

                                    for email_item in temp_email_list:
                                        try:
                                            email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                       is_member=False)
                                            email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                            email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                            email_detail_obj.cellno = row_values[6]
                                            if email_detail_obj.hash_tag:
                                                email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(row_values[9].strip())
                                            else:
                                                email_detail_obj.hash_tag = str(row_values[9].strip())
                                            email_detail_obj.save()
                                        except Exception, e:
                                            new_email_detail_obj = EmailDetail(
                                                name=row_values[1].strip() if row_values[1].strip() else '',
                                                email=str(email_item).lower().strip(),
                                                designation=row_values[2].strip() if row_values[2] else '',
                                                cellno=row_values[6],
                                                companydetail=member_object,
                                                hash_tag=str(row_values[9].strip()),
                                                is_member=False,
                                                is_mccia_person=True,
                                                created_by='shubham'
                                            )
                                            new_email_detail_obj.save()
                                            pass
                                    pass

                            # For MCCIA Company Start

                            # For Membership Number Start
                            else:
                                try:
                                    member_no_list = row_values[5].split('-')
                                    member_no = str(member_no_list[0].strip()) + '-' + str(member_no_list[1].strip())
                                    company_obj = UserDetail.objects.filter(member_associate_no=member_no).last()
                                    if company_obj:
                                        final_object = company_obj
                                        temp_email_list = row_values[7].split(',')
                                        for item in temp_email_list:
                                            if company_obj.event_email:
                                                if item not in company_obj.event_email.split(','):
                                                    company_obj.event_email = str(company_obj.event_email) + ',' + str(item).lower().strip()
                                                    company_obj.save()
                                            else:
                                                company_obj.event_email = str(item).lower().strip()
                                                company_obj.save()

                                        for email_item in temp_email_list:
                                            try:
                                                nm_email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                             is_member=False)
                                                nm_email_detail_obj.is_deleted = True
                                                nm_email_detail_obj.save()
                                            except Exception as e:
                                                pass

                                            try:
                                                email_detail_obj = EmailDetail.objects.get(email=str(email_item).lower().strip(),
                                                                                           is_member=True)
                                                email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                                email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                                email_detail_obj.cellno = row_values[6]
                                                if email_detail_obj.hash_tag:
                                                    email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(row_values[9].strip())
                                                else:
                                                    email_detail_obj.hash_tag = str(row_values[9].strip())
                                                email_detail_obj.save()
                                            except Exception, e:
                                                new_email_detail_obj = EmailDetail(
                                                    name=row_values[1].strip() if row_values[1].strip() else '',
                                                    email=str(email_item).lower().strip(),
                                                    designation=row_values[2].strip() if row_values[2] else '',
                                                    cellno=row_values[6],
                                                    userdetail=company_obj,
                                                    hash_tag=str(row_values[9].strip()),
                                                    is_member=True,
                                                    created_by='shubham'
                                                )
                                                new_email_detail_obj.save()
                                                pass
                                    else:
                                        print 1/0
                                except Exception, e:
                                    company_obj = CompanyDetail(company_name=row_values[1].replace(u'\xa0', u'').strip() if row_values[3].strip() == 'Individual' else row_values[3].replace(u'\xa0', u'').strip(),
                                                                gst=row_values[4].strip() if row_values[4] else '',is_member=True,
                                                                enroll_type='IN' if row_values[3].strip() == 'Individual' else 'CO', created_by='shubham')
                                    company_obj.save()
                                    final_object = company_obj
                                    temp_email_list = row_values[7].split(',')
                                    for item in temp_email_list:
                                        if company_obj.member_event_email:
                                            if item not in company_obj.member_event_email.split(','):
                                                company_obj.member_event_email = str(company_obj.member_event_email) + ',' + str(item).lower().strip()
                                                company_obj.save()
                                        else:
                                            company_obj.member_event_email = str(item).lower().strip()
                                            company_obj.save()

                                        try:
                                            nm_email_detail_obj = EmailDetail.objects.get(email=str(item).lower().strip(),
                                                                                          is_member=False)
                                            nm_email_detail_obj.is_deleted = True
                                            nm_email_detail_obj.save()
                                        except Exception as e:
                                            pass

                                        try:
                                            email_detail_obj = EmailDetail.objects.get(email=str(item).lower().strip(),
                                                                                       is_member=True)
                                            email_detail_obj.name = row_values[1].strip() if row_values[1].strip() else ''
                                            email_detail_obj.designation = row_values[2].strip() if row_values[2] else ''
                                            email_detail_obj.cellno = row_values[6]
                                            if email_detail_obj.hash_tag:
                                                email_detail_obj.hash_tag = str(email_detail_obj.hash_tag) + ',' + str(
                                                    row_values[9].strip())
                                            else:
                                                email_detail_obj.hash_tag = str(row_values[9].strip())
                                            email_detail_obj.save()
                                        except Exception, e:
                                            new_email_detail_obj = EmailDetail(
                                                name=row_values[1].strip() if row_values[1].strip() else '',
                                                email=str(item).lower().strip(),
                                                designation=row_values[2].strip() if row_values[2] else '',
                                                cellno=row_values[6],
                                                companydetail=company_obj,
                                                hash_tag=str(row_values[9].strip()),
                                                is_member=True,
                                                created_by='shubham'
                                            )
                                            new_email_detail_obj.save()
                                            pass
                                    pass
                            # For Membership Number End

                            # print '============================Company====================', company_obj.company_name

                            temp_list = row_values[7].split(',')
                            for index, email_item in enumerate(temp_list):
                                if index == 0:
                                    event_reg_obj = EventRegistration(
                                        event=event_obj,
                                        name_of_organisation=final_object.company.company_name if final_object.__class__.__name__ in ['UserDetail','NonMemberDetail'] else final_object.company_name,
                                        contact_person_name=row_values[1].strip(),
                                        contact_person_number=row_values[6],
                                        office_contact=row_values[6],
                                        contact_person_email_id=str(email_item).lower().strip(),
                                        no_of_participant=len(temp_list),
                                        gst=row_values[4].strip() if row_values[4] else '',
                                        created_by=row_values[18].strip(),
                                        is_invitee=True if row_values[17].strip() == 'YES' else False,
                                        is_attendees=True,
                                        updated_by='shubham'                                       
                                    )
                                    event_reg_obj.save()
                                    print row_values[0], row_values[1], 'Added'
                                    event_participant_obj = EventParticipantUser(
                                        event_user=event_reg_obj,
                                        event_user_name=row_values[1].strip(),
                                        designation=row_values[2].strip() if row_values[2] else '',
                                        contact_no=row_values[6],
                                        email_id=str(email_item).lower().strip(),
                                        created_by=row_values[18].strip(), 
                                        updated_by='shubham'                                       
                                    )
                                    event_participant_obj.save()

                                else:
                                    # print '=====================Check Object of Event===================', event_reg_obj
                                    event_participant_obj = EventParticipantUser(
                                        event_user=event_reg_obj,
                                        event_user_name=row_values[1].strip(),
                                        designation=row_values[2].strip() if row_values[2] else '',
                                        contact_no=row_values[6],
                                        email_id=str(email_item).lower().strip(),
                                        created_by=row_values[18].strip(),
                                        updated_by='shubham'                                       
                                    )
                                    event_participant_obj.save()

                                if final_object.__class__.__name__ == 'UserDetail':
                                    event_reg_obj.user_details = final_object
                                    event_reg_obj.is_member = True
                                elif row_values[5].strip() == 'M':
                                    event_reg_obj.companydetail = final_object
                                    event_reg_obj.is_member = True
                                elif row_values[5].strip() == 'MCCIA':
                                    event_reg_obj.companydetail = final_object
                                elif row_values[5].strip() not in ['M', 'NM', 'MCCIA']:
                                    event_reg_obj.companydetail = final_object
                                    event_reg_obj.is_member = True
                                else:
                                    event_reg_obj.nonmemberdetail = final_object
                                event_reg_obj.save()
                        except Exception, e:
                            print '\nError = ', e, str(traceback.print_exc())
                            print row_values[7].strip(), len(row_values[7].strip())
                            # print file_item
                            transaction.rollback(sid)
                            # pass
                except Exception, e:
                    if row_values[12].strip() == 'NOT_IN_PROD':
                        pass
                    else:
                        print str(traceback.print_exc())
                        print e
                        transaction.rollback(sid)

                    # try:
                    #     event_detail_obj = EventDetails.objects.get(event_no=row_values[12].strip())
                    #     person_obj.eventdetail.add(event_detail_obj)
                    #     person_obj.save()
                    # except Exception, e:
                    #     print e
                    #     transaction.rollback(sid)

                # except Exception, e:
                #     print str(traceback.print_exc())
                #     transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\nDone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc()),'\n',e
        transaction.rollback(sid)
    return


def get_temp_event_count():
    try:
        total_individual = 0
        total_org = 0
        individual_member = 0
        individual_nonmember = 0
        org_member = 0
        org_nonmember = 0

        for participant_item in EventParticipantUser.objects.filter(event_user__created_by='Sandhya_Mam'):
            total_individual = total_individual + 1
            if participant_item.event_user.is_member:
                individual_member = individual_member + 1
            else:
                individual_nonmember = individual_nonmember + 1

            if participant_item.event_user.user_details:
                if participant_item.event_user.user_details.enroll_type == 'CO':
                    total_org = total_org + 1
                    org_member = org_member + 1
            elif participant_item.event_user.companydetail:
                if participant_item.event_user.companydetail.enroll_type == 'CO':
                    total_org = total_org + 1
                    if participant_item.event_user.companydetail.is_member:
                        org_member = org_member + 1
                    # else:
                    #     org_nonmember = org_nonmember + 1
            elif participant_item.event_user.nonmemberdetail:
                if participant_item.event_user.nonmemberdetail.enroll_type == 'CO':
                    total_org = total_org + 1
                    org_nonmember = org_nonmember + 1
                    print participant_item.event_user.nonmemberdetail.company.company_name

        print 'Total Individual = ', total_individual
        print 'Total Individual Member = ', individual_member
        print 'Total Individual Non-Member = ', individual_nonmember
        print 'Total Organization = ', total_org
        print 'Total Organization Member = ', org_member
        print 'Total Organization Non-Member = ', org_nonmember

        to = 0
        tmo = 0
        tnonm = 0

        to = EventRegistration.objects.filter(Q(user_details__isnull=False, companydetail__isnull=False, nonmemberdetail__isnull=False),created_by='Sandhya_Mam').count()
        for event_user in EventRegistration.objects.filter(created_by='Sandhya_Mam'):
            if event_user.user_details:
                if event_user.user_details.enroll_type == 'CO':
                    to = to + 1
                    tmo = tmo + 1
            elif event_user.companydetail:
                if event_user.companydetail.enroll_type == 'CO':
                    to = to + 1
                    if event_user.companydetail.is_member:
                        tmo = tmo + 1
                    # else:
                    #     org_nonmember = org_nonmember + 1
            elif event_user.nonmemberdetail:
                if event_user.nonmemberdetail.enroll_type == 'CO':
                    to = to + 1
                    tnonm = tnonm + 1

        print to,tmo,tnonm
    except Exception, e:
        print e


def delete_event_data():
    try:
        # reg_list = EventRegistration.objects.filter(event_id__in=[141,142,199,143,144,180,182,193,200,145,212,219,146,147,181,187,192,194,211,213,214,148,223,149,175,201,225,188,189,195,196,150,151,152,217,218,153,154,155,156,226,157,158,184,185,186,190,191,202,197,198,203,210,159,160,215,216,222,172,173,204,161,176,162,163,177,178,205,164,206,165,166,167,168,207,220,221,169,208,224,170,174,179,183,209,227,171,4,1,13,236,2,3,6,10,9,14,18,5,12,11,15,19,8,23,28,16,17,20,21,7,25,26,230,237,22,30,31,32,231,24,232,37,27,29,36,38,47,33,45,46,50,39,40,41,44,233,35,52,234,42,53,54,55,48,34,51,43,56,62,57,61,235,66,58,60,65,73,49,64,70,72,68,63,67,76,77,81,78,59,79,80,85,87,88,89,71,82,94,95,92,97,98,91,100,102,75,83,86,90,106,96,107,99,101])
        reg_list = EventRegistration.objects.filter(event__event_no__in=['E070319104','E150319115','E160319117','E190319123','E200319124','E260219112','E260319126','E270219114','E27021984','E270319125','E270319132'])        
        EventParticipantUser.objects.filter(event_user__in=[item for item in reg_list]).delete()
        for i in reg_list:
            if i.nonmemberdetail:
                i.nonmemberdetail.updated_by = 'deleted_participant'
                i.nonmemberdetail.save()
        EventRegistration.objects.filter(event__event_no__in=['E070319104','E150319115','E160319117','E190319123','E200319124','E260219112','E260319126','E270219114','E27021984','E270319125','E270319132']).delete()
        print '\nDone'
    except Exception as e:
        print e


# For giving data to intern
@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Account Report'], login_url='/backofficeapp/login/', raise_exception=True)
def get_hall_booking_data(request):
    try:
        i = 1
        hall_name = 'NA'
        time_slot = ''
        date_slot = ''

        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Applicant_Detail')

        column_name = ['Sr #', 'Location', 'Event Date', 'Event Time', 'Booking Date', 'Booking No',
                       'Hall Name', 'Event Type', 'Member / Non-Member', 'Company Name', 'Contact Person', 'Contact No',
                       'Email', 'Total Amount', 'Paid', 'Status']

        for i in range(len(column_name)):
            worksheet1.write_string(0, int(i), column_name[i])

        booking_details = HallBookingDetail.objects.filter(is_cancelled=False, is_deleted=False).exclude(booking_status__in=[0, 10])
        for hallbooking in booking_details:
            # final_booking_details = HallBookingDetail.objects.filter(hall_booking=hallbooking.hall_booking)
            # for booking_detail in final_booking_details:
            amount_paid = HallPaymentDetail.objects.filter(hall_booking=hallbooking.hall_booking, paid_amount__gt=0,
                                                           is_deleted=False).aggregate(Sum('paid_amount'))
            if hallbooking.hall_detail:
                hall_name = hallbooking.hall_detail.hall_name
            else:
                hall_name = 'NA'
            if hallbooking.updated_by:
                time_slot = str(hallbooking.booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p')) + '-' + \
                            str(hallbooking.booking_to_date.astimezone(to_zone).time().strftime(
                                '%I:%M %p'))
            else:
                time_slot = str(hallbooking.booking_from_date.strftime('%I:%M %p')) + '-' + \
                            str(hallbooking.booking_to_date.strftime('%I:%M %p'))
            date_slot = str(hallbooking.booking_from_date.strftime('%B %d,%Y'))

            if hallbooking.hall_booking.booking_status in [2, 3, 4, 5, 6, 7, 8]:
                action = 'Pencil_Icon'
            elif hallbooking.hall_booking.payment_status == 1:
                action = 'PAID'

            worksheet1.write_string(i, 0, str(i))
            worksheet1.write_string(i, 1, str(hallbooking.hall_location.location))
            worksheet1.write_string(i, 2, str(date_slot))
            worksheet1.write_string(i, 3, str(time_slot))
            worksheet1.write_string(i, 4, str(hallbooking.hall_booking.created_date.strftime('%B %d,%Y')))
            worksheet1.write_string(i, 5, str(hallbooking.hall_booking.booking_no))
            worksheet1.write_string(i, 6, str(hall_name))
            worksheet1.write_string(i, 7, str(hallbooking.event_nature))

            if hallbooking.hall_booking.member:
                worksheet1.write_string(i, 8, str(hallbooking.hall_booking.member.member_associate_no))
            else:
                worksheet1.write_string(i, 8, 'NM')

            worksheet1.write_string(i, 9, str(hallbooking.hall_booking.name))
            worksheet1.write_string(i, 10, str(hallbooking.contact_person))
            worksheet1.write_string(i, 11, str(hallbooking.mobile_no))
            worksheet1.write_string(i, 12, str(hallbooking.email))
            worksheet1.write_string(i, 13, str(hallbooking.hall_booking.total_payable))
            worksheet1.write_string(i, 14, str(amount_paid['paid_amount__sum']))
            worksheet1.write_string(i, 15, str(hallbooking.hall_booking.get_booking_status_display()))
            i = i + 1
        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Hall_Booking_Data_Demo.xlsx'
        return response
    except Exception as e:
        print e
        print str(traceback.print_exc())
        return HttpResponse(status=400)


if __name__ == "__main__":
    # check_data()
    # update_event_no()
    # save_data()
    # check_mails_matching_members()
    # add_event_data()
    # update_event_no()
    # map_event_with_participant()
    # check_imported_data()
    # import_members_data()
    # import_nonmember_data()
    # insert_event_participant_data()
    # get_temp_event_count()
    # delete_event_data()
    # get_hall_booking_data()
    pass

