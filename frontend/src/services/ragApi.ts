/**
 * Service API pour communiquer avec le backend RAG
 * Gère toutes les requêtes HTTP vers l'API Django
 */

import axios, { type AxiosInstance } from "axios";

// Configuration de base pour les requêtes
const API_BASE_URL = "/api";

// Créer une instance axios avec la configuration par défaut
const apiClient: AxiosInstance = axios.create({
	baseURL: API_BASE_URL,
	headers: {
		"Content-Type": "application/json",
	},
	//timeout: 30000, // 30 secondes
});

// Types TypeScript pour les réponses
export interface QuestionResponse {
	success: boolean;
	reponse: string;
	sources?: string[];
	contextes?: string[];
	message?: string;
}

export interface StatutResponse {
	success: boolean;
	nombre_chunks: number;
	message?: string;
}

export interface HealthResponse {
	status: string;
	message?: string;
}

/**
 * Service RAG - Ensemble des fonctions pour communiquer avec l'API
 */
export const ragApi = {
	/**
	 * Poser une question au système RAG
	 *
	 * @param question - La question de l'utilisateur
	 * @param nResultats - Nombre de résultats à retourner (défaut: 3)
	 * @returns Promise avec la réponse
	 *
	 * @example
	 * const response = await ragApi.poserQuestion('Comment obtenir un passeport ?', 5)
	 */
	async poserQuestion(
		question: string,
		nResultats: number = 3
	): Promise<QuestionResponse> {
		try {
			const response = await apiClient.post<QuestionResponse>(
				"/question/",
				{
					question,
					n_resultats: nResultats,
				}
			);
			return response.data;
		} catch (error) {
			console.error("Erreur lors de la requête:", error);

			// Retourner une réponse d'erreur structurée
			if (axios.isAxiosError(error)) {
				return {
					success: false,
					reponse: "",
					message:
						error.response?.data?.message ||
						error.message ||
						"Erreur de connexion au serveur",
				};
			}

			return {
				success: false,
				reponse: "",
				message: "Une erreur inattendue s'est produite",
			};
		}
	},

	/**
	 * Vérifier le statut de la base de données
	 *
	 * @returns Promise avec le statut
	 *
	 * @example
	 * const status = await ragApi.verifierStatut()
	 * console.log(`${status.nombre_chunks} chunks indexés`)
	 */
	async verifierStatut(): Promise<StatutResponse> {
		try {
			const response = await apiClient.get<StatutResponse>("/statut/");
			return response.data;
		} catch (error) {
			console.error("Erreur lors de la vérification du statut:", error);

			if (axios.isAxiosError(error)) {
				return {
					success: false,
					nombre_chunks: 0,
					message: error.response?.data?.message || error.message,
				};
			}

			return {
				success: false,
				nombre_chunks: 0,
				message: "Erreur lors de la vérification du statut",
			};
		}
	},

	/**
	 * Health check de l'API
	 *
	 * @returns Promise avec le statut de santé de l'API
	 *
	 * @example
	 * const health = await ragApi.healthCheck()
	 * console.log(health.status) // 'ok'
	 */
	async healthCheck(): Promise<HealthResponse> {
		try {
			const response = await apiClient.get<HealthResponse>("/health/");
			return response.data;
		} catch (error) {
			console.error("Erreur lors du health check:", error);

			return {
				status: "error",
				message: "Impossible de joindre le serveur",
			};
		}
	},
};

// Intercepteur pour gérer les erreurs globalement (optionnel)
apiClient.interceptors.response.use(
	(response) => response,
	(error) => {
		// Log des erreurs pour le debug
		if (error.response) {
			console.error(
				"Erreur de réponse:",
				error.response.status,
				error.response.data
			);
		} else if (error.request) {
			console.error("Pas de réponse du serveur:", error.request);
		} else {
			console.error("Erreur de configuration:", error.message);
		}
		return Promise.reject(error);
	}
);

export default ragApi;
