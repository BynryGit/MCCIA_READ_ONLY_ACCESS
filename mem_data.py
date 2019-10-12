import os, sys
import pdb

import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()
import re
import traceback
from django.http import HttpResponse
from xlrd import open_workbook
from django.db import transaction
from adminapp.models import *
from membershipapp.models import *
from eventsapp.models import EventDetails
from massmailingapp.models import CompanyDetail as MMCompanyDetail, PersonDetail
from eventsapp.models import EventDetails, EventRegistration, EventParticipantUser
from backofficeapp.models import SystemUserProfile
import datetime
from dateutil import tz
from xlrd import open_workbook, xldate_as_tuple

# Start:Use this for local system
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_dir = BASE_DIR + '/MCCIA_BACKOFFICE/Final_data'
to_zone = tz.gettz('Asia/Kolkata')


# file_dir = BASE_DIR + '/MCCIA_BACKOFFICE/NFinal_data'
# End:Use this for local system

# Start:on server file path
# file_dir='/srv/wsgi/Final_data'
# End:on server file path


def delete_data():
    # IndustryDescription.objects.all().delete()
    # MembershipDescription.objects.all().delete()
    # LegalStatus.objects.all().delete()
    # MembershipCategory.objects.all().delete()
    # MembershipSlab.objects.all().delete()
    # SlabCriteria.objects.all().delete()
    City.objects.all().delete()
    # State.objects.all().delete()
    # Country.objects.all().delete()
    print "ALl data deleted"


"""Start:This code is to match data (industrydescription ,membershipdescription,legal_status) of prashant sir @mccia """
# @transaction.atomic
# def old_add_industrydescription():
#     try:
#         data={
#             'Automobile & Ancillary':'1',
#             'Construction & Allied':'2',
#             'Chemical':'3',
#             'Electrical':'4',
#             'Electronic':'5',
#             'Food Products':'6',
#             'Glass':'7',
#             'Leather':'8',
#             'Machinery & Machine Tools':'9',
#             'Fabrication & Metallic Products':'10',
#             'Mineral Products':'11',
#             'Paper & Printing':'12',
#             'Metallurgical':'13',
#             'Packaging Materials':'14',
#             'Plastic':'15',
#             'Rubber':'16',
#             'Software':'17',
#             'Textile':'18',
#             'Telecommunications':'19',
#             'Transport Equipment':'20',
#             'Wooden':'21',
#             'Other':'22',
#         }
#         sid = transaction.savepoint()
#         for key,value  in data.iteritems():
#             print key ,value
#             try:
#                 IndustryDescription.objects.get(description=key)
#             except IndustryDescription.DoesNotExist, e:
#                 pass
#                 try:
#                     IndustryDescriptionobj=IndustryDescription(description=key,code=value,created_by="Admin")
#                     IndustryDescriptionobj.save()
#                 except Exception,e:
#                     pass
#                     transaction.rollback(sid)
#
#         transaction.savepoint_commit(sid)
#
#     except Exception,e:
#         print e
#         pass
#         transaction.rollback(sid)

# @transaction.atomic
# def old_add_membershipdescription():
#     try:
#         data={
#             'Manufacturer':'1',
#             'Trader':'2',
#             'Exporter':'3',
#             'Educational':'4',
#             'Association':'5',
#             'Professional':'6',
#             'Govt./Semi Govt. Undertaking':'7',
#             'Service Ind.':'8',
#             'Other':'9',
#         }
#         sid = transaction.savepoint()
#         for key,value  in data.iteritems():
#             print key ,value
#             try:
#                 MembershipDescription.objects.get(membership_description=key)
#             except MembershipDescription.DoesNotExist, e:
#                 pass
#                 try:
#                     MembershipDescriptionobj=MembershipDescription(membership_description=key,code=value,created_by="Admin")
#                     MembershipDescriptionobj.save()
#                 except Exception,e:
#                     pass
#                     transaction.rollback(sid)
#
#         transaction.savepoint_commit(sid)
#
#     except Exception,e:
#         print e
#         pass
#         transaction.rollback(sid)


# @transaction.atomic
# def old_add_legal_status():
#     try:
#         data={
#             'Proprietary':'1',
#             'Partnership':'2',
#             'Pvt. Ltd.':'3',
#             'Public Ltd':'4',
#             'Other':'5',
#             'LLP':'6',
#         }
#         sid = transaction.savepoint()
#         for key, value in data.iteritems():
#             print key, value
#             try:
#                 LegalStatus.objects.get(description=key)
#             except LegalStatus.DoesNotExist, e:
#                 pass
#                 try:
#                     LegalStatusobj = LegalStatus(description=key, code=value, created_by="Admin")
#                     LegalStatusobj.save()
#                 except Exception, e:
#                     print e
#                     pass
#                     transaction.rollback(sid)
#
#         transaction.savepoint_commit(sid)
#
#     except Exception,e:
#         pass


"""End:This code is to match data (industrydescription,membershipdescription,legal_status) of prashant sir @mccia"""

"""Start:This code is to add data from table strcture"""


@transaction.atomic
def add_industrydescription():
    try:
        file_path = [file_dir + '/industry_discription.xlsx']
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            value_list = []
            for row in range(1, number_of_rows):
                PKDEscID = int((wb.sheets()[0].cell(row, 0).value))
                Code = int((wb.sheets()[0].cell(row, 1).value))
                Description = (wb.sheets()[0].cell(row, 2).value)
                CreatedBY = int((wb.sheets()[0].cell(row, 3).value))
                ModifiedBY = "NA" if (wb.sheets()[0].cell(row, 5).value) == 'NULL' else int(
                    (wb.sheets()[0].cell(row, 5).value))
                Status = True if (wb.sheets()[0].cell(row, 7).value) == 'Y' else False
                value_list.append([PKDEscID, Code, Description, CreatedBY, ModifiedBY, Status])
        sid = transaction.savepoint()
        for value in value_list:
            try:
                IndustryDescription.objects.get(previous_id=value[0])
            except IndustryDescription.DoesNotExist, e:
                pass
                try:
                    print value
                    IndustryDescriptionobj = IndustryDescription(
                        previous_id=value[0],
                        code=value[1],
                        description=value[2],
                        created_by=value[3],
                        is_active=value[5],
                        is_deleted=not (value[5])
                    )
                    IndustryDescriptionobj.save()
                except Exception, e:
                    print e
                    pass
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)

    except Exception, e:
        print e
        pass
        transaction.rollback(sid)


@transaction.atomic
def add_membershipdescription():
    try:
        file_path = [file_dir + '/membership_description.xlsx']
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            value_dlist = []
            data = {}
            for row in range(1, number_of_rows):
                PKDEscID = int((wb.sheets()[0].cell(row, 0).value))
                Code = int((wb.sheets()[0].cell(row, 1).value))
                Description = (wb.sheets()[0].cell(row, 2).value)
                CreatedBy = int((wb.sheets()[0].cell(row, 3).value))
                ModifiedBY = "NA" if (wb.sheets()[0].cell(row, 5).value) == 'NULL' else int(
                    (wb.sheets()[0].cell(row, 5).value))
                Status = True if (wb.sheets()[0].cell(row, 7).value) == 'Y' else False
                data = {
                    'PKDEscID': PKDEscID,
                    'Code': Code,
                    'Description': Description,
                    'CreatedBy': CreatedBy,
                    'ModifiedBY': ModifiedBY,
                    'Status': Status,
                }
                # value_list.append([PKDEscID, Code, Description, CreatedBy, ModifiedBY, Status])

                value_dlist.append(data)
        sid = transaction.savepoint()
        for valued in value_dlist:
            try:
                MembershipDescription.objects.get(previous_id=valued['PKDEscID'])
            except MembershipDescription.DoesNotExist, e:
                pass
                try:
                    MembershipDescriptionobj = MembershipDescription(
                        previous_id=valued['PKDEscID'],
                        membership_description=valued['Description'],
                        code=valued['Code'],
                        created_by=valued['CreatedBy'],
                        is_active=valued['Status'],
                        is_deleted=not (valued['Status'])
                    )
                    MembershipDescriptionobj.save()
                except Exception, e:
                    pass
                    transaction.rollback(sid)

            except Exception, e:
                print e
                pass
                transaction.rollback(sid)

        transaction.savepoint_commit(sid)
    except Exception, e:
        pass


"""Start:This code is to add data from table strcture"""


@transaction.atomic
def add_legal_status():
    try:
        file_path = [file_dir + '/legal_status.xlsx']
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            value_dlist = []
            data = {}
            for row in range(1, number_of_rows):
                PKDEscID = int((wb.sheets()[0].cell(row, 0).value))
                Code = int((wb.sheets()[0].cell(row, 1).value))
                Description = (wb.sheets()[0].cell(row, 2).value)
                CreatedBy = int((wb.sheets()[0].cell(row, 3).value))
                ModifiedBY = "NA" if (wb.sheets()[0].cell(row, 5).value) == 'NULL' else int(
                    (wb.sheets()[0].cell(row, 5).value))
                Status = True if (wb.sheets()[0].cell(row, 7).value) == 'Y' else False
                data = {
                    'PKDEscID': PKDEscID,
                    'Code': Code,
                    'Description': Description,
                    'CreatedBy': CreatedBy,
                    'ModifiedBY': ModifiedBY,
                    'Status': Status,
                }
                value_dlist.append(data)
        try:
            sid = transaction.savepoint()

            for valued in value_dlist:
                try:
                    LegalStatus.objects.get(previous_id=valued['PKDEscID'])
                except LegalStatus.DoesNotExist, e:
                    pass
                    try:
                        LegalStatusobj = LegalStatus(
                            previous_id=valued['PKDEscID'],
                            description=valued['Description'],
                            code=valued['Code'],
                            created_by=valued['CreatedBy'],
                            is_active=valued['Status'],
                            is_deleted=not (valued['Status']),
                            status=valued['Status']
                        )
                        LegalStatusobj.save()
                    except Exception, e:
                        pass
                        transaction.rollback(sid)

                except Exception, e:
                    print e
                    pass
                    transaction.rollback(sid)
        except Exception, e:
            print e
            pass
            transaction.savepoint_commit(sid)

    except Exception, e:
        pass


def add_mem_categary():
    try:
        file_path = [file_dir + '/membership_categery.xlsx']
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            value_list = []
            for row in range(1, number_of_rows):
                PkCatID = int((wb.sheets()[0].cell(row, 0).value))
                Category = (wb.sheets()[0].cell(row, 1).value)
                CreatedBY = int((wb.sheets()[0].cell(row, 2).value))
                ModifiedBY = "NA" if (wb.sheets()[0].cell(row, 4).value) == 'NULL' else int(
                    (wb.sheets()[0].cell(row, 4).value))
                Status = True if (wb.sheets()[0].cell(row, 6).value) == 'Y' else False
                type = (wb.sheets()[0].cell(row, 7).value)

                value_list.append([PkCatID, Category, CreatedBY, ModifiedBY, Status, type])

            sid = transaction.savepoint()
            try:
                for value in value_list:
                    try:
                        MembershipCategory.objects.get(membership_code=value[0])
                    except MembershipCategory.DoesNotExist, e:
                        pass
                        try:
                            MembershipCategoryobj = MembershipCategory(
                                membership_code=value[0],
                                membership_category=value[1],
                                created_by=value[2],
                                updated_by=value[3],
                                status=value[4],
                                is_deleted=not (value[4]),
                                membership_type=value[5]
                            )
                            MembershipCategoryobj.save()
                        except Exception, e:
                            print e
                            pass
                            transaction.rollback(sid)

                transaction.savepoint_commit(sid)
            except Exception, e:
                print e
                pass
    except Exception, e:
        print e


def add_membershipslab():
    try:
        file_path = [file_dir + '/membership_slab.xlsx']
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            value_list = []
            applicableto = {'M': 'Members', 'A': 'Associates', 'I': 'Individual'}
            for row in range(1, number_of_rows):
                PkSlabID = int((wb.sheets()[0].cell(row, 0).value))
                Slab = (wb.sheets()[0].cell(row, 1).value)
                FKCatID = int((wb.sheets()[0].cell(row, 2).value))
                ApplicableTo = (wb.sheets()[0].cell(row, 3).value)
                AnnualFee = int((wb.sheets()[0].cell(row, 4).value))
                EntranceFee = int((wb.sheets()[0].cell(row, 5).value))
                CreatedBY = "NA" if (wb.sheets()[0].cell(row, 6).value) == 'NULL' else int(
                    (wb.sheets()[0].cell(row, 4).value))
                Status = True if (wb.sheets()[0].cell(row, 10).value) == 'Y' else False
                cr3 = (wb.sheets()[0].cell(row, 11).value)

                value_list.append(
                    [PkSlabID, Slab, FKCatID, ApplicableTo, AnnualFee, EntranceFee, CreatedBY, Status, cr3])

            # print value_list

            sid = transaction.savepoint()
            try:
                for value in value_list:
                    try:
                        MembershipSlab.objects.get(code=value[0])
                    except MembershipSlab.DoesNotExist, e:
                        pass
                        try:
                            MembershipCategoryobj = MembershipCategory.objects.get(membership_code=value[2])
                            try:
                                try:
                                    if value[8] == 'N':
                                        slab_criteria = 'N'
                                    elif value[8] == 'L':
                                        slab_criteria = 'L'
                                    else:
                                        slab_criteria = int(value[8])

                                except Exception, e:
                                    print e
                                    slab_criteria = value[8]

                                SlabCriteriaobj = SlabCriteria.objects.get(slab_criteria=slab_criteria)
                            except SlabCriteria.DoesNotExist, e:
                                SlabCriteriaobj = SlabCriteria(slab_criteria=slab_criteria)
                                SlabCriteriaobj.save()

                            MembershipSlabobj = MembershipSlab(
                                code=value[0],
                                slab=value[1],
                                membershipCategory=MembershipCategoryobj,
                                applicableTo=applicableto[value[3]],
                                annual_fee=value[4],
                                entrance_fee=value[5],
                                created_by=value[6],
                                status=value[7],
                                is_deleted=not (value[7]),
                                cr3=SlabCriteriaobj
                            )
                            MembershipSlabobj.save()
                            # print MembershipSlabobj.id
                        except Exception, e:
                            print e
                            pass
                            transaction.rollback(sid)

                transaction.savepoint_commit(sid)
            except Exception, e:
                print e
                pass
    except Exception, e:
        print e


paymentmethod = {'C': 'Confirmed', 'Y': 'Online Pending', 'P': 'Offline Pending', 'F': 'Failed', 'N': 'Deactivate',
                 'U': 'Offline Pending'}
from decimal import Decimal


@transaction.atomic
def load_member_data():
    try:
        # file_path = ['/home/bynry01/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/a.xlsx']
        file_path = [file_dir + '/final_mem_data.xls']
        i = 0
        user_slab_list = []
        sid = transaction.savepoint()
        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns
            MEMBER_ASSOCIATION_TYPE = {'M': 'Member', 'A': 'Associate', 'L': 'Life Membership', 'I': 'I'}

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(114):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                try:
                    try:
                        user_detail_obj = UserDetail.objects.get(updated_by=int(row_values[0]))
                        try:
                            if row_values[97] != 'NULL':
                                if str(int(row_values[97])) == '2018' or str(int(row_values[97])) == '2017':
                                    MembershipInvoiceobj = MembershipInvoice(
                                        userdetail=user_detail_obj,
                                        membership_category=user_detail_obj.membership_category,
                                        membership_slab=user_detail_obj.membership_slab,
                                        valid_invalid_member=user_detail_obj.valid_invalid_member,
                                        subscription_charges=Decimal(row_values[103]) if row_values[
                                                                                             103] != 'NULL' else 0,
                                        entrance_fees=Decimal(row_values[98]) if row_values[98] != 'NULL' else 0,
                                        tax=Decimal(row_values[99]) if row_values[99] != 'NULL' else 0,
                                        amount_payable=Decimal(row_values[103]) if row_values[103] != 'NULL' else 0,
                                        without_adv_amount_payable=0,
                                        financial_year=str(int(row_values[97])) + '-' + str(int(row_values[97]) + 1),
                                        last_due_amount=Decimal(row_values[102]) if row_values[102] != 'NULL' else 0,
                                        last_advance_amount=Decimal(row_values[101]) if row_values[
                                                                                            101] != 'NULL' else 0,
                                    )

                                    MembershipInvoiceobj.save()

                                    if MembershipInvoice.objects.filter(userdetail=user_detail_obj). \
                                            exclude(
                                        financial_year=str(int(row_values[97])) + '-' + str(int(row_values[97]) + 1)):
                                        MembershipInvoiceobj.invoice_for = 'RENEW'
                                        MembershipInvoiceobj.save()

                                    PaymentDetailsobj = PaymentDetails(
                                        userdetail=user_detail_obj,
                                        membershipInvoice=MembershipInvoiceobj,
                                        amount_payable=Decimal(row_values[100]) if row_values[100] != 'NULL' else 0,
                                        amount_paid=Decimal(row_values[104]) if row_values[104] != 'NULL' else 0,
                                        partial_amount_paid=0,
                                        amount_last_advance=0,
                                        amount_next_advance=0,
                                        cheque_no=row_values[109] if row_values[109] != 'NULL' else 0,
                                        bank_name=row_values[111] if row_values[111] != 'NULL' else '',
                                        receipt_no=row_values[113] if row_values[113] != 'NULL' else '',
                                        neft_transfer_id=0,
                                        cash_amount=0,
                                        financial_year=MembershipInvoiceobj.financial_year,

                                    )
                                    PaymentDetailsobj.save()
                                    try:
                                        payment_mode = row_values[105]
                                        if payment_mode == 'C':
                                            payment_mode = 'Cash'
                                            PaymentDetailsobj.cash_amount = row_values[104] if row_values[
                                                                                                   104] != 'NULL' else 0
                                            PaymentDetailsobj.save()
                                        elif payment_mode == 'Q':
                                            payment_mode = 'Cheque'
                                        else:
                                            payment_mode = 'Cheque'

                                        PaymentDetailsobj.user_Payment_Type = payment_mode

                                    except Exception, e:
                                        pass

                                    PaymentDetailsobj.save()

                                    PaymentDetailsobj.bk_no = 'MBK' + str(PaymentDetailsobj.id).zfill(7)
                                    PaymentDetailsobj.save()
                                    try:
                                        if row_values[110] != 'NULL':
                                            PaymentDetailsobj.cheque_date = (
                                                datetime.datetime.strptime(row_values[110],
                                                                           '%Y-%m-%d %H:%M:%S.%f')).date()
                                    except Exception, e:
                                        print e
                                        pass

                                    try:
                                        if row_values[112] != 'NULL':
                                            PaymentDetailsobj.receipt_date = (
                                                datetime.datetime.strptime(row_values[112],
                                                                           '%Y-%m-%d %H:%M:%S.%f')).date()
                                    except Exception, e:
                                        print e
                                        pass

                                    PaymentDetailsobj.save()

                        except Exception, e:
                            print e
                            traceback.print_exc()
                            pass
                    except UserDetail.DoesNotExist, e:
                        pass
                        company_detail_obj = None
                        """Start:Code to add member Company Detail"""
                        try:
                            company_detail_obj = CompanyDetail()

                            company_detail_obj.company_name = row_values[5]
                            company_detail_obj.establish_year = row_values[23] if row_values[23] != 'YYYY' else 0000

                            company_detail_obj.textexport = row_values[30]
                            company_detail_obj.textimport = row_values[31]

                            company_detail_obj.rnd_facility = True if row_values[32] == 'Y' else False
                            company_detail_obj.govt_recognised = True if row_values[33] == 'Y' else False

                            company_detail_obj.iso = True if row_values[34] else False
                            company_detail_obj.iso_detail = row_values[34]

                            company_detail_obj.eou = True if row_values[36] == 'Y' else False

                            company_detail_obj.total_manager = int(row_values[38]) if row_values[38] else 0
                            company_detail_obj.total_staff = int(row_values[39]) if row_values[39] else 0
                            company_detail_obj.total_workers = int(row_values[40]) if row_values[40] else 0
                            company_detail_obj.total_employees = int(row_values[41]) if row_values[41] else 0
                            company_detail_obj.save()

                            # here industrydescription is many to many field
                            try:
                                if row_values[44] != '':
                                    industrydescription_list = (str(row_values[44])).split(',')
                                    # print "industrydescription_list",industrydescription_list
                                    for list_obj in industrydescription_list:
                                        try:
                                            obj = IndustryDescription.objects.get(previous_id=int(float(list_obj)))
                                            company_detail_obj.industrydescription.add(obj)
                                            company_detail_obj.save()
                                        except Exception, e:
                                            pass
                            except Exception, e:
                                print e
                                # print "--------row_values[44]---------",row_values[44]
                                pass

                            try:
                                if row_values[43] != '':
                                    LegalStatusobj = LegalStatus.objects.get(previous_id=int(row_values[43]))
                                    company_detail_obj.legalstatus = LegalStatusobj
                            except Exception, e:
                                pass

                            company_detail_obj.created_by = 'Admin'

                            company_detail_obj.save()

                            # print "company Added"
                        except Exception, e:
                            print e
                            traceback.print_exc()
                            transaction.rollback(sid)
                        """End:Code to add member Company Detail"""
                        # -------------

                        """Start:Code to add member User Detail"""
                        try:

                            user_detail_obj = UserDetail()
                            user_detail_obj.company = company_detail_obj
                            user_detail_obj.updated_by = int(row_values[0])

                            user_detail_obj.ceo_name = row_values[6]
                            user_detail_obj.ceo_email = row_values[19]

                            user_detail_obj.ceo_cellno = row_values[17]
                            user_detail_obj.correspond_address = row_values[7]
                            user_detail_obj.correspond_email = row_values[20]
                            try:
                                if row_values[9]:
                                    cityobj = City.objects.get(city_name=row_values[9])
                                    user_detail_obj.correspondcity = cityobj
                            except City.DoesNotExist, e:
                                # print e
                                cityobj = City(city_name=row_values[9])
                                cityobj.save()
                                user_detail_obj.correspondcity = cityobj
                            except Exception, e:
                                print e
                                pass

                            user_detail_obj.correspond_pincode = int(row_values[11]) if row_values[11] != '' else ''
                            user_detail_obj.correspond_std1 = row_values[13]
                            user_detail_obj.correspond_std2 = row_values[14]
                            user_detail_obj.website = row_values[22]

                            user_detail_obj.user_type = MEMBER_ASSOCIATION_TYPE[(row_values[3])]
                            user_detail_obj.member_associate_no = row_values[4]
                            """CHECK REQUIRED FORMAT DATE"""
                            user_detail_obj.membership_acceptance_date = datetime.datetime.strptime(row_values[45],
                                                                                                    '%Y-%m-%d %H:%M:%S.%f')

                            """FOREGIN KEY MembershipCategory and MembershipSlab """
                            try:
                                MembershipCategory_obj = MembershipCategory.objects.get(
                                    membership_code=int(row_values[1]))
                                user_detail_obj.membership_category = MembershipCategory_obj
                            except Exception, e:
                                pass

                            try:
                                MembershipSlab_obj = MembershipSlab.objects.get(code=int(row_values[2]))
                                user_detail_obj.membership_slab = MembershipSlab_obj
                            except Exception, e:
                                try:
                                    MembershipSlab_obj = MembershipSlab.objects.get(code=int(row_values[95]))
                                    user_detail_obj.membership_slab = MembershipSlab_obj
                                except Exception, e:
                                    user_slab_list.append(user_detail_obj.id)

                            user_detail_obj.save()
                            try:
                                if row_values[42] != '':
                                    membership_description_list = (str(row_values[42])).split(',')
                                    for list_obj in membership_description_list:
                                        try:
                                            obj = MembershipDescription.objects.get(previous_id=int(float(list_obj)))
                                            user_detail_obj.membership_description.add(obj)
                                            user_detail_obj.save()
                                        except Exception, e:
                                            pass

                            except Exception, e:
                                print e
                                pass
                            try:
                                user_detail_obj.membership_type = 'MM'
                                user_detail_obj.enroll_type = 'CO' if row_values[74] == 'C' else "IN"
                            except Exception, e:
                                print e

                            user_detail_obj.valid_invalid_member = False if row_values[90] == 'I' else True
                            user_detail_obj.payment_method = paymentmethod[row_values[56]]
                            if paymentmethod[row_values[56]] == 'Deactivate':
                                user_detail_obj.is_deleted = True

                            user_detail_obj.annual_turnover_year = row_values[26]
                            user_detail_obj.annual_turnover_rupees = row_values[25]
                            user_detail_obj.membership_year = str(int(row_values[46])) + '-' + str(
                                int(row_values[46]) + 1) if str(row_values[46]) != 'NULL' else '2026-2027'
                            user_detail_obj.renewal_year = ''
                            user_detail_obj.renewal_status = "NOT_STARTED"
                            user_detail_obj.created_by = 'Admin'
                            user_detail_obj.save()
                        except Exception, e:
                            traceback.print_exc()
                            print e
                            raise

                        # print "user Added"

                        """End:Code to add member User Detail"""

                        """Start:Code to create user login credential"""
                        try:
                            if row_values[57]:
                                if row_values[57] != '':
                                    try:
                                        MembershipUser.objects.get(username=row_values[4])
                                    except MembershipUser.DoesNotExist, e:
                                        # print e

                                        try:
                                            MembershipUserobj = MembershipUser(
                                                userdetail=user_detail_obj,
                                                username=row_values[4],
                                                created_by='Admin'
                                            )
                                            MembershipUserobj.save()
                                            MembershipUserobj.set_password(row_values[57])
                                            MembershipUserobj.save()
                                            # print "MembershipUser Added"
                                        except Exception, e:
                                            print e
                                            pass
                                    except Exception, e:
                                        print e
                                        pass
                        except Exception, e:
                            print e
                            traceback.print_exc()
                            pass
                        """End:Code to create user login credential"""

                        """Start:Code to add MembershipInvoice & PaymentDetails"""
                        try:
                            # Add total amount colmn in table
                            # print row_values[97]
                            if row_values[97] != 'NULL':
                                if str(int(row_values[97])) == '2018' or str(int(row_values[97])) == '2017':
                                    MembershipInvoiceobj = MembershipInvoice(
                                        userdetail=user_detail_obj,
                                        membership_category=user_detail_obj.membership_category,
                                        membership_slab=user_detail_obj.membership_slab,
                                        valid_invalid_member=user_detail_obj.valid_invalid_member,
                                        subscription_charges=Decimal(row_values[103]) if row_values[
                                                                                             103] != 'NULL' else 0,
                                        entrance_fees=Decimal(row_values[98]) if row_values[98] != 'NULL' else 0,
                                        tax=Decimal(row_values[99]) if row_values[99] != 'NULL' else 0,
                                        amount_payable=Decimal(row_values[103]) if row_values[103] != 'NULL' else 0,
                                        without_adv_amount_payable=0,
                                        financial_year=str(int(row_values[97])) + '-' + str(int(row_values[97]) + 1),
                                        last_due_amount=Decimal(row_values[102]) if row_values[102] != 'NULL' else 0,
                                        last_advance_amount=Decimal(row_values[101]) if row_values[
                                                                                            101] != 'NULL' else 0,
                                    )

                                    MembershipInvoiceobj.save()

                                    if MembershipInvoice.objects.filter(userdetail=user_detail_obj). \
                                            exclude(
                                        financial_year=str(int(row_values[97])) + '-' + str(int(row_values[97]) + 1)):
                                        MembershipInvoiceobj.invoice_for = 'RENEW'
                                        MembershipInvoiceobj.save()

                                    PaymentDetailsobj = PaymentDetails(
                                        userdetail=user_detail_obj,
                                        membershipInvoice=MembershipInvoiceobj,
                                        amount_payable=Decimal(row_values[100]) if row_values[100] != 'NULL' else 0,
                                        amount_paid=Decimal(row_values[104]) if row_values[104] != 'NULL' else 0,
                                        partial_amount_paid=0,
                                        amount_last_advance=0,
                                        amount_next_advance=0,
                                        cheque_no=row_values[109] if row_values[109] != 'NULL' else 0,
                                        bank_name=row_values[111] if row_values[111] != 'NULL' else '',
                                        receipt_no=row_values[113] if row_values[113] != 'NULL' else '',
                                        neft_transfer_id=0,
                                        cash_amount=0,
                                        financial_year=MembershipInvoiceobj.financial_year,

                                    )
                                    PaymentDetailsobj.save()
                                    try:
                                        payment_mode = row_values[105]
                                        if payment_mode == 'C':
                                            payment_mode = 'Cash'
                                            PaymentDetailsobj.cash_amount = row_values[104] if row_values[
                                                                                                   104] != 'NULL' else 0
                                            PaymentDetailsobj.save()
                                        elif payment_mode == 'Q':
                                            payment_mode = 'Cheque'
                                        else:
                                            payment_mode = 'Cheque'

                                        PaymentDetailsobj.user_Payment_Type = payment_mode

                                    except Exception, e:
                                        pass

                                    PaymentDetailsobj.save()

                                    PaymentDetailsobj.bk_no = 'MBK' + str(PaymentDetailsobj.id).zfill(7)
                                    PaymentDetailsobj.save()
                                    try:
                                        if row_values[110] != 'NULL':
                                            cheque_date = row_values[110]
                                            cheque_date = (cheque_date.split(' '))[0]
                                            # year, month, day ,hour, minute, second= xldate_as_tuple(int(Bkdate), 0)
                                            cheque_date = datetime.datetime.strptime(cheque_date, '%Y-%m-%d').date()
                                            PaymentDetailsobj.cheque_date = cheque_date
                                    except Exception, e:
                                        print e
                                        transaction.rollback(sid)
                                        pass

                                    try:
                                        if row_values[112] != 'NULL':
                                            receipt_date = row_values[112]
                                            receipt_date = (receipt_date.split(' '))[0]
                                            receipt_date = datetime.datetime.strptime(receipt_date, '%Y-%m-%d').date()
                                            PaymentDetailsobj.receipt_date = receipt_date
                                    except Exception, e:
                                        print e
                                        transaction.rollback(sid)
                                        pass

                                    PaymentDetailsobj.save()

                        except Exception, e:
                            print e
                            traceback.print_exc()
                            pass

                        """End:Code to add MembershipInvoice & PaymentDetails"""
                except Exception, e:
                    print e
                    pass
                    transaction.rollback(sid)

            transaction.savepoint_commit(sid)


    except Exception, e:
        print e
        traceback.print_exc()
        transaction.rollback(sid)
        print 'Exception In|Adminapp|Helper.py|load_consumer_data', str(traceback.print_exc())
        # transaction.rollback(sid)
        print 'Exception In|Adminapp|Helper.py|load_consumer_data', e
        return HttpResponse(500)


# Update Category
@transaction.atomic
def update_category_data():
    sid = transaction.savepoint()
    try:
        cat_obj = MembershipCategory()

        for mem_data in UserDetail.objects.all():
            if mem_data.enroll_type == 'CO':
                if mem_data.user_type == 'Associate':
                    try:
                        cat_obj = MembershipCategory.objects.get(
                            membership_category='Industry / Trade Association' if mem_data.membership_category.membership_category == 'Trade Association' else str(
                                mem_data.membership_category.membership_category),
                            category_enroll_type='Organizational',
                            enroll_type='Annual')
                        # print cat_obj.membership_category
                    except Exception, e:
                        pass
                elif mem_data.user_type == 'Member':
                    try:
                        cat_obj = MembershipCategory.objects.get(
                            membership_category='Industry / Trade Association' if mem_data.membership_category.membership_category == 'Trade Association' else str(
                                mem_data.membership_category.membership_category),
                            category_enroll_type='Organizational',
                            enroll_type='Annual')
                        # print cat_obj.membership_category
                    except Exception, e:
                        pass
                elif mem_data.user_type == 'Life Membership':
                    try:
                        cat_obj = MembershipCategory.objects.get(
                            membership_category='Industry / Trade Association' if mem_data.membership_category.membership_category == 'Trade Association' else str(
                                mem_data.membership_category.membership_category),
                            category_enroll_type='Organizational',
                            enroll_type='Life Membership')
                        # print cat_obj.membership_category
                    except Exception, e:
                        pass
            else:
                if mem_data.user_type == 'Associate':
                    try:
                        cat_obj = MembershipCategory.objects.get(
                            membership_category='Industry / Trade Association' if mem_data.membership_category.membership_category == 'Trade Association' else str(
                                mem_data.membership_category.membership_category),
                            category_enroll_type='Individual',
                            enroll_type='Annual')
                        # print cat_obj.membership_category
                    except Exception, e:
                        pass
                elif mem_data.user_type == 'Member':
                    try:
                        cat_obj = MembershipCategory.objects.get(
                            membership_category='Industry / Trade Association' if mem_data.membership_category.membership_category == 'Trade Association' else str(
                                mem_data.membership_category.membership_category),
                            category_enroll_type='Individual',
                            enroll_type='Annual')
                        # print cat_obj.membership_category
                    except Exception, e:
                        pass
                elif mem_data.user_type == 'Life Membership':
                    try:
                        cat_obj = MembershipCategory.objects.get(
                            membership_category='Industry / Trade Association' if mem_data.membership_category.membership_category == 'Trade Association' else str(
                                mem_data.membership_category.membership_category),
                            category_enroll_type='Individual',
                            enroll_type='Life Membership')
                        # print cat_obj.membership_category
                    except Exception, e:
                        pass

            mem_data.membership_category = cat_obj
            mem_data.save()
        transaction.savepoint_commit(sid)
        print '\nCategory Updated'
    except Exception, e:
        print 'exce = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


# Update Slab & Slab Criteria
@transaction.atomic
def update_member_data():
    sid = transaction.savepoint()
    try:
        # file_path = [file_dir +'/Category_Wise_Slab/Trader.xlsx']
        # no_found_obj_list = []
        # value_list = []
        # for file in file_path:
        #     wb = open_workbook(file)
        #     number_of_rows = wb.sheets()[0].nrows
        #     for row in range(1, number_of_rows):
        #         old_slab_id = int((wb.sheets()[0].cell(row, 0).value))
        #         new_slab_id = int((wb.sheets()[0].cell(row, 9).value))
        #         value_list.append([old_slab_id, new_slab_id])

        # for value in value_list:
        #     try:
        #         old_slab_obj = MembershipSlab.objects.get(id=value[0])
        #         old_slab_obj.updated_by = int(value[1])
        #         old_slab_obj.save()
        #     except MembershipSlab.DoesNotExist, e:
        #         pass
        #         print '\nexcp = ', e

        # for item in MembershipSlab.objects.filter(updated_by__isnull=False):
        #     new_slab_obj = MembershipSlab.objects.get(id=int(item.updated_by))
        #     for user_obj in UserDetail.objects.filter(membership_slab=item):
        #         user_obj.membership_slab = new_slab_obj
        #         user_obj.save()
        # new_slab_obj = MembershipSlab.objects.get(id=570)
        # for user_obj in UserDetail.objects.filter(membership_slab_id=440):
        #     user_obj.membership_slab = new_slab_obj
        #     user_obj.save()
        #     user_obj.membership_category = user_obj.membership_slab.membershipCategory
        #     user_obj.save()

        file_path = [file_dir + '/2018_payment_data.xlsx']
        # file_path = ['/home/admin12/Downloads/Final_Dump_Dimakkh_System_mem_hall_copy/2017_payment_data.xlsx']
        i = 0
        user_slab_list = []
        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns
            MEMBER_ASSOCIATION_TYPE = {'M': 'Member', 'A': 'Associate', 'L': 'Life Membership', 'I': 'I'}

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(114):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                try:
                    if str(row_values[4]) and str(row_values[4]) != 'NULL':
                        user_detail_obj_list = UserDetail.objects.filter(member_associate_no=str(row_values[4]))
                        if user_detail_obj_list:
                            for i in user_detail_obj_list:
                                invoice_obj_list = MembershipInvoice.objects.filter(userdetail=i,
                                                                                    financial_year='2018-2019')
                                if invoice_obj_list:
                                    for item in invoice_obj_list:
                                        item.amount_payable = Decimal(str(row_values[103]))
                                        item.save()
                                        payment_obj_list = PaymentDetails.objects.get(userdetail=i,
                                                                                      membershipInvoice=item,
                                                                                      financial_year='2018-2019')
                                        payment_obj_list.amount_payable = item.amount_payable
                                        input_date = str(row_values[96]).split(' ')[0]
                                        formatted_payment_date = datetime.datetime.strptime(input_date,
                                                                                            '%Y-%m-%d').date()
                                        payment_obj_list.payment_date = formatted_payment_date
                                        payment_obj_list.save()

                                        if item.amount_payable == payment_obj_list.amount_paid:
                                            payment_obj_list.payment_received_status = 'Paid'
                                            item.is_paid = True
                                            payment_obj_list.save()
                                            item.save()

                        # print '\nMember Found'
                        # invoice_obj_list = MembershipInvoice.objects.filter(userdetail=user_detail_obj, financial_year='2017-2018')
                        # invoice_obj = ''
                        # if invoice_obj_list.count() >= 1:
                        #     invoice_obj = MembershipInvoice.objects.filter(userdetail=user_detail_obj,
                        #                                                         financial_year='2017-2018').last()
                        # payment_obj = PaymentDetails.objects.get(userdetail=user_detail_obj, membershipInvoice=invoice_obj,
                        #                                          financial_year='2017-2018')
                        # print '\nInvoice & Payment Obj Found'
                        # invoice_obj.amount_payable = Decimal(str(row_values[103]))
                        # invoice_obj.save()
                        # payment_obj.amount_payable = invoice_obj.amount_payable
                        # input_date = str(row_values[96]).split(' ')[0]
                        # formatted_payment_date = datetime.datetime.strptime(input_date, '%Y-%m-%d').date()
                        # payment_obj.payment_date = formatted_payment_date
                        # payment_obj.save()
                        # print '\nInvoice & Payment Updated'
                        #
                        # if invoice_obj.amount_payable == payment_obj.amount_paid:
                        #     payment_obj.payment_received_status = 'Paid'
                        #     invoice_obj.is_paid = True
                        #     payment_obj.save()
                        #     invoice_obj.save()
                        #     print '\nPayment Details updated'
                except UserDetail.DoesNotExist, e:
                    print '\n', e
                    pass
                except Exception, e:
                    print e
                    print str(row_values[4])
                    transaction.rollback(sid)
        transaction.savepoint_commit(sid)
        print '\ndone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def update_company_scale():
    sid = transaction.savepoint()
    try:
        i = 1
        for member_obj in UserDetail.objects.filter(membership_slab__isnull=False):
            if member_obj.user_type != 'Life Membership':
                if member_obj.membership_slab.applicableTo == 'Associates':
                    if int(member_obj.membership_slab.annual_fee) <= 7800:
                        member_obj.company.company_scale = 'MR'
                    elif int(member_obj.membership_slab.annual_fee) > 7800 and int(
                            member_obj.membership_slab.annual_fee) <= 23500:
                        member_obj.company.company_scale = 'SM'
                    elif int(member_obj.membership_slab.annual_fee) > 23500 and int(
                            member_obj.membership_slab.annual_fee) <= 31500:
                        member_obj.company.company_scale = 'MD'
                elif member_obj.membership_slab.applicableTo == 'Members':
                    if int(member_obj.membership_slab.annual_fee) <= 8500:
                        member_obj.company.company_scale = 'MR'
                    elif int(member_obj.membership_slab.annual_fee) > 8500 and int(
                            member_obj.membership_slab.annual_fee) <= 35000:
                        member_obj.company.company_scale = 'SM'
                    elif int(member_obj.membership_slab.annual_fee) > 35000 and int(
                            member_obj.membership_slab.annual_fee) < 54000:
                        member_obj.company.company_scale = 'MD'
                    elif int(member_obj.membership_slab.annual_fee) == 54000:
                        member_obj.company.company_scale = 'LR'
            else:
                if member_obj.enroll_type == 'IN':
                    if re.search('ltd', str(member_obj.company.company_name), re.IGNORECASE) or re.search('limited',
                                                                                                          str(
                                                                                                                  member_obj.company.company_name),
                                                                                                          re.IGNORECASE):
                        member_obj.company.company_scale = 'LR'
                    else:
                        member_obj.company.company_scale = 'MR'
                else:
                    member_obj.company.company_scale = 'LR'

            # member_obj.save()
            member_obj.company.save()
            print 'Updated = ', str(
                member_obj.company.company_name).strip(), member_obj.membership_slab.annual_fee, member_obj.company.company_scale
            i = i + 1
        transaction.savepoint_commit(sid)
        print '\ndone = ', i
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def update_city_data():
    sid = transaction.savepoint()
    try:
        file_path = [file_dir + '/final_mah_city_data.xlsx']
        i = 0
        user_slab_list = []
        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            company_name_list = []
            count_var_user = 0
            count_var_city = 0
            for row in range(1, number_of_rows):
                row_values = []
                for col in range(6):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                try:
                    user_obj_list = UserDetail.objects.filter(member_associate_no=str(row_values[0]).strip())
                    city_obj_list = City.objects.filter(city_name=str(row_values[4]).strip(), created_by='admin')
                    if city_obj_list or city_obj_list.count() > 1:
                        count_var_city = count_var_city + 1
                        city_obj = City.objects.filter(city_name=str(row_values[4]).strip(), created_by='admin').first()
                        state_obj = State.objects.get(id=city_obj.state.id)
                        if user_obj_list:
                            count_var_user = count_var_user + 1
                            for user in user_obj_list:
                                user.correspondcity = city_obj
                                user.correspondstate = state_obj
                                user.save()
                except Exception, e:
                    print e
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\ndone'
        print '\nupdated user count = ', count_var_user
        print '\nupdated city count = ', count_var_city
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def insert_data():
    sid = transaction.savepoint()
    try:
        # file_path = [file_dir +'/Shubham_Data_Format.xlsx']
        # file_path = ['/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/Data_Check_Update/updated_new_18-19_member_add.xlsx']
        file_path = ['/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/New_Member_Files/MISSING.xlsx']
        # file_path = [file_dir +'/New_Member_Files/2018_DEC_29_New_Members.xlsx']
        # file_path = ['/home/admin12/Test_project/Membership/2018_DEC_29_New_Members.xlsx']
        # file_path = ['/home/admin12/Test_project/Membership/MISSING.xlsx']
        i = 0
        user_slab_list = []
        for file in file_path:
            wb = open_workbook(file)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            i = 1
            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)

                # print row_values
                # return

                try:
                    # for i in row_values:
                    #     print i
                    # print '\n1 = ',str(row_values[42]).strip()
                    # print '\n2 = ',row_values[53],row_values[54],row_values[55]
                    # print '\nconverted = ', int(float(row_values[53]))
                    try:
                        member_obj_list = UserDetail.objects.filter(member_associate_no=str(row_values[3]).strip())
                        for member_obj in member_obj_list:
                            MembershipUser.objects.filter(userdetail=member_obj).delete()
                            PaymentDetails.objects.filter(userdetail=member_obj).delete()
                            MembershipInvoice.objects.filter(userdetail=member_obj).delete()
                            if member_obj.company.hoddetail:
                                member_obj.company.hoddetail.delete()
                            member_obj.company.delete()
                            member_obj.delete()
                        if member_obj_list:
                            print 'Exists & Deleted'
                        a = 2 / 0
                    except Exception, e:
                        company_obj = CompanyDetail(company_name=str(row_values[4]).strip(),
                                                    establish_year=int(float(str(row_values[42]).strip())) if
                                                    row_values[42] else 0,
                                                    block_inv_plant=0, block_inv_land=0, block_inv_total=0,
                                                    rnd_facility=False, govt_recognised=False,
                                                    foreign_collaboration=False, eou=False,
                                                    total_manager=int(float(row_values[53])) if row_values[53] else 0,
                                                    total_staff=int(float(row_values[54])) if row_values[54] else 0,
                                                    total_workers=int(float(row_values[55])) if row_values[55] else 0,
                                                    total_employees=int(float(row_values[53])) if row_values[
                                                        53] else 0 + int(
                                                        float(row_values[54])) if row_values[54] else 0 + int(
                                                        float(row_values[55])) if row_values[55] else 0,
                                                    created_by='new_member', updated_by='march_18')
                        company_obj.save()

                        if row_values[123]:
                            industry_list = row_values[123].split(',')
                            print '\nindustry_list = ', industry_list, len(industry_list)
                            if len(industry_list) > 1:
                                for industry_text in industry_list:
                                    print str(industry_text).strip()
                                    industry_obj = IndustryDescription.objects.get(
                                        description=str(industry_text).strip(),
                                        is_active=True, is_deleted=False)
                                    company_obj.industrydescription.add(industry_obj)
                            else:
                                industry_obj = IndustryDescription.objects.get(
                                    description=str(industry_list[0]).strip(),
                                    is_active=True, is_deleted=False)
                                company_obj.industrydescription.add(industry_obj)

                        legal_obj = LegalStatus.objects.get(description=row_values[124], is_active=True,
                                                            is_deleted=False)
                        company_obj.legalstatus = legal_obj
                        company_obj.save()

                        user_obj = UserDetail(company=company_obj, ceo_name=str(row_values[5]).strip(),
                                              ceo_email=str(row_values[6]).strip(),
                                              ceo_cellno=int(float(row_values[7])) if row_values[7] and row_values[
                                                  7] > 0 else None,
                                              correspond_address=str(row_values[26]).strip() + ' ' + str(
                                                  row_values[27]).strip(),
                                              correspond_email=str(row_values[32]).strip(),
                                              correspond_pincode=str(int(float(row_values[29]))).strip() if row_values[
                                                  29] else None,
                                              person_email=str(row_values[33]).strip(),
                                              website=str(row_values[34]).strip() if row_values[34] else '',
                                              factory_address=str(row_values[35]).strip() + ' ' + str(
                                                  row_values[36]).strip(),
                                              factory_pincode=str(int(float(row_values[38]))).strip() if row_values[
                                                  38] else None,
                                              membership_acceptance_date=datetime.datetime.strptime(
                                                  str(row_values[69]).strip(),
                                                  '%d/%m/%Y').date())
                        user_obj.save()

                        if len(str(row_values[30]).strip()) == 10:
                            user_obj.correspond_cellno = int(str(row_values[30]).strip())
                        elif str(row_values[30]).strip():
                            temp_cont_list = str(row_values[30]).split('-')
                            if len(temp_cont_list) > 1:
                                # print str(row_values[30]).strip()
                                # print temp_cont_list
                                user_obj.correspond_std1 = int(temp_cont_list[0])
                                user_obj.correspond_landline1 = int(temp_cont_list[1])
                            else:
                                user_obj.correspond_landline1 = str(row_values[30]).strip()

                        if len(str(row_values[39]).strip()) == 10:
                            user_obj.factory_cellno = str(row_values[30]).strip()
                        elif str(row_values[39]).strip():
                            temp_cont_list = str(row_values[30]).split('-')
                            if len(temp_cont_list) > 1:
                                user_obj.factory_std1 = int(temp_cont_list[0])
                                user_obj.factory_landline1 = int(temp_cont_list[1])
                            else:
                                user_obj.factory_landline1 = str(row_values[39]).strip()

                        user_obj.save()

                        if str(row_values[28]).strip():
                            user_obj.correspondcity = City.objects.filter(city_name=str(row_values[28]).strip(),
                                                                          created_by='admin', is_active=True,
                                                                          is_deleted=False).first()
                        if str(row_values[37]).strip():
                            user_obj.factorycity = City.objects.filter(city_name=str(row_values[37]).strip(),
                                                                       created_by='admin', is_active=True,
                                                                       is_deleted=False).first()
                        user_obj.save()

                        if user_obj.correspondcity:
                            user_obj.correspondstate = user_obj.correspondcity.state
                        elif user_obj.factorycity:
                            user_obj.factorystate = user_obj.factorycity.state
                        user_obj.save()

                        user_obj.user_type = 'Associate'
                        if row_values[115].strip() == 'Life Membership':
                            user_obj.user_type = 'Life Membership'
                        if str(row_values[116]).strip() == 'Organizational':
                            user_obj.enroll_type = 'CO'
                            print '\nCompany'
                        else:
                            user_obj.enroll_type = 'IN'
                            print '\nIndividual'

                        user_obj.member_associate_no = str(row_values[3]).strip()
                        user_obj.membership_year = '2018-2019'
                        user_obj.valid_invalid_member = True
                        user_obj.payment_method = 'Confirmed'
                        user_obj.created_by = 'admin'
                        user_obj.save()

                        print row_values[117]
                        print row_values[116]
                        category_obj = MembershipCategory.objects.get(membership_category=row_values[117],
                                                                      created_by='admin',
                                                                      enroll_type=row_values[115],
                                                                      category_enroll_type=str(row_values[116]).strip())
                        print category_obj.membership_category
                        # for slab in MembershipSlab.objects.filter(membershipCategory=category_obj, created_by='admin'):
                        #     print slab.applicableTo
                        #     print slab.annual_fee
                        #     print slab.entrance_fee

                        slab_obj = MembershipSlab.objects.get(membershipCategory=category_obj, created_by='admin',
                                                              applicableTo=str(row_values[118]),
                                                              annual_fee=str(int(float(row_values[119]))),
                                                              entrance_fee=str(int(float(row_values[120]))))

                        user_obj.membership_category = category_obj
                        user_obj.membership_slab = slab_obj
                        if str(slab_obj.cr3.slab_criteria).split('-')[0] != 'NA':
                            if str(slab_obj.cr3.slab_criteria) == '0-0.50':
                                user_obj.annual_turnover_rupees = 0.05
                            else:
                                user_obj.annual_turnover_rupees = int(str(slab_obj.cr3.slab_criteria).split('-')[0])
                        else:
                            user_obj.annual_turnover_rupees = 'NA'
                        user_obj.save()

                        if str(row_values[130]).strip():
                            user_obj.gst = str(row_values[130]).strip()
                            user_obj.gst_in = 'AP'
                            user_obj.save()
                        else:
                            user_obj.gst_in = 'NA'
                            user_obj.save()

                        # if str(row_values[3]).strip() == 'B-0034':
                        #     invoice_obj = MembershipInvoice(userdetail=user_obj,
                        #                                     membership_category=user_obj.membership_category,
                        #                                     membership_slab=user_obj.membership_slab,
                        #                                     valid_invalid_member=True,
                        #                                     subscription_charges=Decimal(300000),
                        #                                     entrance_fees=Decimal(str(row_values[109])),
                        #                                     tax=Decimal(54000),
                        #                                     amount_payable=Decimal(354000),
                        #                                     financial_year='2018-2019', is_paid=True,
                        #                                     created_by='admin')
                        #     invoice_obj.save()

                        #     payment_obj = PaymentDetails(userdetail=user_obj, membershipInvoice=invoice_obj,
                        #                                  amount_payable=invoice_obj.amount_payable,
                        #                                  amount_paid=Decimal(354000),
                        #                                  financial_year='2018-2019', created_by='admin',
                        #                                  payment_received_status='Paid')
                        #     payment_obj.save()

                        #     if str(row_values[126]).strip() == 'NEFT':
                        #         payment_obj.user_Payment_Type = 'NEFT'
                        #     elif str(row_values[126]).strip() == 'Cash':
                        #         payment_obj.user_Payment_Type = 'Cash'
                        #         payment_obj.cash_amount = payment_obj.amount_paid
                        #     elif str(row_values[126]).strip() == 'Online':
                        #         payment_obj.user_Payment_Type = 'Online'
                        #     else:
                        #         payment_obj.user_Payment_Type = 'Cheque'
                        #         payment_obj.cheque_no = int(float(row_values[127]))
                        #         payment_obj.cheque_date = datetime.datetime.strptime(str(row_values[128]).strip(),
                        #                                                              '%d/%m/%Y').date()
                        #         payment_obj.bank_name = str(row_values[129]).strip()
                        #     payment_obj.save()

                        #     bk_no = 'MBK' + str(payment_obj.id).zfill(7)
                        #     payment_obj.bk_no = str(bk_no)
                        #     payment_obj.payment_date = datetime.datetime.strptime(str(row_values[69]).strip(), '%d/%m/%Y').date()
                        #     payment_obj.save()
                        # else:
                        invoice_obj = MembershipInvoice(userdetail=user_obj,
                                                        membership_category=user_obj.membership_category,
                                                        membership_slab=user_obj.membership_slab,
                                                        valid_invalid_member=True,
                                                        subscription_charges=Decimal(str(row_values[107])),
                                                        # subscription_charges=Decimal(300000),
                                                        entrance_fees=Decimal(str(row_values[109])),
                                                        tax=Decimal(str(row_values[110])),
                                                        # tax=Decimal(54000),
                                                        amount_payable=Decimal(str(row_values[107])) + Decimal(
                                                            str(row_values[109])) + Decimal(str(row_values[110])),
                                                        # amount_payable=Decimal(354000),
                                                        financial_year='2018-2019', is_paid=True, created_by='admin')
                        invoice_obj.save()

                        payment_obj = PaymentDetails(userdetail=user_obj, membershipInvoice=invoice_obj,
                                                     amount_payable=invoice_obj.amount_payable,
                                                     amount_paid=invoice_obj.amount_payable,
                                                     # amount_paid=Decimal(177000),
                                                     # amount_due=Decimal(354000)-Decimal(177000),
                                                     financial_year='2018-2019', created_by='admin',
                                                     payment_received_status='Paid')
                        payment_obj.save()

                        if str(row_values[126]).strip() == 'NEFT':
                            payment_obj.user_Payment_Type = 'NEFT'
                        elif str(row_values[126]).strip() == 'Cash':
                            payment_obj.user_Payment_Type = 'Cash'
                            payment_obj.cash_amount = payment_obj.amount_paid
                        elif str(row_values[126]).strip() == 'Online':
                            payment_obj.user_Payment_Type = 'Online'
                        else:
                            payment_obj.user_Payment_Type = 'Cheque'
                            payment_obj.cheque_no = int(float(row_values[127]))
                            payment_obj.cheque_date = datetime.datetime.strptime(str(row_values[128]).strip(),
                                                                                 '%d/%m/%Y').date()
                            payment_obj.bank_name = str(row_values[129]).strip()
                        payment_obj.save()

                        bk_no = 'MBK' + str(payment_obj.id).zfill(7)
                        payment_obj.bk_no = str(bk_no)
                        payment_obj.payment_date = datetime.datetime.strptime(str(row_values[69]).strip(),
                                                                              '%d/%m/%Y').date()
                        payment_obj.save()

                        # For LF
                        # if invoice_obj.amount_payable != payment_obj.amount_paid:
                        #     new_payment_obj = PaymentDetails(userdetail=user_obj, membershipInvoice=invoice_obj,
                        #                                  amount_payable=invoice_obj.amount_payable - payment_obj.amount_paid,
                        #                                  # amount_paid=invoice_obj.amount_payable,
                        #                                  # amount_paid=Decimal(177000),
                        #                                  financial_year='2018-2019', created_by='admin',
                        #                                  payment_received_status='UnPaid')
                        #     new_payment_obj.save()

                        # MembershipUser.objects.get(username=str(user_obj.member_associate_no).strip()).delete()
                        user_login_obj = MembershipUser(userdetail=user_obj, created_by='admin',
                                                        username=str(user_obj.member_associate_no).strip())
                        user_login_obj.save()
                        user_login_obj.set_password('mccia@test')
                        user_login_obj.save()

                        print '\nAdded = ', user_obj.member_associate_no, i
                        i = i + 1
                        pass
                except Exception, e:
                    print '\nInner Exception = ', str(traceback.print_exc()), row_values
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\ndone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def add_city_state_data():
    sid = transaction.savepoint()
    try:
        file_path = [file_dir + '/No_Tel_Andhra_City.xlsx']
        i = 0
        user_slab_list = []
        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            company_name_list = []
            count_var_user = 0
            count_var_city = 0
            for row in range(1, number_of_rows):
                row_values = []
                for col in range(3):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                try:
                    print row_values
                    try:
                        state_obj = State.objects.get(state_name=str(row_values[2]).strip())
                        new_city = City(city_name=str(row_values[1]).strip(),
                                        state=state_obj, created_by='admin')
                        new_city.save()
                    except Exception, e:
                        new_state = State(state_name=str(row_values[2]).strip(),
                                          country_id=561, created_by='admin')
                        new_state.save()
                        new_city = City(city_name=str(row_values[1]).strip(),
                                        state=new_state, created_by='admin')
                        new_city.save()
                        pass
                except Exception, e:
                    print e
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\ndone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


def delete_mem_data():
    CompanyDetail.objects.all().delete()
    UserDetail.objects.all().delete()
    MembershipUser.objects.all().delete()
    MembershipInvoice.objects.all().delete()
    PaymentDetails.objects.all().delete()


def check_inds():
    IndustryDescriptionobj = IndustryDescription.objects.get(previous_id=12)
    print IndustryDescriptionobj


@transaction.atomic
def check_cat_slab():
    sid = transaction.savepoint()
    try:
        file_path = [
            '/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/Data_Check_Update/update_in_system_131_updated.xlsx']
        i = 0
        user_slab_list = []
        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            company_name_list = []
            count_var_user = 0
            count_var_city = 0
            i = 1
            for row in range(2, number_of_rows):
                row_values = []
                for col in range(123):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                # print row_values,
                # return
                try:
                    # Check if Member already exists
                    try:
                        user_detail_obj = UserDetail.objects.get(member_associate_no=str(row_values[2]).strip())
                        print 'Exists = ', '\t', row_values[2]
                        pass
                    except Exception, e:
                        print 'Not Exists = ', '\t', row_values[2]
                        company_obj = CompanyDetail(company_name=str(row_values[3]).strip(),
                                                    establish_year=row_values[41] if row_values[41] else 0,
                                                    block_inv_plant=row_values[42] if row_values[42] else 0,
                                                    block_inv_land=0,
                                                    block_inv_total=row_values[42] if row_values[42] else 0,
                                                    rnd_facility=True if row_values[47] else False,
                                                    govt_recognised=True if row_values[48] else False,
                                                    foreign_collaboration=True if row_values[50] else False,
                                                    eou=False, iso=True if row_values[49] else False,
                                                    iso_detail=str(row_values[49]).strip() if row_values[49] else None,
                                                    total_manager=row_values[52] if row_values[52] else 0,
                                                    total_staff=row_values[53] if row_values[53] else 0,
                                                    total_workers=row_values[54] if row_values[54] else 0,
                                                    total_employees=row_values[52] if row_values[52] else 0 +
                                                                                                          row_values[
                                                                                                              53] if
                                                    row_values[53] else 0 + row_values[54] if row_values[54] else 0,
                                                    created_by='155_missing_list', updated_by='155_missing_list')
                        company_obj.save()

                        if row_values[9] or row_values[10] or row_values[11] or row_values[9] or row_values[10] or \
                                row_values[11] or row_values[12] or row_values[13] or row_values[14] or row_values[
                            15] or row_values[16] or row_values[17] or row_values[18] or row_values[19] or row_values[
                            20] or row_values[21] or row_values[22] or row_values[23] or row_values[24]:
                            hod_obj = HOD_Detail(
                                hr_name=str(row_values[9]).strip() if row_values[9] else '',
                                hr_email=str(row_values[10]).strip() if row_values[10] else '',
                                finance_name=str(row_values[11]).strip() if row_values[11] else '',
                                finance_email=str(row_values[12]).strip() if row_values[12] else '',
                                marketing_name=str(row_values[13]).strip() if row_values[13] else '',
                                marketing_email=str(row_values[14]).strip() if row_values[14] else '',
                                IT_name=str(row_values[15]).strip() if row_values[15] else '',
                                IT_email=str(row_values[16]).strip() if row_values[16] else '',
                                corp_rel_name=str(row_values[17]).strip() if row_values[17] else '',
                                corp_rel_email=str(row_values[18]).strip() if row_values[18] else '',
                                tech_name=str(row_values[19]).strip() if row_values[19] else '',
                                tech_email=str(row_values[20]).strip() if row_values[20] else '',
                                rnd_name=str(row_values[21]).strip() if row_values[21] else '',
                                rnd_email=str(row_values[22]).strip() if row_values[22] else '',
                                exim_name=str(row_values[23]).strip() if row_values[23] else '',
                                exim_email=str(row_values[24]).strip() if row_values[24] else '',
                                created_by='155_missing_list').save()
                            company_obj.hoddetail = hod_obj
                            company_obj.save()

                        industry_list = []
                        industry_list = row_values[121].split(',')
                        # print '\nindustry_list = ', industry_list, len(industry_list)
                        if len(industry_list) > 1:
                            for industry_text in industry_list:
                                print str(industry_text).strip()
                                industry_obj = IndustryDescription.objects.get(description=str(industry_text).strip(),
                                                                               is_active=True, is_deleted=False)
                                company_obj.industrydescription.add(industry_obj)
                        else:
                            industry_obj = IndustryDescription.objects.get(description=str(industry_list[0]).strip(),
                                                                           is_active=True, is_deleted=False)
                            company_obj.industrydescription.add(industry_obj)

                        legal_obj = LegalStatus.objects.get(description=row_values[122], is_active=True,
                                                            is_deleted=False)
                        company_obj.legalstatus = legal_obj
                        company_obj.save()

                        user_obj = UserDetail(company=company_obj, ceo_name=str(row_values[4]).strip(),
                                              ceo_email=str(row_values[5]).strip(),
                                              ceo_cellno=row_values[6] if row_values[6] > 0 else None,
                                              correspond_address=str(row_values[25]).strip() + ' ' + str(
                                                  row_values[26]).strip(),
                                              correspond_email=str(row_values[31]).strip(),
                                              correspond_pincode=str(row_values[28]).strip(),
                                              person_email=str(row_values[32]).strip(),
                                              website=str(row_values[33]).split(),
                                              factory_address=str(row_values[34]).strip() + ' ' + str(
                                                  row_values[35]).strip(),
                                              factory_pincode=str(row_values[37]).strip(),
                                              membership_acceptance_date=datetime.datetime.strptime(str(row_values[68]),
                                                                                                    '%d/%m/%Y').date() if
                                              row_values[68] else '',
                                              created_by='155_missing_list')
                        user_obj.save()

                        if len(str(row_values[29]).strip()) == 10:
                            user_obj.correspond_cellno = int(str(row_values[29]).strip())
                        elif str(row_values[29]).strip():
                            temp_cont_list = str(row_values[29]).split('-')
                            if len(temp_cont_list) > 1:
                                # print str(row_values[30]).strip()
                                # print temp_cont_list
                                user_obj.correspond_std1 = int(temp_cont_list[0])
                                user_obj.correspond_landline1 = int(temp_cont_list[1])
                            else:
                                user_obj.correspond_landline1 = str(row_values[29]).strip()

                        if len(str(row_values[38]).strip()) == 10:
                            user_obj.factory_cellno = str(row_values[38]).strip()
                        elif str(row_values[38]).strip():
                            temp_cont_list = str(row_values[38]).split('-')
                            if len(temp_cont_list) > 1:
                                user_obj.factory_std1 = int(temp_cont_list[0])
                                user_obj.factory_landline1 = int(temp_cont_list[1])
                            else:
                                user_obj.factory_landline1 = str(row_values[38]).strip()

                        user_obj.save()

                        user_obj.correspondcity = City.objects.filter(city_name=str(row_values[27]).strip(),
                                                                      created_by='admin', is_active=True,
                                                                      is_deleted=False).first()
                        if str(row_values[37]).strip():
                            user_obj.factorycity = City.objects.filter(city_name=str(row_values[36]).strip(),
                                                                       created_by='admin', is_active=True,
                                                                       is_deleted=False).first()
                        user_obj.save()

                        if user_obj.correspondcity:
                            user_obj.correspondstate = user_obj.correspondcity.state
                        elif user_obj.factorycity:
                            user_obj.factorystate = user_obj.factorycity.state
                        user_obj.save()

                        # user_obj.user_type = 'Associate'
                        if str(row_values[114]).strip() == 'Organizational':
                            user_obj.enroll_type = 'CO'
                            print '\nCompany'
                        else:
                            user_obj.enroll_type = 'IN'
                            print '\nIndividual'

                        if str(row_values[113]).strip() == 'Life Membership':
                            user_obj.user_type = 'Life Membership'
                        elif str(row_values[116]).strip() == 'Associates':
                            user_obj.user_type = 'Associate'
                        else:
                            user_obj.user_type = 'Member'

                        m_no_list = str(row_values[2]).strip().split('-')
                        mem_no = str(m_no_list[0].strip()) + '-' + str(m_no_list[1].strip())
                        user_obj.member_associate_no = mem_no
                        user_obj.membership_year = '2018-2019'
                        user_obj.valid_invalid_member = True
                        user_obj.payment_method = 'Confirmed'
                        user_obj.created_by = '155_missing_list'

                        # print i
                        # print 'Company = ', row_values[3]
                        category_obj = MembershipCategory.objects.get(membership_category=row_values[115],
                                                                      created_by='admin',
                                                                      enroll_type=row_values[113],
                                                                      category_enroll_type=str(row_values[114]).strip())
                        # print 'Category = ', category_obj.membership_category
                        # for slab in MembershipSlab.objects.filter(membershipCategory=category_obj,created_by='admin'):
                        #     print slab.applicableTo
                        #     print slab.annual_fee
                        #     print slab.entrance_fee

                        try:
                            slab_obj = MembershipSlab.objects.get(membershipCategory=category_obj, created_by='admin',
                                                                  applicableTo=str(row_values[116]),
                                                                  annual_fee=str(int(float(row_values[117]))),
                                                                  entrance_fee=str(int(float(row_values[118]))),
                                                                  status=True, is_deleted=False)
                        except Exception, e:
                            slab_obj = MembershipSlab.objects.filter(membershipCategory=category_obj,
                                                                     created_by='admin',
                                                                     applicableTo=str(row_values[116]),
                                                                     annual_fee=str(int(float(row_values[117]))),
                                                                     entrance_fee=str(int(float(row_values[118]))),
                                                                     status=True, is_deleted=False).last()
                        # print 'Slab = ', slab_obj.slab, '\n'
                        i = i + 1
                        user_obj.membership_category = category_obj
                        user_obj.membership_slab = slab_obj
                        user_obj.save()

                        try:
                            member_login_obj = MembershipUser.objects.get(username=user_obj.member_associate_no)
                        except Exception, e:
                            new_user_login_obj = MembershipUser(userdetail=user_obj, created_by='155_missing_list',
                                                                username=user_obj.member_associate_no)
                            new_user_login_obj.save()
                            new_user_login_obj.set_password('mccia@test')
                            new_user_login_obj.save()
                            pass

                        if row_values[108]:
                            new_invoice_obj = MembershipInvoice(
                                userdetail=user_obj, membership_category=user_obj.membership_category,
                                membership_slab=user_obj.membership_slab, valid_invalid_member=True,
                                subscription_charges=int(row_values[107]),
                                tax=int(row_values[108]),
                                amount_payable=int(row_values[107]) + int(row_values[108]),
                                financial_year='2018-2019', invoice_for='RENEW', is_paid=True,
                                created_by='155_missing_list', updated_by='no_payment_detail')
                            new_invoice_obj.save()

                            payment_obj = PaymentDetails(userdetail=user_obj,
                                                         membershipInvoice=new_invoice_obj,
                                                         amount_payable=new_invoice_obj.amount_payable,
                                                         amount_paid=int(row_values[107]) + int(row_values[108]),
                                                         payment_date=datetime.datetime.now().date(),
                                                         user_Payment_Type='NEFT',
                                                         financial_year='2018-2019',
                                                         created_by='155_missing_list', updated_by='no_payment_detail')
                            payment_obj.save()
                            user_obj.membership_year = '2018-2019'
                            user_obj.valid_invalid_member = True
                            user_obj.payment_method = 'Confirmed'
                            user_obj.save()
                        else:
                            if row_values[107]:
                                gst_tax = round(row_values[107] * 18 / 100, 0)
                                new_invoice_obj = MembershipInvoice(
                                    userdetail=user_obj, membership_category=user_obj.membership_category,
                                    membership_slab=user_obj.membership_slab, valid_invalid_member=True,
                                    subscription_charges=int(row_values[107]),
                                    tax=gst_tax,
                                    amount_payable=int(row_values[107]) + gst_tax,
                                    financial_year='2018-2019', invoice_for='RENEW', is_paid=True,
                                    created_by='155_missing_list', updated_by='no_payment_detail')
                                new_invoice_obj.save()

                                payment_obj = PaymentDetails(userdetail=user_obj,
                                                             membershipInvoice=new_invoice_obj,
                                                             amount_payable=new_invoice_obj.amount_payable,
                                                             financial_year='2018-2019',
                                                             created_by='155_missing_list',
                                                             updated_by='no_payment_detail')
                                payment_obj.save()
                                user_obj.membership_year = '2018-2019'
                                user_obj.valid_invalid_member = True
                                user_obj.payment_method = 'Confirmed'
                                user_obj.save()

                        print '\nAdded = ', user_obj.member_associate_no

                        # if str(row_values[113]).strip() == 'Life Membership':
                        #     due_amt = 0
                        #     amt = 0
                        #     st_amt = 0
                        #     if row_values[72] and int(row_values[72]) > 0:
                        #         due_amt = due_amt + int(row_values[72])
                        #         amt = amt + int(row_values[73])
                        #         st_amt = st_amt + int(row_values[74])
                        #     if row_values[78] and int(row_values[78]) > 0:
                        #         due_amt = due_amt + int(row_values[78])
                        #         amt = amt + int(row_values[79])
                        #         st_amt = st_amt + int(row_values[80])
                        #     if row_values[85] and int(row_values[85]) > 0:
                        #         due_amt = due_amt + int(row_values[85])
                        #         amt = amt + int(row_values[86])
                        #         st_amt = st_amt + int(row_values[87])
                        #     if row_values[92] and int(row_values[92]) > 0:
                        #         due_amt = due_amt + int(row_values[92])
                        #         amt = amt + int(row_values[93])
                        #         st_amt = st_amt + int(row_values[94])
                        #     if row_values[99] and int(row_values[99]) > 0:
                        #         due_amt = due_amt + int(row_values[99])
                        #         amt = amt + int(row_values[100])
                        #         st_amt = st_amt + int(row_values[101])
                        #     if row_values[106] and int(row_values[106]) > 0:
                        #         due_amt = due_amt + int(row_values[106])
                        #         amt = amt + int(row_values[107])
                        #         st_amt = st_amt + int(row_values[108])
                        #     new_invoice_obj = MembershipInvoice(
                        #         userdetail=user_obj,membership_category=user_obj.membership_category,
                        #         membership_slab=user_obj.membership_slab, valid_invalid_member=True,
                        #         subscription_charges=due_amt, tax=st_amt,
                        #         amount_payable=due_amt+st_amt
                        #     ).save()
                        #
                        #     new_payment_obj = PaymentDetails()

                        pass
                except Exception, e:
                    print e
                    print row_values
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\ndone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


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
        for event_item in EventDetails.objects.filter(is_deleted=0).order_by('from_date'):
            # a = event_item.from_date
            # b = 'E' + str(event_item.from_date.strftime('%d%m%y')) + str(event_item.id)            
            # if int(a.day) == int(b[1:3]) and int(a.month) == int(b[3:5]):
            #     print event_item.from_date, '\t', 'E' + str(event_item.from_date.strftime('%d%m%y')) + str(event_item.id), '\t', 'CORRECT'
            # else:
            #     print event_item.from_date, '\t', 'E' + str(event_item.from_date.strftime('%d%m%y')) + str(event_item.id), '\t', 'INCORRECT'

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


@transaction.atomic
def add_event_data():
    sid = transaction.savepoint()
    try:
        file_path = [
            '/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/Event_Data/Add_Event_in_PROD.xlsx']

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(89, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)

                    row_values.append(value)
                # print row_values                
                # return
                try:
                    event_obj = EventDetails(event_title=row_values[0].strip(),
                                             from_date=datetime.datetime.strptime(str(row_values[1]).strip(),
                                                                                  '%d/%m/%Y'),
                                             to_date=datetime.datetime.strptime(str(row_values[2]).strip(), '%d/%m/%Y'),
                                             organising_committee=Committee.objects.get(
                                                 committee=str(row_values[3]).strip()))
                    event_obj.save()
                    if row_values[2]:
                        event_obj.to_date = datetime.datetime.strptime(str(row_values[2]).strip(), '%d/%m/%Y')
                        event_obj.save()
                    event_obj.event_no = 'E' + str(event_obj.from_date.strftime('%d%m%y')) + str(event_obj.id)
                    event_obj.contact_person1 = SystemUserProfile.objects.get(id=str(int(float(row_values[4]))).strip())

                    if row_values[6].strip() == 'Free':
                        event_obj.event_mode = 0
                    else:
                        event_obj.event_mode = 1
                    event_obj.event_status = 1
                    event_obj.view_status = 0

                    if row_values[5]:
                        event_obj.contact_person2 = SystemUserProfile.objects.get(
                            id=str(int(float(row_values[5]))).strip())
                    event_obj.save()
                    print event_obj.from_date, event_obj.to_date, event_obj.event_no, event_obj.id
                except Exception, e:
                    print str(traceback.print_exc())
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\nDone'

    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def map_event_with_participant():
    sid = transaction.savepoint()
    try:
        file_path = [
            '/home/admin12/Test_project/Mass_Mailing/Madhura_Mam/FT Event Particicipants during April to December 2018 revised list.xls']
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
                                        if 'Madhura_Chipade' not in person_obj.updated_by:
                                            person_obj.updated_by = str(person_obj.updated_by) + ',Madhura_Chipade'
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
                                            created_by='Madhura_Chipade'
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
def update_life_member():
    sid = transaction.savepoint()
    try:
        file_path = [
            '/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/Data_Check_Update/Life_Member_DAta.xlsx']

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[3].nrows
            number_of_columns = wb.sheets()[3].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[3].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                # return
                try:
                    print 'Processing = ', row_values[0]
                    user_detail_obj = UserDetail.objects.get(member_associate_no=row_values[0].strip())
                    user_detail_obj.user_type = 'Life Membership'
                    user_detail_obj.membership_year = str(row_values[4]).strip()
                    user_detail_obj.valid_invalid_member = True
                    user_detail_obj.membership_category_id = int(row_values[2])
                    user_detail_obj.membership_slab_id = int(row_values[3])
                    user_detail_obj.save()

                    invoice_obj = MembershipInvoice(
                        userdetail=user_detail_obj,
                        membership_category=user_detail_obj.membership_category,
                        membership_slab=user_detail_obj.membership_slab,
                        valid_invalid_member=True,
                        subscription_charges=int(user_detail_obj.membership_slab.annual_fee),
                        tax=Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18),
                        amount_payable=Decimal(user_detail_obj.membership_slab.annual_fee) + Decimal(
                            Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18)),
                        financial_year=str(row_values[4]).strip(),
                        is_paid=True,
                        created_by='admin'
                    )
                    invoice_obj.save()

                    payment_obj = PaymentDetails(
                        userdetail=user_detail_obj,
                        membershipInvoice=invoice_obj,
                        amount_payable=invoice_obj.amount_payable,
                        amount_paid=invoice_obj.amount_payable,
                        cheque_no='000000',
                        cheque_date=datetime.datetime.strptime('01/01/1900', '%d/%m/%Y').date(),
                        bank_name='Dummy',
                        user_Payment_Type='Cheque',
                        payment_date=datetime.datetime.strptime('01/01/1900', '%d/%m/%Y').date(),
                        payment_received_status='Paid',
                        financial_year=invoice_obj.financial_year,
                        payment_remark='Dummy',
                        created_by='admin',
                    )
                    payment_obj.save()
                    bk_no = 'MBK' + str(payment_obj.id).zfill(7)
                    payment_obj.bk_no = str(bk_no)
                    payment_obj.save()
                    print 'Updated = ', row_values[0]
                except Exception, e:
                    print str(traceback.print_exc())
                    transaction.rollback(sid)
        transaction.savepoint_commit(sid)
        print '\nDone'
        return True
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
        return False


@transaction.atomic
def update_membership_no():
    sid = transaction.savepoint()
    try:
        # id_list = UserDetail.objects.exclude(member_associate_no__in=['NULL','TMP', 'HHHHHHH', 'HHHHHHH1','test','TEST1001'])
        # print id_list[:].count()
        # # return
        # for item in id_list[:]:
        #     member_obj = UserDetail.objects.get(id=item.id)
        #     # print member_obj.member_associate_no
        #     if member_obj.member_associate_no and member_obj.member_associate_no not in ['NULL','TMP', 'HHHHHHH', 'HHHHHHH1','test','TEST1001']:
        #         m_no_list = member_obj.member_associate_no.split('-')
        #         print m_no_list
        #         mem_no = str(m_no_list[0].strip()) + '-' + str(m_no_list[1].strip())
        #         member_obj.member_associate_no = mem_no
        #         member_obj.save()
        #     print member_obj.member_associate_no
        # transaction.savepoint_commit(sid)
        # print 'DONE'

        # id_list = UserDetail.objects.exclude(member_associate_no__in=['NULL', 'TMP', 'HHHHHHH', 'HHHHHHH1', 'test', 'TEST1001'])
        id_list = MembershipUser.objects.all()
        total = id_list.count()
        i = 1
        print id_list[:].count()
        # return
        for item in id_list[:]:
            # print member_obj.member_associate_no
            if not item.userdetail.payment_method == 'Deactivate':
                if item.username:
                    m_no_list = item.username.split('-')
                    print m_no_list
                    mem_no = str(m_no_list[0].strip()) + '-' + str(m_no_list[1].strip())
                    item.username = mem_no
                    item.save()
                print item.username
            else:
                item.is_deleted = True
                item.save()
            i = i + 1
        transaction.savepoint_commit(sid)
        print 'DONE'
        return True
    except Exception, e:
        print e, '\n', str(traceback.print_exc())
        print '\n ', i, 'Out of ', total
        transaction.rollback(sid)
        return False


def new_member_not_present():
    try:
        file_path = [
            '/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/Data_Check_Update/Check_18-19_New_Member.xlsx']
        new_member_not_present_list = []

        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(0, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                # print row_values                
                try:
                    # if row_values[0].strip() not in [i.member_associate_no.strip() for i in UserDetail.objects.filter(member_associate_no__isnull=False).exclude(member_associate_no='NULL')]:
                    #     new_member_not_present_list.append({'mem_no': row_values[0]})
                    #     new_member_not_present_list.append({'company': row_values[1]})
                    #     print row_values[0], row_values[1]
                    if row_values[0].strip() in [i.member_associate_no.strip() for i in
                                                 UserDetail.objects.filter(member_associate_no__isnull=False).exclude(
                                                         member_associate_no='NULL')]:
                        member_obj = UserDetail.objects.get(member_associate_no=row_values[0].strip())
                        print row_values[0], '\t', row_values[
                            1], '\t', member_obj.membership_acceptance_date, '\t', member_obj.valid_invalid_member
                except Exception, e:
                    print str(traceback.print_exc())
                    # transaction.rollback(sid)

        # transaction.savepoint_commit(sid)
        print '\nDone'

    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        # transaction.rollback(sid)
    return


def some_check():
    try:
        # for i in UserDetail.objects.filter(member_associate_no__isnull=False).exclude(member_associate_no='NULL'):
        #     print i.member_associate_no, '\t', i.company.company_name, '\t', i.membership_year, '\t', i.membership_acceptance_date, '\t', i.valid_invalid_member
        check_list = ['IA-10348', 'IA-10349', 'IA-10335', 'IA-5357', 'IA-10353', 'IA-10297', 'IA-10355', 'IA-10439',
                      'IA-10298', 'AH-2549', 'IA-10445', 'IA-10448', 'IA-10336', 'AG-0137', 'IA-10299', 'IA-6718',
                      'A-0039', 'IA-10300', 'IA-10337', 'B-0034', 'IA-10301', 'IA-10338', 'HA-6105', 'IA-10339',
                      'IA-10302', 'IA-10340', 'IH-2306', 'IA-10303', 'IA-10367', 'IA-10464', 'IA-10540', 'IA-10304',
                      'IA-10341', 'IA-10305', 'IA-10306', 'IA-10473', 'IA-10374', 'IA-10307', 'IA-10371', 'AG-0058',
                      'IA-10376', 'IA-10478', 'IA-10308', 'IA-4509', 'IA-10309', 'IA-10278', 'IA-10379', 'H-2604',
                      'IA-10279', 'IA-7178', 'H-1542', 'IA-10380', 'IA-10486', 'IA-8094', 'IA-7179', 'IA-10281',
                      'IA-9485', 'IA-10310', 'IA-10383', 'IA-10282', 'IA-10311', 'IA-10312', 'IA-10387', 'IA-10388',
                      'IA-10313', 'IA-10314', 'IA-10342', 'IA-10315', 'IA-10316', 'IA-10317', 'IA-10318', 'IA-10394',
                      'IA-10319', 'IA-10283', 'IA-10507', 'H-2605', 'IA-10343', 'IA-10284', 'IA-10398', 'IA-10320',
                      'IA-10513', 'IA-10285', 'IA-10401', 'IA-9632', 'IA-10519', 'WES-0074', 'IA-10523', 'IA-7136',
                      'IA-7137', 'IA-10321', 'IA-10287', 'IA-10288', 'IA-10322', 'IA-10289', 'IA-10290', 'IA-10291',
                      'IA-7139', 'IA-10344', 'IA-10408', 'IA-10323', 'SIA-7335', 'IA-10532', 'IA-10345', 'IA-10324',
                      'IA-10292', 'IA-10537', 'SSI-0039', 'IA-10538', 'IA-10293', 'IA-10346', 'IA-8067', 'B-0024',
                      'IA-10545', 'IA-10347', 'IA-10294', 'IA-10325', 'H-1178', 'IH-1155', 'IA-1032', 'IA-10327',
                      'IA-10328', 'IA-10554', 'IA-10295', 'IA-10329', 'IA-7152', 'IA-10330', 'IA-10331', 'IA-10332',
                      'IA-10333', 'IA-10334', 'IA-10562']
        for j in check_list:
            if j not in [i.member_associate_no.strip() for i in
                         UserDetail.objects.filter(member_associate_no__isnull=False).exclude(
                                 member_associate_no='NULL')]:
                print j
    except Exception as e:
        raise
    return


def update_invitee():
    sid = transaction.savepoint()
    try:
        for event_reg_obj in EventRegistration.objects.filter(is_deleted=False):
            if event_reg_obj.is_invitee:
                EventParticipantUser.objects.filter(event_user=event_reg_obj, is_deleted=False).update(is_invitee=True)

            if event_reg_obj.is_attendees:
                EventParticipantUser.objects.filter(event_user=event_reg_obj, is_deleted=False).update(
                    is_attendees=True)
        transaction.savepoint_commit(sid)
        print '\nDone'
    except Exception as e:
        transaction.rollback(sid)
        return
        print e


def check_data():
    try:
        sid = transaction.savepoint()
        file_path = ['/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/New_Member_Files/Final_File.xlsx']
        not_found_list = []
        multiple_obj_list = []
        no_payment_data = []
        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            print wb.sheet_names()
            number_of_rows = wb.sheets()[2].nrows
            number_of_columns = wb.sheets()[2].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[2].cell(row, col).value)
                    row_values.append(value)
                # print row_values        
                # return        
                try:
                    if row_values[1].strip():
                        m_no_list = row_values[1].split('-')
                        mem_no = str(m_no_list[0].strip()) + '-' + str(m_no_list[1].strip())
                        try:
                            user_detail_obj = UserDetail.objects.get(member_associate_no=mem_no)

                            try:
                                # invoice_obj = MembershipInvoice.objects.get(userdetail=user_detail_obj, financial_year='2018-2019', is_deleted=False)
                                invoice_obj_list_1 = MembershipInvoice.objects.filter(userdetail=user_detail_obj,
                                                                                      financial_year='2018-2019',
                                                                                      is_deleted=False)
                                invoice_obj_list_2 = MembershipInvoice.objects.filter(userdetail=user_detail_obj,
                                                                                      financial_year='2019-2020',
                                                                                      is_deleted=False)
                                if not invoice_obj_list_1 and not invoice_obj_list_2:
                                    no_payment_data.append({
                                        'mem_no': str(user_detail_obj.member_associate_no),
                                        'company_name': str(user_detail_obj.company.company_name)
                                    })
                            except Exception, e:
                                # no_payment_data.append({
                                #     'mem_no': str(user_detail_obj.member_associate_no),
                                #     'company_name': str(user_detail_obj.company.company_name)
                                #     })
                                pass

                        except Exception, e:
                            user_detail_list = UserDetail.objects.filter(member_associate_no=mem_no)
                            for user_obj in user_detail_list:
                                multiple_obj_list.append({
                                    'sys_mem_no': str(user_obj.member_associate_no),
                                    'excel_mem_no': str(mem_no),
                                    'company_name': str(user_obj.company.company_name)
                                })
                            print e, '\n', 'mem_no = ', mem_no, '\nrow_value = ', row_values[1]
                            not_found_list.append(mem_no)
                            pass

                except Exception, e:
                    print str(traceback.print_exc())
                    print '\nmem_no = ', mem_no, '\nrow_value = ', row_values[1]
                    print 'Multiple List = ', multiple_obj_list, '\n'
                    print 'Not found List = ', not_found_list
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\nDone'
        print 'Multiple List = ', multiple_obj_list, '\n'
        print 'Not found List = ', not_found_list, '\n'
        print 'no_payment_data = ', no_payment_data
    except Exception, e:
        print '\nEXCP = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def update_members():
    sid = transaction.savepoint()
    try:
        file_path = ['/home/admin12/Test_project/Membership/Update_Members_Data.xlsx']
        i = 0
        user_slab_list = []
        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
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
                    # Check if Member already exists
                    try:
                        user_detail_obj = UserDetail.objects.get(member_associate_no=str(row_values[0]).strip())
                        # user_detail_obj.user_type = 'Member'
                        if not user_detail_obj.member_associate_no == 'H-2568':
                            user_detail_obj.membership_year = '2018-2019'
                        user_detail_obj.valid_invalid_member = True
                        user_detail_obj.payment_method = 'Confirmed'
                        user_detail_obj.created_by = 'admin_no_payment_18_19'
                        user_detail_obj.is_deleted = False

                        category_obj = MembershipCategory.objects.get(membership_category=row_values[4],
                                                                      created_by='admin',
                                                                      enroll_type=row_values[2],
                                                                      category_enroll_type=str(row_values[3]).strip())

                        try:
                            slab_obj = MembershipSlab.objects.get(membershipCategory=category_obj, created_by='admin',
                                                                  applicableTo=str(row_values[5]),
                                                                  annual_fee=str(int(float(row_values[6]))),
                                                                  entrance_fee=str(int(float(row_values[7]))),
                                                                  status=True, is_deleted=False)
                            print user_detail_obj.member_associate_no, slab_obj.slab
                        except Exception, e:
                            slab_obj = MembershipSlab.objects.filter(membershipCategory=category_obj,
                                                                     created_by='admin',
                                                                     applicableTo=str(row_values[5]),
                                                                     annual_fee=str(int(float(row_values[6]))),
                                                                     entrance_fee=str(int(float(row_values[7]))),
                                                                     status=True, is_deleted=False).last()
                            print user_detail_obj.member_associate_no, slab_obj.slab
                        user_detail_obj.membership_category = category_obj
                        user_detail_obj.membership_slab = slab_obj
                        user_detail_obj.save()

                        try:
                            member_login_obj = MembershipUser.objects.get(username=user_detail_obj.member_associate_no)
                        except Exception, e:
                            new_user_login_obj = MembershipUser(userdetail=user_detail_obj,
                                                                created_by='admin_no_payment_18_19',
                                                                username=str(
                                                                    user_detail_obj.member_associate_no).strip())
                            new_user_login_obj.save()
                            new_user_login_obj.set_password('mccia@test')
                            new_user_login_obj.save()
                            pass

                        new_invoice_obj = MembershipInvoice(
                            userdetail=user_detail_obj, membership_category=category_obj,
                            membership_slab=slab_obj, valid_invalid_member=True,
                            subscription_charges=Decimal(slab_obj.annual_fee),
                            tax=Decimal(Decimal(slab_obj.annual_fee) * Decimal(0.18)),
                            amount_payable=Decimal(slab_obj.annual_fee) + Decimal(
                                Decimal(slab_obj.annual_fee) * Decimal(0.18)),
                            financial_year='2018-2019', invoice_for='RENEW', is_paid=True,
                            created_by='admin_no_payment_18_19', updated_by='no_payment_detail')
                        new_invoice_obj.save()

                        payment_obj = PaymentDetails(userdetail=user_detail_obj,
                                                     membershipInvoice=new_invoice_obj,
                                                     amount_payable=new_invoice_obj.amount_payable,
                                                     amount_paid=new_invoice_obj.amount_payable,
                                                     payment_date=datetime.datetime.now().date(),
                                                     user_Payment_Type='NEFT',
                                                     financial_year='2018-2019',
                                                     created_by='admin_no_payment_18_19',
                                                     updated_by='no_payment_detail')
                        payment_obj.save()
                        user_detail_obj.valid_invalid_member = True
                        user_detail_obj.payment_method = 'Confirmed'
                        user_detail_obj.save()
                    except Exception, e:
                        print e
                except Exception, e:
                    print e
                    print row_values
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)
        print '\ndone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def update_associates():
    sid = transaction.savepoint()
    try:
        file_path = ['/home/admin12/Test_project/Membership/Update_Associate_data.xlsx']
        i = 0
        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            i = 1
            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                # return
                try:
                    user_detail_obj = UserDetail.objects.get(member_associate_no=str(row_values[1]).strip())
                    print user_detail_obj.member_associate_no, user_detail_obj.membership_slab.slab, user_detail_obj.membership_year

                    if user_detail_obj.membership_year == '2019-2020':
                        invoice_obj_list = MembershipInvoice.objects.filter(userdetail=user_detail_obj,
                                                                            financial_year='2018-2019',
                                                                            is_deleted=False)
                        if invoice_obj_list:
                            for item in invoice_obj_list:
                                item.is_paid = True
                                item.save()
                        else:
                            new_invoice_obj = MembershipInvoice(
                                userdetail=user_detail_obj, membership_category=user_detail_obj.membership_category,
                                membership_slab=user_detail_obj.membership_slab, valid_invalid_member=True,
                                subscription_charges=Decimal(user_detail_obj.membership_slab.annual_fee),
                                tax=Decimal(Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18)),
                                amount_payable=Decimal(user_detail_obj.membership_slab.annual_fee) + Decimal(
                                    Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18)),
                                financial_year='2018-2019', invoice_for='RENEW', is_paid=True,
                                created_by='admin_no_payment_18_19', updated_by='no_payment_detail')
                            new_invoice_obj.save()

                            payment_obj = PaymentDetails(userdetail=user_detail_obj,
                                                         membershipInvoice=new_invoice_obj,
                                                         amount_payable=new_invoice_obj.amount_payable,
                                                         amount_paid=new_invoice_obj.amount_payable,
                                                         payment_date=datetime.datetime.now().date(),
                                                         user_Payment_Type='NEFT',
                                                         financial_year='2018-2019',
                                                         created_by='admin_no_payment_18_19',
                                                         updated_by='no_payment_detail')
                            payment_obj.save()

                            user_detail_obj.valid_invalid_member = True
                            user_detail_obj.payment_method = 'Confirmed'
                            user_detail_obj.save()

                    elif user_detail_obj.membership_year == '2018-2019':
                        invoice_obj_list = MembershipInvoice.objects.filter(userdetail=user_detail_obj,
                                                                            financial_year='2018-2019',
                                                                            is_deleted=False)
                        if invoice_obj_list:
                            for item in invoice_obj_list:
                                item.is_paid = True
                                item.save()
                        else:
                            new_invoice_obj = MembershipInvoice(
                                userdetail=user_detail_obj, membership_category=user_detail_obj.membership_category,
                                membership_slab=user_detail_obj.membership_slab, valid_invalid_member=True,
                                subscription_charges=Decimal(user_detail_obj.membership_slab.annual_fee),
                                tax=Decimal(Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18)),
                                amount_payable=Decimal(user_detail_obj.membership_slab.annual_fee) + Decimal(
                                    Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18)),
                                financial_year='2018-2019', invoice_for='RENEW', is_paid=True,
                                created_by='admin_no_payment_18_19', updated_by='no_payment_detail')
                            new_invoice_obj.save()

                            payment_obj = PaymentDetails(userdetail=user_detail_obj,
                                                         membershipInvoice=new_invoice_obj,
                                                         amount_payable=new_invoice_obj.amount_payable,
                                                         amount_paid=new_invoice_obj.amount_payable,
                                                         payment_date=datetime.datetime.now().date(),
                                                         user_Payment_Type='NEFT',
                                                         financial_year='2018-2019',
                                                         created_by='admin_no_payment_18_19',
                                                         updated_by='no_payment_detail')
                            payment_obj.save()

                            user_detail_obj.valid_invalid_member = True
                            user_detail_obj.payment_method = 'Confirmed'
                            user_detail_obj.save()
                    else:
                        new_invoice_obj = MembershipInvoice(
                            userdetail=user_detail_obj, membership_category=user_detail_obj.membership_category,
                            membership_slab=user_detail_obj.membership_slab, valid_invalid_member=True,
                            subscription_charges=Decimal(user_detail_obj.membership_slab.annual_fee),
                            tax=Decimal(Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18)),
                            amount_payable=Decimal(user_detail_obj.membership_slab.annual_fee) + Decimal(
                                Decimal(user_detail_obj.membership_slab.annual_fee) * Decimal(0.18)),
                            financial_year='2018-2019', invoice_for='RENEW', is_paid=True,
                            created_by='admin_no_payment_18_19', updated_by='no_payment_detail')
                        new_invoice_obj.save()

                        payment_obj = PaymentDetails(userdetail=user_detail_obj,
                                                     membershipInvoice=new_invoice_obj,
                                                     amount_payable=new_invoice_obj.amount_payable,
                                                     amount_paid=new_invoice_obj.amount_payable,
                                                     payment_date=datetime.datetime.now().date(),
                                                     user_Payment_Type='NEFT',
                                                     financial_year='2018-2019',
                                                     created_by='admin_no_payment_18_19',
                                                     updated_by='no_payment_detail')
                        payment_obj.save()

                        user_detail_obj.valid_invalid_member = True
                        user_detail_obj.payment_method = 'Confirmed'
                        user_detail_obj.membership_year = '2018-2019'
                        user_detail_obj.save()

                    user_detail_obj.is_deleted = False
                    user_detail_obj.save()

                except Exception, e:
                    print row_values
                    print '\nexcp = ', str(traceback.print_exc())

        transaction.savepoint_commit(sid)
        print '\ndone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def update_membership_data():
    sid = transaction.savepoint()
    try:
        file_path = ['/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/Final_data/Data_Check_Update/MASTER_DATA_19-20_MAy_17_Shubham.xlsx']
        membership_no_list = []
        for file_item in file_path:
            print file_item
            wb = open_workbook(file_item)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            i = 1
            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                # print row_values
                # return
                try:
                    if row_values[1]:
                        temp_no_list = str(row_values[1]).split('-')
                        mem_no = str(temp_no_list[0]) + '-' + str(temp_no_list[1])
                        user_detail_obj = UserDetail.objects.get(member_associate_no=mem_no, is_deleted=False)
                        user_detail_obj.valid_invalid_member = True
                        user_detail_obj.payment_method = 'Confirmed'
                        user_detail_obj.save()
                        membership_no_list.append(mem_no)
                        print i, 'Added = ', '\t', mem_no, '-', user_detail_obj.company.company_name
                        i = i + 1
                except Exception, e:
                    print row_values
                    print '\nexcp = ', str(traceback.print_exc())
                    raise

        print '\n\n\n'
        for user_obj in UserDetail.objects.filter(member_associate_no__isnull=False):
            if user_obj.member_associate_no not in membership_no_list:
                user_obj.is_deleted = True
                user_obj.valid_invalid_member = False
                user_obj.payment_method= 'Deactivate'
                user_obj.save()
                MembershipUser.objects.filter(userdetail=user_obj).update(is_deleted=True)
                print 'Deactivated = ', user_obj.member_associate_no, '-', user_obj.company.company_name
        transaction.savepoint_commit(sid)
        print '\ndone'
    except Exception, e:
        print '\nexcp = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return


@transaction.atomic
def delete_empty_invoice():
    try:
        sid = transaction.savepoint()
        invoice_id_list = []
        payment_id_list = [8768, 8767, 9104, 8518, 8582, 9374, 9044, 9043, 8348, 8850, 8884, 8883, 8755, 9014, 9068,
                           9027, 8217, 7755, 7861, 7921, 7920, 9032, 8083, 9358, 9030, 9341, 8976, 7757, 7729, 9057,
                           8763, 8762, 9022, 7693, 7870, 8806, 7744, 7791, 7937, 8236, 7678, 8247, 8246, 8317, 8316,
                           9047, 9243, 8196, 8195, 8193, 8194, 9331]
        for item_id in payment_id_list:
            print 'Current PID = ', item_id
            try:
                payment_obj = PaymentDetails.objects.get(id=item_id)
                invoice_id_list.append(payment_obj.membershipInvoice.id)
            except Exception, e:
                pass
        i = 0
        for invoice_id in invoice_id_list:
            # print 'Invoice id = ', invoice_id
            try:
                invoice_obj = MembershipInvoice.objects.get(id=invoice_id)
                PaymentDetails.objects.filter(membershipInvoice=invoice_obj).delete()
                MembershipInvoice.objects.get(id=invoice_id).delete()
                print 'Deleted Payment id = ', payment_id_list[i]
                print 'Deleted Invoice id = ', invoice_id
            except Exception, e:
                pass
            i = i + 1
        print 'Deleted'
        transaction.savepoint_commit(sid)
    except Exception, e:
        print '\nError = ',str(traceback.print_exc())
        transaction.rollback(sid)


@transaction.atomic
def update_recent_member():
    try:
        sid = transaction.savepoint()
        date1 = datetime.datetime.strptime('2018-09-17', '%Y-%m-%d').date()
        date2 = datetime.datetime.strptime('2018-10-30', '%Y-%m-%d').date()
        date3 = datetime.datetime.strptime('2018-12-29', '%Y-%m-%d').date()
        date4 = datetime.datetime.strptime('2019-02-12', '%Y-%m-%d').date()
        date5 = datetime.datetime.strptime('2019-04-16', '%Y-%m-%d').date()
        date6 = datetime.datetime.strptime('2019-05-22', '%Y-%m-%d').date()
        date_list = []
        date_list.append(date1)
        date_list.append(date2)
        date_list.append(date3)
        date_list.append(date4)
        date_list.append(date5)
        date_list.append(date6)

        print 'Count = ', UserDetail.objects.filter(membership_acceptance_date__in=date_list).count()
        for member_obj in UserDetail.objects.filter(membership_acceptance_date__in=date_list):
            member_obj.valid_invalid_member = True
            member_obj.payment_method = 'Confirmed'  
            member_obj.is_deleted = False
            member_obj.save()     
            MembershipUser.objects.filter(userdetail=member_obj).update(is_deleted=False)     

        transaction.savepoint_commit(sid)

    except Exception, e:
        print 'Error = ',str(traceback.print_exc())
        transaction.rollback(sid)


if __name__ == "__main__":
    # delete_data()
    # delete_mem_data()
    # add_industrydescription()
    # add_membershipdescription()
    # add_legal_status()
    # add_mem_categary()
    # add_membershipslab()
    # load_member_data()
    # update_category_data()
    # show_slab()
    # check_inds()
    # print not(True)
    # update_member_data()
    # update_company_scale()
    # update_city_data()
    # insert_data()
    # add_city_state_data()
    # check_cat_slab()
    # check_data()    
    # save_data()
    # check_mails_matching_members()
    # add_event_data()
    # update_event_no()
    # map_event_with_participant()
    # check_imported_data()
    # import_members_data()
    # import_nonmember_data()
    # update_membership_no()
    # new_member_not_present()
    # some_check()
    # check_cat_slab()
    # update_invitee()
    # check_data()
    # update_life_member()
    # update_members()
    # update_associates()
    # update_associates()
    # update_membership_data()
    # delete_empty_invoice()
    # update_recent_member()
    pass
