// -------------------- Global Constants --------------------
const charId = document.body.dataset.charId;

// -------------------- Helper Functions --------------------
function logMessage(msg) {
    const log = document.getElementById('log');
    const p = document.createElement('p');
    p.textContent = msg;
    log.appendChild(p);
    log.scrollTop = log.scrollHeight;
}

function monsterExists() {
    const monsterDiv = document.getElementById('monster');
    const monsterHp = document.getElementById('monster_hp');
    return monsterDiv.style.display === 'block' && parseInt(monsterHp.textContent) > 0;
}

function updateButtons(monster) {
    const attackBtn = document.getElementById('attack_btn');
    const exploreBtn = document.getElementById('explore_btn');
    const runBtn = document.getElementById('run_btn');

    if (monster && monster.hp > 0) {
        attackBtn.style.display = 'inline-block';
        attackBtn.disabled = false;

        exploreBtn.style.display = 'none';
        exploreBtn.disabled = true;

        runBtn.style.display = 'inline-block';
        runBtn.disabled = false;
    } else {
        attackBtn.style.display = 'none';
        attackBtn.disabled = true;

        exploreBtn.style.display = 'inline-block';
        exploreBtn.disabled = false;

        runBtn.style.display = 'none';
        runBtn.disabled = true;
    }
}

function updateMonsterUI(monsterData) {
    const monsterDiv = document.getElementById('monster');
    if (monsterData && monsterData.monster_name) {
        monsterDiv.style.display = 'block';
        document.getElementById('monster_name_placeholder').textContent = monsterData.monster_name;
        document.getElementById('monster_hp').textContent = monsterData.monster_hp;
        document.getElementById('monster_max_hp').textContent = monsterData.monster_max_hp || monsterData.monster_hp;
    } else {
        monsterDiv.style.display = 'none';
        document.getElementById('monster_name_placeholder').textContent = '';
        document.getElementById('monster_hp').textContent = '0';
        document.getElementById('monster_max_hp').textContent = '0';
    }
    updateButtons(monsterData && monsterData.monster_name ? { hp: monsterData.monster_hp } : null);
}

// -------------------- Main Action Function --------------------
function performAction(action) {
    if (action === 'explore' && monsterExists()) {
        logMessage("A monster blocks your path! You must defeat it first.");
        return;
    }
    if (action === 'attack' && !monsterExists()) {
        logMessage("There is no monster to attack!");
        return;
    }

    fetch(`/${action}/${charId}`)
        .then(res => res.json())
        .then(data => {
            if (data.message) logMessage(data.message);

            if (data.player_hp !== undefined) document.querySelectorAll('.player_hp').forEach(el => el.textContent = data.player_hp);
            if (data.gold !== undefined) document.getElementById('gold').textContent = data.gold;
            if (data.player_strength !== undefined) document.getElementById('player_strength').textContent = data.player_strength;

            updateMonsterUI(data);
        })
        .catch(err => {
            console.error("Error performing action:", err);
            logMessage("An error occurred. Check console for details.");
        });
}

function loadShop() {
    fetch(`/shop/${charId}`)
        .then(res => res.json())
        .then(data => {
            const shopList = document.getElementById('shop_items');
            shopList.innerHTML = '';
            data.items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.name} - ${item.cost} gold`;
                li.dataset.itemName = item.name; // add this for click handler
                shopList.appendChild(li);
            });
        })
        .catch(err => console.error("Error loading shop items:", err));
}

// Event delegation to buy items when clicked
document.getElementById('shop_items').addEventListener('click', (event) => {
    const li = event.target;
    if (li.dataset.itemName) {
        buyItem(li.dataset.itemName);
    }
});

function buyItem(itemId) {
    fetch(`/buy_item/${charId}/${itemId}`)
        .then(res => res.json())
        .then(data => {
            logMessage(data.message);
            if (data.gold !== undefined) document.getElementById('gold').textContent = data.gold;
            if (data.player_hp !== undefined) document.querySelectorAll('.player_hp').forEach(el => el.textContent = data.player_hp);
        });
}

// Load shop on page load
document.addEventListener('DOMContentLoaded', () => {
    loadShop();
});


// -------------------- Initialize --------------------
document.addEventListener('DOMContentLoaded', () => {
    fetch(`/current_monster/${charId}`)
        .then(res => res.json())
        .then(data => {
            updateMonsterUI(data.monster_name ? data : null);
        })
        .catch(err => console.error('Error fetching current monster:', err));
});
