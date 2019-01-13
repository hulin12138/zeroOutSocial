from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

def login(request):
    response = render(request, 'web/login.html')
    return response
