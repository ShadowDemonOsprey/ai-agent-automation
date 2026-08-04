"""
Tests for versioned API routes.
"""


from fastapi.testclient import TestClient

from app.main import app



client = TestClient(app)



def test_v1_agent_route_exists():
    """
    Test that API v1 agent endpoint is available.
    """


    response = client.post(
        "/api/v1/agent",
        json={
            "message": "Calculate 5 * 5"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert "response" in data

