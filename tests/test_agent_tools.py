"""
Test AI agent tool calling.

This verifies:
- The agent detects when a tool is needed.
- The calculator tool is executed.
- The agent returns the tool result.
"""


from app.agent import AIAgent
from app.memory import memory



def test_agent_calculator_tool():
    """
    Test calculator tool execution through the agent.
    """


    # Clear previous conversations.
    # Tests should always start clean.
    memory.clear()


    # Create a new agent.
    agent = AIAgent()


    # Ask a calculation question.
    result = agent.run(
        "Calculate 25 * 40"
    )


    # Check that a tool was used.
    assert result["tool_used"] == "calculator"


    # Check that the calculator returned the correct value.
    assert result["tool_result"]["result"] == 1000


    # Check that the agent returned a response.
    assert len(result["response"]) > 0