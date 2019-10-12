from django.shortcuts import render

# Create your views here.
def technology_transfer(request):
    return render(request, 'initiatives/technology-transfer.html')


def mfg_lean_transfer(request):
    return render(request, 'initiatives/mfg-lean-transfer.html')


def electronic_clusture(request):
    return render(request, 'initiatives/electronic-clusture.html')


def apprenticeship(request):
    return render(request, 'initiatives/apprenticeship.html')


def enterpreneurship(request):
    return render(request, 'initiatives/enterpreneurship.html')


def contact_us(request):
    return render(request, 'contact-us.html')


def media(request):
    return render(request, 'media.html')