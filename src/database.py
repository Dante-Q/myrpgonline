from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

# Initialize SQLAlchemy 
db = SQLAlchemy()

# -------------------- Models --------------------

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    # Relationship to characters
    characters = db.relationship('Character', backref='user', lazy=True)


class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # links character to user
    name = db.Column(db.String(20), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    luck = db.Column(db.Integer, nullable=False)
    total_skill = db.Column(db.Integer, nullable=False)
    dev_mode = db.Column(db.Boolean, default=False)
    gold = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, default=50)  # <-- HP for combat
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    hp = db.Column(db.Integer, default=50)


class Monster(db.Model):
    __tablename__ = 'monster'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    current_hp = db.Column(db.Integer, nullable=False)
    gold_reward = db.Column(db.Integer, default=10)
    attack = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# -------------------- DB Initialization --------------------

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Database tables created.")
