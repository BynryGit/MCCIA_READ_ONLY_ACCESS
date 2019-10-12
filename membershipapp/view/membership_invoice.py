import traceback
import pdb
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from membershipapp.models import HOD_Detail, CompanyDetail,UserDetail,MembershipInvoice

from adminapp.models import MembershipCategory,MembershipSlab,Country,SlabCriteria, LegalStatus, State, City,IndustryDescription,MembershipDescription
from eventsapp.models import EventDetails

############### require for recaptcha ###########
import urllib
import urllib2
import json
from django.conf import settings
from django.contrib import messages


# Show Member Invoice Data
def member_invoice(request):
    data = {}
    try:
        print '\nRequest IN | membership_landing.py | member_invoice = ',request.GET.get('slab_id'),request.GET.get('quarter')

        category_obj = MembershipCategory.objects.get(id=request.GET.get('cat_id'))
        slab_obj = MembershipSlab.objects.get(id=request.GET.get('slab_id'))
        annual_fee = ''
        if category_obj.enroll_type == "Life Membership":
            annual_fee = float(slab_obj.annual_fee)
        else:
            if str(request.GET.get('quarter')) == '2018-2019/ full year':
                annual_fee = float(slab_obj.annual_fee)
            elif str(request.GET.get('quarter')) == '2018-2019/ half year':
                annual_fee = float(slab_obj.annual_fee) / 2
            elif str(request.GET.get('quarter')) == '2018-2019/ 3 quarters':
                annual_fee = float(slab_obj.annual_fee) / 3
            elif str(request.GET.get('quarter')) == '2018-2019/ Last Quarters':
                annual_fee = float(slab_obj.annual_fee) / 4

        tax_amount = (annual_fee + float(slab_obj.entrance_fee)) * 0.18
        amount_payable = float(annual_fee) + float(slab_obj.entrance_fee) + tax_amount

        data = {'membership_category': str(category_obj.membership_category),
                'slab_category': str(slab_obj.slab),
                'membership_year': str(request.GET.get('quarter')),
                'subscription_charges': float(annual_fee),
                'entrance_fee': str(slab_obj.entrance_fee),
                'tax_amount': tax_amount, 'amount_payable': amount_payable
                }
        print '\nResponse OUT | membership_landing.py | member_invoice = '
    except Exception,e:
        print '\nException | membership_landing.py | member_invoice = ',str(traceback.print_exc())
    return render(request, 'membership/membership-invoice.html', data)


# Save Membership Invoice Data
@csrf_exempt
@transaction.atomic
def save_member_invoice_detail(request):
    data = {}
    sid = transaction.savepoint()
    try:
        print '\nRequest IN | membership_landing.py | save_member_invoice_detail = '

        member_invoice_obj = MembershipInvoice(userdetail_id=str(request.POST.get('member_id')),
                                               subscription_charges=request.POST.get('subsciption_charges'),
                                               entrance_fees=request.POST.get('entrance_fees'),
                                               tax=request.POST.get('tax_amount'),
                                               amount_payable=request.POST.get('payable_amount'))
        member_invoice_obj.save()
        transaction.savepoint_commit(sid)
        data = {'success': 'true'}
        print '\nResponse OUT | membership_landing.py | save_member_invoice_detail = '
    except Exception,e:
        print '\nException | membership_landing.py | save_member_invoice_detail = ', str(traceback.print_exc())
        data = {'success': 'false'}
        transaction.rollback(sid)
    return HttpResponse(json.dumps(data), content_type='application/json')



