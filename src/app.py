from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange
from flask_bcrypt import Bcrypt

# Import database and models
from database import db, User, Character, init_db
from routes import game_routes

# -------------------- Flask App Setup --------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize DB and Bcrypt
init_db(app)
bcrypt = Bcrypt(app)
app.register_blueprint(game_routes)

# -------------------- Flask-Login Setup --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- Forms --------------------

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data.title()).first()
        if existing_user:
            raise ValidationError("That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class CharacterForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(max=20)], render_kw={"placeholder": "Character Name"})
    submit = SubmitField("Create")

# -------------------- Routes --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.title()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data.title(), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/create_character', methods=['GET', 'POST'])
@login_required
def create_character():
    form = CharacterForm()
    if form.validate_on_submit():

        new_character = Character(
            user_id=current_user.id,
            name=form.name.data.title()
        )
        db.session.add(new_character)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('create_character.html', form=form)

@app.route('/view_character/<int:char_id>')
@login_required
def view_character(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403
    return render_template('view_character.html', character=character)

@app.route('/dashboard')
@login_required
def dashboard():
    characters = current_user.characters  # list of characters for this user
    return render_template('dashboard.html', name=current_user.username, characters=characters)

# -------------------- Main Entry Point -------------------- 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
