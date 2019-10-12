from django.shortcuts import render

# Create your views here.

def agriculture(request):
    return render(request, 'committee/agriculture.html')


def defence(request):
    return render(request, 'committee/defence.html')


def electronics(request):
    return render(request, 'committee/electronics.html')

def food_processing(request):
    return render(request, 'committee/food-processing.html')


def infrastructure(request):
    return render(request, 'committee/infrastructure.html')


def sme(request):
    return render(request, 'committee/sme.html')


def women_entrepreneurs(request):
    return render(request, 'committee/women-entrepreneurs.html')


def IT_ITES(request):
    return render(request, 'committee/IT-ITES.html')


def hr_ir(request):
    return render(request, 'committee/hr-ir.html')


def energy(request):
    return render(request, 'committee/energy.html')


def education_skill_development(request):
    return render(request, 'committee/education-skill-development.html')


def civil_aviation(request):
    return render(request, 'committee/civil-aviation.html')


def ahmednagar(request):
    return render(request, 'committee/ahmednagar.html')


def corporate_legislation(request):
    return render(request, 'committee/corporate_legislation.html')


def foreign_trade(request):
    return render(request, 'committee/foreign_trade.html')


def higher_education_skill_development(request):
    return render(request, 'committee/higher_education_skill_development.html')


def innovation_incubation(request):
    return render(request, 'committee/innovation_incubation.html')


def taxation(request):
    return render(request, 'committee/taxation.html')