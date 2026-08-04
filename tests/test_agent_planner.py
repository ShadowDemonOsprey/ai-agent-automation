"""
Test agent planner integration.

This verifies:
- Agent uses the planner.
- Tool requests go through planner.
- Normal requests go to the LLM.
"""


from app.agent import AIAgent
from app.memory import memory



def test_agent_uses_planner_for_tools():
    """
    Test that calculator requests
    are handled by the planner.
    """


    # Start with clean memory.
    memory.clear()


    agent = AIAgent()


    result = agent.run(
        "Calculate 30 * 10"
    )


    # Check planner decision.
    assert result["plan"]["action"] == "tool"


    # Check selected tool.
    assert result["plan"]["tool"] == "calculator"


    # Check tool execution.
    assert result["tool_result"]["result"] == 300



def test_agent_uses_planner_for_llm():
    """
    Test that normal questions
    are sent to the LLM.
    """


    memory.clear()


    agent = AIAgent()


    result = agent.run(
        "What is artificial intelligence?"
    )


    # Planner should choose LLM.
    assert result["plan"]["action"] == "llm"


    # Response should exist.
    assert len(result["response"]) > 0