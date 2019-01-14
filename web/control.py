from django.shortcuts import render, redirect
from GstoreConnector import GstoreConnector
from django.http import HttpResponseNotFound
from django.urls import reverse
from hashlib import sha256
from datetime import datetime
from model.followRelation import User as follow_user#TODO
from model.userAccount import userAccount as account_user

prefix = "prefix wb: <http://localhost:2020/vocab/> "
gstore = GstoreConnector("localhost", 9000, 'root', '123456')

def login(request):
    try:
        name = request.POST['username']
        password = str(request.POST['password'])
    except KeyError:
        return HttpResponseNotFound("No username or password sent")
    else:
        sparql = '''{} select ?m where {{ ?x wb:user_name "{}". 
                    ?x wb:user_uid ?m .}}'''.format(prefix, name)
        result = gstore.query('weibo', sparql)['results']['bindings']
        print('get uid', result)
        if not result:
            return HttpResponseNotFound('User name or password is not correct!')

        uid = result[0]['m']['value']
        sparql = '''{} select ?m where {{ ?x wb:user_password ?m. 
                            ?x wb:user_uid "{}" .}}'''.format(prefix, uid)
        result = gstore.query('weibo', sparql)['results']['bindings']
        print('get password', result)
        if not result:
            if uid != password:
                return HttpResponseNotFound('User name or password is not correct!')
        else:
            true_passwd = result[0]['m']['value']
            if true_passwd != password:

                return HttpResponseNotFound('User name or password is not correct!')

        request.session['uid'] = uid
        #return redirect(reverse('myapp:profile'))
        return redirect(reverse('web:get_home'))#TODO
        # response.set_cookie("user", "1749705962")


def register(request):
    return render(request, 'web/register.html')#TODO


def check_register(request):
    name = request.POST['name']
    password = request.POST['password']
    print('check name: ', name)
    sparql = '''{} select ?m where {{ ?x wb:user_name "{}". 
                        ?x wb:user_uid ?m .}}'''.format(prefix, name)
    result = gstore.query('weibo', sparql)['results']['bindings']
    if len(result) > 0:
        print(result)
        return HttpResponseNotFound('User name already exist.')

    sha_hex = sha256(name.encode('utf-8')).hexdigest()
    uid = int(sha_hex, 16) % 10**10
    uid = str(uid)
    print('new uid: ', uid)

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = account_user(uid, name, request.POST['nick'], request.POST['city'],
                request.POST['sex'], date, password)
    user.save_to_db()
    request.session['uid'] = uid
    return redirect(reverse('web:profile'))#TODO

def profile(request):
    uid = request.session['uid']
    print(uid, request.session)

    user = account_user(uid)
    user.load_from_db()

    f_user = follow_user(gstore)
    weibo_num = f_user.get_weibo_num(uid)
    follow_num = f_user.get_follow_num(uid)
    fan_num = f_user.get_fan_num(uid)
    context = {'user': user, 'weibo_num': weibo_num, 'follow_num': follow_num, 'fan_num': fan_num}#TODO
    return render(request, 'web/profile.html', context)#TODO

def edit_profile(request):
    uid = request.session['uid']
    user = account_user(uid)
    user.load_from_db()
    context = {'user': user}
    return render(request, 'web/edit_profile.html', context)#TODO


def update_profile(request):
    uid = request.POST['uid']
    nickName = request.POST['nickName']
    password = request.POST['password']
    sex = request.POST['sex']
    city = request.POST['city']
    query = '''{} 
                delete {{ ?user wb:user_screen_name ?s }}
                insert {{ ?user wb:user_screen_name "{}" }}
                where {{ ?user wb:user_uid "{}" .
                        ?user wb:user_screen_name ?s}} 
                '''.format(prefix, nickName, uid)
    gstore.query('weibo', query)
    query = '''{} 
                    delete {{ ?user wb:user_password ?s }}
                    insert {{ ?user wb:user_password "{}" }}
                    where {{ ?user wb:user_uid "{}" .
                            ?user wb:user_password ?s}} 
                    '''.format(prefix, password, uid)
    gstore.query('weibo', query)
    query = '''{} 
            delete {{ ?user wb:user_gender ?g }}
            insert {{ ?user wb:user_gender "{}" }}
            where {{ ?user wb:user_uid "{}" .
                    ?user wb:user_gender ?g}} 
            '''.format(prefix, sex, uid)
    gstore.query('weibo', query)
    query = '''{} 
                delete {{ ?user wb:user_location ?l }}
                insert {{ ?user wb:user_location "{}" }}
                where {{ ?user wb:user_uid "{}" .
                        ?user wb:user_location ?l}} 
                '''.format(prefix, city, uid)
    response = gstore.query('weibo', query)
    print(response)
    request.session['uid'] = uid
    return redirect(reverse('web:profile'))#TODO
