"""
Web chat UI tests.
"""


from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_ui_served():
    """
    The static chat UI is available at /ui.
    """

    response = client.get(
        "/ui"
    )

    assert response.status_code == 200

    assert "text/html" in response.headers["content-type"]

    assert "AI Agent" in response.text
