import { cn } from "@/lib/utils";
import {
	Bot,
	User,
	FileText,
	BookOpen,
	ChevronDown,
	ChevronUp,
} from "lucide-react";
import { useState } from "react";

interface ChatMessageProps {
	role: "user" | "assistant";
	content: string;
	timestamp?: Date;
	sources?: string[];
	contextes?: string[];
}

export default function ChatMessage({
	role,
	content,
	timestamp,
	sources = [],
	contextes = [],
}: ChatMessageProps) {
	const [showContexts, setShowContexts] = useState(false);

	return (
		<div
			className={cn(
				"flex w-full gap-4 animate-in fade-in-50 duration-300 py-6",
				role === "user" ? "bg-gray-50" : "bg-white"
			)}
		>
			<div className="max-w-3xl mx-auto w-full flex gap-4 px-4">
				<div className="shrink-0">
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
						{role === "user" ? "Vous" : "Assistant"}
					</div>

					{/* Contenu principal */}
					<div className="whitespace-pre-wrap leading-relaxed">
						{content}
					</div>

					{/* Sources - Affichage sous forme de badges */}
					{role === "assistant" && sources.length > 0 && (
						<div className="mt-4 pt-3 border-t border-border">
							<div className="flex items-center gap-2 mb-2">
								<BookOpen className="w-4 h-4 text-primary" />
								<span className="text-xs font-semibold text-primary uppercase tracking-wide">
									Sources utilisées
								</span>
							</div>
							<div className="flex flex-wrap gap-2">
								{sources.map((source, idx) => (
									<div
										key={idx}
										className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-primary/10 text-primary rounded-full text-xs font-medium border border-primary/20 hover:bg-primary/20 transition-colors"
									>
										<FileText className="w-3 h-3" />
										<span>{source}</span>
									</div>
								))}
							</div>

							{/* Contextes - Section dépliable */}
							{contextes.length > 0 && (
								<div className="mt-3">
									<button
										onClick={() =>
											setShowContexts(!showContexts)
										}
										className="flex items-center gap-2 text-xs text-muted-foreground hover:text-foreground transition-colors"
									>
										{showContexts ? (
											<ChevronUp className="w-3 h-3" />
										) : (
											<ChevronDown className="w-3 h-3" />
										)}
										<span>
											{showContexts ? "Masquer" : "Voir"}{" "}
											les extraits ({contextes.length})
										</span>
									</button>

									{showContexts && (
										<div className="mt-2 space-y-2">
											{contextes.map((contexte, idx) => (
												<div
													key={idx}
													className="p-3 bg-muted/50 rounded-lg text-xs text-muted-foreground border border-border"
												>
													<div className="flex items-start gap-2">
														<span className="shrink-0 w-5 h-5 rounded-full bg-primary/20 text-primary flex items-center justify-center text-[10px] font-bold">
															{idx + 1}
														</span>
														<p className="flex-1 italic leading-relaxed">
															"{contexte}"
														</p>
													</div>
												</div>
											))}
										</div>
									)}
								</div>
							)}
						</div>
					)}

					{/* Timestamp */}
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
