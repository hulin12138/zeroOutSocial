from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

import time
import json
from . import GstoreConnector

print("\n\n\n\n\nNew Compile =========================================================================================")

class User_Info():
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

class User():
    def __init__(self, gstore):
        self.gstore = gstore#TODO

    def get_user_name(self, user_id):
        query_str = "select ?x where{ <file:///D:/d2rq-0.8.1/weibo.nt#user/" + user_id + "> <file:///D:/d2rq-0.8.1/vocab/user_screen_name> ?x.}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"][0]["x"]["value"]
        return res

    def get_location(self, user_id):
        query_str = "select ?x where{ <file:///D:/d2rq-0.8.1/weibo.nt#user/" + user_id + "> <file:///D:/d2rq-0.8.1/vocab/user_location> ?x.}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"][0]["x"]["value"]
        return res
		
    def get_gender(self, user_id):
        query_str = "select ?x where{ <file:///D:/d2rq-0.8.1/weibo.nt#user/" + user_id + "> <file:///D:/d2rq-0.8.1/vocab/user_gender> ?x.}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"][0]["x"]["value"]
        return res
		
    def get_weibo_num(self, user_id):
        query_str = "select ?x where{ ?x <file:///D:/d2rq-0.8.1/vocab/weibo_uid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        print(res)
        return len(res)
		
    def get_follow_num(self, user_id):
        query_str = "select ?x where{ ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        return len(res)
		
    def get_fan_num(self, user_id):
        query_str = "select ?x where{ ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_tuid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        return len(res)

    def get_my_home(self, request):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        name = self.get_user_name(user_id)
        weibo_num = self.get_weibo_num(user_id)	
        follow_num = self.get_follow_num(user_id)	
        fan_num = self.get_fan_num(user_id)	
        context = {'uid': user_id, 'name': name, 'weibo_num': weibo_num, 'follow_num': follow_num, 'fan_num': fan_num}
        return render(request, 'user/my.html', context)
	
    def get_user_home(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        st = "<file:///D:/d2rq-0.8.1/weibo.nt#userrelation/" + user_id + "/" + uid + ">"
        query_str = "select * where{ " + st + " <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> \"" + user_id + "\".}"
        res = self.gstore.query("weibo", query_str)
        res = res["results"]["bindings"]
        name = self.get_user_name(uid)
        location = self.get_location(uid)
        gender = self.get_gender(uid)		
        weibo_num = self.get_weibo_num(uid)	
        follow_num = self.get_follow_num(uid)	
        fan_num = self.get_fan_num(uid)	
        flag = len(res)
        context = {'uid': uid, 'name': name, 'location': location, 'gender': gender, 'weibo_num': weibo_num, 'follow_num': follow_num, 'fan_num': fan_num, 'flag': flag}
        return render(request, 'user/user.html', context)	
		
    def get_my_follow_user(self, request):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> \"" + user_id + "\".}"
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
        return render(request, 'user/my_follow.html', context)
		
    def get_follow_user(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> \"" + uid + "\".}"
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
        return render(request, 'user/follow.html', context)	

    def delete_follow_user(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        st = "<file:///D:/d2rq-0.8.1/weibo.nt#userrelation/" + user_id + "/" + uid + ">"
        query_str = "delete data{ " + st + " <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> \"" + user_id + "\"." + st + " <file:///D:/d2rq-0.8.1/vocab/userrelation_tuid> \"" + uid + "\".}"
        res = self.gstore.query("weibo", query_str)
        return self.get_my_follow_user(request)
		
    def add_follow_user(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        st = "<file:///D:/d2rq-0.8.1/weibo.nt#userrelation/" + user_id + "/" + uid + ">"
        query_str = "insert data{ " + st + " <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> \"" + user_id + "\"." + st + " <file:///D:/d2rq-0.8.1/vocab/userrelation_tuid> \"" + uid + "\".}"
        res = self.gstore.query("weibo", query_str)
        return self.get_user_home(request, uid)
		
    def get_my_fan(self, request):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_tuid> \"" + user_id + "\".}"
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
        return render(request, 'user/my_fan.html', context)
		
    def get_fan(self, request, uid):
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        user_id = request.session.get("uid")
        query_str = "select ?x where{ ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_tuid> \"" + uid + "\".}"
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
        return render(request, 'user/fan.html', context)	
