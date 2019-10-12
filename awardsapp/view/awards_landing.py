
# System Packages

from django.shortcuts import render
import traceback
from django.http import HttpResponseServerError

# User Model

from awardsapp.models import AwardDetail, AwardFor
from adminapp.models import City


def awards_home(request):
    return render(request, 'awards/awards.html')


def awards_details(request):
    return render(request, 'awards/awards-details.html')


def awards_details1(request):
    return render(request, 'awards/awards-details1.html')


def awards_details2(request):
    return render(request, 'awards/awards-details2.html')


def awards_details3(request):
    return render(request, 'awards/awards-details3.html')


def awards_details4(request):
    return render(request, 'awards/awards-details4.html')


def awards_details5(request):
    return render(request, 'awards/awards-details5.html')


def awards_details6(request):
    return render(request, 'awards/awards-details6.html')



def awards_registration(request, award_id=None):
    try:
        print '\nRequest IN | awardsapp | awards_landing.py | awards_registration | User = ', request.user
        city_list = City.objects.filter(created_by='admin', is_active=True, is_deleted=False, state_id__isnull=False)
        award_detail_list = AwardDetail.objects.all()
        data = {
            'award_detail_list': award_detail_list,
            'city_list': city_list,
            'award_id': int(award_id) if award_id else None
        }
        print '\nResponse OUT | awardsapp | awards_landing.py | awards_registration | User = ', request.user
        return render(request, 'awards/awards_registration.html', data)
    except Exception, e:
        print '\nException IN | awardsapp | awards_landing.py | awards_registration | EXCP = ', str(traceback.print_exc())
        return HttpResponseServerError()


