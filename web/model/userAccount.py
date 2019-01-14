#from django.shortcuts import render, redirect
import sys
sys.path.append('..')
from GstoreConnector import GstoreConnector
#from django.http import HttpResponseNotFound
#from django.urls import reverse
#from hashlib import sha256
#from datetime import datetime
#from .followRelation import User as follow_user

gstore = GstoreConnector("localhost", 9000, "root", "123456")
#gstore = GstoreConnector("162.105.88.93", 9000, "root", "123456")

class userAccount:
    def __init__ (self,uid,name='',nickName='',sex='',city='',creaDate='',password=''):
        self.name = name
        self.nickName = nickName
        self.sex = sex
        self.city = city
        self.creaDate = creaDate
        self.password = passwd
        self.uid = uid
        self.predicates = ['user_name', 'user_screen_name', 'user_location',
                           'user_gender', 'user_created_at']

    def query_generator(self):
        template = prefix + ' select ?m where {{ ?x wb:{} ?m . ?x wb:user_uid "{}" .}}'
        return [template.format(pred, self.uid) for pred in self.predicates]  

    def load_from_db(self):
        queries = self.query_generator()
        results = [gstore.query('weibo', query)['results']['bindings'] for query in queries]
        results = [r[0]['m']['value'] for r in results]
        self.name = results[0]
        self.nickName = results[1]
        self.city = results[2]
        self.sex = results[3]
        self.creaDate = results[4]
        query = template.format('user_password', self.uid)
        res = gstore.query('weibo', query)['results']['bindings']
        if len(res) > 0:
            self.password = res[0]['m']['value']
        else:
            self.password = self.uid
            user_entity = '<http://localhost:2020/user/{}>'.format(self.uid)
            query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_password', self.password)
            gstore.query('weibo', query)
            print('first insert password when load user.')

    def save_to_db(self):
        user_entity = '<http://localhost:2020/user/{}>'.format(self.uid)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_name', self.name)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
            prefix, user_entity, 'user_password', self.password)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
            prefix, user_entity, 'user_screen_name', self.nickName)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_gender', self.sex)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
            prefix, user_entity, 'user_location', self.city)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}" .}}'.format(
                prefix, user_entity, 'user_uid', self.uid)
        gstore.query('weibo', query)
        query = '{} insert data {{ {} wb:{} "{}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .}}'.format(
            prefix, user_entity, 'user_created_at', self.creaDate)
        gstore.query('weibo', query)	





