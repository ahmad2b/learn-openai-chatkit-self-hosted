# ChatKit Backend

FastAPI backend implementing a ChatKit server for conversational Agent agents.

## Overview

This backend provides:

- ChatKit-compatible API endpoint (`/chatkit`) for streaming conversations
- Custom agent implementation using OpenAI Agents SDK
- In-memory conversation storage (development only)
- Health check endpoint

## Quick Start

```bash
# Install dependencies
uv sync

# Copy environment file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /chatkit` - Main ChatKit endpoint for conversations
- `GET /health` - Health check

## Architecture

- `app/main.py` - FastAPI application with CORS setup
- `app/chat.py` - ChatKit server implementation with agent logic
- `app/memory_store.py` - In-memory storage for threads and messages
