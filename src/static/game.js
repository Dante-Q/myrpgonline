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

function updateButtons() {
    const attackBtn = document.getElementById('attack_btn');
    const exploreBtn = document.getElementById('explore_btn');
    const runBtn = document.getElementById('run_btn');

    if (monsterExists()) {
        attackBtn.disabled = false;
        exploreBtn.disabled = true;
        runBtn.style.display = 'inline-block';
    } else {
        attackBtn.disabled = true;
        exploreBtn.disabled = false;
        runBtn.style.display = 'none';
    }
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
            // Log message
            if (data.message) logMessage(data.message);

            // Update player stats
            if (data.player_hp !== undefined) document.getElementById('player_hp').textContent = data.player_hp;
            if (data.gold !== undefined) document.getElementById('gold').textContent = data.gold;

            // Handle monster spawn/update
            const monsterDiv = document.getElementById('monster');
            if (data.monster_name) {
                monsterDiv.style.display = 'block';
                document.getElementById('monster_name_placeholder').textContent = data.monster_name;
                document.getElementById('monster_hp').textContent = data.monster_hp;
                document.getElementById('monster_max_hp').textContent = data.monster_max_hp;
            } else if (data.monster_hp !== undefined) {
                document.getElementById('monster_hp').textContent = data.monster_hp;
            }

            // Hide monster if defeated
            if (data.monster_hp === 0) {
                setTimeout(() => {
                    monsterDiv.style.display = 'none';
                    document.getElementById('monster_name_placeholder').textContent = '';
                    document.getElementById('monster_hp').textContent = '0';
                    document.getElementById('monster_max_hp').textContent = '0';
                    updateButtons();
                }, 2000);
            }

            // Update buttons dynamically
            updateButtons();
        })
        .catch(err => {
            console.error("Error performing action:", err);
            logMessage("An error occurred. Check console for details.");
        });
}

// -------------------- Initialize --------------------
document.addEventListener('DOMContentLoaded', updateButtons);
