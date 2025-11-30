from study_app import app
import pytest
import json
import hmac
import hashlib
from study_messages import Student,StudentSchema
from marshmallow import ValidationError


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hmack(client):
    WEBHOOK_KEY = "webhook"

    data = {
        "name":"tanmay",
        "age": 12
    }

    url = "/webhooks"
    datab=json.dumps(data).encode('utf-8')
    keyb=WEBHOOK_KEY.encode('utf-8')

    key = hmac.new(keyb,datab,hashlib.sha256).hexdigest()
    response= client.post(url,json=data,headers={
    'X-Signature': key
    })
    assert response.status_code == 200

def test_student_dataclass():
    s=Student(name="tanmay",age=15)
    assert s.name=="tanmay"
    assert s.is_adult()==False

def test_student_schema():
    s={"name":"tanm","age":15}
    ss= StudentSchema()
    with pytest.raises(ValidationError) as execinfo:
        res = ss.load(s)
    assert "name" not in execinfo.value.messages
