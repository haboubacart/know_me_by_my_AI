import secrets
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_token():
    token = secrets.token_urlsafe(16)
    new_token = Token(token=token)
    db.session.add(new_token)
    db.session.commit()
    return token

def verify_token(token):
    token_entry = Token.query.filter_by(token=token).first()
    if token_entry and not token_entry.used:
        token_entry.used = True
        db.session.commit()
        return True
    return False

def invalidate_token(token):
    token_entry = Token.query.filter_by(token=token).first()
    if token_entry:
        db.session.delete(token_entry)
        db.session.commit()
        return True
    return False
