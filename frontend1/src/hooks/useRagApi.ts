/**
 * Hooks personnalisés utilisant TanStack Query pour le service RAG
 * Gestion optimisée du cache, loading, et erreurs
 */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
	ragApi,
	type QuestionResponse,
	type StatutResponse,
	type HealthResponse,
} from "../services/ragApi";

/**
 * Hook pour poser une question au système RAG
 * Utilise useMutation car c'est une action qui modifie l'état
 *
 * @example
 * const { mutate, isPending, error, data } = usePoserQuestion();
 *
 * mutate({ question: "Comment obtenir un passeport ?", nResultats: 3 });
 */
export function usePoserQuestion() {
	return useMutation({
		mutationFn: ({
			question,
			nResultats = 3,
		}: {
			question: string;
			nResultats?: number;
		}) => ragApi.poserQuestion(question, nResultats),
		onSuccess: (data) => {
			console.log("Question posée avec succès:", data);
		},
		onError: (error) => {
			console.error("Erreur lors de la question:", error);
		},
	});
}

/**
 * Hook pour vérifier le statut de la base de données
 * Utilise useQuery pour le cache automatique
 *
 * @param enabled - Active ou désactive la requête automatique
 * @param refetchInterval - Intervalle de rafraîchissement automatique (ms)
 *
 * @example
 * const { data, isLoading, error, refetch } = useVerifierStatut();
 * console.log(`${data?.nombre_chunks} chunks indexés`);
 */
export function useVerifierStatut(enabled = true, refetchInterval?: number) {
	return useQuery<StatutResponse>({
		queryKey: ["rag-statut"],
		queryFn: () => ragApi.verifierStatut(),
		enabled,
		refetchInterval,
		staleTime: 5 * 60 * 1000, // Les données sont considérées fraîches pendant 5 minutes
		gcTime: 10 * 60 * 1000, // Garbage collection après 10 minutes
	});
}

/**
 * Hook pour vérifier la santé de l'API
 *
 * @param enabled - Active ou désactive la requête automatique
 *
 * @example
 * const { data, isLoading } = useHealthCheck();
 * console.log(data?.status); // 'ok' ou 'error'
 */
export function useHealthCheck(enabled = true) {
	return useQuery<HealthResponse>({
		queryKey: ["rag-health"],
		queryFn: () => ragApi.healthCheck(),
		enabled,
		retry: 3, // Réessayer 3 fois en cas d'échec
		//retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
		//staleTime: 1 * 60 * 1000, // 1 minute
	});
}

/**
 * Hook personnalisé combinant question et gestion de l'historique
 * Plus adapté pour une interface de chat
 *
 * @example
 * const { sendQuestion, isPending, error } = useChatQuestion({
 *   onSuccess: (response) => {
 *     console.log('Réponse:', response.reponse);
 *   }
 * });
 */
export function useChatQuestion(options?: {
	onSuccess?: (data: QuestionResponse) => void;
	onError?: (error: Error) => void;
}) {
	const queryClient = useQueryClient();

	const mutation = useMutation({
		mutationFn: ({
			question,
			nResultats = 3,
		}: {
			question: string;
			nResultats?: number;
		}) => ragApi.poserQuestion(question, nResultats),
		onSuccess: (data) => {
			// Invalider le cache du statut après une question
			queryClient.invalidateQueries({ queryKey: ["rag-statut"] });
			options?.onSuccess?.(data);
		},
		onError: (error: Error) => {
			options?.onError?.(error);
		},
	});

	return {
		sendQuestion: mutation.mutate,
		sendQuestionAsync: mutation.mutateAsync,
		isPending: mutation.isPending,
		error: mutation.error,
		data: mutation.data,
		reset: mutation.reset,
	};
}

/**
 * Hook pour gérer les questions avec retry automatique
 * Utile pour les connexions instables
 *
 * @example
 * const { sendQuestion, isPending, retryCount } = useRobustQuestion();
 */
export function useRobustQuestion() {
	const mutation = useMutation({
		mutationFn: ({
			question,
			nResultats = 3,
		}: {
			question: string;
			nResultats?: number;
		}) => ragApi.poserQuestion(question, nResultats),
		retry: 2, // Réessayer 2 fois en cas d'échec
		retryDelay: 1000, // Attendre 1 seconde entre chaque tentative
	});

	return {
		sendQuestion: mutation.mutate,
		isPending: mutation.isPending,
		error: mutation.error,
		data: mutation.data,
		retryCount: mutation.failureCount,
	};
}
