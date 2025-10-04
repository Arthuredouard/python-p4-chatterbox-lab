from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime 

# Définition de la convention de nommage
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    
    # 1. Corps du message (requis par le frontend)
    body = db.Column(db.String, nullable=False)
    
    # 2. Nom d'utilisateur (requis par le frontend)
    username = db.Column(db.String, nullable=False)
    
    # 3. Date de création (valeur par défaut pour l'insertion)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 4. Date de mise à jour (valeur par défaut + mise à jour auto lors de PATCH)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Définition des règles de sérialisation 
    serialize_rules = () 

    def __repr__(self):
        return f'<Message {self.id}: {self.username}>'
