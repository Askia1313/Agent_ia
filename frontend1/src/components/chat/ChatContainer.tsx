import React, { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import { ScrollArea } from "../ui/scroll-area";

interface Message {
	id: string;
	role: "user" | "assistant";
	content: string;
	timestamp: Date;
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
		<ScrollArea className="flex-1">
			<div className="w-full">
				{messages.length === 0 ? (
					<div className="flex items-center justify-center h-screen text-center px-4">
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
							/>
						))}
					</>
				)}
				<div ref={scrollRef} />
			</div>
		</ScrollArea>
	);
}
