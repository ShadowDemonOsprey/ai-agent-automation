"""
AI Agent core module.

The agent workflow:

User request
    ↓
Memory
    ↓
Planner
    ↓
Decision
    ├── Tool execution
    │       ↓
    │   Tool result
    │
    └── LLM reasoning
            ↓
        AI response

    ↓
Memory update


Current capabilities:
- Local LLM with Ollama
- Conversation memory
- Tool calling
- Agent planning
- Structured AgentState output
- Streaming AI responses


Current tools:
- Calculator


Future tools:
- RAG search
- File analysis
- Database access
- Web search
"""


from app.core.constants import AGENT_NAME
from app.llm.ollama_client import ollama_client
from app.memory import memory
from app.tools import TOOLS
from app.planner import planner
from app.models.agent_state import AgentState
from app.logger import logger



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



    def run_tool(self, tool_name: str, argument: str):
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



    def run(self, user_input: str):
        """
        Normal non-streaming agent execution.

        Existing agent pipeline remains unchanged.
        """

        logger.info(
            f"Received user request: {user_input}"
        )


        memory.add_message(
            "user",
            user_input
        )


        plan = planner.decide(
            user_input
        )


        logger.info(
            f"Planner decision: {plan}"
        )


        if plan["action"] == "tool":

            tool_name = plan["tool"]


            if tool_name == "calculator":

                logger.info(
                    f"Executing tool: {tool_name}"
                )


                expression = (
                    user_input
                    .lower()
                    .replace("calculate", "")
                    .replace("times", "*")
                )


                tool_result = self.run_tool(
                    tool_name,
                    expression.strip()
                )


                response = (
                    f"I used the {tool_name} tool. "
                    f"The result is {tool_result['result']}."
                )


                memory.add_message(
                    "assistant",
                    response
                )


                return AgentState(
                    agent=self.name,
                    plan=plan,
                    tool_used=tool_name,
                    tool_result=tool_result,
                    response=response,
                    memory=memory.get_history()
                )



        history = memory.get_history()


        conversation = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in history
            ]
        )


        prompt = f"""
        You are an AI business automation assistant.

        Conversation history:
        {conversation}

        User request:
        {user_input}

        Provide a helpful answer.
        """


        response = ollama_client.generate(
            prompt
        )


        memory.add_message(
            "assistant",
            response
        )


        return AgentState(
            agent=self.name,
            plan=plan,
            response=response,
            memory=memory.get_history()
        )



    def stream_run(self, user_input: str):
        """
        Streaming agent execution.

        This method provides ChatGPT-style responses.

        Flow:

        User
          ↓
        Agent
          ↓
        Ollama streaming LLM
          ↓
        Token chunks
          ↓
        API Server Sent Events


        Args:
            user_input:
                User message.

        Yields:
            Text chunks from the LLM.
        """

        logger.info(
            f"Received streaming request: {user_input}"
        )


        # Store user message before generating response.
        memory.add_message(
            "user",
            user_input
        )


        plan = planner.decide(
            user_input
        )


        logger.info(
            f"Streaming planner decision: {plan}"
        )


        # Tool responses are returned as one chunk.
        if plan["action"] == "tool":

            tool_name = plan["tool"]


            if tool_name == "calculator":

                expression = (
                    user_input
                    .lower()
                    .replace("calculate", "")
                    .replace("times", "*")
                )


                tool_result = self.run_tool(
                    tool_name,
                    expression.strip()
                )


                response = (
                    f"I used the {tool_name} tool. "
                    f"The result is {tool_result['result']}."
                )


                memory.add_message(
                    "assistant",
                    response
                )


                yield response
                return



        history = memory.get_history()


        conversation = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in history
            ]
        )


        prompt = f"""
        You are an AI business automation assistant.

        Conversation history:
        {conversation}

        User request:
        {user_input}

        Provide a helpful answer.
        """


        complete_response = ""


        for chunk in ollama_client.stream_generate(
            prompt
        ):

            complete_response += chunk

            yield chunk



        # Save complete response after streaming finishes.
        memory.add_message(
            "assistant",
            complete_response
        )



# Shared agent instance.
agent = AIAgent()

