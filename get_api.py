#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
url = "http://amls.intrumnet.com:81/sharedapi/purchaser/filter"
url_add = "http://amls.intrumnet.com:81/sharedapi/purchaser/insert"
url_update = "http://amls.intrumnet.com:81/sharedapi//purchaser/update"
def get_user_by_telegram_id(telegram_id):
  data = {
    'apikey': '0635d163f4c298d4383e50e8902d0f5a',
    'params': {
      'fields':{
        'id': '1560',
        'value': telegram_id
      }
    }
  }
  response = requests.get(url,params=data)
  print(response.json())

def get_ref_parent(ref_parent):
  data = {
  'apikey': '0635d163f4c298d4383e50e8902d0f5a',
  'params': {
    'fields':{
      'id': '1563',
      'value': ref_parent
      }
    } 
  }
  response = requests.get(url,params=data)
  print(response.json())

def get_phone_duplicate(phone):
  data = {
    'apikey': '0635d163f4c298d4383e50e8902d0f5a',
    'params': {
      'search': phone
    }
  }

response = requests.get(url,params=data)
print(response.json())

def update_contact_duplicate(id,telegram_id,parentRef,ref):
  data = {
  'apikey': '0635d163f4c298d4383e50e8902d0f5a',
  'params':
    {'id': id,'fields':
    {
      {'id': '1560','value': telegram_id},
      {'id': '1561','value': parentRef},
      {'id': '1563','value': ref}
    }
    }
  }

  response = requests.get(url_update,params=data)
  print(response.json())
def add(name,phone,telegram_id):
  data = {
  'apikey': '0635d163f4c298d4383e50e8902d0f5a',
  'params': 
    {
      'manager_id': '0',
      'name': name,
      'phone': phone,
      'fields':
      {
      {
        'id': '1560',
        'value': telegram_id
      },
      {
        'id': '1561',
        'value': parentRef
      },
      {
        'id': '1563',
        'value': ref
      }
      }
    }
  }

  response = requests.get(url_add,params=data)
  print(response.json())

def update_contact(id,wallet_id):
  data = {
  'apikey': '0635d163f4c298d4383e50e8902d0f5a',
  'params': 
    {
      'id': id,
      'fields':
      {
      {
        'id': '1564',
        'value': wallet_id
      },
      {
        'id': '1566',
        'value': '0'
      }
      }
    }
  }

  response = requests.get(url_update,params=data)
  print(response.json())
