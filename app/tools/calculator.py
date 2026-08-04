"""
Calculator tool module.

This tool allows the AI agent to perform
mathematical calculations.

Future improvements:
- Replace eval() with a safer math parser.
- Add support for advanced mathematics.
"""


def calculator(expression: str):
    """
    Calculate a mathematical expression.

    Args:
        expression (str):
            Mathematical expression.

            Example:
            "25 * 40"

    Returns:
        dict:
            Calculation result or error.
    """

    try:
        # Evaluate the expression.
        # This is acceptable for this learning project.
        # Later we will replace it with a secure parser.
        result = eval(expression)


        return {
            "tool": "calculator",
            "expression": expression,
            "result": result
        }


    except Exception as error:

        return {
            "tool": "calculator",
            "error": str(error)
        }