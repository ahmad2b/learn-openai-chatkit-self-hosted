"use client";

import { ChatKit, ChatKitOptions, useChatKit } from "@openai/chatkit-react";

type ChatKitPanelProps = {
	onResponseEnd?: () => void;
	theme?: Partial<ChatKitOptions>;
};

const apiUrl =
	process.env.NEXT_PUBLIC_CHATKIT_API_URL?.trim() ||
	"http://127.0.0.1:8000/chatkit";
const domainKey =
	process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY?.trim() || "domain_pk_local_dev";

const defaultTheme: ChatKitOptions["theme"] = {
	colorScheme: "light",
	color: {
		grayscale: {
			hue: 220,
			tint: 6,
			shade: -4,
		},
		accent: {
			primary: "#0f172a",
			level: 1,
		},
	},
	radius: "round",
};

export function ChatKitPanel({ onResponseEnd, theme }: ChatKitPanelProps = {}) {
	const defaultOptions = {
		api: {
			url: apiUrl,
			domainKey,
		},
		theme: defaultTheme,
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
			placeholder: "Ask anything...",
		},
		onResponseEnd: () => {
			onResponseEnd?.();
		},
		onError: ({ error }: { error: unknown }) => {
			console.error("ChatKit error", error);
		},
	};

	const chatkit = useChatKit(
		theme ? { ...defaultOptions, ...theme } : defaultOptions
	);

	return (
		<div className="relative flex h-[100vh] w-full flex-col overflow-hidden bg-white transition-colors dark:bg-slate-900">
			<ChatKit
				control={chatkit.control}
				className="block h-full w-full"
			/>
		</div>
	);
}
