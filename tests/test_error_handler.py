"""
Tests for API error handling.

Verifies that unexpected application
errors are converted into structured JSON.
"""


from fastapi.testclient import TestClient

from app.main import app



client = TestClient(
    app,
    raise_server_exceptions=False
)



def test_error_response_format():
    """
    Test that API errors return
    structured error responses.
    """


    @app.get("/test-error")
    def test_error():

        raise Exception(
            "Test failure"
        )


    response = client.get(
        "/test-error"
    )


    assert response.status_code == 500


    data = response.json()


    assert data["error"] == "Agent execution failed"

    assert data["message"] == "Test failure"