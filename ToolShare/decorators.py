from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import get_model
"""
This is a decorator
It wrapps any function that you decorate with the @loggedin 
This checks to see if the user in the request is logged in and either call the function or returns them to the home page
DOnt want to explain how decorators work so if you wana know look it up
"""
def loggedin(func,*args,**kwargs):
    def view(request,*args,**kwargs):
        if request.user.is_authenticated():
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/user/login/')
    return view
