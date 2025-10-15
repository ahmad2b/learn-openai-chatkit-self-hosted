"use client";

import { ChatInput } from "./ChatInput";

interface WelcomeScreenProps {
	onMessageSent: (message: string) => Promise<void>;
}

export function WelcomeScreen({ onMessageSent }: WelcomeScreenProps) {
	return (
		<div
			className={`w-full h-full flex items-center justify-center bg-background`}
		>
			<div className="w-full px-6">
				<div className="max-w-3xl mx-auto text-center mt-24">
					{/* Large centered heading */}
					<h1
						className={`text-3xl md:text-4xl font-semibold text-center text-foreground mb-12`}
					>
						What&apos;s on the agenda today?
					</h1>

					{/* Pill-style search bar container */}
					<div className="relative">
						<div
							className={`mx-auto w-full max-w-3xl flex items-center bg-input border-input shadow-input  rounded-full shadow-inner px-4 py-3`}
						>
							{/* ChatInput - styled to look like placeholder inside pill */}
							<div className="flex-1">
								<ChatInput
									onMessageSent={onMessageSent}
									className="w-full bg-transparent"
								/>
							</div>
						</div>
					</div>

					{/* Footer small text */}
					<div className="mt-12 text-center">
						<p className={`text-sm`}>Powered by OpenAI ChatKit</p>
					</div>
				</div>
			</div>
		</div>
	);
}
