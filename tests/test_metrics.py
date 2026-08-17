"""
Monitoring metrics endpoint tests.
"""


from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_metrics_endpoint():
    """
    Metrics report request counts after traffic.
    """

    # Generate some traffic.
    client.get("/health")

    client.get("/")

    response = client.get(
        "/metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_requests" in data

    assert "total_errors" in data

    assert "error_rate" in data

    assert "average_latency_ms" in data

    assert "by_method" in data

    assert "by_path" in data

    assert "by_status" in data

    assert data["total_requests"] >= 3


def test_metrics_track_paths():
    """
    Metrics record individual request paths.
    """

    client.get("/health")

    data = client.get("/metrics").json()

    assert data["by_path"].get("/health", 0) >= 1
