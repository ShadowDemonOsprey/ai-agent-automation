"""
Agent planner module.

The planner decides what action the AI agent should take.

Current capabilities:
- Detect calculator usage
- Detect statistics requests
- Detect date/time requests
- Detect text analysis requests
- Detect knowledge base searches
- Route everything else to the LLM

Future capabilities:
- Multi-step planning
- Task decomposition
"""


import re


class AgentPlanner:
    """
    Determines the next action for the agent.
    """


    def decide(self, user_input: str):
        """
        Analyze user input and choose an action.

        Args:
            user_input (str):
                User request.

        Returns:
            dict:
                Planned action.
        """

        text = user_input.lower().strip()

        if not text:
            return {"action": "llm"}

        # Statistics before calculator: statistic
        # questions contain numbers but no operators.
        if any(
            re.search(rf"\b{re.escape(word)}\b", text)
            for word in [
                "mean",
                "median",
                "average",
                "mode",
                "sum of",
                "total of",
                "statistics",
                "quartile",
            ]
        ) or any(
            phrase in text
            for phrase in [
                "standard deviation",
                "stddev",
                "variance",
            ]
        ):
            return {
                "action": "tool",
                "tool": "statistics"
            }

        # Date and time questions.
        if (
            any(
                phrase in text
                for phrase in [
                    "what time",
                    "current time",
                    "what date",
                    "today's date",
                    "today is",
                    " add ",
                    " subtract ",
                    "days between",
                    "date of",
                ]
            )
            or re.search(r"\b(add|subtract)\s+\d+\s+days?\b", text)
            or re.search(r"\d+\s+days?\s+(from|ago)\b", text)
            or re.search(r"\bin\s+\d+\s+days?\b", text)
            or (
                " date" in text
                and any(word in text for word in [
                    "what", "current", "today", "add",
                    "subtract", "between"
                ])
            )
        ):
            return {
                "action": "tool",
                "tool": "date_time"
            }

        # Text / file analysis.
        if any(
            phrase in text
            for phrase in [
                "analyze this text",
                "analyze the text",
                "word count",
                "character count",
                "analyze text",
                "text analysis",
            ]
        ):
            return {
                "action": "tool",
                "tool": "file_analyzer"
            }

        # Knowledge base search.
        if any(
            phrase in text
            for phrase in [
                "search the knowledge",
                "search knowledge",
                "knowledge base",
                "look up in the knowledge",
                "retrieve from knowledge",
                "search the documents",
            ]
        ):
            return {
                "action": "tool",
                "tool": "knowledge_search"
            }

        # If the request looks like mathematics,
        # choose the calculator tool.
        if any(
            re.search(rf"\b{re.escape(word)}\b", text)
            for word in [
                "calculate",
                "multiply",
                "times",
                "plus",
                "minus",
            ]
        ) or any(
            phrase in text
            for phrase in [
                "divided by",
                "power of",
                "square root",
                "cube root",
                "cbrt",
            ]
        ) or any(
            op in text
            for op in ["+", "-", "*", "/"]
        ) or (
            "=" in text and "==" not in text and "!=" not in text
        ) or self._looks_like_math(text):
            return {
                "action": "tool",
                "tool": "calculator"
            }

        # Otherwise use the language model.
        return {
            "action": "llm"
        }



    def _looks_like_math(self, text: str) -> bool:
        """
        Detect compact math expressions such as
        "25 * 40" or "sqrt(16)".
        """

        # Math function calls.
        if any(
            function in text
            for function in [
                "sqrt",
                "log(",
                "sin(",
                "cos(",
                "tan(",
                "factorial",
            ]
        ):
            return True

        # Bare arithmetic between numbers.
        if re.search(r"\d+\s*[\+\-\*/\^]\s*\d+", text):
            return True

        return False



# Create shared planner instance.
planner = AgentPlanner()
