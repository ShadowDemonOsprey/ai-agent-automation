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
    from app.models.agent_state import AgentState

    assert isinstance(response, AgentState)

    # Check that the AI generated a response.
    assert response.response is not None

    # Check that response is not empty.
    assert len(response.response) > 0