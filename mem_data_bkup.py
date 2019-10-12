import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCCIA.settings')
django.setup()

import traceback
from django.http import HttpResponse
from xlrd import open_workbook
from django.db import transaction

from adminapp.models import *
from membershipapp.models import *
import datetime

#Start:Use this for local system
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_dir = BASE_DIR + '/MCCIA_BACKOFFICE/Final_data'
#End:Use this for local system

#Start:on server file path
# file_dir='/srv/wsgi/Final_data'
#End:on server file path




def delete_data():
    IndustryDescription.objects.all().delete()
    MembershipDescription.objects.all().delete()
    LegalStatus.objects.all().delete()
    MembershipCategory.objects.all().delete()
    MembershipSlab.objects.all().delete()
    SlabCriteria.objects.all().delete()
    City.objects.all().delete()
    # State.objects.all().delete()
    Country.objects.all().delete()
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
        file_path = [file_dir +'/industry_discription.xlsx']
        for file in file_path:
            wb = open_workbook(file)
            number_of_rows = wb.sheets()[0].nrows
            value_list = []
            for row in range(1, number_of_rows):
                PKDEscID = int((wb.sheets()[0].cell(row, 0).value))
                Code = int((wb.sheets()[0].cell(row, 1).value))
                Description = (wb.sheets()[0].cell(row, 2).value)
                CreatedBY = int((wb.sheets()[0].cell(row, 3).value))
                ModifiedBY = "NA" if (wb.sheets()[0].cell(row, 5).value) == 'NULL' else int((wb.sheets()[0].cell(row, 5).value))
                Status = True if (wb.sheets()[0].cell(row, 7).value) == 'Y' else False
                value_list.append([PKDEscID, Code, Description,CreatedBY, ModifiedBY, Status])
        sid = transaction.savepoint()
        for value  in value_list:
            try:
                IndustryDescription.objects.get(code=value[1],description=value[2])
            except IndustryDescription.DoesNotExist, e:
                pass
                try:
                    print value
                    IndustryDescriptionobj=IndustryDescription(
                        previous_id=value[0],
                        code=value[1],
                        description=value[2],
                        created_by=value[3],
                        is_active=value[5],
                        is_deleted= not(value[5])
                    )
                    IndustryDescriptionobj.save()
                except Exception,e:
                    print e
                    pass
                    transaction.rollback(sid)

        transaction.savepoint_commit(sid)

    except Exception,e:
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
            data={}
            for row in range(1, number_of_rows):
                PKDEscID = int((wb.sheets()[0].cell(row, 0).value))
                Code = int((wb.sheets()[0].cell(row, 1).value))
                Description = (wb.sheets()[0].cell(row, 2).value)
                CreatedBy = int((wb.sheets()[0].cell(row, 3).value))
                ModifiedBY = "NA" if (wb.sheets()[0].cell(row, 5).value) == 'NULL' else int(
                    (wb.sheets()[0].cell(row, 5).value))
                Status = True if (wb.sheets()[0].cell(row, 7).value) == 'Y' else False
                data={
                    'PKDEscID':PKDEscID,
                    'Code':Code,
                    'Description':Description,
                    'CreatedBy':CreatedBy,
                    'ModifiedBY':ModifiedBY,
                    'Status':Status,
                }
                # value_list.append([PKDEscID, Code, Description, CreatedBy, ModifiedBY, Status])

                value_dlist.append(data)
        sid = transaction.savepoint()
        for valued in value_dlist:
            try:
                MembershipDescription.objects.get(membership_description=valued['Description'],code=valued['Code'])
            except MembershipDescription.DoesNotExist, e:
                pass
                try:
                    MembershipDescriptionobj=MembershipDescription(
                        previous_id=valued['PKDEscID'],
                        membership_description=valued['Description'],
                        code=valued['Code'],
                        created_by=valued['CreatedBy'],
                        is_active=valued['Status'],
                        is_deleted= not(valued['Status'])
                    )
                    MembershipDescriptionobj.save()
                except Exception,e:
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
                    LegalStatus.objects.get(description=valued['Description'],code=valued['Code'])
                except LegalStatus.DoesNotExist, e:
                    pass
                    try:
                        LegalStatusobj=LegalStatus(
                            previous_id=valued['PKDEscID'],
                            description=valued['Description'],
                            code=valued['Code'],
                            created_by=valued['CreatedBy'],
                            is_active=valued['Status'],
                            is_deleted= not(valued['Status']),
                            status=valued['Status']
                        )
                        LegalStatusobj.save()
                    except Exception,e:
                        pass
                        transaction.rollback(sid)

                except Exception, e:
                    print e
                    pass
                    transaction.rollback(sid)
        except Exception,e:
            print e
            pass
            transaction.savepoint_commit(sid)

    except Exception,e:
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
                ModifiedBY = "NA" if (wb.sheets()[0].cell(row, 4).value)== 'NULL' else int((wb.sheets()[0].cell(row, 4).value))
                Status = True if (wb.sheets()[0].cell(row, 6).value)=='Y' else False
                type = (wb.sheets()[0].cell(row, 7).value)

                value_list.append([PkCatID,Category,CreatedBY,ModifiedBY,Status,type])

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
                                is_deleted= not(value[4]),
                                membership_type=value[5]
                            )
                            MembershipCategoryobj.save()
                        except Exception, e:
                            print e
                            pass
                            transaction.rollback(sid)

                transaction.savepoint_commit(sid)
            except Exception,e:
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
            applicableto={'M': 'Members', 'A': 'Associates', 'I': 'Individual'}
            for row in range(1, number_of_rows):
                PkSlabID = int((wb.sheets()[0].cell(row, 0).value))
                Slab = (wb.sheets()[0].cell(row, 1).value)
                FKCatID = int((wb.sheets()[0].cell(row, 2).value))
                ApplicableTo = (wb.sheets()[0].cell(row, 3).value)
                AnnualFee = int((wb.sheets()[0].cell(row, 4).value))
                EntranceFee = int((wb.sheets()[0].cell(row, 5).value))
                CreatedBY = "NA" if (wb.sheets()[0].cell(row, 6).value)== 'NULL' else int((wb.sheets()[0].cell(row, 4).value))
                Status = True if (wb.sheets()[0].cell(row, 10).value)=='Y' else False
                cr3 = (wb.sheets()[0].cell(row, 11).value)

                value_list.append([PkSlabID,Slab,FKCatID,ApplicableTo,AnnualFee,EntranceFee,CreatedBY,Status,cr3])

            # print value_list

            sid = transaction.savepoint()
            try:
                for value in value_list:
                    try:
                        MembershipSlab.objects.get(code=value[0])
                    except MembershipSlab.DoesNotExist, e:
                        pass
                        try:
                            MembershipCategoryobj=MembershipCategory.objects.get(membership_code=value[2])
                            try:
                                try:
                                    if value[8] == 'N':
                                        slab_criteria='N'
                                    elif value[8] == 'L':
                                        slab_criteria = 'L'
                                    else:
                                        slab_criteria=int(value[8])

                                except Exception,e:
                                    print e
                                    slab_criteria = value[8]

                                SlabCriteriaobj=SlabCriteria.objects.get(slab_criteria=slab_criteria)
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
                                is_deleted= not(value[7]),
                                cr3=SlabCriteriaobj
                            )
                            MembershipSlabobj.save()
                            print MembershipSlabobj.id
                        except Exception, e:
                            print e
                            pass
                            transaction.rollback(sid)

                transaction.savepoint_commit(sid)
            except Exception,e:
                print e
                pass
    except Exception, e:
        print e



@transaction.atomic
def load_member_data():
    try:
        # file_path = ['/home/bynry01/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/a.xlsx']
        file_path = [file_dir + '/memberdata_new.xlsx']
        i = 0
        sid = transaction.savepoint()
        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns


            MEMBER_ASSOCIATION_TYPE = {'M': 'Member', 'A': 'Associate', 'L': 'Life Membership','I':'I'}

            for row in range(1,number_of_rows):
                row_values = []
                for col in range(114):
                    value = (wb.sheets()[0].cell(row, col).value)
                    row_values.append(value)
                try:
                    try:
                        UserDetail.objects.get(member_associate_no=row_values[4])
                    except UserDetail.DoesNotExist,e:
                        # print e
                        pass


                        """Start:Code to add member HOD Detail"""
                        # hod_detail_obj=HOD_Detail()
                        # hod_detail_obj.hr_name=row_values[8]
                        # # hod_detail_obj.hr_contact=row_values[0]
                        # hod_detail_obj.hr_email=row_values[9]
                        #
                        # hod_detail_obj.finance_name = row_values[10]
                        # # hod_detail_obj.finance_contact = row_values[0]
                        # hod_detail_obj.finance_email = row_values[11]
                        #
                        # hod_detail_obj.marketing_name = row_values[12]
                        # # hod_detail_obj.marketing_contact = row_values[0]
                        # hod_detail_obj.marketing_email = row_values[13]
                        #
                        # hod_detail_obj.IT_name = row_values[14]
                        # # hod_detail_obj.IT_contact = row_values[0]
                        # hod_detail_obj.IT_email = row_values[15]
                        #
                        # hod_detail_obj.corp_rel_name = row_values[16]
                        # # hod_detail_obj.corp_rel_contact = row_values[0]
                        # hod_detail_obj.corp_rel_email = row_values[17]
                        #
                        # hod_detail_obj.tech_name = row_values[18]
                        # # hod_detail_obj.tech_contact = row_values[0]
                        # hod_detail_obj.tech_email = row_values[19]
                        #
                        # hod_detail_obj.rnd_name = row_values[20]
                        # # hod_detail_obj.rnd_contact = row_values[0]
                        # hod_detail_obj.rnd_email = row_values[21]
                        #
                        # hod_detail_obj.exim_name = row_values[22]
                        # # hod_detail_obj.exim_contact = row_values[0]
                        # hod_detail_obj.exim_email = row_values[23]
                        #
                        # hod_detail_obj.created_by = "Admin"
                        #
                        # hod_detail_obj.save()

                        """End:Code to add member HOD Detail"""
                        #-----------------------#

                        """Start:Code to add member Company Detail"""
                        try:
                            company_detail_obj=CompanyDetail()

                            company_detail_obj.company_name=row_values[5]
                            # company_detail_obj.description_of_business=row_values[0]
                            company_detail_obj.establish_year=row_values[23] if row_values[23] != 'YYYY' else 0000
                            # company_detail_obj.company_scale=row_values[0]

                            # company_detail_obj.block_inv_plant=row_values[0]
                            # company_detail_obj.block_inv_land=row_values[0]
                            # company_detail_obj.block_inv_total=row_values[0]




                            # here country is many to many field
                            # company_detail_obj.exportcountry=row_values[43]
                            # company_detail_obj.importcountry=row_values[44]

                            company_detail_obj.textexport = row_values[30]
                            company_detail_obj.textimport = row_values[31]

                            company_detail_obj.rnd_facility=True if row_values[32] == 'Y' else False
                            company_detail_obj.govt_recognised=True if row_values[33] == 'Y' else False

                            company_detail_obj.iso = True if row_values[34] else False
                            company_detail_obj.iso_detail = row_values[34]

                            # company_detail_obj.foreign_collaboration=row_values[0]

                            company_detail_obj.eou= True if row_values[36] == 'Y' else False
                            # company_detail_obj.eou_detail=row_values[49]

                            company_detail_obj.total_manager=int(row_values[38]) if row_values[38] else 0
                            company_detail_obj.total_staff=int(row_values[39]) if row_values[39] else 0
                            company_detail_obj.total_workers=int(row_values[40]) if row_values[40] else 0
                            # company_detail_obj.total_employees=int(row_values[0])

                            # here industrydescription is many to many field

                            # company_detail_obj.industrydescription=int(row_values[55])

                            # here legalstatus is FK field
                            # company_detail_obj.legalstatus = int(row_values[54])

                            # here hoddetail is FK field
                            # company_detail_obj.hoddetail = hod_detail_obj

                            company_detail_obj.created_by = 'Admin'

                            company_detail_obj.save()

                            print "company Added"
                        except Exception,e:
                            print e
                            print row_values[30]
                            print row_values[31]
                            print row_values[32]
                            print row_values[33]
                            print row_values[34]
                            # print row_values[35]
                            print row_values[36]
                            print row_values[37]
                            print row_values[38]
                            print row_values[39]
                            print row_values[40]
                            traceback.print_exc()
                            print e
                            print e
                            print "-----------"
                            transaction.rollback(sid)
                            print abcd

                        """End:Code to add member Company Detail"""

                        #-------------

                        """Start:Code to add member User Detail"""
                        try:

                            user_detail_obj=UserDetail()
                            user_detail_obj.company=company_detail_obj

                            user_detail_obj.ceo_name=row_values[6]
                            user_detail_obj.ceo_email=row_values[19]
                            # user_detail_obj.ceo_designation=row_values[0]
                            user_detail_obj.ceo_cellno=row_values[17]

                            # user_detail_obj.person_name=row_values[6]
                            # user_detail_obj.person_email=row_values[0]
                            # user_detail_obj.person_designation=row_values[0]
                            # user_detail_obj.person_cellno=row_values[0]

                            user_detail_obj.correspond_address=row_values[7]
                            user_detail_obj.correspond_email=row_values[20]
                            # user_detail_obj.correspondstate=row_values[0]
                            try:
                                if row_values[9]:
                                    cityobj=City.objects.get(city_name=row_values[9])
                                    user_detail_obj.correspondcity = cityobj
                            except City.DoesNotExist,e:
                                print e
                                cityobj = City(city_name=row_values[9])
                                cityobj.save()
                                user_detail_obj.correspondcity = cityobj
                            except Exception,e:
                                print e
                                pass

                            user_detail_obj.correspond_pincode=row_values[11]
                            user_detail_obj.correspond_std1=row_values[13]
                            user_detail_obj.correspond_std2=row_values[14]
                            # user_detail_obj.correspond_landline1=row_values[28]
                            # user_detail_obj.correspond_landline2=row_values[28]

                            # user_detail_obj.factory_cellno=row_values[37]
                            # user_detail_obj.factory_address=row_values[33] + ' ' +row_values[34]
                            # user_detail_obj.factorystate=row_values[0]
                            # user_detail_obj.factorycity=row_values[35]
                            # user_detail_obj.factory_pincode=row_values[36]
                            # user_detail_obj.factory_std1=row_values[0]
                            # user_detail_obj.factory_std2=row_values[0]
                            # user_detail_obj.factory_landline1=row_values[0]
                            # user_detail_obj.factory_landline2=row_values[0]

                            user_detail_obj.website=row_values[22]
                            # user_detail_obj.gst=row_values[0]
                            # user_detail_obj.gst_in=row_values[0]
                            # user_detail_obj.pan=row_values[0]
                            # user_detail_obj.aadhar=row_values[0]
                            # user_detail_obj.awards=row_values[0]

                            # user_detail_obj.membership_type=row_values[0]
                            # user_detail_obj.enroll_type=row_values[0]
                            user_detail_obj.user_type= MEMBER_ASSOCIATION_TYPE[(row_values[3])]
                            user_detail_obj.member_associate_no=row_values[4]
                            """CHECK REQUIRED FORMAT DATE"""
                            user_detail_obj.membership_acceptance_date= datetime.datetime.strptime(row_values[45],'%Y-%m-%d %H:%M:%S.%f')

                            """FOREGIN KEY MembershipCategory and MembershipSlab """
                            try:
                                MembershipCategory_obj=MembershipCategory.objects.get(membership_code=int(row_values[1]))
                                user_detail_obj.membership_category = MembershipCategory_obj
                            except Exception,e:
                                pass

                            try:
                                MembershipSlab_obj=MembershipSlab.objects.get(code=int(row_values[2]))
                                user_detail_obj.membership_slab = MembershipSlab_obj
                            except Exception,e:
                                print row_values[2]
                                print "===slab---"
                                pass

                            user_detail_obj.annual_turnover_year=row_values[26]
                            user_detail_obj.annual_turnover_rupees=row_values[25]
                            user_detail_obj.membership_year=row_values[46]
                            # user_detail_obj.renewal_year=row_values[0]
                            # user_detail_obj.renewal_status=row_values[0]

                            #here membership_description is many to many field

                            # user_detail_obj.membership_description=row_values[0]

                            # user_detail_obj.exclude_from_mailing=row_values[0]
                            # user_detail_obj.valid_invalid_member=row_values[0]
                            # user_detail_obj.executive_committee_member=row_values[0]
                            # user_detail_obj.membership_ceritificate_dispatch=row_values[0]
                            # user_detail_obj.payment_method=row_values[0]
                            user_detail_obj.created_by='Admin'
                            user_detail_obj.save()
                        except Exception,e:
                            traceback.print_exc()
                            print e
                            print e
                            print "-----------"
                            print abcd
                            raise

                        print "user Added"

                        """End:Code to add member User Detail"""

                        """Start:Code to add MembershipInvoice & PaymentDetails"""
                        # try:
                        #     #Add total amount colmn in table
                        #     MembershipInvoiceobj=MembershipInvoice(
                        #         userdetail=user_detail_obj,
                        #         subscription_charges=0,
                        #         entrance_fees=row_values[98] if row_values[98] != 'NULL' else 0,
                        #         tax=row_values[99] if row_values[99] != 'NULL' else 0,
                        #         amount_payable=row_values[100] if row_values[100] != 'NULL' else 0,
                        #         without_adv_amount_payable=0,
                        #         financial_year=row_values[97] ,
                        #         last_due_amount=row_values[102] if row_values[102] != 'NULL' else 0 ,
                        #         last_advance_amount=row_values[101] if row_values[101] != 'NULL' else 0,
                        #         invoice_for=0,
                        #         is_paid=True,
                        #     )
                        #
                        #     MembershipInvoiceobj.save()
                        #
                        #     print "--------------------------------",MembershipInvoiceobj.id
                        #
                        #     PaymentDetailsobj = PaymentDetails(
                        #         userdetail=user_detail_obj,
                        #         membershipInvoice=MembershipInvoiceobj,
                        #         amount_payable=row_values[100] if row_values[100] != 'NULL' else 0 ,
                        #         amount_paid=row_values[104] if row_values[104] != 'NULL' else 0,
                        #         partial_amount_paid=0,
                        #         amount_last_advance=0,
                        #         amount_next_advance=0,
                        #         cheque_no=row_values[109] if row_values[109] != 'NULL' else 0,
                        #         bank_name=row_values[111] if row_values[111] != 'NULL' else 0,
                        #         receipt_no=row_values[113] if row_values[113] != 'NULL' else 0,
                        #         neft_transfer_id=0,
                        #         cash_amount=0,
                        #         # user_Payment_Type=row_values[105],
                        #         # payment_date=0,
                        #         financial_year=0,
                        #         bk_no=0,
                        #     )
                        #     PaymentDetailsobj.save()
                        #
                        #     try:
                        #         if row_values[45] != 'NULL':
                        #             PaymentDetailsobj.cheque_date = (datetime.datetime.strptime(row_values[45], '%Y-%m-%d %H:%M:%S.%f')).date()
                        #     except Exception,e:
                        #         print e
                        #         pass
                        #
                        #     try:
                        #         if row_values[112] != 'NULL':
                        #             PaymentDetailsobj.receipt_date = (datetime.datetime.strptime(row_values[112], '%Y-%m-%d %H:%M:%S.%f')).date()
                        #     except Exception,e:
                        #         print e
                        #         pass
                        #
                        #     PaymentDetailsobj.save()
                        #
                        # except Exception,e:
                        #     print e
                        #     traceback.print_exc()
                        #     pass

                        """End:Code to add MembershipInvoice & PaymentDetails"""

                        """Start:Code to create user login credential"""
                        try:
                            if row_values[57]:
                                if row_values[57] != '':
                                    try:
                                        MembershipUser.objects.get(userdetail=user_detail_obj)
                                    except MembershipUser.DoesNotExist,e:
                                        # print e

                                        try:
                                            MembershipUserobj=MembershipUser(
                                                userdetail=user_detail_obj,
                                                username=row_values[4],
                                                created_by='Admin'
                                            )
                                            MembershipUserobj.save()
                                            MembershipUserobj.set_password(row_values[57])
                                            MembershipUserobj.save()
                                            print "MembershipUse Added"
                                        except Exception,e:
                                            print e
                                            pass
                                    except Exception,e:
                                        print e
                        except Exception,e:
                            print e
                            traceback.print_exc()
                            pass
                        """End:Code to create user login credential"""

                except Exception,e:
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

def delete_mem_data():
    CompanyDetail.objects.all().delete()
    UserDetail.objects.all().delete()
    MembershipUser.objects.all().delete()

if __name__ == "__main__":
    # delete_data()
    # add_industrydescription()
    # add_membershipdescription()
    # add_legal_status()
    # add_mem_categary()
    # add_membershipslab()
    # load_member_data()
    delete_mem_data()

    # print not(True)
    pass


# username:medhak@mcciapune.com
# pw:awsmccia@2018

