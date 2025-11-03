import React, { useState } from "react";
import { Button } from "../ui/button";
import { ArrowUp } from "lucide-react";
import { Textarea } from "../ui/textarea";

interface ChatInputProps {
	onSend: (message: string) => void;
	disabled?: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
	const [message, setMessage] = useState("");

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		if (message.trim() && !disabled) {
			onSend(message);
			setMessage("");
		}
	};

	const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			handleSubmit(e);
		}
	};

	return (
		<form onSubmit={handleSubmit} className="w-full">
			<div className="relative">
				<Textarea
					value={message}
					onChange={(e) => setMessage(e.target.value)}
					onKeyDown={handleKeyDown}
					placeholder="Comment puis-je vous aider ?"
					disabled={disabled}
					className="min-h-[60px] max-h-[200px] resize-none rounded-2xl border-input bg-muted pr-12 text-foreground placeholder:text-muted-foreground"
					rows={1}
				/>
				<Button
					type="submit"
					size="icon"
					disabled={!message.trim() || disabled}
					className="absolute bottom-2 right-2 h-8 w-8 rounded-lg bg-primary hover:bg-primary/90 transition-all disabled:opacity-30"
				>
					<ArrowUp className="h-4 w-4" />
				</Button>
			</div>
		</form>
	);
}
