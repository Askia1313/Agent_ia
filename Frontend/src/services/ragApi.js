/**
 * Service API pour communiquer avec le backend RAG
 * Gère toutes les requêtes HTTP vers l'API Django
 */

import axios from 'axios'

// Configuration de base pour les requêtes
const API_BASE_URL = 'http://localhost:8000/api'

// Créer une instance axios avec la configuration par défaut
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Service RAG - Ensemble des fonctions pour communiquer avec l'API
 */
export const ragApi = {
  /**
   * Poser une question au système RAG
   * 
   * @param {string} question - La question de l'utilisateur
   * @param {number} nResultats - Nombre de résultats à retourner (défaut: 3)
   * @returns {Promise} Réponse avec les résultats
   * 
   * @example
   * const response = await ragApi.poserQuestion('Comment obtenir un passeport ?', 5)
   */
  async poserQuestion(question, nResultats = 3) {
    try {
      const response = await apiClient.post('/question/', {
        question: question,
        n_resultats: nResultats
      })
      return response.data
    } catch (error) {
      console.error('Erreur lors de la requête:', error)
      throw error
    }
  },

  /**
   * Vérifier le statut de la base de données
   * 
   * @returns {Promise} Statut avec le nombre de chunks
   * 
   * @example
   * const status = await ragApi.verifierStatut()
   * console.log(`${status.nombre_chunks} chunks indexés`)
   */
  async verifierStatut() {
    try {
      const response = await apiClient.get('/statut/')
      return response.data
    } catch (error) {
      console.error('Erreur lors de la vérification du statut:', error)
      throw error
    }
  },

  /**
   * Health check de l'API
   * 
   * @returns {Promise} Statut de l'API
   * 
   * @example
   * const health = await ragApi.healthCheck()
   * console.log(health.status) // 'ok'
   */
  async healthCheck() {
    try {
      const response = await apiClient.get('/health/')
      return response.data
    } catch (error) {
      console.error('Erreur lors du health check:', error)
      throw error
    }
  }
}
