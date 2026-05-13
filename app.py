from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Configuration de la sécurité CORS
# Cela permet à ton site GitHub Pages d'envoyer des requêtes à ce serveur
CORS(app)

# Configuration de l'API BrixHub
API_KEY = "brix_uNAGYffSgJk1fKnq2VLmq0p2ZI9es2_3Y_Ef-spgPBKzPi6q"
SEARCH_URL = "https://brixhub.net/api/v1/search"

@app.route('/search', methods=['POST'])
def proxy_search():
    """
    Ce point d'entrée reçoit les données du formulaire HTML,
    ajoute la clé API et interroge BrixHub.
    """
    try:
        # 1. Récupération des données envoyées par le site HTML
        donnees_utilisateur = request.json
        
        # 2. Préparation des headers sécurisés
        headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }

        # 3. Envoi de la requête à BrixHub
        # On transmet tout le dictionnaire 'donnees_utilisateur' tel quel
        response = requests.post(
            SEARCH_URL, 
            json=donnees_utilisateur, 
            headers=headers,
            timeout=30 # Sécurité pour éviter que le script ne bloque trop longtemps
        )

        # 4. Retour de la réponse de l'API (succès ou erreur) au site HTML
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        # En cas d'erreur de connexion vers BrixHub
        return jsonify({"status": 500, "message": f"Erreur de connexion à l'API : {str(e)}"}), 500
    except Exception as e:
        # En cas d'erreur interne au script
        return jsonify({"status": 500, "message": f"Erreur interne : {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Vérifie si le serveur Python est en ligne."""
    return jsonify({"status": "online"}), 200

if __name__ == "__main__":
    # Récupération du port dynamique (nécessaire pour Render, Heroku, etc.)
    port = int(os.environ.get("PORT", 5000))
    # Lancement du serveur sur toutes les interfaces réseaux
    app.run(host='0.0.0.0', port=port)