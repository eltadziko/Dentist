# -*- coding: utf-8 -*-
from django import template
from django.utils.encoding import force_unicode
import calendar, locale

register = template.Library()

@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg) + 1

@register.filter
def mul(value, arg):
    "Divides the value by the arg"
    return int(value) * int(arg)

@register.filter
def add(value, arg):
    "Divides the value by the arg"
    return int(value) + int(arg)

@register.filter
def in_group(user, groups):
    """Returns a boolean if the user is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if user|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    if user.is_authenticated():
        group_list = force_unicode(groups).split(',')
        return bool(user.groups.filter(name__in=group_list).values('name'))
    else:
        return False
    
@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter
def day(int):
    return {
        1: 'pon',
        2: 'wt',
        3: 'śr',
        4: 'czw',
        5: 'pt',
        6: 'so',
        7: 'nd'
    }[int]
    
@register.filter
def is_false(arg): 
    return arg is False

@register.filter
def month_name(month_number):
    return {
        1: 'styczeń',
        2: 'luty',
        3: 'marzec',
        4: 'kwiecień',
        5: 'maj',
        6: 'czerwiec',
        7: 'lipiec',
        8: 'sierpień',
        9: 'wrzesień',
        10: 'październik',
        11: 'listopad',
        12: 'grudzień'
    }[month_number]