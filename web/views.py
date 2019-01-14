from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    response = render(requset, 'login.html')
    return response

def register(request):
    response = render(request, 'register.html')
    return response
