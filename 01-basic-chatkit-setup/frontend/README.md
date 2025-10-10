# ChatKit Frontend

Next.js frontend with ChatKit React components for conversational Agent interfaces.

## Overview

This frontend provides:

- ChatKit React integration for chat UI
- Basic theming and customization
- Connection to self-hosted ChatKit backend
- Responsive design with Tailwind CSS

## Quick Start

```bash
# Install dependencies
npm install

# Copy environment file (optional - defaults should work)
cp .env.example .env.local

# Run the development server
npm run dev
```

Visit `http://localhost:3000` to see the chat interface.

## Configuration

Environment variables in `.env.local`:

- `NEXT_PUBLIC_CHATKIT_API_URL` - Backend API URL (default: http://127.0.0.1:8000/chatkit)
- `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` - Domain key for ChatKit in production (default: domain_pk_local_dev)

## Architecture

- `app/page.tsx` - Main page with ChatKitPanel component
- `components/ChatKitPanel.tsx` - ChatKit React integration with basic theming
- `app/layout.tsx` - App layout and global styles

## Customization Tips

- Adjust starter prompts, greeting text, and placeholder copy in [`components/ChatKitPanel.tsx`](components/ChatKitPanel.tsx).
- Update the theme defaults or event handlers inside [`components/ChatKitPanel.tsx`](components/ChatKitPanel.tsx) to integrate with your product analytics or storage.

## References

- [ChatKit JavaScript Library](http://openai.github.io/chatkit-js/)
- [Advanced Self-Hosting Examples](https://github.com/openai/openai-chatkit-advanced-samples)
