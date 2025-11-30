import requests
import json 
import os
import hmac
import hashlib

user = {"username":"tanmay", "password":"Ilovec0de"}

jwt= None


login_url = "http://localhost:5000/login"
login_data = {
    "username": user['username'],
    "password": user['password']
}

response = requests.post(login_url,json=login_data)
jwt = response.json().get("jwt")
print(jwt)

get_api_url = "http://localhost:5000/generate_api_key"
response = requests.post(get_api_url,headers={
    "Authorization": f"BEARER {jwt}"
})
print(response.json())
# get webhook from environment and make it bytes
webhook_secret = os.environ.get("WEBHOOK_SECRET")
if not webhook_secret:
    raise Exception("No webhook secret found")
SECRET_KEY = webhook_secret.encode('utf-8')

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
     raise Exception("Api key not found in env")


url = "http://localhost:5000/webhook/123"

data  = {
    "name" : "Tanmay",
    "age" : 12,
    "registered" : True
}

#create x signature 
# convert dict to json string in bytes 
data_bytes = json.dumps(data).encode('utf-8')
signature = hmac.new(SECRET_KEY,data_bytes,hashlib.sha256).hexdigest()

params = {
    "subject" : "math",
    "failed" : True
}

response = requests.post(url,json=data,params=params,headers={
        "Content-Type": "application/json",
        "X-Signature": signature,
        "Authorization": f"BEARER {API_KEY}"
    })
print(response.json())