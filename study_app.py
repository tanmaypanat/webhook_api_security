from flask import Flask,request,jsonify
import hmac 
import hashlib
import jwt
import datetime
import pytz
import secrets

app = Flask(__name__)

WEBHOOK_KEY = "webhook"
jwt_key = "jwtsimple" # os.environ.get("jwt_key")
keyb= WEBHOOK_KEY.encode('utf-8')

@app.route("/webhooks",methods=["POST"])
def webhooks():
    payload = request.get_json()
    payloadb= request.get_data()
    headers= request.headers
    if headers:
        expected_signature = headers.get('X-Signature')

    actual_signature = hmac.new(keyb,payloadb,hashlib.sha256).hexdigest()
    if actual_signature==expected_signature:
        print("Signature matched")    
    print(payload)
    return jsonify({"status":"success"}),200

@app.route("/generate_jwts",methods=["POST"])
def generate_jwts():
    payload=request.get_json()
    username = payload.get("username")
    password = payload.get("password")

    data = {
        "username": username,
        "exp": datetime.datetime.now(pytz.utc) + datetime.timedelta(minutes=10)
    }
    jwtk = jwt.encode(data,jwt_key,algorithm='HS256')
    return jsonify({"key":jwtk}),200

@app.route("/generate_api_keys",methods=["POST"])
def generate_api_keys():
    
    auth = request.headers.get("Authorization")
    auth = auth.split(" ")[1]
    try:
        decode = jwt.decode(auth,jwt_key,algorithms="HS256")
        print(decode)
    except:
        print(decode)
    if decode["username"]=="tanmay":
        print("jwt accespted")
    apik = secrets.token_hex(32)
    return jsonify({"apik":apik}),200

if __name__ == "__main__":
    app.run(host="localhost",port=5000,debug=True)