import { useState } from "react";
import ChatContainer from "./ChatContainer";
import ChatInput from "./ChatInput";
import ConversationSidebar from "./ConversationSidebar";
import { useChatQuestion, useVerifierStatut } from "@/hooks/useRagApi";
//import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2 } from "lucide-react";

interface Message {
	id: string;
	role: "user" | "assistant";
	content: string;
	timestamp: Date;
	sources?: string[];
	contextes?: string[];
}

interface Conversation {
	id: string;
	title: string;
	timestamp: Date;
	messages: Message[];
}

export default function ChatUI() {
	const [conversations, setConversations] = useState<Conversation[]>([
		{
			id: "1",
			title: "Nouvelle conversation",
			timestamp: new Date(),
			messages: [],
		},
	]);
	const [activeConversationId, setActiveConversationId] =
		useState<string>("1");

	// Hook React Query pour poser des questions
	const { sendQuestion, isPending } = useChatQuestion({
		onSuccess: (response) => {
			console.log("Réponse reçue:", response);
		},
		onError: (error) => {
			console.error("Erreur:", error);
		},
	});

	// Hook pour vérifier le statut (optionnel)
	const { data: statusData } = useVerifierStatut(true, 60000); // Refetch toutes les 60s

	const activeConversation = conversations.find(
		(conv) => conv.id === activeConversationId
	);

	const handleSendMessage = async (content: string) => {
		if (!activeConversation) return;

		const userMessage: Message = {
			id: Date.now().toString(),
			role: "user",
			content,
			timestamp: new Date(),
		};

		// Message de chargement temporaire
		const loadingMessageId = (Date.now() + 1).toString();
		const loadingMessage: Message = {
			id: loadingMessageId,
			role: "assistant",
			content: "En train de réfléchir...",
			timestamp: new Date(),
		};

		// Ajouter les messages immédiatement
		setConversations((prev) =>
			prev.map((conv) =>
				conv.id === activeConversationId
					? {
							...conv,
							messages: [
								...conv.messages,
								userMessage,
								loadingMessage,
							],
							title:
								conv.messages.length === 0
									? content.slice(0, 50)
									: conv.title,
					  }
					: conv
			)
		);

		try {
			// Appeler l'API via React Query
			const response = await new Promise((resolve, reject) => {
				sendQuestion(
					{ question: content, nResultats: 3 },
					{
						onSuccess: resolve,
						onError: reject,
					}
				);
			});

			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			const ragResponse = response as any;

			// Construire la réponse
			let aiContent = "";
			let sources: string[] = [];

			if (ragResponse.success && ragResponse.reponse) {
				aiContent = ragResponse.reponse;
				sources = ragResponse.sources || [];
			} else {
				aiContent =
					ragResponse.message ||
					"Désolé, je n'ai pas pu générer une réponse.";
			}

			// Remplacer le message de chargement par la vraie réponse
			setConversations((prev) =>
				prev.map((conv) =>
					conv.id === activeConversationId
						? {
								...conv,
								messages: conv.messages.map((msg) =>
									msg.id === loadingMessageId
										? {
												...msg,
												content: aiContent,
												sources: sources,
												timestamp: new Date(),
										  }
										: msg
								),
						  }
						: conv
				)
			);
		} catch (error) {
			console.error("Erreur lors de l'envoi:", error);

			// Afficher l'erreur
			setConversations((prev) =>
				prev.map((conv) =>
					conv.id === activeConversationId
						? {
								...conv,
								messages: conv.messages.map((msg) =>
									msg.id === loadingMessageId
										? {
												...msg,
												content:
													"❌ Erreur de connexion au serveur. Veuillez réessayer.",
												timestamp: new Date(),
										  }
										: msg
								),
						  }
						: conv
				)
			);
		}
	};

	const handleNewConversation = () => {
		const newConv: Conversation = {
			id: Date.now().toString(),
			title: "Nouvelle conversation",
			timestamp: new Date(),
			messages: [],
		};
		setConversations((prev) => [newConv, ...prev]);
		setActiveConversationId(newConv.id);
	};

	return (
		<div className="flex h-screen bg-background overflow-hidden">
			<ConversationSidebar
				conversations={conversations}
				activeId={activeConversationId}
				onSelect={setActiveConversationId}
				onNew={handleNewConversation}
			/>

			<div className="flex-1 flex flex-col min-h-0">
				{/* Afficher le statut de la DB (optionnel) */}
				{statusData && statusData.success && (
					<div className="p-2 bg-muted/50 text-xs text-center text-muted-foreground">
						📚 {statusData.nombre_chunks} documents indexés
					</div>
				)}

				<ChatContainer messages={activeConversation?.messages || []} />

				<div className="border-t border-border p-4 pb-6">
					<div className="max-w-3xl mx-auto">
						{/* Indicateur de chargement global */}
						{isPending && (
							<div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
								<Loader2 className="h-4 w-4 animate-spin" />
								<span>Traitement en cours...</span>
							</div>
						)}

						<ChatInput
							onSend={handleSendMessage}
							disabled={isPending}
						/>
					</div>
				</div>
			</div>
		</div>
	);
}
