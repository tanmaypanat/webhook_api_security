import requests
import hmac
import hashlib
import json

WEBHOOK_KEY = "webhook"

data = {
    "name":"tanmay",
    "age": 12
}

url = "http://localhost:5000/webhooks"
datab=json.dumps(data).encode('utf-8')
keyb=WEBHOOK_KEY.encode('utf-8')

key = hmac.new(keyb,datab,hashlib.sha256).hexdigest()
response= requests.post(url=url,json=data,headers={
    'X-Signature': key
})
print(response.json())
url = "http://localhost:5000/generate_jwts"

data = {
    "username":"tanmay",
    "password":"1234"
}
response= requests.post(url=url,json=data,)
print(response.json())
jwtk = response.json().get("key")

url = "http://localhost:5000/generate_api_keys"

data = {
    "username":"tanmay",
    "password":"1234"
}
response= requests.post(url=url,json=data,headers={
    "Authorization": f"BEARER {jwtk}"
})
print(response.json())