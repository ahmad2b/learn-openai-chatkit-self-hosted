"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowUp, Loader2 } from "lucide-react";
import { useCallback, useRef, useState } from "react";

interface ChatInputProps {
	onMessageSent: (message: string) => Promise<void>;
	className?: string;
}

export function ChatInput({ onMessageSent, className }: ChatInputProps) {
	const [message, setMessage] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const inputRef = useRef<HTMLInputElement>(null);

	const sendMessage = useCallback(
		async (text: string) => {
			if (!text.trim()) return;

			setIsLoading(true);
			setError(null);

			try {
				// Send the message - ChatKit will handle thread creation and state transitions
				await onMessageSent(text);

				// Clear the input
				setMessage("");
			} catch (err) {
				console.error("Error sending message:", err);
				setError(err instanceof Error ? err.message : "Failed to send message");
			} finally {
				setIsLoading(false);
			}
		},
		[onMessageSent]
	);

	const handleSubmit = useCallback(
		(e: React.FormEvent) => {
			e.preventDefault();
			sendMessage(message);
		},
		[message, sendMessage]
	);

	const handleKeyDown = useCallback(
		(e: React.KeyboardEvent) => {
			if (e.key === "Enter" && !e.shiftKey) {
				e.preventDefault();
				sendMessage(message);
			}
		},
		[message, sendMessage]
	);

	return (
		<div className={className}>
			<form
				onSubmit={handleSubmit}
				className="flex gap-2"
			>
				<div className="flex-1 relative">
					<Input
						ref={inputRef}
						value={message}
						onChange={(e) => setMessage(e.target.value)}
						onKeyDown={handleKeyDown}
						placeholder="Ask me anything..."
						disabled={isLoading}
						className="pr-12 bg-transparent border-none ring-0 ring-offset-0 focus:ring-0 focus:ring-offset-0 focus-visible:ring-0 focus-visible:ring-offset-0 outline-none focus-visible:outline-none focus-visible:border-0 shadow-none"
					/>
					{error && (
						<div className="absolute -bottom-6 left-0 text-sm text-red-500 mt-1">
							{error}
						</div>
					)}
				</div>
				<Button
					type="submit"
					disabled={isLoading || !message.trim()}
					size="icon"
					className="shrink-0 rounded-full"
				>
					{isLoading ? (
						<Loader2 className="h-4 w-4 animate-spin" />
					) : (
						<ArrowUp className="h-4 w-4" />
					)}
				</Button>
			</form>
		</div>
	);
}
