"""
Agent tool routing integration tests.

Verifies the planner routes requests to the correct
tools and that tool results become agent responses.
"""


from app.agent import AIAgent
from app.memory import memory


def _fresh_agent():
    memory.clear()
    return AIAgent()


def test_agent_routes_statistics():
    agent = _fresh_agent()

    result = agent.run(
        "What is the mean of 4 8 15 16 23 42?"
    )

    assert result.tool_used == "statistics"
    assert result.tool_result["mean"] == 18
    assert "mean" in result.response


def test_agent_routes_date_time():
    agent = _fresh_agent()

    result = agent.run(
        "What is the current date?"
    )

    assert result.tool_used == "date_time"
    assert "date" in result.tool_result


def test_agent_routes_file_analyzer():
    agent = _fresh_agent()

    result = agent.run(
        "Analyze this text: hello world hello"
    )

    assert result.tool_used == "file_analyzer"
    assert result.tool_result["words"] == 3
    assert result.tool_result["unique_words"] == 2


def test_agent_routes_calculator_with_words():
    agent = _fresh_agent()

    result = agent.run(
        "Calculate the square root of 144"
    )

    assert result.tool_used == "calculator"
    assert result.tool_result["result"] == 12


def test_agent_advanced_math_expression():
    agent = _fresh_agent()

    result = agent.run(
        "Calculate sin(pi/2) + sqrt(16)"
    )

    assert result.tool_used == "calculator"
    assert result.tool_result["result"] == 5


def test_agent_handles_tool_error():
    agent = _fresh_agent()

    result = agent.run(
        "Calculate 1 / 0"
    )

    assert result.tool_used == "calculator"
    assert "error" in result.tool_result
    assert len(result.response) > 0
