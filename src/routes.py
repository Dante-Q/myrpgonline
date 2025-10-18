from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from database import Character, Monster, db
import random

# Create a Blueprint
game_routes = Blueprint('game_routes', __name__)

# ------------------ Play Game ------------------
@game_routes.route('/play_game/<int:char_id>', methods=['GET', 'POST'])
@login_required
def play_game(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    # Get or create a monster
    monster = Monster.query.first()
    if not monster:
        monster = Monster(
            name="Goblin",
            max_hp=50,
            current_hp=50,
            gold_reward=20
        )
        db.session.add(monster)
        db.session.commit()

    return render_template('play_game.html', character=character, monster=monster)

# ------------------ Attack ------------------
@game_routes.route('/attack/<int:char_id>')
@login_required
def attack(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    monster = Monster.query.first()
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
    monster_base = random.randint(1, 5)
    monster_damage = monster_base  # Could scale with monster difficulty
    character.hp -= monster_damage
    log_messages.append(f"{monster.name} attacks {character.name} for {monster_damage} damage!")

    # Check if player is dead
    if character.hp <= 0:
        log_messages.append(f"{character.name} has been defeated!")
        character.hp = 0  # prevent negative HP

    db.session.commit()

    return jsonify({
        'message': ' '.join(log_messages),
        'gold': character.gold,
        'monster_hp': monster.current_hp,
        'player_hp': character.hp
    })

# ------------------ Explore ------------------
@game_routes.route('/explore/<int:char_id>')
@login_required
def explore(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    gold_found = random.randint(5, 20)
    character.gold += gold_found
    db.session.commit()

    message = f"{character.name} explores and finds {gold_found} gold!"
    return jsonify({'message': message, 'gold': character.gold})

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
