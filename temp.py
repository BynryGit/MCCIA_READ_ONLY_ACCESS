import os
import django
import sys
from MCCIA import settings
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()



import datetime
from backofficeapp.models import UserPrivilege
mccia_privileges = ['Dashboard', 'Membership', 'Hall Booking', 'Event', 'Administrator']

#Don't Use this
def add_privilege():
    today_date = datetime.datetime.now()
    print today_date

    for privilege in mccia_privileges:
        try:
            UserPrivilege.objects.get(privilege=privilege)
        except Exception, e:
            print e
            userPrivilege = UserPrivilege(
                privilege=privilege,
                created_by='admin',
                created_on=today_date,
                is_deleted=False,
            )
            userPrivilege.save()
            pass

def new_add_privilege():
    today_date = datetime.datetime.now()
    print today_date
    data={
        'Dashboard':['Dashboard'],
        'Membership':['Membership Details','Industry Details','Slab','Legal Details','Membership Category',' Executive Committee Member','Valid / Invalid Member','Exclude Mail Member','Top 3 Members','Membership Certificate Dispatched','Membership Registration'],
        'Hall Booking':['Hall Locations','Holidays','Hall Equipments','Manage Halls','Hall Bookings Registrations','Hall Bookings Registrations Report','Internal Hall Booking','Hall Special Announcement'],
        'Event':['Events Details','Events Registrations','Event Special Announcement','Events Participant Report','Delete Events','Delete Events Participants','Event Committees','Event Type'],
        'Administrator':['Country','State','City','Service Tax','User']
    }
    for key, value in data.iteritems():
        # print key, value
        for privilege in value:
            print privilege
            try:
                UserPrivilege.objects.get(module_name=key,privilege=privilege)
            except Exception, e:
                # print e
                userPrivilege = UserPrivilege(
                    privilege=privilege,
                    module_name=key,
                    created_by='admin',
                    created_on=today_date,
                    is_deleted=False,
                )
                userPrivilege.save()
                pass



import traceback
import datetime
from email.mime.image import MIMEImage
from django.http import HttpResponse
from xlrd import open_workbook
from django.db import transaction
from xlrd import xldate_as_tuple

@transaction.atomic
def load_member_data():
    try:
        file_path = ['/home/bynry01/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/demo.xlsx']
        i = 0
        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns
            sid = transaction.savepoint()
            MEMBER_ASSOCIATION_TYPE = {'M': 'Member', 'Associate': 'A', 'L': 'Life Membership'}
            for row in range(1, 7):
            # for row in range(1, number_of_rows):
                row_values = []
                for col in range(68):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)

                print row_values
                print int(row_values[0])

                # try:
                #     """Start:Code to add member HOD Detail"""
                #
                #     hod_detail_obj=HOD_Detail()
                #
                #     hod_detail_obj.hr_name=row_values[8]
                #     # hod_detail_obj.hr_contact=row_values[0]
                #     hod_detail_obj.hr_email=row_values[9]
                #
                #     hod_detail_obj.finance_name = row_values[10]
                #     # hod_detail_obj.finance_contact = row_values[0]
                #     hod_detail_obj.finance_email = row_values[11]
                #
                #     hod_detail_obj.marketing_name = row_values[12]
                #     # hod_detail_obj.marketing_contact = row_values[0]
                #     hod_detail_obj.marketing_email = row_values[13]
                #
                #     hod_detail_obj.IT_name = row_values[14]
                #     # hod_detail_obj.IT_contact = row_values[0]
                #     hod_detail_obj.IT_email = row_values[15]
                #
                #     hod_detail_obj.corp_rel_name = row_values[16]
                #     # hod_detail_obj.corp_rel_contact = row_values[0]
                #     hod_detail_obj.corp_rel_email = row_values[17]
                #
                #     hod_detail_obj.tech_name = row_values[18]
                #     # hod_detail_obj.tech_contact = row_values[0]
                #     hod_detail_obj.tech_email = row_values[19]
                #
                #     hod_detail_obj.rnd_name = row_values[20]
                #     # hod_detail_obj.rnd_contact = row_values[0]
                #     hod_detail_obj.rnd_email = row_values[21]
                #
                #     hod_detail_obj.exim_name = row_values[22]
                #     # hod_detail_obj.exim_contact = row_values[0]
                #     hod_detail_obj.exim_email = row_values[23]
                #
                #     hod_detail_obj.created_by = "Admin"
                #
                #     hod_detail_obj.save()
                #
                #     """End:Code to add member HOD Detail"""
                #     #-----------------------#
                #
                #     """Start:Code to add member Company Detail"""
                #     company_detail_obj=CompanyDetail()
                #
                #     company_detail_obj.company_name=row_values[2]
                #     # company_detail_obj.description_of_business=row_values[0]
                #     company_detail_obj.establish_year=row_values[40]
                #     # company_detail_obj.company_scale=row_values[0]
                #
                #     # company_detail_obj.block_inv_plant=row_values[0]
                #     # company_detail_obj.block_inv_land=row_values[0]
                #     # company_detail_obj.block_inv_total=row_values[0]
                #
                #     #here country is many to many field
                #     company_detail_obj.exportcountry=row_values[43]
                #     company_detail_obj.importcountry=row_values[44]
                #
                #     # company_detail_obj.textexport=row_values[0]
                #     # company_detail_obj.textimport=row_values[0]
                #
                #     company_detail_obj.rnd_facility=row_values[45]
                #     company_detail_obj.govt_recognised=row_values[46]
                #
                #     company_detail_obj.iso = row_values[47]
                #     company_detail_obj.iso_detail = row_values[47]
                #
                #     # company_detail_obj.foreign_collaboration=row_values[0]
                #
                #     company_detail_obj.eou=row_values[49]
                #     company_detail_obj.eou_detail=row_values[49]
                #
                #     company_detail_obj.total_manager=int(row_values[50])
                #     company_detail_obj.total_staff=int(row_values[51])
                #     company_detail_obj.total_workers=int(row_values[52])
                #     # company_detail_obj.total_employees=int(row_values[0])
                #
                #     # here industrydescription is many to many field
                #     company_detail_obj.industrydescription=int(row_values[55])
                #
                #     # here legalstatus is FK field
                #     company_detail_obj.legalstatus = int(row_values[54])
                #
                #     # here hoddetail is FK field
                #     company_detail_obj.hoddetail = hod_detail_obj
                #
                #     company_detail_obj.created_by = 'Admin'
                #
                #     company_detail_obj.save()
                #     """End:Code to add member Company Detail"""
                #
                #     #-------------
                #
                #     """Start:Code to add member User Detail"""
                #     try:
                #         #here first check the user against the membership no
                #         UserDetail.objects.get(member_associate_no=row_values[1])
                #
                #     except UserDetail.DoesNotExist,e:
                #         pass
                #         user_detail_obj=UserDetail()
                #         user_detail_obj.company=company_detail_obj
                #
                #         user_detail_obj.ceo_name=row_values[3]
                #         user_detail_obj.ceo_email=row_values[4]
                #         # user_detail_obj.ceo_designation=row_values[0]
                #         user_detail_obj.ceo_cellno=row_values[5]
                #
                #         user_detail_obj.person_name=row_values[0]
                #         user_detail_obj.person_email=row_values[0]
                #         user_detail_obj.person_designation=row_values[0]
                #         user_detail_obj.person_cellno=row_values[0]
                #
                #         user_detail_obj.correspond_address=row_values[24]
                #         user_detail_obj.correspond_email=row_values[30]
                #         # user_detail_obj.correspondstate=row_values[0]
                #         user_detail_obj.correspondcity=row_values[26]
                #         user_detail_obj.correspond_pincode=row_values[27]
                #         # user_detail_obj.correspond_std1=row_values[28]
                #         # user_detail_obj.correspond_std2=row_values[28]
                #         user_detail_obj.correspond_landline1=row_values[28]
                #         user_detail_obj.correspond_landline2=row_values[28]
                #
                #         user_detail_obj.factory_cellno=row_values[37]
                #         user_detail_obj.factory_address=row_values[33] + ' ' +row_values[34]
                #         # user_detail_obj.factorystate=row_values[0]
                #         user_detail_obj.factorycity=row_values[35]
                #         user_detail_obj.factory_pincode=row_values[36]
                #         # user_detail_obj.factory_std1=row_values[0]
                #         # user_detail_obj.factory_std2=row_values[0]
                #         # user_detail_obj.factory_landline1=row_values[0]
                #         # user_detail_obj.factory_landline2=row_values[0]
                #
                #         user_detail_obj.website=row_values[32]
                #         # user_detail_obj.gst=row_values[0]
                #         # user_detail_obj.gst_in=row_values[0]
                #         # user_detail_obj.pan=row_values[0]
                #         # user_detail_obj.aadhar=row_values[0]
                #         # user_detail_obj.awards=row_values[0]
                #
                #         # user_detail_obj.membership_type=row_values[0]
                #         # user_detail_obj.enroll_type=row_values[0]
                #         # user_detail_obj.user_type=row_values[0]
                #         user_detail_obj.member_associate_no=row_values[1]
                #         user_detail_obj.membership_acceptance_date=row_values[63]
                #         # user_detail_obj.membership_category=row_values[0]
                #         # user_detail_obj.membership_slab=row_values[0]
                #         user_detail_obj.annual_turnover_year=row_values[0]
                #         user_detail_obj.annual_turnover_rupees=row_values[0]
                #         user_detail_obj.membership_year=row_values[0]
                #         user_detail_obj.renewal_year=row_values[0]
                #         user_detail_obj.renewal_status=row_values[0]
                #
                #         #here membership_description is many to many field
                #         user_detail_obj.membership_description=row_values[0]
                #
                #         # user_detail_obj.exclude_from_mailing=row_values[0]
                #         # user_detail_obj.valid_invalid_member=row_values[0]
                #         # user_detail_obj.executive_committee_member=row_values[0]
                #         user_detail_obj.membership_ceritificate_dispatch=row_values[0]
                #         user_detail_obj.payment_method=row_values[0]
                #         user_detail_obj.created_by='Admin'
                #         user_detail_obj.save()
                #
                #
                #
                #
                #     """Start:Code to add member User Detail"""
                #
                # except Exception,e:
                #     print e
                #     pass

    except Exception, e:
        print 'Exception In|Adminapp|Helper.py|load_consumer_data', str(traceback.print_exc())
        # transaction.rollback(sid)
        print 'Exception In|Adminapp|Helper.py|load_consumer_data', e
        return HttpResponse(500)



import hashlib

def check_hash():
    stringResponse='0392|failure|Cancelled_BY_User|12345678901|10|598643003|1.00|{email:test@test.com}{mob:9876543210}|05-09-2018 12:00:00|NA|||||8c2c08fd-e591-4544-bc8c-31f1b14f2aaa|1274238a314dc2023d2599d2105cd9e8b611d6d6197bc707727ce852bf09d6b63fba7a843510ab9b5085df238df8f8fdad23b9a14d5bd8b7b65b9d5bc59b3160'

    salt = '2093514954UVQFBK'

    stringResponse_list = stringResponse.split('|')
    txn_status = stringResponse_list[0]
    txn_msg = stringResponse_list[1]
    txn_err_msg = stringResponse_list[2]
    clnt_txn_ref = stringResponse_list[3]
    tpsl_bank_cd = stringResponse_list[4]
    tpsl_txn_id = stringResponse_list[5]
    txn_amt = stringResponse_list[6]
    clnt_rqst_meta = stringResponse_list[7]
    tpsl_txn_time = stringResponse_list[8]
    bal_amt = stringResponse_list[9]
    card_id = stringResponse_list[10]
    alias_name = stringResponse_list[11]
    BankTransactionID = stringResponse_list[12]
    mandate_reg_no = stringResponse_list[13]
    token = stringResponse_list[14]
    hash = stringResponse_list[15]

    msg = txn_status
    msg += '|' + txn_msg
    msg += '|' + txn_err_msg
    msg += '|' + clnt_txn_ref
    msg += '|' + tpsl_bank_cd
    msg += '|' + tpsl_txn_id
    msg += '|' + txn_amt
    msg += '|' + clnt_rqst_meta
    msg += '|' + tpsl_txn_time
    msg += '|' + bal_amt
    msg += '|' + card_id
    msg += '|' + alias_name
    msg += '|' + BankTransactionID
    msg += '|' + mandate_reg_no
    msg += '|' + token
    msg += '|' + salt

    m = hashlib.sha512()
    m.update(msg)
    hex_msg = m.hexdigest()

    if (hex_msg == hash):
        print "pass"
    else:
        print "failed"


if __name__ == "__main__":
    # add_privilege()
    # new_add_privilege()
    # load_member_data()
    check_hash()
    pass

