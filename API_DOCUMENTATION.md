# Documentation API RAG

## Vue d'ensemble
API REST Django simple pour communiquer avec le système RAG (Retrieval-Augmented Generation).

## Configuration

### Démarrer le serveur Django
```bash
cd Backend_ia
python manage.py runserver
```

Le serveur démarre sur `http://localhost:8000`

---

## Endpoints

### 1. Poser une Question
**Endpoint principal** - Récupère les passages pertinents pour une question

- **URL:** `/api/question/`
- **Méthode:** `POST`
- **Content-Type:** `application/json`

#### Requête
```json
{
    "question": "Comment obtenir un passeport ?",
    "n_resultats": 3
}
```

**Paramètres:**
- `question` (string, obligatoire): La question de l'utilisateur
- `n_resultats` (integer, optionnel): Nombre de résultats à retourner (défaut: 3)

#### Réponse (Succès - 200)
```json
{
    "success": true,
    "question": "Comment obtenir un passeport ?",
    "nombre_resultats": 3,
    "resultats": [
        {
            "texte": "Pour obtenir un passeport, vous devez vous présenter à la mairie...",
            "source": "passeport.pdf",
            "distance": 0.1234
        },
        {
            "texte": "Les documents requis sont: pièce d'identité, justificatif de domicile...",
            "source": "https://www.service-public.fr/particuliers/vosdroits/F1341",
            "distance": 0.2456
        }
    ]
}
```

#### Réponse (Erreur)
```json
{
    "success": false,
    "message": "La question ne peut pas être vide"
}
```

#### Exemple avec cURL
```bash
curl -X POST http://localhost:8000/api/question/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Comment obtenir un passeport ?",
    "n_resultats": 5
  }'
```

#### Exemple avec JavaScript (Vue.js)
```javascript
async function poserQuestion(question, nResultats = 3) {
    try {
        const response = await fetch('http://localhost:8000/api/question/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                n_resultats: nResultats
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('Résultats:', data.resultats);
            return data;
        } else {
            console.error('Erreur:', data.message);
        }
    } catch (error) {
        console.error('Erreur réseau:', error);
    }
}

// Utilisation
poserQuestion('Comment obtenir un passeport ?');
```

---

### 2. Vérifier le Statut de la Base de Données
Vérifie si la base de données est prête et le nombre de chunks indexés

- **URL:** `/api/statut/`
- **Méthode:** `GET`

#### Réponse (Succès - 200)
```json
{
    "success": true,
    "nombre_chunks": 1234,
    "message": "Base de données prête"
}
```

#### Exemple avec cURL
```bash
curl http://localhost:8000/api/statut/
```

#### Exemple avec JavaScript
```javascript
async function verifierStatut() {
    try {
        const response = await fetch('http://localhost:8000/api/statut/');
        const data = await response.json();
        console.log(`Base de données: ${data.nombre_chunks} chunks`);
        return data;
    } catch (error) {
        console.error('Erreur:', error);
    }
}
```

---

### 3. Health Check
Vérification simple de la santé de l'API

- **URL:** `/api/health/`
- **Méthode:** `GET`

#### Réponse (Succès - 200)
```json
{
    "status": "ok",
    "message": "API RAG fonctionnelle"
}
```

#### Exemple avec cURL
```bash
curl http://localhost:8000/api/health/
```

---

## Codes HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 400 | Requête invalide (données manquantes ou mal formées) |
| 500 | Erreur serveur |

---

## Intégration Vue.js

### Service API
```javascript
// services/ragApi.js
export const ragApi = {
    async poserQuestion(question, nResultats = 3) {
        const response = await fetch('http://localhost:8000/api/question/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, n_resultats: nResultats })
        });
        return response.json();
    },
    
    async verifierStatut() {
        const response = await fetch('http://localhost:8000/api/statut/');
        return response.json();
    },
    
    async healthCheck() {
        const response = await fetch('http://localhost:8000/api/health/');
        return response.json();
    }
};
```



