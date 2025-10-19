from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

# Import database and models
from database import db, User, Character, init_db
from routes import core_routes
from game_routes import game_routes

# -------------------- Flask App Setup --------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize DB and Bcrypt
init_db(app)
bcrypt = Bcrypt(app)
app.register_blueprint(core_routes)
app.register_blueprint(game_routes)

# -------------------- Flask-Login Setup --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- Main Entry Point -------------------- 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
