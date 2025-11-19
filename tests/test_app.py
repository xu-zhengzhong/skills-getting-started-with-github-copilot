import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    test_email = "pytester@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={test_email}")
    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert f"Signed up {test_email}" in resp.json()["message"]
    # Duplicate sign up
    resp2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp2.status_code == 400
    # Unregister
    resp3 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp3.status_code == 200
    assert f"Unregistered {test_email}" in resp3.json()["message"]
    # Unregister again
    resp4 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp4.status_code == 400

def test_signup_activity_not_found():
    resp = client.post("/activities/Nonexistent/signup?email=abc@mergington.edu")
    assert resp.status_code == 404

def test_unregister_activity_not_found():
    resp = client.post("/activities/Nonexistent/unregister?email=abc@mergington.edu")
    assert resp.status_code == 404
