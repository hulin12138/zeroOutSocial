from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

import time
import json
import sys
sys.path.append('..')
from GstoreConnector import GstoreConnector

predicatePrefix = 'http://localhost:2020/vocab/'
userPrefix = 'http://localhost:2020/user/'

print("\n\n\n\n\nNew Compile =========================================================================================")

class User_Info():
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

class User():
    def __init__(self, gstore):
        self.gstore = gstore#TODO

    def get_user_name(self, user_id):
        query_str = "select ?x where{ <" + userPrefix + user_id + "> <" + predicatePrefix + "user_screen_name> ?x.}"
        print('*' * 60)
        print(query_str)
        print('*' * 60)
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"][0]["x"]["value"]
        print(res)
        return res

    def get_location(self, user_id):
        query_str = "select ?x where{ <" + userPrefix + user_id + "> <" + predicatePrefix + "user_location> ?x.}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"][0]["x"]["value"]
        return res
		
    def get_gender(self, user_id):
        query_str = "select ?x where{ <" + userPrefix + user_id + "> <" + predicatePrefix + "user_gender> ?x.}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"][0]["x"]["value"]
        return res
		
    def get_weibo_num(self, user_id):
        query_str = "select ?x where{ ?x <" + predicatePrefix + "weibo_uid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        print(res)
        return len(res)
		
    def get_follow_num(self, user_id):
        query_str = "select ?x where{ ?x <" + predicatePrefix + "userrelation_suid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        return len(res)
		
    def get_fan_num(self, user_id):
        query_str = "select ?x where{ ?x <" + predicatePrefix + "userrelation_tuid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        return len(res)

    def get_user_home(self, request,uid):
        name = self.get_user_name(uid)
        weibo_num = self.get_weibo_num(uid)	
        follow_num = self.get_follow_num(uid)	
        fan_num = self.get_fan_num(uid)	
        context = {'uid': user_id, 'name': name, 'weibo_num': weibo_num, 'follow_num': follow_num, 'fan_num': fan_num}
        return render(request, 'my.html', context)#TODO
		
    def get_my_follow_user(self, request):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('zeroOut:index'))#TODO
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <" + predicatePrefix + "userrelation_suid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        users = []
        for i in res:
            sub = i["x"]["value"]
            uid = sub[sub.find(user_id)+len(user_id)+1:]
            name = self.get_user_name(uid)
            user = User_Info(uid, name)
            users.append(user)
        context = {'follow_users': users}
        return render(request, 'follow.html', context)#TODO
		
    def get_follow_user(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('zeroOut:index'))
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <" + predicatePrefix + "userrelation_suid> \"" + uid + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        users = []
        for i in res:
            sub = i["x"]["value"]
            id = sub[sub.find(uid)+len(uid)+1:]
            name = self.get_user_name(id)
            user = User_Info(id, name)
            users.append(user)
        context = {'follow_users': users}
        return render(request, 'user/follow.html', context)#TODO

    def delete_follow_user(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('zeroOut:index'))#TODO
            return response
        user_id = request.session.get("uid")
        st = "<http://localhost:2020/userrelation/" + user_id + "/" + uid + ">"
        query_str = "delete data{ " + st + " <" + predicatePrefix + "userrelation_suid> \"" + user_id + "\"." + st + " <" + predicatePrefix + "userrelation_tuid> \"" + uid + "\".}"
        res = self.gstore.query("weibo", query_str)
        return self.get_my_follow_user(request)
		
    def add_follow_user(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('zeroOut:index'))#TODO
            return response
        user_id = request.session.get("uid")
        st = "<http://localhost:2020/userrelation/" + user_id + "/" + uid + ">"
        query_str = "insert data{ " + st + " <" + predicatePrefix + "userrelation_suid> \"" + user_id + "\"." + st + " <" + predicatePrefix + "userrelation_tuid> \"" + uid + "\".}"
        res = self.gstore.query("weibo", query_str)
        return self.get_user_home(request, uid)#TODO
		
    def get_my_fan(self, request):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('zeroOut:index'))#TODO
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <" + predicatePrefix + "userrelation_tuid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        users = []
        for i in res:
            sub = i["x"]["value"]
            loc = sub.find(user_id)
            uid = sub[loc-11:loc-1] 
            name = self.get_user_name(uid)
            user = User_Info(uid, name)
            users.append(user)
        context = {'fans': users}
        return render(request, 'fans.html', context)#

    def delete_fan(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('zeroOut:index'))#TODO
            return response
        user_id = request.session.get("uid")
        st = "<http://localhost:2020/userrelation/" + uid + "/" + user_id + ">"
        query_str = "delete data{ " + st + " <" + predicatePrefix + "userrelation_tuid> \"" + user_id + "\"." + st + " <" + predicatePrefix + "userrelation_suid> \"" + uid + "\".}"
        res = self.gstore.query("weibo",query_str)
        return self.get_my_fan(request)

    def get_fan(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('zeroOut:index'))#TODO
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <" + predicatePrefix +"userrelation_tuid> \"" + uid + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        users = []
        for i in res:
            sub = i["x"]["value"]
            loc = sub.find(uid)
            id = sub[loc-11:loc-1]
            name = self.get_user_name(id)
            user = User_Info(id, name)
            users.append(user)
        context = {'fans': users}
        return render(request, 'user/fan.html', context)#TODO
