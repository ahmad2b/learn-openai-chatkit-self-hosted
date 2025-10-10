import { ChatKitPanel } from "@/components/ChatKitPanel";

export default function Home() {
	return (
		<main className="flex min-h-screen flex-col items-center justify-center  px-6 py-6">
			<div className="mx-auto w-full max-w-7xl">
				<ChatKitPanel />
			</div>
		</main>
	);
}
