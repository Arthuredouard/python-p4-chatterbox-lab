# from flask import Flask, request, make_response, jsonify
# from flask_cors import CORS
# from flask_migrate import Migrate

# from models import db, Message

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# CORS(app)
# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/messages')
# def messages():
#     return ''

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''

# if __name__ == '__main__':
#     app.run(port=5555)
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

# Importations du modèle et de la base de données (assurez-vous que Message est défini dans models.py)
from models import db, Message 

app = Flask(__name__)
# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialisation des extensions
CORS(app) 
migrate = Migrate(app, db)
db.init_app(app)

# =========================================================
# Route /messages (Collection: GET et POST)
# =========================================================

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # GET /messages: Renvoie un tableau de tous les messages, classés par created_at (ascendant)
        try:
            # Récupérer et trier les messages
            messages = Message.query.order_by(Message.created_at.asc()).all()
            
            # Sérialiser les objets en une liste de dictionnaires
            messages_dict = [message.to_dict() for message in messages]
            
            # Retourner la réponse JSON
            return jsonify(messages_dict), 200
        except Exception as e:
            # Gérer les erreurs de base de données ou de sérialisation
            return jsonify({"error": "Erreur lors de la récupération des messages."}), 500


    elif request.method == 'POST':
        # POST /messages: Crée un nouveau message
        data = request.get_json()
        
        # Validation des données (vérification de la présence de body et username)
        if not data or 'body' not in data or 'username' not in data:
            return jsonify({"error": "Les champs 'body' et 'username' sont requis."}), 400

        try:
            # Créer le nouveau message
            new_message = Message(
                body=data['body'],
                username=data['username']
            )
            
            db.session.add(new_message)
            db.session.commit()
            
            # Retourner le message créé avec le statut 201 CREATED
            return jsonify(new_message.to_dict()), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Erreur d'intégrité de la base de données."}), 400
        except Exception:
            db.session.rollback()
            return jsonify({"error": "Impossible de créer le message."}), 500


# =========================================================
# Route /messages/<int:id> (Élément unique: PATCH et DELETE)
# =========================================================

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # Chercher le message par ID
    message = Message.query.get(id)
    
    # Gérer le cas où le message n'est pas trouvé
    if not message:
        return jsonify({"error": "Message non trouvé"}), 404

    if request.method == 'PATCH':
        # PATCH /messages/<int:id>: Met à jour le corps du message
        data = request.get_json()

        if 'body' not in data:
            return jsonify({"error": "Le champ 'body' est requis pour la mise à jour"}), 400

        try:
            # Mise à jour de l'attribut 'body'
            message.body = data['body']
            # La colonne 'updated_at' est mise à jour automatiquement par le modèle
            db.session.commit()

            # Retourner le message mis à jour (statut 200 OK)
            return jsonify(message.to_dict()), 200

        except Exception:
            db.session.rollback()
            return jsonify({"error": "Échec de la mise à jour du message"}), 400

    elif request.method == 'DELETE':
        # DELETE /messages/<int:id>: Supprime le message
        try:
            db.session.delete(message)
            db.session.commit()
            
            # Retourner le statut 204 No Content pour une suppression réussie
            return '', 204

        except Exception:
            db.session.rollback()
            return jsonify({"error": "Échec de la suppression du message"}), 500


if __name__ == '__main__':
    # Utiliser le port 5555 pour éviter les conflits et pour des raisons de clarté
    app.run(port=5555)
