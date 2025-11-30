from flask import Flask, request, jsonify
from messages import Student,StudentSchema
import os
import hmac
import hashlib
import jwt
import datetime
import secrets
import pytz
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="myuser",
        password="mypassword"
    )

    cur = conn.cursor()
    print("Connected to db")
except Exception as e:
    print("❌ Error:", e)

app = Flask(__name__)

user = {"username":"tanmay", "password":"Ilovec0de"}


WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
if not WEBHOOK_SECRET:
    raise Exception("No webhook secret in environmement")
SECRET_KEY = WEBHOOK_SECRET.encode('utf-8')
print(SECRET_KEY)

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise Exception("API key not found in env")

JWT_SECRET = "jwt_key"

@app.route("/webhook/<student_id>",methods=["POST"])
def webhook(student_id):
    if headers := request.headers:
        print(headers)
        recieved_signature = headers.get("X-Signature")
        authorization = headers.get("Authorization")
    
    actual_api_key = authorization.split(" ")[1]
    print(actual_api_key)
    print(API_KEY)
    if actual_api_key==API_KEY:
        print("API KEY VALIDATED")

    data_bytes = request.get_data()
    expected_signature = hmac.new(SECRET_KEY,data_bytes,hashlib.sha256).hexdigest()
    if expected_signature==recieved_signature:
        print("signature verified")
    print(student_id)
    content_type = request.headers.get("Content-Type")
    payload = None
    if content_type == "application/json":
        payload = request.get_json()
    schema = StudentSchema()
    if not payload:
        payload = request.form.to_dict()

    print(f"payload recieved {payload}")
    optional  = request.args
    if optional:
        print(optional)
    try:
        data = schema.load(payload)
    except Exception as e:
        print(e)
        return jsonify({"error":"Validation error"}),400
    student_dc = Student(**data)
    print("Student data class")
    print(student_dc)

    try:
        insert_query = """
            INSERT INTO students (name, age, registered, admission)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        cur.execute(insert_query, (student_dc.name, student_dc.age, student_dc.registered, student_dc.admission))
        new_id = cur.fetchone()[0]
        conn.commit()

        print(f"✅ Student inserted with id {new_id}")

    except Exception as db_err:
        conn.rollback()
        print("🔥 DB Insert Error:", db_err)
        return jsonify({"error":"database error"}),500

    if not payload:
        return jsonify({"error":"empty json body"}),400

    else:
        return jsonify({"status":"recieved", "keys":list(payload.keys())}),200

@app.route("/login",methods=["POST"])
def login():
    creds = request.get_json()
    print(creds)

    payload = {
        "username":creds["username"],
        "exp": datetime.datetime.now(pytz.utc) + datetime.timedelta(minutes=1)
    }
    jwt_token = jwt.encode(payload,JWT_SECRET,algorithm="HS256")
    return jsonify({"jwt":jwt_token})

@app.route("/generate_api_key",methods=["POST"])
def generate_api_key():
    print("in generate api key")
    auth = request.headers.get("Authorization")
    auth = auth.split(" ")[1]
    try:
        decode = jwt.decode(auth,JWT_SECRET,algorithms="HS256")
        print(decode)
    except:
        print(decode)
    api_key = secrets.token_hex(32)
    return jsonify({"status":"ok","api_key":api_key})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)