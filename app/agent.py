"""
AI Agent core module.

The agent workflow:

User request
    |
Memory
    |
Planner
    |
Decision
    |-- Tool execution
    |       |
    |   Tool result
    |
    |-- LLM reasoning
            |
        AI response
    |
Memory update

Current capabilities:
- Local LLM with Ollama (offline fallback included)
- Per-session persistent memory
- Long-term memory
- Tool calling
- Agent planning
- Structured AgentState output
- Streaming AI responses
- RAG knowledge retrieval

Current tools:
- Calculator (secure advanced math)
- Statistics
- Date/time
- File analyzer
- Knowledge search (RAG)

Future tools:
- Web search
- Database access
- Image analysis
"""


import re
from collections.abc import Iterator

from app.core.constants import AGENT_NAME
from app.llm.ollama_client import ollama_client
from app.logger import logger
from app.memory import ConversationMemory, memory
from app.models.agent_state import AgentState
from app.planner import planner
from app.tools import TOOLS


class AIAgent:
    """
    Main AI agent class.

    Responsible for:
    - Receiving user requests
    - Planning actions
    - Calling tools
    - Communicating with LLM
    - Managing memory
    - Streaming responses
    """



    def __init__(self):
        """
        Initialize the AI agent.
        """

        self.name = AGENT_NAME
        self.tools = TOOLS



    def run_tool(
        self,
        tool_name: str,
        argument: str
    ) -> dict:
        """
        Execute an available tool.

        Args:
            tool_name:
                Name of the tool.

            argument:
                Input for the tool.

        Returns:
            Tool execution result.
        """

        if tool_name in self.tools:
            return self.tools[tool_name](argument)

        logger.error(
            f"Tool not found: {tool_name}"
        )

        return {
            "error": f"Tool {tool_name} not found"
        }



    def _prepare_memory(
        self,
        session_id: str | None
    ) -> ConversationMemory:
        """
        Return the memory object for a session.

        With a session_id, memory is persistent and
        loaded from the database. Without one, the
        shared in-RAM memory is used.
        """

        if session_id:

            return ConversationMemory(
                session_id=session_id,
                persistent=True
            )

        return memory



    def _extract_expression(self, user_input: str) -> str:
        """
        Extract a mathematical expression from natural
        language, converting words into operators.
        """

        expression = user_input.lower()

        # Word replacements.
        expression = expression.replace("multiplied by", "*")
        expression = expression.replace("times", "*")
        expression = expression.replace("divided by", "/")
        expression = expression.replace("plus", "+")
        expression = expression.replace("minus", "-")
        expression = expression.replace("to the power of", "**")
        expression = expression.replace("power of", "**")

        # Multiplication shorthand "x" between numbers.
        # A plain replacement of "x" would corrupt words,
        # so it only applies between digits: "6x7" -> "6*7".
        expression = re.sub(
            r"(?<=\d)\s*[x×]\s*(?=\d)",
            "*",
            expression,
        )

        # Remove filler words.
        for word in [
            "calculate",
            "compute",
            "what is",
            "what's",
            "find",
            "please",
            "the result of",
            "solve",
        ]:
            expression = expression.replace(word, "")

        # Strip leading filler words.
        for _ in range(5):

            stripped = re.sub(
                r"^\s*(what is|what's|whats|the|a|an)\s+",
                "",
                expression,
            )

            if stripped == expression:
                break

            expression = stripped

        # Phrase conversions.
        expression = re.sub(
            r"square root of\s*(-?[0-9a-z.]+)",
            r"sqrt(\1)",
            expression
        )
        expression = re.sub(
            r"cube root of\s*(-?[0-9a-z.]+)",
            r"cbrt(\1)",
            expression
        )
        expression = re.sub(
            r"(\d+)\s+squared",
            r"(\1)**2",
            expression
        )
        expression = re.sub(
            r"(\d+)\s+cubed",
            r"(\1)**3",
            expression
        )

        # Remove sentence punctuation. Commas (function
        # arguments, thousands separators) and periods
        # (decimal points) are preserved.
        expression = re.sub(
            r"[?!;:]",
            "",
            expression
        )
        expression = re.sub(
            r"\.+$",
            "",
            expression
        )

        return expression.strip()



    def _prepare_tool_argument(
        self,
        tool_name: str,
        user_input: str
    ) -> str:
        """
        Prepare tool-specific arguments.
        """

        if tool_name == "calculator":

            return self._extract_expression(user_input)

        if tool_name == "file_analyzer":

            text = user_input.lower()

            # Take everything after the first colon,
            # e.g. "analyze this text: hello world".
            if ":" in text:

                text = text.split(":", 1)[1]

            else:

                text = re.sub(
                    r"^(analyze this text|analyze the text|"
                    r"analyze|word count of|count words in)\s+",
                    "",
                    text,
                    flags=re.IGNORECASE,
                )

            return text.strip() or user_input

        if tool_name == "knowledge_search":

            text = re.sub(
                r"^(search the knowledge base for|search the "
                r"knowledge base|search the knowledge|search "
                r"the kb for|search kb for|search kb|find "
                r"information about|find info on|look up|search "
                r"for|search for|what do you know about|tell "
                r"me about)\s+",
                "",
                user_input,
                flags=re.IGNORECASE,
            )

            return text.strip() or user_input

        return user_input



    def _format_tool_response(
        self,
        tool_name: str,
        result: dict
    ) -> str:
        """
        Convert a tool result into a natural language
        response.
        """

        if "error" in result and result["error"]:

            return (
                f"I tried to use the {tool_name} tool "
                f"but ran into a problem: {result['error']}."
            )

        if tool_name == "calculator":

            return (
                f"I used the calculator tool. "
                f"The result of {result['expression']} "
                f"is {result['result']}."
            )

        if tool_name == "statistics":

            return (
                "I analyzed the numbers with the statistics tool. "
                f"There are {result['count']} values with "
                f"a mean of {result['mean']}, a median of "
                f"{result['median']}, a minimum of {result['min']} "
                f"and a maximum of {result['max']}."
            )

        if tool_name == "date_time":

            if "days_between" in result:

                return (
                    f"There are {result['days_between']} days "
                    f"between {result['start']} and {result['end']}."
                )

            if "result_date" in result:

                operation = result.get("operation", "")

                if operation == "subtract":

                    return (
                        f"{result['amount_days']} days subtracted "
                        f"from today gives {result['result_date']} "
                        f"({result['weekday']})."
                    )

                return (
                    f"{result['amount_days']} days added to "
                    f"today gives {result['result_date']} "
                    f"({result['weekday']})."
                )

            return (
                f"The current date and time is "
                f"{result['datetime']} ({result['weekday']}, UTC)."
            )

        if tool_name == "file_analyzer":

            return (
                "I analyzed the text with the file analyzer. "
                f"It contains {result['words']} words "
                f"({result['unique_words']} unique), "
                f"{result['characters']} characters, "
                f"{result['sentences']} sentences, and about "
                f"{result['estimated_reading_minutes']} minutes "
                "of reading time."
            )

        if tool_name == "knowledge_search":

            snippets = " ".join(
                f"- {item['content'][:150]}"
                for item in result["results"]
            )

            return (
                f"I searched the knowledge base and found "
                f"{result['result_count']} relevant chunks. "
                f"Top matches:\n{snippets}"
            )

        return str(result)



    def _build_prompt(self, user_input: str, history: list) -> str:
        """
        Build the LLM prompt from conversation history.
        """

        conversation = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in history
            ]
        )

        return f"""
        You are an AI business automation assistant.

        Conversation history:
        {conversation}

        User request:
        {user_input}

        Provide a helpful answer.
        """



    def run(
        self,
        user_input: str,
        session_id: str | None = None
    ) -> AgentState:
        """
        Normal non-streaming agent execution.

        Args:
            user_input:
                User message.
            session_id:
                Optional conversation session for
                persistent memory.

        Returns:
            AgentState with the agent response.
        """

        logger.info(
            f"Received user request: {user_input}"
        )

        agent_memory = self._prepare_memory(session_id)

        agent_memory.add_message(
            "user",
            user_input
        )

        plan = planner.decide(user_input)

        logger.info(
            f"Planner decision: {plan}"
        )

        # Tool execution path.
        if plan["action"] == "tool":

            tool_name = plan["tool"]

            logger.info(
                f"Executing tool: {tool_name}"
            )

            argument = self._prepare_tool_argument(
                tool_name,
                user_input
            )

            tool_result = self.run_tool(
                tool_name,
                argument
            )

            response = self._format_tool_response(
                tool_name,
                tool_result
            )

            agent_memory.add_message(
                "assistant",
                response
            )

            return AgentState(
                agent=self.name,
                plan=plan,
                tool_used=tool_name,
                tool_result=tool_result,
                response=response,
                memory=agent_memory.get_history(),
                session_id=session_id
            )

        # LLM reasoning path.
        history = agent_memory.get_history()

        prompt = self._build_prompt(
            user_input,
            history
        )

        response = ollama_client.generate(prompt)

        agent_memory.add_message(
            "assistant",
            response
        )

        return AgentState(
            agent=self.name,
            plan=plan,
            response=response,
            memory=agent_memory.get_history(),
            session_id=session_id
        )



    def stream_run(
        self,
        user_input: str,
        session_id: str | None = None
    ) -> Iterator[str]:
        """
        Streaming agent execution.

        This method provides ChatGPT-style responses.

        Flow:

        User
          |
        Agent
          |
        Ollama streaming LLM
          |
        Token chunks
          |
        API Server Sent Events

        Args:
            user_input:
                User message.
            session_id:
                Optional conversation session for
                persistent memory.

        Yields:
            Text chunks from the LLM.
        """

        logger.info(
            f"Received streaming request: {user_input}"
        )

        agent_memory = self._prepare_memory(session_id)

        # Store user message before generating response.
        agent_memory.add_message(
            "user",
            user_input
        )

        plan = planner.decide(user_input)

        logger.info(
            f"Streaming planner decision: {plan}"
        )

        # Tool responses are returned as one chunk.
        if plan["action"] == "tool":

            tool_name = plan["tool"]

            argument = self._prepare_tool_argument(
                tool_name,
                user_input
            )

            tool_result = self.run_tool(
                tool_name,
                argument
            )

            response = self._format_tool_response(
                tool_name,
                tool_result
            )

            agent_memory.add_message(
                "assistant",
                response
            )

            yield response

            return

        # LLM streaming path.
        history = agent_memory.get_history()

        prompt = self._build_prompt(
            user_input,
            history
        )

        complete_response = ""

        for chunk in ollama_client.stream_generate(prompt):

            complete_response += chunk

            yield chunk

        # Save complete response after streaming finishes.
        agent_memory.add_message(
            "assistant",
            complete_response
        )



# Shared agent instance.
agent = AIAgent()
