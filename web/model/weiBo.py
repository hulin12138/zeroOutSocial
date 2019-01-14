from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

import time
import json
print("\n\n\n\n\nNew Compile =========================================================================================")


class Weibo():
    def __init__(self, gstore):
        self.gstore = gstore#TODO
        self.time_debug = False

    def write_weibo(self, weibo_mid, weibo_date, weibo_text, weibo_source, weibo_repostsnum,  weibo_commentnsum, weibo_attitudesnum, weibo_uid, weibo_topic):
        weibo_x = "<http://localhost:2020/weibo/"+weibo_mid+">"
        yzs = [
            ["weibo_mid", '"'+weibo_mid+'"'],
            ["weibo_date", '"'+weibo_date+'"'+"^^<http://www.w3.org/2001/XMLSchema#dateTime>"],
            ["weibo_text", weibo_text],
            ["weibo_source", '"'+weibo_source+'"'],
            ["weibo_repostsnum", '"'+weibo_repostsnum+'"'+"^^<http://www.w3.org/2001/XMLSchema#integer>"],
            ["weibo_commentnsum", '"'+weibo_commentnsum+'"'+"^^<http://www.w3.org/2001/XMLSchema#integer>"],
            ["weibo_attitudesnum", '"'+weibo_attitudesnum+'"'+"^^<http://www.w3.org/2001/XMLSchema#integer>"],
            ["weibo_uid", '"'+weibo_uid+'"'],
            ["weibo_topic", '"'+weibo_topic+'"']
        ]

        yzs = [ [weibo_x, "<file:///D:/d2rq-0.8.1/vocab/"+i+">",j+" ." ] for i,j in yzs ]
        yzs = [" ".join(i) for i in yzs]
        yzs = "\n".join(yzs)
        sparql_insert_weibo = "INSERT DATA { " + yzs + " }"
        #print(sparql_insert_weibo)
        res = self.gstore.query("weibo", sparql_insert_weibo)
        #print(res)
        #res = json.loads(res)
        #res_check = self.gstore.query("root", "123456", "weibo", "select ?y ?z where { <file:///D:/d2rq-0.8.1/weibo.nt#weibo/123344> ?y ?z . }")
        if res["StatusCode"] == 402:
            return True, None
        else:
            return False, res["StatusMsg"]

    def delete_weibo(self, request):
        if "weibo_mid" in request.GET:
            weibo_mid = request.GET["weibo_mid"]
        else:
            return HttpResponse('{"status":"error"}')
        if "uid" in request.session:
            user_uid = request.session.get("uid")
            sparql_check_user = 'select ?y where {{ <file:///D:/d2rq-0.8.1/weibo.nt#weibo/{}> <file:///D:/d2rq-0.8.1/vocab/weibo_uid> ?y. }}'.format(weibo_mid)
            res = self.gstore.query("weibo", sparql_check_user)
            res = res["results"]["bindings"][0]["y"]["value"]
            if not res==user_uid:
                return HttpResponse('{"status":"permission denied"}')
        else:
            return HttpResponse('{"status":"notlogin"}')

        #print("===================================")
        sparql = "delete {{ <file:///D:/d2rq-0.8.1/weibo.nt#weibo/{}> ?y ?z }} where {{  <file:///D:/d2rq-0.8.1/weibo.nt#weibo/{}> ?y ?z. }}".format(weibo_mid, weibo_mid)
        #sparql_check = "select ?y ?z where {{  <file:///D:/d2rq-0.8.1/weibo.nt#weibo/{}> ?y ?z. }}".format(weibo_mid)
        #print(sparql)
        res = self.gstore.query("weibo", sparql)
        #res_check = self.gstore.query("weibo", sparql_check)
        #print(res)
        #print(res_check)
        return HttpResponse('{"status":"success"}')



    def get_user_name(self, user_id):
        query_str = 'select ?z where {{ <file:///D:/d2rq-0.8.1/weibo.nt#user/{}>  <file:///D:/d2rq-0.8.1/vocab/user_screen_name> ?z .}}'.format(user_id)
        res = self.gstore.query("weibo", query_str)
        #res = json.loads(res)
        if len(res["results"]["bindings"])==0:
            return "UNK" 
        res = res["results"]["bindings"][0]["z"]["value"]
        return res

    def get_user_weibo(self, weibo_uid):
        #if self.time_debug: time_start = time.time()
        #user_name = self.get_user_name(weibo_uid)
        #if self.time_debug: print("Get user name:", time.time()-time_start)
        
        query_str = 'select ?x ?y ?z where {{ ?x <file:///D:/d2rq-0.8.1/vocab/weibo_uid> "{}" . ?x ?y ?z . }}'.format(weibo_uid)
        if self.time_debug: time_start = time.time()
        res = self.gstore.query("weibo", query_str)
        if self.time_debug: print("User query:", time.time()-time_start)
        #res = json.loads(res)
        res = res["results"]["bindings"]
        weibo_mids = [[i["x"]["value"], i["y"]["value"], i["z"]["value"] ] for i in res]
        #print(weibo_mids)
        weibo_group = dict()
        for i,j,k in weibo_mids:
            if i in weibo_group:
                weibo_group[i].append([j,k])
            else:
                weibo_group[i]= [[j,k]]
        weibo_all = []
        for weibo_mid_per, weibo_cons in weibo_group.items():
            weibo_per = dict()
            #weibo_per["weibo_uid_name"] = user_name
            for weibo_y, weibo_z in weibo_cons:
                if weibo_y.startswith("file:///D:/d2rq-0.8.1/vocab"):
                    weibo_y = weibo_y[28:]
                    weibo_per[weibo_y] = weibo_z
            weibo_all.append(weibo_per)
        weibo_all = sorted(weibo_all, key=lambda v:v["weibo_date"], reverse=True)
        return weibo_all
        
        # the following is discard version
        query_str = 'select ?x where {{ ?x <file:///D:/d2rq-0.8.1/vocab/weibo_uid> "{}" . }}'.format(weibo_uid)
        res = self.gstore.query("weibo", query_str)
        weibo_mids = [i["x"]["value"] for i in res["results"]["bindings"]]
        weibo_all = []
        for weibo_mid_per in weibo_mids:
            weibo_per = dict()
            query_str = 'select ?y ?z where {{ <{}> ?y ?z . }}'.format(weibo_mid_per)
            res = self.gstore.query("weibo", query_str)
            res = res["results"]["bindings"]
            for res_per in res:
                y = res_per["y"]["value"]
                z = res_per["z"]["value"]
                if y.startswith("file:///D:/d2rq-0.8.1/vocab"):
                    y = y[28:]
                    weibo_per[y] = z
            weibo_all.append(weibo_per)
        weibo_all = sorted(weibo_all, key=lambda v:v["weibo_date"], reverse=True)
        return weibo_all

    def send_weibo(self, request):
        if "uid"  not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        #print("Gookie got", request.session.get("user"))
        user_id = request.session.get("uid")
        weibo_text = request.POST["weibo_text"]
        weibo_topic = request.POST["weibo_topic"]
        weibo_uid = user_id
        weibo_mid = str(time.time())
        weibo_source = "UNK"
        weibo_date = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        weibo_commentnsum, weibo_repostsnum, weibo_attitudesnum = "0", "0", "0"
        status, error_info = self.write_weibo(weibo_mid, weibo_date, weibo_text, weibo_source, weibo_repostsnum,  weibo_commentnsum, weibo_attitudesnum, weibo_uid, weibo_topic)
        if status:
            return HttpResponse("success")
        else:
            return HttpResponse(error_info)


    def get_my_weibo(self, request):
        #print("Come to get my weibo")
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            print("uid not found")
            return response
        #print("Gookie got", request.session.get("user"))
        user_id = request.session.get("uid")
        if "user_id" in request.GET:
            user_id = request.GET["user_id"]
        start_point = 0
        if "start" in request.GET:
            start_point = int(request.GET["start"])
        user_weibos = self.get_user_weibo(user_id)
        my_name = self.get_user_name(user_id)
        for user_weibo_per in user_weibos:
            user_weibo_per["weibo_uid_name"] = my_name
        user_weibos = sorted(user_weibos, key=lambda v:v["weibo_date"], reverse=True)[start_point:start_point+10]
        user_weibos = json.dumps(user_weibos)
        #print(user_weibos)
        return HttpResponse(user_weibos)

    def get_my_follow_user(self, user_id):
        query_str = 'select ?x where {{ ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> "{}" }} .'.format(user_id)
        #print(query_str)
        res = self.gstore.query("weibo", query_str)
        #print("--------------------------",res)
        #res = json.loads(res)
        res = res["results"]["bindings"]
        res = [i["x"]["value"] for i in res]
        res = [i[i.find(user_id)+len(user_id)+1:] for i in res]
        return res

    def get_my_follow_weibo_old(self, request):
        if self.time_debug: print("Start get_my_follow_weibo", time.asctime( time.localtime(time.time()) ))
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            return response
        print("Gookie got", request.session.get("uid"))
        user_id = request.session.get("uid")
        my_follow_uids = self.get_my_follow_user(user_id)
        my_follow_uids.append(user_id)
        weibo_all = []
        for my_follow_uid_per in my_follow_uids:
            #if self.time_debug: print("End get_user_weibo", time.asctime( time.localtime(time.time()) ))
            weibo_per = self.get_user_weibo(my_follow_uid_per)
            weibo_all.extend(weibo_per)
        weibo_all = sorted(weibo_all, key=lambda v:v["weibo_date"], reverse=True)[:10]
        for i in range(len(weibo_all)):
            #print(weibo_all[i])
            weibo_all[i]["weibo_uid_name"] = self.get_user_name(weibo_all[i]["weibo_uid"])
        tt = [i["weibo_text"] for i in weibo_all]
        #for i in tt:
        #    print(i)
        weibo_all = json.dumps(weibo_all)
        if self.time_debug: print("End   get_my_follow_weibo", time.asctime( time.localtime(time.time()) ))
        return HttpResponse(weibo_all)

    def get_my_follow_weibo(self, request):
        if self.time_debug: print("Start get_my_follow_weibo", time.asctime( time.localtime(time.time()) ))
        if "uid" not in request.session:
            response = HttpResponseRedirect(reverse('myapp:index'))
            print("User not in sesstion")
            return response
        start_point = request.GET["start"]
        start_point = int(start_point)
        print("Gookie got", request.session.get("uid"))
        user_id = request.session.get("uid")
        weibo_all = self.get_user_follow_weibo(user_id)
        weibo_all_my = self.get_user_weibo(user_id)
        my_screen_name = self.get_user_name(user_id)
        for i in range(len(weibo_all_my)):
            weibo_all_my[i]["weibo_uid_name"] = my_screen_name
        weibo_all = weibo_all+weibo_all_my

        """
        my_follow_uids = self.get_my_follow_user(user_id)
        my_follow_uids.append(user_id)
        weibo_all = []
        for my_follow_uid_per in my_follow_uids:
            #if self.time_debug: print("End get_user_weibo", time.asctime( time.localtime(time.time()) ))
            weibo_per = self.get_user_weibo(my_follow_uid_per)
            weibo_all.extend(weibo_per)
        """
        weibo_all = sorted(weibo_all, key=lambda v:v["weibo_date"], reverse=True)[start_point:start_point+10]
        #for i in range(len(weibo_all)):
            #print(weibo_all[i])
        #    weibo_all[i]["weibo_uid_name"] = self.get_user_name(weibo_all[i]["weibo_uid"])
        tt = [i["weibo_text"] for i in weibo_all]
        #for i in tt:
        #    print(i)
        weibo_all = json.dumps(weibo_all)
        if self.time_debug: print("End   get_my_follow_weibo", time.asctime( time.localtime(time.time()) ))
        return HttpResponse(weibo_all)

    #write_weibo("123344", "2014-04-30T15:53:35", "hhh", "UNK", "0", "0", "0", "123456", "hh")
    #get_user_weibo("123456")
    #get_user_weibo("1749705962")

    def get_user_follow_weibo(self, user_id):
        sql = """select ?user ?user_name ?weibo ?weibo_relation ?weibo_z where {{
            ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_suid> "{}".
            ?x <file:///D:/d2rq-0.8.1/vocab/userrelation_tuid> ?user.
            ?user_rep <file:///D:/d2rq-0.8.1/vocab/user_uid> ?user.
            ?user_rep <file:///D:/d2rq-0.8.1/vocab/user_screen_name> ?user_name.
            ?weibo <file:///D:/d2rq-0.8.1/vocab/weibo_uid> ?user.
            ?weibo ?weibo_relation ?weibo_z.
        }}
        """.format(user_id)
        res = self.gstore.query("weibo", sql)
        if False:
            for i in res["results"]["bindings"]:
                print("user ",i["user"],"\nweibo ",i["weibo"], "\nweibo_relation", i["weibo_relation"], "\nweibo_z",i["weibo_z"])
        res = res["results"]["bindings"]

        weibo_all = dict()
        for weibo_tmp in res:
            weibo_rdf_id = weibo_tmp["weibo"]["value"]
            if weibo_rdf_id in weibo_all:
                weibo_relation = weibo_tmp["weibo_relation"]["value"]
                weibo_z = weibo_tmp["weibo_z"]["value"]
                if weibo_relation.startswith("file:///D:/d2rq-0.8.1/vocab"):
                    weibo_relation = weibo_relation[28:]
                if weibo_relation.startswith("http://www.w3.org"):
                    continue
                weibo_all[weibo_rdf_id][weibo_relation]=weibo_z
            else:
                weibo_all[weibo_rdf_id] = {"weibo_uid":weibo_tmp["user"]["value"], "weibo_uid_name":weibo_tmp["user_name"]["value"]} # "weibo_uid_name":weibo_tmp["user_name"]
        weibo_all = [i[1] for i in weibo_all.items()]
        return weibo_all

