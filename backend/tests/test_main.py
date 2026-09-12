from fastapi.testclient import TestClient

from backend.app.main import app


# Create a test client for the FastAPI application.
client = TestClient(app)


def test_root_endpoint():
    """
    Verify that the root endpoint returns
    the expected message and HTTP status code.
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Certificate Forgery Detection API is running"
    }


def test_health_endpoint():
    """
    Verify that the health endpoint reports
    that the application is healthy.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }