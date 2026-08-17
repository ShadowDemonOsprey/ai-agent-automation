"""
Conversation session API tests.

Tests:
- Session creation
- Session listing
- Session retrieval
- Session deletion
- Message history persistence
- Long-term memory management
"""


from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_create_session():
    """
    Verify a new conversation session can be created.
    """

    response = client.post(
        "/api/v1/sessions"
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data

    assert "session_id" in data



def test_list_sessions():
    """
    Verify sessions can be listed.
    """

    client.post("/api/v1/sessions")

    response = client.get(
        "/api/v1/sessions"
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)

    assert len(response.json()) >= 1



def test_get_session():
    """
    Verify an existing session can be retrieved.
    """

    create_response = client.post(
        "/api/v1/sessions"
    )

    session_id = (
        create_response
        .json()["session_id"]
    )

    response = client.get(
        f"/api/v1/sessions/{session_id}"
    )

    assert response.status_code == 200

    assert (
        response.json()["session_id"]
        == session_id
    )



def test_get_missing_session_404():
    """
    Verify unknown sessions return 404.
    """

    response = client.get(
        "/api/v1/sessions/does-not-exist"
    )

    assert response.status_code == 404



def test_delete_session():
    """
    Verify a session can be deleted.
    """

    create_response = client.post(
        "/api/v1/sessions"
    )

    session_id = (
        create_response
        .json()["session_id"]
    )

    response = client.delete(
        f"/api/v1/sessions/{session_id}"
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Session deleted"
    )



def test_session_persists_agent_messages():
    """
    Verify agent conversations are stored per session.
    """

    create_response = client.post(
        "/api/v1/sessions"
    )

    session_id = (
        create_response
        .json()["session_id"]
    )

    # Run the agent against the session.
    agent_response = client.post(
        "/api/v1/agent",
        json={
            "message": "Calculate 6 * 7",
            "session_id": session_id,
        },
    )

    assert agent_response.status_code == 200

    assert (
        agent_response.json()["session_id"]
        == session_id
    )

    # Message history should contain both roles.
    messages_response = client.get(
        f"/api/v1/sessions/{session_id}/messages"
    )

    assert messages_response.status_code == 200

    messages = messages_response.json()

    roles = [message["role"] for message in messages]

    assert "user" in roles

    assert "assistant" in roles



def test_session_memory_crud():
    """
    Verify long-term memory can be set,
    retrieved, searched and deleted.
    """

    create_response = client.post(
        "/api/v1/sessions"
    )

    session_id = (
        create_response
        .json()["session_id"]
    )

    # Store a fact.
    set_response = client.post(
        f"/api/v1/sessions/{session_id}/memory",
        json={
            "key": "user_name",
            "value": "Alex",
        },
    )

    assert set_response.status_code == 200

    # Retrieve all facts.
    get_response = client.get(
        f"/api/v1/sessions/{session_id}/memory"
    )

    assert get_response.status_code == 200

    records = get_response.json()

    assert len(records) == 1

    assert records[0]["key"] == "user_name"

    assert records[0]["value"] == "Alex"

    # Search for the fact.
    search_response = client.get(
        f"/api/v1/sessions/{session_id}/memory/search",
        params={"query": "Alex"},
    )

    assert search_response.status_code == 200

    assert len(search_response.json()) == 1

    # Update the fact.
    client.post(
        f"/api/v1/sessions/{session_id}/memory",
        json={
            "key": "user_name",
            "value": "Alexandra",
        },
    )

    updated = client.get(
        f"/api/v1/sessions/{session_id}/memory"
    ).json()

    assert updated[0]["value"] == "Alexandra"

    # Delete the fact.
    delete_response = client.delete(
        f"/api/v1/sessions/{session_id}/memory/user_name"
    )

    assert delete_response.status_code == 200

    empty = client.get(
        f"/api/v1/sessions/{session_id}/memory"
    ).json()

    assert empty == []



def test_delete_session_removes_messages():
    """
    Verify deleting a session removes its history.
    """

    create_response = client.post(
        "/api/v1/sessions"
    )

    session_id = (
        create_response
        .json()["session_id"]
    )

    client.post(
        "/api/v1/agent",
        json={
            "message": "hello there",
            "session_id": session_id,
        },
    )

    client.delete(
        f"/api/v1/sessions/{session_id}"
    )

    # Messages endpoint 404s because the session is gone.
    response = client.get(
        f"/api/v1/sessions/{session_id}/messages"
    )

    assert response.status_code == 404
