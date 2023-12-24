from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.src.schema import schemas
from app.app import app
from app.utils.deps import get_current_user  # replace with the path to your FastAPI app

client = TestClient(app) 
def mock_get_current_user():
    return schemas.User(id=1, email="", name="")  # Replace with a mock user object

app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

def test_get_user_bot_details_authorized():
    response = client.get("/api/v1/users/1/bots")  # Assuming 1 is the user ID of the mock user
    assert response.status_code == 200
    # Add more assertions here

def test_get_user_bot_details_unauthorized():
    response = client.get("/api/v1/users/2/bots")  # A different user ID
    assert response.status_code == 403
    # Add more assertions here
