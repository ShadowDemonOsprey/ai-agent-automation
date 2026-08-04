# AI Agent Automation Platform

A production-oriented AI Agent platform built with Python, FastAPI, Ollama, and modern AI engineering practices.

This project demonstrates professional Applied AI Engineer skills:

- LLM application development
- AI Agent architecture
- Planning and reasoning systems
- Memory management
- Tool execution
- FastAPI backend engineering
- Automated testing

---

# Project Status

## Phase 1 — Foundation ✅

Completed:

- Project structure
- Configuration management
- Logging system
- Error handling
- FastAPI API structure
- Testing framework

---

## Phase 2 — Agent Architecture ✅

Completed:

- AI Agent core architecture
- Planner system
- Memory system
- Agent state management
- Tool execution framework

---

## Phase 3 — Local LLM Integration ✅

Completed:

- Ollama integration
- TinyLlama local LLM support
- Agent pipeline
- Memory integration
- FastAPI API integration

---

# Phase 4.1 — Streaming AI Responses ✅

Completed:

- ChatGPT-style streaming responses
- Ollama streaming support
- Streaming agent execution
- Server Sent Events (SSE)
- Streaming API endpoint
- Streaming test coverage

## Streaming Architecture

```
User
 |
 |
FastAPI SSE Endpoint
 |
 |
AI Agent stream_run()
 |
 |
Ollama stream_generate()
 |
 |
Local Ollama LLM
 |
 |
Token Chunks
```

## Streaming Endpoint

```
GET /api/v1/chat/stream
```

## Example Request

```
GET /api/v1/chat/stream?message=hello
```

## Response Format

```
data: Hello

data: How

data: can

data: I help?
```

---

# System Architecture

```
                    User
                      |
                      |
                 FastAPI API
                      |
                      |
                  AI Agent
                      |
          -------------------------
          |                       |
       Planner                 Memory
          |
          |
      Tool Router
          |
    ----------------
    |              |
 Calculator       LLM
                    |
                  Ollama
                    |
                TinyLlama
```

---

# Technology Stack

## Backend

- Python 3.13
- FastAPI
- Pydantic v2
- SQLAlchemy
- SQLite


## AI / LLM

- Ollama
- TinyLlama
- AI Agent Architecture


## Testing

- Pytest
- FastAPI TestClient

---

# Current Features

## AI Agent

✅ User request processing  
✅ Planning and decision making  
✅ Tool execution  
✅ Structured agent responses  


## Memory

✅ Conversation history  
✅ Agent context management  


## LLM

✅ Local LLM inference  
✅ Ollama integration  
✅ Streaming responses  


## API

✅ FastAPI backend  
✅ REST API endpoints  
✅ Server Sent Events streaming  

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

---

# Running Tests

Run complete test suite:

```bash
pytest
```

Current test status:

```
26 tests passing
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
    "message": "Calculate 25 times 40"
}
```

---

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

---

# Development Roadmap

## Phase 4.2 — Conversation Session Management

Planned:

- Multiple conversations
- Session database
- Message history


## Phase 4.3 — Persistent Memory System

Planned:

- Permanent user memory
- Memory database
- Memory retrieval


## Phase 4.4 — RAG Knowledge System

Planned:

- Document upload
- Text chunking
- Embeddings
- Vector database
- Knowledge retrieval


## Phase 4.5 — Advanced Agent Tools

Planned:

- Calculator improvements
- File analyzer
- Date/time tools
- Tool routing


## Phase 4.6+ — Production Features

Planned:

- Database migration
- Authentication
- Docker deployment
- React frontend
- Monitoring
- Production documentation

---

# Project Goal

Build a complete production-ready AI Agent platform demonstrating:

- LLM engineering
- AI Agent workflows
- RAG pipelines
- Tool calling
- Backend architecture
- Production AI system design

---

# License

Portfolio project created for Applied AI Engineer development.