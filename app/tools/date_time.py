"""
Date and time tool.

Provides the agent with current date/time information
and simple date arithmetic.

Supported operations:
- Current time and date
- Date in the future or past ("add 5 days")
- Difference between two dates
"""


import re
from datetime import date, datetime, timedelta, timezone


def _utc_now() -> datetime:
    """
    Current UTC time as a naive datetime.
    """

    return datetime.now(timezone.utc).replace(tzinfo=None)


def _parse_date(value: str) -> date | None:
    """
    Parse a date from common formats.
    """

    for pattern in (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
    ):

        try:

            return datetime.strptime(
                value.strip(),
                pattern
            ).date()

        except ValueError:

            continue

    return None


def date_time(query: str) -> dict:
    """
    Answer date/time related queries.

    Args:
        query (str):
            User question about time or dates.

            Examples:
            "what time is it"
            "what is the date"
            "add 5 days"
            "days between 2024-01-01 and 2024-01-10"

    Returns:
        dict:
            Date/time information or error.
    """

    text = query.lower()

    now = _utc_now()

    today = now.date()

    # Date difference between two dates.
    dates = re.findall(
        r"\d{4}[-/]\d{1,2}[-/]\d{1,2}",
        text
    )

    if len(dates) == 2:

        start = _parse_date(dates[0])

        end = _parse_date(dates[1])

        if start and end:

            return {
                "tool": "date_time",
                "query": query,
                "days_between": (end - start).days,
                "start": start.isoformat(),
                "end": end.isoformat(),
            }

    # Date arithmetic: add/subtract days.
    match = re.search(
        r"(add|subtract)\s+(\d+)\s+days?",
        text
    )

    if match:

        operation = match.group(1)

        amount = int(match.group(2))

        if operation == "add":

            result = today + timedelta(days=amount)

        else:

            result = today - timedelta(days=amount)

        return {
            "tool": "date_time",
            "query": query,
            "operation": operation,
            "amount_days": amount,
            "result_date": result.isoformat(),
            "weekday": result.strftime("%A"),
        }

    # "N days from today" / "N days from now".
    match = re.search(
        r"(\d+)\s+days?\s+from\s+(today|now)\b",
        text
    )

    if match:

        amount = int(match.group(1))

        result = today + timedelta(days=amount)

        return {
            "tool": "date_time",
            "query": query,
            "operation": "add",
            "amount_days": amount,
            "result_date": result.isoformat(),
            "weekday": result.strftime("%A"),
        }

    # "N days ago".
    match = re.search(
        r"(\d+)\s+days?\s+ago\b",
        text
    )

    if match:

        amount = int(match.group(1))

        result = today - timedelta(days=amount)

        return {
            "tool": "date_time",
            "query": query,
            "operation": "subtract",
            "amount_days": amount,
            "result_date": result.isoformat(),
            "weekday": result.strftime("%A"),
        }

    # "in N days".
    match = re.search(
        r"\bin\s+(\d+)\s+days?\b",
        text
    )

    if match:

        amount = int(match.group(1))

        result = today + timedelta(days=amount)

        return {
            "tool": "date_time",
            "query": query,
            "operation": "add",
            "amount_days": amount,
            "result_date": result.isoformat(),
            "weekday": result.strftime("%A"),
        }

    # Default: report current date and time.
    return {
        "tool": "date_time",
        "query": query,
        "datetime": now.isoformat(sep=" "),
        "date": today.isoformat(),
        "time": now.strftime("%H:%M:%S"),
        "weekday": today.strftime("%A"),
        "timezone": "UTC",
    }
