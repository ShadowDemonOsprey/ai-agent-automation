"""
Tests for application structured logging.
"""


import json
import logging

from app.logger import JSONFormatter


def test_json_formatter_output():
    """
    Verify that log records are converted
    into valid JSON format.
    """

    formatter = JSONFormatter()


    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )


    output = formatter.format(
        record
    )


    data = json.loads(
        output
    )


    assert data["level"] == "INFO"

    assert data["logger"] == "test"

    assert data["message"] == "Test message"



def test_json_formatter_request_id():
    """
    Verify that request IDs are included
    when available.
    """

    formatter = JSONFormatter()


    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Request message",
        args=(),
        exc_info=None,
    )


    record.request_id = "12345"


    output = formatter.format(
        record
    )


    data = json.loads(
        output
    )


    assert data["request_id"] == "12345"