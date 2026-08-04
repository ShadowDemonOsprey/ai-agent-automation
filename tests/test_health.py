"""
Tests for health check endpoint.
"""


from fastapi.testclient import TestClient

from app.main import app



client = TestClient(app)



def test_health_endpoint():
    """
    Test GET /health endpoint.
    """


    response = client.get(
        "/health"
    )


    assert response.status_code == 200


    data = response.json()


    assert data["status"] == "healthy"

    assert "agent" in data

    