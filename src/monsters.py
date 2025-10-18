import random

# List of monsters with different stats
# Name reflects strength
MONSTERS = [
    {"name": "Goblin", "max_hp": 30, "gold_reward": 10, "strength": 3},
    {"name": "Orc", "max_hp": 50, "gold_reward": 20, "strength": 5},
    {"name": "Troll", "max_hp": 80, "gold_reward": 40, "strength": 8},
    {"name": "Dragon", "max_hp": 150, "gold_reward": 100, "strength": 12},
    {"name": "Skeleton", "max_hp": 25, "gold_reward": 8, "strength": 2},
    {"name": "Bandit", "max_hp": 40, "gold_reward": 15, "strength": 4},
    {"name": "Warlock", "max_hp": 35, "gold_reward": 25, "strength": 6},
    {"name": "Dark Knight", "max_hp": 90, "gold_reward": 50, "strength": 9},
    {"name": "Giant Spider", "max_hp": 45, "gold_reward": 18, "strength": 4},
    {"name": "Vampire", "max_hp": 70, "gold_reward": 35, "strength": 7},
    {"name": "Necromancer", "max_hp": 60, "gold_reward": 40, "strength": 6},
    {"name": "Hydra", "max_hp": 120, "gold_reward": 80, "strength": 10},
    {"name": "Demon Lord", "max_hp": 200, "gold_reward": 150, "strength": 15},
    {"name": "Bandit Chief", "max_hp": 55, "gold_reward": 30, "strength": 5},
    {"name": "Sorcerer", "max_hp": 50, "gold_reward": 35, "strength": 6},
]

def get_random_monster():
    """Return a random monster dict with current HP initialized"""
    m = random.choice(MONSTERS)
    monster_copy = m.copy()
    monster_copy["current_hp"] = monster_copy["max_hp"]
    return monster_copy
