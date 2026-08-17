"""
API documentation helpers.

Centralizes OpenAPI metadata
and documentation examples.
"""


API_DESCRIPTION = """
# AI Agent Automation API

Production-ready AI agent platform.

## Features

- AI reasoning with Ollama (offline fallback included)
- Per-session persistent conversation memory
- Long-term memory (facts and preferences)
- Secure advanced mathematics calculator
- Statistics, date/time and file analysis tools
- RAG knowledge base with local embeddings
- Planner-based tool routing
- Streaming responses (SSE)
- Structured responses

## Main Endpoint

`POST /api/v1/agent`

Send a user request and receive
an AI-generated response.

## Security

When `API_KEY` is configured, all `/api/v1`
endpoints require an `X-API-Key` header.
"""


TAGS_METADATA = [
    {
        "name": "Agent",
        "description": "AI agent execution and streaming endpoints."
    },
    {
        "name": "Sessions",
        "description": "Conversation session, message and memory management."
    },
    {
        "name": "Knowledge",
        "description": "RAG knowledge base ingestion and search."
    },
]
