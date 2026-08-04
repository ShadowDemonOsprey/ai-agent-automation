"""
Agent tools module.

Tools are external capabilities that the AI agent
can call when it needs to perform an action.

Current tools:
- Calculator

Future tools:
- File reader
- Web search
- Database query
- Code execution
"""


def calculator(expression: str):
    """
    Calculate a mathematical expression.

    Args:
        expression (str):
            A mathematical expression.

            Example:
            "25 * 40"

    Returns:
        dict:
            Calculation result.
    """

    try:
        # Evaluate the mathematical expression.
        # Later we will replace this with a safer parser.
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



# Registry of available tools.
# The agent will use this list to know
# which tools exist.
TOOLS = {
    "calculator": calculator
}