import random

# List of monsters with different stats
# Name reflects strength
MONSTERS = [
    {"name": "Skeleton", "max_hp": 25, "gold_reward": 8, "strength": 2},
    {"name": "Goblin", "max_hp": 30, "gold_reward": 10, "strength": 3},
    {"name": "Bandit", "max_hp": 40, "gold_reward": 15, "strength": 4},
    {"name": "Giant Spider", "max_hp": 45, "gold_reward": 18, "strength": 4},
    {"name": "Orc", "max_hp": 50, "gold_reward": 20, "strength": 5},
    {"name": "Bandit Chief", "max_hp": 70, "gold_reward": 30, "strength": 5},
    {"name": "Warlock", "max_hp": 35, "gold_reward": 25, "strength": 9},
    {"name": "Necromancer", "max_hp": 60, "gold_reward": 40, "strength": 7},
    {"name": "Sorcerer", "max_hp": 50, "gold_reward": 35, "strength": 6},
    {"name": "Vampire", "max_hp": 70, "gold_reward": 35, "strength": 7},
    {"name": "Troll", "max_hp": 100, "gold_reward": 35, "strength": 9},
    {"name": "Dark Knight", "max_hp": 100, "gold_reward": 50, "strength": 10},
    {"name": "Hydra", "max_hp": 130, "gold_reward": 60, "strength": 13},
    {"name": "Dragon", "max_hp": 160, "gold_reward": 80, "strength": 15},
    {"name": "Demon Lord", "max_hp": 200, "gold_reward": 100, "strength": 17},
    {"name": "Oblivion King", "max_hp": 500, "gold_reward": 250, "strength": 25},
    {"name": "Alien Spacecraft", "max_hp": 3000, "gold_reward": 500, "strength": 0},
]

def get_random_monster():
    """Return a random monster dict with current HP initialized"""
    m = random.choice(MONSTERS)
    monster_copy = m.copy()
    monster_copy["current_hp"] = monster_copy["max_hp"]
    return monster_copy
