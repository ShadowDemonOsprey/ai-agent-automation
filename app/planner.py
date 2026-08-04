"""
Agent planner module.

The planner decides what action
the AI agent should take.

Current capabilities:
- Detect calculator usage

Future capabilities:
- Multi-step planning
- Tool selection
- Task decomposition
"""


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


        text = user_input.lower()


        # If the request looks like mathematics,
        # choose calculator tool.
        if any(
            word in text
            for word in [
                "calculate",
                "multiply",
                "times",
                "+",
                "-",
                "*",
                "/"
            ]
        ):

            return {
                "action": "tool",
                "tool": "calculator"
            }


        # Otherwise use the language model.
        return {
            "action": "llm"
        }



# Create shared planner instance.
planner = AgentPlanner()