/**
 * Point d'entrée principal de l'application Vue.js
 * Initialise l'app et monte le composant racine
 */

import { createApp } from 'vue'
import App from './App.vue'

// Créer et monter l'application Vue
const app = createApp(App)
app.mount('#app')
