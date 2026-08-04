"""
Test agent state model.

This verifies:
- AgentState accepts valid data.
- Optional fields work correctly.
- Data validation works.
"""


from app.models.agent_state import AgentState



def test_agent_state_creation():
    """
    Test creating a complete agent state.
    """


    state = AgentState(
        agent="Business Automation Agent",
        response="AI can help businesses.",
        plan={
            "action": "llm"
        },
        memory=[
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    )


    # Check agent name.
    assert state.agent == "Business Automation Agent"


    # Check response.
    assert state.response == "AI can help businesses."


    # Check plan.
    assert state.plan["action"] == "llm"


    # Check memory.
    assert len(state.memory) == 1



def test_agent_state_optional_fields():
    """
    Test that optional fields can be empty.
    """


    state = AgentState(
        agent="Test Agent",
        response="Hello",
        memory=[]
    )


    # Optional values should be None.
    assert state.plan is None
    assert state.tool_used is None
    assert state.tool_result is None