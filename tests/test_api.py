"""
Test FastAPI agent endpoint.

This verifies:
- API receives user messages.
- API calls the AI agent.
- API returns AgentState JSON.
"""


from fastapi.testclient import TestClient

from app.main import app



# Create a test client.
# This simulates HTTP requests
# without running a real server.
client = TestClient(app)



def test_agent_api_endpoint():
    """
    Test POST /agent endpoint.
    """


    response = client.post(
        "/api/v1/agent",
        json={
           "message": "Calculate 10 * 10"
        }
    )

    # Check HTTP status code.
    assert response.status_code == 200


    # Convert response into JSON.
    data = response.json()


    # Check required AgentState fields.
    assert "agent" in data
    assert "response" in data
    assert "memory" in data


    # Check calculator was used.
    assert data["tool_used"] == "calculator"


    # Check calculation result.
    assert data["tool_result"]["result"] == 100

    