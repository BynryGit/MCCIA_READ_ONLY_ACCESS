
import traceback
import datetime
from email.mime.image import MIMEImage

from xlrd import open_workbook
from django.db import transaction
from adminapp.models import MembershipCategory,MembershipSlab,SlabCriteria, State, City, Country
from django.http import HttpResponse

from xlrd import xldate_as_tuple




@transaction.atomic
def load_membership_category_data(request):
    try:

        #file_path = ['/srv/wsgi/membership_category.xlsx']

        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    try:
                        x = str((wb.sheets()[0].cell(row, col).value)).split('.')
                        if len(x) > 1:
                            if (len(str(x[0])) == 2 and len(str(x[1])) > 5) or str(x[0]) == '00':
                                value = str(value)
                            else:
                                value = str(int(value))
                    except ValueError:
                        pass
                    finally:
                        row_values.append(value)

                values.append(row_values)
            sid = transaction.savepoint()
            for value in values:
                print "value--------", value
             

                MembershipCategory.objects.filter(enroll_type=value[1],membership_code=value[0],membership_category=value[3],category_enroll_type=value[0]).delete()
                membership_category = MembershipCategory(
                    membership_code=value[0],
                    membership_category=value[3],
                    category_enroll_type=value[2],
                    enroll_type=value[1],
                    is_deleted=False
                )
                membership_category.save()
            transaction.savepoint_commit(sid)
        print "load_membership_category_data is updated======="
    except Exception, e:
        print 'Exception In|Adminapp|import_data.py|load_membership_category_data', str(traceback.print_exc())
        transaction.rollback(sid)
        print 'Exception In|Adminapp|import_data.py|load_membership_category_data', e



@transaction.atomic
def load_criteria_data(request):
    try:

        #file_path = ['/srv/wsgi/SlabsCriteria.xlsx']

        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    try:
                        x = str((wb.sheets()[0].cell(row, col).value)).split('.')
                        if len(x) > 1:
                            if (len(str(x[0])) == 2 and len(str(x[1])) > 5) or str(x[0]) == '00':
                                value = str(value)
                            else:
                                value = str(int(value))
                    except ValueError:
                        pass
                    finally:
                        row_values.append(value)

                values.append(row_values)
            sid = transaction.savepoint()
            for value in values:
                print "value--------",value[0]

                SlabCriteria.objects.filter(slab_criteria=value[1]).delete()
                slabcriteria = SlabCriteria(
                    slab_criteria=value[1],
                    status=True,
                    is_deleted=False
                )
                slabcriteria.save()
            transaction.savepoint_commit(sid)
        print "load_slab_criteria_data is updated======="
    except Exception, e:
        print 'Exception In|Adminapp|import_data.py|load_slab_criteria_data', str(traceback.print_exc())
        transaction.rollback(sid)
        print 'Exception In|Adminapp|import_data.py|load_slab_criteria_data', e




@transaction.atomic
def load_slab_data(request):
    try:

        #file_path = ['/srv/wsgi/MembershipSlabsNew.xlsx']

        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print 'number_of_rows', number_of_rows
            print 'number_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    try:
                        x = str((wb.sheets()[0].cell(row, col).value)).split('.')
                        if len(x) > 1:
                            if (len(str(x[0])) == 2 and len(str(x[1])) > 5) or str(x[0]) == '00':
                                value = str(value)
                            else:
                                value = str(int(value))
                    except ValueError:
                        pass
                    finally:
                        row_values.append(value)

                values.append(row_values)
            sid = transaction.savepoint()
            for value in values:
                print "value--------", value[0],value[3],value[9]

                membershipCategoryObj = MembershipCategory.objects.get(membership_category=value[3],category_enroll_type=value[2],enroll_type=value[1],is_deleted=False)
                MembershipSlab.objects.filter(code=value[0],slab_type=value[2],slab=value[4],applicableTo=value[5],annual_fee=value[6],entrance_fee=value[7]).delete()

                # if value[8] == 'NA':
                #     slab_criteria = SlabCriteria.objects.get(slab_criteria=value[8])
                # else:
                #     slabcriteriaObj=
                # slab_criteria = slabcriteriaObj
                membership_slab = MembershipSlab(
                    code=value[0],
                    enroll_type=value[1],
                    slab_type=value[2],
                    membershipCategory_id=membershipCategoryObj.id,
                    slab=value[4],
                    applicableTo=value[5],
                    annual_fee=value[6],
                    entrance_fee=value[7],
                    cr3=SlabCriteria.objects.get(slab_criteria=value[9]),
                    status=True,
                    is_deleted=False
                )
                membership_slab.save()

                # if value[0] == '88':
                #     break
                # else:
                #     pass
            transaction.savepoint_commit(sid)
            print "load_slab_data is updated======="
    except Exception, e:
        print 'Exception In|Adminapp|import_data.py|load_slab_data', str(traceback.print_exc())
        transaction.rollback(sid)
        print 'Exception In|Adminapp|import_data.py|load_slab_data', e

@transaction.atomic
def load_state_data(request):
    try:

        file_path = ['/home/ec2-user/City.xlsx']

        i = 0
        for file in file_path:
            print file
            wb = open_workbook(file)
            values = []
            number_of_rows = wb.sheets()[0].nrows
            number_of_columns = wb.sheets()[0].ncols
            print '\nnumber_of_rows', number_of_rows
            print '\nnumber_of_columns', number_of_columns

            for row in range(1, number_of_rows):
                row_values = []
                for col in range(number_of_columns):
                    value = (wb.sheets()[0].cell(row, col).value)
                    try:
                        x = str((wb.sheets()[0].cell(row, col).value)).split('.')
                        if len(x) > 1:
                            if (len(str(x[0])) == 2 and len(str(x[1])) > 5) or str(x[0]) == '00':
                                value = str(value)
                            else:
                                value = str(int(value))
                    except ValueError:
                        pass
                    finally:
                        row_values.append(value)

                values.append(row_values)
            sid = transaction.savepoint()
            try:
                for value in values: 
                    print '>>>>>>>>>>>',value[1]
                                  
                    city_obj = City(
                        city_name=value[1], 
                        state_id=2,
                        created_by='admin'             
                    )
                    city_obj.save()
                transaction.savepoint_commit(sid)
                print "City Details is updated======="
                i = i + 1
            except Exception as e:
                print e
                     
        return HttpResponse(200)
    except Exception, e:
        print 'Exception In|Adminapp|Helper.py|load_state_data', str(traceback.print_exc())
        transaction.rollback(sid)
        print 'Exception In|Adminapp|Helper.py|load_state_data', e
        return HttpResponse(500)





# @transaction.atomic
# def load_visa_data(request):
#     try:
#         file_path = ['/home/ec2-user/visa2.xlsx']

#         i = 0
#         for file in file_path:
#             print file
#             wb = open_workbook(file)
# @transaction.atomic
# def load_visa_data(request):
#     try:
#         file_path = ['/home/ec2-user/visa2.xlsx']

#         i = 0
#         for file in file_path:
#             print file
#             wb = open_workbook(file)
#             values = []
#             number_of_rows = wb.sheets()[0].nrows
#             number_of_columns = wb.sheets()[0].ncols
#             print '\nnumber_of_rows', number_of_rows
#             print '\nnumber_of_columns', number_of_columns

#             for row in range(1, number_of_rows):
#                 row_values = []
#                 for col in range(number_of_columns):
#                     value = (wb.sheets()[0].cell(row, col).value)

#                     row_values.append(value)

#                 values.append(row_values)

#             print '......................SHUBHAM...............',values
#             sid = transaction.savepoint()
#             try:
#                 for value in values:    
#                     embacy_obj = Country(
#                         country_name=str(value[0]), 
#                         updated_by='Admin'
#                     )
#                     embacy_obj.save()  
#                     print 'lasttttttttttttttttttttttttttttttttt',embacy_obj

#                 transaction.savepoint_commit(sid)
#                 print "Visa is updated======="
#                 i = i + 1
#             except Exception as e:
#                 print '.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',e
                     
#         return HttpResponse(200)
#     except Exception, e:
#         print 'Exception In|Adminapp|Helper.py|load_state_data', str(traceback.print_exc())
#         transaction.rollback(sid)
#         print 'Exception In|Adminapp|Helper.py|load_state_data', e
#         return HttpResponse(500)
#             values = []
#             number_of_rows = wb.sheets()[0].nrows
#             number_of_columns = wb.sheets()[0].ncols
#             print '\nnumber_of_rows', number_of_rows
#             print '\nnumber_of_columns', number_of_columns

#             for row in range(1, number_of_rows):
#                 row_values = []
#                 for col in range(number_of_columns):
#                     value = (wb.sheets()[0].cell(row, col).value)

#                     row_values.append(value)

#                 values.append(row_values)

#             print '......................SHUBHAM...............',values
#             sid = transaction.savepoint()
#             try:
#                 for value in values:    
#                     embacy_obj = Country(
#                         country_name=str(value[0]), 
#                         updated_by='Admin'
#                     )
#                     embacy_obj.save()  
#                     print 'lasttttttttttttttttttttttttttttttttt',embacy_obj

#                 transaction.savepoint_commit(sid)
#                 print "Visa is updated======="
#                 i = i + 1
#             except Exception as e:
#                 print '.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',e
                     
#         return HttpResponse(200)
#     except Exception, e:
#         print 'Exception In|Adminapp|Helper.py|load_state_data', str(traceback.print_exc())
#         transaction.rollback(sid)
#         print 'Exception In|Adminapp|Helper.py|load_state_data', e
#         return HttpResponse(500)

# from visarecommendationapp.models import PlaceOfEmbassy
# @transaction.atomic
# def load_embassy_data(request):
#     try:
#         file_path = ['/home/ec2-user/visa.xlsx']

#         i = 0
#         for file in file_path:
#             print file
#             wb = open_workbook(file)
#             values = []
#             number_of_rows = wb.sheets()[0].nrows
#             number_of_columns = wb.sheets()[0].ncols
#             print '\nnumber_of_rows', number_of_rows
#             print '\nnumber_of_columns', number_of_columns

#             for row in range(1, number_of_rows):
#                 row_values = []
#                 for col in range(number_of_columns):
#                     value = (wb.sheets()[0].cell(row, col).value)

#                     row_values.append(value)

#                 values.append(row_values)

#             sid = transaction.savepoint()
#             try:
#                 for value in values:    
#                     country_obj = Country.objects.get(country_name=str(value[0]))
#                     print '>>>>>>>>>>>>>>>>',country_obj
#                     embacy_obj = PlaceOfEmbassy(
#                         embassy_name=str(value[1]), 
#                         address=str(value[1]), 
#                         country=country_obj
#                     )
#                     embacy_obj.save()  

#                 transaction.savepoint_commit(sid)
#                 print "Visa is updated======="
#                 i = i + 1
#             except Exception as e:
#                 print 'Exception In|Adminapp|Helper.py|load_state_data', str(traceback.print_exc())
#                 #transaction.rollback(sid)
#                 print 'Exception In|Adminapp|Helper.py|load_state_data', e
#                 return HttpResponse(500)
                     
#         return HttpResponse(200)
#     except Exception, e:
#         print 'Exception In|Adminapp|Helper.py|load_state_data', str(traceback.print_exc())
#         transaction.rollback(sid)
#         print 'Exception In|Adminapp|Helper.py|load_state_data', e
#         return HttpResponse(500)
