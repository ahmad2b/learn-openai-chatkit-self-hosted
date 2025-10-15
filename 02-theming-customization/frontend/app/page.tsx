"use client";

import { WelcomeScreen } from "@/components/WelcomeScreen";
import { ChatKit, ChatKitOptions, useChatKit } from "@openai/chatkit-react";
import { useCallback, useState } from "react";

const apiUrl =
	process.env.NEXT_PUBLIC_CHATKIT_API_URL?.trim() ||
	"http://127.0.0.1:8000/chatkit";
const domainKey =
	process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY?.trim() || "domain_pk_local_dev";

export default function Home() {
	// Track if user has an active conversation (for showing/hiding custom overlay)
	const [hasActiveThread, setHasActiveThread] = useState(false);

	// Configure ChatKit with theme and callbacks
	const chatKitOptions = {
		api: {
			url: apiUrl,
			domainKey,
		},
		theme: {
			// Comprehensive theming demonstrating all built-in ChatKit options
			colorScheme: "light",
			color: {
				accent: {
					primary: "#343434",
					level: 1,
				},
			},
			radius: "pill" as const,
			density: "normal" as const,
			typography: {
				baseSize: 16,
				fontFamily:
					"system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
				fontFamilyMono:
					"'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
			},
		} satisfies ChatKitOptions["theme"],
		// OFFICIAL APPROACH: Use initialThread to restore from localStorage
		// ChatKit will validate if the thread exists and fire onThreadChange accordingly
		initialThread:
			typeof window !== "undefined"
				? localStorage.getItem("chatkit-thread-id") || null
				: null,
		startScreen: {
			greeting: "How can I help you today?",
			prompts: [
				{
					label: "What can you do?",
					prompt: "What can you do?",
				},
			],
		},
		composer: {
			placeholder: "Ask anything....",
		},
		onError: ({ error }: { error: unknown }) => {
			console.error("ChatKit error", error);
		},
		onThreadChange: ({ threadId }: { threadId: string | null }) => {
			// ChatKit's built-in callback - track when conversations start/end
			const hasThread = !!threadId;
			setHasActiveThread(hasThread);

			// Persist thread state to localStorage
			if (typeof window !== "undefined") {
				if (threadId) {
					localStorage.setItem("chatkit-thread-id", threadId);
				} else {
					localStorage.removeItem("chatkit-thread-id");
				}
			}
		},
	};

	// Initialize ChatKit with our configuration
	const chatkit = useChatKit(chatKitOptions);

	// Handle sending messages from our custom UI
	const handleMessageSent = useCallback(
		async (message: string) => {
			try {
				// Use ChatKit's imperative method to send the message
				await chatkit.sendUserMessage({ text: message });
			} catch (error) {
				console.error("Error sending message:", error);
				throw error;
			}
		},
		[chatkit]
	);

	return (
		<main className="h-screen w-full relative">
			{/* Main Chat Interface with Custom Overlay */}
			<div className="relative flex h-[100vh] w-full flex-col overflow-hidden">
				{/* Custom UI overlay - only show when no active conversation */}
				{!hasActiveThread ? (
					<div className="absolute inset-0 z-10 flex items-center justify-center">
						<WelcomeScreen onMessageSent={handleMessageSent} />
					</div>
				) : null}

				{/* ChatKit - always rendered, becomes visible when overlay disappears */}
				<ChatKit
					control={chatkit.control}
					className="block h-full w-full"
				/>
			</div>
		</main>
	);
}
