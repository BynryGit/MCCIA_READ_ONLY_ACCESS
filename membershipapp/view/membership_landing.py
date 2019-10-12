import hashlib
import pdb
import traceback
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db import transaction
from django.db.models import Q, Max
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from membershipapp.models import HOD_Detail, CompanyDetail,UserDetail,MembershipInvoice,PaymentDetails
from backofficeapp.view.membership_details import send_mail_offline_payment
from backofficeapp.view import membership_details
from adminapp.models import MembershipCategory,MembershipSlab,Country,SlabCriteria, LegalStatus, State, City,IndustryDescription,MembershipDescription
from eventsapp.models import EventDetails, EventBannerImage, EventRegistration
from Paymentapp.models import PendingTransaction, MembershipPaymentTransaction
from Paymentapp.view.common import add_to_pending
from publicationapp.models import PublicationFile
from visarecommendationapp.models import Membership_Visa_Recommendations

############### require for recaptcha ###########
import urllib
import urllib2
import json
from django.conf import settings
from django.contrib import messages
import datetime
from datetime import date
from django.contrib.sites.shortcuts import get_current_site
from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required
from mediaapp.models import MCCIABanner

# try:  # Python 2.7+
#     from logging import NullHandler
# except ImportError:
#     class NullHandler(logging.Handler):
#         def emit(self, record):
#             pass

# log = logging.getLogger(__name__)
# log.addHandler(NullHandler())


# import sys
# sys.stdout = sys.stderr


def membership_home(request):
    return render(request, 'membership/membership.html')


def member_benifits(request):
    return render(request, 'membership/member-benifits.html')


def eligibility_criteria(request):
    return render(request, 'membership/eligibility-crieteria.html')    


def about_us(request):
    return render(request, 'about_us/about_us.html')


def maha_industry_policy(request):
    company_obj = CompanyDetail.objects.get(id=42030)
    company_obj.updated_by = int(company_obj.updated_by) + 1
    company_obj.save()
    my_file = open('/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/sitemedia/Manual_Uploaded_Documents/Maharashtra_Industrial_Policy_2019.pdf', 'rb').read()
    return HttpResponse(my_file, content_type="application/pdf")


def mh_govt_amnesty_scheme_2019(request):
    hod_detail_obj = HOD_Detail.objects.get(id=36)
    hod_detail_obj.updated_by = int(hod_detail_obj.updated_by) + 1
    hod_detail_obj.save()
    my_file = open('/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/sitemedia/Manual_Uploaded_Documents/MAHARASHTRA_ORDINANCE_No._V_OF_2019.pdf', 'rb').read()
    return HttpResponse(my_file, content_type="application/pdf")


def mccia_one_pager_2019(request):    
    my_file = open('/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/sitemedia/Manual_Uploaded_Documents/MCCIA_One_Pager_2019.pdf', 'rb').read()
    return HttpResponse(my_file, content_type="application/pdf")


def national_guidelines_on_responsible_business_conduct_2019(request):    
    my_file = open('/home/ec2-user/NEW_MCCIA_BACKOFFICE/MCCIA_BACKOFFICE/sitemedia/Manual_Uploaded_Documents/National_Guildelines_on_Responsible_Business_Conduct_March_2019.pdf', 'rb').read()
    return HttpResponse(my_file, content_type="application/pdf")


# For giving data to intern
from django.http import HttpResponse
from xlsxwriter import Workbook
from datetime import datetime, timedelta
from hallbookingapp.models import HallBooking,HallBookingDetail,HallLocation,HallDetail, HallCheckAvailability, HallPaymentDetail, HallEquipment,BookingDetailHistory, Holiday, HallBookingDepositDetail, UserTrackDetail
import datetime
import io
def get_hall_booking_data():
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
                       'Email', 'Total Amount', 'Status']

        for i in range(len(column_name)):
            worksheet1.write_string(0, int(i), column_name[i])

        booking_details = HallBookingDetail.objects.filter(hall_location__location='MCCIA Trade Tower (5th Floor)').exclude(booking_status__in=[0, 10])
        for hallbooking in booking_details:
            # final_booking_details = HallBookingDetail.objects.filter(hall_booking=hallbooking.hall_booking)
            # for booking_detail in final_booking_details:
            if hallbooking.hall_detail:
                hall_name = hallbooking.hall_detail.hall_name
            else:
                hall_name = 'NA'
            if hallbooking.updated_by:
                time_slot = str(hallbooking.booking_from_date.astimezone(to_zone).time().strftime('%I:%M %p')) + '-' + \
                            str(hallbooking.booking_to_date.astimezone(to_zone).time().strftime(
                                '%I:%M %p')) + '\n'
            else:
                time_slot = str(hallbooking.booking_from_date.strftime('%I:%M %p')) + '-' + \
                            str(hallbooking.booking_to_date.strftime('%I:%M %p')) + '\n'
            date_slot = str(hallbooking.booking_from_date.strftime('%B %d,%Y')) + '\n'

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
            worksheet1.write_string(i, 14, str(hallbooking.hall_booking.get_booking_status_display()))
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

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())



def landing_page(request):
    try:        
        print '\nRequest IN | membership_landing | landing_page | user = ',request.user

        banner_obj_list = MCCIABanner.objects.filter(is_expired=False,is_deleted=False)
        banner_doc_list = []            

        for obj in banner_obj_list:
            docs_address = 'https://' + get_current_site(request).domain + obj.document_files.url
            data = {'docs_address': docs_address,'banner_link': obj.banner_link}
            banner_doc_list.append(data)

        publication_list = PublicationFile.objects.filter(id__in=[item['max_of'] for item in PublicationFile.objects.filter(is_deleted=False).values('publication_type').annotate(max_of=Max('id'))]).order_by('publication_type')

        final_event_list = []
        event_detail_list = EventDetails.objects.filter(view_status=1,event_status=0,is_deleted=False).order_by('from_date')
        for obj in event_detail_list:
            start_date = str(obj.from_date.strftime('%d %B %Y %I:%M %p'))
            end_date = str(obj.to_date.strftime('%d %B %Y %I:%M %p'))

            when_to_attend = start_date + ' To ' + end_date
            if obj.from_date.strftime("%d %M %Y") == obj.to_date.strftime("%d %M %Y"):
                when_to_attend = str(obj.from_date.strftime('%d %B %Y %I:%M %p')) + ' - ' + str(obj.to_date.strftime('%I:%M %p'))

            if obj.hall_details:
                location = obj.hall_details.hall_location.location
            else:
                location = obj.other_location_address

            try:
                event_banner_obj = EventBannerImage.objects.get(event_detail_id_id=obj.id)
                docs_address = 'https://' + get_current_site(request).domain + event_banner_obj.document_files.url
            except Exception, e:
                print e,str(obj.id)
                # print >> sys.stdout, '\nEEEEEERRRRRRRRROOOOOOOOOORRRRRRRR ========== ', str(obj.id)
                docs_address = ''
                log.debug('Error 1 = {0}\n'.format(e))
                pass

            event_dict = {
                'id':obj.id,
                'event_date':obj.from_date.strftime('%d'),
                'event_title':obj.event_title,
                'when_to_attend':when_to_attend,
                'event_location':location,
                'docs_address':docs_address
            }
            final_event_list.append(event_dict)
        data = {
            'final_event_list':final_event_list,
            'banner_doc_list':banner_doc_list,
            'publication_list': publication_list
        }        
        print 'Request OUT | membership_landing | landing_page | user %s', request.user
    except Exception as e:
        print 'Exception | membership_landing | landing_page | user %s. Exception = ', e
        log.debug('Error 2 = {0}\n'.format(e))
        data ={}        
    return render(request, 'landing_page.html',data)


def elected_member(request):
    return render(request, 'about_us/elected-member.html')


def co_members(request):
    return render(request, 'about_us/co-members.html')


def chairman_committee(request):
    return render(request, 'about_us/chairman-committee.html')


def special_invitees(request):
    return render(request, 'about_us/special-invitees.html')


def article_of_association(request):
    return render(request, 'membership/article-of-association.html')


# Member can Edit Profile - Landing Page
def edit_member_profile(request):
    data = {}
    try:
        print '\nRequest IN | membership_landing | edit_member_profile | user %s', request.user

        member_obj = request.user.membershipuser.userdetail
    

        membershipCategory = MembershipCategory.objects.filter(is_deleted=False)
        industrydescObj = IndustryDescription.objects.filter(is_deleted=False)
        legalstatusObj = LegalStatus.objects.filter(is_deleted=False)
        stateObj = State.objects.filter(is_deleted=False)
        cityObj = City.objects.filter(state=member_obj.correspondstate, is_deleted=False)
        fact_cityObj = City.objects.filter(state=member_obj.factorystate, is_deleted=False)
        countryObj = Country.objects.filter(is_deleted=False)
        membershipDescriptionObj = MembershipDescription.objects.filter(is_deleted=False)

        data = {
            'industrydescObj': industrydescObj, 'legalstatusObj': legalstatusObj, 'stateObj': stateObj,
            'cityObj': cityObj, 'countryObj': countryObj, 'membershipDescriptionObj': membershipDescriptionObj,
            'membershipCategory': membershipCategory, 'fact_cityObj': fact_cityObj, 'member_obj': member_obj,
            'export_country_list': str(
                member_obj.company.textexport.split(",")) if member_obj.company.textexport else None,
            'import_country_list': str(
                member_obj.company.textimport.split(",")) if member_obj.company.textimport else None
        }

        print '\nResponse OUT | membership_landing | edit_member_profile | user %s', request.user
    except Exception, e:
        print 'Exception| membership_landing | edit_member_profile = ', traceback.print_exc()
        data = {'msg': 'error'}
    return render(request, 'membership/edit_member_profile.html', data)


# Update Member Profile - Front End
@transaction.atomic
@csrf_exempt
def update_member_profile(request):
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_landing | update_member_profile | user %s', request.user
        print "_________areaofexperties___________________",request.POST.get('areaofexperties')


        IndustryDescriptionList = []
        MembershipDescriptionList = []
        data = request.POST
        factory_cellno =''

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

        if request.POST.get('correspondence_GST') == "UnderProcess":
            gst_option = "UP"
        elif request.POST.get('correspondence_GST') == "Applicable":
            gst_option = "AP"
        elif request.POST.get('correspondence_GST') == "NotApplicable":
            gst_option = "NA"

        # if request.POST.get('company_scale_radiobtn'):
        if request.POST.get('radiobtn-1'):
            if request.POST.get('radiobtn-1') == "Micro":
                company_scale = "MR"
            elif request.POST.get('radiobtn-1') == "Small":
                company_scale = "SM"
            elif request.POST.get('radiobtn-1') == "MediumScale":
                company_scale = "MD"
            elif request.POST.get('radiobtn-1') == "LargeScale":
                company_scale = "LR"
        else:
            company_scale = "MR"

        userDetail_obj = UserDetail.objects.get(id=request.POST.get('edit_member_id'))
        userDetail_obj.poc_name = request.POST.get("pocName")
        userDetail_obj.poc_contact = request.POST.get("POCContact")
        userDetail_obj.poc_email = request.POST.get("POCEmail")
        userDetail_obj.save()

        userDetail = UserDetail.objects.get(id=request.POST.get('edit_member_id'))
        company_detail = CompanyDetail.objects.get(id=userDetail.company.id)
        hoddetail = ''

        try:
            if company_detail.hoddetail:
                hoddetail = HOD_Detail.objects.get(id=company_detail.hoddetail.id)
                hoddetail.hr_name = request.POST.get('HRName')
                hoddetail.hr_contact = request.POST.get('HRContact')
                hoddetail.hr_email = request.POST.get('HREmail')
                hoddetail.finance_name = request.POST.get('FinanceName')
                hoddetail.finance_contact = request.POST.get('FinanceContact')
                hoddetail.finance_email = request.POST.get('FinanceEmail')
                hoddetail.marketing_name = request.POST.get('MarketingName')
                hoddetail.marketing_contact = request.POST.get('MarketingContact')
                hoddetail.marketing_email = request.POST.get('MarketingEmail')
                hoddetail.IT_name = request.POST.get('ITName')
                hoddetail.IT_contact = request.POST.get('ITContact')
                hoddetail.IT_email = request.POST.get('ITEmail')
                hoddetail.corp_rel_name = request.POST.get('CorpRelName')
                hoddetail.corp_rel_contact = request.POST.get('CorpRelContact')
                hoddetail.corp_rel_email = request.POST.get('CorpRelEmail')
                hoddetail.tech_name = request.POST.get('TechName')
                hoddetail.tech_contact = request.POST.get('TechContact')
                hoddetail.tech_email = request.POST.get('TechEmail')
                hoddetail.rnd_name = request.POST.get('RandDName')
                hoddetail.rnd_email = request.POST.get('RandDEmail')
                hoddetail.rnd_contact = request.POST.get('RandDContact')
                hoddetail.exim_name = request.POST.get('EXIMName')
                hoddetail.exim_contact = request.POST.get('EXIMContact')
                hoddetail.exim_email = request.POST.get('EXIMEmail')
                hoddetail.stores_name = request.POST.get('StoreName')
                hoddetail.stores_contact = request.POST.get('StoreContact')
                hoddetail.stores_email = request.POST.get('StoreEmail')
                hoddetail.purchase_name = request.POST.get('PurchaseName')
                hoddetail.purchase_contact = request.POST.get('PurchaseContact')
                hoddetail.purchase_email = request.POST.get('PurchaseEmail')
                hoddetail.production_name = request.POST.get('ProductionName')
                hoddetail.production_contact = request.POST.get('ProductionContact')
                hoddetail.production_email = request.POST.get('ProductionEmail')
                hoddetail.quality_name = request.POST.get('QualityName')
                hoddetail.quality_contact = request.POST.get('QualityContact')
                hoddetail.quality_email = request.POST.get('QualityEmail')
                hoddetail.supply_chain_name = request.POST.get('SupplyName')
                hoddetail.supply_chain_contact = request.POST.get('SupplyContact')
                hoddetail.supply_chain_email = request.POST.get('SupplyEmail')

            else:
                new_hoddetail_obj = HOD_Detail(hr_name=request.POST.get('HRName'), hr_contact=request.POST.get('HRContact'), hr_email=request.POST.get('HREmail'),
                            finance_name = request.POST.get('FinanceName'),finance_contact = request.POST.get('FinanceContact'), finance_email = request.POST.get('FinanceEmail'),
                            marketing_name=request.POST.get('MarketingName'),marketing_contact=request.POST.get('MarketingContact'),marketing_email=request.POST.get('MarketingEmail'),
                            IT_name=request.POST.get('ITName'), IT_contact=request.POST.get('ITContact'), IT_email=request.POST.get('ITEmail'),
                            corp_rel_name=request.POST.get('CorpRelName'),corp_rel_contact=request.POST.get('CorpRelContact'),corp_rel_email=request.POST.get('CorpRelEmail'),
                            tech_name=request.POST.get('TechName'), tech_contact=request.POST.get('TechContact'), tech_email=request.POST.get('TechEmail'),
                            rnd_name=request.POST.get('RandDName'), rnd_email=request.POST.get('RandDEmail'), rnd_contact=request.POST.get('RandDContact'),
                            exim_name=request.POST.get('EXIMName'), exim_contact=request.POST.get('EXIMContact'), exim_email=request.POST.get('EXIMEmail'),
                            stores_name=request.POST.get('StoreName'),stores_contact=request.POST.get('StoreContact'),stores_email=request.POST.get('StoreEmail'),
                            purchase_name=request.POST.get('PurchaseName'),purchase_contact=request.POST.get('PurchaseContact'),purchase_email=request.POST.get('PurchaseEmail'),
                            production_name=request.POST.get('ProductionName'),production_contact=request.POST.get('ProductionContact'),production_email=request.POST.get('ProductionEmail'),
                            quality_name=request.POST.get('QualityName'),quality_contact=request.POST.get('QualityContact'),quality_email=request.POST.get('QualityEmail'),
                            supply_chain_name=request.POST.get('SupplyName'),supply_chain_contact=request.POST.get('SupplyContact'),supply_chain_email=request.POST.get('SupplyEmail'))
                new_hoddetail_obj.save()
                company_detail.hoddetail = new_hoddetail_obj
                company_detail.save()
                hoddetail = new_hoddetail_obj                
                pass

        except Exception, exc:
            print 'exception in Hod Detail', str(traceback.print_exc())

        try:

            # if request.POST.get('RandDfacilityAvailable') == "RandDfacilityAvailable":
            #     rnd_facility = True
            # else:
            #     rnd_facility = False
            #
            # if request.POST.get('RecognisedbyGovt') == "RecognisedbyGovt":
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
            # if request.POST.get('ISOAwards') == "YES":
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

            if request.POST.get('areaofexperties') == "Engineer":
                area_of_experties = 1
            elif request.POST.get('areaofexperties') == "CA":
                area_of_experties = 2
            elif request.POST.get('areaofexperties') == "Doctors":
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
                area_of_experties = 12
            elif request.POST.get('areaofexperties') == "others":
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
            area_of_experties= 0

            # iso_check = False
            pass

        print "request.POST.getmembership_selection", request.POST.get("check_user_type")

        if (request.POST.get("check_user_type") == "CO"):

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

            ceo_name = request.POST.get('CEO')
            ceo_contact = request.POST.get('CEOContact')
            person_name = request.POST.get('CEO')
            person_email = request.POST.get('FactoryEmail')
            person_designation = request.POST.get('FactoryWebsite')
            person_cellno = request.POST.get('FactoryContact')
            factory_address = request.POST.get('FactoryAddress')
            factorystate = State.objects.get(id=request.POST.get('FactoryState'))

            factorycity = City.objects.get(id=request.POST.get('FactoryCity'))
            factory_pincode = request.POST.get('FactoryPin')
            factory_std1 = request.POST.get('FactorySTD1')
            factory_std2 = request.POST.get('FactorySTD2')
            factory_landline1 = request.POST.get('FactoryLandline2')
            factory_landline2 = request.POST.get('FactoryLandline2')
            factory_cellno = request.POST.get('FactoryContact')
            membership_type = "MM"
            enroll_type = "CO"
        else:
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
            factory_address = " "
            factorystate = State.objects.get(id=request.POST.get('CorrespondenceState'))
            factorycity = City.objects.get(id=request.POST.get('CorrespondenceCity'))
            factory_pincode = " "
            factory_std1 = " "
            factory_std2 = " "
            factory_landline1 = " "
            factory_landline2 = " "
            membership_type = "MM"
            enroll_type = "IN"

        if request.POST.get('YearofEstablishment'):
            yearOfEstablishment = request.POST.get('YearofEstablishment')
        else:
            yearOfEstablishment = 0

        userDetail = UserDetail.objects.get(id=request.POST.get('edit_member_id'))
        try:
            company_detail = CompanyDetail.objects.get(id=userDetail.company.id)
            company_detail.company_name = request.POST.get('CompanyApplicantName')
            company_detail.description_of_business = request.POST.get('DescriptionofBusiness')
            company_detail.establish_year = yearOfEstablishment
            company_detail.company_scale = company_scale
            company_detail.block_inv_plant = block_inv_plant
            company_detail.block_inv_land = block_inv_land
            company_detail.block_inv_total = block_inv_total
            company_detail.textexport = request.POST.get('TextExport')
            company_detail.textimport = request.POST.get('TextImport')
            # company_detail.rnd_facility = rnd_facility
            # company_detail.govt_recognised = govt_recognised
            # company_detail.iso = iso_check
            # company_detail.iso_detail = isodetail
            # company_detail.foreign_collaboration = foreign_collaboration
            # company_detail.eou = eou
            company_detail.eou_detail = request.POST.get('NameCountries')
            company_detail.total_manager = total_manager
            company_detail.total_staff = total_staff
            company_detail.total_workers = total_workers
            company_detail.total_employees = total_employees
            company_detail.same_as_above = same_as_above
            company_detail.ceo_email_confirmation = ceo_email_confirmation
            company_detail.industrydescription_other = request.POST.get('otherindustry_discription')


            # industrydescription=IndustryDescription.objects.get(id=request.POST.get('industry_description')),
            company_detail.legalstatus = LegalStatus.objects.get(id=request.POST.get('legalStatus'))
        except Exception, exc:
            print 'exception in Company Detail Saving ', str(traceback.print_exc())

        if request.POST.get('CorrespondenceAadharCheck') == "on":
            aadhar_no = 0
        else:
            aadhar_no = str(request.POST.get('CorrespondenceAadhar'))


        if request.POST.get('CorrespondencePanCheck') == "on":
            panNo = "NA"
        else:
            panNo = request.POST.get('CorrespondencePan')

        if request.POST.get('CorrespondenceGSTText'):
            CorrespondenceGSTText = request.POST.get('CorrespondenceGSTText')
        else:
            CorrespondenceGSTText = 'NA'
        try:
            userDetail = UserDetail.objects.get(id=request.POST.get('edit_member_id'))

            userDetail.ceo_name = ceo_name
            # userDetail.ceo_email = request.POST.get('CEOEmail') if request.POST.get('CEOEmail') else request.POST.get('CEOEmailin')
            userDetail.ceo_designation = ceo_name
            userDetail.ceo_cellno = ceo_contact
            if (request.POST.get("check_user_type") == "CO"):
                userDetail.ceo_email = request.POST.get('CEOEmail')
            else:
                userDetail.ceo_email=request.POST.get('CEOEmailin')




            userDetail.correspond_address = request.POST.get('CorrespondenceAddress')
            userDetail.correspond_email = request.POST.get('CorrespondenceEmail')
            userDetail.correspondstate = State.objects.get(id=request.POST.get('CorrespondenceState'))
            userDetail.correspondcity = City.objects.get(id=request.POST.get('CorrespondenceCity'))
            userDetail.correspond_cellno = request.POST.get('CorrespondenceContact')
            userDetail.correspond_pincode = request.POST.get('CorrespondencePin')
            userDetail.correspond_std1 = request.POST.get('CorrespondenceStd1')
            userDetail.correspond_std2 = request.POST.get('CorrespondenceStd2')
            userDetail.correspond_landline1 = request.POST.get('CorrespondenceLandline1')
            userDetail.correspond_landline2 = request.POST.get('CorrespondenceLandline2')
            userDetail.website = request.POST.get('CorrespondenceWebsite')
            userDetail.gst = CorrespondenceGSTText
            userDetail.gst_in = gst_option
            userDetail.pan = panNo
            userDetail.aadhar = str(aadhar_no)
            # userDetail.awards = isodetail
            userDetail.person_name = person_name
            userDetail.person_email = person_email
            userDetail.person_designation = person_designation
            userDetail.person_cellno = str(request.POST.get('CorrespondenceContact'))
            userDetail.factory_address = factory_address
            userDetail.factorystate = factorystate
            userDetail.factorycity = factorycity
            userDetail.factory_pincode = factory_pincode
            userDetail.factory_std1 = factory_std1
            userDetail.factory_std2 = factory_std2
            userDetail.factory_landline1 = factory_landline1
            userDetail.factory_landline2 = factory_landline2
            userDetail.factory_cellno = factory_cellno
            userDetail.membership_type = membership_type
            userDetail.enroll_type = enroll_type
            userDetail.area_of_experties = area_of_experties
            userDetail.experties_other = request.POST.get('otherareaofexperties')
            # userDetail.membership_category = MembershipCategory.objects.get(id=request.POST.get('MembershipCategory'))
            # userDetail.annual_turnover_year = request.POST.get('foryear')
            # userDetail.annual_turnover_rupees = request.POST.get('Rscrore')
            # userDetail.membership_slab = MembershipSlab.objects.get(id=request.POST.get('MembershipSlab'))
            # userDetail.membership_year = str(request.POST.get('MembershipForYear'))[0:9]

        except Exception, exc:
            print 'exception in USER DETAIL SAVING ', str(traceback.print_exc())

        print request.POST.get('entrance_fee')

        if company_detail.hoddetail:
            hoddetail.save()
        else:
            pass
        company_detail.save()
        if hoddetail:
            hod_id = HOD_Detail.objects.get(id=hoddetail.id)
        else:
            hod_id = None
        company_detail.hoddetail = hod_id
        company_detail.save()
        exportList = []        
        if request.POST.get('multi-select-export-country'):
            exportList = request.POST.getlist('multi-select-export-country')
            for i in exportList:
                print '\n i = ',i
                exportcountryobj = Country.objects.get(id=i)
                company_detail.exportcountry.add(exportcountryobj)
                company_detail.save()
        if request.POST.get('multi-select-import-country'):
            importList = request.POST.getlist('multi-select-import-country')
            for i in importList:
                importcountryobj = Country.objects.get(id=i)
                company_detail.importcountry.add(importcountryobj)
                company_detail.save()

        userDetail.save()
        userDetail.company_id = company_detail.id

        company_detail.industrydescription.clear()
        for key, value in data.iteritems():
            valueList = []
            print value
            if str(key) == 'IndustryDescription':
                value = request.POST.getlist('IndustryDescription')
                valueList = value
                for j in value:
                    print "----------------value-------------------", j
                    company_detail.industrydescription.add(j)
                    company_detail.save()

        transaction.savepoint_commit(sid)
        # member_invoice(request, userDetail.id, userDetail.membership_year)

        data = {'success': 'true'}
        print '\nResponse OUT | membership_landing | update_member_profile | user %s', request.user
    except Exception, e:
        data = {'success': 'false'}
        print '\nException| membership_landing | update_member_profile = ', str(traceback.print_exc())
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Member can Renew Membership - Landing Page
def renew_member_profile_page(request):
    data = {}
    try:
        print '\nRequest IN | membership_landing | renew_member_profile_page | user %s', request.user

        user_detail_obj = request.user.membershipuser.userdetail
        membershipCategory = MembershipCategory.objects.filter(status=True)
        industrydescObj = IndustryDescription.objects.filter(is_active=True)
        legalstatusObj = LegalStatus.objects.filter(status=True)

        current_year = datetime.datetime.now()
        next_year = current_year + relativedelta(years=+1)

        year_list = []
        i = 0
        to_current_year = datetime.datetime.now()
        prev_year = to_current_year - relativedelta(years=+1)
        while i < 5:
            year_list.append(str(prev_year.year) + '-' + str(to_current_year.year))
            prev_year = prev_year - relativedelta(years=+1)
            to_current_year = to_current_year - relativedelta(years=+1)
            i = i + 1

        data = {
            'industrydescObj': industrydescObj, 'legalstatusObj': legalstatusObj,
            'membershipCategory': membershipCategory, 'member_obj': user_detail_obj,
            'formatted_renewal_year': str(request.session['renewal_year']),
            'year_list': year_list, 'renewal_year': str(request.session['renewal_year'])
        }

        print '\nResponse OUT | membership_landing | renew_member_profile_page | user %s', request.user
    except Exception,e:
        print 'Exception| membership_landing | renew_member_profile_page = ', traceback.print_exc()
    return render(request, 'membership/renew_member_profile.html', data)


def membership_form(request):
    data = {}
    membershipCategory = MembershipCategory.objects.filter(status=True, is_deleted=False)
    industrydescObj = IndustryDescription.objects.filter(is_active=True,is_deleted=False)
    legalstatusObj = LegalStatus.objects.filter(status=True,is_deleted=False)
    stateObj = State.objects.filter(is_deleted=False)
    cityObj = City.objects.filter(is_deleted=False)
    countryObj = Country.objects.filter(is_deleted=False)
    membershipDescriptionObj = MembershipDescription.objects.filter(is_deleted=False)
    turnoverangeObj = CompanyDetail.objects.filter(is_deleted=False)
    data = {'industrydescObj': industrydescObj, 'legalstatusObj': legalstatusObj, 'stateObj': stateObj,
            'cityObj': cityObj, 'countryObj': countryObj,'membershipDescriptionObj':membershipDescriptionObj,'membershipCategory':membershipCategory,'turnoverangeObj':turnoverangeObj}
    return render(request, 'membership/membership-form-page.html',data)


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Registration'],login_url='/backofficeapp/login/',raise_exception=True)
def membership_form_admin(request):
    data = {}
    membershipCategory = MembershipCategory.objects.filter(status=True,is_deleted=False)
    industrydescObj = IndustryDescription.objects.filter(is_active=True,is_deleted=False)
    legalstatusObj = LegalStatus.objects.filter(status=True,is_deleted=False)
    stateObj = State.objects.filter(is_deleted=False)
    cityObj = City.objects.filter(is_deleted=False)
    countryObj = Country.objects.filter(is_deleted=False)
    membershipDescriptionObj = MembershipDescription.objects.filter(is_deleted=False)
    data = {'industrydescObj': industrydescObj, 'legalstatusObj': legalstatusObj, 'stateObj': stateObj,
            'cityObj': cityObj, 'countryObj': countryObj,'membershipDescriptionObj':membershipDescriptionObj,
            'membershipCategory':membershipCategory}

    return render(request, 'membership/membership_form_admin.html',data)


from sets import Set


def get_slab(request):
    try:
        print '\nRequest IN | membership_landing | get_slab | User = ', request.user
        data = {}
        slabRangeList=[]
        slabCriteriaList=[]
        slab_criteriaList=[]
        a=[]
        b=[]
        membershipSlabObj = []
        membershipCategoryObj = MembershipCategory.objects.get(id=request.GET.get('membershipCategory'), is_deleted=False)

        user_type = 'Associates'
        if request.user.is_anonymous():
            user_type = 'Associates'
        else:
            member_obj = request.user.membershipuser.userdetail
            if member_obj.user_type == 'Associate':
                user_type = 'Associates'
            elif member_obj.user_type == 'Member':
                user_type = 'Members'
            elif member_obj.user_type != 'Associate' and member_obj.user_type != 'Member' and member_obj.user_type != 'Life Membership':
                user_type = 'Individual'

        if request.GET.get('annual_turnover_Rscrore'):
            annual_turnover_Rscrore = request.GET.get('annual_turnover_Rscrore')
        else:
            annual_turnover_Rscrore = 0

        slabCriteriaObj = SlabCriteria.objects.filter(is_deleted=False)

        for i in slabCriteriaObj:
            try:
                if i.slab_criteria == "NA":
                    # print '------slab_criteriaList------',slab_criteriaList
                    slab_criteriaList.append(i.slab_criteria)

                else:
                    a = i.slab_criteria.split('-')[0]
                    b = i.slab_criteria.split('-')[1]
                    check_val=annual_turnover_Rscrore
                    if ((float(check_val) >= float(a)) and (float(check_val) <= float(b))):
                        slab_criteriaList.append(i.slab_criteria)
                    else:
                        pass
            except (IndexError, ValueError):
                pass
                # slab_criteriaList.append(i.slab_criteria)

        print '\nslab_criteriaList = ',slab_criteriaList
        if slab_criteriaList:
            slab_criteriaList= slab_criteriaList
        else:
            slab_criteria = ''
        for i in slab_criteriaList:
            abc = 60
            slabCriteriaObj = SlabCriteria.objects.get(slab_criteria=i,is_deleted=False)
            print slabCriteriaObj.slab_criteria

            try:
                if float(annual_turnover_Rscrore) == float(abc):
                    membershipSlabObjs = MembershipSlab.objects.filter(~Q(slab="Cttee. Membership") & Q(applicableTo=user_type),
                                                                       membershipCategory_id=membershipCategoryObj.id,cr3_id=slabCriteriaObj.id,status=True,is_deleted=False)
                elif float(annual_turnover_Rscrore) > float(abc) :
                    if slabCriteriaObj.slab_criteria == "NA":                        

                        if membershipCategoryObj.enroll_type == "Annual":
                            membershipSlabObjs = MembershipSlab.objects.filter(~Q(slab="Cttee. Membership") & Q(applicableTo=user_type),
                                                                               membershipCategory_id=membershipCategoryObj.id, cr3_id=slabCriteriaObj.id, status=True,is_deleted=False)
                        elif membershipCategoryObj.membership_category == "Professional":
                            # membershipSlabObjs = MembershipSlab.objects.filter((Q(slab="Patron Membership") & Q(applicableTo=user_type)),
                                                                               # membershipCategory_id=membershipCategoryObj.id, cr3_id=slabCriteriaObj.id, status=True,is_deleted=False)                            
                            # print '\nmembershipSlabObjs = ',membershipSlabObjs
                            # continue

                        # if membershipCategoryObj.membership_category == "Professional":
                            membershipSlabObjs = MembershipSlab.objects.filter((~Q(slab="Cttee. Membership") & Q(applicableTo=user_type)),
                                                                                    membershipCategory_id=membershipCategoryObj.id,
                                                                                    cr3_id=slabCriteriaObj.id, is_deleted=False)
                        elif membershipCategoryObj.membership_category == "Life Memb-small prop":
                            # membershipSlabObjs = MembershipSlab.objects.filter(Q(applicableTo=user_type),membershipCategory_id=membershipCategoryObj.id,cr3_id=slabCriteriaObj.id,is_deleted=False)
                            # print '\nElse prof slab = ',membershipSlabObjs
                            membershipSlabObjs = MembershipSlab.objects.filter(membershipCategory_id=membershipCategoryObj.id,applicableTo=user_type,
                                                                                cr3_id=slabCriteriaObj.id, is_deleted=False)
                        else:
                            membershipSlabObjs = MembershipSlab.objects.filter((Q(slab="Patron Membership") & Q(applicableTo=user_type)),
                                                                               membershipCategory_id=membershipCategoryObj.id, cr3_id=slabCriteriaObj.id, status=True,is_deleted=False)                            

                    else:
                        membershipSlabObjs = MembershipSlab.objects.filter((Q(applicableTo=user_type)),
                                                                           membershipCategory_id=membershipCategoryObj.id,cr3_id=slabCriteriaObj.id, status=True, is_deleted=False)

                else:
                    if membershipCategoryObj.membership_category == "Professional":
                        membershipSlabObjs = MembershipSlab.objects.filter((~Q(slab="Cttee. Membership") & Q(applicableTo=user_type)),
                                                                           membershipCategory_id=membershipCategoryObj.id,
                                                                           cr3_id=slabCriteriaObj.id, is_deleted=False)
                    else:
                        membershipSlabObjs = MembershipSlab.objects.filter(Q(applicableTo=user_type),membershipCategory_id=membershipCategoryObj.id,cr3_id=slabCriteriaObj.id,is_deleted=False)

                    print "membershipSlabObjs",membershipSlabObjs
            except Exception, exc:
                print 'exception ', str(traceback.print_exc())
            for i in membershipSlabObjs:
                print '\ni = ',i
                membershipSlabObj.append({'membershipSlab_id': i.id, 'membershipSlab_name': i.slab +' - Rs ' + i.annual_fee + ' - ' + i.applicableTo})
        data = {'membershipSlabObj': membershipSlabObj}        
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_slab_admin(request):
    try:
        data = {}
        slabRangeList=[]
        slabCriteriaList=[]
        slab_criteriaList=[]
        a=[]
        b=[]
        membershipSlabObj = []
        # membershipCategory = '+membershipCategory+"annual_turnover_foryear="+annual_turnover_foryear+"annual_turnover_Rscrore="+annual_turnover_Rscrore
        membershipCategoryObj = MembershipCategory.objects.get(id=request.GET.get('membershipCategory'), is_deleted=False)
        if request.GET.get('annual_turnover_Rscrore'):
            annual_turnover_Rscrore = request.GET.get('annual_turnover_Rscrore')
        else:
            annual_turnover_Rscrore = 0

        # if annual_turnover_Rscrore in range(0,0):
        #     slab_criteria='0-0.05'


        slabCriteriaObj = SlabCriteria.objects.filter(is_deleted=False)
        for i in slabCriteriaObj:
            #slab_criteriaList = []
            # slab_criteria = i.slab_criteria


            try:
                if i.slab_criteria == "NA":
                    # print '------slab_criteriaList------',slab_criteriaList
                    slab_criteriaList.append(i.slab_criteria)
                #
                # elif annual_turnover_Rscrore == "0.50":
                #     slab_criteriaList.append(i.slab_criteria)

                else:
                    a = i.slab_criteria.split('-')[0]
                    b = i.slab_criteria.split('-')[1]
                    check_val=annual_turnover_Rscrore
                    if ((float(check_val) > float(a)) and (float(check_val) <= float(b))):
                        slab_criteriaList.append(i.slab_criteria)
                    else:
                        pass
            except (IndexError, ValueError):
                pass
                # slab_criteriaList.append(i.slab_criteria)


        if slab_criteriaList:
            print '\nslab_criteriaList = ',slab_criteriaList

            slab_criteriaList= slab_criteriaList
        else:
            slab_criteria =''


        for i in slab_criteriaList:
            abc = 60
            slabCriteriaObj = SlabCriteria.objects.get(slab_criteria=i,is_deleted=False)
            try:
                if float(annual_turnover_Rscrore) == float(abc) :
                    membershipSlabObjs = MembershipSlab.objects.filter(membershipCategory_id=membershipCategoryObj.id,cr3_id=slabCriteriaObj.id,status=True,is_deleted=False)
                elif float(annual_turnover_Rscrore) > float(abc):
                    if slabCriteriaObj.slab_criteria == "NA":

                        membershipSlabObjs = MembershipSlab.objects.filter((Q(slab="Patron Membership")),membershipCategory_id=membershipCategoryObj.id, cr3_id=slabCriteriaObj.id,status=True,is_deleted=False)
                    else:
                        membershipSlabObjs = MembershipSlab.objects.filter(membershipCategory_id=membershipCategoryObj.id, cr3_id=slabCriteriaObj.id,status=True,is_deleted=False)
                else:
                    membershipSlabObjs = MembershipSlab.objects.filter(membershipCategory_id=membershipCategoryObj.id,cr3_id=slabCriteriaObj.id,status=True,is_deleted=False)
            except Exception, exc:
                print 'exception ', str(traceback.print_exc())
            for i in membershipSlabObjs:
                membershipSlabObj.append({'membershipSlab_id': i.id, 'membershipSlab_name': i.slab +' - Rs ' + i.annual_fee + ' - ' + i.applicableTo})
        data = {'membershipSlabObj': membershipSlabObj}
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_membership_category(request):
    try:
        data = {}
        membershipCategoryList = []
        print request.GET.get("radiobtn_membership_selection")

        if request.GET.get("radiobtn_membership_selection") == "Company":
            membershipCategoryObj = MembershipCategory.objects.filter(category_enroll_type='Organizational',status=True, is_deleted=False)
        else:
            membershipCategoryObj = MembershipCategory.objects.filter(category_enroll_type='Individual',status=True, is_deleted=False)

        for i in membershipCategoryObj:
            membershipCategoryList.append({'id':i.id,'membership_category':i.membership_category +' - '+i.enroll_type})
        data = {'membershipCategoryObj':membershipCategoryList}
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_city(request):
    try:
        data = {}
        cityObj = []

        stateObj = State.objects.get(id=request.GET.get('state'),is_deleted=False)
        cityObjs = City.objects.filter(state_id=stateObj.id,is_deleted=False)

        for i in cityObjs:
            cityObj.append({'city_id':i.id,'city_name':i.city_name})
        data = {'cityObj':cityObj}
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic()
@csrf_exempt
def save_new_member(request):
    sid = transaction.savepoint()
    FactoryCityObj=''
    try:
        print '\nRequest IN | mccia_landing | save_new_consumer | user %s', request.user

        IndustryDescriptionList = []
        MembershipDescriptionList = []

        data = request.POST
        print data
        print float(request.POST.get('subsciption_charges'))
        print request.POST.get('FactoryState')
        print "_______________________________________",request.POST.get('turnover_range')
        print "____________________________________________",request.POST.get('employee_range')
        print "_________________mailreceiveconfirmbox___________________",request.POST.get('mailreceiveconfirmbox')
        print "________________areaofexperties____________",request.POST.get('areaofexperties')
        print "___________otherareaofexperties______________________",request.POST.get('otherareaofexperties')
        print "_______________legalStatus_________________",request.POST.get('legalStatus')
        print "_________________factoryAddressField_________________",request.POST.get('factoryAddressField')
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
                        hr_name = request.POST.get('HRName'),
                        hr_contact = request.POST.get('HRContact'),
                        hr_email = request.POST.get('HREmail'),
                        finance_name = request.POST.get('FinanceName'),
                        finance_contact = request.POST.get('FinanceContact'),
                        finance_email = request.POST.get('FinanceEmail'),
                        marketing_name = request.POST.get('MarketingName'),
                        marketing_contact = request.POST.get('MarketingContact'),
                        marketing_email = request.POST.get('MarketingEmail'),
                        IT_name = request.POST.get('ITName'),
                        IT_contact = request.POST.get('ITContact'),
                        IT_email = request.POST.get('ITEmail'),
                        corp_rel_name = request.POST.get('CorpRelName'),
                        corp_rel_contact = request.POST.get('CorpRelContact'),
                        corp_rel_email = request.POST.get('CorpRelEmail'),
                        tech_name = request.POST.get('TechName'),
                        tech_contact = request.POST.get('TechContact'),
                        tech_email = request.POST.get('TechEmail'),
                        rnd_name = request.POST.get('RandDName'),
                        rnd_email = request.POST.get('RandDEmail'),
                        rnd_contact = request.POST.get('RandDContact'),
                        exim_name = request.POST.get('EXIMName'),
                        exim_contact = request.POST.get('EXIMContact'),
                        exim_email = request.POST.get('EXIMEmail'),
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
            # if request.POST.get('RecognisedbyGovt') == "RecognisedbyGovt":
            #     govt_recognised =True
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
            # if request.POST.get('ISOAwards') :
            #     isodetail = request.POST.get('ISOOtherStdsAwards')
            #     iso_check = True
            # else:
            #     isodetail = "NA"
            #     iso_check =False
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
                area_of_experties =4
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
                area_of_experties = 12
            elif request.POST.get('areaofexperties') =="others":
                area_of_experties = 13
            else:
                area_of_experties = 0
        except:
            # rnd_facility = False
            # govt_recognised = False
            # foreign_collaboration = False
            # eou=False
            same_as_above=False
            ceo_email_confirmation=False
            area_of_experties=0
            pass

        print "request.POST.getmembership_selection",request.POST.get("membership_selection")
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
                correspondStd2 =request.POST.get('CorrespondenceStd2')
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
            if request.POST.get('FactoryState'):
                factorystate = State.objects.get(id=request.POST.get('FactoryState')) 
            else:
                factorystate = None
            if request.POST.get('FactoryCity'):
                factorycity = City.objects.get(id=request.POST.get('FactoryCity'))
            else:
                factorycity = None
            factory_pincode = request.POST.get('FactoryPin') if request.POST.get('FactoryPin') else 0


            if request.POST.get('FactorySTD1'):
                factoryStd1 = request.POST.get('FactorySTD1')
                factory_landline1 =request.POST.get('FactoryLandline1')
            else:
                factoryStd1 =""
                factory_landline1 = request.POST.get('FactoryLandline1')

            if request.POST.get('FactorySTD2'):
                factoryStd2 = request.POST.get('FactorySTD2')
                factory_landline2 =request.POST.get(
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
            elif request.POST.get('CorrespondenceLandline1') :
                correspondStd1 = ""
                CorrespondenceLandline1 = request.POST.get('CorrespondenceLandline1')
            else:
                correspondStd1 = ""
                CorrespondenceLandline1 = ""


            if request.POST.get('CorrespondenceStd2') and request.POST.get('CorrespondenceLandline2'):
                correspondStd2 =request.POST.get('CorrespondenceStd2')
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
            if request.POST.get('FactoryState'):
                factorystate = State.objects.get(id=request.POST.get('FactoryState')) 
            else:
                factorystate = None
            if request.POST.get('FactoryCity'):
                factorycity = City.objects.get(id=request.POST.get('FactoryCity'))
            else:
                factorycity = None
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
            company_detail=CompanyDetail(
                            company_name = request.POST.get('CompanyApplicantName'),
                            description_of_business = description_of_business,
                            establish_year = yearOfEstablishment,
                            company_scale = company_scale,
                            block_inv_plant = block_inv_plant,
                            block_inv_land = block_inv_land,
                            block_inv_total = block_inv_total,
                            textexport = request.POST.get('TextExport'),
                            textimport = request.POST.get('TextImport'),
                            # rnd_facility = rnd_facility,
                            # govt_recognised = govt_recognised,
                            # iso = iso_check,
                            # iso_detail = isodetail,
                            # foreign_collaboration = foreign_collaboration,
                            # eou = eou,
                            eou_detail=request.POST.get('NameCountries'),
                            total_manager = total_manager,
                            total_staff = total_staff,
                            total_workers = total_workers,
                            total_employees = total_employees,
                            same_as_above = same_as_above,
                            ceo_email_confirmation = ceo_email_confirmation,
                            turnover_range = turnover_range,
                            employee_range = employee_range,
                            industrydescription_other = request.POST.get('otherindustry_discription'),
                            # industrydescription=IndustryDescription.objects.get(id=request.POST.get('industry_description')),
                            legalstatus=LegalStatus.objects.get(id=legal_var),
                            is_deleted=False)
        except Exception, exc:
            print 'exception in Company Detail Saving ', str(traceback.print_exc())


        if request.POST.get('CorrespondenceAadharCheck') == "on":
            aadhar_no= 0
        else:
            aadhar_no = request.POST.get('CorrespondenceAadhar')

        if request.POST.get('CorrespondencePanCheck') == "on":
            panNo = "NA"
        else:
            panNo = request.POST.get('CorrespondencePan')


        if request.POST.get('CorrespondenceGSTText'):
            CorrespondenceGSTText=request.POST.get('CorrespondenceGSTText')
        else:
            CorrespondenceGSTText= 'NA'

        # if request.POST.get('pocName') == 'None':
        #     pocName='NA'
        # else:
        #     pocName=request.POST.get('pocName')

        # if request.POST.get('pocContact'):
        #     pocContact=request.POST.get('pocContact')
        # else:
        #     pocContact='NA'

        # if request.POST.get('pocEmail'):
        #     pocContact=request.POST.get('pocEmail')
        # else:
        #     pocContact='pocEmail'


        try:
            userDetail=UserDetail(
                ceo_name = ceo_name,
                ceo_email = request.POST.get('CEOEmail') if request.POST.get('CEOEmail') else request.POST.get('CEOEmailin'),
                ceo_designation = ceo_name,
                ceo_cellno = ceo_contact,
                person_cellno=request.POST.get('CorrespondenceContact'),
                correspond_cellno=request.POST.get('CorrespondenceContact'),
                correspond_address = request.POST.get('CorrespondenceAddress'),
                correspond_email = request.POST.get('CorrespondenceEmail'),
                correspondstate = State.objects.get(id=request.POST.get('CorrespondenceState')),
                correspondcity = City.objects.get(id=request.POST.get('CorrespondenceCity')),
                correspond_pincode = request.POST.get('CorrespondencePin'),
                correspond_std1 =correspondStd1,
                correspond_std2 =correspondStd2,
                correspond_landline1 = CorrespondenceLandline1,
                correspond_landline2 = CorrespondenceLandline2,
                poc_name = request.POST.get('pocName') if request.POST.get('pocName') else None,
                poc_contact = request.POST.get('POCContact') if request.POST.get('POCContact') else None,
                poc_email = request.POST.get('POCEmail') if request.POST.get('POCEmail') else None,
                # poc_name = pocName,
                # poc_email = pocEmail,
                # poc_contact = pocContact,
                website = request.POST.get('CorrespondenceWebsite'),
                gst = CorrespondenceGSTText,
                gst_in = gst_option,
                pan = panNo,
                aadhar = aadhar_no,
                # awards = isodetail,
                person_name = person_name,
                person_email = person_email,
                person_designation = person_designation,
                factory_cellno = factory_cellno,
                factory_address=factory_address,
                factorystate = factorystate,
                factorycity = factorycity,
                factory_pincode = factory_pincode,
                factory_std1 = factoryStd1,
                factory_std2 = factoryStd2,
                factory_landline1 = factory_landline1,
                factory_landline2 = factory_landline2,
                membership_type = membership_type,
                enroll_type=enroll_type,
                membership_category = MembershipCategory.objects.get(id=request.POST.get('MembershipCategory')),
                annual_turnover_year = request.POST.get('foryear'),
                annual_turnover_rupees = request.POST.get('Rscrore'),
                membership_slab = MembershipSlab.objects.get(id=request.POST.get('MembershipSlab')),
                membership_year = str(request.POST.get('MembershipForYear'))[0:9],
                updated_date = datetime.datetime.now(),
                area_of_experties = area_of_experties,
                experties_other = request.POST.get('otherareaofexperties')
            )
            #
        except Exception, exc:
            print 'exception in USER DETAIL SAVING ', str(traceback.print_exc())


        print request.POST.get('entrance_fee')
        hoddetail.save()
        company_detail.save()
        if hoddetail:
            hod_id = HOD_Detail.objects.get(id=hoddetail.id)
        else:
            hod_id = ''
        company_detail.hoddetail=hod_id
        company_detail.save()
        exportList=[]
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
        print "user_Payment_Type",user_Payment_Type, request.POST.get("paymentMode")
        if (request.POST.get("paymentMode") == "OfflinePending"):
            userDetail.payment_method = "Offline Pending"
            if user_Payment_Type == "ByCash":
                cash_amount = request.POST.get('cash_amount')
                cheque_date = None
                user_Payment_Type = "Cash"
            elif user_Payment_Type == "ByCheque":
                cheque_date = None
                user_Payment_Type = "Cheque"
            else:
                user_Payment_Type = "NEFT"

            # cheque_no = request.POST.get('Cheque_no')
            # cheque_date = datetime.datetime.strptime(request.POST.get('cheque_date'), '%d/%m/%Y')
            # bank_name = request.POST.get('bank_name')
        else:
            userDetail.payment_method = "Online Pending"

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
                                            user_Payment_Type= user_Payment_Type,
                                            financial_year=str(request.POST.get('MembershipForYear'))[0:9],
                                            amount_payable=float(request.POST.get('payable_amount')))
        paymentDetails_obj.save()

        print "userDetail.membership_category.enroll_type",userDetail.membership_category.enroll_type
        if userDetail.membership_category.enroll_type == "Life Membership":
            userDetail.user_type = "Life Membership"
        else:
            userDetail.user_type = "Associate"
        userDetail.save()
        transaction.savepoint_commit(sid)        
        send_mail_offline_payment(paymentDetails_obj, member_invoice_obj, userDetail)
        data = {'success': 'true', 'user_detail_id': str(userDetail.id), 'quarter': str(userDetail.membership_year)}
        print 'Request OUT | mccia_landing | save_new_consumer | user %s', request.user
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | mccia_landing | save_new_consumer | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


def member_pre_invoice(request):
    try:
        print "request.GET.get('slab_id')", request.GET.get('slab_id')
        print "request.GET.get('quarter')", request.GET.get('quarter')
        slabID = MembershipSlab.objects.get(id=request.GET.get('slab_id'))
        print "slabID", slabID,request.GET.get('show_data')
        data = {
                'slab_id': str(slabID.id),
                'quarter': request.GET.get('quarter'),
                'show_data' : request.GET.get('show_data'),
                }
    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        data = {'success': 'false'}
        print 'Exception | mccia_landing | member_pre_invoice | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Show Member Invoice Data
def member_invoice(request):
    data = {}
    try:
        print '\nRequest IN | membership_landing.py | member_invoice = ', request.user        
        print "request.GET.get('show_data')",request.GET.get('show_data')
        slabID=MembershipSlab.objects.get(id=request.GET.get('slab_id'))
        annual_fee=''

        if slabID.membershipCategory.enroll_type == "Life Membership":
            annual_fee = float(slabID.annual_fee)
        else:
            if str(request.GET.get('quarter')) == '2019-2020/ full year':
                annual_fee = float(slabID.annual_fee)
            elif str(request.GET.get('quarter')) == '2019-2020/ half year':
                annual_fee = float(slabID.annual_fee) * 2/4
            elif str(request.GET.get('quarter')) == '2019-2020/ 3 quarters':
                annual_fee = float(slabID.annual_fee) * 3/4
            elif str(request.GET.get('quarter')) == '2019-2020/ Last Quarters':
                annual_fee = float(slabID.annual_fee) * 1/4
            elif str(request.GET.get('quarter')) == '2018-2019/ full year':
                annual_fee = float(slabID.annual_fee)
            elif str(request.GET.get('quarter')) == '2018-2019/ half year':
                annual_fee = float(slabID.annual_fee) * 2/4
            elif str(request.GET.get('quarter')) == '2018-2019/ 3 quarters':
                annual_fee = float(slabID.annual_fee) * 3/4
            elif str(request.GET.get('quarter')) == '2018-2019/ Last Quarters':
                annual_fee = float(slabID.annual_fee) * 1/4

        if request.GET.get('is_previous') != 'uncheck':
            entrance_fee = 0
        else:
            entrance_fee = slabID.entrance_fee
        slab_category = slabID.slab
        membership_for_year = request.GET.get('quarter')
        subscription_charges = slabID.annual_fee
        # annual_fee = ''
        # if str(request.GET.get('quarter')) == '2018-2019/ full year':
        #     annual_fee = float(member_obj.membership_slab.annual_fee)
        # elif str(request.GET.get('quarter')) == '2018-2019/ half year':
        #     annual_fee = float(member_obj.membership_slab.annual_fee) * 2 / 4
        # elif str(request.GET.get('quarter')) == '2018-2019/ 3 quarters':
        #     annual_fee = float(member_obj.membership_slab.annual_fee) * 3 / 4
        # elif str(request.GET.get('quarter')) == '2018-2019/ Last Quarters':
        #     annual_fee = float(member_obj.membership_slab.annual_fee) * 1 / 4

        tax_amount = (float(annual_fee) + float(entrance_fee)) * 0.18
        amount_payable = float(annual_fee) + float(entrance_fee) + tax_amount

        data = {'membership_category': str(slabID.membershipCategory.membership_category),
                'slab_category': str(slab_category),
                'membership_year': str(membership_for_year),
                'subscription_charges': float(annual_fee),
                'entrance_fee': float(entrance_fee),
                'tax_amount': float(tax_amount), 'amount_payable':round(float(amount_payable),0) ,
                'member_id': request.GET.get('member_id'),
                'show_data' : request.GET.get('show_data'),
                }
        print '\nResponse OUT | membership_landing.py | member_invoice = ',request.user
    except Exception,e:
        print '\nException | membership_landing.py | member_invoice = ',str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Save Membership Invoice Data
@csrf_exempt
@transaction.atomic
def save_member_invoice_detail(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_landing.py | save_member_invoice_detail = ',request.POST
        user_detail_obj = UserDetail.objects.get(id=str(request.POST.get('member_id')))
        member_invoice_obj = MembershipInvoice(userdetail_id=str(request.POST.get('member_id')),
                                               subscription_charges=request.POST.get('subsciption_charges'),
                                               entrance_fees=request.POST.get('entrance_fees'),
                                               tax=request.POST.get('tax_amount'),
                                               amount_payable=request.POST.get('payable_amount'),
                                               membership_category=user_detail_obj.membership_category,
                                               membership_slab=user_detail_obj.membership_slab,
                                               valid_invalid_member=user_detail_obj.valid_invalid_member)
        member_invoice_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print '\nResponse OUT | membership_landing.py | save_member_invoice_detail = '
    except Exception,e:
        print '\nException | membership_landing.py | save_member_invoice_detail = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Renew Member Page Front End
@csrf_exempt
def get_renew_invoice(request):
    data = {}
    try:
        print '\nRequest IN | membership_landing | get_renew_invoice | User %s ', request.user
        user_detail_obj = UserDetail.objects.get(id=request.POST.get('user_detail_id'))
        category_obj = MembershipCategory.objects.get(id=request.POST.get('category_id'))
        slab_obj = MembershipSlab.objects.get(id=request.POST.get('slab_id'))

        gst_amount = round(float(slab_obj.annual_fee) * 0.18, 0)

        payment_detail_obj = PaymentDetails.objects.filter(userdetail=user_detail_obj,
                                                           financial_year=user_detail_obj.membership_year,
                                                           is_deleted=False).last()
        
        due_amount = 0
        advance_amount = round(float(payment_detail_obj.amount_next_advance), 0)
        
        amount_payable = 0
        temp_amount_payable = round(float(slab_obj.annual_fee), 0) + gst_amount        

        if Decimal(advance_amount) > Decimal(temp_amount_payable):
            amount_payable = 0            
        else:
            amount_payable = temp_amount_payable - advance_amount

        if payment_detail_obj.payment_received_status == 'UnPaid':
            
            payment_detail_obj_list = PaymentDetails.objects.filter(userdetail=user_detail_obj,
                                                                    financial_year=user_detail_obj.membership_year,
                                                                    is_deleted=False)
            if payment_detail_obj_list.count() == 1:
                due_amount = round(float(payment_detail_obj_list.amount_payable), 0)

            for i in payment_detail_obj_list:
                if i.amount_due > 0 and i.payment_received_status == 'Partial':
                    due_amount = i.amount_due

        amount_payable = Decimal(amount_payable) + due_amount

        print '\nResponse OUT | membership_landing | get_renew_invoice | User %s ', request.user
        data = {'success': 'true', 'category': str(category_obj.membership_category),
                'slab': str(slab_obj.slab), 'renewal_year': str(request.POST.get('renewal_year')),
                'subscription_charge': str(slab_obj.annual_fee), 'gst_amount': str(gst_amount),
                'due_amount': str(due_amount), 'advance_amount': str(advance_amount), 'amount_payable': str(amount_payable),
                'turnover_value': str(request.POST.get('turnover_value')),
                'employee_value': str(request.POST.get('employee_value'))
                }
    except Exception, e:
        data = {'success': 'false'}
        print '\nException IN | membership_landing | get_renew_invoice = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Renew Member Request - Front End
@transaction.atomic
@csrf_exempt
def renew_member_request(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_landing | renew_member_request | User = ', request.user
        user_detail_obj = UserDetail.objects.get(id=request.POST.get('member_id'))

        consumerMobileNo = ''
        total_amount = str(request.POST.get('amount_payable'))
        consumer_name = str(user_detail_obj.company.company_name)
        if user_detail_obj.enroll_type == 'CO':
            if user_detail_obj.ceo_cellno:
                if len(user_detail_obj.ceo_cellno) == 10:
                    consumerMobileNo = str(user_detail_obj.ceo_cellno)
                else:
                    consumerMobileNo = '8308809005'
            else:
                consumerMobileNo = '8308809005'
        else:
            if user_detail_obj.person_cellno:
                if len(user_detail_obj.person_cellno) == 10:
                    consumerMobileNo = str(user_detail_obj.person_cellno)
                else:
                    consumerMobileNo = '8308809005'
        if user_detail_obj.ceo_email:
            consumerEmailId = str(user_detail_obj.ceo_email)
        else:
            consumerEmailId = 'membership@mcciapune.com'

        merchant_id = 'L172654'
        salt = '2093514954UVQFBK'
        # merchant_id = 'T172654'
        # salt = '2093514954UVQFBK'
        itemId = 'MCCI'  # scheme code
        transaction_id = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        try:
            MembershipPaymentTransaction_obj = MembershipPaymentTransaction(
                transaction_id=transaction_id,
                merchant_id=merchant_id,
                total_amount=total_amount,
                consumer_name=consumer_name,
                consumer_mobile_no=consumerMobileNo,
                consumer_email=consumerEmailId
            )
            MembershipPaymentTransaction_obj.save()

            m = hashlib.sha512()
            parameters = {'company_name': str(user_detail_obj.company.company_name),
                          'membership_no': str(user_detail_obj.member_associate_no) if user_detail_obj.member_associate_no else 'NA'}
            cart_desc = str(json.dumps(parameters))
            cart_desc = cart_desc.replace('"', '')

            msg = merchant_id + "|"  # consumerData.merchantId|
            msg += str(transaction_id) + "|"  # consumerData.txnId|
            msg += str(total_amount) + "|"  # totalamount|
            msg += "" + "|"  # consumerData.accountNo|
            msg += "" + "|"  # consumerData.consumerId|
            msg += consumerMobileNo + "|"  # consumerData.consumerMobileNo|
            msg += consumerEmailId + "|"  # consumerData.consumerEmailId |
            msg += "" + "|"  # consumerData.debitStartDate|
            msg += "" + "|"  # consumerData.debitEndDate|
            msg += "" + "|"  # consumerData.maxAmount|
            msg += "" + "|"  # consumerData.amountType|
            msg += "" + "|"  # consumerData.frequency|
            msg += "" + "|"  # consumerData.cardNumber|
            msg += "" + "|"  # consumerData. expMonth|
            msg += "" + "|"  # consumerData.expYear|
            msg += "" + "|"  # consumerData.cvvCode|
            msg += salt  # salt

            print msg

            m.update(msg)
            configJson = {
                'tarCall': False,
                'features': {
                    'showPGResponseMsg': True,
                    'enableNewWindowFlow': True
                },
                'consumerData': {
                    'deviceId': 'WEBSH2',
                    'token': str(m.hexdigest()),
                    'responseHandler': 'handleResponse',
                    'paymentMode': 'all',
                    'merchantLogoUrl': 'https://www.paynimo.com/CompanyDocs/company-logo-md.png',
                    'merchantId': merchant_id,
                    'currency': 'INR',
                    'consumerId': '',
                    'consumerMobileNo': consumerMobileNo,
                    'consumerEmailId': consumerEmailId,
                    'txnId': str(transaction_id),
                    'cardNumber': '',
                    'expMonth': '',
                    'expYear': '',
                    'cvvCode': '',
                    'amount_type': '',
                    'frequency': '',
                    'amountType': '',
                    'debitStartDate': '',
                    'debitEndDate': '',
                    'maxAmount': '',
                    'accountNo': '',
                    'items': [{
                        'itemId': itemId,
                        'amount': str(total_amount),
                        'comAmt': '0'
                    }],
                    'cartDescription': cart_desc,
                    'customStyle': {
                        'PRIMARY_COLOR_CODE': '#3977b7',
                        'SECONDARY_COLOR_CODE': '#FFFFFF',
                        'BUTTON_COLOR_CODE_1': '#1969bb',
                        'BUTTON_COLOR_CODE_2': '#FFFFFF'
                    }
                }
            }
            transaction.savepoint_commit(sid)
            data = {'configJson': configJson, 'success': 'true'}
        except Exception, e:
            print '\nException IN | membership_landing | renew_member_request | Excp = ', str(traceback.print_exc())
            pass
            transaction.rollback(sid)
            data = {'success': 'false'}
    except Exception, e:
        print '\nException IN | membership_landing | renew_member_request | Excp = ', str(traceback.print_exc())
        pass
        transaction.rollback(sid)
        data = {'success': 'false'}
    print data
    print '\nResponse OUT | membership_landing | renew_member_request | User = ', request.user
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@transaction.atomic
def renew_membership_response_save(request):
    sid = transaction.savepoint()
    data = request.POST
    response_data = {}
    try:
        print '\nRequest IN | membership_landing.py | renew_membership_response_save | User = ', request.user

        salt = '2093514954UVQFBK'
        stringResponse = data['stringResponse']
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
        bank_transaction_id = stringResponse_list[12]
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
        msg += '|' + bank_transaction_id
        msg += '|' + mandate_reg_no
        msg += '|' + token
        msg += '|' + salt

        m = hashlib.sha512()
        m.update(msg)
        hex_msg = m.hexdigest()
        is_hash_match = hex_msg == hash

        try:
            statusCode = data['statusCode']  # 0300=Success,0398=Initiated,0399=failure,0396=Aborted,0392=CancelledByUser
            responseType = data['responseType']  # hasg algo name
            errorMessage = data['errorMessage']
            accountNo = data['accountNo']
            reference = data['reference']
            bankReferenceIdentifier = data['bankReferenceIdentifier']
            merchantTransactionIdentifier = data['merchantTransactionIdentifier']
            merchantAdditionalDetails = data['merchantAdditionalDetails']
            dateTime = data['dateTime']  # convert to datetime object
            amount = data['amount']
            statusMessage = data['statusMessage']
            balanceAmount = data['balanceAmount']
            error = data['error']
            identifier = data['identifier']
            merchantTransactionRequestType = data['merchantTransactionRequestType']
            refundIdentifier = data['refundIdentifier']
            transactionState = data['transactionState']

            paymenttransactionobj = MembershipPaymentTransaction.objects.get(transaction_id=merchantTransactionIdentifier)
            paymenttransactionobj.txn_status = txn_status  # statusCode
            paymenttransactionobj.txn_msg = txn_msg  # statusMessage
            paymenttransactionobj.txn_err_msg = txn_err_msg  # errorMessage
            paymenttransactionobj.clnt_txn_ref = clnt_txn_ref
            paymenttransactionobj.tpsl_bank_cd = tpsl_bank_cd
            paymenttransactionobj.tpsl_txn_id = tpsl_txn_id  # identifier
            paymenttransactionobj.txn_amt = txn_amt
            paymenttransactionobj.clnt_rqst_meta = clnt_rqst_meta
            paymenttransactionobj.tpsl_txn_time = tpsl_txn_time
            paymenttransactionobj.bal_amt = bal_amt
            paymenttransactionobj.card_id = card_id
            paymenttransactionobj.alias_name = alias_name
            paymenttransactionobj.bank_transaction_id = bank_transaction_id
            paymenttransactionobj.mandate_reg_no = mandate_reg_no
            paymenttransactionobj.save()

            user_detail_obj = UserDetail.objects.get(id=request.POST.get('member_id'))

            if statusCode == '0300' and is_hash_match:
                # Paid Successfully
                print '\nSuccess'
                user_detail_obj.membership_category = MembershipCategory.objects.get(id=str(request.POST.get('membership_category')))
                user_detail_obj.membership_slab = MembershipSlab.objects.get(id=str(request.POST.get('slab_category')))
                user_detail_obj.annual_turnover_year = request.POST.get('annual_to_year')
                user_detail_obj.annual_turnover_rupees = request.POST.get('annual_to')
                user_detail_obj.renewal_year = request.POST.get('membership_renew_year')
                user_detail_obj.renewal_status = 'COMPLETED'
                user_detail_obj.membership_year = str(request.POST.get('membership_renew_year')).strip()
                user_detail_obj.valid_invalid_member = True
                user_detail_obj.payment_method = 'Online Pending'
                user_detail_obj.updated_date = datetime.datetime.now()
                user_detail_obj.save()

                member_invoice_obj = MembershipInvoice(userdetail=user_detail_obj,
                                                       subscription_charges=str(
                                                           request.POST.get('subscription_charges')),
                                                       tax=str(request.POST.get('tax_amount')),
                                                       without_adv_amount_payable=Decimal(
                                                           str(request.POST.get('subscription_charges'))) + Decimal(
                                                           str(request.POST.get('tax_amount'))),
                                                       amount_payable=str(request.POST.get('amount_payable')),
                                                       financial_year=str(request.POST.get('membership_renew_year')),
                                                       last_due_amount=str(request.POST.get('due_amount')),
                                                       last_advance_amount=str(request.POST.get('advance_amount')),
                                                       invoice_for='RENEW',
                                                       membership_category=user_detail_obj.membership_category,
                                                       membership_slab=user_detail_obj.membership_slab,
                                                       valid_invalid_member=user_detail_obj.valid_invalid_member,
                                                       is_paid=True, turnover_range=int(request.POST.get('turnover_value')),
                                                       employee_range=int(request.POST.get('employee_value')))
                member_invoice_obj.save()

                payment_detail_obj = PaymentDetails(userdetail=user_detail_obj,
                                                    membershipInvoice=member_invoice_obj,
                                                    amount_payable=str(request.POST.get('amount_payable')),
                                                    amount_paid = Decimal(txn_amt),
                                                    payment_date=datetime.date.today(),
                                                    payment_received_status='Paid',
                                                    user_Payment_Type='Online',
                                                    neft_transfer_id='Paid_Online',
                                                    financial_year=str(request.POST.get('membership_renew_year')),
                                                    amount_last_advance=str(request.POST.get('advance_amount')))
                payment_detail_obj.save()
                bk_no = 'MBK' + str(payment_detail_obj.id).zfill(7)
                payment_detail_obj.bk_no = str(bk_no)
                payment_detail_obj.save()

                if Decimal(payment_detail_obj.amount_last_advance) > Decimal(payment_detail_obj.amount_payable):
                    payment_detail_obj.amount_next_advance = Decimal(payment_detail_obj.amount_last_advance) - Decimal(
                        member_invoice_obj.without_adv_amount_payable)
                    payment_detail_obj.save()

                paymenttransactionobj.payment_status = 1
                paymenttransactionobj.payment_mode = 1
                paymenttransactionobj.membership_invoice = member_invoice_obj
                paymenttransactionobj.payment_detail = payment_detail_obj
                paymenttransactionobj.is_renew = True
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                membership_details.send_renew_mail_ack(request, payment_detail_obj, user_detail_obj)
                response_data['success'] = 'true'
                # pass
            elif statusCode == '0398' and is_hash_match:
                # Transaction Initiated. Add Entry in Pending Transaction
                print '\nInitiated'
                user_detail_obj.membership_category = MembershipCategory.objects.get(id=str(request.POST.get('membership_category')))
                user_detail_obj.membership_slab = MembershipSlab.objects.get(id=str(request.POST.get('slab_category')))
                user_detail_obj.annual_turnover_year = request.POST.get('annual_to_year')
                user_detail_obj.annual_turnover_rupees = request.POST.get('annual_to')
                user_detail_obj.renewal_year = request.POST.get('membership_renew_year')
                user_detail_obj.renewal_status = 'STARTED'
                user_detail_obj.payment_method = 'Online Pending'
                user_detail_obj.updated_date = datetime.datetime.now()
                user_detail_obj.save()

                member_invoice_obj = MembershipInvoice(userdetail=user_detail_obj,
                                                       subscription_charges=str(
                                                           request.POST.get('subscription_charges')),
                                                       tax=str(request.POST.get('tax_amount')),
                                                       without_adv_amount_payable=Decimal(
                                                           str(request.POST.get('subscription_charges'))) + Decimal(
                                                           str(request.POST.get('tax_amount'))),
                                                       amount_payable=str(request.POST.get('amount_payable')),
                                                       financial_year=str(request.POST.get('membership_renew_year')),
                                                       last_due_amount=str(request.POST.get('due_amount')),
                                                       last_advance_amount=str(request.POST.get('advance_amount')),
                                                       invoice_for='RENEW',
                                                       membership_category=user_detail_obj.membership_category,
                                                       membership_slab=user_detail_obj.membership_slab,
                                                       valid_invalid_member=user_detail_obj.valid_invalid_member,
                                                       turnover_range=int(request.POST.get('turnover_value')),
                                                       employee_range=int(request.POST.get('employee_value'))
                                                       )
                member_invoice_obj.save()

                payment_detail_obj = PaymentDetails(userdetail=user_detail_obj,
                                                    membershipInvoice=member_invoice_obj,
                                                    amount_payable=str(request.POST.get('amount_payable')),
                                                    payment_received_status='UnPaid',
                                                    financial_year=str(request.POST.get('membership_renew_year')),
                                                    amount_last_advance=str(request.POST.get('advance_amount')),
                                                    )
                payment_detail_obj.save()

                if Decimal(payment_detail_obj.amount_last_advance) > Decimal(payment_detail_obj.amount_payable):
                    payment_detail_obj.amount_next_advance = Decimal(payment_detail_obj.amount_last_advance) - Decimal(
                        member_invoice_obj.without_adv_amount_payable)
                    payment_detail_obj.save()

                paymenttransactionobj.membership_invoice = member_invoice_obj
                paymenttransactionobj.payment_detail = payment_detail_obj
                paymenttransactionobj.payment_status = 2
                paymenttransactionobj.is_renew = True
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                add_to_pending(paymenttransactionobj.id)
                membership_details.send_renew_mail_ack(request, payment_detail_obj, user_detail_obj)
                response_data['success'] = 'initiated'
                # pass
            elif statusCode == '0399' and is_hash_match:
                # Failed Transaction
                print '\nFailed'
                paymenttransactionobj.payment_status = 3
                paymenttransactionobj.is_renew = True
                paymenttransactionobj.save()
                transaction.savepoint_commit(sid)
                response_data['success'] = 'failed'
                # pass
            elif statusCode == '0396' and is_hash_match:
                # Cancelled by User
                print '\nCancelled'
                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.is_renew = True
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                response_data['success'] = 'cancelled'
                # pass
            elif statusCode == '0392' and is_hash_match:
                print '\nCancelled by user'
                paymenttransactionobj.payment_status = 4
                paymenttransactionobj.is_renew = True
                paymenttransactionobj.save()

                transaction.savepoint_commit(sid)
                response_data['success'] = 'cancelled'
                # pass
            elif is_hash_match:
                # code if hash is matched but no status code
                pass

            elif not is_hash_match and statusCode in ['0300', '0398', '0399', '0396', '0392']:
                paymenttransactionobj.is_hash_matched = False
                paymenttransactionobj.is_renew = True
                paymenttransactionobj.save()

                if statusCode == '0300':
                    print '\nSuccess not hash'
                    user_detail_obj.membership_category = MembershipCategory.objects.get(id=str(request.POST.get('membership_category')))
                    user_detail_obj.membership_slab = MembershipSlab.objects.get(id=str(request.POST.get('slab_category')))
                    user_detail_obj.annual_turnover_year = request.POST.get('annual_to_year')
                    user_detail_obj.annual_turnover_rupees = request.POST.get('annual_to')
                    user_detail_obj.renewal_year = request.POST.get('membership_renew_year')
                    user_detail_obj.renewal_status = 'COMPLETED'
                    user_detail_obj.membership_year = str(request.POST.get('membership_renew_year')).strip()
                    user_detail_obj.valid_invalid_member = True
                    user_detail_obj.payment_method = 'Online Pending'
                    user_detail_obj.updated_date = datetime.datetime.now()
                    user_detail_obj.save()

                    member_invoice_obj = MembershipInvoice(userdetail=user_detail_obj,
                                                           subscription_charges=str(request.POST.get('subscription_charges')),
                                                           tax=str(request.POST.get('tax_amount')),
                                                           without_adv_amount_payable=Decimal(str(request.POST.get('subscription_charges'))) + Decimal(str(request.POST.get('tax_amount'))),
                                                           amount_payable=str(request.POST.get('amount_payable')),
                                                           financial_year=str(request.POST.get('membership_renew_year')),
                                                           last_due_amount=str(request.POST.get('due_amount')),
                                                           last_advance_amount=str(request.POST.get('advance_amount')),
                                                           invoice_for='RENEW',
                                                           membership_category=user_detail_obj.membership_category,
                                                           membership_slab=user_detail_obj.membership_slab,
                                                           valid_invalid_member=user_detail_obj.valid_invalid_member,
                                                           is_paid=True,turnover_range=int(request.POST.get('turnover_value')),
                                                           employee_range=int(request.POST.get('employee_value')))
                    member_invoice_obj.save()

                    payment_detail_obj = PaymentDetails(userdetail=user_detail_obj,
                                                        membershipInvoice=member_invoice_obj,
                                                        amount_payable=str(request.POST.get('amount_payable')),
                                                        amount_paid=Decimal(txn_amt),
                                                        payment_date=datetime.date.today(),
                                                        payment_received_status='Paid',
                                                        user_Payment_Type='Online',
                                                        neft_transfer_id='Paid_Online',
                                                        financial_year=str(request.POST.get('membership_renew_year')),
                                                        amount_last_advance=str(request.POST.get('advance_amount')))
                    payment_detail_obj.save()
                    bk_no = 'MBK' + str(payment_detail_obj.id).zfill(7)
                    payment_detail_obj.bk_no = str(bk_no)
                    payment_detail_obj.save()

                    if Decimal(payment_detail_obj.amount_last_advance) > Decimal(payment_detail_obj.amount_payable):
                        payment_detail_obj.amount_next_advance = Decimal(
                            payment_detail_obj.amount_last_advance) - Decimal(
                            member_invoice_obj.without_adv_amount_payable)
                        payment_detail_obj.save()

                    paymenttransactionobj.payment_status = 1
                    paymenttransactionobj.payment_mode = 1
                    paymenttransactionobj.is_renew = True
                    paymenttransactionobj.membership_invoice = member_invoice_obj
                    paymenttransactionobj.payment_detail = payment_detail_obj
                    paymenttransactionobj.save()

                    transaction.savepoint_commit(sid)
                    membership_details.send_renew_mail_ack(request, payment_detail_obj, user_detail_obj)
                    response_data['success'] = 'true'
                elif statusCode == '0398':
                    print '\nInitiated not hash'
                    user_detail_obj.membership_category = MembershipCategory.objects.get(
                        id=str(request.POST.get('membership_category')))
                    user_detail_obj.membership_slab = MembershipSlab.objects.get(
                        id=str(request.POST.get('slab_category')))
                    user_detail_obj.annual_turnover_year = request.POST.get('annual_to_year')
                    user_detail_obj.annual_turnover_rupees = request.POST.get('annual_to')
                    user_detail_obj.renewal_year = request.POST.get('membership_renew_year')
                    user_detail_obj.renewal_status = 'STARTED'
                    user_detail_obj.payment_method = 'Online Pending'
                    user_detail_obj.updated_date = datetime.datetime.now()
                    user_detail_obj.save()

                    member_invoice_obj = MembershipInvoice(userdetail=user_detail_obj,
                                                           subscription_charges=str(
                                                               request.POST.get('subscription_charges')),
                                                           tax=str(request.POST.get('tax_amount')),
                                                           without_adv_amount_payable=Decimal(
                                                               str(request.POST.get('subscription_charges'))) + Decimal(
                                                               str(request.POST.get('tax_amount'))),
                                                           amount_payable=str(request.POST.get('amount_payable')),
                                                           financial_year=str(
                                                               request.POST.get('membership_renew_year')),
                                                           last_due_amount=str(request.POST.get('due_amount')),
                                                           last_advance_amount=str(request.POST.get('advance_amount')),
                                                           invoice_for='RENEW',
                                                           membership_category=user_detail_obj.membership_category,
                                                           membership_slab=user_detail_obj.membership_slab,
                                                           valid_invalid_member=user_detail_obj.valid_invalid_member,
                                                           turnover_range=int(request.POST.get('turnover_value')),
                                                           employee_range=int(request.POST.get('employee_value'))
                                                           )
                    member_invoice_obj.save()

                    payment_detail_obj = PaymentDetails(userdetail=user_detail_obj,
                                                        membershipInvoice=member_invoice_obj,
                                                        amount_payable=str(request.POST.get('amount_payable')),
                                                        payment_received_status='UnPaid',
                                                        financial_year=str(request.POST.get('membership_renew_year')),
                                                        amount_last_advance=str(request.POST.get('advance_amount')),
                                                        )
                    payment_detail_obj.save()

                    if Decimal(payment_detail_obj.amount_last_advance) > Decimal(payment_detail_obj.amount_payable):
                        payment_detail_obj.amount_next_advance = Decimal(
                            payment_detail_obj.amount_last_advance) - Decimal(
                            member_invoice_obj.without_adv_amount_payable)
                        payment_detail_obj.save()

                    paymenttransactionobj.membership_invoice = member_invoice_obj
                    paymenttransactionobj.payment_detail = payment_detail_obj
                    paymenttransactionobj.payment_status = 2
                    paymenttransactionobj.is_renew = True
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    add_to_pending(paymenttransactionobj.id)
                    membership_details.send_renew_mail_ack(request, payment_detail_obj, user_detail_obj)
                    response_data['success'] = 'initiated'
                elif statusCode == '0399':
                    print '\nFailed not hash'
                    paymenttransactionobj.payment_status = 3
                    paymenttransactionobj.is_renew = True
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'failed'
                elif statusCode == '0396':
                    print '\nCancelled not hash'
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.is_renew = True
                    paymenttransactionobj.save()

                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'cancelled'
                elif statusCode == '0392':
                    print '\nCancelled by user not hash'
                    paymenttransactionobj.payment_status = 4
                    paymenttransactionobj.is_renew = True
                    paymenttransactionobj.save()
                    transaction.savepoint_commit(sid)
                    response_data['success'] = 'cancelled'
                # code if hash code is not matched and with match statusCode
                pass

            else:
                print '\nLast Else'
                # code if hash code is not matched and without match statusCode
                pass

            # transaction.savepoint_commit(sid)

        except Exception, e:
            print e
            pass

    except Exception, e:
        print e
        transaction.rollback(sid)
        pass
        response_data['success'] = 'false'
    print '\nResponse OUT | membership_landing.py | renew_membership_response_save | User = ', request.user
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def member_timeline(request):
    try:
        print '\nRequest IN | membership_landing.py | member_timeline | User = ', request.user
        if request.session['user_type'] == 'frontend':
            return render(request, 'membership/member_timeline.html')
        else:
            return HttpResponseForbidden()
    except Exception, e:
        print '\nException IN | membership_landing.py | member_timeline | EXCP = ', str(traceback.print_exc())
    return render(request, 'membership/member_timeline.html')


def get_member_timeline_data(request):
    data = {}
    try:
        print '\nRequest IN | membership_landing.py | get_member_timeline_data | User = ', request.user
        response_data = []
        x = 2
        y = 1

        user_detail_obj = request.user.membershipuser.userdetail
        first_data = {
            'x': "1",
            'y': y,
            'text': str('[bold]Membership Accepted on') + '[/]\n' + str(user_detail_obj.membership_acceptance_date.strftime('%d/%m/%Y')),
            'center': 'bottom'
        }

        member_invoice_list = MembershipInvoice.objects.filter(userdetail=user_detail_obj, is_paid=True, invoice_for__in=['RENEW', 'RE-ASSOCIATE'],
                                                        is_deleted=False)
        hall_booking_list = HallBookingDetail.objects.filter(hall_booking__member=user_detail_obj, is_deleted=False).exclude(booking_status__in=[0, 10])
        event_list = EventRegistration.objects.filter(user_details=user_detail_obj, is_deleted=False).values('event_id').distinct()
        visa_list = Membership_Visa_Recommendations.objects.filter(mcciamember=user_detail_obj, is_deleted=False,
                                                                   is_completed=True)

        for invoice_item in member_invoice_list:
            payment_obj = PaymentDetails.objects.filter(membershipInvoice=invoice_item, is_deleted=False).last()            
            response_data.append({
                'x': str(x),
                'y': y,
                'text': str('[bold]Membership Renewed on') if invoice_item.invoice_for == 'RENEW' else str('[bold]Membership Re-associated on') + '[/]\n' + str(payment_obj.payment_date.strftime('%d/%m/%Y')),
                'center': 'bottom',
                'date': payment_obj.payment_date
            })

        for hall_booking_item in hall_booking_list:
            response_data.append({
                'x': str(x),
                'y': y,
                'text': str('[bold]Hall Booked on') + '[/]\n' + str(hall_booking_item.booking_from_date.strftime('%d/%m/%Y')),
                'center': 'bottom',
                'date': hall_booking_item.booking_from_date.date()
            })

        for event_reg_item in event_list:
            event_obj = EventDetails.objects.get(id=event_reg_item['event_id'])
            response_data.append({
                'x': str(x),
                'y': y,
                'text': str('[bold]Event Attended on') + '[/]\n' + str(event_obj.from_date.strftime('%d/%m/%Y')),
                'center': 'bottom',
                'date': event_obj.from_date.date()
            })

        for visa_item in visa_list:
            response_data.append({
                'x': str(x),
                'y': y,
                'text': str('[bold]Applied For Visa Recommendation Letter on') + '[/]\n' + str(visa_item.created_date.strftime('%d/%m/%Y')),
                'center': 'bottom',
                'date': visa_item.created_date.date()
            })

        response_data = sorted(response_data, key=lambda i: i['date'])
        for list_item in response_data:
            if x % 2 == 0:
                list_item['center'] = 'top'
            else:
                list_item['center'] = 'bottom'

            list_item['x'] = str(x)
            x = x + 1

        response_data = [{k: v for k, v in d.items() if k != 'date'} for d in response_data]
        response_data.insert(0, first_data)

        data['success'] = 'true'
        data['response_data'] = response_data
        print '\nResponse OUT | membership_landing.py | get_member_timeline_data | User = ', request.user
    except Exception, e:
        data['success'] = 'false'
        print '\nException IN | membership_landing.py | get_member_timeline_data | EXCP = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')
