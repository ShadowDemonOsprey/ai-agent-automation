"""
Tests for API request logging middleware.
"""


from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_request_middleware():

    """
    Test that requests pass through
    the logging middleware successfully.
    """


    response = client.get(
        "/"
    )


    assert response.status_code == 200


    data = response.json()


    assert data["message"] == (
        "AI Agent Automation API is running"
    )