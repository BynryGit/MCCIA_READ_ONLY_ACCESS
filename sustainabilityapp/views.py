from django.shortcuts import render


# Create your views here.


def sustainability_desk(request):
    return render(request, 'services/sustainability_desk.html')

def sustainability_tab(request):
    return render(request, 'services/sustainability_tab.html')