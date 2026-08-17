"""
Date/time tool tests.
"""


from app.tools.date_time import date_time


def test_current_datetime():
    result = date_time("what time is it")

    assert result["tool"] == "date_time"
    assert "datetime" in result
    assert "date" in result
    assert "weekday" in result


def test_current_date():
    result = date_time("what is today's date")

    assert "date" in result


def test_add_days():
    result = date_time("add 5 days")

    assert result["operation"] == "add"
    assert result["amount_days"] == 5
    assert "result_date" in result


def test_subtract_days():
    result = date_time("subtract 3 days")

    assert result["operation"] == "subtract"
    assert result["amount_days"] == 3


def test_days_between():
    result = date_time(
        "days between 2024-01-01 and 2024-01-10"
    )

    assert result["days_between"] == 9
