/**
 * MYSTERYBOX – THE DETECTIVE GAME
 * Core Interactive Client Engine
 */

// Global Audio Synthesizer (Zero External Dependencies)
class DetectiveSoundEngine {
    constructor() {
        this.ctx = null;
        this.enabled = localStorage.getItem("mysterybox_sound") !== "false";
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    toggle() {
        this.enabled = !this.enabled;
        localStorage.setItem("mysterybox_sound", this.enabled);
        return this.enabled;
    }

    playTone(freq, type, duration, gainVal = 0.1) {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        try {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
            gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch (e) {
            console.log("Audio not allowed yet:", e);
        }
    }

    // Typewriter mechanical keystroke
    typewriter() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(320 + Math.random() * 80, now);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.04);
    }

    // Clue discovery chime
    clueDiscovered() {
        if (!this.enabled) return;
        this.playTone(523.25, 'sine', 0.2, 0.15); // C5
        setTimeout(() => this.playTone(659.25, 'sine', 0.25, 0.15), 100); // E5
        setTimeout(() => this.playTone(783.99, 'sine', 0.4, 0.2), 200); // G5
        setTimeout(() => this.playTone(1046.50, 'sine', 0.6, 0.25), 320); // C6
    }

    // Dramatic contradiction hit ("OBJECTION!")
    contradictionHit() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        // Dramatic minor low chord
        this.playTone(130.81, 'sawtooth', 0.8, 0.3); // C3
        this.playTone(155.56, 'sawtooth', 0.8, 0.3); // Eb3
        this.playTone(196.00, 'sawtooth', 0.9, 0.35); // G3
        setTimeout(() => {
            this.playTone(98.00, 'triangle', 1.0, 0.4); // G2 bass boom
        }, 80);
    }

    // Triumphant victory fanfare
    victory() {
        if (!this.enabled) return;
        const notes = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99];
        notes.forEach((freq, idx) => {
            setTimeout(() => {
                this.playTone(freq, 'triangle', 0.4, 0.2);
            }, idx * 120);
        });
    }

    // Melancholy failure chord
    defeat() {
        if (!this.enabled) return;
        this.playTone(220.00, 'sine', 0.7, 0.2); // A3
        setTimeout(() => this.playTone(207.65, 'sine', 0.8, 0.2), 300); // Ab3
        setTimeout(() => this.playTone(196.00, 'sawtooth', 1.2, 0.25), 650); // G3
    }
}

const sounds = new DetectiveSoundEngine();

// Toast helper
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? 'fa-check-circle' : (type === 'error' ? 'fa-triangle-exclamation' : 'fa-info-circle');
    toast.innerHTML = `<i class="fa-solid ${icon}"></i><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Game State Management
let currentCaseId = null;
let caseData = null;
let activeSuspectId = null;
let brokenAlibis = new Set();
let askedDialogues = new Set();
let discoveredClues = new Set();

// Initialize Case Page
async function initCaseInvestigation(caseId) {
    currentCaseId = caseId;
    try {
        const res = await fetch(`/api/case/${caseId}`);
        if (!res.ok) throw new Error("Failed to load case data");
        caseData = await res.json();
        
        // Populate default discovered clues
        if (caseData.clues) {
            caseData.clues.forEach(c => discoveredClues.add(c.id));
        }

        // Setup sound toggle button
        const soundBtn = document.getElementById('soundToggleBtn');
        if (soundBtn) {
            updateSoundBtnUi(soundBtn);
            soundBtn.addEventListener('click', () => {
                const state = sounds.toggle();
                updateSoundBtnUi(soundBtn);
                showToast(`Audio effects ${state ? 'enabled' : 'muted'}`);
            });
        }

        setupTabs();
        setupScenes();
        setupSuspects();
        setupEvidenceDropdown();
        setupIndictmentForm();
        renderCorkboard();

        // Auto select first suspect
        if (caseData.suspects && caseData.suspects.length > 0) {
            selectSuspect(caseData.suspects[0].id);
        }

    } catch (err) {
        console.error("Initialization error:", err);
        showToast("Error loading case file.", "error");
    }
}

function updateSoundBtnUi(btn) {
    if (sounds.enabled) {
        btn.innerHTML = `<i class="fa-solid fa-volume-high"></i><span>Sound On</span><span class="sound-active-dot"></span>`;
    } else {
        btn.innerHTML = `<i class="fa-solid fa-volume-xmark"></i><span>Sound Off</span>`;
    }
}

// Tab navigation
function setupTabs() {
    const tabs = document.querySelectorAll('.nav-tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            sounds.typewriter();
            const targetId = tab.dataset.tab;
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            const activePane = document.getElementById(targetId);
            if (activePane) activePane.classList.add('active');

            if (targetId === 'tab-corkboard') {
                renderCorkboard();
            }
        });
    });
}

// Scene filtering
function setupScenes() {
    const sceneCards = document.querySelectorAll('.scene-card');
    sceneCards.forEach(card => {
        card.addEventListener('click', () => {
            sounds.typewriter();
            sceneCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            const sceneId = card.dataset.sceneId;
            filterCluesByScene(sceneId);
        });
    });
}

function filterCluesByScene(sceneId) {
    const clueCards = document.querySelectorAll('.clue-card');
    let visibleCount = 0;
    clueCards.forEach(card => {
        if (sceneId === 'all' || card.dataset.sceneId === sceneId) {
            card.style.display = 'flex';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
}

// Suspects list setup
function setupSuspects() {
    const suspectCards = document.querySelectorAll('.suspect-selectable-card');
    suspectCards.forEach(card => {
        card.addEventListener('click', () => {
            sounds.typewriter();
            const suspectId = card.dataset.suspectId;
            selectSuspect(suspectId);
        });
    });
}

function selectSuspect(suspectId) {
    activeSuspectId = suspectId;
    const suspect = caseData.suspects.find(s => s.id === suspectId);
    if (!suspect) return;

    // Highlight card
    document.querySelectorAll('.suspect-selectable-card').forEach(c => {
        c.classList.toggle('active', c.dataset.suspectId === suspectId);
    });

    // Populate Interrogation Profile
    document.getElementById('interrogateAvatar').textContent = getAvatarEmoji(suspect.avatar_svg);
    document.getElementById('interrogateName').textContent = suspect.name;
    document.getElementById('interrogateRole').textContent = `${suspect.role} · ${suspect.age} years old`;
    document.getElementById('interrogateBio').textContent = suspect.bio;
    document.getElementById('interrogateAlibi').textContent = `"${suspect.alibi_claim}"`;

    // Clear dialogue history and load initial statement
    const historyBox = document.getElementById('dialogueHistory');
    historyBox.innerHTML = `
        <div class="dialogue-bubble suspect">
            <span class="bubble-speaker">${suspect.name}</span>
            <div class="bubble-text">"${suspect.initial_statement}"</div>
        </div>
    `;

    // If suspect alibi already broken, add note
    if (brokenAlibis.has(suspectId)) {
        historyBox.innerHTML += `
            <div class="dialogue-bubble suspect contradiction-break">
                <span class="bubble-speaker">${suspect.name} [STRESSED / CORNERED]</span>
                <div class="bubble-text">"You've already exposed my lie! What else do you want from me?!"</div>
            </div>
        `;
    }

    // Populate Question Buttons
    const questionsContainer = document.getElementById('questionsGrid');
    questionsContainer.innerHTML = '';

    const dialogues = (caseData.dialogues && caseData.dialogues[suspectId]) || [];
    if (dialogues.length === 0) {
        questionsContainer.innerHTML = `<span style="color:var(--text-dim);font-size:0.85rem;">No further direct questions available for this person.</span>`;
    } else {
        dialogues.forEach(d => {
            const btn = document.createElement('button');
            btn.className = `btn-question ${askedDialogues.has(d.id) ? 'asked' : ''}`;
            btn.innerHTML = `<i class="fa-regular fa-comment-dots"></i><span>${d.topic}: "${d.question}"</span>`;
            btn.onclick = () => askQuestion(d, btn);
            questionsContainer.appendChild(btn);
        });
    }
}

// Ask question
async function askQuestion(dialogue, btnElement) {
    sounds.typewriter();
    askedDialogues.add(dialogue.id);
    btnElement.classList.add('asked');

    const historyBox = document.getElementById('dialogueHistory');
    
    // Detective bubble
    const detBubble = document.createElement('div');
    detBubble.className = 'dialogue-bubble detective';
    detBubble.innerHTML = `
        <span class="bubble-speaker">Detective</span>
        <div class="bubble-text">${dialogue.question}</div>
    `;
    historyBox.appendChild(detBubble);

    try {
        const res = await fetch('/api/interrogate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dialogue_id: dialogue.id })
        });
        const data = await res.json();

        // Suspect bubble
        const suspect = caseData.suspects.find(s => s.id === dialogue.suspect_id);
        const suspBubble = document.createElement('div');
        suspBubble.className = 'dialogue-bubble suspect';
        suspBubble.innerHTML = `
            <span class="bubble-speaker">${suspect ? suspect.name : 'Suspect'}</span>
            <div class="bubble-text">"${data.answer}"</div>
        `;
        historyBox.appendChild(suspBubble);
        historyBox.scrollTop = historyBox.scrollHeight;

        if (data.unlocked_clue) {
            sounds.clueDiscovered();
            showToast(`New Clue Unlocked: ${data.unlocked_clue.title}!`, 'success');
            discoveredClues.add(data.unlocked_clue.id);
            setupEvidenceDropdown();
            renderCorkboard();
        }

    } catch (e) {
        console.error(e);
    }
}

// Setup Evidence Present Dropdown
function setupEvidenceDropdown() {
    const dropdown = document.getElementById('presentEvidenceSelect');
    if (!dropdown || !caseData || !caseData.clues) return;

    dropdown.innerHTML = '<option value="">-- Pick a Clue to Catch Their Lie --</option>';
    caseData.clues.forEach(clue => {
        if (discoveredClues.has(clue.id)) {
            const opt = document.createElement('option');
            opt.value = clue.id;
            opt.textContent = `[${clue.category}] ${clue.title}`;
            dropdown.appendChild(opt);
        }
    });
}

// Present evidence to suspect
async function presentEvidence() {
    if (!activeSuspectId) {
        showToast("Click on a person to talk to first.", "error");
        return;
    }

    const dropdown = document.getElementById('presentEvidenceSelect');
    const clueId = dropdown.value;
    if (!clueId) {
        showToast("Pick a clue from the dropdown first.", "error");
        return;
    }

    try {
        const res = await fetch('/api/present-evidence', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ suspect_id: activeSuspectId, clue_id: clueId })
        });
        const data = await res.json();
        const historyBox = document.getElementById('dialogueHistory');

        if (data.is_contradiction) {
            // Big Dramatic contradiction!
            sounds.contradictionHit();
            brokenAlibis.add(activeSuspectId);

            // Add callout bubble
            const detBubble = document.createElement('div');
            detBubble.className = 'dialogue-bubble detective';
            detBubble.innerHTML = `
                <span class="bubble-speaker">Detective [CAUGHT YOU IN A LIE!]</span>
                <div class="bubble-text" style="background:#b91c1c;">${data.callout_text}</div>
            `;
            historyBox.appendChild(detBubble);

            // Suspect breakdown bubble
            const suspBubble = document.createElement('div');
            suspBubble.className = 'dialogue-bubble suspect contradiction-break';
            suspBubble.innerHTML = `
                <span class="bubble-speaker">${data.suspect_name} [PANICKING]</span>
                <div class="bubble-text">"${data.suspect_response}"</div>
            `;
            historyBox.appendChild(suspBubble);
            historyBox.scrollTop = historyBox.scrollHeight;

            // Mark card with broken alibi badge
            const suspectCard = document.querySelector(`.suspect-selectable-card[data-suspect-id="${activeSuspectId}"]`);
            if (suspectCard && !suspectCard.querySelector('.alibi-broken-stamp')) {
                const stamp = document.createElement('div');
                stamp.className = 'alibi-broken-stamp';
                stamp.textContent = 'CAUGHT IN A LIE!';
                suspectCard.querySelector('.suspect-card-info').appendChild(stamp);
            }

            showToast(`CAUGHT IN A LIE! ${data.suspect_name}'s story is ruined!`, 'success');
            renderCorkboard();

        } else {
            // Dismissed
            sounds.typewriter();
            const detBubble = document.createElement('div');
            detBubble.className = 'dialogue-bubble detective';
            detBubble.innerHTML = `
                <span class="bubble-speaker">Detective</span>
                <div class="bubble-text">${data.callout_text}</div>
            `;
            historyBox.appendChild(detBubble);

            const suspBubble = document.createElement('div');
            suspBubble.className = 'dialogue-bubble suspect';
            suspBubble.innerHTML = `
                <span class="bubble-speaker">${data.suspect_name}</span>
                <div class="bubble-text">${data.suspect_response}</div>
            `;
            historyBox.appendChild(suspBubble);
            historyBox.scrollTop = historyBox.scrollHeight;
            showToast("That clue didn't prove they were lying. Try another clue!", "error");
        }

    } catch (e) {
        console.error(e);
        showToast("Error presenting evidence.", "error");
    }
}

// Corkboard Pinboard Visualizer
function renderCorkboard() {
    const grid = document.getElementById('corkboardGrid');
    if (!grid || !caseData) return;

    grid.innerHTML = '';

    // Suspects pinned
    caseData.suspects.forEach(s => {
        const isBroken = brokenAlibis.has(s.id);
        const card = document.createElement('div');
        card.className = `pin-card suspect-pin ${isBroken ? 'contradiction-pin' : ''}`;
        card.innerHTML = `
            <div class="pin-card-title">${getAvatarEmoji(s.avatar_svg)} ${s.name}</div>
            <div class="pin-card-body">
                <strong>Role:</strong> ${s.role}<br>
                <strong>What they said:</strong> ${s.alibi_claim}<br>
                ${isBroken ? '<strong style="color:var(--accent-crimson);">⚠️ CAUGHT IN A LIE!</strong>' : '<span style="color:var(--text-dim);">Status: Suspect</span>'}
            </div>
        `;
        grid.appendChild(card);
    });

    // Key Clues Pinned
    caseData.clues.forEach(c => {
        if (discoveredClues.has(c.id)) {
            const card = document.createElement('div');
            card.className = 'pin-card clue-pin';
            card.innerHTML = `
                <div class="pin-card-title"><i class="fa-solid ${c.icon}"></i> ${c.title}</div>
                <div class="pin-card-body">
                    <strong>Type:</strong> ${c.category}<br>
                    ${c.short_desc}<br>
                    <div style="margin-top:0.4rem;font-size:0.75rem;color:#475569;">${c.full_analysis}</div>
                </div>
            `;
            grid.appendChild(card);
        }
    });
}

// Clue Magnifier Modal
function openClueMagnifier(clueId) {
    sounds.clueDiscovered();
    const clue = caseData.clues.find(c => c.id === clueId);
    if (!clue) return;

    document.getElementById('modalClueTitle').innerHTML = `<i class="fa-solid ${clue.icon}"></i> ${clue.title}`;
    document.getElementById('modalClueCategory').textContent = `Category: ${clue.category} Evidence`;
    document.getElementById('modalClueDesc').textContent = clue.short_desc;
    document.getElementById('modalClueAnalysis').textContent = clue.full_analysis;

    const modal = document.getElementById('clueMagnifierModal');
    if (modal) modal.classList.add('active');
}

function closeClueMagnifier() {
    sounds.typewriter();
    const modal = document.getElementById('clueMagnifierModal');
    if (modal) modal.classList.remove('active');
}

// Indictment & Accusation Modal
function openAccusationModal() {
    sounds.typewriter();
    const modal = document.getElementById('accusationModal');
    if (modal) modal.classList.add('active');
}

function closeAccusationModal() {
    sounds.typewriter();
    const modal = document.getElementById('accusationModal');
    if (modal) modal.classList.remove('active');
}

function setupIndictmentForm() {
    if (!caseData) return;

    const suspectSelect = document.getElementById('accusedSuspectSelect');
    const weaponSelect = document.getElementById('accusedWeaponSelect');
    const proofSelect = document.getElementById('accusedProofSelect');

    if (suspectSelect) {
        suspectSelect.innerHTML = '<option value="">-- Choose Person --</option>';
        caseData.suspects.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.id;
            opt.textContent = `${s.name} (${s.role})`;
            suspectSelect.appendChild(opt);
        });
    }

    if (weaponSelect) {
        weaponSelect.innerHTML = '<option value="">-- Choose Weapon or Method --</option>';
        caseData.clues.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.id;
            opt.textContent = `[${c.category}] ${c.title}`;
            weaponSelect.appendChild(opt);
        });
    }

    if (proofSelect) {
        proofSelect.innerHTML = '<option value="">-- Choose Clue That Proves Guilt --</option>';
        caseData.clues.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.id;
            opt.textContent = `[${c.category}] ${c.title}`;
            proofSelect.appendChild(opt);
        });
    }
}

// Submit Accusation
async function submitIndictment(event) {
    if (event) event.preventDefault();

    const suspectId = document.getElementById('accusedSuspectSelect').value;
    const weaponId = document.getElementById('accusedWeaponSelect').value;
    const proofId = document.getElementById('accusedProofSelect').value;
    const motiveText = document.getElementById('accusedMotiveText').value;

    if (!suspectId || !weaponId || !proofId) {
        showToast("Please choose the person, method, and proof clue.", "error");
        return;
    }

    try {
        const res = await fetch('/api/accuse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                case_id: currentCaseId,
                suspect_id: suspectId,
                weapon_clue_id: weaponId,
                proof_clue_id: proofId,
                motive_statement: motiveText
            })
        });

        const data = await res.json();
        closeAccusationModal();

        // Render cinematic verdict
        renderVerdictModal(data);

    } catch (e) {
        console.error(e);
        showToast("Error filing indictment.", "error");
    }
}

function renderVerdictModal(data) {
    const verdictModal = document.getElementById('verdictModal');
    const header = document.getElementById('verdictHeader');
    const icon = document.getElementById('verdictIcon');
    const title = document.getElementById('verdictTitle');
    const scoreBadge = document.getElementById('verdictScoreBadge');
    const confessionQuote = document.getElementById('verdictConfessionQuote');
    const narrative = document.getElementById('verdictNarrative');

    // Clean previous classes
    header.className = `verdict-header ${data.verdict_type}`;
    title.textContent = data.title;
    scoreBadge.textContent = `DETECTIVE RATING: ${data.score} / 1000 PTS`;
    confessionQuote.textContent = data.confession;
    narrative.textContent = data.full_narrative;

    if (data.is_flawless) {
        sounds.victory();
        icon.className = 'fa-solid fa-trophy verdict-icon-stamp';
    } else if (data.verdict_type === 'partial') {
        sounds.defeat();
        icon.className = 'fa-solid fa-gavel verdict-icon-stamp';
    } else {
        sounds.defeat();
        icon.className = 'fa-solid fa-handcuffs verdict-icon-stamp';
    }

    verdictModal.classList.add('active');
}

function closeVerdictModal() {
    sounds.typewriter();
    document.getElementById('verdictModal').classList.remove('active');
}

// Detective Notebook
async function addDetectiveNote() {
    const input = document.getElementById('noteTextInput');
    const text = input.value.trim();
    if (!text) return;

    sounds.typewriter();
    try {
        const res = await fetch('/api/notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ case_id: currentCaseId, note_text: text })
        });
        const data = await res.json();
        if (data.success) {
            input.value = '';
            const list = document.getElementById('notesList');
            const noteEl = document.createElement('div');
            noteEl.className = 'note-item';
            noteEl.textContent = data.note_text;
            list.insertBefore(noteEl, list.firstChild);
            showToast("Note added to case file.");
        }
    } catch (e) {
        console.error(e);
    }
}

// Emoji avatars
function getAvatarEmoji(name) {
    const map = {
        'butler': '🤵',
        'art_dealer': '🕵️‍♀️',
        'nephew': '💼',
        'socialite': '👑',
        'violinist': '🎻',
        'stage_manager': '🎭',
        'pianist': '🎹',
        'patron': '🎩',
        'engineer': '👩‍💻',
        'security': '👮‍♂️',
        'sysadmin': '🛠️',
        'ceo': '👔'
    };
    return map[name] || '👤';
}

/* ============================================================
   WELCOME SCREEN & CASES SHOWCASE ENGINE (Homepage Interactivity)
   ============================================================ */
let caseIdsList = [];
let currentShowcaseIndex = 0;

function openCasesView(shouldScroll = true) {
    sounds.clueDiscovered();
    const welcomeSection = document.getElementById('welcomeSection');
    const casesSection = document.getElementById('casesSection');
    if (!welcomeSection || !casesSection) return;

    welcomeSection.style.display = 'none';
    casesSection.style.display = 'block';
    window.location.hash = 'cases';

    if (shouldScroll) {
        casesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function openWelcomeView(shouldScroll = true) {
    sounds.typewriter();
    const welcomeSection = document.getElementById('welcomeSection');
    const casesSection = document.getElementById('casesSection');
    if (!welcomeSection || !casesSection) return;

    casesSection.style.display = 'none';
    welcomeSection.style.display = 'block';
    window.location.hash = 'welcome';

    if (shouldScroll) {
        welcomeSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function switchCaseShowcase(caseId, index = -1) {
    sounds.typewriter();
    if (index >= 0) {
        currentShowcaseIndex = index;
    } else {
        const found = caseIdsList.indexOf(caseId);
        if (found !== -1) currentShowcaseIndex = found;
    }

    // Update active tab buttons
    document.querySelectorAll('.case-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.id === `caseTab_${caseId}`);
    });

    // Update active showcase card
    document.querySelectorAll('.case-showcase-card').forEach(card => {
        card.classList.toggle('active', card.id === `showcase_${caseId}`);
    });

    // Update index counter
    const counter = document.getElementById('caseIndexCounter');
    if (counter && caseIdsList.length > 0) {
        counter.textContent = `Case ${currentShowcaseIndex + 1} of ${caseIdsList.length}`;
    }
}

function cyclePrevCase() {
    if (caseIdsList.length === 0) return;
    currentShowcaseIndex = (currentShowcaseIndex - 1 + caseIdsList.length) % caseIdsList.length;
    switchCaseShowcase(caseIdsList[currentShowcaseIndex], currentShowcaseIndex);
}

function cycleNextCase() {
    if (caseIdsList.length === 0) return;
    currentShowcaseIndex = (currentShowcaseIndex + 1) % caseIdsList.length;
    switchCaseShowcase(caseIdsList[currentShowcaseIndex], currentShowcaseIndex);
}

// Interactive Detective Magnifying Glass & Artwork Inspector
function setupDetectiveSearchInteractive() {
    const artFrame = document.getElementById('detectiveArtFrame');
    const magnifier = document.getElementById('artInteractiveMagnifier');
    const popup = document.getElementById('artCluePopup');
    const popupText = document.getElementById('artCluePopupText');
    const nodes = document.querySelectorAll('.evidence-node');

    let popupTimeout = null;

    if (artFrame && magnifier) {
        artFrame.addEventListener('mousemove', (e) => {
            const rect = artFrame.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            magnifier.style.left = `${x}px`;
            magnifier.style.top = `${y}px`;
        });

        // Evidence node clicks
        nodes.forEach(node => {
            node.addEventListener('click', (e) => {
                e.stopPropagation();
                sounds.clueDiscovered();
                const info = node.getAttribute('data-info') || "Evidence node inspected.";
                if (popup && popupText) {
                    popupText.textContent = info;
                    popup.classList.add('active');
                    clearTimeout(popupTimeout);
                    popupTimeout = setTimeout(() => {
                        popup.classList.remove('active');
                    }, 3500);
                }
            });
        });
    }

    // Support legacy floor clues if present
    const legacyScene = document.getElementById('detectiveSearchScene');
    const armLens = document.getElementById('detectiveArmLens');
    const legacyPopup = document.getElementById('sceneCluePopup');
    const legacyPopupText = document.getElementById('sceneClueText');
    const floorClues = document.querySelectorAll('.floor-clue');

    if (legacyScene && armLens) {
        legacyScene.addEventListener('mousemove', (e) => {
            const rect = legacyScene.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            const dx = mouseX - 140;
            const dy = mouseY - 180;
            let angle = Math.atan2(dy, dx) * (180 / Math.PI);
            angle = Math.max(-20, Math.min(45, angle));
            const distance = Math.min(520, Math.max(80, Math.sqrt(dx * dx + dy * dy)));
            const translateX = (distance - 80) * 0.8;
            armLens.style.animation = 'none';
            armLens.style.transform = `rotate(${angle.toFixed(1)}deg) translate(${translateX.toFixed(1)}px, 0px)`;
        });

        legacyScene.addEventListener('mouseleave', () => {
            armLens.style.animation = 'searchPatrol 7s ease-in-out infinite alternate';
            armLens.style.transform = '';
        });

        floorClues.forEach(clue => {
            clue.addEventListener('click', (e) => {
                e.stopPropagation();
                sounds.clueDiscovered();
                const text = clue.getAttribute('data-clue') || "Evidence located!";
                if (legacyPopup && legacyPopupText) {
                    legacyPopupText.textContent = text;
                    legacyPopup.classList.add('active');
                    setTimeout(() => legacyPopup.classList.remove('active'), 2800);
                }
            });
        });
    }
}

// Initialize Homepage
function initHomepage() {
    const welcomeSection = document.getElementById('welcomeSection');
    if (!welcomeSection) return; // Not on index page

    // Sound button setup on index page
    const soundBtn = document.getElementById('soundToggleBtn');
    if (soundBtn) {
        updateSoundBtnUi(soundBtn);
        soundBtn.addEventListener('click', () => {
            const state = sounds.toggle();
            updateSoundBtnUi(soundBtn);
            showToast(`Audio effects ${state ? 'enabled' : 'muted'}`);
        });
    }

    // Collect case IDs from tabs
    const tabBtns = document.querySelectorAll('.case-tab-btn');
    caseIdsList = Array.from(tabBtns).map(btn => btn.id.replace('caseTab_', ''));

    // Setup interactive search scene
    setupDetectiveSearchInteractive();

    // Check URL hash
    if (window.location.hash === '#cases') {
        openCasesView(false);
    } else {
        openWelcomeView(false);
    }

    // Keyboard arrow navigation between cases
    window.addEventListener('keydown', (e) => {
        const casesSection = document.getElementById('casesSection');
        if (casesSection && casesSection.style.display !== 'none') {
            if (e.key === 'ArrowLeft') cyclePrevCase();
            if (e.key === 'ArrowRight') cycleNextCase();
        }
    });

    // Hook up navbar links
    const navWelcomeBtn = document.getElementById('navWelcomeBtn');
    if (navWelcomeBtn) {
        navWelcomeBtn.addEventListener('click', (e) => {
            if (document.getElementById('welcomeSection')) {
                e.preventDefault();
                openWelcomeView();
            }
        });
    }

    const navCasesBtn = document.getElementById('navCasesBtn');
    if (navCasesBtn) {
        navCasesBtn.addEventListener('click', (e) => {
            if (document.getElementById('casesSection')) {
                e.preventDefault();
                openCasesView();
            }
        });
    }
}

// Auto-run on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHomepage);
} else {
    initHomepage();
}

