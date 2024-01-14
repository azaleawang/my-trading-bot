from fastapi.testclient import TestClient
from app.app import app  # replace with the path to your FastAPI app

client = TestClient(app)
def test_create_worker_server_with_auth(monkeypatch):
    # Prepare data for the test
    test_auth_token = "test_secret_password"
    monkeypatch.setenv("WORKER_SERVER_AUTH", test_auth_token)
    
    worker_server_data = {
        "instance_id": "Test Worker",
        "private_ip": "192.168.1.1",
        "total_memory": 1000
    }

    # Call the API endpoint
    # TODO Use test database table (使用測試模式的資料庫)
    response = client.post("/api/v1/worker-servers/", json=worker_server_data, headers={"Auth": "test_secret_password"})

    # Check the response
    assert response.status_code == 200
    assert response.json()["instance_id"] == worker_server_data["instance_id"]
    assert response.json()["private_ip"] == worker_server_data["private_ip"]
    assert response.json()["total_memory"] == worker_server_data["total_memory"]

def test_create_worker_server_without_auth():
    # Prepare data for the test
    
    worker_server_data = {
        "instance_id": "Test Worker",
        "private_ip": "192.168.1.1",
        "total_memory": 1000
    }

    # Call the API endpoint
    response = client.post("/api/v1/worker-servers/", json=worker_server_data)

    # Check the response
    assert response.status_code == 403

def test_create_worker_server_with_wrong_auth():
    # Prepare data for the test
    
    worker_server_data = {
        "instance_id": "Test Worker",
        "private_ip": "192.168.1.1",
        "total_memory": 1000
    }

    # Call the API endpoint
    response = client.post("/api/v1/worker-servers/", json=worker_server_data, headers={'Auth': 'wrong_auth'})

    # Check the response
    assert response.status_code == 403
