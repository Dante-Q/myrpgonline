import time, sys, random, re
import json, subprocess

full_dot = '●'
empty_dot = '○'

# Creates Character
def create_character(character_name, strength, intelligence, charisma, dev_mode):

    # Assign's Luck and Skill
    skill = sum([strength,intelligence,charisma])
    if dev_mode:
        luck = 10
    else:
        luck = random.randint(1,10)

    # Saves Character Data to json
    character_data = {
    "name": character_name,
    "strength": strength,
    "intelligence": intelligence,
    "charisma": charisma,
    "luck": luck,
    "total_skill": skill,
    "dev_mode": dev_mode,
    }
    with open("character.json", "w") as f:
        json.dump(character_data, f, indent=4)

# Makes Character Bar
def make_bar(value, dev_mode):
    if dev_mode:
        return str(value)
    else:
        return full_dot * value + empty_dot * (10 - value)

# Returns Character info
def display_character(character_name, strength, intelligence, charisma, dev_mode):  
    STR = 'STR ' + make_bar(strength, dev_mode)
    INT = 'INT ' + make_bar(intelligence, dev_mode)
    CHA = 'CHA ' + make_bar(charisma, dev_mode)
    return character_name + '\n' + STR + '\n' + INT + '\n' + CHA

# Dev Function to add extra points 
def dev_function():
    dev_mode = True
    skill_points = get_int_input("Please input number of Skill points", 1, 300, dev_mode)
    max_skillpoints = 100
    return skill_points, max_skillpoints, dev_mode

# Sexy little dots for added effect
def animated_start_over(cycles=3, delay=0.5):
    for _ in range(cycles):
        for dots in range(1, 4):  # 1 to 3 dots
            sys.stdout.write(f"\rStarting over{'.' * dots}{' ' * (3 - dots)}")
            sys.stdout.flush()
            time.sleep(delay)
    sys.stdout.write("\rStarting over... Done!\n\n")  
    sys.stdout.flush()

# Controls Inputs
def get_int_input(prompt, min_val, max_val, dev_mode):
    while True:
        try:
            value = int(input(f"{prompt} ({min_val}-{max_val}): "))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number, not text.")

def get_name():
    max_name_length = 10
        
    while True:
        name = input(f"\nPlease input your Character's name (max {max_name_length} chars): ").strip()
        # checks for developer and returns True if so
        if name.lower() == "developer":
            print("Developer Mode Activated!!")
            return "Developer", True
        # checks for empty
        if not name:
            print("Name cannot be Empty")
            continue
        # checks length
        if len(name) > max_name_length:
            print(f"Name cannot be longer than {max_name_length} characters")
            continue
        # must start with letter
        if not name[0].isalpha():
            print("Name must start with a letter")
            continue
        # checks for allowed characters
        if not re.match(r'^[A-Za-z][A-Za-z0-9_ ]*$', name):
            print("Invalid characters! Only letters, numbers, underscores, and spaces are allowed")
            continue
        # checks for reserved names
        reserved = ["admin", "system", "null", "test"]
        if name.lower() in reserved:
            print(f" {name} is a reserved name")
            continue
        return name.title(), False

print('''\n            --------------------------
            Welcome to the Python RPG!
            --------------------------''')

# ----------------------------  Main Loop for Character Creation --------------------------------------
while True:
    break_outer = False
    dev_mode = False

    # Name
    character_name, dev_mode = get_name()

    while True:
        strength = 0
        intelligence = 0
        charisma = 0

        if dev_mode:
            skill_points, max_skillpoints, dev_mode = dev_function()
        else:   
            skill_points = 7 
            max_skillpoints = 4
            print(f"\nYou have {skill_points} skill points to assign.")
            print(f"A maximum of {max_skillpoints} points can be assigned to each trait.")

        # Strength
        max_for_strength = min(max_skillpoints, skill_points)
        strength = get_int_input("\nPlease input Strength", 0, max_for_strength, dev_mode)
        skill_points -= strength   

        print(f"You have {skill_points} points left.")

        # Intelligence
        if skill_points > 0:
            max_for_intelligence = min(max_skillpoints, skill_points)
            intelligence = get_int_input("Please input Intelligence", 0, max_for_intelligence, dev_mode)
            skill_points -= intelligence
        else:
            intelligence = 0

        # Charisma
        if skill_points <= max_skillpoints:
            print("Assigning remaining points to charisma")
            charisma = skill_points
            time.sleep(2)
            break
        if skill_points > max_skillpoints:
            print(f"\nYou have {skill_points} leftover points, which exceeds the max per trait ({max_skillpoints}). Please redistribute your points.")
            continue

    # Prints result of create_character
    result = display_character('\n' + character_name, strength, intelligence, charisma, dev_mode)
    print(result)
    time.sleep(3)  

    # Final Check - Restarts loop or triggers character creation
    while True:     
        start_over = input(f"Are you happy with this selection?(Yes/No)").strip().lower()
        if start_over == "yes":
            time.sleep(2)  
            print(character_name + ' has been saved! :)')
            create_character(character_name, strength, intelligence, charisma, dev_mode)
            break
        if start_over == "no":
            animated_start_over()
            break_outer = True
            break
        else:
            print("Please enter Yes or No")
    if break_outer:
        continue
    
    time.sleep(1)  
    subprocess.run(["python", "adventure_begins.py"])
    break