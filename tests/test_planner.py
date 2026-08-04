"""
Test agent planning system.

This verifies:
- The planner can detect when a tool is needed.
- The planner can choose normal LLM responses.
"""


from app.planner import AgentPlanner



def test_planner_detects_calculator():
    """
    Test calculator tool detection.
    """

    planner = AgentPlanner()


    plan = planner.decide(
        "Calculate 100 * 5"
    )


    # The planner should choose a tool.
    assert plan["action"] == "tool"


    # The selected tool should be calculator.
    assert plan["tool"] == "calculator"



def test_planner_uses_llm():
    """
    Test normal conversation routing.
    """

    planner = AgentPlanner()


    plan = planner.decide(
        "Explain artificial intelligence."
    )


    # The planner should choose the LLM.
    assert plan["action"] == "llm"