# MyRPG Online

This is the backend server for the MyRPG game, built with Flask. It handles login, player stats, inventory, and core game logic.

## Features

* Player registration and login
* Inventory and stats management
* Combat and skill system via API routes

## Setup Instructions

### 1. Install pip for Python 3

```bash
sudo apt update
sudo apt install python3-pip
```

This gives you `pip3`, which is safe to use in virtual environments.

### 2. Install the virtual environment module (if not installed)

```bash
sudo apt install python3-venv
```

Needed to create isolated environments like `my_flask_env`.

### 3. Create a virtual environment

```bash
python3 -m venv my_flask_env
```

This creates a folder `my_flask_env` containing its own Python and pip.

### 4. Activate the virtual environment

```bash
source my_flask_env/bin/activate
```

Your terminal should now show `(my_flask_env)` at the start of the prompt.

### 5. Upgrade pip inside the venv

```bash
python -m pip install --upgrade pip
```

Now your virtual environment has an up-to-date pip.

### 6. Install project dependencies

```bash
python -m pip install -r requirements.txt
```

This installs all packages from `requirements.txt` into the virtual environment, not the system Python.

### 7. Launch the project

```bash
python backend/app.py
```

Then open your browser, create an account on localhost, and log in.

