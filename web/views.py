from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
import sys
sys.path.append('./web/model')
sys.path.append('./web')
from GstoreConnector import GstoreConnector
from weiBo import Weibo
from followRelation import User

gstore = GstoreConnector("localhost", 9000, "root", "123456")
weibo = Weibo(gstore)
user = User(gstore)

def index(request):
    response = render(request, 'login.html')
    return response

def register(request):
    response = render(request, 'register.html')
    return response

def about(request):
    response = render(request, 'about.html')
    return response

def get_my_follow_user(request):
    return user.get_my_follow_user(request)

def delete_follow_user(request):
    uid = request.POST['followuid']
    return user.delete_follow_user(request, uid)

def get_my_fan(request):
    return user.get_my_fan(request)

def delete_fan(request):
    uid = request.POST['fanuid']
    return user.delete_fan(request,uid)

def get_my_weibo(request):
    return weibo.get_my_weibo(request)

def get_my_follow_weibo(request):
    return weibo.get_my_follow_weibo(request)

def enter_change_passwd(request):
	return render(request, 'changePwd.html')
