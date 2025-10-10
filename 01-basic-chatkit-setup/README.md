# Step 1: Basic ChatKit Setup

This step demonstrates the fundamental integration flow for ChatKit's advanced (self-hosted) approach. We'll build a minimal chat interface that connects a Next.js frontend to a FastAPI backend running our agent.

## Architecture Overview

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│   Next.js       │ ──────────────────► │   FastAPI       │
│   Frontend      │                     │   Backend       │
│                 │ ◄────────────────── │                 │
│ - ChatKit React │    Server-Sent      │ - ChatKit Server│
│ - UI Components │      Events         │ - OpenAI Agents │
│ - Theming       │                     │ - Memory Store  │
└─────────────────┘                     └─────────────────┘
                                              │
                                              ▼
                                       ┌─────────────────┐
                                       │   OpenAI API    │
                                       │   (GPT-4.1-mini)│
                                       └─────────────────┘
```

**Data Flow:**

1. User types message in ChatKit UI (frontend)
2. Frontend sends HTTP request to `/chatkit` endpoint (backend)
3. Backend processes request through ChatKit server
4. ChatKit server streams agent responses back via Server-Sent Events
5. Frontend displays streaming responses in real-time

## Features Implemented

- ✅ **Minimal Chat Interface**: Clean, responsive chat UI with ChatKit
- ✅ **Basic Agent**: conversational Agent using OpenAI Agents SDK
- ✅ **Thread Persistence**: In-memory storage for conversation history
- ✅ **Real-time Streaming**: Server-Sent Events for live responses
- ✅ **CORS Configuration**: Proper cross-origin setup for development

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+ and uv
- OpenAI API key with access to GPT-4.1-mini

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### 2. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# The default values should work for local development
# NEXT_PUBLIC_CHATKIT_API_URL=http://127.0.0.1:8000/chatkit
# NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=domain_pk_local_dev
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**

```
INFO:     Will watch for changes in these directories: ['backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

**Expected Output:**

```
▲ Next.js 15.5.4
- Local:        http://localhost:3000
- Environments: .env.local
✓ Ready in 2.1s
```

## Testing the Setup

### 1. Health Check

Test that the backend is running:

```bash
curl http://127.0.0.1:8000/health
```

**Expected Response:**

```json
{ "status": "ok" }
```

### 2. Frontend Access

Open http://localhost:3000 in your browser. You should see:

- A chat interface with a greeting message
- A prompt suggestion: "What can you do?"
- A text input field at the bottom

### 3. Test Chat Interaction

1. Click "What can you do?" or type your own message
2. The agent should respond with a helpful message
3. Responses should stream in real-time
4. Conversation history persists during the session

## Code Structure

### Backend (`backend/`)

```
app/
├── main.py          # FastAPI app with CORS and ChatKit endpoint
├── chat.py          # ChatKit server implementation with agent
└── memory_store.py  # In-memory storage for threads/messages
```

**Key Components:**

- `MyChatServer`: Extends `ChatKitServer` to handle user messages
- `MyAgentContext`: Provides thread/store context to the agent
- `MemoryStore`: Simple in-memory persistence (threads, messages)

### Frontend (`frontend/`)

```
app/
├── page.tsx         # Main page with ChatKitPanel
└── layout.tsx       # App layout

components/
└── ChatKitPanel.tsx # ChatKit React integration
```

**Key Features:**

- `useChatKit` hook for ChatKit state management
- Custom theming with color scheme and accent colors
- Configurable start screen with greeting and prompts

## Troubleshooting

### Backend Won't Start

**Issue:** `ModuleNotFoundError: No module named 'chatkit'`
**Solution:** Use `uv run` to ensure virtual environment activation:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Shows Connection Error

**Issue:** ChatKit can't connect to backend
**Solutions:**

1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_CHATKIT_API_URL` in frontend `.env`
3. Ensure CORS is properly configured in backend

### Agent Not Responding

**Issue:** Chat messages don't get responses
**Solutions:**

1. Verify `OPENAI_API_KEY` is set in backend `.env`
2. Check OpenAI API key has access to GPT-4.1-mini
3. Look for errors in backend terminal output

### Port Already in Use

**Issue:** Port 3000 or 8000 already occupied
**Solutions:**

1. Kill existing processes: `lsof -ti:3000 | xargs kill -9`
2. Use different ports and update environment variables

## What You Learned

By completing this step, you understand:

- **ChatKit Architecture**: How frontend and backend communicate
- **Agent Integration**: Using OpenAI Agents SDK with ChatKit
- **Streaming Responses**: Real-time message delivery via SSE
- **State Management**: Thread and message persistence
- **Development Setup**: Running full-stack ChatKit applications

## Next Steps

In [Step 2](../02-theming-customization/), you'll learn how to customize the ChatKit UI with advanced theming, colors, and component styling.</content>
<parameter name="filePath">d:\code\learn-openai-chatkit-self-hosted\01-basic-chatkit-setup\README.md
