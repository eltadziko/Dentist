# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect

def anonymous_required( view_function, redirect_to = None ):
    return AnonymousRequired( view_function, redirect_to )

class AnonymousRequired( object ):
    def __init__( self, view_function, redirect_to ):
        if redirect_to is None:
            redirect_to = '/access_denied/'
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__( self, request, *args, **kwargs ):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect( self.redirect_to ) 
        return self.view_function( request, *args, **kwargs )

def in_patient_group(user):
    if user:
        return user.groups.filter(name='pacjent').count() == 1
    return False

def in_receptionist_group(user):
    if user:
        return user.groups.filter(name='rejestrator').count() == 1
    return False

def in_group(user):
    if user:
        return user.groups.filter(name='rejestrator').count() == 1 or user.groups.filter(name='pacjent').count() == 1
    return False
