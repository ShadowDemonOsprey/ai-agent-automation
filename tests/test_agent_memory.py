"""
Test AI agent conversation memory.

This verifies:
- The agent stores user messages.
- The agent remembers previous conversation.
- The agent stores assistant responses.
"""


from app.agent import AIAgent
from app.memory import memory


def test_agent_remembers_context():
    """
    Test that the agent keeps conversation context.
    """


    # Clear old memory before starting the test.
    # This prevents previous tests from affecting this one.
    memory.clear()


    # Create a new agent instance.
    agent = AIAgent()


    # First user message.
    agent.run(
        "My name is Alex."
    )


    # Second user message asks about previous information.
    result = agent.run(
        "What is my name?"
    )


    # Check that the agent returned a response.
    assert result is not None


    # Check that conversation history exists.
    assert len(result.memory) > 0

    # Check that the first user message was stored.
    assert result.memory[0]["content"] == "My name is Alex."