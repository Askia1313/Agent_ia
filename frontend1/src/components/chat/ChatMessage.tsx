import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";
import React from "react";

interface ChatMessageProps {
	role: "user" | "assistant";
	content: string;
	timestamp?: Date;
}

export default function ChatMessage({
	role,
	content,
	timestamp,
}: ChatMessageProps) {
	return (
		<div
			className={cn(
				"flex w-full gap-4 animate-in fade-in-50 duration-300 py-6",
				role === "user"
					? "bg-[hsl(var(--chat-user-bg))]"
					: "bg-transparent"
			)}
		>
			<div className="max-w-3xl mx-auto w-full flex gap-4 px-4">
				<div className="flex-shrink-0">
					<div
						className={cn(
							"w-8 h-8 rounded-full flex items-center justify-center",
							role === "user"
								? "bg-primary text-primary-foreground"
								: "bg-accent text-accent-foreground"
						)}
					>
						{role === "user" ? (
							<User className="w-5 h-5" />
						) : (
							<Bot className="w-5 h-5" />
						)}
					</div>
				</div>

				<div className="flex-1 min-w-0">
					<div className="text-sm font-medium mb-2">
						{role === "user" ? "You" : "Assistant"}
					</div>
					<div className="markdown-content text-[hsl(var(--chat-assistant-fg))]">
						{content}
					</div>
					{timestamp && (
						<p className="text-xs mt-2 text-muted-foreground">
							{timestamp.toLocaleTimeString([], {
								hour: "2-digit",
								minute: "2-digit",
							})}
						</p>
					)}
				</div>
			</div>
		</div>
	);
}
