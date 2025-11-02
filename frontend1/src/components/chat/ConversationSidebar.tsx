import React from "react";
import { Button } from "../ui/button";
import { Menu, MessageSquare, Plus } from "lucide-react";
import { ScrollArea } from "../ui/scroll-area";
import { cn } from "@/lib/utils";

interface Conversation {
	id: string;
	title: string;
	timestamp: Date;
}

interface ConversationSidebarProps {
	conversations: Conversation[];
	activeId: string | null;
	onSelect: (id: string) => void;
	onNew: () => void;
}

export default function ConversationSidebar({
	conversations,
	activeId,
	onSelect,
	onNew,
}: ConversationSidebarProps) {
	return (
		<div className="w-64 h-full bg-[hsl(var(--sidebar-bg))] border-r border-border flex flex-col">
			<div className="p-3 border-b border-border flex items-center gap-2">
				<Button variant="ghost" size="icon" className="h-9 w-9">
					<Menu className="h-4 w-4" />
				</Button>
				<Button
					onClick={onNew}
					variant="ghost"
					size="icon"
					className="h-9 w-9 ml-auto"
				>
					<Plus className="h-4 w-4" />
				</Button>
			</div>

			<ScrollArea className="flex-1">
				<div className="p-2 space-y-1">
					{conversations.map((conv) => (
						<button
							key={conv.id}
							onClick={() => onSelect(conv.id)}
							className={cn(
								"w-full text-left px-3 py-2.5 rounded-lg transition-all duration-200 flex items-start gap-2 group",
								activeId === conv.id
									? "bg-[hsl(var(--sidebar-hover))]"
									: "hover:bg-[hsl(var(--sidebar-hover))]"
							)}
						>
							<MessageSquare className="h-4 w-4 mt-0.5 shrink-0 opacity-60" />
							<div className="flex-1 min-w-0">
								<p className="text-sm truncate">{conv.title}</p>
							</div>
						</button>
					))}
				</div>
			</ScrollArea>
		</div>
	);
}
