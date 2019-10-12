import json
import traceback
from datetime import date, datetime

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from adminapp.models import Hall_detail_list,Location,Hall_pricing,Country
from django.views.decorators.csrf import csrf_exempt

from membershipapp.models import CompanyDetail, UserDetail
from visarecommendationapp.models import Membership_Visa_Recommendations, PlaceOfEmbassy
from hallbookingapp.models import HallLocation



def visa_pre_condition(request):
    """
    code for rendering on following HTML file

    **Template:**

    :template:`visarecommendation/pre_condition.html`
    """
    user_detail_id = ''
    data={}
    if not request.user.is_anonymous():
        if request.session['user_type'] == 'frontend':
            user_detail_id = request.user.membershipuser.userdetail.id
    data={
        'user_detail_id':user_detail_id
    }
    return render(request, 'visarecommendation/pre_condition.html',data)



def visa_recommendations(request):
    """
    code for for rendering if user is logged in

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.UserDetail`.

    **Template:**

    :template:`visarecommendation/visa_recommendation.html`
    """
    data={}
    countryObj = Country.objects.filter(is_deleted=False)
    locationObj = HallLocation.objects.filter(is_deleted=False)
    if not request.user.is_anonymous():
        if request.session['user_type'] == 'frontend':
            member_obj = UserDetail.objects.get(id=request.user.membershipuser.userdetail.id)
            data={
                'countryObj':countryObj,
                'locationObj':locationObj,
                'member_associate_no':member_obj.member_associate_no,
                'enroll_type':member_obj.enroll_type,
                'ceo_name':member_obj.ceo_name,
                'ceo_designation':member_obj.ceo_designation,
                'company_name':member_obj.company.company_name if member_obj.company else None, 
                'correspond_address':member_obj.correspond_address,
                'ceo_cellno':member_obj.ceo_cellno,
                'ceo_email':member_obj.ceo_email
            }
            return render(request, 'visarecommendation/visa_recommendation.html',data)
        return render(request, 'visarecommendation/pre_condition.html')
    else:
        return render(request, 'visarecommendation/pre_condition.html')




import datetime
from dateutil import tz 

@transaction.atomic()
@csrf_exempt
def save_visa_recommendation_detail(request):
    """
    Code for saving new Visa recommendation object

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.Membership_Visa_Recommendations`.

    """
    sid = transaction.savepoint()

    try:
        print 'Request IN | visa_recommendation | save_visa_recommendation_detail | user %s', request.user
        try:
            if request.POST.get('PassportCopyFlag') == 'YES':
                passport_copy= "YES"
                passportDoc = request.FILES['passportDoc']
            else:
                passport_copy = "NO"
                passportDoc = ''

            visafromDate = datetime.datetime.strptime(request.POST.get('txtFDate'),'%m/%d/%Y')

            print request.POST.get('txtFDate'), visafromDate
            passport_valid_from_date = datetime.datetime.strptime(request.POST.get('txtVFDate'),'%m/%d/%Y')
            passport_valid_to_date = datetime.datetime.strptime(request.POST.get('txtVTDate'),'%m/%d/%Y')

         
            try:
                member_obj = UserDetail.objects.get(member_associate_no=request.POST.get('membershipId'))

                try:
                    visa_rec_obj = Membership_Visa_Recommendations.objects.filter().last()
                    rec_no = int(visa_rec_obj.visa_recommendation_no[3:]) + 1
                    rec_no = str(rec_no).zfill(6)
                    rec_no = 'VRL'+str(rec_no)
                except Exception as e :
                    print e
                    rec_no = 'VRL000001'
                    pass

                from_zone = tz.tzutc()
                to_zone = tz.gettz('Asia/Kolkata')                

                visaRecommendations = Membership_Visa_Recommendations(  
                                    visa_recommendation_no = rec_no,                                  
                                    to_which_country = Country.objects.get(id=request.POST.get('drpCountry')),
                                    location = HallLocation.objects.get(id=request.POST.get('McciaLocation')),
                                    place_of_embassy = PlaceOfEmbassy.objects.get(id=request.POST.get('drpEmbasy')),
                                    person_title = request.POST.get('PersonTitle'),
                                    person_name = request.POST.get('txtName').title(),
                                    person_designation = request.POST.get('txtDesg'),
                                    mobile_no = request.POST.get('txtContact'),
                                    email = request.POST.get('txtEmail'),
                                    purpose_to_visit = request.POST.get('PurposeToVisit'),
                                    visiting_from_date = visafromDate,
                                    visa_type = request.POST.get('VisaType'),
                                    radio_choice = request.POST.get('radioChoices'),
                                    passport_no = request.POST.get('passport_no'),
                                    passport_valid_from_date = passport_valid_from_date,
                                    passport_valid_to_date = passport_valid_to_date,
                                    mcciamember = UserDetail.objects.get(id=member_obj.id),
                                    company_name = request.POST.get('txtCompany'),
                                    passport_copy = passport_copy,
                                    address = request.POST.get('txtAdd').strip(),
                                    visitDurations = request.POST.get('visitDurations'),
                                    total_visit_durations = request.POST.get('TotalvisitDurations'),
                                    doc_file = passportDoc,
                                    created_date=datetime.datetime.now().replace(tzinfo=from_zone).astimezone(to_zone)
                                    )

                visaRecommendations.save()

                transaction.savepoint_commit(sid)

                send_visa_ack_mail(visaRecommendations)


                data = {'success': 'true'}
                print 'Request OUT | visa_recommendation | save_visa_recommendation_detail | user %s', request.user
                return HttpResponse(json.dumps(data), content_type='application/json')

            except Exception as exc:
                print '>>>>>>>>>Exception>>>>>>>>',exc    
                print 'exception ', str(traceback.print_exc())
                data = {'success': 'false'} 


            #
        except Exception, exc:
            print 'exception ', str(traceback.print_exc())
            transaction.rollback(sid)
            data = {'success': 'false'}            
            print 'exception in Member Visa Recommendation SAVING ', str(traceback.print_exc())



    except Exception, exc:
        print 'exception ', str(traceback.print_exc())
        transaction.rollback(sid)
        data = {'success': 'false'}
        print 'Exception | visa_recommendation | save_visa_recommendation_detail | user %s. Exception = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')

from django.template import Context
from django.template.loader import render_to_string, get_template
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import os
from django.conf import settings
import smtplib

charset = 'utf-8'

def send_visa_ack_mail(visaRecommendations):
    """
    Code for sending acknowledge mail locationvise

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.Membership_Visa_Recommendations`.

    """
    try:
        data = {'visaRecommendations':visaRecommendations}
        location = HallLocation.objects.get(id=visaRecommendations.location.id)
        if location.location == 'Hadapsar':
            mait_cc_list = ['roshnim@mcciapune.com','mandarm@mcciapune.com']
            email_username = "visahadapsar@mcciapune.com"
            email_paswd = "visa@2017hadapsar"       

        elif location.location == 'Bhosari':
            mait_cc_list = ['sasidharan@mcciapune.com']
            email_username = "visabhosari@mcciapune.com"
            email_paswd = "visa@2013bhosari"       

        elif location.location == 'Tilak Road':
            mait_cc_list = ['yashodhanj@mcciapune.com','shrikantk@mcciapune.com']
            email_username = "visatilakrd@mcciapune.com"
            email_paswd = "visa@2013tilakrd"             

        elif location.location == 'MCCIA Trade Tower (5th Floor)':
            mait_cc_list = ['madhurac@mcciapune.com','snigdhag@mcciapune.com','sonalp@mcciapune.com']
            email_username = "visaicc@mcciapune.com"
            email_paswd = "visa@2013icc"            


        imgpath=os.path.join(settings.BASE_DIR, "site-static/assets/MCCIA-logo.png")
        fp = open(imgpath, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<img1>')

        gmail_user = email_username
        gmail_pwd = email_paswd 

        user_email = visaRecommendations.email
        mait_to_list = [visaRecommendations.email]
        TO = mait_to_list  
        CC = mait_cc_list

        html=get_template('visarecommendation/visa_acknowledgement.html').render(Context(data))
        msg = MIMEMultipart('related')
        htmlfile = MIMEText(html, 'html',_charset=charset)
        msg.attach(htmlfile)
        msg.attach(msgImage)

        server = smtplib.SMTP("mcciapune.mithiskyconnect.com", 587) 
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        
        subject_line = 'Visa Recommendation Acknowledgement'
        msg['subject'] = str(subject_line)
        msg['from'] = 'mailto: <'+email_username+'>'
        msg['to'] = ",".join(TO)
        msg['cc'] = ",".join(CC)
        toaddrs = TO + CC
        server.sendmail(msg['from'], toaddrs, msg.as_string())
        server.quit()   
        print '\nMail Sent'
        return
    except Exception,e:
        print '\nMail NOT Sent',str(traceback.print_exc())
        return    

def get_embassy_location(request):
    """
    For getting embassy location depend on given country ID

    **Context**

    ``mymodel``
        An instance of :model:`visarecommendationapp.PlaceOfEmbassy`.

    """
    try:
        embassy_list = []
        embassy_obj_list = PlaceOfEmbassy.objects.filter(country=request.GET.get('country_id'),is_deleted=False)
        for obj in embassy_obj_list:            
            embassy_list.append(
                {'id': obj.id, 'embassy_name': obj.embassy_name +', '+ obj.city })
        data ={
            'success':'true',
            'embassy_list':embassy_list,
        }
    except Exception, e:
        print 'Exception ', e
        data = {'success':'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')      



