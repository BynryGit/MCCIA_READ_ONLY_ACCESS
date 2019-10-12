
# System Packages
import json
import traceback
from decimal import Decimal
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# User Model

from awardsapp.models import AwardDetail, AwardRegistration
from adminapp.models import City


@csrf_exempt
@transaction.atomic
def save_award_registration(request):
    data = {}
    sid = transaction.savepoint()
    output = False
    try:
        print '\nRequest IN | awardsapp | save_award.py | save_award_registration | User = ', request.user
        if request.POST.get('form_type') == 'bg_deshmukh_form':
            output = save_bg_deshmukh_form(request)
        elif request.POST.get('form_type') == 'three_form':
            output = save_parkhe_hari_ramabai_form(request)
        elif request.POST.get('form_type') == 'natu_form':
            output = save_natu_form(request)
        else:
            output = save_rathi_form(request)
        if output:
            transaction.savepoint_commit(sid)
            data['success'] = 'true'
        else:
            transaction.rollback(sid)
            data['success'] = 'false'
        print '\nResponse OUT | awardsapp | save_award.py | save_award_registration | User = ', request.user
    except Exception, e:
        print '\nException IN | awardsapp | save_award.py | save_award_registration | EXCP = ', str(traceback.print_exc())
        transaction.rollback(sid)
        data['success'] = 'false'
    return HttpResponse(json.dumps(data), content_type='application/json')


def save_bg_deshmukh_form(request):
    try:
        print '\nRequest IN | awardsapp | save_award.py | save_bg_deshmukh_form | User = ', request.user
        new_award_reg = AwardRegistration(
            awarddetail=AwardDetail.objects.get(id=request.POST.get('award_id')),
            company_name=str(request.POST.get('bg_award_company_name')).strip(),
            concerned_person_name=str(request.POST.get('bg_award_concerned_person_name')).strip(),
            address=str(request.POST.get('bg_award_address')).strip(),
            city=City.objects.get(id=request.POST.get('bg_award_city')),
            pin_code=int(request.POST.get('bg_award_pin')),
            telephone_no=str(request.POST.get('bg_award_telephone_no')).strip(),
            fax_no=str(request.POST.get('bg_award_fax_no')).strip(),
            establish_year=int(request.POST.get('bg_award_establish_year')),
            org_chief_name=str(request.POST.get('bg_award_chief_org_name')).strip(),
            org_chief_designation=str(request.POST.get('bg_award_chief_org_designation')).strip(),
            product_description=str(request.POST.get('bg_award_brief_description_award')).strip(),
            product_feature_advantage=str(request.POST.get('bg_award_benefit')).strip()
        )
        new_award_reg.save()
        print '\nResponse OUT | awardsapp | save_award.py | save_bg_deshmukh_form | User = ', request.user
        return True
    except Exception, e:
        print '\nException IN | awardsapp | save_award.py | save_bg_deshmukh_form | EXCP = ', str(traceback.print_exc())
        return False


def save_parkhe_hari_ramabai_form(request):
    try:
        print '\nRequest IN | awardsapp | save_award.py | save_parkhe_hari_ramabai_form | User = ', request.user
        new_award_reg = AwardRegistration(
            awarddetail=AwardDetail.objects.get(id=request.POST.get('award_id')),
            company_name=str(request.POST.get('company_name')).strip(),
            concerned_person_name=str(request.POST.get('concerned_person_name')).strip(),
            address=str(request.POST.get('address')).strip(),
            city=City.objects.get(id=request.POST.get('city')),
            pin_code=int(request.POST.get('pin')),
            telephone_no=str(request.POST.get('telephone_no')).strip(),
            fax_no=str(request.POST.get('fax_no')).strip(),
            establish_year=int(request.POST.get('establish_year')),
            org_chief_name=str(request.POST.get('chief_org_name')).strip(),
            org_chief_designation=str(request.POST.get('chief_org_designation')).strip(),
            product=str(request.POST.get('product_tendered_for_award')).strip(),
            product_description=str(request.POST.get('brief_description_award')).strip(),
            product_feature_advantage=str(request.POST.get('product_feature')).strip(),
            product_manufacture_date=datetime.strptime(str(request.POST.get('manufacture_date')).strip(), '%m/%d/%Y').date() if request.POST.get('manufacture_date') else None,
            commercial_launch_date=datetime.strptime(str(request.POST.get('launch_date')).strip(), '%m/%d/%Y').date() if request.POST.get('launch_date') else None,
            to_year_one=int(request.POST.get('to_year_one')) if request.POST.get('to_year_one') else 0,
            to_year_two=int(request.POST.get('to_year_two')) if request.POST.get('to_year_two') else 0,
            to_year_three=int(request.POST.get('to_year_three')) if request.POST.get('to_year_three') else 0,
            profit_year_one=int(request.POST.get('profit_year_one')) if request.POST.get('profit_year_one') else 0,
            profit_year_two=int(request.POST.get('profit_year_two')) if request.POST.get('profit_year_two') else 0,
            profit_year_three=int(request.POST.get('profit_year_three')) if request.POST.get('profit_year_three') else 0,
            to_one=Decimal(request.POST.get('to_one')) if request.POST.get('to_one') else 0,
            to_two=Decimal(request.POST.get('to_two')) if request.POST.get('to_two') else 0,
            to_three=Decimal(request.POST.get('to_three')) if request.POST.get('to_three') else 0,
            profit_one=Decimal(request.POST.get('profit_one')) if request.POST.get('profit_one') else 0,
            profit_two=Decimal(request.POST.get('profit_two')) if request.POST.get('profit_two') else 0,
            profit_three=Decimal(request.POST.get('profit_three')) if request.POST.get('profit_three') else 0,
        )
        new_award_reg.save()
        print '\nResponse OUT | awardsapp | save_award.py | save_parkhe_hari_ramabai_form | User = ', request.user
        return True
    except Exception, e:
        print '\nException IN | awardsapp | save_award.py | save_parkhe_hari_ramabai_form | EXCP = ', str(traceback.print_exc())
        return False


def save_natu_form(request):
    try:
        print '\nRequest IN | awardsapp | save_award.py | save_natu_form | User = ', request.user
        new_award_reg = AwardRegistration(
            awarddetail=AwardDetail.objects.get(id=request.POST.get('award_id')),
            person_name=str(request.POST.get('natu_name')).strip(),
            first_gen_entp=True if request.POST.get('first_entp') == 'Yes' else False,
            company_name=str(request.POST.get('natu_company_name')).strip(),
            commencement_date=datetime.strptime(str(request.POST.get('commence_date')), '%m/%d/%Y').date() if request.POST.get('commence_date') else None,
            starting_capital=Decimal(request.POST.get('starting_capital')) if request.POST.get('starting_capital') else 0,
            address=str(request.POST.get('natu_address')).strip(),
            city=City.objects.get(id=request.POST.get('natu_city')),
            pin_code=int(request.POST.get('natu_pin')),
            telephone_no=str(request.POST.get('natu_telephone_no')).strip(),
            fax_no=str(request.POST.get('natu_fax_no')).strip(),
            email=str(request.POST.get('email')).strip(),
            msme_reg_no=str(request.POST.get('msme_reg_no')).strip() if request.POST.get('msme_reg_no') else None,
            msme_reg_date=datetime.strptime(str(request.POST.get('msme_reg_date')), '%m/%d/%Y').date() if request.POST.get('msme_reg_date') else None,
            legal_status=int(request.POST.get('legalStatus')),
            no_of_employees=int(request.POST.get('no_of_employees')),
            product=str(request.POST.get('natu_product_name')).strip(),
            product_description=str(request.POST.get('natu_product_description')).strip(),
            locations=str(request.POST.get('natu_location')).strip(),
            gross_block_investment=Decimal(request.POST.get('gross_investment')) if request.POST.get('gross_investment') else 0,
            plant_and_mc_investment=Decimal(request.POST.get('plant_investment')) if request.POST.get('plant_investment') else 0,
            net_block_investment=Decimal(request.POST.get('net_investment')) if request.POST.get('net_investment') else 0,
            to_year_one=int(request.POST.get('natu_to_year_one')) if request.POST.get('natu_to_year_one') else 0,
            to_year_two=int(request.POST.get('natu_to_year_two')) if request.POST.get('natu_to_year_two') else 0,
            to_year_three=int(request.POST.get('natu_to_year_three')) if request.POST.get('natu_to_year_three') else 0,
            profit_year_one=int(request.POST.get('natu_profit_year_one')) if request.POST.get('natu_profit_year_one') else 0,
            profit_year_two=int(request.POST.get('natu_profit_year_two')) if request.POST.get('natu_profit_year_two') else 0,
            profit_year_three=int(request.POST.get('natu_profit_year_three')) if request.POST.get(
                'natu_profit_year_three') else 0,
            to_one=Decimal(request.POST.get('natu_to_one')) if request.POST.get('natu_to_one') else 0,
            to_two=Decimal(request.POST.get('natu_to_two')) if request.POST.get('natu_to_two') else 0,
            to_three=Decimal(request.POST.get('natu_to_three')) if request.POST.get('natu_to_three') else 0,
            profit_one=Decimal(request.POST.get('natu_profit_one')) if request.POST.get('natu_profit_one') else 0,
            profit_two=Decimal(request.POST.get('natu_profit_two')) if request.POST.get('natu_profit_two') else 0,
            profit_three=Decimal(request.POST.get('natu_profit_three')) if request.POST.get('natu_profit_three') else 0,
            patent_registered=True if str(request.POST.get('Patent_Radio')) == 'Patent Yes' else False,
            award_recognition=str(request.POST.get('award_recog')).strip(),
            certification_list=str(request.POST.get('cert_list')).strip(),
            about_yourself=str(request.POST.get('about_you')).strip(),
        )
        new_award_reg.save()
        print '\nResponse OUT | awardsapp | save_award.py | save_natu_form | User = ', request.user
        return True
    except Exception, e:
        print '\nException IN | awardsapp | save_award.py | save_natu_form | EXCP = ', str(traceback.print_exc())
        return False


def save_rathi_form(request):
    try:
        print '\nRequest IN | awardsapp | save_award.py | save_rathi_form | User = ', request.user
        new_award_reg = AwardRegistration(
            awarddetail=AwardDetail.objects.get(id=request.POST.get('award_id')),
            company_name=str(request.POST.get('rathi_company_name')).strip(),
            concerned_person_name=str(request.POST.get('rathi_concerned_person_name')).strip(),
            address=str(request.POST.get('rathi_address')).strip(),
            city=City.objects.get(id=request.POST.get('rathi_city')),
            pin_code=int(request.POST.get('rathi_pin')),
            telephone_no=str(request.POST.get('rathi_telephone_no')).strip(),
            fax_no=str(request.POST.get('rathi_fax_no')).strip(),
            establish_year=int(request.POST.get('rathi_establish_year')),
            org_chief_name=str(request.POST.get('rathi_chief_org_name')).strip(),
            org_chief_designation=str(request.POST.get('rathi_chief_org_designation')).strip(),
            product_description=str(request.POST.get('rathi_initiative_content')).strip(),
        )
        new_award_reg.save()
        print '\nResponse OUT | awardsapp | save_award.py | save_rathi_form | User = ', request.user
        return True
    except Exception, e:
        print '\nException IN | awardsapp | save_award.py | save_rathi_form | EXCP = ', str(traceback.print_exc())
        return False