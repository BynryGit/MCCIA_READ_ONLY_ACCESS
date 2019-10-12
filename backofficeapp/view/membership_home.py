
# System Packages

import traceback
import StringIO
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from captcha_form import CaptchaForm
from django.shortcuts import *
from django.db import transaction
import pdb
import json
from captcha_form import CaptchaForm
from django.db.models import Q
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
from xlsxwriter.workbook import Workbook
from datetime import datetime, timedelta

# User Models

from membershipapp.models import HOD_Detail, CompanyDetail, UserDetail, MembershipInvoice, PaymentDetails, Top3Member
from adminapp.models import MembershipCategory, IndustryDescription, NameSign

from authenticationapp.decorator import role_required
from django.contrib.auth.decorators import login_required


# @login_required(login_url='/backofficeapp/login/')
@csrf_exempt
def membership_home(request):
    print "backofficeapp | view | membership_home.py | membership_home"
    return render(request, 'backoffice/membership/supplier_list.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Category'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def membership_category(request):
    return render(request, 'backoffice/membership/Membership_category.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Category'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def add_membership_category(request):
    return render(request, 'backoffice/membership/add_membership_category.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Certificate Dispatched'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def membership_certificate_dispatched(request):
    industry_list = IndustryDescription.objects.filter(is_active=True)
    data = {'industry_list': industry_list}
    return render(request, 'backoffice/membership/membership_certificate_dispatched.html', data)


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=[' Executive Committee Member'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def executive_committee_members(request):
    industry_list = IndustryDescription.objects.filter(is_active=True)
    data = {'industry_list': industry_list}
    return render(request, 'backoffice/membership/executive_committee_members.html', data)


def download_payment_label(request):
    return render(request, 'backoffice/membership/payment_label.html')

def membership_certificate(request):
    return render(request, 'backoffice/membership/membership_certificate_landing.html')

@csrf_exempt
def top3_members(request):
    return render(request, 'backoffice/membership/top_3_members.html')


@csrf_exempt
def add_top3_members(request):
    return render(request, 'backoffice/membership/add_top3_members.html')


@csrf_exempt
def slab(request):
    return render(request, 'backoffice/membership/slab.html')


@csrf_exempt
def add_new_slab(request):
    return render(request, 'backoffice/membership/add_new_slab.html')

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Exclude Mail Member'],login_url='/backofficeapp/login/',raise_exception=True)
@csrf_exempt
def exclude_mailing_members(request):
    industry_list = IndustryDescription.objects.filter(is_active=True)
    data = {'industry_list': industry_list}
    return render(request, 'backoffice/membership/exclude_mail_members.html', data)

@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Valid / Invalid Member'],login_url='/backofficeapp/login/',raise_exception=True)
def valid_invalid_member(request):
    print '\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>In Valid Invalid>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    industry_list = IndustryDescription.objects.filter(is_active=True)
    data = {'industry_list': industry_list}
    return render(request, 'backoffice/membership/valid_invalid_member.html', data)


def about_us(request):
    return render(request, 'terms_and_condition/About_us.html')


def faq(request):
    return render(request, 'terms_and_condition/FAQ.html')


def listing_policy(request):
    return render(request, 'terms_and_condition/Listing_Policy.html')


def privacy_policy(request):
    return render(request, 'terms_and_condition/PrivacyPolicy.html')


def terms_of_use(request):
    return render(request, 'terms_and_condition/Terms_of_use.html')

# Save Membership Category
@transaction.atomic
@csrf_exempt
def save_membership_category(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nsave_membership_category view'
        membership_category = MembershipCategory(membership_category=str(request.POST.get('category')),
                                                 membership_type=str(request.POST.get('category_type')))
        membership_category.save()
        transaction.savepoint_commit(sid)
        print '\nResponse OUT | save_membership_category'
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | save_membership_category = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Populate Membership Category Table
def get_membership_category_table(request):
    data = {}
    try:
        dataList = []

        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        filter_status = request.GET.get('mem_cat_status')

        membership_category_list = ''

        if filter_status != 'show_all':
            membership_category_list = MembershipCategory.objects.filter(
                status=True if filter_status == 'True' else False,
                is_deleted=False)
        else:
            membership_category_list = MembershipCategory.objects.filter(is_deleted=False)
        print 'membership_category_list=', membership_category_list
        membership_category_list = membership_category_list.filter(Q(membership_category__icontains=searchTxt) |
                                                                   Q(membership_type__icontains=searchTxt))
        
        total_records = membership_category_list.count()
        if length != -1:
            membership_category_list = membership_category_list[start:length]
        else:
            membership_category_list = membership_category_list[::-1]
        total_record = total_records

        i = 1
        for membership_category in membership_category_list:
            temp_list = []
            if membership_category.membership_type != '' and membership_category.membership_type is not None:
                temp_list.append(i)
                temp_list.append(membership_category.membership_category)
                temp_list.append(membership_category.membership_type)

                action_two = ''

                if membership_category.status is True:
                    temp_list.append('<label class="label label-success">Active</label>')
                    mem_cat_status = 'True'
                    action_two = '<a class="icon-trash" title="Change Status" data-toggle="modal" data-target="#active_deactive_mem_cat" onclick=update_mem_cat(' + '"' + str(
                        mem_cat_status) + '"' + ',' + str(membership_category.id) + ')></a>&nbsp;&nbsp;'
                else:
                    temp_list.append('<label class="label label-default">Inactive</label>')
                    mem_cat_status = 'False'
                    action_two = '<a class="icon-reload" title="Change Status" data-toggle="modal" data-target="#active_deactive_mem_cat" onclick=update_mem_cat(' + '"' + str(
                        mem_cat_status) + '"' + ',' + str(membership_category.id) + ')></a>&nbsp;&nbsp;'

                action = '<a class="fa fa-pencil" title="Membership Category" data-toggle="modal" data-target="#update_membership_cat_modal" onclick=show_edit_membership_category(' + str(
                    membership_category.id) + ')></a>&nbsp; &nbsp;'

                temp_list.append(action_two + action)
                dataList.append(temp_list)
                i = i + 1
        
        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        print '\nResponse OUT | get_membership_category_table'
    except Exception, e:
        print '\nException | get_membership_category_table = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Change Membership Category Status
@transaction.atomic
def update_membership_category_status(request):
    data = {}
    sid = transaction.savepoint()
    try:
        membership_category_obj = MembershipCategory.objects.get(id=str(request.GET.get('mem_cat_id')))
        if membership_category_obj.status is True:
            membership_category_obj.status = False
        else:
            membership_category_obj.status = True

        membership_category_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print '\nResponse OUT | update_membership_category_status'
    except Exception, e:
        print '\nException | update_membership_category_status = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Show Membership Category Form
def show_edit_membership_category(request):
    data = {}
    try:
        membership_category_obj = MembershipCategory.objects.get(id=str(request.GET.get('mem_cat_id')))
        data = {'success': 'true', 'mem_cat': membership_category_obj.membership_category,
                'mem_cat_type': membership_category_obj.membership_type}
    except Exception, e:
        print '\nException | show_edit_membership_category = ', str(traceback.print_exc())
        data = {'success': 'false'}
    return HttpResponse(json.dumps(data), content_type='application/json')


# Update Membership Category
@csrf_exempt
@transaction.atomic
def update_membership_category(request):
    data = {}
    sid = transaction.savepoint()
    try:
        membership_category_obj = MembershipCategory.objects.get(id=str(request.POST.get('mem_cat_id')))
        membership_category_obj.membership_category = str(request.POST.get('edit_cat'))
        membership_category_obj.membership_type = str(request.POST.get('edit_cat_type'))
        membership_category_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_membership_category = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Populate Executive Committee Member
def get_executive_committee_member_table(request):
    data = {}
    try:
        dataList = []
        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':
            order = "-"
        start = int(request.GET.get('start'))
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        industry = request.GET.get('industry_val')
        member_association_val = request.GET.get('member_association_val')
        executive_member = request.GET.get('executive_member')

        executive_committee_member_list = ''

        if industry == 'show_all' and member_association_val == 'show_all' and executive_member == 'show_all':
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False)
        elif industry == 'show_all' and member_association_val == 'show_all' and executive_member != 'show_all':
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                        executive_committee_member=True if executive_member == 'True' else False)
        elif industry == 'show_all' and member_association_val != 'show_all' and executive_member == 'show_all':
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                        user_type=member_association_val)
        elif industry == 'show_all' and member_association_val != 'show_all' and executive_member != 'show_all':
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                        executive_committee_member=True if executive_member == 'True' else False,
                                                                        user_type=member_association_val)
        elif industry != 'show_all' and member_association_val == 'show_all' and executive_member == 'show_all':
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                        company__industrydescription__id=industry)
        elif industry != 'show_all' and member_association_val == 'show_all' and executive_member != 'show_all':
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                        company__industrydescription__id=industry,
                                                                        executive_committee_member=True if executive_member == 'True' else False)
        elif industry != 'show_all' and member_association_val != 'show_all' and executive_member == 'show_all':
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                        company__industrydescription__id=industry,
                                                                        user_type=member_association_val)
        else:
            executive_committee_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                        company__industrydescription__id=industry,
                                                                        executive_committee_member=True if executive_member == 'True' else False,
                                                                        user_type=member_association_val)

        executive_committee_member_list = executive_committee_member_list.filter(
            Q(company__company_name__icontains=searchTxt) |
            Q(member_associate_no__icontains=searchTxt))

        total_records = executive_committee_member_list.count()
        if length != -1:
            executive_committee_member_list = executive_committee_member_list[start:length]
        else:
            executive_committee_member_list = executive_committee_member_list[::-1]
        total_record = total_records

        i = 1
        for item in executive_committee_member_list:
            temp_list = []
            temp_list.append(i)
            temp_list.append(str(item.membership_year)[0:9])
            temp_list.append(str(item.member_associate_no) if item.member_associate_no else '')
            temp_list.append(item.company.company_name if item.company else '')
            temp_list.append('0.0')
            temp_list.append('0.0')
            temp_list.append('0.0')
            temp_list.append(str(item.annual_turnover_rupees))
            temp_list.append(item.ceo_email)
            temp_list.append(item.ceo_cellno)

            if item.executive_committee_member is True:
                temp_list.append('<label class="label label-success">Yes</label>')
            else:
                temp_list.append('<label class="label label-default">No</label>')

            member_type = 'executive_committee_member'
            status = str(item.executive_committee_member)
            action = '<a class="fa fa-pencil" data-toggle="modal" data-target=#active_deactive_executive onclick=update_member(' + '"' + str(
                member_type) + '"' + ',' + str(item.id) + ',' + '"' + str(status) + '"' + ')></a>'

            temp_list.append(action)
            dataList.append(temp_list)
            i = i + 1

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        print '\nResponse OUT | get_executive_committee_member_table'
    except Exception, e:
        print '\nException | get_executive_committee_member_table = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Populate Valid / Invalid Member
def get_valid_invalid_member_table(request):
    data = {}
    try:
        dataList = []

        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        industry = request.GET.get('industry_val')
        member_association_val = request.GET.get('member_association_val')
        valid_invalid_member_status = request.GET.get('valid_invalid_member')

        valid_invalid_member_list = ''

        if industry == 'show_all' and member_association_val == 'show_all' and valid_invalid_member_status == 'show_all':
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False)
        elif industry == 'show_all' and member_association_val == 'show_all' and valid_invalid_member_status != 'show_all':
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                  valid_invalid_member=True if valid_invalid_member_status == 'True' else False)
        elif industry == 'show_all' and member_association_val != 'show_all' and valid_invalid_member_status == 'show_all':
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                  user_type=member_association_val)
        elif industry == 'show_all' and member_association_val != 'show_all' and valid_invalid_member_status != 'show_all':
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                  valid_invalid_member=True if valid_invalid_member_status == 'True' else False,
                                                                  user_type=member_association_val)
        elif industry != 'show_all' and member_association_val == 'show_all' and valid_invalid_member_status == 'show_all':
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                  company__industrydescription__id=industry)
        elif industry != 'show_all' and member_association_val == 'show_all' and valid_invalid_member_status != 'show_all':
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                  company__industrydescription__id=industry,
                                                                  valid_invalid_member=True if valid_invalid_member_status == 'True' else False)
        elif industry != 'show_all' and member_association_val != 'show_all' and valid_invalid_member_status == 'show_all':
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                  company__industrydescription__id=industry,
                                                                  user_type=member_association_val)
        else:
            valid_invalid_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                  company__industrydescription__id=industry,
                                                                  valid_invalid_member=True if valid_invalid_member_status == 'True' else False,
                                                                  user_type=member_association_val)

        valid_invalid_member_list = valid_invalid_member_list.filter(Q(company__company_name__icontains=searchTxt)|
                                                                     Q(member_associate_no__icontains=searchTxt))

        
        total_records = valid_invalid_member_list.count()
        if length != -1:
            valid_invalid_member_list = valid_invalid_member_list[start:length]
        else:
            valid_invalid_member_list = valid_invalid_member_list[::-1]
        total_record = total_records

        i = 1
        for item in valid_invalid_member_list:
            temp_list = []
            temp_list.append(i)
            temp_list.append(str(item.membership_year)[0:9])
            temp_list.append(str(item.member_associate_no) if item.member_associate_no else '')
            temp_list.append(item.company.company_name if item.company else '')
            temp_list.append(item.ceo_email)
            temp_list.append(item.ceo_cellno)

            if item.valid_invalid_member is True:
                temp_list.append('<label class="label label-success">Valid</label>')
            else:
                temp_list.append('<label class="label label-default">Invalid</label>')

            member_type = 'valid_invalid_member'
            status = str(item.valid_invalid_member)
            action = '<a class="fa fa-pencil" data-toggle="modal" data-target=#active_deactive_valid_invalid_mem onclick=update_member(' + '"' + str(
                member_type) + '"' + ',' + str(item.id) + ',' + '"' + str(status) + '"' + ')></a>'

            temp_list.append(action)
            dataList.append(temp_list)
            i = i + 1

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        print '\nResponse OUT | get_valid_invalid_member_table'
    except Exception, e:
        print '\nException | get_valid_invalid_member_table = ', e
    return HttpResponse(json.dumps(data), content_type='application/json')


# Populate Exclude From Mail Member
def get_exclude_mail_member_table(request):
    data = {}
    try:
        dataList = []

        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        industry = request.GET.get('industry_val')
        member_association_val = request.GET.get('member_association_val')
        excluded_mail_member = request.GET.get('excluded_mail_member')

        exclude_mail_member_list = ''

        if industry == 'show_all' and member_association_val == 'show_all' and excluded_mail_member == 'show_all':
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False)
        elif industry == 'show_all' and member_association_val == 'show_all' and excluded_mail_member != 'show_all':
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                 exclude_from_mailing=True if excluded_mail_member == 'True' else False)
        elif industry == 'show_all' and member_association_val != 'show_all' and excluded_mail_member == 'show_all':
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                 user_type=member_association_val)
        elif industry == 'show_all' and member_association_val != 'show_all' and excluded_mail_member != 'show_all':
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                 exclude_from_mailing=True if excluded_mail_member == 'True' else False,
                                                                 user_type=member_association_val)
        elif industry != 'show_all' and member_association_val == 'show_all' and excluded_mail_member == 'show_all':
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                 company__industrydescription__id=industry)
        elif industry != 'show_all' and member_association_val == 'show_all' and excluded_mail_member != 'show_all':
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                 company__industrydescription__id=industry,
                                                                 exclude_from_mailing=True if excluded_mail_member == 'True' else False)
        elif industry != 'show_all' and member_association_val != 'show_all' and excluded_mail_member == 'show_all':
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                 company__industrydescription__id=industry,
                                                                 user_type=member_association_val)
        else:
            exclude_mail_member_list = UserDetail.objects.filter(is_deleted=False,
                                                                 company__industrydescription__id=industry,
                                                                 exclude_from_mailing=True if excluded_mail_member == 'True' else False,
                                                                 user_type=member_association_val)
        exclude_mail_member_list = exclude_mail_member_list.filter(
            Q(company__company_name__icontains=searchTxt) |
            Q(member_associate_no__icontains=searchTxt))

        total_records = exclude_mail_member_list.count()
        if length != -1:
            exclude_mail_member_list = exclude_mail_member_list[start:length]
        else:
            exclude_mail_member_list = exclude_mail_member_list[::-1]
        total_record = total_records

        i = 1
        for item in exclude_mail_member_list:
            temp_list = []
            temp_list.append(i)
            temp_list.append(item.membership_year)
            temp_list.append(str(item.member_associate_no) if item.member_associate_no else '')
            temp_list.append(item.company.company_name if item.company else '')
            temp_list.append(item.ceo_email)
            temp_list.append(item.ceo_cellno)

            if item.exclude_from_mailing is True:
                temp_list.append('<label class="label label-success">Yes</label>')
            else:
                temp_list.append('<label class="label label-default">No</label>')

            member_type = 'exclude_from_mail'
            status = str(item.exclude_from_mailing)
            action = '<a class="fa fa-pencil" data-toggle="modal" data-target=#active_deactive_exclude_mail onclick=update_member(' + '"' + str(
                member_type) + '"' + ',' + str(item.id) + ',' + '"' + str(status) + '"' + ')></a>'

            temp_list.append(action)
            dataList.append(temp_list)
            i = i + 1

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        print '\nResponse OUT | get_exclude_mail_member_table'
    except Exception, e:
        print '\nException | get_exclude_mail_member_table = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Populate Membership Certificate Dispatch
def get_membership_certificate_table(request):
    data = {}
    try:
        dataList = []

        column = request.GET.get('order[0][column]')
        searchTxt = request.GET.get('search[value]')
        search = '%' + (searchTxt) + '%'
        order = ""
        if request.GET.get('order[0][dir]') == 'desc':  # desc or not
            order = "-"
        start = int(request.GET.get('start'))  # pagination length say 10 25 50 etc
        length = int(request.GET.get('length')) + int(request.GET.get('start'))
        total_record = ''

        industry = request.GET.get('industry_val')
        member_association_val = request.GET.get('member_association_val')
        member_certificate_dispatch = request.GET.get('member_certificate_dispatch')

        membership_certificate_dispatched_list = ''

        if industry == 'show_all' and member_association_val == 'show_all' and member_certificate_dispatch == 'show_all':
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False)
        elif industry == 'show_all' and member_association_val == 'show_all' and member_certificate_dispatch != 'show_all':
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False,
                                                                               membership_ceritificate_dispatch=True if member_certificate_dispatch == 'True' else False)
        elif industry == 'show_all' and member_association_val != 'show_all' and member_certificate_dispatch == 'show_all':
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False,
                                                                               user_type=member_association_val)
        elif industry == 'show_all' and member_association_val != 'show_all' and member_certificate_dispatch != 'show_all':
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False,
                                                                               membership_ceritificate_dispatch=True if member_certificate_dispatch == 'True' else False,
                                                                               user_type=member_association_val)
        elif industry != 'show_all' and member_association_val == 'show_all' and member_certificate_dispatch == 'show_all':
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False,
                                                                               company__industrydescription__id=industry)
        elif industry != 'show_all' and member_association_val == 'show_all' and member_certificate_dispatch != 'show_all':
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False,
                                                                               company__industrydescription__id=industry,
                                                                               membership_ceritificate_dispatch=True if member_certificate_dispatch == 'True' else False)
        elif industry != 'show_all' and member_association_val != 'show_all' and member_certificate_dispatch == 'show_all':
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False,
                                                                               company__industrydescription__id=industry,
                                                                               user_type=member_association_val)
        else:
            membership_certificate_dispatched_list = UserDetail.objects.filter(is_deleted=False,
                                                                               company__industrydescription__id=industry,
                                                                               membership_ceritificate_dispatch=True if member_certificate_dispatch == 'True' else False,
                                                                               user_type=member_association_val)
        membership_certificate_dispatched_list = membership_certificate_dispatched_list.filter(
            Q(company__company_name__icontains=searchTxt) |
            Q(member_associate_no__icontains=searchTxt))

        total_records = membership_certificate_dispatched_list.count()
        if length != -1:
            membership_certificate_dispatched_list = membership_certificate_dispatched_list[start:length]
        else:
            membership_certificate_dispatched_list = membership_certificate_dispatched_list[::-1]
        total_record = total_records

        i = 1
        for item in membership_certificate_dispatched_list:
            temp_list = []
            temp_list.append(i)
            temp_list.append(item.membership_year)
            temp_list.append(str(item.member_associate_no) if item.member_associate_no else '')
            temp_list.append(item.company.company_name if item.company else '')
            temp_list.append(item.ceo_email)
            temp_list.append(item.ceo_cellno)

            member_type = 'membership_ceritificate_dispatch'
            status = str(item.membership_ceritificate_dispatch)
            action = '<a class="icon-paper-plane" data-toggle="modal" data-target=#active_deactive_mem_cert_dispatch onclick=update_member(' + '"' + str(
                member_type) + '"' + ',' + str(item.id) + ',' + '"' + str(status) + '"' + ')></a>&nbsp;&nbsp;'
            download_action = '<a class="icon-cloud-download" title="Download" onclick=download_membership_certificate(' + str(
                item.id) + ')></a>'

            if item.membership_ceritificate_dispatch is True:
                temp_list.append('<label class="label label-success">Yes</label>')
                temp_list.append('&nbsp;&nbsp;' + download_action)
            else:
                temp_list.append('<label class="label label-default">No</label>')
                temp_list.append(action + download_action)

            dataList.append(temp_list)
            i = i + 1

        data = {'iTotalRecords': total_record, 'iTotalDisplayRecords': total_record, 'aaData': dataList}
        print '\nResponse OUT | get_membership_certificate_table'
    except Exception, e:
        print '\nException | get_membership_certificate_table = ', str(traceback.print_exc())
    return HttpResponse(json.dumps(data), content_type='application/json')


# Update Status of Executive Committee , Exclude From Mail & Membership Certificate Dispatch User
@transaction.atomic
def update_member(request):
    data = {}
    sid = transaction.savepoint()
    try:
        # pdb.set_trace()
        member_type = request.GET.get('member_type')
        member_obj = UserDetail.objects.get(id=request.GET.get('userdetail_id'))

        if member_type == 'executive_committee_member':
            if member_obj.executive_committee_member is True:
                member_obj.executive_committee_member = False
            else:
                member_obj.executive_committee_member = True
        elif member_type == 'exclude_from_mail':
            if member_obj.exclude_from_mailing is True:
                member_obj.exclude_from_mailing = False
            else:
                member_obj.exclude_from_mailing = True
        elif member_type == 'membership_ceritificate_dispatch':
            if member_obj.membership_ceritificate_dispatch is True:
                member_obj.membership_ceritificate_dispatch = False
            else:
                member_obj.membership_ceritificate_dispatch = True
        elif member_type == 'valid_invalid_member':
            if member_obj.valid_invalid_member is True:
                member_obj.valid_invalid_member = False
            else:
                member_obj.valid_invalid_member = True

        member_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
    except Exception, e:
        print '\nException | update_member = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')


# Download Membership Certificate Dispatch
def download_membership_certificate(request):
    try:
        membership_certificate_dispatched_obj = UserDetail.objects.get(id=request.GET.get('mem_cert_dispatch_id'))
        data = {'success': 'true'}
        template = get_template('backoffice/membership/membership_certificate.html')
        html = template.render(data)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
        if not pdf.err:
            print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
            return HttpResponse(result.getvalue(), content_type="application/pdf")
        else:
            print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
            return HttpResponse('We are sorry for inconvenience. We will get this back soon.')
    except Exception, e:
        print '\nException | download_membership_certificate = ', str(traceback.print_exc())


def download_event_reciept(request):
    try:

        print request.GET.get('event_reg_id')

        data = {'success': 'true'}
        template = get_template('backoffice/events/event_reciept.html')
        html = template.render(data)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
        if not pdf.err:
            print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
            return HttpResponse(result.getvalue(), content_type="application/pdf")
        else:
            print '\nResponse OUT | nsc_payment.py | download_payment_receipt | User = ', request.user
            return HttpResponse('We are sorry for inconvenience. We will get this back soon.')
    except Exception, e:
        print '\nException | download_membership_certificate = ', str(traceback.print_exc())


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Category'],login_url='/backofficeapp/login/',raise_exception=True)
def download_payment_file(request):
    try:
        print '\nRequest IN | membership_home.py | download_payment_file | User = ', request.user

        if request.GET.get('payment_from') and request.GET.get('payment_to'):
            payment_from_date = datetime.strptime(str(request.GET.get('payment_from')), '%d/%m/%Y').date()
            payment_to_date = (datetime.strptime(str(request.GET.get('payment_to')), '%d/%m/%Y') + timedelta(days=1)).date()
            if request.GET.get('select_type') == 'all':
                payment_list = PaymentDetails.objects.filter(payment_date__range=[payment_from_date, payment_to_date],
                                                             is_deleted=False, amount_paid__gt=0)
            elif request.GET.get('select_type') == 'new':
                payment_list = PaymentDetails.objects.filter(payment_date__range=[payment_from_date, payment_to_date],
                                                             membershipInvoice__invoice_for='NEW',is_deleted=False,
                                                             amount_paid__gt=0)
            else:
                payment_list = PaymentDetails.objects.filter(payment_date__range=[payment_from_date, payment_to_date],
                                                             membershipInvoice__invoice_for='RENEW',is_deleted=False,
                                                             amount_paid__gt=0)
        else:
            acceptance_from_date = datetime.strptime(str(request.GET.get('acceptance_from')), '%d/%m/%Y').date()
            acceptance_to_date = (datetime.strptime(str(request.GET.get('acceptance_to')), '%d/%m/%Y') + timedelta(days=1)).date()
            payment_list = PaymentDetails.objects.filter(userdetail__membership_acceptance_date=acceptance_from_date,
                                                         is_deleted=False, amount_paid__gt=0)

        print '\n\nLen = ', payment_list.count()        
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Payment_Detail')

        column_name = ['Payment Date','Membership No','Company Name', 'CEO Name', 'CEO Contact', 'Other Contact', 'Address', 'City',
                       'Pin Code', 'GSTIN', 'Year', 'New/Renew', 'Category', 'Total Payable', 'Amount', 'Entrance Fee', 'GST Amount',
                       'Total Paid', 'Payment Mode', 'Cheque No', 'Cheque Date', 'Bank Name']

        for i in range(21):
            worksheet1.write_string(0, int(i), column_name[i])

        i = 1
        for payment_obj in payment_list:
            worksheet1.write_string(i, 0, str(payment_obj.payment_date.strftime('%d/%m/%Y')))
            worksheet1.write_string(i, 1, str(payment_obj.userdetail.member_associate_no if payment_obj.userdetail.member_associate_no else ''))
            worksheet1.write_string(i, 2, str(payment_obj.userdetail.company.company_name))
            worksheet1.write_string(i, 3, str(payment_obj.userdetail.ceo_name))
            worksheet1.write_string(i, 4, str(payment_obj.userdetail.ceo_cellno if payment_obj.userdetail.ceo_cellno else ''))
            worksheet1.write_string(i, 5, str(payment_obj.userdetail.correspond_std1 if payment_obj.userdetail.correspond_std1 else '') + ' ' + str(payment_obj.userdetail.correspond_landline1 if payment_obj.userdetail.correspond_landline1 else ''))
            worksheet1.write_string(i, 6, str(payment_obj.userdetail.correspond_address))
            worksheet1.write_string(i, 7, str(payment_obj.userdetail.correspondcity.city_name if payment_obj.userdetail.correspondcity else ''))
            worksheet1.write_string(i, 8, payment_obj.userdetail.correspond_pincode if payment_obj.userdetail.correspond_pincode else '')
            worksheet1.write_string(i, 9, str(payment_obj.userdetail.gst if payment_obj.userdetail.gst else 'NA'))
            worksheet1.write_string(i, 10, str(payment_obj.financial_year))
            worksheet1.write_string(i, 11, str(payment_obj.membershipInvoice.invoice_for))
            worksheet1.write(i, 12, payment_obj.membershipInvoice.membership_slab.annual_fee)
            worksheet1.write(i, 13, payment_obj.amount_payable)
            without_gst_amount = payment_obj.amount_paid * 100 / 118
            gst_amount = payment_obj.amount_paid - without_gst_amount

            worksheet1.write(i, 14, round(payment_obj.membershipInvoice.subscription_charges, 0))
            worksheet1.write(i, 15, round(payment_obj.membershipInvoice.entrance_fees, 0))
            worksheet1.write(i, 16, round(gst_amount,0))
            worksheet1.write(i, 17, round(payment_obj.amount_paid,0))
            if payment_obj.user_Payment_Type == 'Cash':
                worksheet1.write_string(i, 18, 'Cash')
            elif payment_obj.cheque_no:
                worksheet1.write_string(i, 18, 'Cheque')
            elif payment_obj.user_Payment_Type == 'Online':
                worksheet1.write_string(i, 18, 'Online')
            else:
                worksheet1.write_string(i, 18, 'NEFT')
            if str(payment_obj.user_Payment_Type) == 'Cheque':
                worksheet1.write_string(i, 19, str(payment_obj.cheque_no if payment_obj.cheque_no else ''))
                worksheet1.write_string(i, 20, str(payment_obj.cheque_date.strftime('%d/%m/%Y') if payment_obj.cheque_date else ''))
                worksheet1.write_string(i, 21, str(payment_obj.bank_name if payment_obj.bank_name else ''))
            elif str(payment_obj.user_Payment_Type) == 'NEFT':
                worksheet1.write_string(i, 19, str(payment_obj.neft_transfer_id if payment_obj.neft_transfer_id else ''))
            else:
                worksheet1.write_string(i, 19, '')
                worksheet1.write_string(i, 20, '')
                worksheet1.write_string(i, 21, '')

            i = i + 1

        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Payment_Data.xlsx'
        print '\nResponse OUT | membership_home.py | download_payment_file | User = ', request.user
        return response
    except Exception,e:
        print '\nException IN | membership_home.py | download_payment_file | EXCP = ', str(traceback.print_exc())
        return False


@login_required(login_url='/backofficeapp/login/')
@role_required(privileges=['Membership Category'],login_url='/backofficeapp/login/',raise_exception=True)
def download_all_member_data(request):
    try:
        print '\nRequest IN | membership_home.py | download_all_member_data | User = ', request.user
        all_member_list = UserDetail.objects.all()
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet1 = workbook.add_worksheet('Payment_Detail')

        column_name = ['Sr #', 'Membership No', 'Company Name', 'CEO Name', 'CEO Contact', 'Correspondence Address',
                       'Correspondence City', 'Pin Code', 'Factory Address', 'Factory City', 'GSTIN', 'Scale','TO','Financial Year',
                       'Payment Method', 'Payment For Year', 'Total Payable', 'Total Paid', 'Payment Date',
                       'Payment Mode', 'Cheque No', 'Cheque Date', 'Bank Name']

        for i in range(len(column_name)):
            worksheet1.write_string(0, int(i), column_name[i])

        i = 1
        for user_obj in all_member_list:
            payment_list = PaymentDetails.objects.filter(userdetail=user_obj, is_deleted=False)
            if payment_list:
                for payment_obj in payment_list:
                    worksheet1.write_string(i, 0, str(i))
                    worksheet1.write_string(i, 1, str(user_obj.member_associate_no if user_obj.member_associate_no else ''))
                    worksheet1.write_string(i, 2, str(user_obj.company.company_name))
                    worksheet1.write_string(i, 3, str(user_obj.ceo_name))
                    worksheet1.write_string(i, 4, str(user_obj.ceo_cellno))
                    worksheet1.write_string(i, 5, str(user_obj.correspond_address))
                    worksheet1.write_string(i, 6, str(user_obj.correspondcity.city_name if user_obj.correspondcity else ''))
                    worksheet1.write_string(i, 7, user_obj.correspond_pincode if user_obj.correspond_pincode else '')
                    worksheet1.write_string(i, 8, str(user_obj.factory_address) if user_obj.factory_address else '')
                    worksheet1.write_string(i, 9, str(user_obj.factorycity.city_name if user_obj.factorycity else ''))
                    worksheet1.write_string(i, 10, str(user_obj.gst if user_obj.gst else 'NA'))
                    worksheet1.write_string(i, 11, str(user_obj.company.get_company_scale_display()))
                    worksheet1.write_string(i, 12, str(user_obj.annual_turnover_rupees if user_obj.annual_turnover_rupees else ''))
                    worksheet1.write_string(i, 13, str(user_obj.membership_year))
                    worksheet1.write_string(i, 14, str(user_obj.payment_method))
                    worksheet1.write_string(i, 15, str(payment_obj.financial_year))
                    worksheet1.write(i, 16, payment_obj.amount_payable)
                    worksheet1.write(i, 17, payment_obj.amount_paid)
                    worksheet1.write_string(i, 18, str(payment_obj.payment_date.strftime('%d/%m/%Y')) if payment_obj.payment_date else '')

                    if payment_obj.user_Payment_Type == 'Cash':
                        worksheet1.write_string(i, 19, 'Cash')
                    elif payment_obj.cheque_no:
                        worksheet1.write_string(i, 19, 'Cheque')
                    else:
                        worksheet1.write_string(i, 19, 'NEFT')
                    if str(payment_obj.user_Payment_Type) == 'Cheque':
                        worksheet1.write_string(i, 20, str(payment_obj.cheque_no if payment_obj.cheque_no else ''))
                        worksheet1.write_string(i, 21, str(
                            payment_obj.cheque_date.strftime('%d/%m/%Y') if payment_obj.cheque_date else ''))
                        worksheet1.write_string(i, 22, str(payment_obj.bank_name if payment_obj.bank_name else ''))
                    else:
                        worksheet1.write_string(i, 20, '')
                        worksheet1.write_string(i, 21, '')
                        worksheet1.write_string(i, 22, '')
            else:
                worksheet1.write_string(i, 0, str(i))
                worksheet1.write_string(i, 1, str(user_obj.member_associate_no if user_obj.member_associate_no else ''))
                worksheet1.write_string(i, 2, str(user_obj.company.company_name))
                worksheet1.write_string(i, 3, str(user_obj.ceo_name))
                worksheet1.write_string(i, 4, str(user_obj.ceo_cellno))
                worksheet1.write_string(i, 5, str(user_obj.correspond_address))
                worksheet1.write_string(i, 6, str(user_obj.correspondcity.city_name if user_obj.correspondcity else ''))
                worksheet1.write_string(i, 7, user_obj.correspond_pincode)
                worksheet1.write_string(i, 8, str(user_obj.factory_address) if user_obj.factory_address else '' )
                worksheet1.write_string(i, 9, str(user_obj.factorycity.city_name if user_obj.factorycity else ''))
                worksheet1.write_string(i, 10, str(user_obj.gst if user_obj.gst else 'NA'))
                worksheet1.write_string(i, 11, str(user_obj.company.get_company_scale_display()))
                worksheet1.write_string(i, 12, str(user_obj.annual_turnover_rupees if user_obj.annual_turnover_rupees else ''))
                worksheet1.write_string(i, 13, str(user_obj.membership_year))
                worksheet1.write_string(i, 14, str(user_obj.payment_method))
                worksheet1.write_string(i, 15, str(''))
                worksheet1.write_string(i, 16, str(''))
                worksheet1.write_string(i, 17, str(''))
                worksheet1.write_string(i, 18, str(''))
                worksheet1.write_string(i, 19, str(''))
                worksheet1.write_string(i, 20, str(''))
                worksheet1.write_string(i, 21, str(''))
                worksheet1.write_string(i, 22, str(''))

            i = i + 1

        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=Member_data.xlsx'
        print '\nResponse OUT | membership_home.py | download_all_member_data | User = ', request.user
        return response
    except Exception,e:
        print '\nException IN | membership_home.py | download_all_member_data | EXCP = ', str(traceback.print_exc())
        return False



def dashboard_screen(request):
    return render(request, 'backoffice/membership/dashboard.html')