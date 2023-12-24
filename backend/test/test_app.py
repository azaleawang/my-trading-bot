from fastapi.testclient import TestClient
from app.app import app  # replace with the path to your FastAPI app

client = TestClient(app)

def test_test_endpoint():

    # Call the API endpoint
    response = client.get("/test")

    # Check the response
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}