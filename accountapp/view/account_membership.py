from django.shortcuts import render


def account(request):
    return render(request ,'account/account_membership_landing.html')


def download_account_label(request):
    return render(request, 'account/account_label.html')

    