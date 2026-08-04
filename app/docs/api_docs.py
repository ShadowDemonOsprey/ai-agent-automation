"""
API documentation helpers.

Centralizes OpenAPI metadata
and documentation examples.
"""


API_DESCRIPTION = """
# AI Agent Automation API

Production-ready AI agent system.

## Features

- AI reasoning with Ollama
- Conversation memory
- Tool execution
- Planner-based decisions
- Structured responses

## Main Endpoint

`POST /api/v1/agent`

Send a user request and receive
an AI-generated response.
"""


TAGS_METADATA = [
    {
        "name": "Agent",
        "description": "AI agent execution endpoints."
    }
]

