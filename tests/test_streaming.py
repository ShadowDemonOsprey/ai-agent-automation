"""
Streaming API tests.

Tests:
- Streaming endpoint availability
- SSE response format
- Error handling behavior
"""


from fastapi.testclient import TestClient

from app.main import app



client = TestClient(app)



def test_streaming_endpoint_exists():
    """
    Verify the streaming chat endpoint works.

    The endpoint should:
    - Accept a message query parameter
    - Return Server Sent Events response
    """

    response = client.get(
        "/api/v1/chat/stream?message=hello"
    )


    assert response.status_code == 200

    assert (
        response.headers["content-type"]
        .startswith("text/event-stream")
    )



def test_streaming_returns_chunks(monkeypatch):
    """
    Verify streamed chunks are returned.

    Ollama is mocked because tests should not
    depend on a running local LLM server.
    """


    def fake_stream_run(message: str):
        yield "Hello"
        yield " world"



    from app import agent

    monkeypatch.setattr(
        agent.agent,
        "stream_run",
        fake_stream_run
    )


    response = client.get(
        "/api/v1/chat/stream?message=test"
    )


    assert response.status_code == 200

    assert "data: Hello" in response.text

    assert "data:  world" in response.text



def test_streaming_error_handling(monkeypatch):
    """
    Verify streaming endpoint handles agent errors safely.
    """


    def fake_error_stream(message: str):
        raise Exception("Test error")

        yield "never"



    from app import agent

    monkeypatch.setattr(
        agent.agent,
        "stream_run",
        fake_error_stream
    )


    response = client.get(
        "/api/v1/chat/stream?message=test"
    )


    assert response.status_code == 200

    assert "[ERROR] Test error" in response.text