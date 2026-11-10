# MysteryBox – The Detective Game 🔍🕵️‍♂️

A rich, web-based mystery-solving detective game where players investigate fictional crimes by examining physical and forensic clues, interrogating suspects, exposing contradictory alibis, and issuing formal indictments.

---

## 🌟 Key Features

1. **Three Playable Mystery Cases**:
   - 💎 **Case 1: The Blackwood Sapphire Heist** (*Intermediate*) — A 150-carat royal sapphire vanished from a locked steel vault during a stormy birthday masquerade gala.
   - 🎻 **Case 2: The Cyanide Sonata** (*Hard*) — A ruthless maestro collapses dead mid-rehearsal at the Royal Concert Hall from cyanide-laced tea.
   - 💻 **Case 3: The Silicon Vault Sabotage** (*Expert*) — A quantum AI architect suffocated inside an airtight sub-zero cleanroom with erased optical cores.

2. **Interactive Crime Scene Investigation**:
   - Explore multiple crime scenes per case (Vault, Kennels, Portrait Gallery, Green Room, Cleanroom, etc.).
   - Inspect evidence items with forensic lab reports, microscopic findings, and chemical analysis.

3. **Suspect Interrogation & Contradiction System**:
   - Dynamic dialogue trees for each person of interest.
   - **Phoenix Wright / Sherlock style Contradiction Mechanic**: Present discovered evidence to suspects to expose their lies and shatter their alibis with dramatic audiovisual flair!

4. **Detective's Corkboard & Field Notebook**:
   - Visual investigation pinboard with red pins, classified tags, and dynamically updated alibi statuses.
   - Persistent timestamped pocket notebook to record deductions.

5. **Official Indictment & Verdict Engine**:
   - File formal arrest warrants by selecting the **Prime Suspect**, **Weapon/Method**, and **Decisive Proof**.
   - Cinematic verdict reveals with culprit confessions, detective ratings (up to 1,000 points), and full narrative debriefs.

6. **Audio Engine (Web Audio API)**:
   - Built-in zero-dependency procedural audio synthesizer (typewriter clicks, clue discovery chimes, dramatic contradiction stingers, victory fanfare). Can be toggled on/off at any time.

---

## 🚀 Quickstart & How to Run

### 1. Requirements
- Python 3.10+
- Flask (`pip install flask`)

### 2. Run the Application
From the project folder:
```powershell
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Re-seed Database (Optional)
If you want to reset all cases, notes, and alibi statuses to initial defaults:
```powershell
python seed_data.py
```

### 4. Run Test Suite
```powershell
python test_app.py
```

---

## 📁 Project Directory Structure
```
mysterybox/
│
├── app.py              # Flask server, API routes, interrogation & accusation logic
├── database.py         # SQLite connection and table schemas
├── seed_data.py        # Database seeder with 3 full cases, suspects, clues & dialogues
├── test_app.py         # Automated unit and integration test suite
├── mysterybox.db       # SQLite database file
├── README.md           # Documentation and gameplay guide
│
├── static/
│   ├── css/
│   │   └── style.css   # Noir aesthetic, corkboard styling, responsive layout
│   └── js/
│       └── game.js     # Web Audio synth, interrogation engine, pinboard visualizer
│
└── templates/
    ├── base.html       # Global navigation, audio toggles, toast notifications
    ├── index.html      # Case selection hub, bureau statistics, gameplay manual
    └── case.html       # Full investigation hub: scenes, suspects, corkboard, indictment
```
