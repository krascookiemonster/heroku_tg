import requests
url = "http://amls.intrumnet.com:81/sharedapi/purchaser/filter"
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