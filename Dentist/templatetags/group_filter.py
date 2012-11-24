# -*- coding: utf-8 -*-
from django import template
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg) + 1

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