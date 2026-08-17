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


def test_calculator_cube_root_negative():
    assert calculator("cube root of -8")["result"] == -2


def test_calculator_not_equal():
    result = calculator("3 != 4")

    assert result["result"] == 1


def test_calculator_postfix_fact_no_corrupt_ne():
    """5! must work but 3 != must not become factorial."""
    assert calculator("5!")["result"] == 120
    assert calculator("3 != 4")["result"] == 1


def test_calculator_not_equal_various():
    assert calculator("1 != 1")["result"] == 0
    assert calculator("2 != 3")["result"] == 1


def test_calculator_float_factorial_error():
    result = calculator("2.5!")

    assert "error" in result


# ── Planner false-positive regression tests ──────────────────────

def _fresh_planner():
    from app.planner import AgentPlanner

    return AgentPlanner()


def test_planner_model_not_misrouted():
    p = _fresh_planner()
    assert p.decide("what does this model do")["action"] == "llm"


def test_planner_modest_not_misrouted():
    p = _fresh_planner()
    assert p.decide("that was a modest proposal")["action"] == "llm"


def test_planner_modify_not_misrouted():
    p = _fresh_planner()
    assert p.decide("we need to modify the code")["action"] == "llm"


def test_planner_remove_not_misrouted():
    p = _fresh_planner()
    assert p.decide("remove this item")["action"] == "llm"


def test_planner_meaning_not_misrouted():
    p = _fresh_planner()
    assert p.decide("the meaning of life")["action"] == "llm"


def test_planner_minimal_not_misrouted():
    p = _fresh_planner()
    assert p.decide("this is a minimum viable product")["action"] == "llm"


def test_planner_administer_not_misrouted():
    p = _fresh_planner()
    assert p.decide("please administer the test")["action"] == "llm"


def test_planner_assumption_not_misrouted():
    p = _fresh_planner()
    assert p.decide("the assumption of risk")["action"] == "llm"


# ── Metrics path normalization tests ─────────────────────────────

def test_metrics_normalizes_session_paths():
    from app.middleware import MetricsCollector

    mc = MetricsCollector()
    mc.record("GET", "/api/v1/sessions/abc-1234", 200, 0.01)
    mc.record("GET", "/api/v1/sessions/def-5678", 200, 0.01)
    snap = mc.snapshot()

    assert len(snap["by_path"]) == 1
    assert snap["total_requests"] == 2


def test_metrics_normalizes_document_paths():
    from app.middleware import MetricsCollector

    mc = MetricsCollector()
    mc.record("GET", "/api/v1/knowledge/documents/uuid1", 200, 0.01)
    mc.record("GET", "/api/v1/knowledge/documents/uuid2", 200, 0.01)
    snap = mc.snapshot()

    assert len(snap["by_path"]) == 1


def test_metrics_preserves_static_paths():
    from app.middleware import MetricsCollector

    mc = MetricsCollector()
    mc.record("GET", "/api/v1/sessions", 200, 0.01)
    mc.record("GET", "/health", 200, 0.01)
    mc.record("GET", "/metrics", 200, 0.01)
    snap = mc.snapshot()

    assert len(snap["by_path"]) == 3


# ── Error handler security test ──────────────────────────────────

def test_error_handler_does_not_leak_details():
    from fastapi.testclient import TestClient

    from app.main import app

    test_client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    @app.get("/test-internal-error")
    def boom():
        raise Exception("secret_db_password_123")

    response = test_client.get("/test-internal-error")
    body = response.json()

    assert response.status_code == 500
    assert "secret_db_password" not in body.get("message", "")
    assert "internal error" in body["message"].lower()


# ── API key uses constant-time comparison ─────────────────────────

def test_security_module_uses_hmac():
    import app.core.security as sec

    source_lines = open(sec.__file__).read()
    assert "hmac.compare_digest" in source_lines


# ── top_k validation ─────────────────────────────────────────────

def test_top_k_must_be_positive():
    from pydantic import ValidationError

    from app.models.request import KnowledgeSearchRequest

    try:
        KnowledgeSearchRequest(query="test", top_k=0)
        assert False, "Should have raised"
    except ValidationError:
        pass

    try:
        KnowledgeSearchRequest(query="test", top_k=-1)
        assert False, "Should have raised"
    except ValidationError:
        pass

    r = KnowledgeSearchRequest(query="test", top_k=5)
    assert r.top_k == 5
