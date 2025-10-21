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

- `app/page.tsx` - Main page with ChatKit integration, inline theming, and overlay welcome screen
- `components/WelcomeScreen.tsx` - Custom branded welcome screen overlay
- `components/ChatInput.tsx` - Styled input component for the welcome screen
- `app/layout.tsx` - App layout and global styles

## Customization Tips

- Adjust starter prompts, greeting text, and placeholder copy in [`app/page.tsx`](app/page.tsx).
- Update the theme configuration directly in [`app/page.tsx`](app/page.tsx) to integrate with your product analytics or storage.

## References

- [ChatKit JavaScript Library](http://openai.github.io/chatkit-js/)
- [Advanced Self-Hosting Examples](https://github.com/openai/openai-chatkit-advanced-samples)
