from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from database import Character, Monster, db
from monsters import get_random_monster
import random

# Create a Blueprint
game_routes = Blueprint('game_routes', __name__)

# ------------------ Play Game ------------------
@game_routes.route('/play_game/<int:char_id>', methods=['GET'])
@login_required
def play_game(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    return render_template('play_game.html', character=character)

# ------------------ Attack ------------------
@game_routes.route('/attack/<int:char_id>')
@login_required
def attack(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    monster = Monster.query.filter_by(character_id=character.id).first()
    if not monster:
        return jsonify({'message': 'No monster to attack!'}), 400

    log_messages = []

    # -------- Player attack --------
    player_base = random.randint(1, 5)
    player_damage = player_base + character.strength
    monster.current_hp -= player_damage
    log_messages.append(f"{character.name} attacks {monster.name} for {player_damage} damage!")

    # Check if monster is dead
    if monster.current_hp <= 0:
        character.gold += monster.gold_reward
        log_messages.append(f"{monster.name} is defeated! {character.name} gains {monster.gold_reward} gold!")
        db.session.delete(monster)
        db.session.commit()
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold,
            'monster_hp': 0,
            'player_hp': character.hp
        })

    # -------- Monster attacks --------
    monster_damage = monster.attack
    character.hp -= monster_damage
    log_messages.append(f"{monster.name} attacks {character.name} for {monster_damage} damage!")

    if character.hp <= 0:
        log_messages.append(f"{character.name} has been defeated!")
        character.hp = 0

    db.session.commit()
    return jsonify({
        'message': ' '.join(log_messages),
        'gold': character.gold,
        'monster_hp': monster.current_hp,
        'player_hp': character.hp
    })

@game_routes.route('/run/<int:char_id>')
@login_required
def run_away(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    monster = Monster.query.first()
    if not monster:
        return jsonify({'message': 'There is no monster to run from!'}), 400

    log_messages = []
    success = random.random() < 0.5  # 50% chance to run
    if success:
        log_messages.append(f"{character.name} successfully ran away from {monster.name}!")
        db.session.delete(monster)  # remove monster from DB
        db.session.commit()
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold,
            'player_hp': character.hp,
            'monster_hp': 0,
            'monster_name': ''
        })
    else:
        # Monster attacks on failed escape
        monster_base = random.randint(1, 5)
        character.hp -= monster_base
        if character.hp < 0:
            character.hp = 0
        log_messages.append(f"{character.name} failed to run! {monster.name} attacks for {monster_base} damage!")
        db.session.commit()
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold,
            'player_hp': character.hp,
            'monster_hp': monster.current_hp,
            'monster_name': monster.name
        })

# ------------------ Explore ------------------
@game_routes.route('/explore/<int:char_id>')
@login_required
def explore(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    log_messages = []
    chance = random.random()

    if chance < 0.1:
        # Shop encounter
        log_messages.append(f"{character.name} discovers a hidden shop!")
        return jsonify({
            'message': ' '.join(log_messages),
            'outcome': 'shop',
            'gold': character.gold
        })
    elif chance < 0.5:
        # Monster encounter
        monster_template = get_random_monster()  # returns dict with current_hp already
        monster = Monster(
            name=monster_template['name'],
            max_hp=monster_template['max_hp'],
            current_hp=monster_template['current_hp'],
            gold_reward=monster_template['gold_reward'],
            attack=monster_template['strength'],
            character_id=character.id   # LINK MONSTER TO THIS CHARACTER
        )
        db.session.add(monster)
        db.session.commit()
        log_messages.append(f"{character.name} encounters a {monster.name}!")

        return jsonify({
            'message': ' '.join(log_messages),
            'monster_name': monster.name,
            'monster_hp': monster.current_hp,
            'monster_max_hp': monster.max_hp,
            'gold': character.gold
        })
    else:
        # Find gold
        gold_found = random.randint(5, 20)
        character.gold += gold_found
        db.session.commit()
        log_messages.append(f"{character.name} explores and finds {gold_found} gold!")
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold
        })

# ------------------ Buy Item ------------------
@game_routes.route('/buy_item/<int:char_id>')
@login_required
def buy_item(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    item_cost = 15
    if character.gold >= item_cost:
        character.gold -= item_cost
        db.session.commit()
        message = f"{character.name} buys an item for {item_cost} gold!"
    else:
        message = f"{character.name} does not have enough gold to buy an item."

    return jsonify({'message': message, 'gold': character.gold})
