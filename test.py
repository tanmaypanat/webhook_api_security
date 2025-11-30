import json
import hmac
import hashlib
import pytest
from app import app, SECRET_KEY, API_KEY
from messages import Student

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_webhook_success(client):
    # Sample student payload
    payload = {
        "name": "John Doe",
        "age": 20,
        "registered": True,
        "admission": "2025-09-01"
    }
    # Convert payload to JSON bytes
    data_bytes = json.dumps(payload).encode('utf-8')
    
    # Generate HMAC signature
    signature = hmac.new(SECRET_KEY, data_bytes, hashlib.sha256).hexdigest()
    
    # Generate Authorization header with API key
    headers = {
        "Content-Type": "application/json",
        "X-Signature": signature,
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Send POST request to webhook endpoint
    response = client.post("/webhook/1", data=data_bytes, headers=headers)
    
    # Validate response
    assert response.status_code == 200
    resp_json = response.get_json()
    assert resp_json["status"] == "recieved"
    assert set(resp_json["keys"]) == set(payload.keys())


def test_student_dataclass():
    s=Student(name="tanmay",age=16,registered=True)
    assert s.name is "tanmay"
    assert s.is_adult() is False