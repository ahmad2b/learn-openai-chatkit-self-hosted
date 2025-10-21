# Step 03: Implementing Interactive Widgets

In this step, we build interactive widgets from our self-hosted ChatKit backend and handle basic client-side actions. We start with static widgets, move to streaming updates, and end with instant UI responses—all without complex server-side state.

## What We Build

- **Static widgets:** Simple product cards with buttons that render in the chat.
- **Streaming widgets:** Progressive widget updates from backend tools for dynamic content.
- **Client-side actions:** Immediate UI feedback from widget clicks, like adding to a local cart.

## Phase-by-Phase Guide

### Phase 1: Static Widgets

**Goal:** Get widgets rendering in the chat UI.

**What we do:** Uncomment the Phase 1 code in `backend/app/chat.py` to return a static product card when we say "show products".

**Files:** `backend/app/chat.py` (respond method), `frontend/components/ChatKitPanel.tsx`.

**Test:** Run backend and frontend, prompt "show products"—see the card with button.

### Phase 2: Streaming Widgets

**Goal:** Make widgets update live as they're built.

**What we do:** Use the `@function_tool` in `backend/app/chat.py` (already added) to stream a product card in pieces via the agent.

**Files:** `backend/app/chat.py` (tool and agent setup), `frontend/app/page.tsx`.

**Test:** Prompt "show products"—watch the widget build incrementally.

### Phase 3: Client-Side Actions

**Goal:** Handle widget clicks instantly in the browser.

**What we do:** Add `widgets.onAction` in `frontend/app/page.tsx` to update a local cart on "add to cart" clicks.

**Files:** `frontend/app/page.tsx`, `frontend/components/ChatKitPanel.tsx`.

**Test:** Click "Add to Cart"—see instant UI update, no backend call.

## Quick Setup

Backend:

```bash
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Checklist

- [ ] Static card renders
- [ ] Streaming updates work
- [ ] Client actions update UI instantly

## Test Prompts

- "Show me products"
- "Add to cart" (Phase 3)

## Links

- [Widget Builder](https://widgets.chatkit.studio/)
- [Server Docs](https://openai.github.io/chatkit-python/server/#widgets)
