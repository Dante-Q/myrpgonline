from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .database import db
from .routes import core_routes
from .game_routes import game_routes

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "core_routes.login"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # User loader
    from .database import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(core_routes)
    app.register_blueprint(game_routes)

    # Create DB tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
