from django import template
#from django.template import Template

register = template.Library()

@register.filter
def check_list(list, elements):
    elements = elements.split(',')
    flag = 'no'
    for element in elements:
        if element in list:
            flag = 'yes'
    if flag == 'yes':
        return 'true'
    else:
        return 'false'

@register.filter
def check_login(list, elements):
    print list,elements
    print list.user.is_authenticated()
    if list.user.is_authenticated():
        print "true--------------------------",list
        return 'true'
    else:
        return 'false'

@register.filter
def check_previlege(list, elements):
    elements = elements.split(',')
    flag = 'no'
    for element in elements:
        if element in list:
            flag = 'yes'
    if flag == 'yes':
        return 'true'
    else:
        return 'false'
