import { useState } from "react";
import ChatContainer from "./ChatContainer";
import ChatInput from "./ChatInput";
import ConversationSidebar from "./ConversationSidebar";

interface Message {
	id: string;
	role: "user" | "assistant";
	content: string;
	timestamp: Date;
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

	const activeConversation = conversations.find(
		(conv) => conv.id === activeConversationId
	);

	const handleSendMessage = (content: string) => {
		if (!activeConversation) return;

		const userMessage: Message = {
			id: Date.now().toString(),
			role: "user",
			content,
			timestamp: new Date(),
		};

		// Simulate AI response with markdown
		const aiMessage: Message = {
			id: (Date.now() + 1).toString(),
			role: "assistant",
			content: `Votre **.gitignore** est globalement bon mais peut être amélioré. Voici une analyse détaillée :

✅ **Points positifs**

- Exclut les fichiers Python compilés (\`__pycache__/\`, \`*.pyc\`)
- Exclut \`node_modules/\` et les dossiers de build
- Exclut \`db.sqlite3\` (base de données locale)

⚠️ **Problèmes identifiés**

**1. Base de données ChromaDB non ignorée**

\`\`\`
chroma_db/
...
\`\`\`

Votre dossier \`chroma_db/\` contient une base de données vectorielle qui devrait probablement être ignorée.

**Comment puis-je vous aider ?**`,
			timestamp: new Date(),
		};

		setConversations((prev) =>
			prev.map((conv) =>
				conv.id === activeConversationId
					? {
							...conv,
							messages: [
								...conv.messages,
								userMessage,
								aiMessage,
							],
							title:
								conv.messages.length === 0
									? content.slice(0, 50)
									: conv.title,
					  }
					: conv
			)
		);
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

			<div className="flex-1 flex flex-col">
				<ChatContainer messages={activeConversation?.messages || []} />

				<div className="border-t border-border p-4 pb-6">
					<div className="max-w-3xl mx-auto">
						<ChatInput onSend={handleSendMessage} />
					</div>
				</div>
			</div>
		</div>
	);
}
