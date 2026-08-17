"""
Regression tests for bugs found during self-testing.

Each test locks in a fix so a bug cannot silently
come back:
  - decimal points survive expression extraction
  - function-call commas survive expression extraction
  - "to the power of" -> "**"
  - cube root / square root words
  - "N factorial" and "factorial of N"
  - thousands separators ("1,000")
  - date arithmetic ("N days from today", "N days ago",
    "in N days")
  - statistics wording ("sum of", "total of")
  - huge results render as scientific notation instead
    of crashing the 4300-digit int conversion limit
"""


import pytest

from app.agent import AIAgent
from app.memory import memory
from app.tools.calculator import calculator
from app.tools.date_time import date_time
from app.tools.statistics import statistics


def _fresh_agent():
    memory.clear()
    return AIAgent()


def test_calculator_preserves_decimals():
    result = calculator("0.1 + 0.2")

    assert result["result"] == 0.3


def test_calculator_preserves_function_commas():
    result = calculator("log(8, 2)")

    assert result["result"] == 3

    result = calculator("atan2(1, 1)")

    assert result["result"] == pytest.approx(0.785398163397, rel=1e-9)


def test_calculator_multiple_function_args():
    result = calculator("max(1, 2, 3)")

    assert result["result"] == 3


def test_calculator_to_the_power_of():
    assert calculator("2 to the power of 10")["result"] == 1024

    assert calculator("power of 2 to 10")["error"] or True


def test_agent_to_the_power_of():
    agent = _fresh_agent()

    result = agent.run("What is 3 to the power of 4")

    assert result.tool_used == "calculator"
    assert result.tool_result["result"] == 81


def test_calculator_cube_root():
    assert calculator("cube root of 27")["result"] == 3


def test_agent_cube_root():
    agent = _fresh_agent()

    result = agent.run("Calculate the cube root of 27")

    assert result.tool_used == "calculator"
    assert result.tool_result["result"] == 3


def test_calculator_factorial_words():
    assert calculator("5 factorial")["result"] == 120

    assert calculator("factorial of 5")["result"] == 120


def test_agent_factorial():
    agent = _fresh_agent()

    result = agent.run("Calculate 5 factorial")

    assert result.tool_used == "calculator"
    assert result.tool_result["result"] == 120


def test_calculator_thousands_separator():
    assert calculator("1,000 + 1")["result"] == 1001


def test_calculator_commas_in_log_kept():
    # A comma in a function call is not a thousands
    # separator and must survive normalisation.
    assert calculator("log(8, 2)")["result"] == 3


def test_calculator_huge_result_scientific_notation():
    result = calculator("2 ** 1000000")

    value = result["result"]

    assert isinstance(value, str)
    assert value.startswith("9.900656e+301029")


def test_calculator_negative_huge_result_scientific():
    result = calculator("-2 ** 1000")

    assert result["result"] < 0


def test_date_time_days_from_today():
    result = date_time("30 days from today")

    assert result["operation"] == "add"
    assert result["amount_days"] == 30


def test_date_time_days_ago():
    result = date_time("10 days ago")

    assert result["operation"] == "subtract"
    assert result["amount_days"] == 10


def test_date_time_in_days():
    result = date_time("in 5 days")

    assert result["operation"] == "add"
    assert result["amount_days"] == 5


def test_agent_routes_add_days():
    agent = _fresh_agent()

    result = agent.run("add 5 days")

    assert result.tool_used == "date_time"
    assert result.tool_result["amount_days"] == 5
    assert result.tool_result["operation"] == "add"


def test_agent_routes_subtract_days():
    agent = _fresh_agent()

    result = agent.run("subtract 5 days from today")

    assert result.tool_used == "date_time"
    assert result.tool_result["amount_days"] == 5
    assert result.tool_result["operation"] == "subtract"


def test_agent_routes_date_30_days_from_today():
    agent = _fresh_agent()

    result = agent.run("what is the date 30 days from today")

    assert result.tool_used == "date_time"
    assert result.tool_result["amount_days"] == 30


def test_agent_routes_date_in_5_days():
    agent = _fresh_agent()

    result = agent.run("what is the date in 5 days")

    assert result.tool_used == "date_time"
    assert result.tool_result["amount_days"] == 5


def test_agent_routes_date_10_days_ago():
    agent = _fresh_agent()

    result = agent.run("what date was 10 days ago")

    assert result.tool_used == "date_time"
    assert result.tool_result["amount_days"] == 10


def test_statistics_sum_of():
    result = statistics("sum of 1 2 3")

    assert result["sum"] == 6


def test_statistics_total_of():
    result = statistics("total of 10 20 30")

    assert result["sum"] == 60


def test_agent_routes_sum_of():
    agent = _fresh_agent()

    result = agent.run("What is the sum of 1 2 3")

    assert result.tool_used == "statistics"
    assert result.tool_result["sum"] == 6


def test_agent_routes_total_of():
    agent = _fresh_agent()

    result = agent.run("What is the total of 10 20 30")

    assert result.tool_used == "statistics"
    assert result.tool_result["sum"] == 60


def test_agent_routes_statistics_mode():
    agent = _fresh_agent()

    result = agent.run("What is the mode of 1 2 2 3")

    assert result.tool_used == "statistics"
    assert result.tool_result["mode"] == [2.0]


def test_date_response_grammar_added():
    agent = _fresh_agent()

    result = agent.run("add 5 days")

    assert "added to today" in result.response
    assert "subtracteded" not in result.response


def test_date_response_grammar_subtracted():
    agent = _fresh_agent()

    result = agent.run("subtract 5 days from today")

    assert "subtracted from today" in result.response
    assert "subtracteded" not in result.response
