"""
API key authentication tests.

Verifies that /api/v1 endpoints enforce the
X-API-Key header when an API key is configured,
and allow open access when it is not.
"""


from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)



def test_open_access_when_no_key_configured(monkeypatch):
    """
    Without an API key, endpoints work freely.
    """

    monkeypatch.setattr(settings, "API_KEY", None)

    response = client.get(
        "/api/v1/sessions"
    )

    assert response.status_code == 200



def test_401_without_key(monkeypatch):
    """
    With an API key set, missing keys are rejected.
    """

    monkeypatch.setattr(settings, "API_KEY", "test-secret")

    response = client.get(
        "/api/v1/sessions"
    )

    assert response.status_code == 401


def test_401_with_wrong_key(monkeypatch):
    """
    With an API key set, wrong keys are rejected.
    """

    monkeypatch.setattr(settings, "API_KEY", "test-secret")

    response = client.get(
        "/api/v1/sessions",
        headers={"X-API-Key": "wrong"},
    )

    assert response.status_code == 401


def test_200_with_correct_key(monkeypatch):
    """
    The correct API key is accepted.
    """

    monkeypatch.setattr(settings, "API_KEY", "test-secret")

    response = client.get(
        "/api/v1/sessions",
        headers={"X-API-Key": "test-secret"},
    )

    assert response.status_code == 200


def test_public_endpoints_not_protected(monkeypatch):
    """
    Health, metrics and UI remain public.
    """

    monkeypatch.setattr(settings, "API_KEY", "test-secret")

    assert client.get("/health").status_code == 200

    assert client.get("/metrics").status_code == 200
