"""
Test AI agent tools.

This verifies:
- Tools can be called.
- The calculator returns correct results.
"""


from app.tools import calculator


def test_calculator_tool():
    """
    Test the calculator tool.
    """


    result = calculator(
        "25 * 40"
    )


    # Check that the result exists.
    assert result is not None


    # Check that the calculation is correct.
    assert result["result"] == 1000



def test_calculator_error():
    """
    Test calculator error handling.
    """


    result = calculator(
        "invalid expression"
    )


    # Check that an error is returned.
    assert "error" in result