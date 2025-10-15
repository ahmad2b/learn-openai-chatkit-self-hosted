# Step 2: Make ChatKit Your Own 🎨

**Transform ChatKit from a generic chat widget into a branded, themed experience that matches your app's personality.**

## What We Built

We created a custom welcome screen that replaces ChatKit's default start screen with our own branded experience, complete with themes and smooth transitions.

## Quick Start (5 minutes)

### Backend (Same as Step 1)

```bash
cd 02-theming-customization/backend
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd ../frontend
npm install && npm run dev
```

Visit `http://localhost:3000` and see our custom welcome screen! Send a message to see the smooth transition.

## Our Approach

We wanted to completely replace ChatKit's default start screen with our own branded experience. The challenge was that ChatKit's imperative methods (like `sendUserMessage`) aren't available until ChatKit is mounted and initialized.

**We chose an overlay approach:** ChatKit is always mounted and ready underneath, but our custom UI sits on top until the conversation begins. This ensures ChatKit's methods are always available when we need them.

```tsx
// ChatKit is ALWAYS mounted and ready
<ChatKit control={chatkit.control} />;

// Our custom UI sits on top as an overlay
{
	!hasActiveThread && (
		<div className="absolute inset-0 z-10">
			<WelcomeScreen onMessageSent={handleMessageSent} />
		</div>
	);
}
```

## ChatKit Limitations

ChatKit's built-in theming is powerful but has limitations:

- **Start Screen**: Only supports greeting text and predefined prompts—no full custom layouts (e.g., centered inputs, branding elements).
- **UI Customization**: Limited to theme properties; for complete control, use an overlay as demonstrated here.

This step shows how to work within these constraints while achieving branded experiences.

## Key Files

```
frontend/app/page.tsx           # Main logic: inline theme + overlay + ChatKit
frontend/components/
├── WelcomeScreen.tsx           # Our custom landing page
└── ChatInput.tsx               # Styled input component
```

## Try It Out

1. **Custom Landing**: See our branded welcome screen on load
2. **Smooth Transition**: Send a message and watch the overlay disappear

## Design Example

### 💼 Professional Corporate

Clean, trustworthy design for startup and business apps with pill-shaped elements, and system fonts.

## Implementation Highlights

- **Inline Theming**: Comprehensive theme configuration directly in ChatKit options
- **Official ChatKit APIs**: Uses `initialThread` + `onThreadChange` for production-ready state management
- **Stale-Safe localStorage**: ChatKit validates thread existence before showing conversations
- **Responsive**: Works perfectly on mobile and desktop

````tsx
// Everything in one file: page.tsx
export default function Home() {
  // 1. Theme state management
  const [currentTheme, setCurrentTheme] = useState<ThemeKey>("professional");

  // 2. Conversation state tracking
  const [hasActiveThread, setHasActiveThread] = useState(() => {
    return !!localStorage.getItem("chatkit-thread-id");
  });

  // 3. ChatKit configuration with theme
  const chatKitOptions = {
    theme: selectedTheme.theme,
    onThreadChange: ({ threadId }) => {
      // Track conversation state
      setHasActiveThread(!!threadId);
    }
  };

  // 4. Initialize ChatKit
  const chatkit = useChatKit(chatKitOptions);

  // 5. Render with overlay
  return (
    <div className="relative">
      {!hasActiveThread && (
        <div className="absolute inset-0 z-10">
          <WelcomeScreen onMessageSent={handleMessageSent} />
        </div>
      )}
      <ChatKit control={chatkit.control} />
    </div>
  );
}
## State Management

**Production-Ready Approach**: We use ChatKit's official APIs to avoid stale localStorage issues.

```typescript
// ✅ PRODUCTION APPROACH: Let ChatKit be the source of truth
const [hasActiveThread, setHasActiveThread] = useState(false); // Start false

const chatKitOptions = {
  // Official: Use initialThread - ChatKit validates thread existence
  initialThread: localStorage.getItem("chatkit-thread-id") || null,
  onThreadChange: ({ threadId }) => {
    // SOURCE OF TRUTH: ChatKit tells us if thread actually exists
    const hasThread = !!threadId;
    setHasActiveThread(hasThread);
    // Only persist valid threads
    if (threadId) {
      localStorage.setItem("chatkit-thread-id", threadId);
    } else {
      localStorage.removeItem("chatkit-thread-id");
    }
  }
};
```

**Why This Works in Production:**
- **No Stale State**: If stored thread doesn't exist, ChatKit fires `onThreadChange(null)`
- **Server Validation**: ChatKit checks with backend before showing conversations
- **Automatic Cleanup**: Invalid threads are automatically removed from localStorage
- **Race-Condition Safe**: ChatKit's callbacks happen after proper initialization

## Testing Our Implementation

1. **Custom Empty Screen**:
   - Verify overlay appears instantly on page load
   - Test custom composer sends messages correctly
   - Confirm smooth transition to ChatKit when conversation starts

2. **Theme Integration**:
   - Verify the customized theme applies to ChatKit component (not custom overlay)

3. **State Persistence**:
   - Send a message to start conversation
   - Refresh page - should return to ChatKit (thread validated by backend)
   - Stop backend and refresh - should show custom overlay (stale thread detected)
   - Clear localStorage to reset to custom overlay

4. **Responsive Design**:
   - Test on different screen sizes
   - Verify overlay centers properly on mobile devices

## Production Considerations

**Thread State Management**: Our implementation uses ChatKit's official APIs to handle edge cases that would break simpler approaches:

- **Stale localStorage**: Old thread IDs from previous sessions/backends
- **Backend Restarts**: Threads that existed but are now gone
- **Multi-tab Sync**: Different tabs with conflicting thread states
- **Network Issues**: Failed connections that leave state inconsistent

**The Solution**: Use `initialThread` + `onThreadChange` - let ChatKit validate thread existence and be the source of truth for your UI state.

## What We Learned

✅ **Overlay Architecture**: Smart way to customize ChatKit without breaking functionality
✅ **Theme Configuration**: How to style ChatKit's built-in components
✅ **State Management**: Leveraging ChatKit's lifecycle callbacks
✅ **Component Integration**: Building custom UI that works with ChatKit's API
✅ **Transition Design**: Creating smooth UX flows between custom and native UI

## Next: Interactive Widgets

Ready for more? In [Step 3](../03-implementing-widgets/), we add interactive widgets that agents can render - buttons, forms, charts, and more - turning our chat into a dynamic app interface.</content>
<parameter name="filePath">d:\code\learn-openai-chatkit-self-hosted\02-theming-customization\README.md
````
