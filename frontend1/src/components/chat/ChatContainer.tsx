import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";

interface Message {
	id: string;
	role: "user" | "assistant";
	content: string;
	timestamp: Date;
	sources?: string[];
	contextes?: string[];
}

interface ChatContainerProps {
	messages: Message[];
}

export default function ChatContainer({ messages }: ChatContainerProps) {
	const scrollRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		if (scrollRef.current) {
			scrollRef.current.scrollIntoView({ behavior: "smooth" });
		}
	}, [messages]);

	return (
		<div className="flex-1 overflow-y-auto">
			<div className="w-full min-h-full">
				{messages.length === 0 ? (
					<div className="flex items-center justify-center min-h-[calc(100vh-180px)] text-center px-4">
						<div className="space-y-3">
							<h2 className="text-3xl font-semibold">
								Comment puis-je vous aider ?
							</h2>
							<p className="text-muted-foreground">
								Posez-moi n'importe quelle question pour
								commencer.
							</p>
						</div>
					</div>
				) : (
					<>
						{messages.map((message) => (
							<ChatMessage
								key={message.id}
								role={message.role}
								content={message.content}
								timestamp={message.timestamp}
								sources={message.sources}
								contextes={message.contextes}
							/>
						))}
					</>
				)}
				<div ref={scrollRef} />
			</div>
		</div>
	);
}
