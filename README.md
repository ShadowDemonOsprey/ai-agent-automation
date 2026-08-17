# AI Agent Automation Platform

A production-oriented AI Agent platform built with Python, FastAPI, Ollama, ChromaDB, and modern AI engineering practices.

[![CI](https://github.com/ShadowDemonOsprey/ai-agent-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/ShadowDemonOsprey/ai-agent-automation/actions/workflows/ci.yml)

This project demonstrates professional Applied AI Engineer skills:

- LLM application development
- AI Agent architecture
- Planning and reasoning systems
- Persistent memory management
- Secure advanced mathematics
- RAG knowledge retrieval
- Tool execution
- FastAPI backend engineering
- Automated testing

---

# Project Status

## Phase 1 — Foundation ✅

Completed:

- Project structure
- Configuration management (Pydantic Settings)
- Structured JSON logging
- Error handling
- FastAPI API structure
- Testing framework

## Phase 2 — Agent Architecture ✅

Completed:

- AI Agent core architecture
- Planner system
- Memory system
- Agent state management
- Tool execution framework

## Phase 3 — Local LLM Integration ✅

Completed:

- Ollama integration
- TinyLlama local LLM support
- Agent pipeline
- Memory integration
- FastAPI API integration
- Offline fallback model (tests never need a live LLM)

## Phase 4.1 — Streaming AI Responses ✅

Completed:

- ChatGPT-style streaming responses
- Ollama streaming support
- Streaming agent execution
- Server Sent Events (SSE)
- Streaming API endpoint
- Streaming test coverage

## Phase 4.2 — Conversation Session Management ✅

Completed:

- Multiple conversations
- Session database
- Per-session message history
- Session create / list / retrieve / delete
- Session-scoped agent execution

## Phase 4.3 — Persistent Memory System ✅

Completed:

- Database-backed conversation history
- Long-term key-value memory
- Memory API (set / get / search / delete)
- Memory survives application restarts

## Phase 4.4 — RAG Knowledge System ✅

Completed:

- Document ingestion API
- Sentence-aware text chunking with overlap
- Local deterministic embeddings (offline, no downloads)
- ChromaDB vector store
- Similarity-based knowledge retrieval
- Knowledge search agent tool
- Knowledge API (ingest / list / search / delete)

## Phase 4.5 — Advanced Agent Tools ✅

Completed:

- Secure advanced mathematics calculator
  (replaces `eval()` with an AST whitelist evaluator)
- Statistics tool
- Date/time tool
- File analyzer tool
- Knowledge search tool
- Planner-based tool routing

## Phase 4.6 — Production Features ✅

Completed:

- Optional API key authentication
- Monitoring metrics endpoint
- Docker + docker-compose deployment
- Web chat UI
- Production documentation

---

# Code Quality & CI

Every change is validated automatically on GitHub (push to `main` and pull requests):

- **Tests**: `pytest` — the full suite (96 tests) runs against a fresh environment.
- **Lint**: `ruff` — import sorting and static error checks.

Run the same checks locally:

```bash
pip install -r requirements-dev.txt
ruff check .
pytest
```

---

# System Architecture

```
                       User
                         |
                 Web UI + FastAPI API
                         |
                     AI Agent
                         |
             -------------------------
             |            |           |
          Planner      Memory     Ollama LLM
             |            |        (fallback)
             |            |
         Tool Router    Database
             |           (SQLite)
    ---------|---------
    |        |        |
Calculator Statistics Knowledge
+ tools    + tools   + date/time
             |         + file analyzer
             |
         RAG Pipeline
             |
   Chunking -> Embeddings -> ChromaDB
```

---

# Technology Stack

## Backend

- Python 3.13
- FastAPI
- Pydantic v2
- SQLAlchemy 2 (async + sync)
- SQLite (aiosqlite)

## AI / LLM

- Ollama
- TinyLlama / llama3
- AI Agent Architecture
- RAG with local embeddings

## Storage

- SQLite for sessions, messages, memory, documents
- ChromaDB for the vector store

## Testing

- Pytest (96 tests, offline — no live LLM required)
- FastAPI TestClient

---

# Current Features

## AI Agent

✅ User request processing
✅ Planning and tool routing
✅ Tool execution
✅ Structured agent responses
✅ Streaming responses
✅ Offline fallback mode

## Mathematics (strong)

✅ Secure expression parser (no eval)
✅ Arithmetic, powers, roots
✅ Trigonometry and hyperbolic functions
✅ Logarithms and exponentials
✅ Factorials, GCD, LCM, combinations
✅ Gamma, error and special functions
✅ Constants (pi, e, tau, golden ratio)
✅ Natural notation (2pi, 5!, mod, ^)
✅ Descriptive statistics (mean, median, mode, variance, stddev, quartiles)

## Memory

✅ Per-session conversation history
✅ Persistent database storage
✅ Long-term key-value memory
✅ Memory search

## RAG

✅ Document ingestion
✅ Sentence-aware chunking
✅ Offline local embeddings
✅ ChromaDB vector search
✅ Knowledge agent tool

## API

✅ FastAPI backend
✅ REST API endpoints
✅ Server Sent Events streaming
✅ Optional API key auth
✅ Monitoring metrics
✅ Swagger docs
✅ Web chat UI

---

# Installation

## Create Environment

```bash
conda create -n ai-agent python=3.13
```

## Activate Environment

```bash
conda activate ai-agent
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment (optional)

```bash
cp .env.example .env
```

---

# Running the Application

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

API:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

Web Chat UI:

```
http://localhost:8000/ui
```

Monitoring Metrics:

```
http://localhost:8000/metrics
```

---

# Running Tests

Run complete test suite (no Ollama required):

```bash
pytest
```

Current test status:

```
96 tests passing
```

---

# API Examples

## Normal Agent Request

Endpoint:

```
POST /api/v1/agent
```

Request:

```json
{
    "message": "Calculate 25 * 40"
}
```

Response:

```json
{
    "agent": "Business Automation Agent",
    "response": "I used the calculator tool. The result of 25 * 40 is 1000.",
    "plan": {"action": "tool", "tool": "calculator"},
    "tool_used": "calculator",
    "tool_result": {"tool": "calculator", "expression": "25 * 40", "result": 1000},
    "memory": [...],
    "session_id": null
}
```

## Advanced Mathematics

```
POST /api/v1/agent
{"message": "Calculate sin(pi/2) + sqrt(144)"}
```

```
POST /api/v1/agent
{"message": "What is the mean of 4 8 15 16 23 42?"}
```

```
POST /api/v1/agent
{"message": "Calculate the square root of 144"}
```

## Session-Scoped Conversation

Create a session:

```
POST /api/v1/sessions
```

Chat within the session:

```json
{
    "message": "My name is Alex.",
    "session_id": "2c8e3a4b-..."
}
```

View message history:

```
GET /api/v1/sessions/2c8e3a4b-.../messages
```

## Long-Term Memory

```
POST /api/v1/sessions/2c8e3a4b-.../memory
{"key": "user_name", "value": "Alex"}
```

```
GET /api/v1/sessions/2c8e3a4b-.../memory
```

```
GET /api/v1/sessions/2c8e3a4b-.../memory/search?query=Alex
```

## Knowledge Base (RAG)

Ingest a document:

```
POST /api/v1/knowledge/documents
{
    "filename": "ml-notes.txt",
    "title": "Machine Learning Notes",
    "content": "Deep learning uses neural networks with many layers..."
}
```

Search the knowledge base:

```
POST /api/v1/knowledge/search
{"query": "neural networks", "top_k": 3}
```

Let the agent answer from knowledge:

```
POST /api/v1/agent
{"message": "search the knowledge base for neural networks"}
```

List / delete documents:

```
GET    /api/v1/knowledge/documents
DELETE /api/v1/knowledge/documents/{document_id}
```

## Streaming AI Chat

Endpoint:

```
GET /api/v1/chat/stream
```

Example:

```
GET /api/v1/chat/stream?message=Explain AI agents
```

Response:

```
data: AI

data: agents

data: are

data: systems...
```

## API Authentication (optional)

Set `API_KEY` in your `.env`. Then all `/api/v1` endpoints require:

```
X-API-Key: your-secret-key
```

---

# Docker Deployment

Build and run with docker-compose (includes Ollama):

```bash
docker compose up --build
```

- App: `http://localhost:8000`
- Ollama: `http://localhost:11434`

---

# Development Roadmap

Future improvements:

- Authentication with users and scopes
- Postgres + Alembic migrations
- React frontend
- Async Ollama client
- Multi-agent orchestration
- LangGraph-based state machines
- Full monitoring stack (Prometheus + Grafana)
- Model evaluation and prompt testing

---

# Project Goal

Build a complete production-ready AI Agent platform demonstrating:

- LLM engineering
- AI Agent workflows
- RAG pipelines
- Tool calling
- Strong mathematical tooling
- Backend architecture
- Production AI system design

---

# License

Portfolio project created for Applied AI Engineer development.
