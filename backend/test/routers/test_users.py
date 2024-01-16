from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.app import app
from app.schema import user as schemas
from app.utils.deps import get_current_user

client = TestClient(app) 
def mock_get_current_user():
    return schemas.User(id=1, email="", name="")

app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

def test_get_user_bot_details_authorized():
    response = client.get("/api/v1/users/1/bots")  # Assuming 1 is the user ID of the mock user
    assert response.status_code == 200

def test_get_user_bot_details_unauthorized():
    response = client.get("/api/v1/users/2/bots")  # A different user ID
    assert response.status_code == 403
