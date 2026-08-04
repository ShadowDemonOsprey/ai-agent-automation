"""
Tools package.

This file exports available AI agent tools.
"""


from app.tools.calculator import calculator


# Tool registry.
# The agent uses this dictionary
# to discover available tools.
TOOLS = {
    "calculator": calculator
}