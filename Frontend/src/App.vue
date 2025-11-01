<template>
  <div class="app-container">
    <!-- En-tête -->
    <header class="app-header">
      <div class="header-content">
        <h1><i class="fas fa-robot"></i> Agent IA</h1>
        <p>Système de recherche documentaire intelligent</p>
      </div>
      <div class="header-stats">
        <i class="fas fa-comments"></i>
        <span class="stat">{{ conversations.length }} conversation(s)</span>
      </div>
    </header>

    <!-- Zone de chat -->
    <main class="chat-container">
      <!-- Messages -->
      <div class="messages-area" ref="messagesContainer">
        <div v-if="conversations.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fas fa-comments fa-3x"></i>
          </div>
          <p>Aucune conversation pour le moment</p>
          <p class="hint">Posez une question pour commencer</p>
        </div>

        <div v-for="(conv, index) in conversations" :key="index" class="conversation-group">
          <!-- Question de l'utilisateur -->
          <div class="message user-message">
            <div class="message-content">
              <p>{{ conv.question }}</p>
            </div>
            <span class="message-time">{{ formatTime(conv.timestamp) }}</span>
          </div>

          <!-- Réponse de l'agent -->
          <div class="message agent-message">
            <div class="message-content">
              <div v-if="conv.loading" class="loading">
                <span></span><span></span><span></span>
              </div>
              <div v-else>
                <div v-if="conv.reponse">
                  <!-- Réponse générée par Ollama -->
                  <div class="generated-response">
                    <p class="response-text">{{ conv.reponse }}</p>
                  </div>
                  
                  <!-- Sources utilisées -->
                  <div v-if="conv.sources && conv.sources.length > 0" class="sources-section">
                    <p class="sources-title"><i class="fas fa-book"></i> Sources:</p>
                    <div class="sources-list">
                      <span v-for="(source, idx) in conv.sources" :key="idx" class="source-tag">
                        <i class="fas fa-file-alt"></i> {{ source }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-else class="no-results">
                  <i class="fas fa-exclamation-triangle"></i> Aucune réponse générée
                </div>
              </div>
            </div>
            <span class="message-time">{{ formatTime(conv.responseTime) }}</span>
          </div>
        </div>
      </div>

      <!-- Zone de saisie -->
      <div class="input-area">
        <form @submit.prevent="envoyerQuestion" class="input-form">
          <input
            v-model="question"
            type="text"
            placeholder="Posez votre question..."
            class="input-field"
            :disabled="loading"
            @keyup.enter="envoyerQuestion"
          />
          <button
            type="submit"
            class="send-button"
            :disabled="loading || !question.trim()"
          >
            <i v-if="!loading" class="fas fa-paper-plane"></i>
            <span v-if="!loading">Envoyer</span>
            <i v-else class="fas fa-spinner fa-spin"></i>
          </button>
        </form>

        <!-- Actions -->
        <div class="actions">
          <button @click="effacerConversation" class="action-btn delete-btn">
            <i class="fas fa-trash-alt"></i> Effacer
          </button>
          <button @click="telechargerConversation" class="action-btn download-btn">
            <i class="fas fa-download"></i> Télécharger
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { ragApi } from './services/ragApi'

export default {
  name: 'App',
  setup() {
    // État réactif
    const question = ref('')
    const loading = ref(false)
    const conversations = ref([])
    const messagesContainer = ref(null)

    // Charger les conversations du localStorage au démarrage
    onMounted(() => {
      const saved = localStorage.getItem('conversations')
      if (saved) {
        conversations.value = JSON.parse(saved)
      }
      scrollToBottom()
    })

    /**
     * Envoyer une question à l'API
     */
    const envoyerQuestion = async () => {
      if (!question.value.trim()) return

      // Créer une nouvelle conversation
      const newConversation = {
        question: question.value,
        timestamp: new Date().toLocaleTimeString(),
        reponse: null,
        sources: [],
        contextes: [],
        responseTime: null,
        loading: true
      }

      conversations.value.push(newConversation)
      const currentQuestion = question.value
      question.value = ''
      loading.value = true

      try {
        // Appeler l'API
        const response = await ragApi.poserQuestion(currentQuestion)

        if (response.success) {
          newConversation.reponse = response.reponse
          newConversation.sources = response.sources || []
          newConversation.contextes = response.contextes || []
          newConversation.responseTime = new Date().toLocaleTimeString()
        } else {
          newConversation.reponse = "Erreur: " + (response.message || "Impossible de générer une réponse")
        }
      } catch (error) {
        console.error('Erreur:', error)
        newConversation.reponse = "Erreur de connexion au serveur"
      } finally {
        newConversation.loading = false
        loading.value = false
        sauvegarderConversations()
        nextTick(() => scrollToBottom())
      }
    }

    /**
     * Sauvegarder les conversations dans le localStorage
     */
    const sauvegarderConversations = () => {
      localStorage.setItem('conversations', JSON.stringify(conversations.value))
    }

    /**
     * Effacer toutes les conversations
     */
    const effacerConversation = () => {
      if (confirm('Êtes-vous sûr de vouloir effacer toutes les conversations ?')) {
        conversations.value = []
        sauvegarderConversations()
      }
    }

    /**
     * Télécharger les conversations en JSON
     */
    const telechargerConversation = () => {
      const dataStr = JSON.stringify(conversations.value, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `conversations-${new Date().toISOString().split('T')[0]}.json`
      link.click()
      URL.revokeObjectURL(url)
    }

    /**
     * Formater l'heure
     */
    const formatTime = (time) => {
      if (!time) return ''
      return time
    }

    /**
     * Scroller vers le bas des messages
     */
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    return {
      question,
      loading,
      conversations,
      messagesContainer,
      envoyerQuestion,
      effacerConversation,
      telechargerConversation,
      formatTime
    }
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

/* En-tête */
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.header-content h1 {
  font-size: 24px;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-content h1 i {
  font-size: 28px;
}

.header-content p {
  font-size: 14px;
  opacity: 0.9;
}

.header-stats {
  font-size: 14px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Zone de chat */
.chat-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.messages-area::-webkit-scrollbar {
  width: 8px;
}

.messages-area::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.messages-area::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.messages-area::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* État vide */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  text-align: center;
}

.empty-icon {
  margin-bottom: 16px;
  color: #ccc;
}

.empty-icon i {
  font-size: 64px;
}

.empty-state p {
  margin: 4px 0;
}

.empty-state .hint {
  font-size: 12px;
  color: #bbb;
}

/* Groupes de conversation */
.conversation-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Messages */
.message {
  display: flex;
  flex-direction: column;
  gap: 4px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-message {
  align-items: flex-end;
}

.user-message .message-content {
  background: #667eea;
  color: white;
  border-radius: 12px 12px 4px 12px;
  max-width: 70%;
}

.agent-message {
  align-items: flex-start;
}

.agent-message .message-content {
  background: #f0f0f0;
  color: #333;
  border-radius: 12px 12px 12px 4px;
  max-width: 70%;
}

.message-content {
  padding: 12px 16px;
  word-wrap: break-word;
}

.message-content p {
  margin: 0;
  line-height: 1.4;
}

.message-time {
  font-size: 12px;
  color: #999;
  padding: 0 4px;
}

/* Réponse générée */
.generated-response {
  margin-bottom: 12px;
}

.response-text {
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

/* Sources */
.sources-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e0e0e0;
}

.sources-title {
  font-size: 12px;
  font-weight: 600;
  color: #667eea;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.sources-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.source-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  padding: 4px 10px;
  background: white;
  border: 1px solid #667eea;
  border-radius: 12px;
  color: #667eea;
}

.source-tag i {
  font-size: 10px;
}

.no-results {
  color: #999;
  font-size: 14px;
  text-align: center;
  padding: 12px;
}

/* Loading */
.loading {
  display: flex;
  gap: 4px;
  align-items: center;
  height: 20px;
}

.loading span {
  width: 6px;
  height: 6px;
  background: #667eea;
  border-radius: 50%;
  animation: bounce 1.4s infinite;
}

.loading span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  40% {
    opacity: 1;
    transform: translateY(-8px);
  }
}

/* Zone de saisie */
.input-area {
  padding: 16px;
  background: #f9f9f9;
  border-top: 1px solid #eee;
}

.input-form {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.input-field {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-field:disabled {
  background: #f0f0f0;
  cursor: not-allowed;
}

.send-button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.send-button i {
  font-size: 14px;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Actions */
.actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  flex: 1;
  padding: 10px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.action-btn i {
  font-size: 12px;
}

.action-btn:hover {
  background: #f5f5f5;
  border-color: #999;
}

.delete-btn:hover {
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.download-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

/* Responsive */
@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .user-message .message-content,
  .agent-message .message-content {
    max-width: 100%;
  }

  .input-form {
    flex-direction: column;
  }

  .send-button {
    width: 100%;
  }
}
</style>
