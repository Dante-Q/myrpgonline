from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from forms import RegistrationForm, LoginForm, CharacterForm
from database import db, User, Character
from flask_bcrypt import Bcrypt

core_routes = Blueprint('core_routes', __name__, template_folder='templates')
bcrypt = Bcrypt()  

# -------------------- Routes --------------------

@core_routes.route('/')
def index():
    return render_template('index.html')


@core_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.title()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('core_routes.dashboard'))
    return render_template('login.html', form=form)


@core_routes.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('core_routes.index'))


@core_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data.title(), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('core_routes.dashboard'))
    return render_template('register.html', form=form)


@core_routes.route('/create_character', methods=['GET', 'POST'])
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
        return redirect(url_for('core_routes.dashboard'))
    return render_template('create_character.html', form=form)


@core_routes.route('/view_character/<int:char_id>')
@login_required
def view_character(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403
    return render_template('view_character.html', character=character)


@core_routes.route('/dashboard')
@login_required
def dashboard():
    characters = current_user.characters
    return render_template('dashboard.html', name=current_user.username, characters=characters)
