#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import bs4
import parser
import markups as m
import sys
import subprocess
import json
import time
import requests


def checkPhone(phone):
	try:
		return (int(phone) < 80000000000 and int(phone) > 70000000000 and int(phone) / 10000000000 == 7)
	except:
		return False

print checkPhone("89998406120")

def send_p2p(my_login,api_access_token,to_qw,comment,sum_p2p):
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + api_access_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept']= 'application/json'
    postjson = json.loads('{"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"},"comment":"'+comment+'","fields":{"account":""}}')
    postjson['id']=str(int(time.time() * 1000))
    postjson['sum']['amount']=sum_p2p
    postjson['sum']['currency']='643'
    postjson['fields']['account']=to_qw
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments',json=postjson)
    print(res)
    return json.loads(res.text)