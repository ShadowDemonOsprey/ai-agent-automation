"""
Test the AI Agent workflow.

This verifies:
- The agent can receive input.
- The agent can call Ollama.
- The agent returns a valid response.
"""


from app.agent import agent


def test_agent_response():
    """
    Test the complete agent pipeline.

    User input:
        A simple business question.

    Expected:
        The AI agent returns a non-empty text response.
    """

    response = agent.run(
        "How can AI improve customer service?"
    )


    # Check that the agent returns a result.
    assert response is not None


    # Check that the result is a dictionary.
    assert isinstance(response, dict)


    # Check that the AI generated a response.
    assert "response" in response


    # Check that the generated response is not empty.
    assert len(response["response"]) > 0

    