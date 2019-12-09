import requests

url = "http://amls.intrumnet.com:81/sharedapi/purchaser/filter"

data = {
	'apikey': '0635d163f4c298d4383e50e8902d0f5a',
	'params': {
		'fields':{
			'id': '1563',
			'value': '89ys89fga9fpag9as'
		}
	}
}

response = requests.get(url,params=data)
print(response.json())