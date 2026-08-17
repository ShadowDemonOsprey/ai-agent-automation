"""
Tools package.

This file exports available AI agent tools.
"""


from app.tools.calculator import calculator
from app.tools.date_time import date_time
from app.tools.file_analyzer import analyze_text as file_analyzer
from app.tools.knowledge_search import knowledge_search
from app.tools.statistics import statistics

# Tool registry.
# The agent uses this dictionary
# to discover available tools.
TOOLS = {
    "calculator": calculator,
    "statistics": statistics,
    "date_time": date_time,
    "file_analyzer": file_analyzer,
    "knowledge_search": knowledge_search,
}
