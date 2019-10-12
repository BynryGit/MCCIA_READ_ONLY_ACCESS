import pdb
import traceback

from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from membershipapp.models import HOD_Detail, CompanyDetail,UserDetail,MembershipInvoice,PaymentDetails
from backofficeapp.view import membership_details
from adminapp.models import MembershipCategory,MembershipSlab,Country,SlabCriteria, LegalStatus, State, City,IndustryDescription,MembershipDescription
from eventsapp.models import EventDetails

############### require for recaptcha ###########
import urllib
import urllib2
import json
from django.conf import settings
from django.contrib import messages
import datetime
from datetime import date


# Save New Member
@transaction.atomic
def save_new_member(request):
    sid = transaction.savepoint()
    FactoryCityObj = ''
    try:
        print '\nRequest IN | membership.py | save_new_consumer | user %s', request.user

        IndustryDescriptionList = []
        MembershipDescriptionList = []
        data = request.POST
        print data
        print float(request.POST.get('subsciption_charges'))
        print request.POST.get('FactoryState')
        print '\n============================================================= Slab  ', request.POST.get('MembershipSlab')
        # captcha = request.POST.get('g - recaptcha - response')

        # ''' Begin reCAPTCHA validation '''
        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # print "recaptcha_response",recaptcha_response
        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # values = {
        #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # data = urllib.urlencode(values)
        # print data
        # req = urllib2.Request(url, data)
        # print "req", req
        # response = urllib2.urlopen(req)
        # result = json.load(response)
        # ''' End reCAPTCHA validation '''

        # if result['success']:
        #
        #     messages.success(request, 'New comment added with success!')
        # else:
        #     messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        if (request.POST.get('correspondence_GST') == "UnderProcess"):
            gst_option = "UP"
        elif (request.POST.get('correspondence_GST') == "Applicable"):
            gst_option = "AP"
        elif (request.POST.get('correspondence_GST') == "NotApplicable"):
            gst_option = "NA"

        # if request.POST.get('company_scale_radiobtn'):
        if (request.POST.get('radiobtn-1')):
            if (request.POST.get('radiobtn-1') == "Micro"):
                company_scale = "MR"
            elif (request.POST.get('radiobtn-1') == "Small"):
                company_scale = "SM"
            elif (request.POST.get('radiobtn-1') == "MediumScale"):
                company_scale = "MD"
            elif (request.POST.get('radiobtn-1') == "LargeScale"):
                company_scale = "LR"
        else:
            company_scale = "MR"

        try:
            hoddetail = HOD_Detail(
                hr_name=request.POST.get('HRName'),
                hr_contact=request.POST.get('HRContact'),
                hr_email=request.POST.get('HREmail'),
                finance_name=request.POST.get('FinanceName'),
                finance_contact=request.POST.get('FinanceContact'),
                finance_email=request.POST.get('FinanceEmail'),
                marketing_name=request.POST.get('MarketingName'),
                marketing_contact=request.POST.get('MarketingContact'),
                marketing_email=request.POST.get('MarketingEmail'),
                IT_name=request.POST.get('ITName'),
                IT_contact=request.POST.get('ITContact'),
                IT_email=request.POST.get('ITEmail'),
                corp_rel_name=request.POST.get('CorpRelName'),
                corp_rel_contact=request.POST.get('CorpRelContact'),
                corp_rel_email=request.POST.get('CorpRelEmail'),
                tech_name=request.POST.get('TechName'),
                tech_contact=request.POST.get('TechContact'),
                tech_email=request.POST.get('TechEmail'),
                rnd_name=request.POST.get('RandDName'),
                rnd_email=request.POST.get('RandDEmail'),
                rnd_contact=request.POST.get('RandDContact'),
                exim_name=request.POST.get('EXIMName'),
                exim_contact=request.POST.get('EXIMContact'),
                exim_email=request.POST.get('EXIMEmail'),
                stores_name=request.POST.get('StoreName'),
                stores_contact=request.POST.get('StoreContact'),
                stores_email=request.POST.get('StoreEmail'),
                purchase_name=request.POST.get('PurchaseName'),
                purchase_contact=request.POST.get('PurchaseContact'),
                purchase_email=request.POST.get('PurchaseEmail'),
                production_name=request.POST.get('ProductionName'),
                production_contact=request.POST.get('ProductionContact'),
                production_email=request.POST.get('ProductionEmail'),
                quality_name=request.POST.get('QualityName'),
                quality_contact=request.POST.get('QualityContact'),
                quality_email=request.POST.get('QualityEmail'),
                supply_chain_name=request.POST.get('SupplyName'),
                supply_chain_contact=request.POST.get('SupplyContact'),
                supply_chain_email=request.POST.get('SupplyEmail'),
                is_deleted=False
            )

        except Exception, exc:
            print 'exception in Hod Detail', str(traceback.print_exc())

        try:

            # if request.POST.get('RandDfacilityAvailable') == "RandDfacilityAvailable":
            #     rnd_facility = True
            # else:
            #     rnd_facility = False
            #
            # if request.POST.get('RandDfacilityAvailable') == "RecognisedbyGovt":
            #     govt_recognised = True
            # else:
            #     govt_recognised = False
            #
            # if request.POST.get('ForeignCollaborations') == "ForeignCollaborations":
            #     foreign_collaboration = True
            # else:
            #     foreign_collaboration = False
            # if request.POST.get('100EOU') == "100EOU":
            #     eou = True
            # else:
            #     eou = False
            #
            # if request.POST.get('ISOAwards'):
            #     isodetail = request.POST.get('ISOOtherStdsAwards')
            #     iso_check = True
            # else:
            #     isodetail = "NA"
            #     iso_check = False
                
            if request.POST.get('factoryAddressField') == "factoryAddressField":
                same_as_above = True
            else:
                same_as_above = False

            if request.POST.get('mailreceiveconfirmbox') == "mailreceiveconfirmbox":
                ceo_email_confirmation = True
            else:
                ceo_email_confirmation = False


            if request.POST.get('areaofexperties') =="Engineer":
                area_of_experties = 1
            elif request.POST.get('areaofexperties') =="CA":
                area_of_experties = 2
            elif request.POST.get('areaofexperties') =="Doctors":
                area_of_experties = 3
            elif request.POST.get('areaofexperties') == "Consultant":
                area_of_experties = 4
            elif request.POST.get('areaofexperties') == "Marketing_Professional":
                area_of_experties = 5
            elif request.POST.get('areaofexperties') == "Valuers":
                area_of_experties = 6
            elif request.POST.get('areaofexperties') == "individual_finance_brokers":
                area_of_experties = 7
            elif request.POST.get('areaofexperties') == "real_estate_broker":
                area_of_experties = 8
            elif request.POST.get('areaofexperties') == "lawyers_solicitors":
                area_of_experties = 9
            elif request.POST.get('areaofexperties') == "management_consultant":
                area_of_experties = 10
            elif request.POST.get('areaofexperties') == "trainers":
                area_of_experties = 11
            elif request.POST.get('areaofexperties') == "project_consultants":
                area_of_experties =  12
            elif request.POST.get('areaofexperties') =="others":
                area_of_experties = 13
            else:
                area_of_experties = 0



        except:
            # rnd_facility = False
            # govt_recognised = False
            # foreign_collaboration = False
            # eou = False
            same_as_above = False
            ceo_email_confirmation = False
            area_of_experties=0
            pass

        print "request.POST.getmembership_selection", request.POST.get("membership_selection")
        if (request.POST.get("membership_selection") == "Company"):
            if request.POST.get('PlantMcRs'):
                block_inv_plant = request.POST.get('PlantMcRs')
            else:
                block_inv_plant = 0
            if request.POST.get('LandBldgRs'):
                block_inv_land = request.POST.get('LandBldgRs')
            else:
                block_inv_land = 0
            if request.POST.get('TotalRsCr'):
                block_inv_total = request.POST.get('TotalRsCr')
            else:
                block_inv_total = 0

            if request.POST.get('Manager'):
                total_manager = request.POST.get('Manager')
            else:
                total_manager = 0

            if request.POST.get('Staff'):
                total_staff = request.POST.get('Staff')
            else:
                total_staff = 0
            if request.POST.get('Workers'):
                total_workers = request.POST.get('Workers')
            else:
                total_workers = 0
            if request.POST.get('Total'):
                total_employees = request.POST.get('Total')
            else:
                total_employees = 0

            if request.POST.get('CorrespondenceStd1') and request.POST.get('CorrespondenceLandline1'):
                correspondStd1 = request.POST.get('CorrespondenceStd1')
                CorrespondenceLandline1 = request.POST.get('CorrespondenceLandline1')
            elif request.POST.get('CorrespondenceLandline1'):
                correspondStd1 = ""
                CorrespondenceLandline1 = request.POST.get('CorrespondenceLandline1')
            else:
                correspondStd1 = ""
                CorrespondenceLandline1 = ""

            if request.POST.get('CorrespondenceStd2') and request.POST.get('CorrespondenceLandline2'):
                correspondStd2 = request.POST.get('CorrespondenceStd2')
                CorrespondenceLandline2 = request.POST.get('CorrespondenceLandline2')
            elif request.POST.get('CorrespondenceLandline2'):
                correspondStd2 = ""
                CorrespondenceLandline2 = request.POST.get('CorrespondenceLandline2')
            else:
                correspondStd2 = ""
                CorrespondenceLandline2 = ""

            ceo_name = request.POST.get('CEO')
            ceo_contact = request.POST.get('CEOContact')
            person_name = request.POST.get('CEO')
            person_email = request.POST.get('FactoryEmail')
            person_designation = request.POST.get('FactoryWebsite')

            factory_cellno = request.POST.get('FactoryContact')
            factory_address = request.POST.get('FactoryAddress')
            factorystate = State.objects.get(id=request.POST.get('FactoryState'))

            factorycity = City.objects.get(id=request.POST.get('FactoryCity'))
            factory_pincode = request.POST.get('FactoryPin')

            if request.POST.get('FactorySTD1'):
                factoryStd1 = request.POST.get('FactorySTD1')
                factory_landline1 = request.POST.get('FactoryLandline1')
            else:
                factoryStd1 = ""
                factory_landline1 = request.POST.get('FactoryLandline1')

            if request.POST.get('FactorySTD2'):
                factoryStd2 = request.POST.get('FactorySTD2')
                factory_landline2 = request.POST.get(
                    'FactoryLandline2')
            else:
                factoryStd2 = ""
                factory_landline2 = request.POST.get('FactoryLandline2')
            # factory_landline1 = request.POST.get('FactoryLandline2')
            # factory_landline2 = request.POST.get('FactoryLandline2')
            membership_type = "MM"
            enroll_type = "CO"
        else:
            if request.POST.get('CorrespondenceStd1') and request.POST.get('CorrespondenceLandline1'):
                correspondStd1 = request.POST.get('CorrespondenceStd1')
                CorrespondenceLandline1 = request.POST.get('CorrespondenceLandline1')
            elif request.POST.get('CorrespondenceLandline1'):
                correspondStd1 = ""
                CorrespondenceLandline1 = request.POST.get('CorrespondenceLandline1')
            else:
                correspondStd1 = ""
                CorrespondenceLandline1 = ""

            if request.POST.get('CorrespondenceStd2') and request.POST.get('CorrespondenceLandline2'):
                correspondStd2 = request.POST.get('CorrespondenceStd2')
                CorrespondenceLandline2 = request.POST.get('CorrespondenceLandline2')
            elif request.POST.get('CorrespondenceLandline2'):
                correspondStd2 = ""
                CorrespondenceLandline2 = request.POST.get('CorrespondenceLandline2')
            else:
                correspondStd2 = ""
                CorrespondenceLandline2 = request.POST.get('CorrespondenceLandline2')
            block_inv_plant = 0
            block_inv_land = 0
            block_inv_total = 0
            total_manager = 0
            total_staff = 0
            total_workers = 0
            total_employees = 0
            ceo_name = " "
            ceo_contact = " "
            person_name = " "
            person_email = " "
            person_designation = " "
            person_cellno = " "
            factory_cellno = ""
            factory_address = " "
            factorystate = State.objects.get(id=request.POST.get('CorrespondenceState'))
            factorycity = City.objects.get(id=request.POST.get('CorrespondenceCity'))
            factory_pincode = " "
            factoryStd1 = ""
            factoryStd2 = ""
            factory_landline1 = " "
            factory_landline2 = " "
            membership_type = "MM"
            enroll_type = "IN"

        if request.POST.get('YearofEstablishment'):
            yearOfEstablishment = request.POST.get('YearofEstablishment')
        else:
            yearOfEstablishment = 0

        if request.POST.get('DescriptionofBusiness'):
            description_of_business = request.POST.get('DescriptionofBusiness')
        else:
            description_of_business = ""

        if request.POST.get('turnover_range') == "to_0_1":
            turnover_range = 0

        elif request.POST.get('turnover_range') == "to_1_5":
            turnover_range = 1

        elif request.POST.get('turnover_range') == "to_5_25":
            turnover_range = 2

        elif request.POST.get('turnover_range') == "to_25_100":
            turnover_range = 3

        elif request.POST.get('turnover_range') == "to_100_500":
            turnover_range = 4

        elif request.POST.get('turnover_range') == "to_500":
            turnover_range = 5
        else:
            turnover_range = 0

        if request.POST.get('employee_range') == "emp_0_10":
            employee_range = 0

        elif request.POST.get('employee_range') == "emp_10_100":
            employee_range = 1

        elif request.POST.get('employee_range') == "emp_100_500":
            employee_range = 2

        elif request.POST.get('employee_range') == "emp_500_1000":
            employee_range = 3

        elif request.POST.get('employee_range') == "emp_1000+":
            employee_range = 4
        else:
            employee_range = 0

        if request.POST.get('legalStatus'):
            legal_var = request.POST.get('legalStatus')
        else:
            legal_var = 61

        try:
            print "______________________", LegalStatus.objects.get(id=61)
            print "_________description_of_business_____________", description_of_business
            print "______yearOfEstablishment_____________", yearOfEstablishment
            print "____________ceo_email_confirmation__________", ceo_email_confirmation
            print "_________turnover_range_____________", turnover_range
            print "________employee_range______________", employee_range
            print "___________________legalStatus_______________", legal_var
            company_detail = CompanyDetail(
                company_name=request.POST.get('CompanyApplicantName'),
                description_of_business=description_of_business,
                establish_year=yearOfEstablishment,
                company_scale=company_scale,
                block_inv_plant=block_inv_plant,
                block_inv_land=block_inv_land,
                block_inv_total=block_inv_total,
                textexport=request.POST.get('TextExport'),
                textimport=request.POST.get('TextImport'),
                # rnd_facility=rnd_facility,
                # govt_recognised=govt_recognised,
                # iso=iso_check,
                # iso_detail=isodetail,
                # foreign_collaboration=foreign_collaboration,
                # eou=eou,
                eou_detail=request.POST.get('NameCountries'),
                total_manager=total_manager,
                total_staff=total_staff,
                total_workers=total_workers,
                total_employees=total_employees,
                same_as_above=same_as_above,
                turnover_range=turnover_range,
                employee_range=employee_range,
                ceo_email_confirmation=ceo_email_confirmation,
                industrydescription_other=request.POST.get('otherindustry_discription'),
                # industrydescription=IndustryDescription.objects.get(id=request.POST.get('industry_description')),
                legalstatus=LegalStatus.objects.get(id=legal_var),
                is_deleted=False)
        except Exception, exc:
            print 'exception in Company Detail Saving ', str(traceback.print_exc())

        if request.POST.get('CorrespondenceAadharCheck') == "on":
            aadhar_no = 0
        else:
            aadhar_no = request.POST.get('CorrespondenceAadhar')

        if request.POST.get('CorrespondencePanCheck') == "on":
            panNo = "NA"
        else:
            panNo = request.POST.get('CorrespondencePan')

        if request.POST.get('CorrespondenceGSTText'):
            CorrespondenceGSTText = request.POST.get('CorrespondenceGSTText')
        else:
            CorrespondenceGSTText = 'NA'

        try:
            userDetail = UserDetail(
                ceo_name=ceo_name,
                ceo_email = request.POST.get('CEOEmail') if request.POST.get('CEOEmail') else request.POST.get('CEOEmailin'),
                ceo_designation=ceo_name,
                ceo_cellno=ceo_contact,
                person_cellno=request.POST.get('CorrespondenceContact'),
                correspond_cellno=request.POST.get('CorrespondenceContact'),
                correspond_address=request.POST.get('CorrespondenceAddress'),
                correspond_email=request.POST.get('CorrespondenceEmail'),
                correspondstate=State.objects.get(id=request.POST.get('CorrespondenceState')),
                correspondcity=City.objects.get(id=request.POST.get('CorrespondenceCity')),
                correspond_pincode=request.POST.get('CorrespondencePin'),
                correspond_std1=correspondStd1,
                correspond_std2=correspondStd2,
                correspond_landline1=CorrespondenceLandline1,
                correspond_landline2=CorrespondenceLandline2,
                poc_name=request.POST.get('pocName') if request.POST.get('pocName') else None,
                poc_contact=request.POST.get('POCContact') if request.POST.get('POCContact') else None,
                poc_email=request.POST.get('POCEmail') if request.POST.get('POCEmail') else None,
                website=request.POST.get('CorrespondenceWebsite'),
                gst=CorrespondenceGSTText,
                gst_in=gst_option,
                pan=panNo,
                aadhar=aadhar_no,
                # awards=isodetail,
                person_name=person_name,
                person_email=person_email,
                person_designation=person_designation,
                factory_cellno=factory_cellno,
                factory_address=factory_address,
                factorystate=factorystate,
                factorycity=factorycity,
                factory_pincode=factory_pincode,
                factory_std1=factoryStd1,
                factory_std2=factoryStd2,
                factory_landline1=factory_landline1,
                factory_landline2=factory_landline2,
                membership_type=membership_type,
                enroll_type=enroll_type,
                membership_category=MembershipCategory.objects.get(id=request.POST.get('MembershipCategory')),
                annual_turnover_year=request.POST.get('foryear'),
                annual_turnover_rupees=request.POST.get('Rscrore'),
                membership_slab=MembershipSlab.objects.get(id=request.POST.get('MembershipSlab')),
                membership_year=str(request.POST.get('MembershipForYear'))[0:9],
                area_of_experties=area_of_experties,
                experties_other=request.POST.get('otherareaofexperties'),
                updated_date=datetime.datetime.now()
            )
            #
        except Exception, exc:
            print exc
            print 'exception in USER DETAIL SAVING ', str(traceback.print_exc())

        print request.POST.get('entrance_fee')

        hoddetail.save()
        company_detail.save()
        if hoddetail:
            hod_id = HOD_Detail.objects.get(id=hoddetail.id)
        else:
            hod_id = ''
        company_detail.hoddetail = hod_id
        company_detail.save()
        exportList = []
        if data.has_key('multi-select-export-country'):
            exportList = request.POST.get('multi-select-export-country')
            for i in request.POST.getlist('multi-select-export-country'):
                company_detail.exportcountry.add(i)
            company_detail.save()
        if data.has_key('multi-select-import-country'):
            # importList = request.POST.get('multi-select-import-country')
            for i in request.POST.getlist('multi-select-import-country'):
                company_detail.importcountry.add(i)
                company_detail.save()

        userDetail.save()
        userDetail.company_id = company_detail.id
        user_Payment_Type = request.POST.get("paymentType")
        print "user_Payment_Type", user_Payment_Type, request.POST.get("paymentMode")
        # if (request.POST.get("paymentMode") == "OfflinePending"):
        #     userDetail.payment_method = "Offline Pending"
        #     if user_Payment_Type == "ByCash":
        #         cash_amount = request.POST.get('cash_amount')
        #         cheque_date = None
        #         user_Payment_Type = "Cash"
        #     elif user_Payment_Type == "ByCheque":
        #         cheque_date = None
        #         user_Payment_Type = "Cheque"
        #     else:
        #         user_Payment_Type = "NEFT"

            # cheque_no = request.POST.get('Cheque_no')
            # cheque_date = datetime.datetime.strptime(request.POST.get('cheque_date'), '%d/%m/%Y')
            # bank_name = request.POST.get('bank_name')
        userDetail.payment_method = "Offline Pending"
        userDetail.save()

        if data.has_key('IndustryDescription'):
            for i in request.POST.getlist('IndustryDescription'):
                company_detail.industrydescription.add(i)
                company_detail.save()

        member_invoice_obj = MembershipInvoice(userdetail_id=userDetail.id,
                                               subscription_charges=float(request.POST.get('subsciption_charges')),
                                               entrance_fees=float(request.POST.get('entrance_fee')),
                                               tax=float(request.POST.get('tax_amount')),
                                               amount_payable=float(request.POST.get('payable_amount')),
                                               financial_year=str(request.POST.get('MembershipForYear'))[0:9],
                                               membership_category=userDetail.membership_category,
                                               membership_slab=userDetail.membership_slab
                                               )
        member_invoice_obj.save()

        paymentDetails_obj = PaymentDetails(userdetail_id=userDetail.id,
                                            membershipInvoice_id=member_invoice_obj.id,
                                            user_Payment_Type=user_Payment_Type,
                                            financial_year=str(request.POST.get('MembershipForYear'))[0:9],
                                            amount_payable=float(request.POST.get('payable_amount')))
        paymentDetails_obj.save()

        print "userDetail.membership_category.enroll_type", userDetail.membership_category.enroll_type
        if userDetail.membership_category.enroll_type == "Life Membership":
            userDetail.user_type = "Life Membership"
        else:
            userDetail.user_type = "Associate"
        userDetail.save()
        transaction.savepoint_commit(sid)
        response_data = {'success': True, 'payment_id': str(paymentDetails_obj.id)}
        print '\nRequest OUT | membership.py | save_new_consumer | user %s', request.user
        return response_data
    except Exception, exc:
        response_data = {'success': False}
        print '\nException | membership.py | save_new_consumer | user %s. Exception = ', str(traceback.print_exc())
        transaction.rollback(sid)
        return response_data