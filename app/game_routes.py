from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from .database import Character, Monster, db
from .monsters import get_random_monster
from .shop import SHOP_ITEMS

import random

game_routes = Blueprint('game_routes', __name__, template_folder='../templates')

# ------------------ Play Game ------------------
@game_routes.route('/play_game/<int:char_id>', methods=['GET'])
@login_required
def play_game(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    # Get monster linked to this character (if exists)
    monster = Monster.query.filter_by(character_id=character.id).first()
    return render_template('play_game.html', character=character, monster=monster)

# ------------------ Shop ------------------
@game_routes.route('/shop/<int:char_id>')
@login_required
def shop(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    return jsonify({
        "items": SHOP_ITEMS,
        "gold": character.gold,
        "strength": character.strength
    })

#------------------ Buy Item ------------------
@game_routes.route('/buy_item/<int:char_id>/<int:item_id>')
@login_required
def buy_item(char_id, item_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    item = next((i for i in SHOP_ITEMS if i["id"] == item_id), None)
    if not item:
        return jsonify({"message": "Item not found!"}), 404

    if character.gold < item["cost"]:
        return jsonify({"message": f"Not enough gold to buy {item['name']}!", "gold": character.gold})

    # Deduct gold
    character.gold -= item["cost"]

    # Apply item effects
    if "hp_restore" in item:
        character.hp = min(character.max_hp, character.hp + item["hp_restore"])
    if "strength_bonus" in item:
        character.strength += item["strength_bonus"]
    if "hp_bonus" in item:
        character.max_hp += item["hp_bonus"]
        character.hp += item["hp_bonus"]  # also heal by bonus
    
    db.session.commit()

    return jsonify({
        "message": f"{character.name} bought {item['name']}!",
        "gold": character.gold,
        "player_hp": character.hp,
        "player_max_hp": character.max_hp,
        "player_strength": character.strength
    })

# ------------------ Get Current Monster ------------------
@game_routes.route('/current_monster/<int:char_id>')
@login_required
def current_monster(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    monster = Monster.query.filter_by(character_id=character.id).first()
    if monster:
        return jsonify({
            'monster_name': monster.name,
            'monster_hp': monster.current_hp,
            'monster_max_hp': monster.max_hp
        })
    else:
        return jsonify({})  # no monster

    
# ------------------ Attack ------------------
@game_routes.route('/attack/<int:char_id>')
@login_required
def attack(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    log_messages = []

    # Only attack the monster linked to this character
    monster = Monster.query.filter_by(character_id=character.id).first()
    if not monster:
        return jsonify({'message': 'No monster to attack!'}), 400

    # -------- Player attack --------
    player_damage = random.randint(1, 5) + (character.strength // 2)
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
            'monster_name': '',
            'player_hp': character.hp
        })

    # -------- Monster attacks --------
    monster_damage = monster.attack
    character.hp -= monster_damage
    log_messages.append(f"{monster.name} attacks {character.name} for {monster_damage} damage!")

    # Check if player is dead
    if character.hp <= 0:
        lost_gold = character.gold
        character.hp = character.max_hp
        character.gold = 0
        log_messages.append(f"{character.name} has been defeated and loses all {lost_gold} gold!")
        db.session.delete(monster)
        db.session.commit()
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold,
            'player_hp': character.hp,
            'monster_hp': 0,
            'monster_name': ''
        })

    db.session.commit()
    return jsonify({
        'message': ' '.join(log_messages),
        'gold': character.gold,
        'player_hp': character.hp,
        'monster_hp': monster.current_hp,
        'monster_name': monster.name
    })


# ------------------ Run Away ------------------
@game_routes.route('/run/<int:char_id>')
@login_required
def run_away(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    monster = Monster.query.filter_by(character_id=character.id).first()
    if not monster:
        return jsonify({'message': 'There is no monster to run from!'}), 400

    log_messages = []
    if random.random() < 0.5:  # 50% chance to run
        log_messages.append(f"{character.name} successfully ran away from {monster.name}!")
        db.session.delete(monster)
        db.session.commit()
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold,
            'player_hp': character.hp,
            'monster_hp': 0,
            'monster_name': ''
        })
    else:
        monster_damage = monster.attack
        character.hp -= monster_damage
        log_messages.append(f"{character.name} failed to run! {monster.name} attacks for {monster_damage} damage!")
        if character.hp <= 0:
            lost_gold = character.gold
            character.hp = character.max_hp
            character.gold = 0
            log_messages.append(f"{character.name} has been defeated and loses all {lost_gold} gold!")
            db.session.delete(monster)
        db.session.commit()
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold,
            'player_hp': character.hp,
            'monster_hp': monster.current_hp if character.hp > 0 else 0,
            'monster_name': monster.name if character.hp > 0 else ''
        })


# ------------------ Explore ------------------
@game_routes.route('/explore/<int:char_id>')
@login_required
def explore(char_id):
    character = Character.query.get_or_404(char_id)
    if character.user_id != current_user.id:
        return "Unauthorized", 403

    log_messages = []

    # Prevent multiple monsters
    existing_monster = Monster.query.filter_by(character_id=character.id).first()
    if existing_monster:
        return jsonify({'message': f"You are already facing a {existing_monster.name}!"})

    chance = random.random() # 0 - 1 game explore events below
    if chance < 0.06:
        upgrade_type = random.random()
        if upgrade_type < 0.5:
            log_messages.append(f"{character.name} discovers a health upgrade!")
            character.max_hp += 5
            character.hp += 5  
            db.session.commit()
        else:
            log_messages.append(f"{character.name} discovers a sword upgrade!")
            character.strength += 1
            db.session.commit()
        return jsonify({
            'message': ' '.join(log_messages),
            'player_strength': character.strength,
            'player_hp': character.hp,
            'player_max_hp': character.max_hp
        })
    elif chance < 0.1:
        hp_lost = random.randint(1, 10)
        character.hp = max(0, character.hp - hp_lost)
        db.session.commit()
        log_messages.append(f"{character.name} stumbles into a trap and loses {hp_lost} HP!")
        return jsonify({
            'message': ' '.join(log_messages),
            'player_hp': character.hp
        })
    elif chance < 0.55:
        monster_template = get_random_monster()
        monster = Monster(
            name=monster_template['name'],
            max_hp=monster_template['max_hp'],
            current_hp=monster_template['current_hp'],
            gold_reward=monster_template['gold_reward'],
            attack=monster_template['strength'],
            character_id=character.id
        )
        db.session.add(monster)
        db.session.commit()
        log_messages.append(f"\n{character.name} encounters a {monster.name}!\n")
        return jsonify({
            'message': ' '.join(log_messages),
            'monster_name': monster.name,
            'monster_hp': monster.current_hp,
            'monster_max_hp': monster.max_hp,
            'gold': character.gold
        })
    elif chance < 0.65:
        db.session.commit()
        log_messages.append(f"{character.name} navigates through a quiet area and finds nothing of interest.")
        return jsonify({
            'message': ' '.join(log_messages)
        })
    else:
        gold_found = random.randint(5, 15)
        character.gold += gold_found
        db.session.commit()
        log_messages.append(f"{character.name} explores and finds {gold_found} gold!")
        return jsonify({
            'message': ' '.join(log_messages),
            'gold': character.gold
        })
